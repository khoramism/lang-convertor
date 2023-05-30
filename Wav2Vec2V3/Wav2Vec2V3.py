import numpy as np
import pandas as pd
import librosa
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from datasets import load_dataset, load_metric
import os
import time
import codecs
from distutils.sysconfig import get_python_lib

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Wav2Vec2V3:
    def __init__(self):

        #path = os.getcwd()
        path = get_python_lib() + '/Wav2Vec2LargeHoma5V3/model'
        model_name_or_path = path
        self.processor = Wav2Vec2Processor.from_pretrained(model_name_or_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name_or_path).to(device)


    def useModel(self, path):
        speech_array, sampling_rate = torchaudio.load(path)
        speech_array = speech_array.squeeze().numpy()
        batch = librosa.resample(np.asarray(speech_array), orig_sr=sampling_rate,
                                        target_sr=self.processor.feature_extractor.sampling_rate)
        features = self.processor(
            batch,
            sampling_rate=self.processor.feature_extractor.sampling_rate,
            return_tensors="pt",
            padding=True
        )

        input_values = features.input_values.to(device)
        attention_mask = features.attention_mask.to(device)

        with torch.no_grad():
            logits = self.model(input_values, attention_mask=attention_mask).logits

        pred_ids = torch.argmax(logits, dim=-1)

        res = self.processor.batch_decode(pred_ids)
        res = res[0].replace('u200c', ' ')
       
        return res
