import io
import os
# import torch
import inspect
import datetime
import warnings
from PIL import Image
# from tqdm.auto import tqdm
# from torch import autocast
from fastapi import FastAPI, File, UploadFile
# from diffusers import StableDiffusionImg2ImgPipeline
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Response

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = "cuda"
model_path = "CompVis/stable-diffusion-v1-4"

# pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
#     model_path,
#     revision="fp16",
#     torch_dtype=torch.float16,
#     use_auth_token=True
# )
# pipe = pipe.to(device)



async def resize_image_bytes(image: File):
    original_image = await Image.open(io.BytesIO(await image.read())).convert("RGB")
    original_image = original_image.resize((500, 500))
    image_bytes = original_image.tobytes()
    return image_bytes

async def saved_generated_image(image: File):
    output_folder = "out"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_filename = os.path.join(
        output_folder, f"output-{int(datetime.datetime.now().timestamp())}.png"
    )
    image.save(output_filename)
    return output_filename.split("/")[-1]


@app.post("/image")
async def generate(image: bytes = File(...)):
    resized_image_bytes = await resize_image_bytes(image)
    # generator = torch.Generator(device=device)
    with autocast("cuda"):
        generated_image = await pipe(prompt="cute, beautiful", init_image=resized_image_bytes, strength=0.75, guidance_scale=7.5, generator=generator).images[0]
    # output_filename = await saved_generated_image(generated_image)
    return {"file_name": resized_image_bytes}


@app.get("/get/{filename}")
async def get_image(filename: str):
    with open(f"out/{filename}", "rb") as f:
        return Response(f.read(), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


async def convert_uploadfile_to_png(upload_file: UploadFile):
    image = Image.open(upload_file.file)
    png_image = image.convert('RGB')
    png_image_bytes = io.BytesIO()
    png_image.save(png_image_bytes, format='PNG')
    png_image_bytes = png_image_bytes.getvalue()
    return png_image_bytes
