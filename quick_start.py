#!/usr/bin/env python3
"""
Quick Start Guide - Using the Pole Vault Video Analyzer

This script shows the basic usage patterns for the video analysis system.
"""

from video_analyzer import PoleVaultAnalyzer


def example_1_analyze_local_video():
    """Example 1: Analyze a local video file."""
    print("=" * 80)
    print("Example 1: Analyzing a local video file")
    print("=" * 80)
    
    analyzer = PoleVaultAnalyzer()
    
    try:
        # Path to your video file
        video_path = "path/to/your/pole_vault_video.mp4"
        
        # Analyze the video
        print(f"Analyzing: {video_path}")
        results = analyzer.analyze_video(video_path)
        
        # Check for inconsistencies
        print("Checking for inconsistencies...")
        inconsistencies = analyzer.check_inconsistencies(results)
        
        # Save results
        print("Saving results...")
        files = analyzer.save_results(results, inconsistencies)
        
        print(f"\n✓ Analysis complete!")
        print(f"  Results saved to: {files['summary']}")
        
    finally:
        analyzer.cleanup()


def example_2_download_and_analyze():
    """Example 2: Download a video from URL and analyze it."""
    print("\n" + "=" * 80)
    print("Example 2: Download and analyze a video from URL")
    print("=" * 80)
    
    analyzer = PoleVaultAnalyzer()
    
    try:
        # YouTube or other video URL
        url = "https://www.youtube.com/watch?v=VIDEO_ID"
        
        # Download the video
        print(f"Downloading: {url}")
        video_path = analyzer.download_video(url)
        
        if video_path:
            # Analyze the downloaded video
            print(f"Analyzing: {video_path}")
            results = analyzer.analyze_video(video_path)
            
            # Check for inconsistencies
            inconsistencies = analyzer.check_inconsistencies(results)
            
            # Save results
            files = analyzer.save_results(results, inconsistencies)
            
            print(f"\n✓ Analysis complete!")
            print(f"  Video: {video_path}")
            print(f"  Results: {files['summary']}")
        else:
            print("Failed to download video")
            
    finally:
        analyzer.cleanup()


def example_3_batch_analysis():
    """Example 3: Analyze multiple videos."""
    print("\n" + "=" * 80)
    print("Example 3: Batch analysis of multiple videos")
    print("=" * 80)
    
    analyzer = PoleVaultAnalyzer()
    
    try:
        # List of video files
        videos = [
            "videos/athlete1_attempt1.mp4",
            "videos/athlete1_attempt2.mp4",
            "videos/athlete2_attempt1.mp4",
        ]
        
        results_summary = []
        
        for video_path in videos:
            print(f"\nAnalyzing: {video_path}")
            
            try:
                results = analyzer.analyze_video(video_path)
                inconsistencies = analyzer.check_inconsistencies(results)
                files = analyzer.save_results(results, inconsistencies)
                
                # Track summary
                total_issues = (
                    len(inconsistencies['missing_frames']) +
                    len(inconsistencies['low_visibility_frames']) +
                    len(inconsistencies['sudden_movements']) +
                    len(inconsistencies['tracking_issues'])
                )
                
                results_summary.append({
                    'video': video_path,
                    'frames': results['frames_analyzed'],
                    'issues': total_issues,
                    'report': files['summary']
                })
                
            except Exception as e:
                print(f"  Error: {e}")
                continue
        
        # Print summary
        print("\n" + "=" * 80)
        print("BATCH ANALYSIS SUMMARY")
        print("=" * 80)
        for item in results_summary:
            print(f"\n{item['video']}")
            print(f"  Frames analyzed: {item['frames']}")
            print(f"  Issues found: {item['issues']}")
            print(f"  Report: {item['report']}")
            
    finally:
        analyzer.cleanup()


def example_4_custom_thresholds():
    """Example 4: Using custom detection thresholds."""
    print("\n" + "=" * 80)
    print("Example 4: Custom detection thresholds")
    print("=" * 80)
    
    analyzer = PoleVaultAnalyzer()
    
    # Customize thresholds
    analyzer.LOW_VISIBILITY_THRESHOLD = 0.6  # More strict (default: 0.5)
    analyzer.LOW_VISIBILITY_COUNT_THRESHOLD = 3  # More sensitive (default: 5)
    analyzer.SUDDEN_MOVEMENT_THRESHOLD = 0.2  # More sensitive (default: 0.3)
    
    try:
        video_path = "path/to/video.mp4"
        
        print(f"Analyzing with custom thresholds:")
        print(f"  Low visibility: < {analyzer.LOW_VISIBILITY_THRESHOLD}")
        print(f"  Low visibility count: > {analyzer.LOW_VISIBILITY_COUNT_THRESHOLD} landmarks")
        print(f"  Sudden movement: > {analyzer.SUDDEN_MOVEMENT_THRESHOLD} change")
        
        results = analyzer.analyze_video(video_path)
        inconsistencies = analyzer.check_inconsistencies(results)
        files = analyzer.save_results(results, inconsistencies)
        
        print(f"\n✓ Analysis complete with custom settings")
        
    finally:
        analyzer.cleanup()


if __name__ == "__main__":
    print("POLE VAULT VIDEO ANALYZER - QUICK START GUIDE")
    print("=" * 80)
    print("\nThis guide shows common usage patterns.")
    print("Uncomment the example you want to run.\n")
    
    # Uncomment one of these to run:
    
    # example_1_analyze_local_video()
    # example_2_download_and_analyze()
    # example_3_batch_analysis()
    # example_4_custom_thresholds()
    
    # Or run the demonstration:
    print("\nRunning demonstration with mock data...")
    print("(To analyze real videos, edit this file and uncomment an example above)\n")
    
    import demo_analysis
    demo_analysis.run_demonstration()
