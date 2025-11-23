#!/usr/bin/env python3
"""
Example script demonstrating the AI_PVSim system with synthetic data
This can be used to test the system without a video file
"""

import numpy as np
from pv_analyzer import PhaseDetector, EnergyCalculator, PerformanceComparator
from pv_analyzer.phase_detector import VaultPhase


def generate_synthetic_landmarks(num_frames=180, fps=30):
    """
    Generate synthetic pose landmarks simulating a pole vault
    
    Args:
        num_frames: Number of frames to generate
        fps: Frames per second
        
    Returns:
        List of landmark dictionaries
    """
    landmarks_list = []
    
    for i in range(num_frames):
        # Simulate motion through different phases
        t = i / fps  # Time in seconds
        
        # Simulate horizontal motion (run, then slow down)
        if t < 3.0:  # Run phase
            x_pos = 100 + t * 150
            y_hip = 400
        elif t < 3.5:  # Plant/takeoff
            x_pos = 550 + (t - 3.0) * 50
            y_hip = 400 - (t - 3.0) * 100
        elif t < 4.5:  # Swing-up
            x_pos = 575
            y_hip = 350 - (t - 3.5) * 150
        elif t < 5.2:  # Extension/inversion
            x_pos = 580
            y_hip = 200 - (t - 4.5) * 80
        elif t < 5.6:  # Push-off
            x_pos = 585
            y_hip = 140 - (t - 5.2) * 50
        else:  # Pike/descent
            x_pos = 590 + (t - 5.6) * 20
            y_hip = 120 + (t - 5.6) * 100
        
        # Create landmark dictionary
        landmarks = {
            'nose': {'x': x_pos, 'y': y_hip - 40, 'z': 0, 'visibility': 0.99},
            'left_shoulder': {'x': x_pos - 15, 'y': y_hip - 30, 'z': 0, 'visibility': 0.95},
            'right_shoulder': {'x': x_pos + 15, 'y': y_hip - 30, 'z': 0, 'visibility': 0.95},
            'left_elbow': {'x': x_pos - 25, 'y': y_hip - 10, 'z': 0, 'visibility': 0.90},
            'right_elbow': {'x': x_pos + 25, 'y': y_hip - 10, 'z': 0, 'visibility': 0.90},
            'left_wrist': {'x': x_pos - 30, 'y': y_hip + 5, 'z': 0, 'visibility': 0.85},
            'right_wrist': {'x': x_pos + 30, 'y': y_hip + 5, 'z': 0, 'visibility': 0.85},
            'left_hip': {'x': x_pos - 10, 'y': y_hip, 'z': 0, 'visibility': 0.98},
            'right_hip': {'x': x_pos + 10, 'y': y_hip, 'z': 0, 'visibility': 0.98},
            'left_knee': {'x': x_pos - 15, 'y': y_hip + 30, 'z': 0, 'visibility': 0.92},
            'right_knee': {'x': x_pos + 15, 'y': y_hip + 30, 'z': 0, 'visibility': 0.92},
            'left_ankle': {'x': x_pos - 18, 'y': y_hip + 60, 'z': 0, 'visibility': 0.88},
            'right_ankle': {'x': x_pos + 18, 'y': y_hip + 60, 'z': 0, 'visibility': 0.88},
            'left_heel': {'x': x_pos - 20, 'y': y_hip + 65, 'z': 0, 'visibility': 0.85},
            'right_heel': {'x': x_pos + 20, 'y': y_hip + 65, 'z': 0, 'visibility': 0.85},
            'left_foot_index': {'x': x_pos - 18, 'y': y_hip + 68, 'z': 0, 'visibility': 0.82},
            'right_foot_index': {'x': x_pos + 18, 'y': y_hip + 68, 'z': 0, 'visibility': 0.82},
        }
        
        landmarks_list.append(landmarks)
    
    return landmarks_list


def main():
    """Run example analysis with synthetic data"""
    print("=" * 80)
    print("AI_PVSim - Example Demonstration with Synthetic Data")
    print("=" * 80)
    print()
    
    # Generate synthetic data
    print("[1/4] Generating synthetic pole vault data...")
    num_frames = 180
    fps = 30
    landmarks_list = generate_synthetic_landmarks(num_frames, fps)
    
    video_info = {
        'fps': fps,
        'width': 1920,
        'height': 1080,
        'total_frames': num_frames
    }
    
    print(f"✓ Generated {num_frames} frames of synthetic data\n")
    
    # Detect phases
    print("[2/4] Detecting pole vault phases...")
    phase_detector = PhaseDetector()
    phases = phase_detector.detect_phases(landmarks_list, video_info)
    
    print(f"✓ Detected {len(phases)} phases\n")
    print(phase_detector.get_phase_summary())
    
    # Calculate energies
    print("[3/4] Calculating energy for each phase...")
    athlete_mass = 70.0
    energy_calculator = EnergyCalculator(
        athlete_mass=athlete_mass,
        pixel_to_meter_ratio=0.01
    )
    phase_energies = energy_calculator.calculate_phase_energies(
        landmarks_list, phases, video_info
    )
    
    print("✓ Energy calculations complete\n")
    print(energy_calculator.get_energy_summary(phase_energies))
    
    # Compare to references
    print("[4/4] Comparing performance to Olympic athletes...")
    comparator = PerformanceComparator()
    comparisons = comparator.compare_performance(phase_energies, athlete_mass)
    
    print("✓ Performance comparison complete\n")
    print(comparator.get_comparison_summary())
    
    print("=" * 80)
    print("Example demonstration complete!")
    print("=" * 80)
    print("\nTo analyze a real video, use: python pv_sim.py path/to/video.mp4")


if __name__ == '__main__':
    main()
