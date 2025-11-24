# Web Application Deployment Guide

This document provides instructions for deploying the AI_PVSim web application.

## Local Development

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### Configuration

The application can be configured using environment variables:

- `SECRET_KEY`: Flask secret key for session management (default: 'dev-secret-key-change-in-production')
- `MAX_CONTENT_LENGTH`: Maximum upload file size in bytes (default: 100MB)

## Production Deployment

### Using Gunicorn (Recommended)

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Options:
- `-w 4`: Number of worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000
- `--timeout 300`: Increase timeout for long video processing

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "300", "app:app"]
```

Build and run:
```bash
docker build -t ai-pvsim .
docker run -p 5000:5000 ai-pvsim
```

### Environment Variables for Production

```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"
```

## Nginx Reverse Proxy

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for video processing
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

## Storage Considerations

The application creates temporary files in:
- `uploads/`: Uploaded video files (deleted after processing)
- `static/output/`: Processed videos and analysis results

### Cleanup Strategy

For production, implement a cleanup strategy to remove old files:

```bash
# Clean up files older than 24 hours
find uploads/ -type f -mtime +1 -delete
find static/output/ -type f -mtime +1 -delete
```

Add to crontab:
```bash
0 2 * * * find /path/to/ai_pvsim/uploads/ -type f -mtime +1 -delete
0 2 * * * find /path/to/ai_pvsim/static/output/ -type f -mtime +1 -delete
```

## Performance Optimization

### Hardware Requirements

- **Minimum**: 2 CPU cores, 4GB RAM
- **Recommended**: 4+ CPU cores, 8GB+ RAM
- **Video Processing**: More CPU cores = faster processing

### Scaling

For high traffic:
1. Use multiple Gunicorn workers
2. Deploy behind a load balancer
3. Use a task queue (e.g., Celery) for video processing
4. Store videos in cloud storage (S3, etc.)

## Security Considerations

1. **Change the SECRET_KEY** in production
2. **Implement rate limiting** to prevent abuse
3. **Validate file uploads** (already implemented)
4. **Use HTTPS** in production
5. **Implement user authentication** if needed
6. **Set up file size limits** appropriately

## Monitoring

Monitor these metrics:
- Upload success/failure rate
- Video processing time
- Disk space usage
- Memory usage
- CPU usage

## Troubleshooting

### Video Processing Fails

- Check disk space
- Verify MediaPipe installation
- Check video format compatibility
- Increase timeout values

### Out of Memory

- Reduce Gunicorn workers
- Limit concurrent uploads
- Implement queueing system

### Slow Performance

- Increase CPU cores
- Use faster storage (SSD)
- Optimize video processing parameters
- Implement caching for results

## API Usage

The application provides a REST API endpoint:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -F "video=@path/to/video.mp4" \
  -F "mass=75" \
  -F "height=1.85"
```

Response:
```json
{
  "analysis_id": "uuid",
  "phases": [...],
  "energies": {...},
  "comparisons": {...},
  "video_url": "/static/output/uuid_comparison.mp4"
}
```

## Support

For issues and questions:
- Check logs: `tail -f /var/log/gunicorn.log`
- Review Flask app logs
- Check disk space: `df -h`
- Monitor resources: `htop`
