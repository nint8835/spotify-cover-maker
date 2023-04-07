# covers.yaml

All configuration & definition of covers is done through a cover definition file, by default `covers.yaml`.

This file is a YAML file which containing the following keys:

| Key           | Description                                                                                                    | Required | Default    |
|---------------|----------------------------------------------------------------------------------------------------------------|----------|------------|
| `covers`      | A list of [cover definitions](/config/covers).                                                                 | Yes      |            |
| `output_path` | Path to the folder that the generated covers should be placed in. This folder is created if it does not exist. | No       | `./covers` |
