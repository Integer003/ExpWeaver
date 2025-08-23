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

from typing import Any
import json

def convert_to_string_dict(obj):
    """Convert all values in a nested dictionary to strings."""
    if isinstance(obj, dict):
        return {str(k): convert_to_string_dict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return str(obj)  
    else:
        return str(obj)
    
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
    
    for run in runs:
        artifacts = []
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
            
        # try to convert summary to dict with string keys and string values
        try:
            summary_keys = []
            try:
                for key in run.summary.keys():
                    summary_keys.append(key)
            except:
                # fallback method
                summary_keys = list(run.summary._summary.keys()) if hasattr(run.summary, '_summary') else []

            # build the summary dictionary with string keys and string values
            summary_dict_str = {}
            for key in summary_keys:
                try:
                    value = run.summary[key]
                    summary_dict_str[str(key)] = convert_to_string_dict(value)
                except Exception as inner_e:
                    print(f"Warning: Could not get value for key {key} in run {run.name}: {inner_e}")
                    summary_dict_str[str(key)] = "N/A"
                    
        except Exception as e:
            print(f"Warning: Could not convert summary for run {run.name}: {e}")
            summary_dict_str = {}
            
        runs_list.append({
            "entity": getattr(run, "entity", None),
            "id": getattr(run, "id", None),
            "metadata": getattr(run, "metadata", None),
            "name": getattr(run, "name", None),
            "path": getattr(run, "path", None),
            "state": getattr(run, "state", None),
            "url": getattr(run, "url", None),
            "summary": summary_dict_str,
            "config": dict(run.config),
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

@mcp.tool()
async def filter_runs_by_single_param_difference(project_path:str, param_name: str, filters: dict[str, Any]=None) -> list[dict]:
    """
    Filter runs in a W&B project to find experiments that differ only in a single specified parameter, 
    while all other parameters remain identical. This is useful for comparing experiments that form 
    a controlled parameter sweep or ablation study.

    Args:
        project_path (str): The path of the target project in format "entity/project".
        param_name (str): The name of the parameter to check for differences, such as 'learning_rate', 
                         'batch_size', or 'model_type'. This parameter will vary across the filtered runs 
                         while all other config parameters remain constant.
        filters (dict[str, Any], optional): Additional filters to apply before grouping by parameter 
                                          differences. Uses the same filter format as list_runs(). 
                                          Defaults to None.

    Returns:
        list[dict]: A list of run dictionaries that belong to the largest group of experiments 
                   differing only in the specified parameter. The runs are sorted by the parameter 
                   values in ascending order. Each run dictionary contains the same keys as 
                   returned by list_runs(): entity, id, metadata, name, path, state, url, 
                   summary, config, and artifacts.

    Example:
        # Find all runs that differ only in learning rate
        filtered_runs = await filter_runs_by_single_param_difference(
            "my-team/my-project", 
            "learning_rate"
        )
        
        # Find finished runs that differ only in batch size
        filtered_runs = await filter_runs_by_single_param_difference(
            "my-team/my-project", 
            "batch_size",
            filters={"state": "finished"}
        )
    """
    runs=await list_runs(project_path, filters)

    if not runs:
        return []
        
    # 提取所有runs的config，移除指定参数
    configs_without_param = []
    param_values = []
    
    for run in runs:
        config = run["config"]

        # 保存指定参数的值
        param_value = config.get(param_name, None)
        param_values.append(param_value)
        
        # 移除指定参数，创建用于比较的config
        config_copy = config.copy()
        if param_name in config_copy:
            del config_copy[param_name]
        configs_without_param.append(config_copy)
    
    # 找到最常见的config模式（移除指定参数后）
    from collections import defaultdict
    config_groups = defaultdict(list)
    
    for i, config in enumerate(configs_without_param):
        # 将config转换为可哈希的形式进行分组
        config_key = tuple(sorted(config.items()))
        config_groups[config_key].append(i)
    
    # 找到包含runs最多的组
    largest_group_indices = max(config_groups.values(), key=len)
    sorted_indices = sorted(largest_group_indices
                            , key=lambda i: param_values[i])

    filtered_runs = [runs[i] for i in sorted_indices]

    return filtered_runs

if __name__ == "__main__":
    mcp.run()
