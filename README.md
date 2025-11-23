# AI_PVSim - Pole Vault Video Analysis

This is a sandbox to see how an AI would develop my passion project.

## Overview

AI_PVSim is a video analysis system designed to analyze pole vault videos using computer vision and pose detection. The system can download videos from online sources, extract movement data, and detect inconsistencies in the tracking.

## Features

- **Video Download**: Automatically download pole vault videos from YouTube and other sources
- **Pose Detection**: Extract detailed body pose data from each frame using MediaPipe
- **Data Recording**: Save comprehensive frame-by-frame analysis data
- **Inconsistency Detection**: Automatically identify:
  - Missing frames or tracking gaps
  - Low visibility/confidence issues
  - Sudden movements that might indicate tracking problems
  - Other data quality issues

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sandiegoi-PV/AI_PVSim.git
cd AI_PVSim
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Testing with Online Examples

Run the test script to analyze online pole vault videos:

```bash
python test_online_examples.py
```

This will:
1. Download pole vault videos from YouTube
2. Analyze each video for pose data
3. Check for inconsistencies
4. Generate reports in the `output/` directory

### Analyzing Custom Videos

You can also analyze your own videos:

```python
from video_analyzer import PoleVaultAnalyzer

analyzer = PoleVaultAnalyzer()

# Analyze a local video
results = analyzer.analyze_video("path/to/your/video.mp4")
inconsistencies = analyzer.check_inconsistencies(results)
analyzer.save_results(results, inconsistencies)

analyzer.cleanup()
```

### Downloading Videos

To download a video from a URL:

```python
from video_analyzer import PoleVaultAnalyzer

analyzer = PoleVaultAnalyzer()
video_path = analyzer.download_video("https://www.youtube.com/watch?v=example")
```

## Output

The system generates three types of output files in the `output/` directory:

1. **CSV Data File**: Frame-by-frame pose landmark data with timestamps
2. **JSON Results File**: Complete analysis results including metadata
3. **Inconsistencies Report**: Human-readable summary of any issues found

## Requirements

- Python 3.8+
- OpenCV
- MediaPipe
- NumPy
- Pandas
- yt-dlp (for downloading videos)
- Matplotlib

See `requirements.txt` for specific versions.

## Project Structure

```
AI_PVSim/
├── video_analyzer.py          # Main video analysis module
├── test_online_examples.py    # Test script for online videos
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── videos/                    # Downloaded videos (created at runtime)
└── output/                    # Analysis results (created at runtime)
```

## How It Works

1. **Video Input**: Videos can be downloaded from URLs or loaded from local files
2. **Frame Processing**: Each frame is processed using MediaPipe Pose to detect body landmarks
3. **Data Extraction**: Key points (shoulders, hips, knees, etc.) are extracted with 3D positions
4. **Analysis**: The system calculates metrics like center of mass and tracks movement over time
5. **Quality Checks**: Multiple checks identify data quality issues and inconsistencies
6. **Output**: Results are saved in multiple formats for further analysis

## Contributing

This is a personal passion project. Feel free to fork and adapt for your own use.

## License

This project is open source and available under the MIT License.
