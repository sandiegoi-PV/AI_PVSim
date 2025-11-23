"""
Unit tests for the video analysis module.
Tests core functionality without requiring actual video files.
"""

import unittest
import numpy as np
from video_analyzer import VideoAnalyzer, FrameData
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json
import os


class TestVideoAnalyzer(unittest.TestCase):
    """Test cases for VideoAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures with mocked MediaPipe"""
        # Mock MediaPipe to avoid downloading models
        with patch('video_analyzer.mp.solutions.pose.Pose'):
            self.analyzer = VideoAnalyzer(calibration_height_meters=1.8)
            # Replace the pose object with a mock
            self.analyzer.pose = Mock()
    
    def test_initialization(self):
        """Test analyzer initialization"""
        self.assertEqual(self.analyzer.calibration_height_meters, 1.8)
        self.assertIsNone(self.analyzer.pixels_per_meter)
        self.assertEqual(len(self.analyzer.frame_data), 0)
    
    def test_calibrate_scale(self):
        """Test scale calibration"""
        # Create mock frame
        frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
        # Create mock landmarks
        mock_landmarks = Mock()
        nose_landmark = Mock()
        nose_landmark.y = 0.2
        nose_landmark.visibility = 0.9
        
        ankle_landmark = Mock()
        ankle_landmark.y = 0.9
        ankle_landmark.visibility = 0.8
        
        mock_landmarks.landmark = {
            0: nose_landmark,  # NOSE
            27: ankle_landmark,  # LEFT_ANKLE
            28: ankle_landmark,  # RIGHT_ANKLE
        }
        
        # Mock the PoseLandmark enum access
        with patch.object(self.analyzer.mp_pose, 'PoseLandmark') as mock_enum:
            mock_enum.NOSE = 0
            mock_enum.LEFT_ANKLE = 27
            mock_enum.RIGHT_ANKLE = 28
            
            pixels_per_meter = self.analyzer.calibrate_scale(frame, mock_landmarks)
            
            # Expected: pixel_height = (0.9 - 0.2) * 1080 = 756 pixels
            # pixels_per_meter = 756 / 1.8 = 420
            self.assertIsNotNone(pixels_per_meter)
            self.assertAlmostEqual(pixels_per_meter, 420.0, places=1)
    
    def test_calculate_pole_angle(self):
        """Test pole angle calculation"""
        # Vertical pole (90 degrees)
        pole_endpoints = ((100, 500), (100, 100))
        angle = self.analyzer.calculate_pole_angle(pole_endpoints)
        self.assertAlmostEqual(angle, -90.0, places=1)
        
        # Horizontal pole (0 degrees)
        pole_endpoints = ((100, 100), (500, 100))
        angle = self.analyzer.calculate_pole_angle(pole_endpoints)
        self.assertAlmostEqual(angle, 0.0, places=1)
        
        # 45 degree pole
        pole_endpoints = ((0, 0), (100, 100))
        angle = self.analyzer.calculate_pole_angle(pole_endpoints)
        self.assertAlmostEqual(angle, 45.0, places=1)
    
    def test_frame_data_creation(self):
        """Test FrameData dataclass"""
        keypoints = {
            'NOSE': (640.5, 200.3, 0.99),
            'LEFT_SHOULDER': (600.2, 350.1, 0.95)
        }
        pole_endpoints = ((500, 100), (520, 800))
        
        frame_data = FrameData(
            frame_number=0,
            timestamp=0.0,
            athlete_keypoints=keypoints,
            pole_endpoints=pole_endpoints,
            pole_length_pixels=702.1,
            athlete_height_pixels=450.2,
            pole_angle=85.3
        )
        
        self.assertEqual(frame_data.frame_number, 0)
        self.assertEqual(frame_data.timestamp, 0.0)
        self.assertEqual(frame_data.pole_angle, 85.3)
        self.assertEqual(len(frame_data.athlete_keypoints), 2)
    
    def test_export_data(self):
        """Test data export to JSON"""
        # Add some mock frame data
        self.analyzer.pixels_per_meter = 420.0
        frame_data = FrameData(
            frame_number=0,
            timestamp=0.0,
            athlete_keypoints={'NOSE': (640.5, 200.3, 0.99)},
            pole_endpoints=((500, 100), (520, 800)),
            pole_length_pixels=702.1,
            athlete_height_pixels=450.2,
            pole_angle=85.3
        )
        self.analyzer.frame_data.append(frame_data)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            self.analyzer.export_data(temp_path)
            
            # Read and verify
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            self.assertEqual(data['calibration_height_meters'], 1.8)
            self.assertEqual(data['pixels_per_meter'], 420.0)
            self.assertEqual(data['total_frames'], 1)
            self.assertEqual(len(data['frames']), 1)
            self.assertEqual(data['frames'][0]['frame_number'], 0)
            self.assertEqual(data['frames'][0]['pole_angle'], 85.3)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_get_statistics_empty(self):
        """Test statistics with no data"""
        stats = self.analyzer.get_statistics()
        self.assertEqual(stats['total_frames'], 0)
        self.assertEqual(stats['avg_pole_angle'], 0)
    
    def test_get_statistics_with_data(self):
        """Test statistics calculation with data"""
        # Add mock frame data
        self.analyzer.pixels_per_meter = 400.0
        
        for i in range(3):
            frame_data = FrameData(
                frame_number=i,
                timestamp=i * 0.033,
                athlete_keypoints={},
                pole_endpoints=((100, 100), (200, 200)),
                pole_length_pixels=100.0 + i * 10,
                athlete_height_pixels=400.0,
                pole_angle=45.0 + i * 5
            )
            self.analyzer.frame_data.append(frame_data)
        
        stats = self.analyzer.get_statistics()
        
        self.assertEqual(stats['total_frames'], 3)
        self.assertAlmostEqual(stats['avg_pole_angle'], 50.0, places=1)  # (45 + 50 + 55) / 3
        self.assertAlmostEqual(stats['max_pole_angle'], 55.0, places=1)
        self.assertAlmostEqual(stats['min_pole_angle'], 45.0, places=1)
        self.assertAlmostEqual(stats['avg_athlete_height_pixels'], 400.0, places=1)
        self.assertAlmostEqual(stats['avg_athlete_height_meters'], 1.0, places=1)  # 400 / 400
    
    def test_extract_keypoints(self):
        """Test keypoint extraction"""
        # Create mock landmarks
        mock_landmarks = Mock()
        landmark1 = Mock()
        landmark1.x = 0.5
        landmark1.y = 0.3
        landmark1.visibility = 0.95
        
        landmark2 = Mock()
        landmark2.x = 0.6
        landmark2.y = 0.4
        landmark2.visibility = 0.90
        
        mock_landmarks.landmark = [landmark1, landmark2]
        
        # Mock the PoseLandmark enum properly
        with patch.object(self.analyzer.mp_pose, 'PoseLandmark') as mock_enum:
            # Create proper enum-like side_effect for name access
            def mock_name(idx):
                mock_landmark = Mock()
                mock_landmark.name = f'LANDMARK_{idx}'
                return mock_landmark
            mock_enum.side_effect = mock_name
            
            keypoints = self.analyzer.extract_keypoints(mock_landmarks, 1920, 1080)
            
            self.assertEqual(len(keypoints), 2)
            # First landmark should be at (960, 324) with visibility 0.95
            first_key = list(keypoints.keys())[0]
            self.assertAlmostEqual(keypoints[first_key][0], 960.0, places=1)  # 0.5 * 1920
            self.assertAlmostEqual(keypoints[first_key][1], 324.0, places=1)  # 0.3 * 1080
            self.assertAlmostEqual(keypoints[first_key][2], 0.95, places=2)


class TestFrameData(unittest.TestCase):
    """Test FrameData dataclass functionality"""
    
    def test_frame_data_with_none_values(self):
        """Test FrameData with None values for optional fields"""
        frame_data = FrameData(
            frame_number=5,
            timestamp=0.167,
            athlete_keypoints={},
            pole_endpoints=None,
            pole_length_pixels=None,
            athlete_height_pixels=None,
            pole_angle=None
        )
        
        self.assertEqual(frame_data.frame_number, 5)
        self.assertIsNone(frame_data.pole_endpoints)
        self.assertIsNone(frame_data.pole_angle)


if __name__ == '__main__':
    unittest.main()
