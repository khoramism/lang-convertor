from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from conversions import convert_it
import asyncio


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware



origins = [
    "http://localhost",
    "http://localhost:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-librispeech", savedir="pretrained_models/asr-wav2vec2-librispeech")
FILE_STORAGE = "../../files"
@app.post("/files/")
async def create_file(lang: str, file: bytes = File()):
    '''
    Just for wav formats 
    '''
    #print(type(file))
    
    try:
        file_name = f"{FILE_STORAGE}/{datetime.now().timestamp()}.wav"
        with open(file_name, 'wb+') as f:
            f.write(file)
        asr_model = convert_it(lang)
        text = asr_model.transcribe_file(file_name)
        ok = True
    
    except:
        ok = False
        text = 'failed'
        import traceback; traceback.print_exc();
    #if ok:
    #    text = convert.delay(f'./{file_name}')
    return {"file_size": len(file), 'ok' : ok, 'text':text}

"""
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    #print
    contents = await file.read()
    return {"content": contents}
"""