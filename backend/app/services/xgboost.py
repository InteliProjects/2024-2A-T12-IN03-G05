from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

def train_and_evaluate_xgboost(df, name):
    # Criando as colunas 'Ano', 'Mes', 'Semestre', 'Mes do Semestre'
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    df['Semestre'] = df['Mes'].apply(lambda x: 1 if x <= 6 else 2)
    df['Mes do Semestre'] = df['Mes'].apply(lambda x: x if x <= 6 else x - 6)

    # Mantendo a coluna 'Data' para uso futuro
    df_datas = df[['Data', 'Ano', 'Semestre', 'Mes do Semestre', 'Vl Liquido Final']]

    # Separar variáveis independentes (features) e dependente (target)
    X = df_datas[['Ano', 'Semestre', 'Mes do Semestre']]
    y = df_datas['Vl Liquido Final']

    # Dividir os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Treinar o modelo XGBoost
    model = xgb.XGBRegressor(n_estimators=1000, max_depth=7, eta=0.1, subsample=0.7, colsample_bytree=0.8, random_state=42)
    model.fit(X_train, y_train)
    print(f"Modelo treinado para {name}")
    
    # Fazer previsões no conjunto de teste
    y_pred = model.predict(X_test)
    
    # Usar as datas reais para associar com as previsões
    test_dates = df_datas.loc[X_test.index, 'Data']

    # Separando os últimos 12 meses
    last_12_months_dates = df_datas['Data'][-12:]
    last_12_months_values = df_datas['Vl Liquido Final'][-12:]
    
    last_12_months_dict = {date.strftime('%Y-%m'): float(round(value, 2)) for date, value in zip(last_12_months_dates, last_12_months_values)}

    # Previsões para os próximos 12 meses
    # Determinar a última data no conjunto de dados
    last_date = df_datas['Data'].max()

    # Gerar as próximas 12 datas mensais
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=12, freq='MS')

    # Criar features para as datas futuras
    future_df = pd.DataFrame({'Data': future_dates})
    future_df['Ano'] = future_df['Data'].dt.year
    future_df['Mes'] = future_df['Data'].dt.month
    future_df['Semestre'] = future_df['Mes'].apply(lambda x: 1 if x <= 6 else 2)
    future_df['Mes do Semestre'] = future_df['Mes'].apply(lambda x: x if x <= 6 else x - 6)
    
    future_X = future_df[['Ano', 'Semestre', 'Mes do Semestre']]

    # Fazer previsões para as datas futuras
    future_predictions = model.predict(future_X)

    future_forecast_dict = {date.strftime('%Y-%m'): float(round(prediction, 2)) for date, prediction in zip(future_dates, future_predictions)}

    print(f"Previsões feitas para {name}")

    # Calcular as métricas de avaliação
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    r2 = r2_score(y_test, y_pred)

    result_dict = {
        "metricas": {
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
            "mape": mape
        },
        "lastmonths": last_12_months_dict,
        "forecast": future_forecast_dict,
    }
    
    # Retorno do dicionário de previsões
    return result_dict
