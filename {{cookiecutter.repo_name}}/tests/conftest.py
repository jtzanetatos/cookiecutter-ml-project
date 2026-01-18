
import pytest
from pathlib import Path
import os
import sys

# Ensure src is in path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

{% if cookiecutter.ml_framework == 'pytorch' %}
import shutil
import pytorch_lightning as pl
import torch
import numpy as np

@pytest.fixture(scope="session", autouse=True)
def seed_everything():
    """Set a fixed seed for reproducible tests."""
    pl.seed_everything(42, workers=True)

@pytest.fixture
def tmp_path_with_logs(tmp_path):
    """Fixture providing a temp dir that cleans up lightning logs."""
    yield tmp_path
    if (tmp_path / "lightning_logs").exists():
        shutil.rmtree(tmp_path / "lightning_logs")

{% elif cookiecutter.ml_framework == 'tensorflow' %}
import tensorflow as tf
import numpy as np
import random

@pytest.fixture(scope="session", autouse=True)
def seed_everything():
    """Set a fixed seed for reproducible tests."""
    np.random.seed(42)
    random.seed(42)
    tf.random.set_seed(42)
{% endif %}

@pytest.fixture(scope="session")
def root_dir():
    """Return the root directory of the repository."""
    return PROJECT_ROOT

@pytest.fixture
def cfg_train_global(root_dir):
    """(Optional) Return a specific config for testing training."""
    # This is a placeholder for loading hydra config in tests if needed
    pass
