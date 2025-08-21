# Speech Recognition API

A FastAPI-based multilingual speech recognition service that supports Persian (Farsi), Spanish, and English audio transcription using Wav2Vec2 models.

## Features

- **Multilingual Support**: Supports Persian (fa), Spanish (sp), and English (en) speech recognition
- **RESTful API**: Simple HTTP endpoints for audio file uploads with proper validation
- **Docker Support**: Containerized deployment with Docker Compose
- **CORS Enabled**: Cross-origin resource sharing configured for web applications
- **Multiple Model Support**: Uses different specialized models for each language
- **Production Ready**: Proper error handling, logging, health checks, and file management
- **Automatic Model Loading**: Models are loaded once at startup for optimal performance
- **File Safety**: Temporary file handling with automatic cleanup and size limits

## Supported Languages

- **Persian (fa)**: Custom Wav2Vec2V3 model (`m3hrdadfi/wav2vec2-large-xlsr-persian-v3`)
- **Spanish (sp)**: Voyager1/asr-wav2vec2-commonvoice-es
- **English (en)**: speechbrain/asr-wav2vec2-librispeech

## Requirements

- Python 3.10+
- WAV audio files only
- Maximum file size: 50MB
- Sufficient disk space for model downloads (~2-3GB)
- At least 8GB RAM recommended for all models

## Installation & Usage

### Quick Start with Docker (Recommended)

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd speech-recognition-api
```

1. **Build and run with Docker Compose:**

```bash
docker-compose up --build
```

1. The API will be available at:
   - Main API: `http://localhost:8010`
   - Interactive docs: `http://localhost:8010/docs`
   - Health check: `http://localhost:8010/health`

## API Documentation

### Endpoints

#### 1. Health Check

**GET** `/health`

Check if the API is running and models are loaded.

**Response:**

```json
{
  "status": "healthy",
  "models_loaded": true
}
```

#### 2. Transcribe Audio (Recommended)

**POST** `/transcribe`

Transcribe an audio file to text with full validation and proper response format.

**Parameters:**

- `lang` (query parameter): Language code (`fa`, `sp`, or `en`)
- `file` (form-data): Audio file in WAV format (max 50MB)

**Example Request:**

```bash
curl -X POST "http://localhost:8010/transcribe?lang=en" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample.wav"
```

**Response:**

```json
{
  "file_size": 1234567,
  "success": true,
  "text": "Hello, this is the transcribed text from your audio file.",
  "language": "en",
  "processing_time": 2.45
}
```

**Error Response:**

```json
{
  "detail": "Only WAV files are supported"
}
```



## Usage Examples

### cURL Examples

```bash
# English transcription
curl -X POST "http://localhost:8010/transcribe?lang=en" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@english_audio.wav"

# Persian transcription
curl -X POST "http://localhost:8010/transcribe?lang=fa" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@persian_audio.wav"

# Spanish transcription
curl -X POST "http://localhost:8010/transcribe?lang=sp" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@spanish_audio.wav"

# Health check
curl http://localhost:8010/health
```

# API settings

CORS_ORIGINS=http://localhost:3000,http://localhost:8080
API_TITLE=Speech Recognition API
API_VERSION=1.0.0

## Performance Considerations

### Model Loading

- Models are loaded once at startup to avoid per-request loading overhead
- Initialization may take 1-2 minutes depending on system specifications
- Models are cached in memory for fast inference

### File Processing

- Temporary files are created and automatically cleaned up
- Processing time varies by audio length and language
- Typical processing time: 0.1-0.5x real-time audio duration

### Resource Requirements

| Component | Minimum      | Recommended                       |
| --------- | ------------ | --------------------------------- |
| RAM       | 4GB          | 8GB+                              |
| Storage   | 5GB          | 10GB+                             |
| CPU       | 2 cores      | 4+ cores                          |
| GPU       | Not required | Recommended for faster processing |

