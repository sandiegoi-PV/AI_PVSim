# AI_PVSim - Pole Vault Video Analysis System

This is an AI-powered pole vault video analysis system that provides accurate tracking of athlete movements and pole positions for performance analysis and comparison.

## Features

- **Accurate Pose Detection**: Uses MediaPipe's advanced pose estimation to track athlete body keypoints with high precision
- **Pole Tracking**: Detects and tracks pole position, length, and angle throughout the vault
- **Automatic Calibration**: Calibrates measurements using athlete's known height for accurate real-world measurements
- **Data Export**: Exports detailed frame-by-frame data in JSON format for comparison with other athletes
- **Video Annotation**: Generates annotated videos showing detected poses, pole position, and measurements
- **Performance Statistics**: Calculates key metrics like pole angles, athlete height, and movement patterns

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sandiegoi-PV/AI_PVSim.git
cd AI_PVSim
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze a pole vault video:

```bash
python example_usage.py your_video.mp4
```

### Advanced Usage

Generate annotated output video with custom athlete height:

```bash
python example_usage.py input_video.mp4 output_annotated.mp4 1.85
```

Parameters:
- `input_video.mp4`: Path to your pole vault video
- `output_annotated.mp4`: (Optional) Path where annotated video will be saved
- `1.85`: (Optional) Athlete's height in meters for calibration (default: 1.8m)

### Using the API

You can also use the VideoAnalyzer class directly in your Python code:

```python
from video_analyzer import VideoAnalyzer

# Initialize analyzer with athlete's height for calibration
analyzer = VideoAnalyzer(calibration_height_meters=1.85)

# Analyze video
frame_data = analyzer.analyze_video(
    video_path="pole_vault.mp4",
    output_video_path="annotated_output.mp4"
)

# Get statistics
stats = analyzer.get_statistics()
print(f"Average pole angle: {stats['avg_pole_angle']:.2f}°")

# Export data for comparison
analyzer.export_data("analysis_results.json")
```

## How It Works

### 1. Pose Detection
The system uses MediaPipe Pose with the highest complexity model (complexity=2) to accurately detect 33 body landmarks including:
- Head and facial features
- Upper body (shoulders, elbows, wrists)
- Torso (hips)
- Lower body (knees, ankles)

### 2. Automatic Calibration
The system calibrates pixel-to-meter ratio by:
- Measuring the athlete's pixel height from nose to ankles
- Comparing to the known athlete height provided
- This ensures accurate real-world measurements throughout the video

### 3. Pole Detection
Pole tracking uses:
- Edge detection (Canny edge detector)
- Hough Line Transform to detect straight lines
- Filtering for long lines at typical pole vault angles
- Selection of the most prominent line as the pole

### 4. Measurement Accuracy
To ensure accurate data:
- Smooth landmark tracking reduces jitter
- Calibration is performed on first clear detection
- All measurements are converted from pixels to real-world units (meters)
- Pole angles are calculated relative to horizontal

### 5. Data Export
The system exports comprehensive JSON data including:
- Frame-by-frame athlete keypoints
- Pole position and angle for each frame
- Calibration information
- Timestamp information for temporal analysis

## Output Data Format

The exported JSON file contains:

```json
{
  "calibration_height_meters": 1.8,
  "pixels_per_meter": 250.5,
  "total_frames": 300,
  "frames": [
    {
      "frame_number": 0,
      "timestamp": 0.0,
      "athlete_keypoints": {
        "NOSE": [640.5, 200.3, 0.99],
        "LEFT_SHOULDER": [600.2, 350.1, 0.95],
        ...
      },
      "pole_endpoints": [[500, 100], [520, 800]],
      "pole_length_pixels": 702.1,
      "athlete_height_pixels": 450.2,
      "pole_angle": 85.3
    },
    ...
  ]
}
```

## Comparison with Other Athletes

The JSON export enables detailed comparison between athletes:
- Compare pole angles at different phases of the vault
- Analyze body positioning and kinematics
- Measure timing differences
- Evaluate technical efficiency

## System Requirements

- **CPU**: Multi-core processor recommended for faster processing
- **RAM**: Minimum 4GB, 8GB+ recommended for high-resolution videos
- **Storage**: Space for video files and exported data
- **Python**: Version 3.8 or higher

## Dependencies

- **OpenCV**: Video processing and computer vision operations
- **MediaPipe**: Advanced pose estimation and landmark detection
- **NumPy**: Numerical computations and array operations
- **SciPy**: Scientific computing and interpolation
- **Matplotlib**: Data visualization (for future enhancements)

## Accuracy Considerations

For best results:
- Use high-resolution video (720p or higher)
- Ensure good lighting conditions
- Position camera perpendicular to the vault plane
- Provide accurate athlete height for calibration
- Use consistent camera position throughout recording
- Avoid excessive camera movement

## Future Enhancements

Potential improvements:
- 3D pose estimation for depth analysis
- Multi-camera support for 3D reconstruction
- Real-time analysis capability
- Advanced biomechanical calculations
- Automated performance scoring
- Integration with training databases

## Contributing

This project is a passion project exploring AI-assisted pole vault analysis. Contributions and suggestions are welcome!

## License

This project is provided as-is for educational and analysis purposes.

## Contact

For questions or suggestions, please open an issue on GitHub.
