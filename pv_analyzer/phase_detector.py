"""
Phase Detection Module
Detects the 7 phases of pole vaulting: run, plant, take-off, swing-up, 
extension/inversion, push-off, and pike
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from enum import Enum


class VaultPhase(Enum):
    """Enumeration of pole vault phases"""
    RUN = "run"
    PLANT = "plant"
    TAKEOFF = "take-off"
    SWING_UP = "swing-up"
    EXTENSION_INVERSION = "extension/inversion"
    PUSH_OFF = "push-off"
    PIKE = "pike"


class PhaseDetector:
    """Detect phases of pole vaulting from pose landmarks"""
    
    def __init__(self):
        self.phases = []
        self.velocity_data = {}  # Store velocity data per phase
        
    def detect_phases(self, landmarks_list: List[Optional[dict]], video_info: dict) -> List[Dict]:
        """
        Detect pole vault phases from landmark data
        
        Args:
            landmarks_list: List of landmark dictionaries for each frame
            video_info: Video metadata including fps
            
        Returns:
            List of phase dictionaries with start_frame, end_frame, and phase type
        """
        if not landmarks_list:
            return []
        
        fps = video_info['fps']
        phases = []
        
        # Calculate metrics for each frame
        velocities = self._calculate_velocities(landmarks_list, fps)
        heights = self._calculate_heights(landmarks_list)
        body_angles = self._calculate_body_angles(landmarks_list)
        
        # Detect phases based on motion characteristics
        current_phase = None
        phase_start = 0
        
        for frame_idx in range(len(landmarks_list)):
            if landmarks_list[frame_idx] is None:
                continue
                
            detected_phase = self._identify_phase(
                frame_idx, landmarks_list, velocities, heights, body_angles
            )
            
            if detected_phase != current_phase:
                if current_phase is not None:
                    # Calculate velocity statistics for the phase
                    phase_velocities = velocities[phase_start:frame_idx]
                    phase_velocities_filtered = [v for v in phase_velocities if v is not None and v != 0]
                    
                    if phase_velocities_filtered:
                        velocity_stats = {
                            'max': max(phase_velocities_filtered),
                            'average': np.mean(phase_velocities_filtered),
                            'min': min(phase_velocities_filtered),
                            'initial': phase_velocities[0] if phase_velocities else 0,
                            'final': phase_velocities[-1] if phase_velocities else 0,
                        }
                    else:
                        velocity_stats = {
                            'max': 0,
                            'average': 0,
                            'min': 0,
                            'initial': 0,
                            'final': 0,
                        }
                    
                    phases.append({
                        'phase': current_phase,
                        'start_frame': phase_start,
                        'end_frame': frame_idx - 1,
                        'duration': (frame_idx - phase_start) / fps,
                        'velocity_stats': velocity_stats
                    })
                current_phase = detected_phase
                phase_start = frame_idx
        
        # Add final phase
        if current_phase is not None:
            phase_velocities = velocities[phase_start:]
            phase_velocities_filtered = [v for v in phase_velocities if v is not None and v != 0]
            
            if phase_velocities_filtered:
                velocity_stats = {
                    'max': max(phase_velocities_filtered),
                    'average': np.mean(phase_velocities_filtered),
                    'min': min(phase_velocities_filtered),
                    'initial': phase_velocities[0] if phase_velocities else 0,
                    'final': phase_velocities[-1] if phase_velocities else 0,
                }
            else:
                velocity_stats = {
                    'max': 0,
                    'average': 0,
                    'min': 0,
                    'initial': 0,
                    'final': 0,
                }
            
            phases.append({
                'phase': current_phase,
                'start_frame': phase_start,
                'end_frame': len(landmarks_list) - 1,
                'duration': (len(landmarks_list) - phase_start) / fps,
                'velocity_stats': velocity_stats
            })
        
        self.phases = phases
        return phases
    
    def _calculate_velocities(self, landmarks_list: List[Optional[dict]], fps: float) -> List[float]:
        """Calculate horizontal velocity of the center of mass"""
        velocities = []
        
        for i in range(len(landmarks_list)):
            if landmarks_list[i] is None:
                velocities.append(0.0)
                continue
                
            if i == 0 or landmarks_list[i-1] is None:
                velocities.append(0.0)
                continue
            
            # Calculate center of mass position
            com_x_curr = self._get_center_of_mass_x(landmarks_list[i])
            com_x_prev = self._get_center_of_mass_x(landmarks_list[i-1])
            
            # Velocity in pixels per second
            velocity = (com_x_curr - com_x_prev) * fps
            velocities.append(velocity)
        
        return velocities
    
    def _calculate_heights(self, landmarks_list: List[Optional[dict]]) -> List[float]:
        """Calculate height of center of mass from ground"""
        heights = []
        
        for landmarks in landmarks_list:
            if landmarks is None:
                heights.append(0.0)
                continue
            
            # Use average of hip height as proxy for COM height
            left_hip_y = landmarks['left_hip']['y']
            right_hip_y = landmarks['right_hip']['y']
            com_y = (left_hip_y + right_hip_y) / 2
            
            # Get foot position as ground reference
            left_foot_y = landmarks['left_ankle']['y']
            right_foot_y = landmarks['right_ankle']['y']
            ground_y = max(left_foot_y, right_foot_y)  # Lower foot position
            
            height = ground_y - com_y  # Invert because y increases downward
            heights.append(height)
        
        return heights
    
    def _calculate_body_angles(self, landmarks_list: List[Optional[dict]]) -> List[float]:
        """Calculate body angle relative to horizontal"""
        angles = []
        
        for landmarks in landmarks_list:
            if landmarks is None:
                angles.append(0.0)
                continue
            
            # Calculate angle between shoulders and hips
            shoulder_x = (landmarks['left_shoulder']['x'] + landmarks['right_shoulder']['x']) / 2
            shoulder_y = (landmarks['left_shoulder']['y'] + landmarks['right_shoulder']['y']) / 2
            hip_x = (landmarks['left_hip']['x'] + landmarks['right_hip']['x']) / 2
            hip_y = (landmarks['left_hip']['y'] + landmarks['right_hip']['y']) / 2
            
            dx = hip_x - shoulder_x
            dy = hip_y - shoulder_y
            
            angle = np.arctan2(dy, dx) * 180 / np.pi
            angles.append(angle)
        
        return angles
    
    def _get_center_of_mass_x(self, landmarks: dict) -> float:
        """Calculate x-coordinate of center of mass"""
        key_points = ['left_hip', 'right_hip', 'left_shoulder', 'right_shoulder']
        x_sum = sum(landmarks[point]['x'] for point in key_points)
        return x_sum / len(key_points)
    
    def _identify_phase(self, frame_idx: int, landmarks_list: List[Optional[dict]], 
                       velocities: List[float], heights: List[float], 
                       body_angles: List[float]) -> VaultPhase:
        """
        Identify the current phase based on motion characteristics
        
        Uses heuristics based on velocity, height, and body angle
        """
        velocity = velocities[frame_idx]
        height = heights[frame_idx]
        angle = body_angles[frame_idx]
        
        # Create a window for smoothing
        window_size = 5
        start_idx = max(0, frame_idx - window_size)
        end_idx = min(len(velocities), frame_idx + window_size + 1)
        
        avg_velocity = np.mean(velocities[start_idx:end_idx])
        avg_height = np.mean(heights[start_idx:end_idx])
        avg_angle = np.mean(body_angles[start_idx:end_idx])
        
        # Phase detection logic
        # 1. RUN: High horizontal velocity, low height, body relatively upright
        if avg_velocity > 50 and avg_height < 150 and abs(avg_angle) < 30:
            return VaultPhase.RUN
        
        # 2. PLANT: Velocity decreasing, height starting to increase
        if 20 < avg_velocity < 50 and 100 < avg_height < 200:
            return VaultPhase.PLANT
        
        # 3. TAKEOFF: Rapid height increase, velocity still moderate
        if avg_velocity > 0 and 150 < avg_height < 300 and abs(avg_angle) < 60:
            return VaultPhase.TAKEOFF
        
        # 4. SWING_UP: Body rotating, height increasing rapidly
        if avg_height > 200 and 30 < abs(avg_angle) < 90:
            return VaultPhase.SWING_UP
        
        # 5. EXTENSION_INVERSION: Body inverted (angle > 90), at peak height
        if avg_height > 250 and abs(avg_angle) > 80:
            return VaultPhase.EXTENSION_INVERSION
        
        # 6. PUSH_OFF: Height at maximum, body starting to extend
        if avg_height > 300 and 45 < abs(avg_angle) < 90:
            return VaultPhase.PUSH_OFF
        
        # 7. PIKE: Descending, body folded
        if avg_height > 200 and abs(avg_angle) < 45:
            return VaultPhase.PIKE
        
        # Default to RUN if no other phase detected
        return VaultPhase.RUN
    
    def get_phase_summary(self) -> str:
        """Get a text summary of detected phases"""
        if not self.phases:
            return "No phases detected"
        
        summary = "Detected Pole Vault Phases:\n"
        summary += "=" * 50 + "\n"
        
        for i, phase_info in enumerate(self.phases, 1):
            phase = phase_info['phase']
            duration = phase_info['duration']
            start = phase_info['start_frame']
            end = phase_info['end_frame']
            velocity_stats = phase_info.get('velocity_stats', {})
            
            summary += f"{i}. {phase.value.upper()}\n"
            summary += f"   Frames: {start} - {end}\n"
            summary += f"   Duration: {duration:.2f} seconds\n"
            
            # Add velocity information
            if velocity_stats:
                summary += f"   Velocity (pixels/sec):\n"
                summary += f"     Initial: {velocity_stats.get('initial', 0):.2f}\n"
                summary += f"     Max:     {velocity_stats.get('max', 0):.2f}\n"
                summary += f"     Average: {velocity_stats.get('average', 0):.2f}\n"
                summary += f"     Final:   {velocity_stats.get('final', 0):.2f}\n"
            
            summary += "\n"
        
        return summary
