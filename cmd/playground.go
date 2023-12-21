package cmd

import (
	"bytes"
	"context"
	"fmt"
	"os"

	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"
	"gopkg.in/yaml.v3"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
	"github.com/nint8835/spotify-cover-maker/pkg/templating"
	"github.com/nint8835/spotify-cover-maker/pkg/utils"
)

var playgroundCmd = &cobra.Command{
	Use:  "playground",
	Args: cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		configFile, err := templating.LoadConfig("covers.yaml")
		checkError(err, "error loading config")

		fmt.Printf("%#+v\n", configFile)

		err = yaml.NewEncoder(os.Stdout).Encode(configFile)
		checkError(err, "error encoding config")

		err = templating.LoadTemplates()
		checkError(err, "error loading templates")

		testCoverDef := templating.Cover{
			Meta: templating.CoverMeta{
				Name:     "2023-12",
				Template: "gradient",
			},
			Data: templating.GradientTemplateConfig{
				HeadingLines: &[]string{"Favourite", "Songs"},
				Title:        utils.PointerTo("December"),
				Subtitle:     utils.PointerTo("2023"),
				Font:         utils.PointerTo("IBM Plex Sans"),
			},
		}

		templateContext := templating.TemplateDefinitionMap["gradient"].TemplateContext(testCoverDef)

		var testBuf bytes.Buffer
		err = templating.Templates["gradient"].Execute(&testBuf, templateContext)
		if err != nil {
			panic(err)
		}

		testSvgFile, _ := os.Create("test.svg")
		testSvgFile.Write(testBuf.Bytes())

		png, err := rendering.SvgToPng(context.Background(), testBuf.Bytes())
		if err != nil {
			panic(err)
		}

		pngFile, _ := os.Create("test.png")
		pngFile.Write(png)

		log.Info().Msg("Testing cover generated")
	},
}

func init() {
	rootCmd.AddCommand(playgroundCmd)
}
