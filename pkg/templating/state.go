package templating

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
)

type State struct {
	DataHash     string `yaml:"data_hash"`
	TemplateHash string `yaml:"template_hash"`
}

type StateFile struct {
	GeneratedCovers map[string]State `yaml:"generated_covers"`
}

func LoadStateFile(path string) (StateFile, error) {
	var stateFile StateFile

	file, err := os.OpenFile(path, os.O_RDONLY, 0o644)
	if err != nil {
		if os.IsNotExist(err) {
			return StateFile{GeneratedCovers: map[string]State{}}, nil
		}

		return stateFile, fmt.Errorf("error opening state file: %w", err)
	}

	err = yaml.NewDecoder(file).Decode(&stateFile)
	if err != nil {
		return stateFile, fmt.Errorf("error decoding state file: %w", err)
	}

	return stateFile, nil
}

func SaveStateFile(path string, stateFile StateFile) error {
	file, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("error creating state file: %w", err)
	}

	err = yaml.NewEncoder(file).Encode(stateFile)
	if err != nil {
		return fmt.Errorf("error encoding state file: %w", err)
	}

	return nil
}

func ComputeState(template TemplateDefinition, cover Cover) State {
	return State{
		DataHash:     GetTemplateContextHash(template.TemplateContext(cover)),
		TemplateHash: GetTemplateHash(template),
	}
}
