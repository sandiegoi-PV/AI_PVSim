# AI_PVSim - Pole Vault Video Analysis System

An AI-powered system for analyzing pole vault videos, detecting phases of the vault, calculating energy generated in each phase, and comparing athlete performance to Olympic-level vaulters like Mondo Duplantis.

## Features

- **Automated Phase Detection**: Detects the 7 phases of pole vaulting:
  1. Run
  2. Plant
  3. Take-off
  4. Swing-up
  5. Extension/Inversion
  6. Push-off
  7. Pike

- **Velocity Tracking**: Records and reports athlete velocity during each phase:
  - Initial, final, max, and average velocity values
  - Velocity analysis per phase to identify speed patterns
  
- **Equipment Tracking**: Records pole length used by the athlete

- **Energy Analysis**: Calculates kinetic and potential energy for each phase:
  - Initial, final, max, and average energy values
  - Energy generated per phase
  - Total energy analysis

- **Performance Comparison**: Compares athlete performance to Olympic athletes:
  - Mondo Duplantis (World Record Holder)
  - Reference athletes with elite-level performance data
  - Phase-by-phase comparison with performance ratios
  - Overall performance score (0-100)

- **Training Recommendations**: Provides specific suggestions for improvement:
  - Identifies phases that need work
  - Suggests specific training exercises
  - Optimizes timing and technique

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

### Requirements

- Python 3.8+
- OpenCV (opencv-python)
- MediaPipe
- NumPy
- SciPy
- Matplotlib

## Usage

### Basic Usage

Analyze a pole vault video:

```bash
python pv_sim.py path/to/video.mp4
```

### Advanced Options

Specify athlete parameters:

```bash
python pv_sim.py video.mp4 --mass 75 --height 1.85 --pole-length 4.8
```

Save analysis to file:

```bash
python pv_sim.py video.mp4 --mass 70 --output analysis.txt
```

### Command Line Arguments

- `video`: Path to the pole vault video file (required)
- `--mass`: Athlete mass in kg (default: 70.0)
- `--height`: Athlete height in meters (default: 1.80)
- `--pole-length`: Pole length in meters (default: 4.5)
- `--pixel-ratio`: Pixel to meter conversion ratio (default: 0.01)
- `--output`: Output file for analysis results (default: print to console)

### Example Output

```
================================================================================
AI_PVSim - Pole Vault Video Analysis System
================================================================================
Video: athlete_vault.mp4
Athlete Mass: 75.0 kg
Athlete Height: 1.85 m
Pole Length: 4.5 m
================================================================================

[1/4] Processing video and extracting pose landmarks...
Processing video: athlete_vault.mp4
FPS: 30.0, Resolution: 1920x1080, Total frames: 180
✓ Extracted landmarks from 180 frames

[2/4] Detecting pole vault phases...
✓ Detected 7 phases

Detected Pole Vault Phases:
==================================================
1. RUN
   Frames: 0 - 90
   Duration: 3.00 seconds
   Velocity (pixels/sec):
     Initial: 0.00
     Max:     180.00
     Average: 150.00
     Final:   150.00

2. PLANT
   Frames: 91 - 100
   Duration: 0.30 seconds
   Velocity (pixels/sec):
     Initial: 150.00
     Max:     150.00
     Average: 125.00
     Final:   50.00

... (additional phases)

[3/4] Calculating energy for each phase...
✓ Energy calculations complete

Energy Analysis by Phase:
======================================================================

RUN:
  Duration: 3.00s
  Kinetic Energy:
    Initial: 0.00 J
    Final:   2200.00 J
    Max:     2300.00 J
  ... (additional energy data)

[4/4] Comparing performance to Olympic athletes...
✓ Performance comparison complete

================================================================================
PERFORMANCE COMPARISON TO OLYMPIC ATHLETES
================================================================================

Comparison to Armand "Mondo" Duplantis:
Overall Score: 87.5/100
--------------------------------------------------------------------------------

  RECOMMENDATIONS FOR IMPROVEMENT:
  ----------------------------------------------------------------------------
  1. SWING-UP: Energy generation is 12.5% below optimal
     → Work on core strength and hip drive. Practice swing drills on low bars.

... (additional recommendations)
```

## How It Works

### 1. Video Processing
- Uses MediaPipe Pose estimation to extract 3D body landmarks
- Tracks key body points: shoulders, hips, knees, ankles, etc.
- Processes video frame-by-frame for continuous motion analysis

### 2. Phase Detection
- Analyzes velocity, height, and body angles
- Uses motion characteristics to identify each phase
- Provides timing information for each phase

### 3. Energy Calculation
- **Kinetic Energy**: KE = 0.5 × m × v²
- **Potential Energy**: PE = m × g × h
- Tracks center of mass motion
- Calculates energy transfers between phases

### 4. Performance Comparison
- Compares to reference data from elite athletes
- Adjusts for mass differences between athletes
- Generates performance ratios and scores
- Identifies specific areas for improvement

## Technical Details

### Phase Detection Algorithm

The system uses a combination of:
- **Velocity Analysis**: Horizontal speed of center of mass
- **Height Tracking**: Vertical position above ground
- **Body Angle**: Orientation relative to horizontal
- **Temporal Smoothing**: Moving average filters for stability

### Energy Calculations

- **Mass**: User-specified athlete mass
- **Gravity**: 9.81 m/s²
- **Pixel-to-Meter Conversion**: Calibrated based on known reference
- **Center of Mass**: Calculated from key body landmarks

### Reference Athletes

The system includes performance data for:
- **Mondo Duplantis**: 6.24m world record holder
- **Reference profiles**: Based on Olympic-level performance

## Limitations

- Requires clear visibility of the athlete throughout the vault
- Camera position and angle affect accuracy
- Pixel-to-meter calibration may need adjustment per video
- Reference data is approximate based on published performance metrics

## Future Enhancements

- Automatic camera calibration
- 3D reconstruction for improved accuracy
- Real-time analysis from live video
- Machine learning for improved phase detection
- Mobile app for on-field analysis
- Comparison to personal best performances

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- MediaPipe by Google for pose estimation
- OpenCV for video processing
- Inspired by the incredible athletes pushing the boundaries of pole vaulting

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This system is designed as a training aid and should be used in conjunction with professional coaching. Always prioritize safety when practicing pole vaulting.
