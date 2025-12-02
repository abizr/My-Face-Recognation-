import io
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from loguru import logger

from src.config import Settings
from src.models.face_detector import detect_face
from src.models.registry import load_model


class FaceEmbedder:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = load_model(settings.model_path, self.device)
        self.model_version = settings.model_version
        self.preproc_hash = settings.preproc_hash
        self.transform = transforms.Compose(
            [
                transforms.Resize((112, 112)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
            ]
        )
        logger.info(f"Embedder ready on {self.device} with version {self.model_version}")

    @torch.inference_mode()
    def embed(self, img_bytes: bytes) -> np.ndarray:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        face = detect_face(img)
        if face is None:
            raise ValueError("No face detected")
        x = self.transform(face).unsqueeze(0).to(self.device)
        feats = self.model(x)
        if isinstance(feats, (list, tuple)):
            feats = feats[0]
        feats = torch.nn.functional.normalize(feats, dim=1)
        return feats.cpu().numpy().astype("float32")[0]
