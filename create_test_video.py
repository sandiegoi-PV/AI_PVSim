"""
Create a synthetic test video for pole vault analysis.
This creates a simple animation of a stick figure for testing the video analysis.
"""

import cv2
import numpy as np
import os


def create_test_video(output_path="videos/test_pole_vault.mp4", duration_sec=5, fps=30):
    """
    Create a synthetic test video with a simple stick figure animation.
    
    Args:
        output_path: Path to save the video
        duration_sec: Duration of the video in seconds
        fps: Frames per second
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Video parameters
    width, height = 640, 480
    total_frames = duration_sec * fps
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Creating synthetic test video: {output_path}")
    print(f"Duration: {duration_sec}s, FPS: {fps}, Total frames: {total_frames}")
    
    for frame_num in range(total_frames):
        # Create a blank white frame
        frame = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # Calculate animation progress (0 to 1)
        progress = frame_num / total_frames
        
        # Simulate a jumping motion (simplified pole vault motion)
        # Start low, jump high, come back down
        jump_height = np.sin(progress * np.pi)
        
        # Calculate positions for stick figure
        base_y = height - 100  # Ground level
        jump_offset = int(jump_height * 150)  # Maximum jump height
        
        # Center of figure
        center_x = int(width * (0.3 + progress * 0.4))  # Move from left to right
        center_y = base_y - jump_offset
        
        # Draw stick figure
        # Head
        cv2.circle(frame, (center_x, center_y - 40), 15, (0, 0, 0), 2)
        
        # Body
        cv2.line(frame, (center_x, center_y - 25), (center_x, center_y + 30), (0, 0, 0), 2)
        
        # Arms - vary angle based on progress
        arm_angle = progress * 180  # Rotate arms
        arm_length = 30
        left_arm_x = center_x - int(arm_length * np.cos(np.radians(arm_angle)))
        left_arm_y = center_y - int(arm_length * np.sin(np.radians(arm_angle)))
        right_arm_x = center_x + int(arm_length * np.cos(np.radians(arm_angle)))
        right_arm_y = center_y + int(arm_length * np.sin(np.radians(arm_angle)))
        
        cv2.line(frame, (center_x, center_y), (left_arm_x, left_arm_y), (0, 0, 0), 2)
        cv2.line(frame, (center_x, center_y), (right_arm_x, right_arm_y), (0, 0, 0), 2)
        
        # Legs - vary angle based on jump phase
        leg_angle = jump_height * 45  # Bend legs during jump
        leg_length = 35
        left_leg_x = center_x - int(leg_length * np.sin(np.radians(leg_angle)))
        left_leg_y = center_y + 30 + int(leg_length * np.cos(np.radians(leg_angle)))
        right_leg_x = center_x + int(leg_length * np.sin(np.radians(leg_angle)))
        right_leg_y = center_y + 30 + int(leg_length * np.cos(np.radians(leg_angle)))
        
        cv2.line(frame, (center_x, center_y + 30), (left_leg_x, left_leg_y), (0, 0, 0), 2)
        cv2.line(frame, (center_x, center_y + 30), (right_leg_x, right_leg_y), (0, 0, 0), 2)
        
        # Draw ground line
        cv2.line(frame, (0, base_y + 20), (width, base_y + 20), (100, 100, 100), 2)
        
        # Add frame number text
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(frame, f"Time: {frame_num/fps:.2f}s", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(frame, "TEST POLE VAULT VIDEO", (width//2 - 150, height - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:
            print(f"  Generated {frame_num + 1}/{total_frames} frames ({(frame_num+1)/total_frames*100:.1f}%)")
    
    out.release()
    print(f"✓ Video created successfully: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path


if __name__ == "__main__":
    # Create a test video
    video_path = create_test_video()
    print(f"\nTest video ready for analysis: {video_path}")
