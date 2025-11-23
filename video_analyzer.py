"""
Video Analysis Module for Pole Vault
This module provides functionality to analyze pole vault videos using pose detection.
"""

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class PoleVaultAnalyzer:
    """Analyzes pole vault videos to extract movement data and detect inconsistencies."""
    
    # Configuration constants
    LOW_VISIBILITY_THRESHOLD = 0.5  # Minimum confidence for landmark visibility
    LOW_VISIBILITY_COUNT_THRESHOLD = 5  # Number of low visibility landmarks to flag a frame
    SUDDEN_MOVEMENT_THRESHOLD = 0.3  # Maximum position change (as fraction of frame) between frames
    
    def __init__(self):
        """Initialize the analyzer with MediaPipe pose detection."""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # Use model complexity 1 instead of 2
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.results_data = []
        
    def download_video(self, url: str, output_path: str = "videos") -> Optional[str]:
        """
        Download a video from a URL using yt-dlp.
        
        Args:
            url: The URL of the video to download
            output_path: Directory to save the video
            
        Returns:
            Path to the downloaded video file, or None if failed
        """
        import yt_dlp
        
        os.makedirs(output_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True,  # Suppress verbose output
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"Downloaded: {filename}")
                return filename
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None
    
    def analyze_video(self, video_path: str) -> Dict:
        """
        Analyze a pole vault video and extract pose data.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing analysis results
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        
        print(f"Analyzing video: {video_path}")
        print(f"FPS: {fps}, Frames: {frame_count}, Duration: {duration:.2f}s")
        
        frame_data = []
        frame_num = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                landmarks = self._extract_landmarks(results.pose_landmarks, frame_num, fps)
                frame_data.append(landmarks)
            
            frame_num += 1
            
            # Progress indicator
            if frame_num % 30 == 0:
                print(f"Processed {frame_num}/{frame_count} frames ({frame_num/frame_count*100:.1f}%)")
        
        cap.release()
        
        analysis_results = {
            'video_path': video_path,
            'fps': fps,
            'frame_count': frame_count,
            'duration': duration,
            'frames_analyzed': len(frame_data),
            'frame_data': frame_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return analysis_results
    
    def _extract_landmarks(self, pose_landmarks, frame_num: int, fps: float) -> Dict:
        """
        Extract relevant landmarks from pose detection results.
        
        Args:
            pose_landmarks: MediaPipe pose landmarks
            frame_num: Current frame number
            fps: Frames per second
            
        Returns:
            Dictionary of landmark positions and calculated metrics
        """
        landmarks = {}
        landmarks['frame'] = frame_num
        landmarks['time'] = frame_num / fps if fps > 0 else 0
        
        # Extract key points for pole vault analysis
        key_points = {
            'nose': self.mp_pose.PoseLandmark.NOSE,
            'left_shoulder': self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            'right_shoulder': self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            'left_elbow': self.mp_pose.PoseLandmark.LEFT_ELBOW,
            'right_elbow': self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            'left_wrist': self.mp_pose.PoseLandmark.LEFT_WRIST,
            'right_wrist': self.mp_pose.PoseLandmark.RIGHT_WRIST,
            'left_hip': self.mp_pose.PoseLandmark.LEFT_HIP,
            'right_hip': self.mp_pose.PoseLandmark.RIGHT_HIP,
            'left_knee': self.mp_pose.PoseLandmark.LEFT_KNEE,
            'right_knee': self.mp_pose.PoseLandmark.RIGHT_KNEE,
            'left_ankle': self.mp_pose.PoseLandmark.LEFT_ANKLE,
            'right_ankle': self.mp_pose.PoseLandmark.RIGHT_ANKLE,
        }
        
        for name, landmark_id in key_points.items():
            lm = pose_landmarks.landmark[landmark_id]
            landmarks[f'{name}_x'] = lm.x
            landmarks[f'{name}_y'] = lm.y
            landmarks[f'{name}_z'] = lm.z
            landmarks[f'{name}_visibility'] = lm.visibility
        
        # Calculate derived metrics
        landmarks['center_of_mass_y'] = np.mean([
            pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP].y,
            pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP].y
        ])
        
        return landmarks
    
    def check_inconsistencies(self, analysis_results: Dict) -> Dict:
        """
        Check for inconsistencies in the analyzed data.
        
        Args:
            analysis_results: Results from analyze_video
            
        Returns:
            Dictionary containing inconsistencies found
        """
        inconsistencies = {
            'missing_frames': [],
            'low_visibility_frames': [],
            'sudden_movements': [],
            'tracking_issues': []
        }
        
        frame_data = analysis_results['frame_data']
        
        if not frame_data:
            inconsistencies['tracking_issues'].append("No pose data detected in video")
            return inconsistencies
        
        # Check for missing consecutive frames
        for i in range(1, len(frame_data)):
            frame_gap = frame_data[i]['frame'] - frame_data[i-1]['frame']
            if frame_gap > 1:
                inconsistencies['missing_frames'].append({
                    'start_frame': frame_data[i-1]['frame'],
                    'end_frame': frame_data[i]['frame'],
                    'gap': frame_gap - 1
                })
        
        # Check for low visibility
        for frame in frame_data:
            low_vis_count = sum(1 for key in frame.keys() 
                               if key.endswith('_visibility') and frame[key] < self.LOW_VISIBILITY_THRESHOLD)
            if low_vis_count > self.LOW_VISIBILITY_COUNT_THRESHOLD:
                inconsistencies['low_visibility_frames'].append({
                    'frame': frame['frame'],
                    'time': frame['time'],
                    'low_visibility_count': low_vis_count
                })
        
        # Check for sudden movements (large position changes)
        for i in range(1, len(frame_data)):
            prev = frame_data[i-1]
            curr = frame_data[i]
            
            # Check center of mass sudden changes
            if abs(curr['center_of_mass_y'] - prev['center_of_mass_y']) > self.SUDDEN_MOVEMENT_THRESHOLD:
                inconsistencies['sudden_movements'].append({
                    'frame': curr['frame'],
                    'time': curr['time'],
                    'metric': 'center_of_mass_y',
                    'change': abs(curr['center_of_mass_y'] - prev['center_of_mass_y'])
                })
        
        return inconsistencies
    
    def save_results(self, analysis_results: Dict, inconsistencies: Dict, output_dir: str = "output"):
        """
        Save analysis results and inconsistencies to files.
        
        Args:
            analysis_results: Results from analyze_video
            inconsistencies: Results from check_inconsistencies
            output_dir: Directory to save output files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a sanitized filename
        video_name = os.path.basename(analysis_results['video_path']).replace('.', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        csv_path = None
        # Save frame data to CSV
        if analysis_results['frame_data']:
            df = pd.DataFrame(analysis_results['frame_data'])
            csv_path = os.path.join(output_dir, f"{video_name}_{timestamp}_data.csv")
            df.to_csv(csv_path, index=False)
            print(f"Saved frame data to: {csv_path}")
        
        # Save full results to JSON
        json_path = os.path.join(output_dir, f"{video_name}_{timestamp}_results.json")
        with open(json_path, 'w') as f:
            # Remove frame_data from JSON as it's in CSV
            results_copy = analysis_results.copy()
            if csv_path:
                results_copy['frame_data'] = f"See {csv_path}"
            else:
                results_copy['frame_data'] = "No frame data available"
            json.dump({
                'analysis': results_copy,
                'inconsistencies': inconsistencies
            }, f, indent=2)
        print(f"Saved analysis results to: {json_path}")
        
        # Save inconsistencies summary
        summary_path = os.path.join(output_dir, f"{video_name}_{timestamp}_inconsistencies.txt")
        with open(summary_path, 'w') as f:
            f.write("POLE VAULT VIDEO ANALYSIS - INCONSISTENCIES REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Video: {analysis_results['video_path']}\n")
            f.write(f"Analysis Date: {analysis_results['timestamp']}\n")
            f.write(f"Duration: {analysis_results['duration']:.2f}s\n")
            f.write(f"Frames Analyzed: {analysis_results['frames_analyzed']}/{analysis_results['frame_count']}\n\n")
            
            f.write("INCONSISTENCIES FOUND:\n")
            f.write("-" * 60 + "\n\n")
            
            if inconsistencies['missing_frames']:
                f.write(f"Missing Frames: {len(inconsistencies['missing_frames'])} gaps found\n")
                for gap in inconsistencies['missing_frames'][:5]:  # Show first 5
                    f.write(f"  - Frames {gap['start_frame']}-{gap['end_frame']}: {gap['gap']} missing\n")
                if len(inconsistencies['missing_frames']) > 5:
                    f.write(f"  - ... and {len(inconsistencies['missing_frames']) - 5} more\n")
                f.write("\n")
            
            if inconsistencies['low_visibility_frames']:
                f.write(f"Low Visibility Frames: {len(inconsistencies['low_visibility_frames'])} frames\n")
                for frame in inconsistencies['low_visibility_frames'][:5]:
                    f.write(f"  - Frame {frame['frame']} (t={frame['time']:.2f}s): {frame['low_visibility_count']} low visibility landmarks\n")
                if len(inconsistencies['low_visibility_frames']) > 5:
                    f.write(f"  - ... and {len(inconsistencies['low_visibility_frames']) - 5} more\n")
                f.write("\n")
            
            if inconsistencies['sudden_movements']:
                f.write(f"Sudden Movements: {len(inconsistencies['sudden_movements'])} detected\n")
                for movement in inconsistencies['sudden_movements'][:5]:
                    f.write(f"  - Frame {movement['frame']} (t={movement['time']:.2f}s): {movement['metric']} changed by {movement['change']:.3f}\n")
                if len(inconsistencies['sudden_movements']) > 5:
                    f.write(f"  - ... and {len(inconsistencies['sudden_movements']) - 5} more\n")
                f.write("\n")
            
            if inconsistencies['tracking_issues']:
                f.write(f"Tracking Issues: {len(inconsistencies['tracking_issues'])}\n")
                for issue in inconsistencies['tracking_issues']:
                    f.write(f"  - {issue}\n")
                f.write("\n")
            
            total_issues = (len(inconsistencies['missing_frames']) + 
                          len(inconsistencies['low_visibility_frames']) + 
                          len(inconsistencies['sudden_movements']) + 
                          len(inconsistencies['tracking_issues']))
            
            f.write("-" * 60 + "\n")
            f.write(f"TOTAL ISSUES FOUND: {total_issues}\n")
        
        print(f"Saved inconsistencies report to: {summary_path}")
        
        return {
            'csv': csv_path,
            'json': json_path,
            'summary': summary_path
        }
    
    def cleanup(self):
        """Release resources."""
        self.pose.close()


def main():
    """Main function to run video analysis."""
    print("Pole Vault Video Analyzer")
    print("=" * 60)
    
    # Example URLs of pole vault videos (these are sample, would need real URLs)
    example_videos = [
        # These would be real YouTube or video URLs
        # "https://www.youtube.com/watch?v=example1",
        # "https://www.youtube.com/watch?v=example2",
    ]
    
    # For testing with local videos
    local_videos = []
    if os.path.exists("videos"):
        local_videos = [os.path.join("videos", f) for f in os.listdir("videos") 
                       if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    if not example_videos and not local_videos:
        print("\nNo videos specified for analysis.")
        print("Please add video URLs to example_videos or place videos in 'videos/' directory")
        return
    
    analyzer = PoleVaultAnalyzer()
    
    try:
        # Download and analyze online videos
        for url in example_videos:
            print(f"\n\nDownloading video from: {url}")
            video_path = analyzer.download_video(url)
            
            if video_path:
                print(f"\nAnalyzing downloaded video...")
                results = analyzer.analyze_video(video_path)
                inconsistencies = analyzer.check_inconsistencies(results)
                files = analyzer.save_results(results, inconsistencies)
                
                print("\n" + "=" * 60)
                print("Analysis complete!")
                print(f"Results saved to: {files['summary']}")
        
        # Analyze local videos
        for video_path in local_videos:
            print(f"\n\nAnalyzing local video: {video_path}")
            results = analyzer.analyze_video(video_path)
            inconsistencies = analyzer.check_inconsistencies(results)
            files = analyzer.save_results(results, inconsistencies)
            
            print("\n" + "=" * 60)
            print("Analysis complete!")
            print(f"Results saved to: {files['summary']}")
    
    finally:
        analyzer.cleanup()


if __name__ == "__main__":
    main()
