"""
Example usage of the AI PVSim video analysis module.
This script demonstrates how to analyze a pole vault video.
"""

import sys
from video_analyzer import VideoAnalyzer


def main():
    """
    Main function to demonstrate video analysis usage.
    """
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <video_path> [output_video_path] [athlete_height_meters]")
        print("\nExample:")
        print("  python example_usage.py pole_vault.mp4")
        print("  python example_usage.py pole_vault.mp4 output_annotated.mp4")
        print("  python example_usage.py pole_vault.mp4 output_annotated.mp4 1.85")
        print("\nNote: athlete_height_meters is used for calibration (default: 1.8m)")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_video_path = sys.argv[2] if len(sys.argv) > 2 else None
    athlete_height = float(sys.argv[3]) if len(sys.argv) > 3 else 1.8
    
    print(f"\n{'='*60}")
    print("AI PVSim - Pole Vault Video Analysis")
    print(f"{'='*60}\n")
    
    # Initialize analyzer with athlete's height for calibration
    analyzer = VideoAnalyzer(calibration_height_meters=athlete_height)
    
    # Analyze the video
    print(f"Analyzing video: {video_path}")
    print(f"Calibration height: {athlete_height}m")
    if output_video_path:
        print(f"Output will be saved to: {output_video_path}")
    print()
    
    frame_data = analyzer.analyze_video(video_path, output_video_path)
    
    # Get statistics
    print("\n" + "="*60)
    print("Analysis Statistics:")
    print("="*60)
    stats = analyzer.get_statistics()
    
    print(f"\nTotal frames analyzed: {stats['total_frames']}")
    
    if stats['avg_pole_angle'] != 0:
        print(f"\nPole Angle Statistics:")
        print(f"  Average: {stats['avg_pole_angle']:.2f}°")
        print(f"  Maximum: {stats['max_pole_angle']:.2f}°")
        print(f"  Minimum: {stats['min_pole_angle']:.2f}°")
    
    if 'avg_athlete_height_meters' in stats:
        print(f"\nAthlete Measurements:")
        print(f"  Average height: {stats['avg_athlete_height_meters']:.2f}m")
    
    if 'avg_pole_length_meters' in stats:
        print(f"\nPole Measurements:")
        print(f"  Average length: {stats['avg_pole_length_meters']:.2f}m")
    
    # Export data for comparison
    output_json = video_path.rsplit('.', 1)[0] + '_analysis.json'
    analyzer.export_data(output_json)
    
    print(f"\n{'='*60}")
    print("Analysis Complete!")
    print(f"{'='*60}\n")
    print(f"Data exported to: {output_json}")
    print("This data can be used to compare with other pole vaulters.")
    print()


if __name__ == "__main__":
    main()
