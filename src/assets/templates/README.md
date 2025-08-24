# PowerPoint Templates

This directory is for storing PowerPoint template files (.pptx or .potx) that can be used with the MCP server.

## Usage

1. Place your template files in this directory
2. Use the `create_presentation_from_template` tool with the template filename
3. The server will automatically search for templates in this directory

## Supported Formats

- `.pptx` - PowerPoint presentation files
- `.potx` - PowerPoint template files

## Example

```python
# Create presentation from template
result = create_presentation_from_template("company_template.pptx")
```

The server will search for templates in:
- Current directory
- ./templates/ (this directory)
- ./assets/
- ./resources/
