NLU training

This script trains a simple spaCy text classification model (TextCategorizer) using labeled examples in `tenali/ml_models/data/Intent.json`.

Usage

1. Ensure `spaCy` is installed and you have the required packages (already in `requirements.txt`).
2. From the repository root, run:

```bash
python -m tenali.ml_models.training.train_nlu
```

3. The trained model will be saved to `tenali/nlu_model` by default.

Notes

- The training script is intentionally simple and designed for small datasets and quick iteration. For production-quality models use proper training configs and evaluation.
- You can update `train_nlu.py` to change training iterations or model architecture.
