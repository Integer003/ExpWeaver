# Remote Execution Tools

This module provides secure SSH-based remote command execution with safety controls and connection management.

## Overview

The remote execution tools enable secure command execution on remote servers via SSH with the same safety features as local terminal execution.

## Available Tools

### `connect_ssh(hostname, username, password=None, key_path=None, port=22)`

Establish SSH connection to a remote server.

**Parameters:**
- `hostname` (str): Server address or IP
- `username` (str): SSH username
- `password` (str, optional): Password authentication
- `key_path` (str, optional): Path to SSH private key file
- `port` (int): SSH port (default: 22)

**Returns:**
- `dict`: Connection result with success status and message

### `execute_remote_command(command, timeout=30)`

Execute commands on the connected remote server.

**Parameters:**
- `command` (str): Command to execute remotely
- `timeout` (int, optional): Command timeout in seconds (default: 30)

**Returns:**
- `dict`: Execution result with stdout, stderr, return_code, and command


Close the SSH connection.

**Returns:**
- `dict`: Closure result with success status and message


### `list_allowed_commands()`

Get list of commands allowed for remote execution.

**Returns:**
- `list[str]`: List of allowed commands with descriptions

## Security Features

### Remote Command Whitelist

Allowed commands for remote execution:

| Command | Description |
|---------|-------------|
| `ls` | List directory contents |
| `pwd` | Show current working directory |
| `echo` | Display text |
| `python` | Execute Python scripts |
| `pip` | Python package manager |
| `nvidia-smi` | Check GPU status |
| `top` | View running processes |
| `ps` | Process status |
| `free` | Memory usage information |
| `df` | Disk usage information |


## Configuration

### SSH Key Setup

You should pass your remote config to the llm. The format is: 
```bash
# Example. Change the parameters to your own settings. 
Host 116.169.116.30
    HostName 116.169.116.30
    Port 41493
    IdentityFile ~/.ssh/id_ed25519
    User root
```

### MCP Client Setup

```json
{
  "mcpServers": {
    "remote-tools": {
      "command": "python",
      "args": ["/path/to/run_remote_tools.py"]
    }
  }
}
```
