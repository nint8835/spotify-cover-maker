package templating_test

import (
	"bytes"
	"context"
	"encoding/xml"
	"image/png"
	"reflect"
	"strings"
	"testing"

	"gopkg.in/yaml.v3"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
	"github.com/nint8835/spotify-cover-maker/pkg/templating"
)

func TestGradientTemplateRendering(t *testing.T) {
	var cover templating.Cover
	if err := yaml.Unmarshal([]byte("name: OKLCH test\ntemplate: gradient\n"), &cover); err != nil {
		t.Fatal(err)
	}
	definition := templating.TemplateDefinitionMap[cover.Meta.Template]
	data := definition.TemplateContext(cover).(templating.GradientTemplateContext)
	if !reflect.DeepEqual(data, definition.TemplateContext(cover)) {
		t.Fatal("same cover must generate deterministic gradient stops")
	}
	var svg bytes.Buffer
	if err := templating.Templates[definition.ID()].Execute(&svg, data); err != nil {
		t.Fatal(err)
	}
	var document struct {
		Stops []struct {
			Offset float64 `xml:"offset,attr"`
			Style  string  `xml:"style,attr"`
		} `xml:"defs>linearGradient>stop"`
	}
	if err := xml.Unmarshal(svg.Bytes(), &document); err != nil {
		t.Fatal(err)
	}
	if len(document.Stops) != 129 {
		t.Fatalf("SVG contains %d stops, want 129", len(document.Stops))
	}
	for i, stop := range document.Stops {
		if stop.Offset != data.Stops[i].Offset || !strings.Contains(stop.Style, "stop-color:"+data.Stops[i].Colour+";") {
			t.Fatalf("SVG stop %d does not match generated stop", i)
		}
	}
	imageBytes, err := rendering.SvgToPng(context.Background(), svg.Bytes(), nil)
	if err != nil {
		t.Fatal(err)
	}
	image, err := png.Decode(bytes.NewReader(imageBytes))
	if err != nil {
		t.Fatal(err)
	}
	if image.Bounds().Dx() != 1000 || image.Bounds().Dy() != 1000 {
		t.Fatalf("unexpected image size: %v", image.Bounds())
	}
	// Background pixels away from text must differ along the gradient.
	if image.At(500, 500) == image.At(900, 800) {
		t.Fatal("rendered gradient has a flat background")
	}
}
