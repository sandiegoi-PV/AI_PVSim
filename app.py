#!/usr/bin/env python3
"""
AI_PVSim - Web Application
Flask web server for pole vault video analysis
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from pv_analyzer import VideoProcessor, PhaseDetector, EnergyCalculator, PerformanceComparator
import json
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Configure upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_side_by_side_video(original_path: str, landmarks_list: list, 
                               video_info: dict, output_path: str) -> bool:
    """
    Create a side-by-side comparison video with original and annotated versions
    
    Args:
        original_path: Path to original video
        landmarks_list: List of pose landmarks
        video_info: Video metadata
        output_path: Path to save the output video
        
    Returns:
        True if successful, False otherwise
    """
    try:
        cap = cv2.VideoCapture(original_path)
        if not cap.isOpened():
            return False
        
        # Get video properties
        fps = video_info['fps']
        width = video_info['width']
        height = video_info['height']
        
        # Create video writer for side-by-side output (double width)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width * 2, height))
        
        frame_idx = 0
        while cap.isOpened() and frame_idx < len(landmarks_list):
            ret, frame = cap.read()
            if not ret:
                break
            
            # Create annotated version
            annotated_frame = frame.copy()
            landmarks = landmarks_list[frame_idx]
            
            if landmarks is not None:
                # Draw pose landmarks on annotated frame
                for name, lm in landmarks.items():
                    if lm['visibility'] > 0.5:
                        x, y = int(lm['x']), int(lm['y'])
                        cv2.circle(annotated_frame, (x, y), 5, (0, 255, 0), -1)
                
                # Draw skeleton connections
                connections = [
                    ('left_shoulder', 'right_shoulder'),
                    ('left_shoulder', 'left_elbow'),
                    ('left_elbow', 'left_wrist'),
                    ('right_shoulder', 'right_elbow'),
                    ('right_elbow', 'right_wrist'),
                    ('left_shoulder', 'left_hip'),
                    ('right_shoulder', 'right_hip'),
                    ('left_hip', 'right_hip'),
                    ('left_hip', 'left_knee'),
                    ('left_knee', 'left_ankle'),
                    ('right_hip', 'right_knee'),
                    ('right_knee', 'right_ankle'),
                ]
                
                for start, end in connections:
                    if start in landmarks and end in landmarks:
                        if landmarks[start]['visibility'] > 0.5 and landmarks[end]['visibility'] > 0.5:
                            pt1 = (int(landmarks[start]['x']), int(landmarks[start]['y']))
                            pt2 = (int(landmarks[end]['x']), int(landmarks[end]['y']))
                            cv2.line(annotated_frame, pt1, pt2, (0, 255, 255), 2)
            
            # Add labels
            cv2.putText(frame, 'Original', (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(annotated_frame, 'With Pose Detection', (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Combine frames side by side
            combined = np.hstack((frame, annotated_frame))
            out.write(combined)
            
            frame_idx += 1
        
        cap.release()
        out.release()
        return True
        
    except Exception as e:
        print(f"Error creating side-by-side video: {e}")
        return False


@app.route('/')
def index():
    """Home page with upload form"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle video upload and processing"""
    if 'video' not in request.files:
        flash('No video file provided', 'error')
        return redirect(url_for('index'))
    
    file = request.files['video']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash(f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
        return redirect(url_for('index'))
    
    try:
        # Get athlete parameters
        mass = float(request.form.get('mass', 70.0))
        height = float(request.form.get('height', 1.80))
        pixel_ratio = float(request.form.get('pixel_ratio', 0.01))
        
        # Validate parameters
        if mass <= 0 or mass > 200:
            flash('Invalid mass. Must be between 0 and 200 kg.', 'error')
            return redirect(url_for('index'))
        
        # Generate unique ID for this analysis
        analysis_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{analysis_id}.{file_ext}")
        file.save(upload_path)
        
        # Process video
        video_processor = VideoProcessor()
        frames, landmarks_list, video_info = video_processor.process_video(upload_path)
        video_processor.close()
        
        if not landmarks_list or all(lm is None for lm in landmarks_list):
            flash('No pose detected in video. Ensure the athlete is clearly visible.', 'error')
            os.remove(upload_path)
            return redirect(url_for('index'))
        
        # Detect phases
        phase_detector = PhaseDetector()
        phases = phase_detector.detect_phases(landmarks_list, video_info)
        
        if not phases:
            flash('No pole vault phases detected in video.', 'error')
            os.remove(upload_path)
            return redirect(url_for('index'))
        
        # Calculate energy
        energy_calculator = EnergyCalculator(
            athlete_mass=mass,
            pixel_to_meter_ratio=pixel_ratio
        )
        phase_energies = energy_calculator.calculate_phase_energies(
            landmarks_list, phases, video_info
        )
        
        # Compare performance
        comparator = PerformanceComparator()
        comparisons = comparator.compare_performance(phase_energies, mass)
        
        # Create side-by-side comparison video
        output_video_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{analysis_id}_comparison.mp4")
        video_created = create_side_by_side_video(
            upload_path, landmarks_list, video_info, output_video_path
        )
        
        # Prepare results data
        results = {
            'analysis_id': analysis_id,
            'video_info': video_info,
            'athlete_params': {
                'mass': mass,
                'height': height
            },
            'phases': phases,
            'energies': phase_energies,
            'comparisons': comparisons,
            'video_available': video_created,
            'video_filename': f"{analysis_id}_comparison.mp4" if video_created else None,
            'phase_summary': phase_detector.get_phase_summary(),
            'energy_summary': energy_calculator.get_energy_summary(phase_energies),
            'comparison_summary': comparator.get_comparison_summary()
        }
        
        # Save results to JSON file
        results_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{analysis_id}_results.json")
        with open(results_path, 'w') as f:
            # Convert numpy types to native Python types for JSON serialization
            def convert_to_json_serializable(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return obj
            
            json.dump(results, f, default=convert_to_json_serializable, indent=2)
        
        # Clean up uploaded file after processing
        try:
            os.remove(upload_path)
        except OSError:
            pass
        
        return redirect(url_for('results', analysis_id=analysis_id))
        
    except Exception as e:
        flash(f'Error processing video: {str(e)}', 'error')
        # Clean up files on error
        try:
            if 'upload_path' in locals() and os.path.exists(upload_path):
                os.remove(upload_path)
        except OSError:
            pass
        return redirect(url_for('index'))


@app.route('/results/<analysis_id>')
def results(analysis_id):
    """Display analysis results"""
    results_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{analysis_id}_results.json")
    
    if not os.path.exists(results_path):
        flash('Analysis results not found', 'error')
        return redirect(url_for('index'))
    
    try:
        with open(results_path, 'r') as f:
            results_data = json.load(f)
        
        return render_template('results.html', results=results_data)
    
    except Exception as e:
        flash(f'Error loading results: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for video analysis (JSON response)"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    try:
        # Get parameters
        mass = float(request.form.get('mass', 70.0))
        height = float(request.form.get('height', 1.80))
        pixel_ratio = float(request.form.get('pixel_ratio', 0.01))
        
        # Generate unique ID
        analysis_id = str(uuid.uuid4())
        
        # Save and process video
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{analysis_id}.{file_ext}")
        file.save(upload_path)
        
        # Process video
        video_processor = VideoProcessor()
        frames, landmarks_list, video_info = video_processor.process_video(upload_path)
        video_processor.close()
        
        # Detect phases
        phase_detector = PhaseDetector()
        phases = phase_detector.detect_phases(landmarks_list, video_info)
        
        # Calculate energy
        energy_calculator = EnergyCalculator(athlete_mass=mass, pixel_to_meter_ratio=pixel_ratio)
        phase_energies = energy_calculator.calculate_phase_energies(landmarks_list, phases, video_info)
        
        # Compare performance
        comparator = PerformanceComparator()
        comparisons = comparator.compare_performance(phase_energies, mass)
        
        # Create comparison video
        output_video_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{analysis_id}_comparison.mp4")
        video_created = create_side_by_side_video(upload_path, landmarks_list, video_info, output_video_path)
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        # Return results
        return jsonify({
            'analysis_id': analysis_id,
            'phases': phases,
            'energies': phase_energies,
            'comparisons': comparisons,
            'video_url': url_for('static', filename=f'output/{analysis_id}_comparison.mp4') if video_created else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
