package cmd

import (
	"fmt"

	"github.com/pterm/pterm"
	"github.com/spf13/cobra"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
	"github.com/nint8835/spotify-cover-maker/pkg/templating"
)

var fontsCmd = &cobra.Command{
	Use:   "fonts",
	Short: "List available fonts",
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		config, err := templating.LoadConfig(coverPath)
		checkError(err, "error loading config")

		fonts, err := rendering.ListFonts(config.FontPath)
		checkError(err, "error listing fonts")

		for _, font := range fonts {
			pterm.DefaultSection.WithBottomPadding(0).Println(font.Name)
			var source string
			if font.Embedded {
				source = "Bundled"
			} else {
				source = "User-provided"
			}
			pterm.Println(pterm.Gray(source) + "\n")

			pterm.Println(font.Copyright + "\n" + font.License + "\n")

			pterm.Println(pterm.Cyan("Variants:"))

			var variantListItems []pterm.BulletListItem

			for index, variant := range font.Variants {
				variantListItems = append(
					variantListItems,
					pterm.BulletListItem{
						Text: fmt.Sprintf("%s (%s)", variant, font.Paths[index]),
					},
				)
			}

			_ = pterm.DefaultBulletList.WithItems(variantListItems).Render()
		}
	},
}

func init() {
	rootCmd.AddCommand(fontsCmd)
}
