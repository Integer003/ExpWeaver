# SwanLab Integration Tools

This module provides comprehensive integration with the SwanLab experiment tracking platform.

## Overview

The SwanLab integration tools allow you to connect to SwanLab's API and retrieve experiment data, workspace information, and metrics for analysis.

## Available Tools

### `user_workspace(input_api, workspace_name=None)`

Get information about user's workspaces.

**Parameters:**
- `input_api` (str): Your SwanLab API key
- `workspace_name` (str, optional): Specific workspace name to filter

**Returns:**
- `list[dict]`: List of workspace information dictionaries


### `user_workspace_project(input_api, workspaces=None, project_name=None)`

Get project information from workspaces.

**Parameters:**
- `input_api` (str): Your SwanLab API key
- `workspaces` (list, optional): List of workspace information
- `project_name` (str, optional): Specific project name to filter

**Returns:**
- `list[dict]`: List of project information dictionaries


### `user_project_expe(input_api, projects_list, expe_name=None)`

Get experiment information from projects.

**Parameters:**
- `input_api` (str): Your SwanLab API key
- `projects_list` (list): List of project information
- `expe_name` (str, optional): Specific experiment name to filter

**Returns:**
- `dict[str, list[dict]]`: Dictionary mapping project names to experiment lists


### `get_expe_metrics(input_api, expe_dict)`

Extract metrics data from experiments.

**Parameters:**
- `input_api` (str): Your SwanLab API key
- `expe_dict` (dict): Dictionary of experiment information

**Returns:**
- `dict[str, str]`: Dictionary mapping experiment IDs to CSV-formatted metrics

### `swanlab_pipeline(input_api, workspace_name=None, project_name=None, expe_name=None)`

Complete pipeline to extract experiment information with fallback handling.

**Parameters:**
- `input_api` (str): Your SwanLab API key
- `workspace_name` (str, optional): Target workspace name
- `project_name` (str, optional): Target project name  
- `expe_name` (str, optional): Target experiment name

**Returns:**
- `dict[str, dict[str, str]]`: Complete experiment metrics data


## Getting Started

1. **Obtain API Key**: Get your SwanLab API key from your account settings
2. **Start the Server**: Run `python run_swanlab_tools.py`
3. **Use the Tools**: Connect via MCP client and call the available tools. You should pass your SwanLba API key to the agent by prompt or global environment.

## Configuration

### MCP Client Setup

```json
{
  "mcpServers": {
    "swanlab-tools": {
      "command": "python",
      "args": ["/path/to/swanlab_api_tool.py"]
    }
  }
}
```
