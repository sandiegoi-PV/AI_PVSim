# Development Guide

## Project Structure

```
AI_PVSim/
├── pv_analyzer/                 # Main package
│   ├── __init__.py             # Package initialization
│   ├── video_processor.py      # Video processing and pose estimation
│   ├── phase_detector.py       # Phase detection logic
│   ├── energy_calculator.py    # Energy calculations
│   └── performance_comparator.py # Performance comparison
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_pv_analyzer.py     # Test suite
├── pv_sim.py                   # Main application CLI
├── example.py                  # Example with synthetic data
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore patterns
└── README.md                   # Documentation

```

## Architecture

### 1. VideoProcessor
- Uses MediaPipe Pose for pose estimation
- Extracts 17 key body landmarks per frame
- Returns frames, landmarks, and video metadata

### 2. PhaseDetector
- Analyzes motion characteristics (velocity, height, angles)
- Identifies 7 pole vault phases:
  1. Run - High velocity, low height
  2. Plant - Velocity decreasing, height starting to rise
  3. Take-off - Rapid height increase
  4. Swing-up - Body rotating, height increasing
  5. Extension/Inversion - Body inverted at peak
  6. Push-off - Maximum height, body extending
  7. Pike - Descending with body folded

### 3. EnergyCalculator
- Calculates kinetic energy: KE = 0.5 × m × v²
- Calculates potential energy: PE = m × g × h
- Tracks center of mass motion
- Provides energy statistics per phase

### 4. PerformanceComparator
- Compares to reference athletes
- Adjusts for mass differences
- Generates performance scores
- Provides training recommendations

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
python -m unittest tests.test_pv_analyzer -v
```

3. Run example:
```bash
python example.py
```

## Adding New Features

### Adding a New Reference Athlete

Edit `pv_analyzer/performance_comparator.py`:

```python
REFERENCE_ATHLETES = {
    'new_athlete': {
        'name': 'Athlete Name',
        'best_height': 6.00,  # meters
        'mass': 75,  # kg
        'phase_energies': {
            'run': { ... },
            # ... other phases
        }
    }
}
```

### Improving Phase Detection

The phase detection algorithm is in `pv_analyzer/phase_detector.py`. 

Key methods to modify:
- `_identify_phase()`: Main phase identification logic
- `_calculate_velocities()`: Velocity calculation
- `_calculate_heights()`: Height tracking
- `_calculate_body_angles()`: Body orientation

### Customizing Energy Calculations

Energy calculations are in `pv_analyzer/energy_calculator.py`.

Parameters to adjust:
- `GRAVITY`: Gravitational constant (default: 9.81 m/s²)
- `pixel_to_meter_ratio`: Pixel-to-meter conversion

## Testing

### Unit Tests

Run all tests:
```bash
python -m unittest discover tests -v
```

Run specific test:
```bash
python -m unittest tests.test_pv_analyzer.TestPhaseDetector -v
```

### Integration Testing

Use the example script with synthetic data:
```bash
python example.py
```

Test with real video:
```bash
python pv_sim.py path/to/video.mp4 --mass 70 --output results.txt
```

## Performance Optimization

### Video Processing
- Process every Nth frame for faster analysis
- Use lower resolution videos
- Reduce MediaPipe model complexity

### Phase Detection
- Adjust window size for smoothing
- Fine-tune threshold values
- Use parallel processing for batch analysis

## Troubleshooting

### No pose detected
- Ensure athlete is clearly visible
- Check lighting and camera angle
- Try different MediaPipe confidence thresholds

### Incorrect phase detection
- Adjust thresholds in `_identify_phase()`
- Increase smoothing window size
- Calibrate pixel-to-meter ratio

### Energy calculations seem off
- Verify athlete mass parameter
- Adjust pixel-to-meter conversion ratio
- Check video frame rate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## Future Enhancements

- [ ] Automatic camera calibration
- [ ] Real-time video processing
- [ ] Machine learning for phase detection
- [ ] 3D reconstruction
- [ ] Mobile app
- [ ] Multi-athlete comparison
- [ ] Historical performance tracking
- [ ] Video annotations and overlays
