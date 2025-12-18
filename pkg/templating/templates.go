package templating

import (
	"crypto/sha512"
	"embed"
	"encoding/json"
	"fmt"
	"io"
	"text/template"

	"github.com/Masterminds/sprig/v3"
	"github.com/rs/zerolog/log"
	"gopkg.in/yaml.v3"
)

//go:embed templates
var templateFs embed.FS

var Templates map[string]*template.Template

type TemplateDefinition interface {
	// ID returns a unique identifier for the template.
	// The value should match the filename for the template, without the .svg extension.
	ID() string

	// DecodeConfig decodes the config for the template from the given yaml.Node.
	// The yaml.Node will be a mapping node.
	DecodeConfig(value *yaml.Node) (any, error)

	// TemplateContext returns the data to be passed to the template for a given cover.
	TemplateContext(cover Cover) any

	// RequiredFonts returns a list of font names required by the template for the given cover.
	RequiredFonts(cover Cover) []string
}

var templateDefinitions = []TemplateDefinition{
	&GradientTemplate{},
}

var TemplateDefinitionMap = map[string]TemplateDefinition{}

func init() {
	Templates = make(map[string]*template.Template)

	for _, t := range templateDefinitions {
		TemplateDefinitionMap[t.ID()] = t

		templateFileName := getTemplateFilename(t)
		templateBytes, err := templateFs.ReadFile(templateFileName)
		if err != nil {
			log.Fatal().Err(err).Str("template", t.ID()).Msg("Error reading template file")
		}

		parsedTemplate, err := template.New(t.ID()).Funcs(sprig.FuncMap()).Parse(string(templateBytes))
		if err != nil {
			log.Fatal().Err(err).Str("template", t.ID()).Msg("Error parsing template")
		}

		Templates[t.ID()] = parsedTemplate
	}
}

func getTemplateFilename(template TemplateDefinition) string {
	return fmt.Sprintf("templates/%s.svg", template.ID())
}

func GetTemplateContextHash(templateContext any) string {
	hash := sha512.New()

	templateContextJson, _ := json.Marshal(templateContext)
	hash.Write(templateContextJson)

	return fmt.Sprintf("%x", hash.Sum(nil))
}

func GetTemplateHash(template TemplateDefinition) string {
	hash := sha512.New()

	templateFile, _ := templateFs.Open(getTemplateFilename(template))
	_, _ = io.Copy(hash, templateFile)

	return fmt.Sprintf("%x", hash.Sum(nil))
}
