from __future__ import annotations

from dataclasses import dataclass

{% if cookiecutter.ml_framework == 'pytorch' %}
import torch
from torch import nn


@dataclass
class Predictor:
    model: nn.Module
    device: str = "cpu"

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        self.model.eval()
        with torch.no_grad():
            x = x.to(self.device)
            logits = self.model(x)
            return logits.softmax(dim=-1)

{% elif cookiecutter.ml_framework == 'tensorflow' %}
import tensorflow as tf
import numpy as np


@dataclass
class Predictor:
    model: tf.keras.Model

    def predict_proba(self, x: np.ndarray | tf.Tensor) -> tf.Tensor:
        # Keras models usually output probabilities directly if activation is softmax
        # Otherwise, add softmax here. Assuming logic matches specific model.
        return self.model(x, training=False)
{% endif %}
