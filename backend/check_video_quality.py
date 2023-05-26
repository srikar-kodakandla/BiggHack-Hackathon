"""

This file is used to check the quality of the video and audio quality
The video quality is checked by using the variance of the laplacian of the image
The audio quality is checked by using the zero crossing rate of the audio
The video quality is normalized between 0 and 1
The audio quality is normalized between 0 and 1

"""

import cv2
import numpy as np
import librosa
from scipy import ndimage

def video_clarity(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.Laplacian(gray, cv2.CV_64F).var()
            frames.append(blur)
            frame = None
        else:
            break

    cap.release()

    max_value = max(frames)
    min_value = min(frames)
    frames = [(i-min_value)/(max_value-min_value) for i in frames]

    return np.mean(frames)

def audio_clarity(video_path):
    hop_length = 512
    zcr_arr = []

    for i in range(0, int(librosa.get_duration(filename=video_path)*22050), hop_length*512):
        y, sr = librosa.load(video_path, sr=None, mono=True, offset=i/22050, duration=hop_length/22050)
        zcr = librosa.feature.zero_crossing_rate(y).mean()
        zcr_arr.append(zcr)

    zcr = 1 - np.mean(zcr_arr)
    return zcr

video_path = 'demo.mp4'

def check_quality(video_path):
    return {"video_quality":video_clarity(video_path),"audio_quality":audio_clarity(video_path)}

