package rendering

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"path"

	"github.com/pterm/pterm"
	"github.com/rs/zerolog/log"

	"github.com/nint8835/spotify-cover-maker/pkg/templating"
)

var PlanModes = map[string]PlanMode{
	"all":     PlanModeAll,
	"missing": PlanModeMissing,
	"changed": PlanModeChanged,
}

type PlanMode int

const (
	PlanModeAll PlanMode = iota
	PlanModeMissing
	PlanModeChanged
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

	ProgressBar *pterm.ProgressbarPrinter
}

func PlanRender(configPath, statePath string, mode PlanMode) (RenderPlan, error) {
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

		plannedRender := PlannedRender{
			Template: templateDefinition,
			Cover:    cover,
		}

		coverPath := path.Join(configFile.OutputPath, cover.Meta.Name+".png")

		switch mode {
		case PlanModeAll:
			log.Debug().Msgf("Adding cover %s to render plan as mode is all", cover.Meta.Name)
			plan.PlannedRenders = append(plan.PlannedRenders, plannedRender)
		case PlanModeMissing:
			if !hasExistingState {
				log.Debug().Msgf(
					"Adding cover %s to render plan as mode is missing and cover does not appear in state",
					cover.Meta.Name,
				)
				plan.PlannedRenders = append(plan.PlannedRenders, plannedRender)
			} else if _, err := os.Stat(coverPath); os.IsNotExist(err) {
				log.Debug().Msgf(
					"Adding cover %s to render plan as mode is missing and cover does not exist on disk",
					cover.Meta.Name,
				)
				plan.PlannedRenders = append(plan.PlannedRenders, plannedRender)
			} else {
				log.Debug().Msgf("Skipping cover %s because it already exists", cover.Meta.Name)
			}
		case PlanModeChanged:
			if !hasExistingState {
				log.Debug().Msgf(
					"Adding cover %s to render plan as mode is changed and cover does not appear in state",
					cover.Meta.Name,
				)
				plan.PlannedRenders = append(plan.PlannedRenders, plannedRender)
			} else if existingState != newState {
				log.Debug().Msgf(
					"Adding cover %s to render plan as mode is changed and cover is out of date",
					cover.Meta.Name,
				)
				plan.PlannedRenders = append(plan.PlannedRenders, plannedRender)
			} else {
				log.Debug().Msgf("Skipping cover %s because it is up to date", cover.Meta.Name)
			}
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

	var progressBar *pterm.ProgressbarPrinter

	if plan.ProgressBar != nil {
		plan.ProgressBar = plan.ProgressBar.WithTotal(len(plan.PlannedRenders)).WithTitle("Rendering covers")
		progressBar, _ = plan.ProgressBar.Start()
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

		if progressBar != nil {
			progressBar.Increment()
		}
	}

	err := templating.SaveStateFile(plan.StatePath, plan.State)
	if err != nil {
		return fmt.Errorf("error saving state file: %w", err)
	}

	return nil
}
