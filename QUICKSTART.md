# Quick Start Guide

## Installation (1 minute)

```bash
# Clone the repository
git clone https://github.com/sandiegoi-PV/AI_PVSim.git
cd AI_PVSim

# Install dependencies
pip install -r requirements.txt
```

## Web Application (Recommended)

### Start the Web Server
```bash
python app.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Using the Web Interface

1. **Upload Your Video**
   - Click "Choose Video File"
   - Select your pole vault video (MP4, AVI, MOV, etc.)
   - Enter athlete parameters (mass, height)
   - Click "Analyze Video"

2. **View Results**
   - Watch the side-by-side comparison video (original vs. pose detection)
   - Review detected phases and timing
   - See energy analysis for each phase
   - Get performance comparison to Olympic athletes
   - Read personalized training recommendations

3. **Analyze Another Video**
   - Click "Analyze Another Video" to upload a new video

The web interface provides:
- 🎥 Side-by-side video comparison
- 📊 Interactive results dashboard
- 🏃 Real-time pose detection visualization
- 📈 Performance metrics and recommendations
- 💾 Downloadable analysis reports

## Command Line Interface

### Try the Example (30 seconds)

Run the example with synthetic data:
```bash
python example.py
```

This will demonstrate the full system with generated data showing:
- Phase detection
- Energy calculations
- Performance comparison to Olympic athletes
- Training recommendations

## Analyze Your Video (2 minutes)

### Step 1: Prepare your video
- Record a pole vault from the side view
- Ensure the athlete is clearly visible
- Higher frame rate = better accuracy

### Step 2: Run the analysis
```bash
python pv_sim.py path/to/your/video.mp4
```

### Step 3: With athlete details
```bash
python pv_sim.py your_video.mp4 --mass 75 --height 1.85
```

### Step 4: Save results to file
```bash
python pv_sim.py your_video.mp4 --mass 75 --output analysis.txt
```

## Understanding the Output

### Phase Summary
```
Detected Pole Vault Phases:
1. RUN
   Frames: 0 - 90
   Duration: 3.00 seconds
...
```

### Energy Analysis
```
Energy Analysis by Phase:
RUN:
  Duration: 3.00s
  Kinetic Energy:
    Initial: 0.00 J
    Final:   2200.00 J
    Max:     2300.00 J
  Potential Energy:
    Initial: 400.00 J
    Final:   500.00 J
    Max:     520.00 J
  Total Energy:
    Initial: 400.00 J
    Final:   2700.00 J
    Max:     2820.00 J
  Energy Generated: 2300.00 J
```

### Performance Comparison
```
Comparison to Armand "Mondo" Duplantis:
Overall Score: 87.5/100

Phase-by-Phase Comparison:
  RUN:
    Your Energy: 2300.0 J
    Reference Energy: 2500.0 J
    Performance Ratio: 92.0%
    Performance Level: Good

  RECOMMENDATIONS FOR IMPROVEMENT:
  1. RUN: Energy generation is 8.0% below optimal
     → Focus on building running speed and acceleration.
```

## Tips for Best Results

### Video Quality
- ✅ 1080p or higher resolution
- ✅ 30 fps or higher frame rate
- ✅ Side view of the vault
- ✅ Good lighting
- ✅ Minimal background clutter

### Camera Position
- ✅ Perpendicular to the runway
- ✅ Capture full vault from run to landing
- ✅ Keep athlete in frame throughout

### Calibration
If results seem off, adjust the pixel-to-meter ratio:
```bash
python pv_sim.py video.mp4 --pixel-ratio 0.02
```

## Common Issues

### "No pose landmarks detected"
- Check if athlete is clearly visible
- Improve lighting
- Try a different camera angle

### "No phases detected"
- Video might be too short
- Ensure full vault is captured
- Try adjusting thresholds (see DEVELOPMENT.md)

### Energy values seem incorrect
- Verify athlete mass parameter
- Adjust pixel-to-meter ratio
- Check video frame rate

## Next Steps

1. **Read the full README.md** for detailed documentation
2. **Check DEVELOPMENT.md** to understand the architecture
3. **Run tests** to verify installation: `python -m unittest tests.test_pv_analyzer -v`
4. **Customize parameters** for your specific use case
5. **Compare multiple videos** to track progress over time

## Getting Help

- 📖 See README.md for detailed documentation
- 🔧 See DEVELOPMENT.md for technical details
- 🐛 Report issues on GitHub
- 💡 Suggest features via pull requests

## Example Workflow

```bash
# 1. Test installation
python example.py

# 2. Analyze your first video
python pv_sim.py athlete_vault1.mp4 --mass 70 --output results1.txt

# 3. Analyze after training
python pv_sim.py athlete_vault2.mp4 --mass 70 --output results2.txt

# 4. Compare results
diff results1.txt results2.txt
```

## Pro Tips

1. **Record multiple vaults** and analyze the best one
2. **Save all results** to track progress over time
3. **Focus on one phase at a time** when training
4. **Compare to your personal best** not just Olympic athletes
5. **Use slow-motion video** for better pose estimation

---

**Ready to optimize your pole vault? Start with `python example.py`!**
