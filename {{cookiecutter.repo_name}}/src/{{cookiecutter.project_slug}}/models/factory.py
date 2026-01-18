from omegaconf import DictConfig

{% if cookiecutter.ml_framework == 'pytorch' %}
from {{cookiecutter.project_slug}}.models.lightning.modules import ClassificationModule
from {{cookiecutter.project_slug}}.models.torch.nets import MLPClassifier


def build_lightning_module(cfg: DictConfig) -> ClassificationModule:
    n_features = int(cfg.data.get("n_features", 32))
    n_classes = int(cfg.data.get("n_classes", 2))
    hidden = int(cfg.model.get("hidden", 128))
    dropout = float(cfg.model.get("dropout", 0.0))
    lr = (
        float(cfg.trainer.get("lr", 1e-3))
        if "trainer" in cfg
        else float(cfg.model.get("lr", 1e-3))
    )
    wd = (
        float(cfg.trainer.get("weight_decay", 0.0))
        if "trainer" in cfg
        else float(cfg.model.get("weight_decay", 0.0))
    )

    model = MLPClassifier(
        n_features=n_features, n_classes=n_classes, hidden=hidden, dropout=dropout
    )
    return ClassificationModule(model=model, lr=lr, weight_decay=wd)

{% elif cookiecutter.ml_framework == 'tensorflow' %}
import tensorflow as tf
from tensorflow import keras

def build_keras_model(cfg: DictConfig, n_features: int, n_classes: int) -> keras.Model:
    hidden = int(cfg.model.get("hidden", 128))
    dropout = float(cfg.model.get("dropout", 0.0))
    lr = float(cfg.trainer.get("lr", 1e-3))

    model = keras.Sequential([
        keras.layers.Dense(hidden, activation='relu', input_shape=(n_features,)),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(n_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model
{% endif %}
