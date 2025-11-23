"""
Alternative test using a simpler approach - create a video with more realistic human figure.
"""

import cv2
import numpy as np
import os


def draw_realistic_person(frame, center_x, center_y, scale=1.0, angle=0):
    """
    Draw a more realistic person figure that MediaPipe can detect.
    
    Args:
        frame: The frame to draw on
        center_x, center_y: Center position
        scale: Scale factor
        angle: Rotation angle for pose variation
    """
    # Define body proportions (more realistic)
    head_radius = int(20 * scale)
    torso_height = int(60 * scale)
    torso_width = int(30 * scale)
    arm_length = int(40 * scale)
    leg_length = int(50 * scale)
    
    # Colors for different body parts (skin tone and clothes)
    skin_color = (200, 170, 150)  # BGR
    shirt_color = (50, 100, 200)
    pants_color = (80, 80, 150)
    
    # Head - draw as filled circle with face
    cv2.circle(frame, (center_x, center_y - torso_height - head_radius), 
               head_radius, skin_color, -1)
    cv2.circle(frame, (center_x, center_y - torso_height - head_radius), 
               head_radius, (0, 0, 0), 2)
    
    # Draw simple face features
    eye_offset = int(head_radius * 0.3)
    eye_y = center_y - torso_height - head_radius - int(head_radius * 0.2)
    cv2.circle(frame, (center_x - eye_offset, eye_y), 3, (0, 0, 0), -1)  # Left eye
    cv2.circle(frame, (center_x + eye_offset, eye_y), 3, (0, 0, 0), -1)  # Right eye
    
    # Torso - draw as filled rectangle/ellipse
    torso_top = center_y - torso_height
    cv2.ellipse(frame, (center_x, center_y - torso_height // 2), 
                (torso_width // 2, torso_height // 2), 0, 0, 360, shirt_color, -1)
    cv2.ellipse(frame, (center_x, center_y - torso_height // 2), 
                (torso_width // 2, torso_height // 2), 0, 0, 360, (0, 0, 0), 2)
    
    # Arms
    arm_angle_left = angle - 30
    arm_angle_right = angle + 30
    
    # Left arm (shoulder to elbow to wrist)
    shoulder_left = (center_x - torso_width // 2, torso_top + 10)
    elbow_left = (
        int(shoulder_left[0] - arm_length * 0.6 * np.cos(np.radians(arm_angle_left))),
        int(shoulder_left[1] + arm_length * 0.6 * np.sin(np.radians(arm_angle_left)))
    )
    wrist_left = (
        int(elbow_left[0] - arm_length * 0.4 * np.cos(np.radians(arm_angle_left + 20))),
        int(elbow_left[1] + arm_length * 0.4 * np.sin(np.radians(arm_angle_left + 20)))
    )
    cv2.line(frame, shoulder_left, elbow_left, skin_color, int(8 * scale))
    cv2.line(frame, elbow_left, wrist_left, skin_color, int(8 * scale))
    cv2.circle(frame, shoulder_left, int(6 * scale), skin_color, -1)
    cv2.circle(frame, elbow_left, int(5 * scale), skin_color, -1)
    cv2.circle(frame, wrist_left, int(5 * scale), skin_color, -1)
    
    # Right arm
    shoulder_right = (center_x + torso_width // 2, torso_top + 10)
    elbow_right = (
        int(shoulder_right[0] + arm_length * 0.6 * np.cos(np.radians(arm_angle_right))),
        int(shoulder_right[1] + arm_length * 0.6 * np.sin(np.radians(arm_angle_right)))
    )
    wrist_right = (
        int(elbow_right[0] + arm_length * 0.4 * np.cos(np.radians(arm_angle_right - 20))),
        int(elbow_right[1] + arm_length * 0.4 * np.sin(np.radians(arm_angle_right - 20)))
    )
    cv2.line(frame, shoulder_right, elbow_right, skin_color, int(8 * scale))
    cv2.line(frame, elbow_right, wrist_right, skin_color, int(8 * scale))
    cv2.circle(frame, shoulder_right, int(6 * scale), skin_color, -1)
    cv2.circle(frame, elbow_right, int(5 * scale), skin_color, -1)
    cv2.circle(frame, wrist_right, int(5 * scale), skin_color, -1)
    
    # Legs
    leg_angle_left = angle + 10
    leg_angle_right = angle - 10
    
    # Left leg (hip to knee to ankle)
    hip_left = (center_x - torso_width // 4, center_y)
    knee_left = (
        int(hip_left[0] + leg_length * 0.5 * np.sin(np.radians(leg_angle_left))),
        int(hip_left[1] + leg_length * 0.5)
    )
    ankle_left = (
        int(knee_left[0] + leg_length * 0.5 * np.sin(np.radians(leg_angle_left))),
        int(knee_left[1] + leg_length * 0.5)
    )
    cv2.line(frame, hip_left, knee_left, pants_color, int(10 * scale))
    cv2.line(frame, knee_left, ankle_left, pants_color, int(10 * scale))
    cv2.circle(frame, hip_left, int(7 * scale), pants_color, -1)
    cv2.circle(frame, knee_left, int(6 * scale), pants_color, -1)
    cv2.circle(frame, ankle_left, int(5 * scale), (0, 0, 0), -1)  # Shoes
    
    # Right leg
    hip_right = (center_x + torso_width // 4, center_y)
    knee_right = (
        int(hip_right[0] - leg_length * 0.5 * np.sin(np.radians(leg_angle_right))),
        int(hip_right[1] + leg_length * 0.5)
    )
    ankle_right = (
        int(knee_right[0] - leg_length * 0.5 * np.sin(np.radians(leg_angle_right))),
        int(knee_right[1] + leg_length * 0.5)
    )
    cv2.line(frame, hip_right, knee_right, pants_color, int(10 * scale))
    cv2.line(frame, knee_right, ankle_right, pants_color, int(10 * scale))
    cv2.circle(frame, hip_right, int(7 * scale), pants_color, -1)
    cv2.circle(frame, knee_right, int(6 * scale), pants_color, -1)
    cv2.circle(frame, ankle_right, int(5 * scale), (0, 0, 0), -1)  # Shoes


def create_realistic_test_video(output_path="videos/test_realistic.mp4", duration_sec=3, fps=30):
    """
    Create a test video with a more realistic human figure.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Video parameters
    width, height = 640, 480
    total_frames = duration_sec * fps
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Creating realistic test video: {output_path}")
    print(f"Duration: {duration_sec}s, FPS: {fps}, Total frames: {total_frames}")
    
    for frame_num in range(total_frames):
        # Create a frame with gradient background
        frame = np.ones((height, width, 3), dtype=np.uint8)
        # Sky gradient
        for y in range(height // 2):
            color_val = int(200 + (y / (height // 2)) * 55)
            frame[y, :] = [color_val, color_val - 20, color_val - 50]
        # Ground
        frame[height // 2:, :] = [100, 180, 100]  # Green ground
        
        # Draw ground line
        cv2.line(frame, (0, height // 2), (width, height // 2), (80, 140, 80), 3)
        
        # Calculate animation progress (0 to 1)
        progress = frame_num / total_frames
        
        # Simulate jumping motion
        jump_phase = np.sin(progress * np.pi * 2)  # Oscillate
        jump_height = int(abs(jump_phase) * 80)  # Jump up and down
        
        # Calculate position
        center_x = int(width * 0.5)  # Stay in center
        base_y = int(height * 0.7)
        center_y = base_y - jump_height
        
        # Vary arm angle with jump
        arm_angle = jump_phase * 45  # Arms move with jump
        
        # Draw the person
        draw_realistic_person(frame, center_x, center_y, scale=1.2, angle=arm_angle)
        
        # Add text overlay
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Time: {frame_num/fps:.2f}s", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, "POLE VAULT TEST", (width//2 - 100, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        out.write(frame)
        
        if (frame_num + 1) % 30 == 0:
            print(f"  Generated {frame_num + 1}/{total_frames} frames ({(frame_num+1)/total_frames*100:.1f}%)")
    
    out.release()
    print(f"✓ Video created successfully: {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path


if __name__ == "__main__":
    video_path = create_realistic_test_video()
    print(f"\nRealistic test video ready: {video_path}")
