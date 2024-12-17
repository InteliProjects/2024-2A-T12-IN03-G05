from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from app.routers import predict

app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost:3000",  # Adicione outras origens conforme necessário
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/download-forecast")
async def download_forecast():
    file_path = 'app/data/forecast.xlsx'
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="forecast.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        return {"error": "File not found"}

app.include_router(predict.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)