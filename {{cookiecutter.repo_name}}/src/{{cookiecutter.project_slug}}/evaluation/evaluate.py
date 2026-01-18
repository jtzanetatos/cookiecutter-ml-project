from __future__ import annotations

from loguru import logger
from omegaconf import DictConfig

{% if cookiecutter.ml_framework == 'pytorch' %}
import pytorch_lightning as pl


def maybe_run_offline_eval(
    cfg: DictConfig,
    trainer: pl.Trainer,
    datamodule: pl.LightningDataModule,
    lightning_module: pl.LightningModule,
) -> None:
    if not bool(cfg.get("evaluation", {}).get("enabled", False)):
        return
    logger.info("Running offline evaluation...")
    trainer.test(lightning_module, datamodule=datamodule)

{% elif cookiecutter.ml_framework == 'tensorflow' %}
import tensorflow as tf

def maybe_run_offline_eval(
    cfg: DictConfig,
    model: tf.keras.Model,
    test_data: any, # Dataset or numpy arrays
) -> None:
    if not bool(cfg.get("evaluation", {}).get("enabled", False)):
        return
    logger.info("Running offline evaluation...")
    # metrics = model.evaluate(test_data)
    # logger.info(f"Test metrics: {metrics}")
    pass
{% endif %}
