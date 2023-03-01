from celery import Celery
from speechbrain.pretrained import EncoderASR

asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-librispeech", savedir="pretrained_models/asr-wav2vec2-librispeech")

broker_url = 'amqp://guest:guest@localhost:5672/myvhost'

celery_app = Celery('conversions', backend='redis://localhost',broker=broker_url)
celery_app.conf.update(
    #task_serializer='json',
    #accept_content=['json'],  # Ignore other content
    #result_serializer='json',
    timezone='Asia/Tehran',
    enable_utc=True,
)
@celery_app.convert
def convert(file_name: str):
    text = asr_model.transcribe_file(file_name)
    return text


