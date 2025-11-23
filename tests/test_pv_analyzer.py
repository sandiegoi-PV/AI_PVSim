"""
Unit tests for the AI_PVSim system
"""

import unittest
import numpy as np
from pv_analyzer import VideoProcessor, PhaseDetector, EnergyCalculator, PerformanceComparator
from pv_analyzer.phase_detector import VaultPhase


class TestPhaseDetector(unittest.TestCase):
    """Test the phase detector"""
    
    def test_phase_detector_initialization(self):
        """Test that phase detector initializes correctly"""
        detector = PhaseDetector()
        self.assertIsNotNone(detector)
        self.assertEqual(detector.phases, [])
    
    def test_detect_phases_with_none_landmarks(self):
        """Test phase detection with None landmarks"""
        detector = PhaseDetector()
        landmarks_list = [None] * 10
        video_info = {'fps': 30}
        phases = detector.detect_phases(landmarks_list, video_info)
        self.assertEqual(phases, [])
    
    def test_detect_phases_with_valid_landmarks(self):
        """Test phase detection with valid landmarks"""
        detector = PhaseDetector()
        
        # Create simple landmark data
        landmarks = {
            'left_hip': {'x': 100, 'y': 200, 'z': 0, 'visibility': 0.9},
            'right_hip': {'x': 120, 'y': 200, 'z': 0, 'visibility': 0.9},
            'left_shoulder': {'x': 100, 'y': 180, 'z': 0, 'visibility': 0.9},
            'right_shoulder': {'x': 120, 'y': 180, 'z': 0, 'visibility': 0.9},
            'left_ankle': {'x': 100, 'y': 250, 'z': 0, 'visibility': 0.9},
            'right_ankle': {'x': 120, 'y': 250, 'z': 0, 'visibility': 0.9}
        }
        
        landmarks_list = [landmarks] * 30
        video_info = {'fps': 30}
        phases = detector.detect_phases(landmarks_list, video_info)
        
        # Should detect at least one phase
        self.assertGreater(len(phases), 0)
        self.assertIn('phase', phases[0])
        self.assertIn('start_frame', phases[0])
        self.assertIn('end_frame', phases[0])


class TestEnergyCalculator(unittest.TestCase):
    """Test the energy calculator"""
    
    def test_energy_calculator_initialization(self):
        """Test that energy calculator initializes correctly"""
        calculator = EnergyCalculator(athlete_mass=70.0)
        self.assertEqual(calculator.athlete_mass, 70.0)
        self.assertEqual(calculator.GRAVITY, 9.81)
    
    def test_calculate_phase_energies(self):
        """Test energy calculation"""
        calculator = EnergyCalculator(athlete_mass=70.0, pixel_to_meter_ratio=0.01)
        
        # Create simple landmark data
        landmarks = {
            'left_hip': {'x': 100, 'y': 200, 'z': 0, 'visibility': 0.9},
            'right_hip': {'x': 120, 'y': 200, 'z': 0, 'visibility': 0.9},
            'left_shoulder': {'x': 100, 'y': 180, 'z': 0, 'visibility': 0.9},
            'right_shoulder': {'x': 120, 'y': 180, 'z': 0, 'visibility': 0.9},
            'left_ankle': {'x': 100, 'y': 250, 'z': 0, 'visibility': 0.9},
            'right_ankle': {'x': 120, 'y': 250, 'z': 0, 'visibility': 0.9}
        }
        
        landmarks_list = [landmarks] * 30
        phases = [{
            'phase': VaultPhase.RUN,
            'start_frame': 0,
            'end_frame': 29,
            'duration': 1.0
        }]
        video_info = {'fps': 30}
        
        energies = calculator.calculate_phase_energies(landmarks_list, phases, video_info)
        
        # Should have energy data for the run phase
        self.assertIn('run', energies)
        self.assertIn('kinetic_energy', energies['run'])
        self.assertIn('potential_energy', energies['run'])
        self.assertIn('total_energy', energies['run'])


class TestPerformanceComparator(unittest.TestCase):
    """Test the performance comparator"""
    
    def test_comparator_initialization(self):
        """Test that comparator initializes correctly"""
        comparator = PerformanceComparator()
        self.assertIsNotNone(comparator)
        self.assertEqual(len(comparator.REFERENCE_ATHLETES), 2)
    
    def test_compare_performance(self):
        """Test performance comparison"""
        comparator = PerformanceComparator()
        
        # Create sample energy data
        athlete_energies = {
            'run': {
                'kinetic_energy': {'initial': 0, 'final': 2000, 'max': 2100, 'average': 1500},
                'potential_energy': {'initial': 0, 'final': 100, 'max': 150, 'average': 75},
                'total_energy': {'initial': 0, 'final': 2100, 'max': 2250, 'average': 1575},
                'energy_generated': 2100,
                'duration': 3.5
            }
        }
        
        comparisons = comparator.compare_performance(athlete_energies, 70.0)
        
        # Should have comparisons for both reference athletes
        self.assertEqual(len(comparisons), 2)
        self.assertIn('mondo_duplantis', comparisons)
        self.assertIn('karvala_manolo', comparisons)
        
        # Check structure of comparison
        mondo_comparison = comparisons['mondo_duplantis']
        self.assertIn('reference_name', mondo_comparison)
        self.assertIn('phase_comparisons', mondo_comparison)
        self.assertIn('overall_score', mondo_comparison)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline"""
    
    def test_full_pipeline_with_synthetic_data(self):
        """Test the full analysis pipeline"""
        # Generate synthetic landmarks
        landmarks = {
            'left_hip': {'x': 100, 'y': 200, 'z': 0, 'visibility': 0.9},
            'right_hip': {'x': 120, 'y': 200, 'z': 0, 'visibility': 0.9},
            'left_shoulder': {'x': 100, 'y': 180, 'z': 0, 'visibility': 0.9},
            'right_shoulder': {'x': 120, 'y': 180, 'z': 0, 'visibility': 0.9},
            'left_ankle': {'x': 100, 'y': 250, 'z': 0, 'visibility': 0.9},
            'right_ankle': {'x': 120, 'y': 250, 'z': 0, 'visibility': 0.9}
        }
        landmarks_list = [landmarks] * 60
        video_info = {'fps': 30}
        
        # Phase detection
        detector = PhaseDetector()
        phases = detector.detect_phases(landmarks_list, video_info)
        self.assertGreater(len(phases), 0)
        
        # Energy calculation
        calculator = EnergyCalculator(athlete_mass=70.0)
        energies = calculator.calculate_phase_energies(landmarks_list, phases, video_info)
        self.assertGreater(len(energies), 0)
        
        # Performance comparison
        comparator = PerformanceComparator()
        comparisons = comparator.compare_performance(energies, 70.0)
        self.assertEqual(len(comparisons), 2)


if __name__ == '__main__':
    unittest.main()
