# Quick Start Guide

This guide will help you get started with ExpWeaver MCP Tools quickly.

## 🚀 Quick Setup

### 1. Clone and Install

```bash
git clone https://github.com/your-username/expweaver-mcp-tools.git
cd expweaver-mcp-tools
pip install -r requirements.txt
```

### 2. Test a Tool

```bash
# Test the plotting server
python scripts/run_plotting_server.py

# Test SwanLab integration (requires API key)
python scripts/run_swanlab_tools.py

# Test terminal tools
python scripts/run_terminal_tools.py
```

### 3. Configure MCP Client

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "expweaver-plotting": {
      "command": "python",
      "args": ["/path/to/expweaver-mcp-tools/scripts/run_plotting_server.py"]
    }
  }
}
```

## 📊 Quick Examples

### Generate a Plot

```python
# CSV data
csv_data = """x,y,group
1,2,A
2,4,A
3,6,A
1,1,B
2,3,B
3,5,B"""

# Generate plot
result = generate_plot(
    csv_data=csv_data,
    plot_type="line",
    json_kwargs='{"x": "x", "y": "y", "hue": "group"}'
)
```

### Get W&B Experiments

```python
# Login to W&B
await wandb_login("your-api-key")

# List projects
projects = await list_projects("your-entity")

# Get runs
runs = await list_runs("entity/project")
```

### Execute Safe Commands

```python
# List directory
result = await execute_terminal_command("ls -la")

# Check Python version
result = await execute_terminal_command("python --version")
```

## 🔧 Tool Categories

| Category | Tools | Use Cases |
|----------|-------|-----------|
| **Experiment Tracking** | SwanLab, W&B | Retrieve experiment data, metrics, artifacts |
| **Visualization** | Plotting, Drawing | Create charts, experiment visualizations |
| **Execution** | Terminal, Remote | Run commands safely locally or remotely |
| **Monitoring** | Supervisor | Monitor experiments, send notifications |

## 📚 Next Steps

1. **Read the docs**: Check `docs/` folder for detailed documentation
2. **Explore examples**: See usage examples in the README
3. **Configure security**: Review security settings for execution tools
4. **Set up monitoring**: Configure email notifications for experiments

## 🆘 Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running scripts from the project root
2. **API key issues**: Verify your SwanLab/W&B API keys are correct
3. **Permission errors**: Check file permissions for script execution

### Getting Help

- Check the documentation in `docs/`
- Look at examples in the README
- Create an issue on GitHub

## 🎯 Popular Use Cases

### ML Experiment Analysis
1. Use W&B tools to fetch experiment data
2. Use plotting tools to visualize results
3. Use drawing tools for publication-ready figures

### Remote Model Training
1. Use remote tools to connect to training servers
2. Use monitoring tools to track experiment progress
3. Get notified when training completes

### Data Visualization Pipeline
1. Export data from experiment tracking platforms
2. Generate multiple plot types for analysis
3. Save high-quality images for reports

Ready to dive deeper? Check out the full documentation!
