import logging
from datetime import datetime
from typing import Any, Callable, Mapping, Tuple

import torch
from app.ai.image_to_image import StableDiffusionImg2ImgPipeline, preprocess_init_image
from diffusers import LMSDiscreteScheduler, PNDMScheduler
from flask import send_file
from PIL import Image
from torch import autocast
from utils import helpers

MODEL_CACHE = "diffusers-cache"


class StableDiffusion:
    """This module will handle the inference pipeline for the pretrained stable diffusion model"""

    def __init__(
        self,
        model_name: str = "CompVis/stable-diffusion-v1-4",
        width: int = 512,
        height: int = 512,
        prompt_strength: float = 0.8,
        num_outputs: int = 1,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        seed: int = 7,
    ):

        self.model_name = model_name
        self.width = width
        self.height = height
        self.prompt_strength = prompt_strength
        self.num_outputs = num_outputs
        self.num_inference_steps = num_inference_steps
        self.guidance_scale = guidance_scale
        self.seed = seed

        try:
            # We will first use the PNDMS scheduler, then change depending on init_image
            scheduler = PNDMScheduler(
                beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
            )
            logging.info("loading model...")
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                scheduler=scheduler,
                torch_dtype=torch.float16,
                revision="fp16",
                cache_dir=MODEL_CACHE,
                local_files_only=True,
            ).to("cuda")

            logging.info("model loaded!")

        except Exception:
            raise RuntimeError(
                f"Model is deprecated; Could not load model: {self.model_name}"
            )

    def read_input(self, form: Mapping[str, Any]) -> Tuple[str, int, int, float, float]:
        """Read prompt and other arguments from the form."""

        prompt = form.get("prompt", None)
        num_outputs = form.get("n", self.num_outputs)
        num_inference_steps = form.get("num_inference_steps", self.num_inference_steps)
        guidance_scale = form.get("guidance_scale", self.guidance_scale)
        prompt_strength = form.get("prompt_strength", self.prompt_strength)

        if not prompt:
            raise ValueError("prompt did not set in request")
        return prompt, num_outputs, num_inference_steps, guidance_scale, prompt_strength

    def img2img(self, form: Mapping[str, Any]) -> Callable:
        pass

    @torch.inference_mode()
    @torch.cuda.amp.autocast()
    def text2img(self, form: Mapping[str, Any]) -> Callable:
        (
            prompt,
            num_outputs,
            num_inference_steps,
            guidance_scale,
            prompt_strength,
        ) = self.read_input(form)
        # use LMS without init images
        scheduler = LMSDiscreteScheduler(
            beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear"
        )
        self.pipe.scheduler = scheduler
        generator = torch.Generator("cuda").manual_seed(self.seed)
        output = self.pipe(
            prompt=[prompt] * 1 if prompt is not None else None,
            init_image=None,
            mask=None,
            width=self.width,
            height=self.height,
            prompt_strength=prompt_strength,
            guidance_scale=guidance_scale,
            generator=generator,
            num_inference_steps=num_inference_steps,
        )
        if any(output["nsfw_content_detected"]):
            raise Exception(
                "NSFW content detected, please try again with a different prompt"
            )
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        for i, sample in enumerate(output["sample"]):
            output_path = f"./images/{now}-out-{i}.png"
            sample.save(output_path)
        # Return image using flask's send_file method
        send_data = helpers.get_bytes(file_path=output_path)
        return send_file(send_data, download_name="test.jpeg")


print("defining model")
painter = StableDiffusion()
