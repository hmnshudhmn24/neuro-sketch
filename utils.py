"""Utility helpers for NEUROSKETCH"""
import os, yaml
def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
def clamp01(x):
    return max(0.0, min(1.0, x))
