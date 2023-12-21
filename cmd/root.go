package cmd

import (
	"fmt"
	"os"
	"strings"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/spf13/cobra"
)

var logLevel string
var coverPath string
var statePath string

var rootCmd = &cobra.Command{
	Use:   "spotify-cover-maker",
	Short: "spotify-cover-maker is a tool for generating Spotify cover images",
}

func initLogging() {
	parsedLevel, err := zerolog.ParseLevel(logLevel)
	checkError(err, "failed to parse log level")

	zerolog.SetGlobalLevel(parsedLevel)

	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
}

func init() {
	rootCmd.PersistentFlags().StringVar(&logLevel, "log-level", "info", "log level to use for output")
	_ = rootCmd.RegisterFlagCompletionFunc(
		"log-level",
		func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
			allLevels := []string{"debug", "info", "warn", "error", "fatal", "disabled"}

			var matchingLevels []string

			for _, level := range allLevels {
				if strings.HasPrefix(level, toComplete) {
					matchingLevels = append(matchingLevels, level)
				}
			}

			return matchingLevels, cobra.ShellCompDirectiveNoFileComp
		},
	)

	rootCmd.PersistentFlags().StringVar(&coverPath, "cover-path", "covers.yaml", "path to the cover config file")
	rootCmd.PersistentFlags().StringVar(&statePath, "state-path", ".scm_state.yaml", "path to the state file")

	cobra.OnInitialize(initLogging)
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		_, _ = fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
