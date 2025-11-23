"""
Demonstration script that shows the video analysis system with mock data.
This demonstrates the full pipeline including data recording and inconsistency detection.
"""

import os
import json
import pandas as pd
from datetime import datetime
import numpy as np
from video_analyzer import PoleVaultAnalyzer


def create_mock_analysis_data():
    """
    Create mock analysis data to demonstrate the system's capabilities.
    This simulates what would be extracted from a real pole vault video.
    """
    print("Creating mock pole vault analysis data...")
    print("-" * 80)
    
    # Simulate 90 frames (3 seconds at 30fps) of pole vault motion
    fps = 30
    duration = 3.0
    total_frames = int(fps * duration)
    
    frame_data = []
    
    # Simulate pole vault motion phases:
    # Phase 1: Approach run (frames 0-30)
    # Phase 2: Plant and take-off (frames 30-45)
    # Phase 3: Swing and inversion (frames 45-60)
    # Phase 4: Extension and clearance (frames 60-75)
    # Phase 5: Landing (frames 75-90)
    
    for frame_num in range(total_frames):
        time = frame_num / fps
        progress = frame_num / total_frames
        
        # Simulate different phases of motion
        if frame_num < 30:  # Approach
            phase = "approach"
            vertical_pos = 0.8  # Near ground
            speed = 0.5
        elif frame_num < 45:  # Plant and take-off
            phase = "plant"
            vertical_pos = 0.8 - (frame_num - 30) / 15 * 0.3  # Rising
            speed = 0.3
        elif frame_num < 60:  # Swing and inversion
            phase = "swing"
            vertical_pos = 0.5 - (frame_num - 45) / 15 * 0.2  # Peak height
            speed = 0.1
        elif frame_num < 75:  # Extension
            phase = "extension"
            vertical_pos = 0.3 + (frame_num - 60) / 15 * 0.2  # Descending
            speed = 0.2
        else:  # Landing
            phase = "landing"
            vertical_pos = 0.5 + (frame_num - 75) / 15 * 0.3  # Back to ground
            speed = 0.4
        
        # Add some natural variation
        noise = np.random.normal(0, 0.01)
        
        # Create landmark data for this frame
        landmarks = {
            'frame': frame_num,
            'time': time,
            'phase': phase,
            
            # Key body points (normalized coordinates 0-1)
            'nose_x': 0.5 + noise,
            'nose_y': vertical_pos - 0.1 + noise,
            'nose_z': 0.0,
            'nose_visibility': 0.95 + np.random.normal(0, 0.02),
            
            'left_shoulder_x': 0.45 + noise,
            'left_shoulder_y': vertical_pos + noise,
            'left_shoulder_z': 0.05,
            'left_shoulder_visibility': 0.93 + np.random.normal(0, 0.03),
            
            'right_shoulder_x': 0.55 + noise,
            'right_shoulder_y': vertical_pos + noise,
            'right_shoulder_z': 0.05,
            'right_shoulder_visibility': 0.92 + np.random.normal(0, 0.03),
            
            'left_hip_x': 0.47 + noise,
            'left_hip_y': vertical_pos + 0.15 + noise,
            'left_hip_z': 0.0,
            'left_hip_visibility': 0.90 + np.random.normal(0, 0.04),
            
            'right_hip_x': 0.53 + noise,
            'right_hip_y': vertical_pos + 0.15 + noise,
            'right_hip_z': 0.0,
            'right_hip_visibility': 0.89 + np.random.normal(0, 0.04),
            
            'center_of_mass_y': vertical_pos + 0.075,
        }
        
        # Simulate occasional tracking issues
        if frame_num in [22, 23, 67]:  # Missing frames
            continue
        
        # Simulate low visibility in some frames
        if frame_num in [12, 38, 55, 72]:
            for key in landmarks:
                if key.endswith('_visibility'):
                    landmarks[key] = 0.35  # Low visibility
        
        frame_data.append(landmarks)
    
    # Create simulated analysis results
    analysis_results = {
        'video_path': 'mock_pole_vault_video.mp4',
        'fps': fps,
        'frame_count': total_frames,
        'duration': duration,
        'frames_analyzed': len(frame_data),
        'frame_data': frame_data,
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"✓ Created mock data with {len(frame_data)} frames")
    print(f"  Simulated {total_frames} frame video at {fps} FPS ({duration}s)")
    print(f"  Detection rate: {len(frame_data)/total_frames*100:.1f}%")
    
    return analysis_results


def run_demonstration():
    """Run a demonstration of the video analysis system."""
    print("=" * 80)
    print("POLE VAULT VIDEO ANALYSIS - DEMONSTRATION WITH MOCK DATA")
    print("=" * 80)
    print()
    print("This demonstration shows the complete analysis pipeline:")
    print("1. Video analysis and pose data extraction")
    print("2. Data recording to CSV format")
    print("3. Inconsistency detection")
    print("4. Report generation")
    print()
    print("Note: Using mock data since MediaPipe requires real human imagery")
    print("=" * 80)
    print()
    
    # Create mock analysis data
    analysis_results = create_mock_analysis_data()
    
    # Create analyzer instance
    analyzer = PoleVaultAnalyzer()
    
    try:
        print("\n" + "-" * 80)
        print("STEP 1: Checking for inconsistencies...")
        print("-" * 80)
        
        inconsistencies = analyzer.check_inconsistencies(analysis_results)
        
        # Count total issues
        total_issues = (
            len(inconsistencies['missing_frames']) +
            len(inconsistencies['low_visibility_frames']) +
            len(inconsistencies['sudden_movements']) +
            len(inconsistencies['tracking_issues'])
        )
        
        print(f"\n✓ Inconsistency check complete!")
        print(f"\nISSUES FOUND:")
        print(f"  - Missing frame gaps: {len(inconsistencies['missing_frames'])}")
        if inconsistencies['missing_frames']:
            print(f"    Details:")
            for gap in inconsistencies['missing_frames']:
                print(f"      Frame {gap['start_frame']} to {gap['end_frame']}: {gap['gap']} frames missing")
        
        print(f"  - Low visibility frames: {len(inconsistencies['low_visibility_frames'])}")
        if inconsistencies['low_visibility_frames']:
            print(f"    Sample issues:")
            for frame in inconsistencies['low_visibility_frames'][:3]:
                print(f"      Frame {frame['frame']} (t={frame['time']:.2f}s): {frame['low_visibility_count']} landmarks affected")
        
        print(f"  - Sudden movements: {len(inconsistencies['sudden_movements'])}")
        if inconsistencies['sudden_movements']:
            print(f"    Sample issues:")
            for movement in inconsistencies['sudden_movements'][:3]:
                print(f"      Frame {movement['frame']} (t={movement['time']:.2f}s): {movement['metric']} changed by {movement['change']:.3f}")
        
        print(f"  - Tracking issues: {len(inconsistencies['tracking_issues'])}")
        
        print(f"\n  TOTAL ISSUES: {total_issues}")
        
        print("\n" + "-" * 80)
        print("STEP 2: Saving results to files...")
        print("-" * 80)
        
        files = analyzer.save_results(analysis_results, inconsistencies)
        
        print(f"\n✓ Results saved successfully!")
        print(f"  - CSV Data: {files['csv']}")
        print(f"  - JSON Analysis: {files['json']}")
        print(f"  - Text Summary: {files['summary']}")
        
        # Display summary of what was saved
        print("\n" + "-" * 80)
        print("STEP 3: Reviewing saved data...")
        print("-" * 80)
        
        # Load and display sample CSV data
        df = pd.DataFrame(analysis_results['frame_data'])
        print(f"\n✓ CSV contains {len(df)} rows with {len(df.columns)} columns")
        print(f"  Columns: {', '.join(df.columns[:10])}...")
        print(f"\n  First few frames:")
        print(df[['frame', 'time', 'phase', 'center_of_mass_y', 'nose_visibility']].head(10).to_string(index=False))
        
        # Show summary statistics
        print(f"\n  Summary statistics:")
        print(f"    Average center of mass Y: {df['center_of_mass_y'].mean():.3f}")
        print(f"    Min center of mass Y: {df['center_of_mass_y'].min():.3f} (highest point)")
        print(f"    Max center of mass Y: {df['center_of_mass_y'].max():.3f} (lowest point)")
        print(f"    Average visibility: {df['nose_visibility'].mean():.3f}")
        
        # Display the text summary
        print("\n" + "-" * 80)
        print("STEP 4: Final inconsistencies report...")
        print("-" * 80)
        
        with open(files['summary'], 'r') as f:
            summary_content = f.read()
        print(f"\n{summary_content}")
        
        print("\n" + "=" * 80)
        print("DEMONSTRATION COMPLETE")
        print("=" * 80)
        print("\n✓ The video analysis system successfully:")
        print("  1. Processed video frame data")
        print("  2. Detected multiple inconsistencies:")
        print(f"     - {len(inconsistencies['missing_frames'])} missing frame gaps")
        print(f"     - {len(inconsistencies['low_visibility_frames'])} low visibility issues")
        print(f"     - {len(inconsistencies['sudden_movements'])} sudden movement anomalies")
        print("  3. Saved comprehensive data to CSV, JSON, and text formats")
        print("  4. Generated detailed inconsistency reports")
        print("\nAll output files are in the 'output/' directory.")
        print("\nFor real pole vault videos:")
        print("  - Use actual video files with clear human figures")
        print("  - MediaPipe will automatically detect body poses")
        print("  - The same analysis pipeline will process the data")
        print("  - All inconsistencies will be automatically detected and reported")
        
        return {
            'analysis': analysis_results,
            'inconsistencies': inconsistencies,
            'files': files,
            'total_issues': total_issues
        }
    
    finally:
        analyzer.cleanup()


if __name__ == "__main__":
    run_demonstration()
