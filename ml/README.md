# 🤖 ML Training Guide

## Quick Start

### 1. Install Dependencies

```bash
cd ml
pip install -r requirements.txt
```

### 2. Prepare Your Data

Organize your data in this structure:

```
ml/data/
├── train/
│   ├── Positive/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── Negative/
│       ├── img1.jpg
│       └── ...
├── val/
│   ├── Positive/
│   └── Negative/
└── test/
    ├── Positive/
    └── Negative/
```

### 3. Train the Model

```bash
python train.py
```

Or with custom config:

```bash
python train.py --config custom_config.yaml
```

### 4. Evaluate the Model

```bash
python evaluate.py ../inference-service/models/model.h5 data/test
```

---

## Configuration

Edit `config.yaml` to customize:

- **Data paths**: Change `train_dir`, `val_dir`, `test_dir`
- **Model params**: Image size, architecture
- **Training params**: Batch size, epochs, learning rate
- **Output path**: Where to save the model

---

## Git LFS Setup

### First Time Setup

```bash
# Install Git LFS
brew install git-lfs  # macOS
# or
sudo apt-get install git-lfs  # Ubuntu

# Initialize in your repo
git lfs install

# Track model files (already done via .gitattributes)
git lfs track "*.h5"
```

### After Training

```bash
# Add the new model
git add inference-service/models/model.h5

# Commit with meaningful message
git commit -m "Update model: accuracy 95.2%"

# Push (triggers GitHub Actions)
git push origin main
```

---

## GitHub Actions Automation

### Setup Secrets

1. Go to your GitHub repo settings
2. Navigate to **Secrets and variables** > **Actions**
3. Add these secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token

### What Happens on Push

1. ✅ Model file is validated
2. ✅ Docker image is built with new model
3. ✅ Image is pushed to Docker Hub
4. ✅ Notification sent

### Monitor Deployments

- Check **Actions** tab on GitHub
- View build logs
- See deployment summary

---

## Model Training Tips

### Data Preparation

- **Balance classes**: Equal Positive/Negative samples
- **Image quality**: Good resolution, not corrupted
- **Data split**: 70% train, 15% val, 15% test

### Hyperparameter Tuning

```yaml
# In config.yaml
training:
  batch_size: 32        # Try: 16, 32, 64
  epochs: 50            # Adjust based on convergence
  learning_rate: 0.001  # Try: 0.0001, 0.001, 0.01
```

### Monitoring Training

```bash
# Launch TensorBoard
tensorboard --logdir logs/

# Open browser
# http://localhost:6006
```

---

## Troubleshooting

### Out of Memory

```yaml
# Reduce batch size in config.yaml
training:
  batch_size: 16  # Instead of 32
```

### Model Not Converging

- Reduce learning rate
- Increase epochs
- Check data quality
- Try data augmentation

### Git LFS Issues

```bash
# Pull LFS files
git lfs pull

# Check LFS status
git lfs ls-files

# Re-track if needed
git lfs track "*.h5"
git add .gitattributes
git commit -m "Update Git LFS tracking"
```

---

## Advanced: Transfer Learning

For better results, use transfer learning:

```python
# In train.py, replace build_model() with:
from tensorflow.keras.applications import ResNet50

def build_transfer_model(input_shape=(128, 128, 3)):
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    base_model.trainable = False  # Freeze base
    
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    
    return model
```

---

## Next Steps

1. ✅ Train your first model
2. ✅ Evaluate metrics
3. ✅ Push to Git
4. ✅ Verify GitHub Actions deployment
5. ✅ Test in production

Happy training! 🚀
