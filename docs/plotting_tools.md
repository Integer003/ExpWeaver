# Data Visualization Tools

This module provides powerful plotting and chart generation capabilities for CSV data using matplotlib, seaborn, and cartopy.

## Overview

The plotting server generates high-quality visualizations from CSV data with support for multiple plot types and customizable styling.

## Available Tools

### `generate_plot(csv_data, plot_type="line", json_kwargs="None", save_route="None")`

Generate plots from CSV data with extensive customization options.

**Parameters:**
- `csv_data` (str): CSV data as a string
- `plot_type` (str): Type of plot ("line", "bar", "pie", "worldmap")
- `json_kwargs` (str): JSON string with additional plotting parameters
- `save_route` (str): Optional file path to save the generated plot

**Returns:**
- `tuple[TextContent, ImageContent]`: Success message and base64-encoded PNG image

## Supported Plot Types

### 1. Line Plots (`plot_type="line"`)

Perfect for time series data and trend visualization.

**Supported Parameters:**
- `x` (str): Column name for x-axis
- `y` (str): Column name for y-axis  
- `hue` (str): Column name for color encoding
- `title` (str): Plot title
- `xlabel` (str): X-axis label
- `ylabel` (str): Y-axis label

### 2. Bar Plots (`plot_type="bar"`)

Ideal for categorical data comparison.

**Supported Parameters:**
- `x` (str): Column name for x-axis (categories)
- `y` (str): Column name for y-axis (values)
- `hue` (str): Column name for color grouping
- `title` (str): Plot title
- `xlabel` (str): X-axis label
- `ylabel` (str): Y-axis label


### 3. Pie Charts (`plot_type="pie"`)

Great for showing proportions and percentages.


### 4. World Maps (`plot_type="worldmap"`)

Visualize geographic coordinate data on world maps.

**Required Columns:**
- Latitude: `lat`, `latitude`, or `y`
- Longitude: `lon`, `lng`, `long`, `longitude`, or `x`

**Supported Parameters:**
- `s` (int): Marker size (default: 50)
- `c` (str): Marker color (default: "red")
- `alpha` (float): Transparency 0-1 (default: 0.7)
- `marker` (str): Marker style (default: "o")


## Features

### Automatic Label Rotation

The system automatically rotates axis labels when:
- More than 8 labels on an axis
- Any label longer than 15 characters  
- Average label length > 10 characters

### High-Quality Output

- **Resolution**: 300 DPI for publication-quality images
- **Format**: PNG with transparency support
- **Size**: Configurable figure dimensions
- **Layout**: Automatic tight layout optimization

### Error Validation

- Checks for empty DataFrames
- Validates against NaN/null values
- Ensures proper data types for plotting
- Provides clear error messages

## Configuration

### Server Setup

```bash
# Start the plotting server
python run_plotting_server.py

# With custom settings
python run_plotting_server.py --log-level DEBUG --reload --transport http
```

### MCP Client Configuration

```json
{
  "mcpServers": {
    "plotting-tools": {
      "command": "python",
      "args": ["/path/to/run_plotting_server.py",
      "custom_args"]
    }
  }
}
```

### Environment Variables

```bash
# Optional: Configure plot settings
export PLOT_DPI=300
export PLOT_FIGURE_SIZE="(10, 6)"
```

