# Gradient

![Gradient cover example](./assets/gradient.png)

## Options

!!! note
    
    Required fields are indicated with a **bold** name.

| Name          | Description                                                                                                                                                                    | Type            | Default                  |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|--------------------------|
| **name**      | A unique name to identify this cover. Will be used to generate the filename, as well as a seed for the background colours.                                                     | `str`           |                          |
| **template**  | Template to use. Set to `gradient` for this template.                                                                                                                          | `str`           |                          |
| heading_lines | The lines that make up the text in the top left of the cover. Each item will be placed on it's own line.                                                                       | `list[str]`     | `["Favourite", "Songs"]` |
| title         | An optional large label to add to the bottom left of the cover.                                                                                                                | `Optional[str]` | `None`                   |
| subtitle      | An optional smaller label to add below the title. title must be provided when using this option.                                                                               | `Optional[str]` | `None`                   |
| font          | Name of the font to use for text of the covers. Must be a valid font on your system, and will fall back to your system's default sans-serif font if the given font is invalid. | `str`           | `sans-serif`             |
