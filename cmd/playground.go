package cmd

import (
	"bytes"
	"context"
	"os"

	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
	"github.com/nint8835/spotify-cover-maker/pkg/templating"
)

var playgroundCmd = &cobra.Command{
	Use:  "playground",
	Args: cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		err := templating.LoadTemplates()
		checkError(err, "error loading templates")

		var testBuf bytes.Buffer
		err = templating.Templates["gradient"].Execute(&testBuf, map[string]any{
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
