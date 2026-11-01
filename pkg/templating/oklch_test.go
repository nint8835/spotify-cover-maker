package templating //nolint:testpackage // Verify gradient samples without exposing implementation details.

import (
	"fmt"
	"image/color"
	"math"
	"testing"

	"github.com/lucasb-eyer/go-colorful"
)

func TestOKLCHGradientStops(t *testing.T) {
	tests := []struct {
		name       string
		start, end color.RGBA
		midpoint   string
	}{
		{"black to white", color.RGBA{A: 255}, color.RGBA{R: 255, G: 255, B: 255, A: 255}, "rgb(99,99,99)"},
		{"red to blue shorter hue", color.RGBA{R: 255, A: 255}, color.RGBA{B: 255, A: 255}, "rgb(186,0,194)"},
		{"identical", color.RGBA{R: 42, G: 100, B: 180, A: 255},
			color.RGBA{R: 42, G: 100, B: 180, A: 255}, "rgb(42,100,180)"},
		{"grey to red", color.RGBA{R: 128, G: 128, B: 128, A: 255},
			color.RGBA{R: 255, A: 255}, "rgb(198,99,86)"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			stops := oklchGradientStops(tt.start, tt.end)
			if len(stops) != 129 {
				t.Fatalf("got %d stops, want 129", len(stops))
			}
			for index, endpoint := range map[int]color.RGBA{0: tt.start, len(stops) - 1: tt.end} {
				want := fmt.Sprintf("rgb(%d,%d,%d)", endpoint.R, endpoint.G, endpoint.B)
				if stops[index].Colour != want {
					t.Errorf("endpoint %d = %s, want %s", index, stops[index].Colour, want)
				}
			}
			if got := stops[len(stops)/2].Colour; got != tt.midpoint {
				t.Errorf("midpoint = %s, want %s", got, tt.midpoint)
			}
			for i, stop := range stops {
				if stop.Offset != float64(i)/128 {
					t.Fatalf("stop %d has incorrect offset %f", i, stop.Offset)
				}
			}
			reversed := oklchGradientStops(tt.end, tt.start)
			for i, stop := range stops {
				if stop.Colour != reversed[len(stops)-1-i].Colour {
					t.Fatalf("gradient differs when reversed at stop %d", i)
				}
			}
		})
	}
}

func TestOKLCHGradientHueWrap(t *testing.T) {
	start := color.RGBAModel.Convert(colorful.OkLch(0.6, 0.08, 170)).(color.RGBA)
	end := color.RGBAModel.Convert(colorful.OkLch(0.6, 0.08, 190)).(color.RGBA)
	stops := oklchGradientStops(start, end)
	var midpoint color.RGBA
	_, err := fmt.Sscanf(stops[len(stops)/2].Colour, "rgb(%d,%d,%d)", &midpoint.R, &midpoint.G, &midpoint.B)
	if err != nil {
		t.Fatal(err)
	}
	midpoint.A = 255
	converted, _ := colorful.MakeColor(midpoint)
	_, _, hue := converted.OkLch()
	if math.Abs(math.Abs(hue)-180) > 2 {
		t.Fatalf("midpoint hue = %f degrees, want near 180 along shorter arc", hue)
	}
}
