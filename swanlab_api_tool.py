from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import pandas
from pandas import DataFrame

# swanlab Part

import swanlab
from swanlab.api.types import ApiResponse, Experiment, Project

mcp = FastMCP()
"""
@mcp.tool()
async def set_api_token(api: str) -> str:
    
    Initialize SwanLab API client with a user-provided token.
    This must be called before using other tools.

    Args:
        user_api (str): The swanlab API of user.

    Returns:
        output (str): The output text.
    
    global user_api
    user_api = swanlab.OpenApi(api_key=api)
    return "API client initialized successfully."
"""

@mcp.tool()
async def user_workspace(input_api: str, workspace_name:str=None) -> list[dict]:
    """
    Get the information of user's workspaces. Support the single input of workspace name. 

    Args:
        input_api (str): The swanlab API of user.
        workspace_name (str, optional): The workspace that user wants to check. Defaults to None.

    Returns:
        List[Dict]: the information list of workspaces. If the workspace is not exist, run user_workspace_project directly. 
    """
    user_api = swanlab.OpenApi(api_key=input_api)
    workspaces = user_api.list_workspaces().model_dump()['data']

    if workspace_name:
        workspaces = [workspace for workspace in workspaces if workspace["name"] == workspace_name]
    if workspaces == []:
        workspaces = None

    return workspaces

@mcp.tool()
async def user_workspace_project(input_api:str, workspaces:list=None, project_name:str=None) -> list[dict]:
    """
    Get the information of projects in every certain workspace of users. 
    If workspaces is not exist, the workspace defaults the personal workspace. 

    Args:
        input_api (str): The swanlab API of user.
        workspaces (List): The information list of the workspace. The workspace can be an empty list.
        project_name (str, optional): The project that user wants to check. Defaults to None.

    Returns:
        projects_list (List[Dict]): the detailed information list of the projects in workspaces list.
    """
    user_api = swanlab.OpenApi(api_key=input_api)
    projects_list = []
    if workspaces:
        for workspace in workspaces:
            projects = user_api.list_projects(username=workspace["username"]).model_dump()['data']
            projects_list += projects
        
        if project_name:
                return [p for p in projects_list if p["name"] == project_name]
    else:
        projects_list = user_api.list_projects().model_dump()['data']

    return projects_list

@mcp.tool()
async def user_project_expe(input_api:str, projects_list:list, expe_name:str=None) -> dict[str, list[dict]]:
    """
    Get the information list of experiments or a certain experiment under the given projects. 
    The variable projects_list depends on user_workspace_project.

    Args:
        input_api (str): The swanlab API of user.
        projects_list (List): The list of projects. 
        expe_name (str, optional): The experiment user wants to check.

    Returns:
       expe_dict (Dict[str, List[Dict]]): The dictionary of projects experiments, experiments list of the projects.
    """
    user_api = swanlab.OpenApi(api_key=input_api)
    
    expe_dict = {}
    for project in projects_list:
        experiments = user_api.list_experiments(project=project["name"], username=project["group"]["username"]).model_dump()['data']
        expe_dict[project["name"]] = experiments
    
    if expe_name:
        for project_name in expe_dict:
            expe_list = expe_dict[project_name]
            for expe in expe_list:
                if expe["name"] == expe_name:
                    return {project_name: [expe]}
        return None

    return expe_dict

@mcp.tool()
async def get_expe_metrics(input_api:str, expe_dict: dict) -> dict[str, str]:
    """
    Get the metrics of experiments or a certain experiment. The variable expe_dict depends on user_project_expe.

    Args:
        input_api (str): The swanlab API of user.
        expe_dict (Dict[str, List[Dict]]): The information dictionary of experiments. 

    Returns:
        data (Dict[str, Dict[str, str]]): The dictionary of experiments metrics in every project. Experiments metrics in csv format.
    """
    user_api = swanlab.OpenApi(api_key=input_api)
    
    metrics = {}
    for project_name in expe_dict:
        expe = expe_dict[project_name]
        temp_dict = {}
        for e in expe:
            keys = list(user_api.get_summary(project=project_name, exp_id=e["cuid"], username=e["user"]["username"]).data.keys())
            exp_metrics = user_api.get_metrics(exp_id=e["cuid"], keys=keys).data.to_csv(index=False)
            temp_dict[e["cuid"]] = exp_metrics
        metrics[project_name] = temp_dict

    return metrics

@mcp.tool()
async def swanlab_pipeline(input_api:str, workspace_name:str=None, project_name:str=None, expe_name:str=None) -> dict[str, dict[str, str]]:
    """
    A full tool to get the experiments information from user's swanlab.

    Args:
        input_api (str): The swanlab api of user.
        workspace_name (str, optional): Specified workspace user wants to check. Defaults to None or the personal space of user.
        project_name (str, optional): Specified project user wants to check. Defaults to None.
        expe_name (str, optional): Specified experiment user wants to check. Defaults to None.

    Returns:
        metrics (dict[str, dict[str, str]]): The information dictionary of "project_name-experiment_cuid-metrics".
    """
    try:
        workspaces = await user_workspace(input_api=input_api, workspace_name=workspace_name)
        if not workspaces:  # fallback: 没有匹配到 → 用 None，表示个人 workspace
            workspaces = None
    except Exception as e:
        workspaces = None  # fallback
        print(f"[Fallback] user_workspace failed: {e}")

    # Step 2. 获取 projects
    try:
        projects_list = await user_workspace_project(
            input_api=input_api, workspaces=workspaces, project_name=project_name
        )
        if not projects_list:  # fallback: 没有匹配到 → 个人 workspace 下所有项目
            projects_list = await user_workspace_project(input_api=input_api, workspaces=None)
    except Exception as e:
        projects_list = []
        print(f"[Fallback] user_workspace_project failed: {e}")

    # Step 3. 获取 experiments
    try:
        expe_dict = await user_project_expe(
            input_api=input_api, projects_list=projects_list, expe_name=expe_name
        )
        if not expe_dict:  # fallback: 没有匹配到 → 返回空字典
            expe_dict = {}
    except Exception as e:
        expe_dict = {}
        print(f"[Fallback] user_project_expe failed: {e}")

    # Step 4. 获取 metrics
    try:
        if expe_dict:
            metrics = await get_expe_metrics(input_api=input_api, expe_dict=expe_dict)
        else:
            metrics = {}
    except Exception as e:
        metrics = {}
        print(f"[Fallback] get_expe_metrics failed: {e}")

    return metrics