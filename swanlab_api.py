#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SwanLab OpenAPI Complete MCP Tools
Contains all SwanLab OpenAPI methods wrapped as MCP tools
"""
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from typing import Dict, List, Union, Optional
import json

import swanlab
from swanlab.api.types import ApiResponse, Experiment, Project

mcp = FastMCP()

# ========== Workspace Related Tools ==========

@mcp.tool()
async def list_workspaces(api_key: str) -> List[Dict]:
    """
    Get all workspaces (Groups) of the current user.
    
    This API allows you to retrieve information about all workspaces that the current user has access to,
    including both personal workspaces and organization workspaces where the user is a member or owner.
    
    Workspaces in SwanLab are containers for projects and can be either:
    - Personal workspace: Individual user's private space
    - Organization workspace: Shared space for team collaboration
    
    The username field in the response is particularly important as it's used as a unique identifier
    for workspace-related operations and URL construction.

    Args:
        api_key (str): SwanLab API key for authentication. You can get your API key from the SwanLab web interface.

    Returns:
        List[Dict]: List of workspace dictionaries, each containing:
            - name (str): Human-readable workspace name displayed in the UI
            - username (str): Unique workspace identifier used in URLs and API calls
            - role (str): User's permission level in this workspace ('OWNER' or 'MEMBER')
    
    Example:
        >>> # Get workspace list
        >>> workspaces = await list_workspaces("your_api_key")
        >>> print(workspaces)
        # [
        #     {
        #         "name": "workspace1",
        #         "username": "kites-test3",
        #         "role": "OWNER"
        #     },
        #     {
        #         "name": "hello-openapi",
        #         "username": "kites-test2",
        #         "role": "MEMBER"
        #     }
        # ]
        
        >>> # Get first workspace name
        >>> print(workspaces[0]["name"])  # "workspace1"
        >>> print(workspaces[0]["username"])  # "kites-test3" 
        >>> print(workspaces[0]["role"])  # "OWNER"
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.list_workspaces()
    return response.model_dump()['data']

# ========== Project Related Tools ==========

@mcp.tool()
async def list_projects(api_key: str, username: str = "", detail: bool = True) -> List[Dict]:
    """
    Get all projects under a specified workspace.
    
    Projects in SwanLab are containers for machine learning experiments. Each project belongs to a workspace
    and contains multiple experiments that share similar goals or use similar datasets/models.
    
    This API retrieves comprehensive information about projects including metadata, statistics, and access permissions.
    The 'detail' parameter controls whether to include statistical information like experiment counts.

    Args:
        api_key (str): SwanLab API key for authentication
        username (str, optional): Workspace identifier (username). If empty, defaults to the user's personal workspace.
                                 For organization workspaces, use the organization's username.
        detail (bool, optional): Whether to include detailed project statistics (experiment count, contributors, etc.). 
                                Defaults to True.

    Returns:
        List[Dict]: List of project dictionaries, each containing:
            - cuid (str): Unique project identifier
            - name (str): Project name
            - description (str): Project description
            - visibility (str): Project visibility ('PUBLIC' or 'PRIVATE')
            - createdAt (str): Creation timestamp in ISO format
            - updatedAt (str): Last update timestamp in ISO format
            - group (Dict): Workspace information with 'type', 'username', 'name'
            - count (Dict): Statistics including 'experiments', 'contributors', 'children', 'runningExps' (if detail=True)
    
    Example:
        >>> projects = await list_projects("your_api_key", username="team_workspace")
        >>> print(projects[0]["name"])  # "Image Classification Project"
        >>> print(projects[0]["count"]["experiments"])  # 15
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.list_projects(username=username, detail=detail)
    return response.model_dump()['data']

@mcp.tool()
async def delete_project(api_key: str, project: str, username: str = "") -> Dict:
    """
    Permanently delete a project and all its associated experiments.
    
    WARNING: This operation is irreversible! Once a project is deleted, all experiments, 
    metrics, logs, and other data within the project will be permanently lost.
    
    Only users with appropriate permissions (project owner or workspace admin) can delete projects.
    This operation will also delete all experiments within the project.

    Args:
        api_key (str): SwanLab API key for authentication
        project (str): Name of the project to delete
        username (str, optional): Workspace identifier where the project is located. 
                                 If empty, defaults to the user's personal workspace.

    Returns:
        Dict: Response dictionary containing:
            - code (int): HTTP status code (200 for success)
            - errmsg (str): Error message (empty if successful)
            - data (dict): Empty dictionary indicating successful deletion
    
    Example:
        >>> result = await delete_project("your_api_key", "old_project")
        >>> print(result["code"])  # 200
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.delete_project(project=project, username=username)
    return response.model_dump()

# ========== Experiment Related Tools ==========

@mcp.tool()
async def list_experiments(api_key: str, project: str, username: str = "") -> List[Dict]:
    """
    Get all experiments under a specified project.
    
    Experiments in SwanLab represent individual machine learning training runs or model evaluations.
    Each experiment contains metrics, hyperparameters, logs, and other tracking information.
    
    This API returns basic experiment information including metadata and configuration.
    For detailed metrics and logs, use get_experiment() or get_metrics().

    Args:
        api_key (str): SwanLab API key for authentication
        project (str): Name of the project containing the experiments
        username (str, optional): Workspace identifier where the project is located.
                                 If empty, defaults to the user's personal workspace.

    Returns:
        List[Dict]: List of experiment dictionaries, each containing:
            - cuid (str): Unique experiment identifier (used for further API calls)
            - name (str): Experiment name
            - description (str): Experiment description
            - state (str): Current experiment state ('RUNNING', 'FINISHED', 'CRASHED', etc.)
            - show (bool): Whether the experiment is visible in the UI
            - createdAt (str): Creation timestamp in ISO format
            - finishedAt (str): Completion timestamp in ISO format (null if still running)
            - user (Dict): Creator information with 'username' and 'name'
            - profile (Dict): Configuration information including 'config' with hyperparameters
    
    Example:
        >>> # Get experiment list
        >>> experiments = await list_experiments("your_api_key", "project1")
        >>> print(experiments)
        # [
        #     {
        #         "cuid": "cuid1",
        #         "name": "experiment1",
        #         "description": "Description 1",
        #         "state": "RUNNING",
        #         "show": true,
        #         "createdAt": "2024-11-23T12:28:04.286Z",
        #         "finishedAt": null,
        #         "user": {
        #             "username": "kites-test3",
        #             "name": "Kites Test"
        #         },
        #         "profile": {
        #             "config": {
        #                 "lr": 0.001,
        #                 "epochs": 10
        #             }
        #         }
        #     },
        #     ...
        # ]
        
        >>> # Get first experiment's CUID
        >>> print(experiments[0]["cuid"])  # "cuid1"
        
        >>> # Get first experiment's name
        >>> print(experiments[0]["name"])  # "experiment1"
        
        >>> # Get experiment state
        >>> print(experiments[0]["state"])  # "RUNNING"
        
        >>> # Get hyperparameters
        >>> print(experiments[0]["profile"]["config"]["lr"])  # 0.001
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.list_experiments(project=project, username=username)
    return response.model_dump()['data']

@mcp.tool()
async def get_experiment(api_key: str, project: str, exp_id: str, username: str = "") -> Dict:
    """
    Get detailed information about a specific experiment.
    
    This API provides comprehensive information about a single experiment, including all metadata,
    configuration, environment details, and system information. It's more detailed than list_experiments()
    which only provides basic information.
    
    The experiment ID (exp_id) is the unique CUID identifier that can be obtained from list_experiments()
    or from the experiment's "Environment" tab in the SwanLab web interface.

    Args:
        api_key (str): SwanLab API key for authentication
        project (str): Name of the project containing the experiment
        exp_id (str): Unique experiment identifier (CUID). This can be found in:
                     - The 'cuid' field from list_experiments() response
                     - The "Experiment ID" in the web interface's Environment tab
        username (str, optional): Workspace identifier where the project is located.
                                 If empty, defaults to the user's personal workspace.

    Returns:
        Dict: Detailed experiment dictionary containing:
            - cuid (str): Unique experiment identifier
            - name (str): Experiment name
            - description (str): Experiment description  
            - state (str): Current state ('RUNNING', 'FINISHED', 'FAILED', etc.)
            - show (bool): Visibility status in UI
            - createdAt (str): Creation timestamp in ISO format
            - finishedAt (str): Completion timestamp (null if running)
            - user (Dict): Creator info with 'username' and 'name'
            - profile (Dict): Comprehensive configuration including:
                - config: User-defined hyperparameters and settings
                - conda: Conda environment information
                - requirements: Python package requirements
                - system: System and hardware information
                - git: Git repository information (if available)
    
    Example:
        >>> # Get detailed experiment information
        >>> exp = await get_experiment("your_api_key", "project1", "cuid1")
        >>> print(exp)
        # {
        #     "cuid": "cuid1",
        #     "name": "experiment1",
        #     "description": "This is a test experiment",
        #     "state": "FINISHED",
        #     "show": true,
        #     "createdAt": "2024-11-23T12:28:04.286Z",
        #     "finishedAt": "2024-11-25T15:56:48.123Z",
        #     "user": {
        #         "username": "kites-test3",
        #         "name": "Kites Test"
        #     },
        #     "profile": {
        #         "conda": "...",
        #         "requirements": "...",
        #         ...
        #     }
        # }
        
        >>> # Get experiment state
        >>> print(exp["state"])  # "FINISHED"
        
        >>> # Get creator username
        >>> print(exp["user"]["username"])  # "kites-test3"
        
        >>> # Get configuration details
        >>> print(exp["profile"]["config"]["learning_rate"])  # 0.001
        >>> print(exp["profile"]["requirements"])  # "torch==1.9.0\nnumpy==1.21.0"
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.get_experiment(project=project, exp_id=exp_id, username=username)
    return response.model_dump()['data']

@mcp.tool()
async def delete_experiment(api_key: str, project: str, exp_id: str, username: str = "") -> Dict:
    """
    Permanently delete a specific experiment and all its associated data.
    
    WARNING: This operation is irreversible! Once an experiment is deleted, all associated data will be 
    permanently lost, including:
    - All logged metrics and charts
    - Hyperparameter configurations  
    - System information and logs
    - Any uploaded files or artifacts
    - Run history and metadata
    
    Only users with appropriate permissions can delete experiments. Make sure you have backed up
    any important data before deletion.

    Args:
        api_key (str): SwanLab API key for authentication
        project (str): Name of the project containing the experiment
        exp_id (str): Unique experiment identifier (CUID) to delete. This can be found in:
                     - The 'cuid' field from list_experiments() response  
                     - The "Experiment ID" in the web interface's Environment tab
        username (str, optional): Workspace identifier where the project is located.
                                 If empty, defaults to the user's personal workspace.

    Returns:
        Dict: Response dictionary containing:
            - code (int): HTTP status code (200 for success)
            - errmsg (str): Error message (empty if successful)
            - data (dict): Empty dictionary indicating successful deletion
    
    Example:
        >>> result = await delete_experiment("your_api_key", "my_project", "exp_cuid_123")
        >>> print(result["code"])  # 200
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.delete_experiment(project=project, exp_id=exp_id, username=username)
    return response.model_dump()

@mcp.tool()
async def get_summary(api_key: str, project: str, exp_id: str, username: str = "") -> Dict:
    """
    Get experiment summary information including statistical analysis of all tracked metrics.
    
    This API provides a comprehensive overview of an experiment's performance by computing statistical
    summaries for each tracked metric. It includes the final values, minimum/maximum values, and the
    training steps where these extrema occurred.
    
    This is particularly useful for:
    - Quick performance evaluation and comparison
    - Identifying the best performing epochs/iterations
    - Understanding metric trends and stability
    - Generating experiment reports and summaries

    Args:
        api_key (str): SwanLab API key for authentication
        project (str): Name of the project containing the experiment
        exp_id (str): Unique experiment identifier (CUID). This can be found in:
                     - The 'cuid' field from list_experiments() response
                     - The "Experiment ID" in the web interface's Environment tab
        username (str, optional): Workspace identifier where the project is located.
                                 If empty, defaults to the user's personal workspace.

    Returns:
        Dict: Summary statistics dictionary where each key is a metric name and each value contains:
            - step (int): The final/last step number where this metric was logged
            - value (float): The final/last value of this metric
            - min (Dict): Minimum value information containing:
                - step (int): Step number where minimum value occurred
                - value (float): The minimum value recorded
            - max (Dict): Maximum value information containing:
                - step (int): Step number where maximum value occurred  
                - value (float): The maximum value recorded
    
    Example:
        >>> # Get experiment summary
        >>> summary = await get_summary("your_api_key", "project1", "cuid1")
        >>> print(summary)
        # {
        #     "loss": {
        #         "step": 47,
        #         "value": 0.1907215012216071,
        #         "min": {
        #             "step": 33,
        #             "value": 0.1745886406861026
        #         },
        #         "max": {
        #             "step": 0,
        #             "value": 0.7108771095136294
        #         }
        #     },
        #     ...
        # }
        
        >>> # Get final loss value
        >>> print(summary["loss"]["value"])  # 0.1907215012216071
        
        >>> # Get best (minimum) loss value
        >>> print(summary["loss"]["min"]["value"])  # 0.1745886406861026
        
        >>> # Get step where minimum loss occurred
        >>> print(summary["loss"]["min"]["step"])  # 33
        
        >>> # Get maximum loss value
        >>> print(summary["loss"]["max"]["value"])  # 0.7108771095136294
        
        >>> # Get step where maximum occurred
        >>> print(summary["loss"]["max"]["step"])  # 0
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.get_summary(project=project, exp_id=exp_id, username=username)
    return response.model_dump()['data']

@mcp.tool()
async def get_metrics(api_key: str, exp_id: str, keys: Union[str, List[str]]) -> str:
    """
    Get detailed time-series metrics data for specific tracked parameters from an experiment.
    
    This API retrieves the complete history of specified metrics throughout the experiment's execution.
    Unlike get_summary() which provides statistical summaries, this function returns the raw time-series
    data showing how metrics evolved over training steps.
    
    The returned data includes both the metric values and their corresponding timestamps, allowing for
    detailed analysis of training dynamics, convergence patterns, and temporal correlations.
    
    This is essential for:
    - Plotting training curves and visualizations
    - Analyzing convergence behavior and stability
    - Comparing different experiments' training dynamics
    - Detecting overfitting, underfitting, or other training issues
    - Exporting data for external analysis tools

    Args:
        api_key (str): SwanLab API key for authentication
        exp_id (str): Unique experiment identifier (CUID). This can be found in:
                     - The 'cuid' field from list_experiments() response
                     - The "Experiment ID" in the web interface's Environment tab
        keys (Union[str, List[str]]): Metric names to retrieve. These are the keys used in swanlab.log() calls.
                                     Can be:
                                     - Single string: "loss" 
                                     - List of strings: ["loss", "accuracy", "val_loss"]
                                     Available metric names can be seen in the web interface or obtained from get_summary()

    Returns:
        str: Complete metrics data in CSV format with columns:
            - step: Training step/iteration number (index)
            - {metric_name}: Value of the metric at each step
            - {metric_name}_timestamp: Unix timestamp when the metric was logged
            
            For each requested metric, you get two columns: the value and the timestamp.
    
    Example:
        >>> csv_data = await get_metrics("your_api_key", "exp_cuid_123", ["loss", "accuracy"])
        >>> print(csv_data)
        # Output CSV format:
        # step,loss,loss_timestamp,accuracy,accuracy_timestamp
        # 1,0.336772,1751712864853,0.670422,1751712864852
        # 2,0.338035,1751712864858,0.830018,1751712864857
        # 3,0.282654,1751712864862,0.794594,1751712864862
        # ...
        
        # For single metric:
        >>> loss_data = await get_metrics("your_api_key", "exp_cuid_123", "loss")
    """
    client = swanlab.OpenApi(api_key=api_key)
    response = client.get_metrics(exp_id=exp_id, keys=keys)
    # Return DataFrame in CSV format
    return response.data.to_csv(index=False)


if __name__ == "__main__":
    import os
    import sys
    
    # 检查是否在调试模式
    debug_mode = os.getenv("DEBUG", "").lower() in ("1", "true", "yes")
    
    if debug_mode:
        print("🐛 Debug mode started...")
        print(f"Python path: {sys.executable}")
        print(f"Working directory: {os.getcwd()}")
        print("Set breakpoints where needed, then continue...")
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        if debug_mode:
            import traceback
            traceback.print_exc()
