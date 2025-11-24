"""
Unit tests for the Flask web application
"""

import unittest
import os
import tempfile
import json
import shutil
from app import app


class TestFlaskApp(unittest.TestCase):
    """Test the Flask web application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Create temporary directories for testing
        self.test_upload_dir = tempfile.mkdtemp()
        self.test_output_dir = tempfile.mkdtemp()
        self.app.config['UPLOAD_FOLDER'] = self.test_upload_dir
        self.app.config['OUTPUT_FOLDER'] = self.test_output_dir
    
    def tearDown(self):
        """Clean up test directories"""
        if os.path.exists(self.test_upload_dir):
            shutil.rmtree(self.test_upload_dir)
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
    
    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI_PVSim', response.data)
        self.assertIn(b'Pole Vault Video Analysis', response.data)
    
    def test_upload_without_file(self):
        """Test upload endpoint without file"""
        response = self.client.post('/upload', data={})
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_results_page_not_found(self):
        """Test results page with non-existent analysis ID"""
        response = self.client.get('/results/nonexistent-id')
        self.assertEqual(response.status_code, 302)  # Redirect to home
    
    def test_api_analyze_without_file(self):
        """Test API endpoint without file"""
        response = self.client.post('/api/analyze', data={})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_allowed_file_function(self):
        """Test allowed file function"""
        from app import allowed_file
        self.assertTrue(allowed_file('test.mp4'))
        self.assertTrue(allowed_file('test.avi'))
        self.assertTrue(allowed_file('test.mov'))
        self.assertFalse(allowed_file('test.txt'))
        self.assertFalse(allowed_file('test'))


if __name__ == '__main__':
    unittest.main()
