package cmd

import (
	"github.com/rs/zerolog/log"
)

func checkError(err error, message string) {
	if err != nil {
		log.Fatal().Err(err).Msg(message)
	}
}
