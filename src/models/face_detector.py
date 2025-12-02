from typing import Optional
from PIL import Image


def detect_face(img: Image.Image) -> Optional[Image.Image]:
    """
    Placeholder face detector: returns a centered square crop.
    Swap with RetinaFace/MTCNN for production.
    """
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    return img.crop((left, top, left + side, top + side))
