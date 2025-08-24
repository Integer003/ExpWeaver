# Experiment Drawing Tools

This module provides specialized visualization tools for machine learning experiment data with advanced plotting capabilities.

## Overview

The drawing tools focus on creating publication-quality visualizations for ML experiments, including accuracy/loss curves, comparison heatmaps, and error band plots.

## Available Tools

### `plot_experiment_acc_loss(metrics_csv, columns=None, save_route="None")`

Generate experiment plots for accuracy, loss, and other metrics over training steps.

**Parameters:**
- `metrics_csv` (str): CSV string containing experiment metrics
- `columns` (list, optional): Specific columns to plot (auto-detected if None)
- `save_route` (str, optional): File path to save the plot

**Returns:**
- `dict`: Contains markdown and base64 file data for the generated plot


### `plot_contrast_experiments(summary_dict_list, param_names=None, save_route="None")`

Create heatmaps comparing multiple experiments across different parameters.

**Parameters:**
- `summary_dict_list` (list[dict]): List of experiment summary dictionaries
- `param_names` (list[str], optional): Parameters to compare (auto-detected if None)
- `save_route` (str, optional): File path to save the heatmap

**Returns:**
- `dict`: Contains markdown and base64 file data for the heatmap


### `plot_with_errorband_mcp(csv_list, x, y, labels=None, ci=-1, save_route="None")`

Generate line plots with error bands for comparing multiple experimental groups.

**Parameters:**
- `csv_list` (list[str]): List of CSV strings, each representing a group of experiments
- `x` (str): Column name for x-axis (typically "step" or "epoch")
- `y` (str): Column name for y-axis (metric to plot)
- `labels` (list[str], optional): Labels for each group
- `ci` (int/str): Confidence interval type (-1 for std dev, int for bootstrap CI, 0 for none)
- `save_route` (str, optional): File path to save the plot

**Returns:**
- `dict`: Contains markdown and base64 file data for the plot

## Features

### Automatic Data Processing

1. **Step Generation**: Automatically adds step numbers if not present
2. **Numeric Detection**: Auto-detects numeric columns for plotting
3. **Data Validation**: Ensures proper CSV format and structure

### Professional Styling

- **High DPI**: 150 DPI for publication-quality output
- **Clean Layout**: Automatic tight layout optimization
- **Grid Lines**: Optional grid lines for better readability
- **Color Palettes**: Uses seaborn's default palettes for consistency

### Multiple Output Formats

Each tool returns data in multiple formats:
- **Markdown**: Direct embedding in notebooks/documents
- **Base64**: For programmatic access and download
- **File Save**: Optional direct file saving

## Configuration

### MCP Client Setup

```json
{
  "mcpServers": {
    "drawing-tools": {
      "command": "python",
      "args": ["/path/to/run_drawing_tools.py"]
    }
  }
}
```

### Styling Customization

Modify the plotting functions to customize appearance:

```python
# In plot_experiment_acc_loss
sns.set_theme()  # Use seaborn themes
plt.style.use('seaborn-v0_8')  # Alternative matplotlib styles
```

