"""
Energy Calculator Module
Calculates kinetic and potential energy for each phase of the pole vault
"""

import numpy as np
from typing import List, Dict, Optional


class EnergyCalculator:
    """Calculate energy metrics for pole vaulting phases"""
    
    # Physical constants
    GRAVITY = 9.81  # m/s^2
    
    def __init__(self, athlete_mass: float = 70.0, pixel_to_meter_ratio: float = 0.01):
        """
        Initialize energy calculator
        
        Args:
            athlete_mass: Mass of athlete in kg (default 70kg)
            pixel_to_meter_ratio: Conversion ratio from pixels to meters (default 0.01)
        """
        self.athlete_mass = athlete_mass
        self.pixel_to_meter = pixel_to_meter_ratio
        
    def calculate_phase_energies(self, landmarks_list: List[Optional[dict]], 
                                 phases: List[Dict], video_info: dict) -> Dict:
        """
        Calculate energy for each phase
        
        Args:
            landmarks_list: List of pose landmarks for each frame
            phases: List of detected phases
            video_info: Video metadata including fps
            
        Returns:
            Dictionary containing energy analysis for each phase
        """
        fps = video_info['fps']
        phase_energies = {}
        
        for phase_info in phases:
            phase = phase_info['phase']
            start_frame = phase_info['start_frame']
            end_frame = phase_info['end_frame']
            
            # Extract landmarks for this phase
            phase_landmarks = landmarks_list[start_frame:end_frame+1]
            
            # Calculate energies
            kinetic_energies = self._calculate_kinetic_energy(phase_landmarks, fps)
            potential_energies = self._calculate_potential_energy(phase_landmarks)
            total_energies = [ke + pe for ke, pe in zip(kinetic_energies, potential_energies)]
            
            # Calculate statistics
            phase_energies[phase.value] = {
                'kinetic_energy': {
                    'initial': kinetic_energies[0] if kinetic_energies else 0,
                    'final': kinetic_energies[-1] if kinetic_energies else 0,
                    'max': max(kinetic_energies) if kinetic_energies else 0,
                    'average': np.mean(kinetic_energies) if kinetic_energies else 0,
                },
                'potential_energy': {
                    'initial': potential_energies[0] if potential_energies else 0,
                    'final': potential_energies[-1] if potential_energies else 0,
                    'max': max(potential_energies) if potential_energies else 0,
                    'average': np.mean(potential_energies) if potential_energies else 0,
                },
                'total_energy': {
                    'initial': total_energies[0] if total_energies else 0,
                    'final': total_energies[-1] if total_energies else 0,
                    'max': max(total_energies) if total_energies else 0,
                    'average': np.mean(total_energies) if total_energies else 0,
                },
                'energy_generated': total_energies[-1] - total_energies[0] if total_energies else 0,
                'duration': phase_info['duration']
            }
        
        return phase_energies
    
    def _calculate_kinetic_energy(self, landmarks_list: List[Optional[dict]], fps: float) -> List[float]:
        """
        Calculate kinetic energy: KE = 0.5 * m * v^2
        
        Args:
            landmarks_list: List of landmarks for frames in a phase
            fps: Frames per second
            
        Returns:
            List of kinetic energies in Joules
        """
        kinetic_energies = []
        
        for i in range(len(landmarks_list)):
            if landmarks_list[i] is None:
                kinetic_energies.append(0.0)
                continue
            
            if i == 0 or landmarks_list[i-1] is None:
                kinetic_energies.append(0.0)
                continue
            
            # Calculate center of mass velocity
            com_curr = self._get_center_of_mass(landmarks_list[i])
            com_prev = self._get_center_of_mass(landmarks_list[i-1])
            
            # Calculate displacement in pixels
            dx = com_curr[0] - com_prev[0]
            dy = com_curr[1] - com_prev[1]
            
            # Convert to meters and calculate velocity
            dx_m = dx * self.pixel_to_meter
            dy_m = dy * self.pixel_to_meter
            dt = 1.0 / fps
            
            velocity = np.sqrt(dx_m**2 + dy_m**2) / dt
            
            # Calculate kinetic energy
            ke = 0.5 * self.athlete_mass * velocity**2
            kinetic_energies.append(ke)
        
        return kinetic_energies
    
    def _calculate_potential_energy(self, landmarks_list: List[Optional[dict]]) -> List[float]:
        """
        Calculate potential energy: PE = m * g * h
        
        Args:
            landmarks_list: List of landmarks for frames in a phase
            
        Returns:
            List of potential energies in Joules
        """
        potential_energies = []
        
        # Find ground level (maximum y value across all frames)
        ground_level = 0
        for landmarks in landmarks_list:
            if landmarks is not None:
                foot_y = max(
                    landmarks['left_ankle']['y'],
                    landmarks['right_ankle']['y']
                )
                ground_level = max(ground_level, foot_y)
        
        for landmarks in landmarks_list:
            if landmarks is None:
                potential_energies.append(0.0)
                continue
            
            # Get center of mass height
            com_y = self._get_center_of_mass(landmarks)[1]
            
            # Calculate height above ground in pixels
            height_pixels = ground_level - com_y  # Invert y-axis
            
            # Convert to meters
            height_m = height_pixels * self.pixel_to_meter
            
            # Calculate potential energy
            pe = self.athlete_mass * self.GRAVITY * height_m
            potential_energies.append(max(0, pe))  # Ensure non-negative
        
        return potential_energies
    
    def _get_center_of_mass(self, landmarks: dict) -> tuple:
        """
        Calculate approximate center of mass position
        
        Args:
            landmarks: Dictionary of pose landmarks
            
        Returns:
            Tuple of (x, y) coordinates
        """
        # Use key body points to estimate COM
        key_points = [
            'left_hip', 'right_hip', 'left_shoulder', 'right_shoulder'
        ]
        
        x_sum = sum(landmarks[point]['x'] for point in key_points)
        y_sum = sum(landmarks[point]['y'] for point in key_points)
        
        com_x = x_sum / len(key_points)
        com_y = y_sum / len(key_points)
        
        return (com_x, com_y)
    
    def get_energy_summary(self, phase_energies: Dict) -> str:
        """
        Generate a text summary of energy analysis
        
        Args:
            phase_energies: Dictionary of energy data by phase
            
        Returns:
            Formatted summary string
        """
        summary = "\nEnergy Analysis by Phase:\n"
        summary += "=" * 70 + "\n\n"
        
        for phase_name, energies in phase_energies.items():
            summary += f"{phase_name.upper()}:\n"
            summary += f"  Duration: {energies['duration']:.2f}s\n"
            summary += f"  Kinetic Energy:\n"
            summary += f"    Initial: {energies['kinetic_energy']['initial']:.2f} J\n"
            summary += f"    Final:   {energies['kinetic_energy']['final']:.2f} J\n"
            summary += f"    Max:     {energies['kinetic_energy']['max']:.2f} J\n"
            summary += f"  Potential Energy:\n"
            summary += f"    Initial: {energies['potential_energy']['initial']:.2f} J\n"
            summary += f"    Final:   {energies['potential_energy']['final']:.2f} J\n"
            summary += f"    Max:     {energies['potential_energy']['max']:.2f} J\n"
            summary += f"  Total Energy:\n"
            summary += f"    Initial: {energies['total_energy']['initial']:.2f} J\n"
            summary += f"    Final:   {energies['total_energy']['final']:.2f} J\n"
            summary += f"    Max:     {energies['total_energy']['max']:.2f} J\n"
            summary += f"  Energy Generated: {energies['energy_generated']:.2f} J\n"
            summary += "\n"
        
        # Calculate total energy generated
        total_generated = sum(e['energy_generated'] for e in phase_energies.values())
        summary += f"TOTAL ENERGY GENERATED: {total_generated:.2f} J\n"
        summary += "=" * 70 + "\n"
        
        return summary
