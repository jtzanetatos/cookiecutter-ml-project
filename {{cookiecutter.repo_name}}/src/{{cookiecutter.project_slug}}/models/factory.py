from __future__ import annotations

from omegaconf import DictConfig

from {{cookiecutter.project_slug}}.models.torch.nets import MLPClassifier
from {{cookiecutter.project_slug}}.models.lightning.modules import ClassificationModule

def build_lightning_module(cfg: DictConfig) -> ClassificationModule:
    n_features = int(cfg.data.get("n_features", 32))
    n_classes = int(cfg.data.get("n_classes", 2))
    hidden = int(cfg.model.get("hidden", 128))
    dropout = float(cfg.model.get("dropout", 0.0))
    lr = float(cfg.trainer.get("lr", 1e-3)) if "trainer" in cfg else float(cfg.model.get("lr", 1e-3))
    wd = float(cfg.trainer.get("weight_decay", 0.0)) if "trainer" in cfg else float(cfg.model.get("weight_decay", 0.0))

    model = MLPClassifier(n_features=n_features, n_classes=n_classes, hidden=hidden, dropout=dropout)
    return ClassificationModule(model=model, lr=lr, weight_decay=wd)
