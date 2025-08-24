#!/usr/bin/env python3
"""
Launcher script for experiment supervision tools
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.monitoring.experiment_supervisor import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
