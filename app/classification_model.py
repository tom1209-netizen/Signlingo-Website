import mediapipe as mp
from sklearn.preprocessing import MinMaxScaler
import cv2
import numpy as np
import tensorflow as tf

# Model
# LSTM INPUT SIZE
INPUT_SHAPE = (30, 1086)

# MEDIAPIPE HOLISTIC
POSE_NUM_LANDMARK = 33
LEFT_HAND_NUM_LANDMARK = 21
RIGHT_HAND_NUM_LANDMARK = 21
FACE_NUM_LANDMARK = 468

classes = [
    'apple', 'architect', 'artist', 'autumn', 'banana', 'bird', 'black', 'blue',
    'brown', 'candy', 'cat', 'cow', 'dad', 'day', 'director', 'dog',
    'gold - silver', 'grapes', 'green', 'hamburger', 'horse', 'lemon', 'milk',
    'mom', 'month', 'night', 'orange', 'pear', 'pig', 'pizza', 'red',
    'sheep', 'spring', 'summer', 'uncle', 'week', 'white', 'will-(future)',
    'winter', 'worker'
]


mp_holistic = mp.solutions.holistic


def apply_mediapipe_holistic(frame):
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # Convert the frame to RGB as Mediapipe Holistic requires RGB input
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image=frame_rgb)

        # Initialize list to store the coordinates
        coordinates = []

        # Pose landmark
        if results.pose_landmarks is not None:
            for landmark in results.pose_landmarks.landmark:
                coordinates.extend([landmark.x, landmark.y])
        else:
            # Add zeros for the pose landmarks if nothing is detected
            num_pose_landmarks = POSE_NUM_LANDMARK * 2
            coordinates.extend([0.0] * num_pose_landmarks)

        # Left-hand landmark
        if results.left_hand_landmarks is not None:
            for landmark in results.left_hand_landmarks.landmark:
                coordinates.extend([landmark.x, landmark.y])
        else:
            # Add zeros for the left-hand landmarks if nothing is detected
            num_left_hand_landmarks = LEFT_HAND_NUM_LANDMARK * 2
            coordinates.extend([0.0] * num_left_hand_landmarks)

        # Right-hand landmark
        if results.right_hand_landmarks is not None:
            for landmark in results.right_hand_landmarks.landmark:
                coordinates.extend([landmark.x, landmark.y])
        else:
            # Add zeros for the right-hand landmarks if nothing is detected
            num_right_hand_landmarks = RIGHT_HAND_NUM_LANDMARK * 2
            coordinates.extend([0.0] * num_right_hand_landmarks)

        # Face landmark
        if results.face_landmarks is not None:
            for landmark in results.face_landmarks.landmark:
                coordinates.extend([landmark.x, landmark.y])
        else:
            # Add zeros for the face landmarks if nothing is detected
            num_face_landmarks = FACE_NUM_LANDMARK * 2
            coordinates.extend([0.0] * num_face_landmarks)

        return np.array(coordinates)


def extract_frames(video_frames):
    frames = []
    total_frames = int(len(video_frames))
    required_frames = 30

    # Calculate the frame interval to extract exactly 30 frames
    frame_interval = max(1, total_frames // required_frames)

    for frame_idx in range(0, total_frames, frame_interval):
        if len(frames) >= required_frames:
            break

        frame = video_frames[frame_idx]

        # Apply mediapipe_holistic
        frame = apply_mediapipe_holistic(frame)
        frames.append(frame)

    return np.array(frames)


def classify_video(video_frames, model):
    # data shape is (30, 1086)
    data = extract_frames(video_frames)
    data = np.expand_dims(data, axis=0)
    prediction = model.predict(data)
    predicted_classes = tf.argmax(prediction, axis=-1).numpy()[0]
    return predicted_classes
