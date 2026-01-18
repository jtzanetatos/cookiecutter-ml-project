from __future__ import annotations

import os
import random

import numpy as np

{% if cookiecutter.ml_framework == 'pytorch' %}
import torch
import pytorch_lightning as pl

def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    pl.seed_everything(seed, workers=True)
    os.environ["PYTHONHASHSEED"] = str(seed)

{% elif cookiecutter.ml_framework == 'tensorflow' %}
import tensorflow as tf

def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
{% endif %}
