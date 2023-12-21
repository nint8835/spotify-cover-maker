package rendering

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"path"

	"github.com/rs/zerolog/log"

	"github.com/nint8835/spotify-cover-maker/pkg/templating"
)

type PlannedRender struct {
	Template templating.TemplateDefinition
	Cover    templating.Cover
}

type RenderPlan struct {
	ConfigPath string
	StatePath  string

	Config templating.Config
	State  templating.StateFile

	PlannedRenders []PlannedRender
}

func PlanRender(configPath, statePath string) (RenderPlan, error) {
	plan := RenderPlan{
		ConfigPath:     configPath,
		StatePath:      statePath,
		PlannedRenders: make([]PlannedRender, 0),
	}

	// TODO: Should this be moved out of this function?
	configFile, err := templating.LoadConfig(configPath)
	if err != nil {
		return plan, fmt.Errorf("error loading config: %w", err)
	}
	stateFile, err := templating.LoadStateFile(statePath)
	if err != nil {
		return plan, fmt.Errorf("error loading state: %w", err)
	}

	plan.Config = *configFile
	plan.State = stateFile

	for _, cover := range configFile.Covers {
		log.Debug().Msgf("Planning render for cover %s", cover.Meta.Name)

		existingState, hasExistingState := stateFile.GeneratedCovers[cover.Meta.Name]

		templateDefinition := templating.TemplateDefinitionMap[cover.Meta.Template]
		newState := templating.ComputeState(templateDefinition, cover)

		// TODO: Implement different render plan modes
		if !hasExistingState {
			log.Debug().Msgf("Adding cover %s to render plan as it does not exist", cover.Meta.Name)
			plan.PlannedRenders = append(plan.PlannedRenders, PlannedRender{
				Template: templateDefinition,
				Cover:    cover,
			})
		} else if existingState != newState {
			log.Debug().Msgf("Adding cover %s to render plan as it is out of date", cover.Meta.Name)
			plan.PlannedRenders = append(plan.PlannedRenders, PlannedRender{
				Template: templateDefinition,
				Cover:    cover,
			})
		} else {
			log.Debug().Msgf("Skipping cover %s because it already exists and is up to date", cover.Meta.Name)
		}
	}

	return plan, nil
}

func ExecutePlan(plan RenderPlan) error {
	if _, err := os.Stat(plan.Config.OutputPath); os.IsNotExist(err) {
		err = os.MkdirAll(plan.Config.OutputPath, 0o755)
		if err != nil {
			return fmt.Errorf("error creating output directory: %w", err)
		}
	}

	for _, plannedRender := range plan.PlannedRenders {
		renderPath := path.Join(plan.Config.OutputPath, plannedRender.Cover.Meta.Name+".png")

		templateContext := plannedRender.Template.TemplateContext(plannedRender.Cover)

		var svgData bytes.Buffer
		err := templating.Templates[plannedRender.Cover.Meta.Template].Execute(&svgData, templateContext)
		if err != nil {
			return fmt.Errorf("error executing template for cover %s: %w", plannedRender.Cover.Meta.Name, err)
		}

		// TODO: Figure out what to do about contexts
		pngData, err := SvgToPng(context.Background(), svgData.Bytes())
		if err != nil {
			return fmt.Errorf("error converting SVG to PNG for cover %s: %w", plannedRender.Cover.Meta.Name, err)
		}

		pngFile, err := os.Create(renderPath)
		if err != nil {
			return fmt.Errorf("error opening PNG file for cover %s: %w", plannedRender.Cover.Meta.Name, err)
		}
		_, err = pngFile.Write(pngData)
		if err != nil {
			return fmt.Errorf("error writing PNG file for cover %s: %w", plannedRender.Cover.Meta.Name, err)
		}

		plan.State.GeneratedCovers[plannedRender.Cover.Meta.Name] = templating.ComputeState(
			plannedRender.Template,
			plannedRender.Cover,
		)
	}

	err := templating.SaveStateFile(plan.StatePath, plan.State)
	if err != nil {
		return fmt.Errorf("error saving state file: %w", err)
	}

	return nil
}
