"""
Test script for pole vault video analysis using online examples.
This script downloads and analyzes pole vault videos from online sources.
"""

import os
import sys
from video_analyzer import PoleVaultAnalyzer


def test_with_online_examples():
    """Test the video analyzer with online pole vault examples."""
    
    print("=" * 80)
    print("POLE VAULT VIDEO ANALYSIS TEST - ONLINE EXAMPLES")
    print("=" * 80)
    print()
    
    # List of online pole vault video examples
    # Using publicly available YouTube videos of pole vault competitions
    test_videos = [
        {
            'url': 'https://www.youtube.com/watch?v=wz9nQ-IsOLQ',
            'description': 'Pole Vault Technique Example'
        },
        # Add more URLs as needed
    ]
    
    print(f"Testing with {len(test_videos)} online video(s)\n")
    
    analyzer = PoleVaultAnalyzer()
    all_results = []
    
    try:
        for i, video_info in enumerate(test_videos, 1):
            print(f"\n{'='*80}")
            print(f"TEST {i}/{len(test_videos)}: {video_info['description']}")
            print(f"URL: {video_info['url']}")
            print(f"{'='*80}\n")
            
            # Download the video
            print("Step 1: Downloading video...")
            video_path = analyzer.download_video(video_info['url'])
            
            if not video_path:
                print(f"❌ Failed to download video from {video_info['url']}")
                print("Skipping to next video...\n")
                continue
            
            print(f"✓ Successfully downloaded to: {video_path}\n")
            
            # Analyze the video
            print("Step 2: Analyzing video for pose data...")
            try:
                results = analyzer.analyze_video(video_path)
                print(f"✓ Analysis complete!")
                print(f"  - Frames analyzed: {results['frames_analyzed']}/{results['frame_count']}")
                print(f"  - Duration: {results['duration']:.2f}s")
                print(f"  - FPS: {results['fps']:.2f}\n")
            except Exception as e:
                print(f"❌ Error analyzing video: {e}")
                print("Skipping to next video...\n")
                continue
            
            # Check for inconsistencies
            print("Step 3: Checking for data inconsistencies...")
            inconsistencies = analyzer.check_inconsistencies(results)
            
            # Count total issues
            total_issues = (
                len(inconsistencies['missing_frames']) +
                len(inconsistencies['low_visibility_frames']) +
                len(inconsistencies['sudden_movements']) +
                len(inconsistencies['tracking_issues'])
            )
            
            print(f"✓ Inconsistency check complete!")
            print(f"  - Missing frame gaps: {len(inconsistencies['missing_frames'])}")
            print(f"  - Low visibility frames: {len(inconsistencies['low_visibility_frames'])}")
            print(f"  - Sudden movements: {len(inconsistencies['sudden_movements'])}")
            print(f"  - Tracking issues: {len(inconsistencies['tracking_issues'])}")
            print(f"  - TOTAL ISSUES: {total_issues}\n")
            
            # Save results
            print("Step 4: Saving results...")
            files = analyzer.save_results(results, inconsistencies)
            print(f"✓ Results saved!")
            print(f"  - Data: {files['csv']}")
            print(f"  - Analysis: {files['json']}")
            print(f"  - Summary: {files['summary']}\n")
            
            all_results.append({
                'video': video_info,
                'results': results,
                'inconsistencies': inconsistencies,
                'files': files,
                'total_issues': total_issues
            })
        
        # Print summary report
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()
        
        if not all_results:
            print("❌ No videos were successfully analyzed.")
        else:
            print(f"✓ Successfully analyzed {len(all_results)} video(s)\n")
            
            for i, result in enumerate(all_results, 1):
                print(f"{i}. {result['video']['description']}")
                print(f"   Total issues found: {result['total_issues']}")
                print(f"   Report: {result['files']['summary']}")
                print()
            
            # Overall assessment
            total_all_issues = sum(r['total_issues'] for r in all_results)
            print(f"Overall: {total_all_issues} total inconsistencies across all videos")
            
            if total_all_issues == 0:
                print("✓ No inconsistencies detected - videos analyzed cleanly!")
            else:
                print("⚠ Some inconsistencies detected - see individual reports for details")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        
        return all_results
        
    finally:
        analyzer.cleanup()


if __name__ == "__main__":
    test_with_online_examples()
