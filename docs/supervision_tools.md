# Experiment Supervision Tools

This module provides automated monitoring and notification system for machine learning experiments with email alerts.

## Overview

The supervision tools enable continuous monitoring of W&B experiments with automatic email notifications when experiment status changes.

## Available Tools

The supervision system runs as a background service and doesn't expose direct MCP tools. Instead, it operates through environment variable configuration and automatic monitoring.

## Core Functions

### `supervise_experiments(run_path, receiver_email)`

Main supervision function that monitors experiments and sends notifications.

**Parameters:**
- `run_path` (str): W&B project path in format "entity/project"
- `receiver_email` (str): Email address to receive notifications

**Behavior:**
- Continuously polls experiment status every 30 seconds
- Detects state changes from "running" to "finished", "crashed", or "failed"
- Sends email notifications for status changes
- Maintains state history to avoid duplicate notifications

### `send_notification(run_name, status, receiver_email)`

Send email notifications for experiment status changes.

**Parameters:**
- `run_name` (str): Name of the experiment
- `status` (str): New experiment status
- `receiver_email` (str): Recipient email address

## Configuration

### Required Environment Variables

```bash
# W&B project to monitor
export WANDB_RUN_PATH="entity/project"

# Email configuration
export RECEIVER_EMAIL="user@example.com"
export SENDER_EMAIL="notifications@yourcompany.com"  
export SENDER_PASS="app-password"
export SMTP_SERVER="smtp.gmail.com"
```

### Optional Configuration

```bash
# Customize check interval (default: 30 seconds)
export CHECK_INTERVAL=60

# SMTP port (default: 465 for SSL)
export SMTP_PORT=587
```
Or you can set the environment variables in the `experiment_supervisor.py` source code. 
### MCP Client Setup

```json
{
  "mcpServers": {
    "remote-tools": {
      "command": "python",
      "args": ["/path/to/run_supervisor.py"]
    }
  }
}
```

## Notification Examples

### Email Format

**Subject:** `W&B 实验 experiment-name-123 状态更新`

**Body:** `🔔 实验 experiment-name-123 已经 finished！`

### Status Transitions

1. **Finished Successfully**
   - Subject: "W&B 实验 resnet50-baseline 状态更新"
   - Body: "🔔 实验 resnet50-baseline 已经 finished！"

2. **Crashed**
   - Subject: "W&B 实验 transformer-large 状态更新"  
   - Body: "🔔 实验 transformer-large 已经 crashed！"

3. **Failed**
   - Subject: "W&B 实验 data-preprocessing 状态更新"
   - Body: "🔔 实验 data-preprocessing 已经 failed！"

## Advanced Configuration

### Custom Email Templates

```python
# Modify email content in send_notification function
def send_notification(run_name: str, status: str, receiver_email: str):
    subject = f"🚀 Experiment Alert: {run_name}"
    
    status_emojis = {
        "finished": "✅",
        "crashed": "💥", 
        "failed": "❌"
    }
    
    emoji = status_emojis.get(status, "ℹ️")
    body = f"{emoji} Experiment '{run_name}' has {status}.\n\n"
    body += f"Check details at: https://wandb.ai/{os.environ['WANDB_RUN_PATH']}"
```

## Troubleshooting

### Common Issues

1. **Email Account Authentication**

    The App key of your email account should be correctly set and needs to have enough permission. 
  
3. **Missing Environment Variables**
   ```bash
   # Check all required variables are set
   env | grep -E "(WANDB_|RECEIVER_|SENDER_|SMTP_)"
   ```
