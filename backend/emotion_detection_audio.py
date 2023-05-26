from moviepy.editor import VideoFileClip
import numpy as np
import math
import cv2

def process_video(video_path, chunk_duration=5):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_duration = audio_clip.duration

    num_chunks = math.ceil(audio_duration / chunk_duration)

    output_dict = {'final_emotion': {}, 'complete_emotion': None}
    output_dict['emotion_for_chunks'] = {} 

    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, audio_duration)

        output_path = f"output_audio_chunk_{i}.wav"

        audio_chunk = audio_clip.subclip(start_time, end_time)
        audio_chunk.write_audiofile(output_path)

        text_lab = perform_sentiment_analysis(output_path)
        output_dict['emotion_for_chunks'][i+1] = text_lab

    complete_text_lab = perform_sentiment_analysis(video_path)
    output_dict['complete_emotion'] = complete_text_lab
    
    keys = list(np.arange(0, chunk_duration * 10, chunk_duration))
    
    values = list(output_dict['emotion_for_chunks'].values())
    if len(keys) == len(values):
        output_dict['emotion_for_chunks'] = dict(zip(keys, values))
    emotion_dict = {
    "neu": "Neutral",
    "N": "Neutral",
    "hap": "Happy",
    "H": "Happy",
    "sad": "Sad",
    "S": "Sad",
    "ang": "Angry",
    "A": "Angry",
    "fea": "Fearful",
    "F": "Fearful",
    "sur": "Surprise",
    "SU": "Surprise",
    "dis": "Disgust",
    "D": "Disgust"
    }

    output_dict['complete_emotion'] = [emotion_dict[emotion] for emotion in output_dict['complete_emotion']]
    output_dict['emotion_for_chunks'] = {key: [emotion_dict[emotion] for emotion in emotions] for key, emotions in output_dict['emotion_for_chunks'].items()}



    return output_dict

def perform_sentiment_analysis(audio_path):
    from speechbrain.pretrained.interfaces import foreign_class
    classifier = foreign_class(source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP", pymodule_file="custom_interface.py", classname="CustomEncoderWav2vec2Classifier")
    out_prob, score, index, text_lab = classifier.classify_file(audio_path)
    return text_lab

video_path = "demo.mp4"

def get_video_length(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    cap.release()

    return duration

def main_video(video_path):

    split_time=get_video_length(video_path)/9

    result_dict = process_video(video_path, chunk_duration=get_video_length(video_path)/9)
    return result_dict

