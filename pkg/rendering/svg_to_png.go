package rendering

import (
	"context"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"strings"

	"github.com/kanrichan/resvg-go"
	"github.com/rs/zerolog/log"
	"golang.org/x/image/font/sfnt"
)

// https://learn.microsoft.com/en-us/typography/opentype/spec/name#name-ids
const nameIDTypographicFamily = 16
const nameIDTypographicSubfamily = 17

type Font struct {
	Name      string
	Embedded  bool
	FS        fs.FS
	License   string
	Copyright string
	Variants  []string
	Paths     []string
}

func listFsFonts(fs fs.ReadDirFS, embedded bool) ([]Font, error) {
	families := make(map[string]*Font)

	dirEntries, err := fs.ReadDir(".")
	if err != nil {
		return nil, fmt.Errorf("error reading custom font directory: %w", err)
	}

	for _, dirEntry := range dirEntries {
		if !strings.HasSuffix(dirEntry.Name(), ".ttf") {
			continue
		}

		fontPath := dirEntry.Name()

		log.Debug().Str("font_path", fontPath).Msg("Loading font...")

		fontFile, err := fs.Open(fontPath)
		if err != nil {
			return nil, fmt.Errorf("error opening font file %s: %w", fontPath, err)
		}

		fontBytes, err := io.ReadAll(fontFile)
		if err != nil {
			return nil, fmt.Errorf("error reading font file %s: %w", fontPath, err)
		}

		sfntObj, err := sfnt.Parse(fontBytes)
		if err != nil {
			return nil, fmt.Errorf("error parsing font file %s: %w", fontPath, err)
		}

		family, err := sfntObj.Name(nil, nameIDTypographicFamily)
		if err != nil {
			if errors.Is(err, sfnt.ErrNotFound) {
				family, err = sfntObj.Name(nil, sfnt.NameIDFamily)
				if err != nil {
					return nil, fmt.Errorf("error getting font family for file %s: %w", fontPath, err)
				}
			} else {
				return nil, fmt.Errorf("error getting font family for file %s: %w", fontPath, err)
			}
		}

		subfamily, err := sfntObj.Name(nil, nameIDTypographicSubfamily)
		if err != nil {
			if errors.Is(err, sfnt.ErrNotFound) {
				subfamily, err = sfntObj.Name(nil, sfnt.NameIDSubfamily)
				if err != nil {
					return nil, fmt.Errorf("error getting font subfamily for file %s: %w", fontPath, err)
				}
			} else {
				return nil, fmt.Errorf("error getting font subfamily for file %s: %w", fontPath, err)
			}
		}

		license, err := sfntObj.Name(nil, sfnt.NameIDLicense)
		if err != nil {
			return nil, fmt.Errorf("error getting font license for file %s: %w", fontPath, err)
		}

		copyright, err := sfntObj.Name(nil, sfnt.NameIDCopyright)
		if err != nil {
			return nil, fmt.Errorf("error getting font copyright for file %s: %w", fontPath, err)
		}

		existingFamily, valid := families[family]
		if !valid {
			existingFamily = &Font{
				Name:      family,
				Embedded:  embedded,
				FS:        fs,
				License:   license,
				Copyright: copyright,
				Variants:  make([]string, 0),
				Paths:     make([]string, 0),
			}

			families[family] = existingFamily
		}

		existingFamily.Paths = append(existingFamily.Paths, fontPath)
		existingFamily.Variants = append(existingFamily.Variants, subfamily)
	}

	fontsArray := make([]Font, 0)
	for _, font := range families {
		fontsArray = append(fontsArray, *font)
	}

	return fontsArray, nil
}

func ListFonts(customFontPath *string) ([]Font, error) {
	fonts := make([]Font, 0)

	if customFontPath != nil {
		customFonts, err := listFsFonts(os.DirFS(*customFontPath).(fs.ReadDirFS), false)
		if err != nil {
			return nil, fmt.Errorf("error listing custom fonts: %w", err)
		}

		fonts = append(fonts, customFonts...)
	}

	return fonts, nil
}

func loadFonts(fontdb *resvg.FontDB, customFontPath *string) error {
	log.Debug().Msg("Loading fonts to render SVG...")

	fonts, err := ListFonts(customFontPath)
	if err != nil {
		return fmt.Errorf("error listing fonts: %w", err)
	}

	for _, font := range fonts {
		log.Debug().Str("font", font.Name).Msg("Loading font...")

		for i, variant := range font.Variants {
			log.Debug().Str("font", font.Name).Str("variant", variant).Msg("Loading font variant...")

			fontPath := font.Paths[i]

			fontFile, err := font.FS.Open(fontPath)
			if err != nil {
				return fmt.Errorf("error opening font file %s: %w", fontPath, err)
			}

			fontBytes, err := io.ReadAll(fontFile)
			if err != nil {
				return fmt.Errorf("error reading font file %s: %w", fontPath, err)
			}

			err = fontdb.LoadFontData(fontBytes)
			if err != nil {
				return fmt.Errorf("error adding font from data for file %s: %w", fontPath, err)
			}
		}
	}

	return nil
}

func SvgToPng(ctx context.Context, svg []byte, customFontPath *string) ([]byte, error) {
	worker, err := resvg.NewDefaultWorker(ctx)
	if err != nil {
		return nil, fmt.Errorf("error creating resvg worker: %w", err)
	}
	defer worker.Close()

	fontdb, err := worker.NewFontDBDefault()
	if err != nil {
		return nil, fmt.Errorf("error creating font database: %w", err)
	}
	defer fontdb.Close()

	err = loadFonts(fontdb, customFontPath)
	if err != nil {
		return nil, fmt.Errorf("error loading fonts: %w", err)
	}

	tree, err := worker.NewTreeFromData(svg, &resvg.Options{})
	if err != nil {
		return nil, fmt.Errorf("error parsing svg tree: %w", err)
	}
	defer tree.Close()

	width, height, err := tree.GetSize()
	if err != nil {
		return nil, fmt.Errorf("error getting svg size: %w", err)
	}

	pixmap, err := worker.NewPixmap(uint32(width), uint32(height))
	if err != nil {
		return nil, fmt.Errorf("error creating pixmap: %w", err)
	}
	defer pixmap.Close()

	err = tree.ConvertText(fontdb)
	if err != nil {
		return nil, fmt.Errorf("error converting text: %w", err)
	}

	err = tree.Render(resvg.TransformIdentity(), pixmap)
	if err != nil {
		return nil, fmt.Errorf("error rendering svg: %w", err)
	}

	png, err := pixmap.EncodePNG()
	if err != nil {
		return nil, fmt.Errorf("error encoding png: %w", err)
	}

	return png, nil
}
