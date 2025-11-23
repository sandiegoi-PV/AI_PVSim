# Video Analysis Technical Details

## System Architecture

The AI PVSim video analysis system consists of three main components:

### 1. Pose Detection (MediaPipe)
- **Model**: MediaPipe Pose with complexity level 2 (highest accuracy)
- **Landmarks**: Tracks 33 body keypoints including:
  - Face (nose, eyes, ears, mouth)
  - Upper body (shoulders, elbows, wrists)
  - Torso (hips)
  - Lower body (knees, ankles, heels, toes)
- **Confidence**: Minimum detection confidence of 0.5
- **Smoothing**: Enabled landmark smoothing to reduce jitter

### 2. Pole Detection (OpenCV)
- **Method**: Computer vision pipeline using:
  1. Grayscale conversion
  2. Gaussian blur (5x5 kernel)
  3. Canny edge detection (thresholds: 50-150)
  4. Hough Line Transform for straight line detection
- **Filtering**: Selects lines that are:
  - Longer than 100 pixels
  - At angles > 30° from horizontal
  - The longest matching line is selected as the pole

### 3. Calibration System
- **Method**: Pixel-to-meter ratio calculation
- **Reference**: Uses athlete's known height (nose to ankle distance)
- **Process**: 
  1. Measures pixel height from nose to ankle landmarks
  2. Divides by known athlete height in meters
  3. Applies ratio to all subsequent measurements

## Accuracy Considerations

### For Best Results:
1. **Video Quality**: Use 720p or higher resolution
2. **Lighting**: Ensure good, even lighting
3. **Camera Position**: 
   - Position camera perpendicular to vault plane
   - Keep camera stable (avoid handheld recording)
   - Maintain consistent distance
4. **Athlete Height**: Provide accurate height for calibration
5. **Frame Rate**: 30fps or higher recommended

### Measurement Accuracy:
- **Pose landmarks**: Typically accurate to within 2-3% of body dimensions
- **Pole detection**: Accuracy depends on pole visibility and contrast
- **Calibration**: Accuracy depends on athlete standing upright in frame

## Data Output Format

### JSON Structure:
```json
{
  "calibration_height_meters": 1.8,
  "pixels_per_meter": 420.5,
  "total_frames": 300,
  "frames": [
    {
      "frame_number": 0,
      "timestamp": 0.0,
      "athlete_keypoints": {
        "NOSE": [x, y, visibility],
        "LEFT_SHOULDER": [x, y, visibility],
        ...
      },
      "pole_endpoints": [[x1, y1], [x2, y2]],
      "pole_length_pixels": 702.1,
      "athlete_height_pixels": 450.2,
      "pole_angle": 85.3
    }
  ]
}
```

### Keypoint Format:
Each keypoint contains:
- **x, y**: Pixel coordinates in the frame
- **visibility**: Confidence score (0.0 to 1.0)

### Using Data for Comparison:
1. **Temporal Analysis**: Compare movements across frames
2. **Cross-Athlete**: Compare same frame numbers or timestamps
3. **Performance Metrics**: 
   - Pole plant angle at specific phases
   - Body position during takeoff
   - Extension angles during vault
   - Landing positions

## Performance

### Processing Speed:
- **MediaPipe Pose**: ~30-60 FPS on modern CPU
- **Pole Detection**: ~60-120 FPS on modern CPU
- **Combined**: Typically processes at 20-40 FPS

### Memory Usage:
- **Base**: ~200-300 MB for models
- **Video Processing**: Depends on video resolution
- **Data Storage**: ~1-2 KB per frame in JSON

## Limitations

1. **Occlusion**: If body parts are hidden, landmarks may be inaccurate
2. **Multiple People**: System tracks the most prominent person in frame
3. **Pole Visibility**: Dark poles on dark backgrounds may not be detected
4. **2D Analysis**: Currently only analyzes 2D movements (not depth)
5. **Camera Movement**: Excessive camera movement affects accuracy

## Future Enhancements

Possible improvements:
1. **Multi-camera 3D tracking**: Use multiple views for depth analysis
2. **Advanced biomechanics**: Calculate velocities, accelerations, forces
3. **Automatic phase detection**: Identify approach, plant, swing, etc.
4. **Performance scoring**: AI-based technique evaluation
5. **Real-time processing**: Live video analysis during training
6. **Trajectory prediction**: Predict vault trajectory early in motion
