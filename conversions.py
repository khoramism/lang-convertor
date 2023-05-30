#from celery import Celery
from speechbrain.pretrained import EncoderASR
#from huggingsound import SpeechRecognitionModel
from Wav2Vec2V3 import Wav2Vec2V3
def convert_it(lang:str):
    if lang == 'fa':
        asr_model = Wav2Vec2V3()
        return asr_model

    elif lang == 'sp':
        asr_model = EncoderASR.from_hparams("Voyager1/asr-wav2vec2-commonvoice-es")
        return asr_model
        
    elif lang == 'en':
        # EnciderASR can't be used in async/await way
        asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-librispeech")
        return asr_model
    




broker_url = 'amqp://guest:guest@localhost:5672/myvhost'

"""app = Celery('conversions',broker=broker_url)
app.conf.update(
    #task_serializer='json',
    #accept_content=['json'],  # Ignore other content
    #result_serializer='json',
    timezone='Asia/Tehran',
    enable_utc=True,
)

@app.task
def convert(file_name: str):
    text = asr_model.transcribe_file(file_name)
    return text
"""

