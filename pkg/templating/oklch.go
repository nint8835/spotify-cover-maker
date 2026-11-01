package templating

import (
	"fmt"
	"image/color"

	"github.com/lucasb-eyer/go-colorful"
)

// GradientStop is an SVG-compatible sRGB sample of an OKLCH gradient.
type GradientStop struct {
	Offset float64
	Colour string
}

func oklchGradientStops(start, end color.RGBA) []GradientStop {
	const segments = 128
	// Template endpoints are opaque sRGB colours.
	from, _ := colorful.MakeColor(start)
	to, _ := colorful.MakeColor(end)

	stops := make([]GradientStop, segments+1)
	for i := range stops {
		t := float64(i) / segments
		// BlendOkLch handles shorter hue interpolation, achromatic endpoints,
		// and clipping colours outside the sRGB gamut.
		r, g, b := from.BlendOkLch(to, t).RGB255()
		// Preserve the original endpoints exactly, independent of conversion rounding.
		switch i {
		case 0:
			r, g, b = start.R, start.G, start.B
		case segments:
			r, g, b = end.R, end.G, end.B
		}
		stops[i] = GradientStop{
			Offset: t,
			Colour: fmt.Sprintf("rgb(%d,%d,%d)", r, g, b),
		}
	}
	return stops
}
