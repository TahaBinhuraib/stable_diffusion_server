import os
import sys

import torch
from diffusers import StableDiffusionPipeline

os.makedirs("diffusers-cache", exist_ok=True)
token = os.getenv("HUGGINGFACE_API")

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    cache_dir="diffusers-cache",
    revision="fp16",
    torch_dtype=torch.float16,
    use_auth_token=token,
)
