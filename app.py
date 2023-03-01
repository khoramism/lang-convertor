from fastapi import FastAPI, File, UploadFile
from datetime import datetime
from conversions import convert
app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File()):
    '''
    Just for wav formats 
    '''
    #print(type(file))
    try:
        file_name = f"{datetime.now().timestamp()}.wav"
        with open(file_name, 'wb+') as f:
            f.write(file)
        convert.delay('./{file_name}')
        ok = True
    except:
        ok = False
    
    return {"file_size": len(file), 'ok' : ok}

"""
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    #print
    contents = await file.read()
    return {"content": contents}
"""