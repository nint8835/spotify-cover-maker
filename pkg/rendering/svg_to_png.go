package rendering

import (
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/kanrichan/resvg-go"
	"github.com/rs/zerolog/log"
)

func loadFonts(fontdb *resvg.FontDB) error {
	log.Debug().Msg("Loading fonts to render SVG...")

	dirEntries, _ := os.ReadDir("fonts")
	for _, dirEntry := range dirEntries {
		if !strings.HasSuffix(dirEntry.Name(), ".ttf") {
			continue
		}

		fontPath := "fonts/" + dirEntry.Name()

		log.Debug().Str("fontPath", fontPath).Msg("Loading font...")

		fontBytes, err := os.ReadFile(fontPath)
		if err != nil {
			return fmt.Errorf("error reading font file %s: %w", fontPath, err)
		}

		err = fontdb.LoadFontData(fontBytes)
		if err != nil {
			return fmt.Errorf("error loading font data for file %s: %w", fontPath, err)
		}
	}

	log.Debug().Msg("Finished loading fonts")

	return nil
}

func SvgToPng(ctx context.Context, svg []byte) ([]byte, error) {
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

	err = loadFonts(fontdb)
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
