package templating

import (
	"embed"
	"fmt"
	"strings"
	"text/template"

	"github.com/Masterminds/sprig/v3"
	"github.com/rs/zerolog/log"
)

//go:embed templates
var templateFs embed.FS

var Templates map[string]*template.Template

func LoadTemplates() error {
	if Templates != nil {
		return nil
	}

	Templates = make(map[string]*template.Template)

	templateFiles, _ := templateFs.ReadDir("templates")
	for _, dirEntry := range templateFiles {
		log.Debug().Str("template", dirEntry.Name()).Msg("Loading template...")

		templateName := strings.TrimSuffix(dirEntry.Name(), ".svg")

		templateBytes, _ := templateFs.ReadFile("templates/" + dirEntry.Name())
		parsedTemplate, err := template.New(templateName).Funcs(sprig.FuncMap()).Parse(string(templateBytes))
		if err != nil {
			return fmt.Errorf("error parsing template %s: %w", templateName, err)
		}

		Templates[templateName] = parsedTemplate
	}

	return nil
}
