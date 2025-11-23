"""
Video Processing Module
Handles video input, frame extraction, and pose estimation
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional


class VideoProcessor:
    """Process pole vault videos and extract pose landmarks"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def process_video(self, video_path: str) -> Tuple[List[np.ndarray], List[dict], dict]:
        """
        Process video and extract pose landmarks for each frame
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Tuple of (frames, landmarks_list, video_info)
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        video_info = {
            'fps': fps,
            'width': frame_width,
            'height': frame_height,
            'total_frames': total_frames
        }
        
        frames = []
        landmarks_list = []
        frame_count = 0
        
        print(f"Processing video: {video_path}")
        print(f"FPS: {fps}, Resolution: {frame_width}x{frame_height}, Total frames: {total_frames}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.pose.process(frame_rgb)
            
            frames.append(frame)
            
            if results.pose_landmarks:
                # Extract landmarks as dictionary
                landmarks = self._extract_landmarks(results.pose_landmarks, frame_height, frame_width)
                landmarks_list.append(landmarks)
            else:
                landmarks_list.append(None)
            
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processed {frame_count}/{total_frames} frames")
        
        cap.release()
        print(f"Video processing complete. Processed {frame_count} frames.")
        
        return frames, landmarks_list, video_info
    
    def _extract_landmarks(self, pose_landmarks, frame_height: int, frame_width: int) -> dict:
        """Extract pose landmarks into a structured dictionary"""
        landmarks = {}
        
        # Key landmarks for pole vault analysis
        landmark_names = [
            'NOSE', 'LEFT_SHOULDER', 'RIGHT_SHOULDER',
            'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST',
            'LEFT_HIP', 'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE',
            'LEFT_ANKLE', 'RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL',
            'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX'
        ]
        
        for name in landmark_names:
            landmark_id = getattr(self.mp_pose.PoseLandmark, name)
            landmark = pose_landmarks.landmark[landmark_id]
            landmarks[name.lower()] = {
                'x': landmark.x * frame_width,
                'y': landmark.y * frame_height,
                'z': landmark.z * frame_width,  # Normalized depth
                'visibility': landmark.visibility
            }
        
        return landmarks
    
    def visualize_landmarks(self, frame: np.ndarray, landmarks: Optional[dict]) -> np.ndarray:
        """
        Visualize pose landmarks on a frame
        
        Args:
            frame: Video frame
            landmarks: Dictionary of landmarks
            
        Returns:
            Frame with landmarks drawn
        """
        annotated_frame = frame.copy()
        
        if landmarks is None:
            return annotated_frame
        
        # Draw key points
        for name, lm in landmarks.items():
            if lm['visibility'] > 0.5:
                x, y = int(lm['x']), int(lm['y'])
                cv2.circle(annotated_frame, (x, y), 5, (0, 255, 0), -1)
        
        return annotated_frame
    
    def close(self):
        """Release resources"""
        self.pose.close()
