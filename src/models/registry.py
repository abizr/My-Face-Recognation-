import os
import torch
from torch import nn
from loguru import logger


def load_model(model_path: str, device: str):
    """
    Load a face embedding model. Replace with ArcFace/InsightFace loader.
    """
    if os.path.exists(model_path):
        state = torch.load(model_path, map_location=device)
        model = state.get("model", state)
        if isinstance(model, nn.Module):
            model.to(device)
            logger.info(f"Loaded model from {model_path}")
            return model
    logger.warning("Model path missing; using Identity stub.")
    return nn.Identity().to(device)
