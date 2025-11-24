# Web Application User Guide

## Overview

AI_PVSim now includes a modern web interface that makes it easy to analyze pole vault videos directly from your browser. Upload a video, enter athlete parameters, and get comprehensive analysis results including a side-by-side comparison video.

## Getting Started

### 1. Start the Server

```bash
cd AI_PVSim
python app.py
```

The server will start at `http://localhost:5000`

### 2. Open Your Browser

Navigate to:
```
http://localhost:5000
```

## Using the Web Interface

### Step 1: Upload Your Video

1. Click the **"Choose Video File"** button
2. Select your pole vault video from your computer
3. Supported formats: MP4, AVI, MOV, MKV, WEBM
4. Maximum file size: 100MB

### Step 2: Enter Athlete Parameters

Fill in the athlete details:

- **Mass (kg)**: Athlete's body mass in kilograms
  - Default: 70.0 kg
  - Range: 30-200 kg
  
- **Height (meters)**: Athlete's height in meters
  - Default: 1.80 m
  - Range: 1.0-2.5 m
  
- **Pixel to Meter Ratio**: Calibration factor for video scale
  - Default: 0.01
  - Adjust if energy values seem incorrect
  - Higher values = larger scale

### Step 3: Analyze Video

Click the **"Analyze Video"** button. The analysis will:

1. Upload your video to the server
2. Process each frame with AI pose detection
3. Detect all 7 phases of the pole vault
4. Calculate energy for each phase
5. Generate a side-by-side comparison video
6. Compare performance to Olympic athletes

**Note**: Processing may take several minutes depending on video length.

### Step 4: View Results

The results page shows:

#### 📊 Video Comparison
- Side-by-side view: Original video (left) vs. Pose detection (right)
- Pose skeleton overlaid on the athlete
- Key body points tracked throughout the vault

#### 🏃 Detected Phases
- All 7 phases of pole vaulting identified
- Start and end frames for each phase
- Duration in seconds for each phase
- Phases include: Run, Plant, Take-off, Swing-up, Extension, Push-off, Pike

#### ⚡ Energy Analysis
For each phase:
- Kinetic Energy (initial, final, max, average)
- Potential Energy (initial, final, max, average)
- Total Energy
- Energy Generated
- Duration

#### 🏆 Performance Comparison
- Comparison to Mondo Duplantis (World Record Holder)
- Comparison to reference Olympic athletes
- Overall performance score (0-100)
- Phase-by-phase performance ratios
- Performance level ratings (Excellent, Good, Fair, etc.)

#### 💡 Training Recommendations
- Specific suggestions for improvement
- Identified weak phases
- Recommended exercises
- Timing optimization tips

## Video Requirements

For best results, your video should have:

### ✅ Good Video Characteristics
- **Resolution**: 720p or higher (1080p recommended)
- **Frame Rate**: 30 fps or higher (60 fps ideal)
- **View Angle**: Side view perpendicular to runway
- **Lighting**: Good, even lighting
- **Background**: Minimal clutter, clear background
- **Visibility**: Athlete clearly visible throughout entire vault
- **Coverage**: Full vault from run to landing

### ❌ Avoid These Issues
- Low resolution (below 480p)
- Poor lighting or shadows
- Athlete obscured or partially out of frame
- Front or diagonal camera angles
- Fast pans or unstable camera
- Missing parts of the vault
- Multiple people in frame

## Calibration Tips

If energy values seem incorrect:

### Too High?
- Decrease pixel-to-meter ratio (try 0.005)
- Check athlete mass is correct

### Too Low?
- Increase pixel-to-meter ratio (try 0.02)
- Verify video shows full athlete height

### Finding the Right Ratio
1. Measure something known in the video (e.g., bar height)
2. Count pixels in video for that distance
3. Calculate: ratio = actual_meters / pixels

Example: Bar at 5m, measures 500 pixels → ratio = 5/500 = 0.01

## Analyzing Multiple Videos

To track progress over time:

1. Upload and analyze first video
2. Save or screenshot the results
3. Train and improve
4. Upload and analyze new video
5. Compare results to see improvement

## API Access

For programmatic access, use the REST API:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "video=@path/to/video.mp4" \
  -F "mass=75" \
  -F "height=1.85"
```

Returns JSON with:
- Analysis ID
- Detected phases
- Energy calculations
- Performance comparisons
- URL to comparison video

## Troubleshooting

### "No pose detected in video"
- Ensure athlete is clearly visible
- Check lighting quality
- Try a different camera angle
- Verify video format is supported

### "No pole vault phases detected"
- Video might be too short
- Ensure complete vault is captured
- Check that athlete is in frame throughout
- Verify side view angle

### "Error processing video"
- Check file size (max 100MB)
- Verify video format is supported
- Ensure sufficient disk space
- Check server logs for details

### Slow Processing
- Normal for longer videos
- Processing time depends on:
  - Video length
  - Video resolution
  - Computer hardware
- Typical: 1-5 minutes for 30-second video

### Video Player Not Working
- Ensure browser supports MP4 format
- Try a different browser (Chrome, Firefox recommended)
- Check that comparison video was generated
- Verify static/output folder permissions

## Privacy and Data

### File Storage
- Uploaded videos are processed temporarily
- Original uploads are deleted after processing
- Processed videos stored in `static/output/`
- Results saved as JSON in `static/output/`

### Data Retention
- Files remain on server until manually deleted
- Consider implementing automatic cleanup
- See DEPLOYMENT.md for cleanup strategies

### Security
- Videos are not shared or transmitted elsewhere
- Processing happens locally on your server
- No data sent to external services
- Change SECRET_KEY for production use

## Performance Tips

### For Faster Analysis
1. Use shorter video clips (focus on one vault)
2. Lower resolution videos process faster
3. Close other applications to free up resources
4. Use SSD storage for faster file I/O

### For Better Accuracy
1. Use higher resolution (1080p or 4K)
2. Higher frame rate (60 fps or more)
3. Ensure good lighting
4. Use stable tripod for camera
5. Position camera perpendicular to runway

## Next Steps

- Read DEPLOYMENT.md for production setup
- Check README.md for technical details
- See DEVELOPMENT.md for architecture info
- Try the command-line interface (pv_sim.py)
- Experiment with different athlete parameters

## Support

For help and questions:
- Check documentation in README.md
- Review troubleshooting section above
- Open issue on GitHub
- Check server logs for errors

---

**Ready to analyze? Start with `python app.py` and open your browser!**
