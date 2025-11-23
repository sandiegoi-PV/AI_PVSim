"""
AI PVSim - Video Analysis Module for Pole Vault Performance Tracking
This module provides accurate tracking of athlete movements and pole positions
in pole vault videos for performance analysis and comparison.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Dict, Optional
import json
from dataclasses import dataclass, asdict


@dataclass
class FrameData:
    """Data structure for storing frame analysis results"""
    frame_number: int
    timestamp: float
    athlete_keypoints: Dict[str, Tuple[float, float, float]]  # landmark_name: (x, y, visibility)
    pole_endpoints: Optional[Tuple[Tuple[float, float], Tuple[float, float]]]  # ((x1, y1), (x2, y2))
    pole_length_pixels: Optional[float]
    athlete_height_pixels: Optional[float]
    pole_angle: Optional[float]  # degrees from horizontal


class VideoAnalyzer:
    """
    Main class for analyzing pole vault videos.
    Tracks athlete pose and pole position with high accuracy.
    """
    
    def __init__(self, calibration_height_meters: float = 1.8):
        """
        Initialize the video analyzer.
        
        Args:
            calibration_height_meters: Known height for calibration (e.g., athlete height)
        """
        self.calibration_height_meters = calibration_height_meters
        self.pixels_per_meter = None
        
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,  # Most accurate model
            smooth_landmarks=True,
            enable_segmentation=False,
            smooth_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        self.frame_data: List[FrameData] = []
        
    def calibrate_scale(self, frame: np.ndarray, landmarks) -> Optional[float]:
        """
        Calibrate pixel-to-meter ratio using athlete's height.
        
        Args:
            frame: Video frame
            landmarks: MediaPipe pose landmarks
            
        Returns:
            Pixels per meter ratio or None if calibration fails
        """
        if landmarks:
            # Calculate athlete height from head to ankle
            image_height, image_width = frame.shape[:2]
            
            # Get head (nose) and ankle positions
            nose = landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
            left_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # Use the more visible ankle
            ankle = left_ankle if left_ankle.visibility > right_ankle.visibility else right_ankle
            
            # Calculate pixel height
            pixel_height = abs(
                (nose.y * image_height) - (ankle.y * image_height)
            )
            
            if pixel_height > 0:
                return pixel_height / self.calibration_height_meters
        
        return None
    
    def extract_keypoints(self, landmarks, image_width: int, image_height: int) -> Dict[str, Tuple[float, float, float]]:
        """
        Extract keypoint coordinates from MediaPipe landmarks.
        
        Args:
            landmarks: MediaPipe pose landmarks
            image_width: Frame width
            image_height: Frame height
            
        Returns:
            Dictionary of keypoint names to (x, y, visibility) tuples
        """
        keypoints = {}
        for idx, landmark in enumerate(landmarks.landmark):
            landmark_name = self.mp_pose.PoseLandmark(idx).name
            keypoints[landmark_name] = (
                landmark.x * image_width,
                landmark.y * image_height,
                landmark.visibility
            )
        return keypoints
    
    def detect_pole(self, frame: np.ndarray, landmarks) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Detect pole position using edge detection and line finding.
        The pole is typically a straight line in the frame.
        
        Args:
            frame: Video frame
            landmarks: MediaPipe pose landmarks for context
            
        Returns:
            Tuple of pole endpoints ((x1, y1), (x2, y2)) or None
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=100,
            minLineLength=100,
            maxLineGap=10
        )
        
        if lines is not None:
            # Filter for long, relatively vertical lines (pole is typically held vertically)
            valid_lines = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                
                # Pole can be at various angles, but typically > 30 degrees from horizontal
                if length > 100 and angle > 30:
                    valid_lines.append((length, ((x1, y1), (x2, y2))))
            
            # Return the longest line as the pole
            if valid_lines:
                longest_line = max(valid_lines, key=lambda x: x[0])
                return longest_line[1]
        
        return None
    
    def calculate_pole_angle(self, pole_endpoints: Tuple[Tuple[float, float], Tuple[float, float]]) -> float:
        """
        Calculate pole angle from horizontal.
        
        Args:
            pole_endpoints: Tuple of pole endpoints ((x1, y1), (x2, y2))
            
        Returns:
            Angle in degrees from horizontal
        """
        (x1, y1), (x2, y2) = pole_endpoints
        angle_rad = np.arctan2(y2 - y1, x2 - x1)
        angle_deg = np.degrees(angle_rad)
        return angle_deg
    
    def analyze_video(self, video_path: str, output_video_path: Optional[str] = None) -> List[FrameData]:
        """
        Analyze a pole vault video and extract movement data.
        
        Args:
            video_path: Path to input video
            output_video_path: Optional path to save annotated video
            
        Returns:
            List of FrameData objects containing analysis results
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup video writer if output path provided
        out = None
        if output_video_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        
        frame_number = 0
        self.frame_data = []
        
        print(f"Analyzing video: {video_path}")
        print(f"Resolution: {frame_width}x{frame_height}, FPS: {fps}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_number / fps
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame with MediaPipe Pose
            results = self.pose.process(rgb_frame)
            
            athlete_keypoints = {}
            athlete_height_pixels = None
            pole_endpoints = None
            pole_length_pixels = None
            pole_angle = None
            
            if results.pose_landmarks:
                # Calibrate scale on first detection
                if self.pixels_per_meter is None:
                    self.pixels_per_meter = self.calibrate_scale(frame, results.pose_landmarks)
                    if self.pixels_per_meter:
                        print(f"Scale calibrated: {self.pixels_per_meter:.2f} pixels per meter")
                
                # Extract keypoints
                athlete_keypoints = self.extract_keypoints(
                    results.pose_landmarks, frame_width, frame_height
                )
                
                # Calculate athlete height
                if 'NOSE' in athlete_keypoints and 'LEFT_ANKLE' in athlete_keypoints:
                    nose_y = athlete_keypoints['NOSE'][1]
                    left_ankle_y = athlete_keypoints['LEFT_ANKLE'][1]
                    right_ankle_y = athlete_keypoints['RIGHT_ANKLE'][1]
                    ankle_y = (left_ankle_y + right_ankle_y) / 2
                    athlete_height_pixels = abs(nose_y - ankle_y)
                
                # Detect pole
                pole_endpoints = self.detect_pole(frame, results.pose_landmarks)
                if pole_endpoints:
                    (x1, y1), (x2, y2) = pole_endpoints
                    pole_length_pixels = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    pole_angle = self.calculate_pole_angle(pole_endpoints)
                
                # Draw annotations on frame
                if output_video_path:
                    # Draw pose landmarks
                    self.mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                    )
                    
                    # Draw pole
                    if pole_endpoints:
                        (x1, y1), (x2, y2) = pole_endpoints
                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 3)
                        cv2.putText(frame, f"Pole: {pole_angle:.1f}deg", 
                                  (int(x1), int(y1) - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    
                    # Display measurements
                    if self.pixels_per_meter and athlete_height_pixels:
                        height_meters = athlete_height_pixels / self.pixels_per_meter
                        cv2.putText(frame, f"Height: {height_meters:.2f}m", 
                                  (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
                    if self.pixels_per_meter and pole_length_pixels:
                        length_meters = pole_length_pixels / self.pixels_per_meter
                        cv2.putText(frame, f"Pole: {length_meters:.2f}m", 
                                  (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Store frame data
            frame_data = FrameData(
                frame_number=frame_number,
                timestamp=timestamp,
                athlete_keypoints=athlete_keypoints,
                pole_endpoints=pole_endpoints,
                pole_length_pixels=pole_length_pixels,
                athlete_height_pixels=athlete_height_pixels,
                pole_angle=pole_angle
            )
            self.frame_data.append(frame_data)
            
            # Write annotated frame
            if out:
                out.write(frame)
            
            frame_number += 1
            
            if frame_number % 30 == 0:
                print(f"Processed {frame_number} frames...")
        
        cap.release()
        if out:
            out.release()
        
        print(f"Analysis complete. Processed {frame_number} frames.")
        return self.frame_data
    
    def export_data(self, output_path: str):
        """
        Export analysis data to JSON file for comparison with other athletes.
        
        Args:
            output_path: Path to output JSON file
        """
        data = {
            'calibration_height_meters': self.calibration_height_meters,
            'pixels_per_meter': self.pixels_per_meter,
            'total_frames': len(self.frame_data),
            'frames': []
        }
        
        for frame in self.frame_data:
            frame_dict = asdict(frame)
            data['frames'].append(frame_dict)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data exported to {output_path}")
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from the analyzed video.
        
        Returns:
            Dictionary containing performance statistics
        """
        stats = {
            'total_frames': len(self.frame_data),
            'avg_pole_angle': 0,
            'max_pole_angle': 0,
            'min_pole_angle': 0,
            'avg_athlete_height_pixels': 0,
            'avg_pole_length_pixels': 0,
        }
        
        pole_angles = [f.pole_angle for f in self.frame_data if f.pole_angle is not None]
        athlete_heights = [f.athlete_height_pixels for f in self.frame_data if f.athlete_height_pixels is not None]
        pole_lengths = [f.pole_length_pixels for f in self.frame_data if f.pole_length_pixels is not None]
        
        if pole_angles:
            stats['avg_pole_angle'] = np.mean(pole_angles)
            stats['max_pole_angle'] = np.max(pole_angles)
            stats['min_pole_angle'] = np.min(pole_angles)
        
        if athlete_heights:
            stats['avg_athlete_height_pixels'] = np.mean(athlete_heights)
            
        if pole_lengths:
            stats['avg_pole_length_pixels'] = np.mean(pole_lengths)
        
        if self.pixels_per_meter:
            stats['avg_athlete_height_meters'] = stats['avg_athlete_height_pixels'] / self.pixels_per_meter
            stats['avg_pole_length_meters'] = stats['avg_pole_length_pixels'] / self.pixels_per_meter
        
        return stats
    
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'pose'):
            self.pose.close()
