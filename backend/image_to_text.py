"""
This file is used to generate the summary of the given image
This is done by using the pretrained model from the huggingface library called vit-gpt2-image-captioning
The model is used to generate the text from the image
The model is a vision encoder decoder model
The model is trained to generate the caption for the image

"""
"""
This script uses the VisionEncoderDecoderModel from the transformers library to generate video summaries based on image captions.
It utilizes the ViTImageProcessor and AutoTokenizer modules for image processing and tokenization.
The generated video summaries are based on the provided pre-trained model 'nlpconnect/vit-gpt2-image-captioning'.


Usage:
1. Make sure you have the required libraries installed.
2. Provide the path to the video you want to generate a summary for in the 'generate_video_summary' function.
3. Adjust the 'max_length' and 'num_beams' parameters according to your preferences.
4. Run the script.

Note: The script assumes that you have a CUDA-compatible GPU for faster processing. If not, it will fall back to CPU.

"""

from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import cv2
import numpy as np

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}
frame_rate = 5  

def generate_video_summary(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: Unable to open video file")
        return

    video_captions = []

    frame_counter = 0
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            if frame_counter % (frame_rate * video.get(cv2.CAP_PROP_FPS)) == 0:
                frame_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                pixel_values = feature_extractor(images=[frame_image], return_tensors="pt").pixel_values
                pixel_values = pixel_values.to(device)
                output_ids = model.generate(pixel_values, **gen_kwargs)
                caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

                video_captions.append(caption)

            frame_counter += 1
        else:
            break

    video.release()

    return '\n'.join(video_captions)
