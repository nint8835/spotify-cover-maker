# generate

Generate images for a given cover definition file.

## Usage

```bash
spotify-cover-maker generate
```

## Options

### `--mode`

The mode to use for selecting which images to generate. Must be one of the following:

| Mode                | Description                                                                                                                                                         |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `all`               | Generate images for all defined covers.                                                                                                                             |
| `changed` (default) | Generate images for all covers that have changed since the last time they were generated, and for all new covers which haven't had images generated for previously. |
| `missing`           | Generate images for new covers and covers for which the image file is missing.                                                                                      |

### `--covers-path`

Path to a cover definition file (see ***TODO: insert link to covers docs***).
 
Defaults to `./covers.yaml`

### `--state-path`

Path to where the cover state should be stored. Is used to keep track of which covers have already been generated.

Defaults to `./.scm_state.yaml`