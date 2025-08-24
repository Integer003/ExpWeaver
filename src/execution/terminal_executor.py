from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import subprocess
import os
import sys
from typing import Optional, List

mcp = FastMCP()

# 安全白名单命令
ALLOWED_COMMANDS = {
    "dir": "列出目录内容",
    "ls": "列出目录内容", 
    "pwd": "显示当前工作目录",
    "echo": "显示文本",
    "python": "执行Python脚本",
    "pip": "包管理器",
    "git": "版本控制",
    "conda": "环境管理"
}

# 危险命令黑名单
BLOCKED_COMMANDS = {
    "rm", "del", "remove",  # 删除
    "format", "mkfs",       # 格式化
    "shutdown", "reboot",   # 系统命令
    ">", ">>",             # 重定向
    "wget", "curl",        # 下载
    "sudo", "su"           # 提权
}

class TerminalSecurityError(Exception):
    """终端安全异常"""
    pass

def validate_command(command: str) -> bool:
    """
    验证命令是否安全
    
    Args:
        command: 要执行的命令
        
    Returns:
        bool: 命令是否安全
        
    Raises:
        TerminalSecurityError: 命令不安全时抛出
    """
    # 检查是否包含黑名单命令
    for blocked in BLOCKED_COMMANDS:
        if blocked in command.lower():
            raise TerminalSecurityError(f"危险命令被拦截: {blocked}")
            
    # 检查命令是否在白名单中
    command_name = command.split()[0].lower()
    if command_name not in ALLOWED_COMMANDS:
        raise TerminalSecurityError(f"未知命令被拦截: {command_name}")
        
    return True

@mcp.tool()
async def execute_terminal_command(
    command: str,
    timeout: Optional[int] = 30,
    working_dir: Optional[str] = None
) -> dict:
    """
    在VSCode终端中安全地执行命令
    
    Args:
        command: 要执行的命令
        timeout: 命令超时时间(秒),默认30秒
        working_dir: 工作目录
        
    Returns:
        dict: 执行结果,包含stdout/stderr/return_code
    """
    try:
        # 验证命令安全性
        validate_command(command)
        
        # 设置工作目录
        cwd = working_dir or os.getcwd()
        
        # 执行命令
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        
        # 等待命令完成,支持超时
        stdout, stderr = process.communicate(timeout=timeout)
        
        return {
            "stdout": stdout,
            "stderr": stderr,
            "return_code": process.returncode,
            "command": command,
            "working_dir": cwd
        }
        
    except TerminalSecurityError as e:
        return {
            "stdout": "",
            "stderr": f"安全错误: {str(e)}",
            "return_code": -1
        }
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            "stdout": "",
            "stderr": f"命令执行超时(>{timeout}秒)",
            "return_code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"执行错误: {str(e)}",
            "return_code": -1
        }

@mcp.tool()
async def list_allowed_commands() -> List[str]:
    """
    列出所有允许执行的命令
    """
    return [f"{cmd}: {desc}" for cmd, desc in ALLOWED_COMMANDS.items()]

if __name__ == "__main__":
    mcp.run()