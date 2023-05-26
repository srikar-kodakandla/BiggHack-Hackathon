    """
This file is used to detect the emotions in the video
The emotions are detected by using the FER library
The video is divided in to 10 chunks 
The emotions are detected for every chunk and the dominant emotion is taken for every chunk
The emotions are plotted for the whole video and for each chunk of the video and saved in 'data' directory
The video input is first converted to frames and then decreased it's quality to 480x360 for faster processing


    """

import cv2
import os
from fer import Video
from fer import FER
import os
import sys
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from collections import Counter
from tqdm import tqdm


def get_video_frames(video_path):
    if not os.path.isfile(video_path):
        print("File does not exist")
        return None
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frames_dict = {}
    frame_index = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if frame_index % int(fps/2) == 0:
            timestamp = frame_index / fps
            frame = cv2.resize(frame, (480, 360))
            frames_dict[timestamp] = frame
        frame_index += 1
    video.release()
    return frames_dict


def get_features(video_name,split_time=10):
    return_features=dict()
    frames_dict = get_video_frames(video_name)

    def get_frames(start_time,end_time):
        frames_1_to_10_secs = []
        for timestamp in sorted(frames_dict.keys()):
            if start_time <= timestamp <= end_time:
                frames_1_to_10_secs.append(frames_dict[timestamp])
        return frames_1_to_10_secs

    last_time=sorted(frames_dict.keys())[-1]

    all_frames=[]
    import numpy as np
    for time in np.arange(0,last_time,split_time):
        all_frames.append(get_frames(time,time+split_time))

    from fer import FER
    emo_detector = FER(mtcnn=True)
    from tqdm.auto import tqdm
    step_count = 0
    timeframe_multiple_people = dict()
    emotion=dict()
    for part in tqdm(all_frames,desc="counting persons in the video"):
        step_count += 1
        timeframe_multiple_people[step_count]=[]
        emotion[step_count]=[]
        for frames in part:
            test_image_two = frames
            captured_emotions_two = emo_detector.detect_emotions(test_image_two)
            dominant_emotion_two, emotion_score_two = emo_detector.top_emotion(test_image_two)
            no_of_persons = len(captured_emotions_two)
            #if no_of_persons > 1:
            #    print(f"Multiple people were detected ,{no_of_persons}")
            timeframe_multiple_people[step_count].append(no_of_persons)
            emotion[step_count].append(dominant_emotion_two)
            #print(dominant_emotion_two, emotion_score_two)



    final_emotion = {}
    for key, values in emotion.items():
        word_count = Counter(filter(lambda x: x is not None, values))
        top_words = [word for word, count in word_count.most_common(2)]
        final_emotion[key] = top_words

    #print(final_emotion)

    people_count = {}

    for key, values in timeframe_multiple_people.items():
        max_value = max(values)
        people_count[key] = max_value

    #print(people_count)





    location_videofile = video_name 
    cap = cv2.VideoCapture(location_videofile)
    fps = cap.get(cv2.CAP_PROP_FPS)
    desired_fps = 10
    frame_skip = int(fps/desired_fps)
    face_detector = FER(mtcnn=True)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    processing_data = []

    frame_count = 0
    with tqdm(total=total_frames, desc='Analyzing the emotions in the video', unit='frame') as pbar:
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                if frame_count % frame_skip == 0:  
                    height, width = frame.shape[:2]
                    new_height = 720
                    new_width = int(new_height * width / height)
                    resized_frame = cv2.resize(frame, (new_width, new_height))
                    
                    frame_result = face_detector.detect_emotions(resized_frame)
                    processing_data.append([frame_count/fps, frame_result])
                frame_count += 1
                pbar.update(1) 
            else: 
                break

    cap.release()


    input_video = Video(location_videofile)

    #vid_df = input_video.to_pandas(processing_data)
    vid_df = pd.DataFrame(processing_data)
    def get_largest_face(data):
        max_size = 0
        max_face = None

        for face in data:
            box = face['box']
            size = box[2] * box[3] 
            if size > max_size:
                max_size = size
                max_face = face
        return max_face

    vid_df['faces'] = vid_df[1].apply(get_largest_face)
    vid_df['faces']=vid_df['faces'].apply(lambda x: x['emotions'] if x is not None else 0)
    
    vid_df.drop(columns=1,inplace=True)
    vid_df.rename(columns={0:"Time in seconds"},inplace=True)
    vid_df.set_index("Time in seconds",inplace=True)
    if 0 in vid_df.columns:
        vid_df = vid_df.drop(columns=0)
    vid_df = vid_df['faces'].apply(pd.Series)
    #vid_df = input_video.get_first_face(vid_df)
    #vid_df = input_video.get_emotions(vid_df)
    
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Plotting the emotions against time in the video
    #pltfig = vid_df.plot().get_figure()
    
    #plt.savefig('plot.png')

    try:
        os.mkdir('data')
    except:
        pass
    
    for emotion in vid_df.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        vid_df[emotion] = pd.to_numeric(vid_df[emotion], errors='coerce')
        vid_df = vid_df.dropna(subset=[emotion])

        vid_df.plot(y=emotion, ax=ax, title=emotion)
        
        ax.set_ylim([0, 1])
        
        #plt.tight_layout()
        plt.ylabel("Confidence")
        plt.savefig(f'data/{emotion}.png') 
        
        plt.close(fig)

    vid_df.dropna(inplace=True)
    angry = sum(vid_df.angry)
    disgust = sum(vid_df.disgust)
    fear = sum(vid_df.fear)
    happy = sum(vid_df.happy)
    sad = sum(vid_df.sad)
    surprise = sum(vid_df.surprise)
    neutral = sum(vid_df.neutral)

    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]
    
    score_comparisons = pd.DataFrame(emotions, columns = ['Human Emotions'])
    score_comparisons['Emotion Value from the Video'] = emotions_values

    return_features['score_comparisons']=score_comparisons
    return_features['final_emotion']=final_emotion
    return_features['people_count']=people_count
    return_features['vid_df']=vid_df
    keys = list(np.arange(0, split_time * 10, split_time))
    
    values = list(return_features['final_emotion'].values())
    if len(keys) == len(values):
        return_features['final_emotion'] = dict(zip(keys, values))
    
    values = list(return_features['people_count'].values())
    if len(keys) == len(values):
        return_features['people_count'] = dict(zip(keys, values))
    
    df = return_features["score_comparisons"]

    scaler = MinMaxScaler()

    num_cols = df.select_dtypes(include=np.number).columns

    df[num_cols] = scaler.fit_transform(df[num_cols])

    return_features["score_comparisons"] = df
    
    df = return_features["score_comparisons"]

    scaler = MinMaxScaler()

    num_cols = df.select_dtypes(include=np.number).columns

    df[num_cols] = scaler.fit_transform(df[num_cols])

    return_features["score_comparisons"] = df
    return return_features




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

def main_function(video_name):
    split_time=get_video_length(video_name)/10
    output=(get_features(video_name,split_time=split_time))
    return output
