"""
Comprehensive test script for pole vault video analysis.
This script creates synthetic test videos and analyzes them to demonstrate the system.
"""

import os
import sys
from create_test_video import create_test_video
from video_analyzer import PoleVaultAnalyzer


def run_comprehensive_test():
    """Run a comprehensive test of the video analysis system."""
    
    print("=" * 80)
    print("POLE VAULT VIDEO ANALYSIS - COMPREHENSIVE TEST")
    print("=" * 80)
    print()
    
    # Step 1: Create synthetic test videos
    print("STEP 1: Creating synthetic test videos")
    print("-" * 80)
    
    test_videos = []
    
    # Create a normal test video
    print("\n1. Creating normal test video...")
    video1 = create_test_video(
        output_path="videos/test_normal.mp4",
        duration_sec=3,
        fps=30
    )
    test_videos.append({
        'path': video1,
        'description': 'Normal synthetic pole vault motion (3 seconds)'
    })
    
    # Create a longer test video
    print("\n2. Creating extended test video...")
    video2 = create_test_video(
        output_path="videos/test_extended.mp4",
        duration_sec=5,
        fps=30
    )
    test_videos.append({
        'path': video2,
        'description': 'Extended synthetic pole vault motion (5 seconds)'
    })
    
    print("\n" + "=" * 80)
    print(f"✓ Created {len(test_videos)} test video(s)")
    print("=" * 80)
    
    # Step 2: Analyze videos
    print("\n\nSTEP 2: Analyzing test videos")
    print("-" * 80)
    
    analyzer = PoleVaultAnalyzer()
    all_results = []
    
    try:
        for i, video_info in enumerate(test_videos, 1):
            print(f"\n{'='*80}")
            print(f"TEST {i}/{len(test_videos)}: {video_info['description']}")
            print(f"Path: {video_info['path']}")
            print(f"{'='*80}\n")
            
            # Analyze the video
            print("Analyzing video for pose data...")
            try:
                results = analyzer.analyze_video(video_info['path'])
                print(f"✓ Analysis complete!")
                print(f"  - Frames analyzed: {results['frames_analyzed']}/{results['frame_count']}")
                print(f"  - Duration: {results['duration']:.2f}s")
                print(f"  - FPS: {results['fps']:.2f}")
                print(f"  - Detection rate: {results['frames_analyzed']/results['frame_count']*100:.1f}%\n")
            except Exception as e:
                print(f"❌ Error analyzing video: {e}")
                import traceback
                traceback.print_exc()
                continue
            
            # Check for inconsistencies
            print("Checking for data inconsistencies...")
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
            
            # Display sample of detected inconsistencies
            if inconsistencies['missing_frames']:
                print("  Sample missing frames:")
                for gap in inconsistencies['missing_frames'][:3]:
                    print(f"    - Frames {gap['start_frame']}-{gap['end_frame']}: {gap['gap']} frames missing")
            
            if inconsistencies['low_visibility_frames']:
                print("  Sample low visibility frames:")
                for frame in inconsistencies['low_visibility_frames'][:3]:
                    print(f"    - Frame {frame['frame']} (t={frame['time']:.2f}s): {frame['low_visibility_count']} landmarks")
            
            if inconsistencies['sudden_movements']:
                print("  Sample sudden movements:")
                for movement in inconsistencies['sudden_movements'][:3]:
                    print(f"    - Frame {movement['frame']} (t={movement['time']:.2f}s): {movement['metric']} change={movement['change']:.3f}")
            
            if inconsistencies['tracking_issues']:
                print("  Tracking issues:")
                for issue in inconsistencies['tracking_issues']:
                    print(f"    - {issue}")
            
            print()
            
            # Save results
            print("Saving results...")
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
            
            print("RESULTS BY VIDEO:")
            print("-" * 80)
            for i, result in enumerate(all_results, 1):
                print(f"\n{i}. {result['video']['description']}")
                print(f"   Path: {result['video']['path']}")
                print(f"   Frames detected: {result['results']['frames_analyzed']}/{result['results']['frame_count']}")
                print(f"   Detection rate: {result['results']['frames_analyzed']/result['results']['frame_count']*100:.1f}%")
                print(f"   Total issues found: {result['total_issues']}")
                print(f"     - Missing frame gaps: {len(result['inconsistencies']['missing_frames'])}")
                print(f"     - Low visibility: {len(result['inconsistencies']['low_visibility_frames'])}")
                print(f"     - Sudden movements: {len(result['inconsistencies']['sudden_movements'])}")
                print(f"     - Tracking issues: {len(result['inconsistencies']['tracking_issues'])}")
                print(f"   Report: {result['files']['summary']}")
            
            # Overall assessment
            print("\n" + "-" * 80)
            print("OVERALL ASSESSMENT:")
            print("-" * 80)
            total_all_issues = sum(r['total_issues'] for r in all_results)
            total_frames = sum(r['results']['frame_count'] for r in all_results)
            total_detected = sum(r['results']['frames_analyzed'] for r in all_results)
            
            print(f"Total videos analyzed: {len(all_results)}")
            print(f"Total frames: {total_frames}")
            print(f"Total frames with pose detected: {total_detected} ({total_detected/total_frames*100:.1f}%)")
            print(f"Total inconsistencies detected: {total_all_issues}")
            
            if total_all_issues == 0:
                print("\n✓ SUCCESS: No inconsistencies detected - videos analyzed cleanly!")
            else:
                print(f"\n⚠ CAUTION: {total_all_issues} inconsistencies detected across all videos")
                print("  See individual reports for details")
            
            print("\nRECOMMENDATIONS:")
            print("-" * 80)
            print("1. Review the generated CSV files for detailed frame-by-frame data")
            print("2. Check the inconsistencies reports for specific issues")
            print("3. For real pole vault videos, ensure:")
            print("   - Good lighting conditions")
            print("   - Clear view of the athlete")
            print("   - Minimal background clutter")
            print("   - Stable camera position")
            print("4. The system works best with videos where the athlete is clearly visible")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        print("\nAll output files are located in the 'output/' directory.")
        print("Test videos are located in the 'videos/' directory.")
        
        return all_results
        
    finally:
        analyzer.cleanup()


if __name__ == "__main__":
    run_comprehensive_test()
