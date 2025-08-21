import logging
from typing import Dict, Any
from speechbrain.pretrained import EncoderASR

# Import your custom model
try:
    from Wav2Vec2V3 import Wav2Vec2V3
except ImportError:
    logging.warning("Wav2Vec2V3 not found, Persian support will be unavailable")
    Wav2Vec2V3 = None

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages ASR models for different languages"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.supported_languages = {
            'fa': 'Persian',
            'sp': 'Spanish', 
            'en': 'English'
        }
        self._load_models()
    
    def _load_models(self):
        """Load all models at startup"""
        logger.info("Loading ASR models...")
        
        try:
            # Load Persian model
            if Wav2Vec2V3:
                logger.info("Loading Persian model...")
                self.models['fa'] = Wav2Vec2V3()
                logger.info("Persian model loaded successfully")
            else:
                logger.warning("Persian model not available")
        
        except Exception as e:
            logger.error(f"Failed to load Persian model: {e}")
        
        try:
            # Load Spanish model
            logger.info("Loading Spanish model...")
            self.models['sp'] = EncoderASR.from_hparams("Voyager1/asr-wav2vec2-commonvoice-es")
            logger.info("Spanish model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Spanish model: {e}")
        
        try:
            # Load English model
            logger.info("Loading English model...")
            self.models['en'] = EncoderASR.from_hparams(
                source="speechbrain/asr-wav2vec2-librispeech"
            )
            logger.info("English model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load English model: {e}")
        
        logger.info(f"Loaded {len(self.models)} models")
    
    def get_model(self, lang: str):
        """Get model for specified language"""
        if lang not in self.supported_languages:
            raise ValueError(f"Unsupported language: {lang}. Supported: {list(self.supported_languages.keys())}")
        
        if lang not in self.models:
            raise ValueError(f"Model for language '{lang}' is not available")
        
        return self.models[lang]
    
    def is_language_supported(self, lang: str) -> bool:
        """Check if language is supported and model is loaded"""
        return lang in self.models

# For backward compatibility
def convert_it(lang: str):
    """Legacy function - use ModelManager instead"""
    logger.warning("convert_it is deprecated, use ModelManager instead")
    manager = ModelManager()
    return manager.get_model(lang)
