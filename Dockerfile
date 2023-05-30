FROM python:3.10-alpine 


COPY . /app

WORKDIR /app 


RUN pip install -r requirements.txt

RUN apt install wget uvicorn git 

RUN git lfs install 

RUN git clone https://huggingface.co/m3hrdadfi/wav2vec2-large-xlsr-persian-v3

RUN mv huggingface.co/m3hrdadfi/wav2vec2-large-xlsr-persian-v3 model

RUN mv model wav2vec2V3/




CMD ['uvicorn','app:app','--host=0.0.0.0','--port=8010']
