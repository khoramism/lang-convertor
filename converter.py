from speechbrain.pretrained import EncoderASR

asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-librispeech", savedir="pretrained_models/asr-wav2vec2-librispeech")
def convert(file_name:str):
    asr_model.transcribe_file(file_name)
