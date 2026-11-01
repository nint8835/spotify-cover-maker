package templating

import (
	"crypto/md5"
	"encoding/binary"
	"image/color"
	"math/rand"

	"gopkg.in/yaml.v3"

	"github.com/nint8835/spotify-cover-maker/pkg/utils"
)

type GradientTemplateContext struct {
	GradientTemplateConfig

	Stops []GradientStop
}

type GradientTemplateConfig struct {
	HeadingLines *[]string `yaml:"heading_lines,omitempty"`
	Title        *string   `yaml:"title,omitempty"`
	Subtitle     *string   `yaml:"subtitle,omitempty"`
	Font         *string   `yaml:"font,omitempty"`
}

type GradientTemplate struct{}

func (t *GradientTemplate) ID() string {
	return "gradient"
}

func (t *GradientTemplate) DecodeConfig(value *yaml.Node) (any, error) {
	var data GradientTemplateConfig
	err := value.Decode(&data)
	if err != nil {
		return data, err
	}

	if data.HeadingLines == nil {
		data.HeadingLines = &[]string{"Favourite", "Songs"}
	}

	if data.Font == nil {
		data.Font = utils.PointerTo("IBM Plex Sans")
	}

	return data, nil
}

func (t *GradientTemplate) TemplateContext(cover Cover) any {
	data := cover.Data.(GradientTemplateConfig)

	sum := md5.Sum([]byte(cover.Meta.Name))
	intSum := binary.BigEndian.Uint64(sum[:])

	random := rand.New(rand.NewSource(int64(intSum)))

	r1 := random.Intn(225)
	g1 := random.Intn(225)
	b1 := random.Intn(225)
	r2 := random.Intn(225)
	g2 := random.Intn(225)
	b2 := random.Intn(225)

	return GradientTemplateContext{
		GradientTemplateConfig: data,

		Stops: oklchGradientStops(
			color.RGBA{R: uint8(r1), G: uint8(g1), B: uint8(b1), A: 255},
			color.RGBA{R: uint8(r2), G: uint8(g2), B: uint8(b2), A: 255},
		),
	}
}

func (t *GradientTemplate) RequiredFonts(cover Cover) []string {
	data := cover.Data.(GradientTemplateConfig)
	return []string{*data.Font}
}
