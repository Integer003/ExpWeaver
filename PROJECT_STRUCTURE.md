# 📁 Project Structure Overview

ExpWeaver MCP Tools are reorganized in a clean, modular structure for better maintainability and usability.

## 🏗️ File Organization

### Root Directory
```
expweaver-mcp-tools/
├── README.md              
├── QUICKSTART.md          
├── LICENSE               
├── requirements.txt      
├── src/                  # Source code
├── scripts/              # Launcher scripts  
├── docs/                 # Detailed documentation
└── templates/            # Template files
```

### Source Code Structure (`src/`)

#### 🔬 Experiment Tracking (`src/experiment_tracking/`)
- `swanlab_api_tool.py` - SwanLab API integration
- `wandb_api_tool.py` - Weights & Biases API integration

#### 📊 Visualization (`src/visualization/`)
- `plotting_server.py` - Main plotting server (renamed from server.py)
- `plot.py` - Core plotting functions
- `experiment_drawing.py` - Experiment-specific visualizations (renamed from draw.py)

#### ⚡ Execution (`src/execution/`)
- `terminal_executor.py` - Safe local terminal execution (renamed from vscodeterminal.py)
- `remote_executor.py` - SSH remote execution (renamed from remote.py)

#### 🎯 Monitoring (`src/monitoring/`)
- `experiment_supervisor.py` - Experiment monitoring and notifications (renamed from supervise.py)

#### 🔧 Shared (`src/shared/`)
- `utils.py` - Common utilities
- `configure_logging.py` - Logging configuration
- `constants.py` - Project constants

### Launcher Scripts (`scripts/`)
- `run_swanlab_tools.py` - Launch SwanLab tools
- `run_wandb_tools.py` - Launch W&B tools
- `run_plotting_server.py` - Launch plotting server
- `run_drawing_tools.py` - Launch experiment drawing tools
- `run_terminal_tools.py` - Launch terminal tools
- `run_remote_tools.py` - Launch remote tools
- `run_supervisor.py` - Launch experiment supervisor

### Documentation (`docs/`)
- `swanlab_tools.md` - SwanLab integration documentation
- `wandb_tools.md` - W&B integration documentation
- `plotting_tools.md` - Plotting tools documentation
- `terminal_tools.md` - Terminal execution documentation
- `remote_tools.md` - Remote execution documentation
- `drawing_tools.md` - Experiment drawing documentation
- `supervision_tools.md` - Monitoring tools documentation

## 🚀 Usage Changes

### Before (Old Structure)
```bash
# Direct file execution
python swanlab_api_tool.py
python wandb_api_tool.py
python server.py
```

### After (New Structure)
```bash
# Using launcher scripts
python scripts/run_swanlab_tools.py
python scripts/run_wandb_tools.py
python scripts/run_plotting_server.py
```

### MCP Configuration Update
```json
{
  "mcpServers": {
    "swanlab-tools": {
      "command": "python",
      "args": ["/path/to/expweaver-mcp-tools/scripts/run_swanlab_tools.py"]
    }
  }
}
```

## ✅ Benefits of New Structure

### 🎯 Organization
- **Logical Grouping**: Tools grouped by functionality
- **Clear Hierarchy**: Easy to find and understand components
- **Scalability**: Easy to add new tools in appropriate categories

### 🔧 Maintainability  
- **Modular Design**: Each module has a specific purpose
- **Clean Imports**: Proper Python package structure
- **Documentation**: Each tool category has dedicated documentation

### 🚀 Usability
- **Simple Launchers**: Easy-to-use scripts for each tool
- **Consistent Interface**: All tools follow the same pattern
- **Quick Start**: New users can get started quickly

### 🔒 Security
- **Isolated Modules**: Security features contained within appropriate modules
- **Clear Boundaries**: Execution tools separate from data tools
- **Easy Auditing**: Security-critical code is clearly identified

## 🔄 Migration Guide

If you were using the old structure:

1. **Update MCP Config**: Use new script paths in your MCP configuration
2. **Update Scripts**: Replace direct file calls with launcher scripts
3. **Check Imports**: If you were importing modules, update import paths
4. **Review Docs**: Check updated documentation for any changes

## 📈 Future Additions

The new structure makes it easy to add:
- New experiment tracking platforms in `src/experiment_tracking/`
- New visualization types in `src/visualization/`
- New execution environments in `src/execution/`
- New monitoring capabilities in `src/monitoring/`

## 🎉 Summary

The reorganization transforms ExpWeaver from a collection of scripts into a professional, modular toolkit that's:
- **Easier to navigate** for new users
- **Simpler to maintain** for developers  
- **More scalable** for future features
- **Better documented** for all users

All functionality remains the same - we've just made it better organized and easier to use!
