# Terminal Execution Tools

This module provides secure terminal command execution with safety controls and whitelisting.

## Overview

The terminal execution tools allow safe execution of system commands with built-in security measures to prevent dangerous operations.

## Available Tools

### `execute_terminal_command(command, timeout=30, working_dir=None)`

Execute terminal commands safely with security validation.

**Parameters:**
- `command` (str): Command to execute
- `timeout` (int, optional): Command timeout in seconds (default: 30)
- `working_dir` (str, optional): Working directory for command execution

**Returns:**
- `dict`: Execution result containing stdout, stderr, return_code, command, and working_dir


### `list_allowed_commands()`

Get list of all commands allowed by the security whitelist.

**Returns:**
- `list[str]`: List of allowed commands with descriptions


## Security Features

### Command Whitelist

Only these commands are permitted:

| Command | Description |
|---------|-------------|
| `dir` | List directory contents (Windows) |
| `ls` | List directory contents (Unix/Linux) |
| `pwd` | Show current working directory |
| `echo` | Display text |
| `python` | Execute Python scripts |
| `pip` | Python package manager |
| `git` | Version control operations |
| `conda` | Environment management |

### Command Blacklist

These dangerous commands are blocked:

- **Deletion**: `rm`, `del`, `remove`
- **Formatting**: `format`, `mkfs`
- **System Control**: `shutdown`, `reboot`
- **Redirection**: `>`, `>>`
- **Downloads**: `wget`, `curl`
- **Privilege Escalation**: `sudo`, `su`

### Security Validation

All commands undergo validation:
1. **Blacklist Check**: Scanned for dangerous keywords
2. **Whitelist Check**: Command must be in approved list
3. **Command Parsing**: First word extracted and validated

## Configuration

### MCP Client Setup

```json
{
  "mcpServers": {
    "terminal-tools": {
      "command": "python",
      "args": ["/path/to/vscodeterminal.py"]
    }
  }
}
```

### Customizing Security Settings

To modify allowed/blocked commands, edit the constants in `vscodeterminal.py`:

```python
# Add new allowed commands
ALLOWED_COMMANDS = {
    "dir": "列出目录内容",
    "ls": "列出目录内容", 
    "your_command": "Your description"
}

# Add new blocked commands
BLOCKED_COMMANDS = {
    "rm", "del", "remove",
    "your_dangerous_command"
}
```


### Platform Differences

Remember to adapt commands for your target platform when use the tools in different platforms.
