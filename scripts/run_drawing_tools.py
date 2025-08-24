#!/usr/bin/env python3
"""
Launcher script for experiment drawing tools
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.visualization.experiment_drawing import mcp

if __name__ == "__main__":
    mcp.run()
