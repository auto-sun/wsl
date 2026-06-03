# Model Weights

Place the trained dragon fruit disease detection model here:

```text
models/dragonfruit_disease_yolov8s.pt
```

The backend reads this path by default through `AI_MODEL_PATH`.

If the file is missing, the diagnosis API keeps using the mock fallback so the demo flow still works.
