"""Test configuration and fixtures.

This module provides common fixtures and configuration for pytest.
It also ensures that the src directory is properly added to the Python path.
"""

import os
import sys
from pathlib import Path

# Disable OpenTelemetry during testing to prevent OTLP collector connection errors
os.environ["OTEL_SDK_DISABLED"] = "true"

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
