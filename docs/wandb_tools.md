# Weights & Biases Integration Tools

This module provides comprehensive integration with Weights & Biases (W&B) for experiment tracking and management.

## Overview

The W&B integration tools enable you to interact with your W&B projects, runs, and artifacts programmatically through MCP.

## Available Tools

### `wandb_login(api_key)`

Login to W&B with your API key.

**Parameters:**
- `api_key` (str): Your W&B API key

**Returns:**
- None (prints success message)


### `list_projects(entity=None)`

Get list of projects in W&B.

**Parameters:**
- `entity` (str, optional): Entity name (username or team)

**Returns:**
- `list[dict]`: List of project information with id, name, path, and url


### `list_runs(project_path, filters=None)`

Get runs from a W&B project with optional filtering.

**Parameters:**
- `project_path` (str): Project path in format "entity/project"
- `filters` (dict, optional): Filtering criteria

**Supported Filters:**
- `state` (str): Run state ("Finished", "Failed", "Crashed", "Running")
- `createdAt` (dict): Creation time with 'gte'/'lte' keys (ISO 8601 format)
- `updatedAt` (dict): Update time with 'gte'/'lte' keys
- `duration` (dict): Duration in seconds with 'gte'/'lte' keys
- `tags` (str/dict): Tag filtering with MongoDB-style operators

**Returns:**
- `list[dict]`: List of run information including summary, config, and artifacts


### `filter_runs_by_single_param_difference(project_path, param_name, filters=None)`

Find experiments that differ only in a single parameter (useful for ablation studies).

**Parameters:**
- `project_path` (str): Project path in format "entity/project"
- `param_name` (str): Parameter name to analyze differences
- `filters` (dict, optional): Additional filters before grouping

**Returns:**
- `list[dict]`: Runs from the largest group differing only in the specified parameter

## Configuration

### MCP Client Setup

```json
{
  "mcpServers": {
    "wandb-tools": {
      "command": "python",
      "args": ["/path/to/run_wandb_tools.py"]
    }
  }
}
```
You should pass you WandB API key to the agent by prompt or global environment. 

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify API key is correct and active
2. **Project Not Found**: Check entity/project path spelling
3. **Network Issue**: The WandB may suffer from network issue, try to set the proxy if timeout or fail to connect is encountered.