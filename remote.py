from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import paramiko
from typing import Optional, List, Dict
import os

mcp = FastMCP()

# 安全白名单命令
ALLOWED_COMMANDS = {
    "ls": "列出目录内容", 
    "pwd": "显示当前工作目录",
    "echo": "显示文本",
    "python": "执行Python脚本",
    "pip": "包管理器",
    "nvidia-smi": "查看GPU状态",
    "top": "查看进程",
    "ps": "进程状态",
    "free": "内存使用情况",
    "df": "磁盘使用情况"
}

# 危险命令黑名单
BLOCKED_COMMANDS = {
    "rm", "remove",      # 删除
    "mkfs", "format",    # 格式化
    "shutdown", "reboot",# 系统命令
    ">", ">>",          # 重定向
    "wget", "curl",     # 下载
    "sudo", "su"        # 提权
}

class SSHClient:
    """SSH客户端管理类"""
    def __init__(self):
        self._client = None
        
    def connect(self, hostname: str, username: str, 
                password: str = None, key_filename: str = None, 
                port: int = 22) -> None:
        """连接到SSH服务器"""
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 使用密码或密钥文件连接
        self._client.connect(
            hostname=hostname,
            username=username,
            password=password,
            key_filename=key_filename,
            port=port
        )
    
    def close(self) -> None:
        """关闭SSH连接"""
        if self._client:
            self._client.close()
            
    def execute_command(self, command: str, timeout: int = 30) -> Dict:
        """执行远程命令"""
        if not self._client:
            raise RuntimeError("未连接到SSH服务器")
            
        stdin, stdout, stderr = self._client.exec_command(command, timeout=timeout)
        return {
            "stdout": stdout.read().decode(),
            "stderr": stderr.read().decode(),
            "return_code": stdout.channel.recv_exit_status()
        }

# 全局SSH客户端实例
ssh_client = SSHClient()

@mcp.tool()
async def connect_ssh(
    hostname: str,
    username: str,
    password: str = None,
    key_path: str = None,
    port: int = 22
) -> dict:
    """
    连接到远程SSH服务器
    
    Args:
        hostname: 服务器地址
        username: 用户名
        password: 密码(可选)
        key_path: SSH密钥文件路径(可选)
        port: SSH端口(默认22)
        
    Returns:
        dict: 连接结果
    """
    try:
        ssh_client.connect(
            hostname=hostname,
            username=username,
            password=password,
            key_filename=key_path,
            port=port
        )
        return {
            "success": True,
            "message": f"成功连接到 {hostname}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"连接失败: {str(e)}"
        }

def validate_command(command: str) -> bool:
    """验证命令是否安全"""
    # 检查黑名单
    for blocked in BLOCKED_COMMANDS:
        if blocked in command.lower():
            raise TerminalSecurityError(f"危险命令被拦截: {blocked}")
            
    # 检查白名单
    command_name = command.split()[0].lower()
    if command_name not in ALLOWED_COMMANDS:
        raise TerminalSecurityError(f"未知命令被拦截: {command_name}")
        
    return True

@mcp.tool()
async def execute_remote_command(
    command: str,
    timeout: Optional[int] = 30
) -> dict:
    """
    在远程服务器上执行命令
    
    Args:
        command: 要执行的命令
        timeout: 超时时间(秒)
        
    Returns:
        dict: 执行结果
    """
    try:
        # 验证命令安全性
        validate_command(command)
        
        # 执行远程命令
        result = ssh_client.execute_command(command, timeout=timeout)
        result["command"] = command
        return result
        
    except TerminalSecurityError as e:
        return {
            "stdout": "",
            "stderr": f"安全错误: {str(e)}",
            "return_code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"执行错误: {str(e)}",
            "return_code": -1
        }

@mcp.tool()
async def close_ssh() -> dict:
    """关闭SSH连接"""
    try:
        ssh_client.close()
        return {
            "success": True,
            "message": "SSH连接已关闭"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"关闭连接失败: {str(e)}"
        }

@mcp.tool()
async def list_allowed_commands() -> List[str]:
    """列出所有允许执行的命令"""
    return [f"{cmd}: {desc}" for cmd, desc in ALLOWED_COMMANDS.items()]

if __name__ == "__main__":
    mcp.run()