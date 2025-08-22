from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import pandas
from pandas import DataFrame

mcp = FastMCP()

# W&B part
import os
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

import wandb
from typing import Any

@mcp.tool()
async def wandb_login(api_key:str):
    """
    Login to W&B with the provided API key. The first step to run.

    Args:
        api_key (str): The W&B API key of the user.
    """
    wandb.login(key=api_key)
    print("Logged in to W&B successfully.")
    

@mcp.tool()
async def list_projects(entity:str=None) -> list[dict]:
    """
    Get the list of projects in W&B, including the id, the name, the path and the url of projects.

    Args:
        entity (str, optional): The entity name of the Projects. Defaults to None.

    Returns:
        projects_list (list[dict]): The list of projects.
    """
    api = wandb.Api()
    projects_list = []

    projects = api.projects(entity=entity)
    for project in projects:
        projects_list.append({
            "id": getattr(project, "id", None),
            "name": getattr(project, "name", None),
            "path": "/".join(project.path),
            "url": getattr(project, "url", None),
        })
    
    return projects_list

@mcp.tool()
async def list_runs(
        project_path:str, 
        filters:dict[str, Any]=None
    ) -> list[dict]:
    """
    Get the list of runs in a W&B project. Runs includes the id, name, path, url, and other metadata.
    Support filtering query.

    Args:
        project_path (str): The path of the target project.
        filters (dict[str, Any], optional): The filters query for runs. Defaults to None. Support keys:
        - state (str, optional): The state of the target. Can be one of: Finished, Failed, Crashed, or Running. Defaults to None.
        - createdAt (Any, optional): The creating time of the run, written in ISO 8601 format.
        For a time period, use a dict with keys 'gte' and 'lte'. Defaults to None.
        - updatedAt (Any, optional): The updating time of the run, written in ISO 8601 format. 
        For a time period, use a dict with keys 'gte' and 'lte'. Defaults to None.
        - duration (Any, optional): The duration of the run, in seconds. 
        For a time period, use a dict with keys 'gte' and 'lte'. Defaults to None.
        - tags (list[str], optional): The tags of the run. Defaults to None.

    Returns:
        runs_list (list[dict]): The list of runs in the project.
    """
    api = wandb.Api()
    runs_list = []

    runs = api.runs(path=project_path, filters=filters)
    for run in runs:
        runs_list.append({
            "entity": getattr(run, "entity", None),
            "id": getattr(run, "id", None),
            "metadata": getattr(run, "metadata", None),
            "name": getattr(run, "name", None),
            "path": getattr(run, "path", None),
            "state": getattr(run, "state", None),
            "url": getattr(run, "url", None),
        })
    
    return runs_list

if __name__ == "__main__":
    mcp.run()