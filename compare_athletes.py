"""
Example script for comparing two pole vaulters' performance using exported data.
This demonstrates how to use the JSON export for athlete comparison.
"""

import json
import sys
import numpy as np
from typing import Dict, List


def load_analysis_data(json_path: str) -> Dict:
    """Load analysis data from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)


def compare_pole_angles(data1: Dict, data2: Dict, athlete1_name: str = "Athlete 1", athlete2_name: str = "Athlete 2"):
    """Compare pole angles between two athletes."""
    print("\n" + "="*60)
    print("POLE ANGLE COMPARISON")
    print("="*60)
    
    # Extract pole angles
    angles1 = [f['pole_angle'] for f in data1['frames'] if f['pole_angle'] is not None]
    angles2 = [f['pole_angle'] for f in data2['frames'] if f['pole_angle'] is not None]
    
    if angles1 and angles2:
        print(f"\n{athlete1_name}:")
        print(f"  Average angle: {np.mean(angles1):.2f}°")
        print(f"  Max angle: {np.max(angles1):.2f}°")
        print(f"  Min angle: {np.min(angles1):.2f}°")
        print(f"  Angle range: {np.max(angles1) - np.min(angles1):.2f}°")
        
        print(f"\n{athlete2_name}:")
        print(f"  Average angle: {np.mean(angles2):.2f}°")
        print(f"  Max angle: {np.max(angles2):.2f}°")
        print(f"  Min angle: {np.min(angles2):.2f}°")
        print(f"  Angle range: {np.max(angles2) - np.min(angles2):.2f}°")
        
        print(f"\nDifference:")
        print(f"  Average angle: {np.mean(angles1) - np.mean(angles2):+.2f}°")
        print(f"  Max angle: {np.max(angles1) - np.max(angles2):+.2f}°")
    else:
        print("Insufficient pole angle data for comparison")


def compare_body_positions(data1: Dict, data2: Dict, frame_idx: int, athlete1_name: str = "Athlete 1", athlete2_name: str = "Athlete 2"):
    """Compare body positions at a specific frame."""
    print("\n" + "="*60)
    print(f"BODY POSITION COMPARISON AT FRAME {frame_idx}")
    print("="*60)
    
    if frame_idx >= len(data1['frames']) or frame_idx >= len(data2['frames']):
        print("Frame index out of range for one or both athletes")
        return
    
    frame1 = data1['frames'][frame_idx]
    frame2 = data2['frames'][frame_idx]
    
    # Compare key landmarks if available
    key_landmarks = ['NOSE', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_HIP', 'RIGHT_HIP']
    
    for landmark in key_landmarks:
        if landmark in frame1['athlete_keypoints'] and landmark in frame2['athlete_keypoints']:
            pos1 = frame1['athlete_keypoints'][landmark]
            pos2 = frame2['athlete_keypoints'][landmark]
            
            # Convert to real-world coordinates if calibration available
            if data1['pixels_per_meter'] and data2['pixels_per_meter']:
                x1_m = pos1[0] / data1['pixels_per_meter']
                y1_m = pos1[1] / data1['pixels_per_meter']
                x2_m = pos2[0] / data2['pixels_per_meter']
                y2_m = pos2[1] / data2['pixels_per_meter']
                
                print(f"\n{landmark}:")
                print(f"  {athlete1_name}: ({x1_m:.2f}m, {y1_m:.2f}m) visibility: {pos1[2]:.2f}")
                print(f"  {athlete2_name}: ({x2_m:.2f}m, {y2_m:.2f}m) visibility: {pos2[2]:.2f}")
                print(f"  Difference: ({x1_m - x2_m:+.2f}m, {y1_m - y2_m:+.2f}m)")


def analyze_vault_phases(data: Dict, athlete_name: str = "Athlete"):
    """Analyze different phases of the vault based on pole angle changes."""
    print("\n" + "="*60)
    print(f"VAULT PHASE ANALYSIS - {athlete_name}")
    print("="*60)
    
    angles = []
    timestamps = []
    
    for frame in data['frames']:
        if frame['pole_angle'] is not None:
            angles.append(frame['pole_angle'])
            timestamps.append(frame['timestamp'])
    
    if len(angles) < 10:
        print("Insufficient data for phase analysis")
        return
    
    # Find key phases based on angle changes
    max_angle_idx = np.argmax(angles)
    min_angle_idx = np.argmin(angles)
    
    print(f"\nApproach/Plant Phase:")
    print(f"  Start: {timestamps[0]:.2f}s, Angle: {angles[0]:.2f}°")
    
    print(f"\nMaximum Pole Bend:")
    print(f"  Time: {timestamps[max_angle_idx]:.2f}s, Angle: {angles[max_angle_idx]:.2f}°")
    
    print(f"\nMinimum Angle (Peak Extension):")
    print(f"  Time: {timestamps[min_angle_idx]:.2f}s, Angle: {angles[min_angle_idx]:.2f}°")
    
    print(f"\nTotal Vault Duration: {timestamps[-1]:.2f}s")


def main():
    """Main comparison function."""
    if len(sys.argv) < 3:
        print("Usage: python compare_athletes.py <athlete1_data.json> <athlete2_data.json> [athlete1_name] [athlete2_name]")
        print("\nExample:")
        print("  python compare_athletes.py john_analysis.json mary_analysis.json John Mary")
        print("\nThis script compares two athletes' pole vault performance using exported JSON data.")
        sys.exit(1)
    
    data1_path = sys.argv[1]
    data2_path = sys.argv[2]
    athlete1_name = sys.argv[3] if len(sys.argv) > 3 else "Athlete 1"
    athlete2_name = sys.argv[4] if len(sys.argv) > 4 else "Athlete 2"
    
    print(f"\n{'='*60}")
    print("AI PVSim - Athlete Performance Comparison")
    print(f"{'='*60}")
    print(f"\nComparing: {athlete1_name} vs {athlete2_name}")
    
    # Load data
    print(f"\nLoading data...")
    data1 = load_analysis_data(data1_path)
    data2 = load_analysis_data(data2_path)
    
    print(f"  {athlete1_name}: {data1['total_frames']} frames")
    print(f"  {athlete2_name}: {data2['total_frames']} frames")
    
    # Perform comparisons
    compare_pole_angles(data1, data2, athlete1_name, athlete2_name)
    
    # Compare at mid-point frame
    mid_frame = min(len(data1['frames']), len(data2['frames'])) // 2
    compare_body_positions(data1, data2, mid_frame, athlete1_name, athlete2_name)
    
    # Analyze each athlete's phases
    analyze_vault_phases(data1, athlete1_name)
    analyze_vault_phases(data2, athlete2_name)
    
    print("\n" + "="*60)
    print("Comparison Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
