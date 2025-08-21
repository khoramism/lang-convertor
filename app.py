import os
import tempfile
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from conversions import ModelManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Speech Recognition API",
    description="Multilingual speech recognition service",
    version="1.0.0"
)

# CORS middleware with specific origins
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    # Add your frontend URLs here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Global model manager
model_manager = None

# Response models
class TranscriptionResponse(BaseModel):
    file_size: int
    success: bool
    text: str
    language: str
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    models_loaded: bool

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    global model_manager
    try:
        model_manager = ModelManager()
        logger.info("Models initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        models_loaded=model_manager is not None
    )

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    lang: str = Query(..., regex="^(fa|sp|en)$", description="Language code: fa, sp, or en"),
    file: UploadFile = File(..., description="Audio file in WAV format")
):
    """
    Transcribe audio file to text
    
    - **lang**: Language code (fa=Persian, sp=Spanish, en=English)
    - **file**: WAV audio file
    """
    start_time = datetime.now()
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only WAV files are supported")
    
    # Check file size (limit to 50MB)
    MAX_FILE_SIZE = 50 * 1024 * 1024
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 50MB)")
    
    # Reset file pointer
    await file.seek(0)
    
    # Process file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Get model and transcribe
            asr_model = model_manager.get_model(lang)
            text = asr_model.transcribe_file(temp_file_path)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return TranscriptionResponse(
                file_size=len(file_content),
                success=True,
                text=text,
                language=lang,
                processing_time=processing_time
            )
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                logger.warning(f"Could not delete temporary file: {temp_file_path}")
    
    except ValueError as e:
        logger.error(f"Model error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")

# Keep the old endpoint for backward compatibility
@app.post("/files/")
async def create_file_legacy(
    lang: str = Query(..., regex="^(fa|sp|en)$"),
    file: bytes = File(...)
):
    """Legacy endpoint - use /transcribe instead"""
    # Create UploadFile-like object from bytes
    from io import BytesIO
    from fastapi import UploadFile
    
    fake_file = UploadFile(
        filename="audio.wav",
        file=BytesIO(file),
        headers={"content-type": "audio/wav"}
    )
    
    response = await transcribe_audio(lang=lang, file=fake_file)
    
    # Return in old format
    return {
        "file_size": response.file_size,
        "ok": response.success,
        "text": response.text
    }
