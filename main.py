from fastapi import FastAPI, status, File, UploadFile, HTTPException
import hashlib
import db
import uvicorn
from datetime import datetime
import os

app = FastAPI()

engine = db.create_db()


@app.post("/protect", status_code=status.HTTP_201_CREATED)
def protect(name, file: UploadFile = File(...)):

    file_location = f"{file.filename}"
    # save file
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # get file check sum
    with open(file_location, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    file_check_sum = file_hash.hexdigest()
    os.remove(file_location)

    dt = datetime.now()
    ts = datetime.timestamp(dt)

    try:
        db.create_row(
            engine,
            db.ChekSum,
            {
                'author_name': f'{name}',
                'file_check_sum': f'{file_check_sum}'
            }
        )
        return {
            'ts': ts,
            'author_name': name,
            'file_check_sum': file_check_sum
        }
    except Exception as e:
        raise HTTPException(
            status_code=501,
            detail="This file has already been saved."
        )



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, debug=True)
