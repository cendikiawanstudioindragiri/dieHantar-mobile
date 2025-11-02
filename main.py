
from fastapi import FastAPI, UploadFile, File
from typing import Optional
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend dieHantar berhasil berjalan!"}

@app.post("/upload-image/")
async def create_upload_file(file: UploadFile):
    """
    Endpoint untuk menerima unggahan file gambar.
    Saat ini, endpoint ini hanya akan mengembalikan nama file dan tipe kontennya.
    Langkah selanjutnya adalah mengintegrasikannya dengan Firebase Storage.
    """
    return {"filename": file.filename, "content_type": file.content_type}

# Baris ini memungkinkan kita menjalankan server langsung untuk pengujian
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
