# Model Repository

This directory serves as the [Model Repository](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_repository.md) for Triton.

Artifacts exported by the CI/CD pipeline (e.g., ONNX, TensorRT models) should be placed here following the strict Triton hierarchy:

```
model_repository/
  <model-name>/
    config.pbtxt
    1/
      model.onnx
```
