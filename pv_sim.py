#!/usr/bin/env python3
"""
AI_PVSim - Pole Vault Video Analysis System
Main application for analyzing pole vault videos
"""

import argparse
import sys
import os
from pv_analyzer import VideoProcessor, PhaseDetector, EnergyCalculator, PerformanceComparator


def main():
    """Main entry point for the pole vault analyzer"""
    parser = argparse.ArgumentParser(
        description='Analyze pole vault videos and compare performance to Olympic athletes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pv_sim.py video.mp4
  python pv_sim.py video.mp4 --mass 75 --height 1.85
  python pv_sim.py video.mp4 --mass 70 --output analysis.txt
        """
    )
    
    parser.add_argument('video', help='Path to the pole vault video file')
    parser.add_argument('--mass', type=float, default=70.0,
                       help='Athlete mass in kg (default: 70.0)')
    parser.add_argument('--height', type=float, default=1.80,
                       help='Athlete height in meters (default: 1.80)')
    parser.add_argument('--pixel-ratio', type=float, default=0.01,
                       help='Pixel to meter conversion ratio (default: 0.01)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output file for analysis results (default: print to console)')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        sys.exit(1)
    
    if args.mass <= 0 or args.mass > 200:
        print(f"Error: Invalid mass: {args.mass}. Must be between 0 and 200 kg.")
        sys.exit(1)
    
    print("=" * 80)
    print("AI_PVSim - Pole Vault Video Analysis System")
    print("=" * 80)
    print(f"Video: {args.video}")
    print(f"Athlete Mass: {args.mass} kg")
    print(f"Athlete Height: {args.height} m")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Process video and extract pose landmarks
        print("[1/4] Processing video and extracting pose landmarks...")
        video_processor = VideoProcessor()
        frames, landmarks_list, video_info = video_processor.process_video(args.video)
        video_processor.close()
        
        if not landmarks_list or all(lm is None for lm in landmarks_list):
            print("Error: No pose landmarks detected in video. Ensure the athlete is visible.")
            sys.exit(1)
        
        print(f"✓ Extracted landmarks from {len(landmarks_list)} frames\n")
        
        # Step 2: Detect pole vault phases
        print("[2/4] Detecting pole vault phases...")
        phase_detector = PhaseDetector()
        phases = phase_detector.detect_phases(landmarks_list, video_info)
        
        if not phases:
            print("Error: No phases detected in video.")
            sys.exit(1)
        
        print(f"✓ Detected {len(phases)} phases\n")
        phase_summary = phase_detector.get_phase_summary()
        print(phase_summary)
        
        # Step 3: Calculate energy for each phase
        print("[3/4] Calculating energy for each phase...")
        energy_calculator = EnergyCalculator(
            athlete_mass=args.mass,
            pixel_to_meter_ratio=args.pixel_ratio
        )
        phase_energies = energy_calculator.calculate_phase_energies(
            landmarks_list, phases, video_info
        )
        
        print("✓ Energy calculations complete\n")
        energy_summary = energy_calculator.get_energy_summary(phase_energies)
        print(energy_summary)
        
        # Step 4: Compare to Olympic athletes
        print("[4/4] Comparing performance to Olympic athletes...")
        comparator = PerformanceComparator()
        comparisons = comparator.compare_performance(phase_energies, args.mass)
        
        print("✓ Performance comparison complete\n")
        comparison_summary = comparator.get_comparison_summary()
        print(comparison_summary)
        
        # Save output if requested
        if args.output:
            with open(args.output, 'w') as f:
                f.write("AI_PVSim - Pole Vault Video Analysis Report\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Video: {args.video}\n")
                f.write(f"Athlete Mass: {args.mass} kg\n")
                f.write(f"Athlete Height: {args.height} m\n")
                f.write("=" * 80 + "\n\n")
                f.write(phase_summary)
                f.write("\n")
                f.write(energy_summary)
                f.write("\n")
                f.write(comparison_summary)
            
            print(f"Analysis saved to: {args.output}")
        
        print("\n" + "=" * 80)
        print("Analysis complete!")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
