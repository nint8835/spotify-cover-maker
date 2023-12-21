package templating

import (
	"gopkg.in/yaml.v3"
)

type TemplateDefinition interface {
	// ID returns a unique identifier for the template.
	// The value should match the filename for the template, without the .svg extension.
	ID() string

	// DecodeConfig decodes the config for the template from the given yaml.Node.
	// The yaml.Node will be a mapping node.
	DecodeConfig(value *yaml.Node) (any, error)

	// TemplateContext returns the data to be passed to the template for a given cover.
	TemplateContext(cover Cover) any
}

var templateDefinitions = []TemplateDefinition{
	&GradientTemplate{},
}

var TemplateDefinitionMap = map[string]TemplateDefinition{}

func init() {
	for _, t := range templateDefinitions {
		TemplateDefinitionMap[t.ID()] = t
	}
}
