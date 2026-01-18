from omegaconf import DictConfig

{% if cookiecutter.ml_framework == 'pytorch' %}
from {{cookiecutter.project_slug}}.data.datamodule import DataModuleConfig, RandomDataModule
from {{cookiecutter.project_slug}}.data.datasets import RandomDatasetConfig
from {{cookiecutter.project_slug}}.data.transforms import Identity
{% else %}
from dataclasses import dataclass
@dataclass
class RandomDataModule:
    n_features: int
    n_classes: int
{% endif %}


def build_datamodule(cfg: DictConfig) -> RandomDataModule:
    {% if cookiecutter.ml_framework == 'pytorch' %}
    ds_cfg = RandomDatasetConfig(
        n_samples=int(cfg.data.get("n_samples", 1024)),
        n_features=int(cfg.data.get("n_features", 32)),
        n_classes=int(cfg.data.get("n_classes", 2)),
    )
    dm_cfg = DataModuleConfig(
        batch_size=int(cfg.data.get("batch_size", 64)),
        num_workers=int(cfg.data.get("num_workers", 0)),
        pin_memory=bool(cfg.data.get("pin_memory", False)),
        persistent_workers=bool(cfg.data.get("persistent_workers", False)),
        seed=int(cfg.get("seed", 42)),
        val_frac=float(cfg.data.get("val_frac", 0.1)),
        test_frac=float(cfg.data.get("test_frac", 0.1)),
    )
    transform = Identity()
    return RandomDataModule(ds_cfg, dm_cfg, transform=transform)
    {% else %}
    return RandomDataModule(
        n_features=int(cfg.data.get("n_features", 32)),
        n_classes=int(cfg.data.get("n_classes", 2)),
    )
    {% endif %}
