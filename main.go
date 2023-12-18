package main

import (
	"bytes"
	"context"
	_ "embed"
	"os"
	"strings"
	"text/template"

	"github.com/Masterminds/sprig/v3"
	"github.com/kanrichan/resvg-go"
)

const testingTemplateText = `<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        {{ range $index, $headingLine := .HeadingLines }}
        <text x="104.209px" y="{{ addf 182.254 (mul 125 $index)}}px" style="font-family:'{{ $.Font }}', sans-serif;font-weight:800;font-size:125px;fill:white;">{{ $headingLine }}</text>
        {{ end }}
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        {{ if .Title }}
        <text x="69.495px" y="{{ if .Subtitle }}918.468px{{ else }}978.7014px{{ end }}" style="font-family:'{{ .Font }}', sans-serif;font-weight:800;font-size:100px;fill:white;">{{ .Title }}</text>
        {{ end }}
        {{ if .Subtitle }}
        <text x="69.495px" y="1001.8px" style="font-family:'{{ .Font }}', sans-serif;font-weight:800;font-size:75px;fill:white;">{{ .Subtitle }}</text>
        {{ end }}
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:{{ .Colour1 }};stop-opacity:1" />
            <stop offset="1" style="stop-color:{{ .Colour2 }};stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>`

var testingTemplate = template.Must(template.New("testing").Funcs(sprig.FuncMap()).Parse(testingTemplateText))

func main() {
	var testBuf bytes.Buffer
	err := testingTemplate.Execute(&testBuf, map[string]any{
		"HeadingLines": []string{"Favourite", "Songs"},
		"Title":        "December",
		"Subtitle":     "2023",
		"Colour1":      "#ff0000",
		"Colour2":      "#0000ff",
		"Font":         "IBM Plex Sans",
	})
	if err != nil {
		panic(err)
	}

	testSvgFile, _ := os.Create("test.svg")
	testSvgFile.Write(testBuf.Bytes())

	worker, err := resvg.NewDefaultWorker(context.Background())
	if err != nil {
		panic(err)
	}
	defer worker.Close()

	fontdb, err := worker.NewFontDBDefault()
	if err != nil {
		panic(err)
	}
	defer fontdb.Close()

	dirEntries, _ := os.ReadDir("fonts")
	for _, dirEntry := range dirEntries {
		if !strings.HasSuffix(dirEntry.Name(), ".ttf") {
			continue
		}

		fontBytes, _ := os.ReadFile("fonts/" + dirEntry.Name())
		fontdb.LoadFontData(fontBytes)
	}

	tree, err := worker.NewTreeFromData(testBuf.Bytes(), &resvg.Options{})
	if err != nil {
		panic(err)
	}
	defer tree.Close()

	width, height, err := tree.GetSize()
	if err != nil {
		panic(err)
	}

	pixmap, err := worker.NewPixmap(uint32(width), uint32(height))
	if err != nil {
		panic(err)
	}
	defer pixmap.Close()

	tree.ConvertText(fontdb)
	tree.Render(resvg.TransformIdentity(), pixmap)

	png, _ := pixmap.EncodePNG()

	pngFile, _ := os.Create("test.png")
	pngFile.Write(png)
}
