{% if cookiecutter.ml_framework == 'pytorch' %}

from dataclasses import dataclass
from typing import Callable, Optional

import torch
from torch.utils.data import Dataset


@dataclass(frozen=True)
class RandomDatasetConfig:
    n_samples: int = 1000
    n_features: int = 32
    n_classes: int = 2


class RandomClassificationDataset(Dataset):
    """
    A synthetic dataset for classification tasks.
    """

    def __init__(
        self,
        cfg: RandomDatasetConfig,
        transform: Optional[Callable] = None,
        seed: int = 42,
    ):
        self.cfg = cfg
        self.transform = transform
        
        # Determine generator for reproducibility
        g = torch.Generator()
        g.manual_seed(seed)
        
        self.X = torch.randn(cfg.n_samples, cfg.n_features, generator=g)
        self.y = torch.randint(0, cfg.n_classes, (cfg.n_samples,), generator=g)

    def __len__(self) -> int:
        return self.cfg.n_samples

    def __getitem__(self, idx: int):
        x, y = self.X[idx], self.y[idx]
        if self.transform:
            x = self.transform(x)
        return x, y

{% elif cookiecutter.ml_framework == 'tensorflow' %}

from dataclasses import dataclass
import tensorflow as tf
import numpy as np

@dataclass(frozen=True)
class RandomDatasetConfig:
    n_samples: int = 1000
    n_features: int = 32
    n_classes: int = 2

class RandomClassificationDataset:
    """
    A synthetic dataset factory for TensorFlow.
    Returns a tf.data.Dataset object.
    """
    def __init__(self, cfg: RandomDatasetConfig, seed: int = 42):
        self.cfg = cfg
        self.seed = seed

    def build(self) -> tf.data.Dataset:
        # Use numpy for generation with fixed seed
        rng = np.random.default_rng(self.seed)
        X = rng.standard_normal((self.cfg.n_samples, self.cfg.n_features), dtype=np.float32)
        y = rng.integers(0, self.cfg.n_classes, size=(self.cfg.n_samples,), dtype=np.int32)
        
        # Create dataset from tensor slices
        ds = tf.data.Dataset.from_tensor_slices((X, y))
        return ds

{% endif %}
