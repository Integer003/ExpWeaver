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
        filters:dict[str, Any]=None,
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
        - tags (Any, optional): The tags of the run. List for tags more than one and Dict for tags with some requirements. Filters for "tags" field follow MongoDB-style operators:
            - {"tags": "baseline"} → runs containing "baseline" tag
            - {"tags": {"$all": ["tag1", "tag2"]}} → runs containing both tag1 AND tag2
            - {"tags": {"$in": ["tag1", "tag2"]}} → runs containing tag1 OR tag2
            - {"tags": {"$nin": ["tag1"]}} → runs NOT containing tag1
        Defaults to None.

    Returns:
        runs_list (list[dict]): The list of runs in the project. Every run include keys:
        - entity (str): The entity of the run.
        - id (str): The id of the run.
        - metadata (dict): The metadata of the run.
        - name (str): The name of the run.
        - path (str): The path of the run.
        - state (str): The state of the run.
        - url (str): The URL of the run.
        - summary (dict): The summary of the run, which is a dictionary containing key-value pairs of metrics.
    """
    api = wandb.Api()
    runs_list = []

    runs = api.runs(path=project_path, filters=filters)
    artifacts = []
    for run in runs:
        for artifact in run.logged_artifacts():
            artifacts.append({
                "name": artifact.name,
                "id": artifact.id,
                "type": artifact.type,
                "version": artifact.version,
                "url": artifact.url,
                "description": artifact.description,
                "createdAt": artifact.created_at,
                "aliases": artifact.aliases,
                "tags": artifact.tags
            })

        runs_list.append({
            "entity": getattr(run, "entity", None),
            "id": getattr(run, "id", None),
            "metadata": getattr(run, "metadata", None),
            "name": getattr(run, "name", None),
            "path": getattr(run, "path", None),
            "state": getattr(run, "state", None),
            "url": getattr(run, "url", None),
            "summary": dict(run.summary),
            "artifacts": artifacts
        })
    
    return runs_list

import re
import requests

@mcp.tool()
async def list_artifact(url:str, save_dir: str = "./artifacts") -> str:
    """
    Download artifact from the new W&B artifact URL format:
    Example: https://wandb.ai/entity/project/artifacts/type/name/version

    Args:
        url (str): The W&B artifact URL to download.
        save_dir (str, optional): The directory to save the downloaded artifact. Defaults to "./artifacts".

    Returns:
        path (str): The path where the artifact is saved.
    """
    # 匹配新格式
    match = re.match(r"https://wandb\.ai/([^/]+)/([^/]+)/artifacts/([^/]+)/([^/]+)/([^/]+)", url)
    if not match:
        raise ValueError("Invalid new-format W&B artifact URL")
    
    entity, project, art_type, art_name, version = match.groups()
    artifact_str = f"{entity}/{project}/{art_name}:{version}"
    print(f"[INFO] Fetching {artifact_str} (type={art_type}) ...")

    api = wandb.Api()
    artifact = api.artifact(artifact_str, type=art_type)
    path = artifact.download(root=save_dir)
    
    return path

if __name__ == "__main__":
    mcp.run()