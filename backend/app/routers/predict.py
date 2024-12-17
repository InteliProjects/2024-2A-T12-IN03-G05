from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from app.services.clean import clean
from app.services.createDF import createDFbyUEN, createDFbyOrigem,createDfByGeral
import pandas as pd
from app.services.sarimax import train_and_evaluate_sarimax
from app.services.xgboost import train_and_evaluate_xgboost
import io
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_csv(file_content: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(file_content))

@router.post("/process-data/")
async def process_data(
    data_file: UploadFile = File(...),
    pmc_file: UploadFile = File(...),
    model: str = Form(...),
    type_model: str = Form(...)
):
    logger.info(f"Received data_file: {data_file.filename}")
    logger.info(f"Received pmc_file: {pmc_file.filename}")
    logger.info(f"Received model: {model}")
    try:
        data_content = await data_file.read()
        pmc_content = await pmc_file.read()

        data = read_csv(data_content)
        pmc = read_csv(pmc_content)

        cleaned_data = clean(data, pmc)

        if model == 'Digital':
            model = 'DIGITAL'

        elif model == 'Vitória':
            model = 'VT - CONTATO - VITÓRIA'

        elif model == 'Cachoeiro':
            model = 'CH - CONTATO - CACHOEIRO'

        elif model == 'Colatina':
            model = 'CO - CONTATO - COLATINA'

        elif model == 'Linhares':
            model = 'LI - CONTATO - LINHARES'

        elif model == 'Mídia Programática':
            model = 'MP - MÍDIA PROGRAMÁTICA'

        elif model == 'Mercado Nacional':
            model = 'RN - MERCADO NACIONAL'
        elif model == 'Geral':
            model = 'Geral'

        modelsByUEN = ['Televisão', 'Rádio', 'DIGITAL']
        modelsByOrigem = ['CH - CONTATO - CACHOEIRO', 'CO - CONTATO - COLATINA', 'LI - CONTATO - LINHARES', 'MP - MÍDIA PROGRAMÁTICA', 'RN - MERCADO NACIONAL', 'VT - CONTATO - VITÓRIA']

        if model in modelsByUEN:
            result_df = createDFbyUEN(cleaned_data, model)
        elif model in modelsByOrigem:
            result_df = createDFbyOrigem(cleaned_data, model)
        elif model == 'Geral':
            result_df = createDfByGeral(cleaned_data,model)
        else:
            raise HTTPException(status_code=400, detail="Invalid model")



        if type_model == 'Sarimax':
            predict = train_and_evaluate_sarimax(result_df, model)
        else:
            predict = train_and_evaluate_xgboost(result_df, model)

        return predict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))