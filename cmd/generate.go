package cmd

import (
	"strings"

	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
)

var generateCmd = &cobra.Command{
	Use:   "generate",
	Short: "Generate images for the defined covers",
	Args:  cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		mode, _ := cmd.Flags().GetString("mode")
		renderMode, validRenderMode := rendering.PlanModes[mode]
		if !validRenderMode {
			log.Fatal().Str("mode", mode).Msg("invalid mode")
		}

		plan, err := rendering.PlanRender(coverPath, statePath, renderMode)
		checkError(err, "error planning render")

		err = rendering.ExecutePlan(plan)
		checkError(err, "error executing render plan")
	},
}

func init() {
	rootCmd.AddCommand(generateCmd)

	generateCmd.Flags().String("mode", "changed", "mode to use for generating covers")
	_ = generateCmd.RegisterFlagCompletionFunc(
		"mode",
		func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
			var matchingModes []string
			for mode := range rendering.PlanModes {
				if strings.HasPrefix(mode, toComplete) {
					matchingModes = append(matchingModes, mode)
				}
			}

			return matchingModes, cobra.ShellCompDirectiveNoFileComp
		},
	)
}
