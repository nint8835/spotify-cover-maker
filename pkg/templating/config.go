package templating

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

func mergeStructs(structs ...any) (map[string]any, error) {
	merged := make(map[string]any)

	for _, s := range structs {
		sYaml, err := yaml.Marshal(s)
		if err != nil {
			return nil, fmt.Errorf("error marshalling struct: %w", err)
		}

		err = yaml.Unmarshal(sYaml, &merged)
		if err != nil {
			return nil, fmt.Errorf("error unmarshalling struct: %w", err)
		}
	}

	return merged, nil
}

type CoverMeta struct {
	Name     string `yaml:"name"`
	Template string `yaml:"template"`
}

type Cover struct {
	Meta CoverMeta
	Data any
}

func (c *Cover) UnmarshalYAML(value *yaml.Node) error {
	var meta CoverMeta
	err := value.Decode(&meta)
	if err != nil {
		return fmt.Errorf("error decoding cover meta: %w", err)
	}

	c.Meta = meta

	templateDefinition, valid := TemplateDefinitionMap[meta.Template]
	if !valid {
		return fmt.Errorf("invalid template %s", meta.Template)
	}

	data, err := templateDefinition.DecodeConfig(value)
	if err != nil {
		return fmt.Errorf("error decoding cover data: %w", err)
	}

	c.Data = data

	return nil
}

func (c Cover) MarshalYAML() (interface{}, error) {
	return mergeStructs(c.Meta, c.Data)
}

type Config struct {
	OutputPath string  `yaml:"output_path,omitempty"`
	Covers     []Cover `yaml:"covers,omitempty"`
}

func LoadConfig(path string) (*Config, error) {
	configFile, err := os.OpenFile(path, os.O_RDONLY, 0o644)
	if err != nil {
		return nil, fmt.Errorf("error opening config file: %w", err)
	}

	var config Config
	err = yaml.NewDecoder(configFile).Decode(&config)
	if err != nil {
		return nil, fmt.Errorf("error decoding config file: %w", err)
	}

	return &config, nil
}
