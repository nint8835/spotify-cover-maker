package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/nint8835/spotify-cover-maker/pkg/rendering"
)

var playgroundCmd = &cobra.Command{
	Use:  "playground",
	Args: cobra.NoArgs,
	Run: func(cmd *cobra.Command, args []string) {
		plan, err := rendering.PlanRender("covers.yaml", ".scm_state.yaml", rendering.PlanModeMissing)
		checkError(err, "error planning render")

		fmt.Printf("%#+v\n", plan)

		err = rendering.ExecutePlan(plan)
		checkError(err, "error executing render plan")
	},
}

func init() {
	rootCmd.AddCommand(playgroundCmd)
}
