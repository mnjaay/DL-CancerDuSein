"""
Script d'évaluation du modèle
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    precision_recall_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import argparse


def load_test_data(test_dir, img_height=128, img_width=128, batch_size=32):
    """Charger les données de test"""
    
    test_ds = keras.preprocessing.image_dataset_from_directory(
        test_dir,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode='binary',
        shuffle=False
    )
    
    # Normalize
    normalization_layer = keras.layers.Rescaling(1./255)
    test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y))
    
    return test_ds


def evaluate_model(model_path, test_ds, output_dir='evaluation'):
    """Évaluer le modèle sur les données de test"""
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load model
    print(f"📦 Loading model from {model_path}...")
    model = keras.models.load_model(model_path)
    
    # Evaluate
    print("\n📊 Evaluating model...")
    results = model.evaluate(test_ds, verbose=1)
    
    metrics_names = model.metrics_names
    eval_metrics = dict(zip(metrics_names, results))
    
    print("\n✅ Evaluation Metrics:")
    for metric, value in eval_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Get predictions
    print("\n🔍 Getting predictions...")
    y_true = []
    y_pred_proba = []
    
    for images, labels in test_ds:
        predictions = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred_proba.extend(predictions.flatten())
    
    y_true = np.array(y_true)
    y_pred_proba = np.array(y_pred_proba)
    y_pred = (y_pred_proba > 0.5).astype(int)
    
    # Classification Report
    print("\n📋 Classification Report:")
    class_report = classification_report(
        y_true,
        y_pred,
        target_names=['Negative', 'Positive'],
        output_dict=True
    )
    print(classification_report(y_true, y_pred, target_names=['Negative', 'Positive']))
    
    # Save classification report
    with open(output_dir / 'classification_report.json', 'w') as f:
        json.dump(class_report, f, indent=2)
    
    # Confusion Matrix
    print("\n🔢 Creating confusion matrix...")
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=['Negative', 'Positive'],
        yticklabels=['Negative', 'Positive'],
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_dir / 'confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Confusion matrix saved to {output_dir / 'confusion_matrix.png'}")
    
    # ROC Curve
    print("\n📈 Creating ROC curve...")
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(10, 8))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic (ROC) Curve', fontsize=16, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'roc_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ ROC curve saved to {output_dir / 'roc_curve.png'}")
    
    # Precision-Recall Curve
    print("\n📊 Creating precision-recall curve...")
    precision, recall, pr_thresholds = precision_recall_curve(y_true, y_pred_proba)
    pr_auc = auc(recall, precision)
    
    plt.figure(figsize=(10, 8))
    plt.plot(recall, precision, color='darkgreen', lw=2, label=f'PR curve (AUC = {pr_auc:.4f})')
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Precision-Recall Curve', fontsize=16, fontweight='bold')
    plt.legend(loc="lower left", fontsize=10)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / 'precision_recall_curve.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Precision-Recall curve saved to {output_dir / 'precision_recall_curve.png'}")
    
    # Save all metrics
    all_metrics = {
        'evaluation_metrics': eval_metrics,
        'classification_report': class_report,
        'confusion_matrix': cm.tolist(),
        'roc_auc': float(roc_auc),
        'pr_auc': float(pr_auc),
        'threshold_0.5': {
            'accuracy': float(np.mean(y_pred == y_true)),
            'precision': float(class_report['Positive']['precision']),
            'recall': float(class_report['Positive']['recall']),
            'f1_score': float(class_report['Positive']['f1-score'])
        }
    }
    
    with open(output_dir / 'metrics_complete.json', 'w') as f:
        json.dump(all_metrics, f, indent=2)
    
    print(f"\n✅ Complete metrics saved to {output_dir / 'metrics_complete.json'}")
    
    return all_metrics


def main():
    parser = argparse.ArgumentParser(description='Evaluate cancer detection model')
    parser.add_argument('model_path', type=str, help='Path to the model file')
    parser.add_argument('test_dir', type=str, help='Path to test data directory')
    parser.add_argument('--output', type=str, default='evaluation', help='Output directory for results')
    parser.add_argument('--img-size', type=int, default=128, help='Image size (height and width)')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔬 Model Evaluation")
    print("=" * 60)
    
    # Load test data
    print(f"\n📂 Loading test data from {args.test_dir}...")
    test_ds = load_test_data(
        args.test_dir,
        img_height=args.img_size,
        img_width=args.img_size,
        batch_size=args.batch_size
    )
    
    # Evaluate
    metrics = evaluate_model(args.model_path, test_ds, args.output)
    
    print("\n" + "=" * 60)
    print("✅ Evaluation completed successfully!")
    print(f"📁 Results saved to {args.output}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
