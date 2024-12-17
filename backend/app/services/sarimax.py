from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from app.models.parameters import radio, televisao, digital, cachoeiro, colatina, linhares, midia_programatica, mercado_nacional, vitoria

def train_and_evaluate_sarimax(df, name):
    print(f"Treinando modelo para {name}...")

    if name == 'Rádio':
        model = radio

    elif name == 'Televisão':
        model = televisao

    elif name == 'DIGITAL':
        model = digital
    
    elif name == 'CH - CONTATO - CACHOEIRO':
        model = cachoeiro
    
    elif name == 'CO - CONTATO - COLATINA':
        model = colatina
    
    elif name == 'LI - CONTATO - LINHARES':
        model = linhares

    elif name == 'MP - MÍDIA PROGRAMÁTICA':
        model = midia_programatica

    elif name == 'Mercado Nacional':
        model = mercado_nacional
    
    elif name == 'VT - CONTATO - VITÓRIA':
        model = vitoria
    else:
        raise ValueError(f"Modelo desconhecido: {name}")

    colunas_to_drop = model['columnsToDrop']
    order_hiperparametros = model['ordem_hiperparametros']
    hiperparametros = model['hiperparametros']
    df = df.dropna()

    # Converta todas as colunas para tipos numéricos, se necessário
    # df = df.apply(pd.to_numeric, errors='coerce')

    # Selecione as features (todas as colunas menos 'Vl Liquido Final', 'VL Tabela', 'Vl Bruto')
    X = df.drop(columns=colunas_to_drop)
    y = df['Vl Liquido Final']
    
    # to csv para comparar as dfs
    
    X.to_csv('test.csv')

    # Divida os dados em treinamento e teste
    train_size = int(len(y) * 0.8)
    train_X, test_X = X[:train_size], X[train_size:]
    train_y, test_y = y[:train_size], y[train_size:]


    model_best = SARIMAX(train_y, exog=train_X, order=order_hiperparametros, 
                         seasonal_order=hiperparametros)
    model_best_fit = model_best.fit(disp=False)

    # Previsão no conjunto de teste com o melhor modelo
    forecast_test_best = model_best_fit.forecast(steps=len(test_y), exog=test_X)

    # Previsão futura de 12 meses
    future_steps = 12
    future_dates = pd.date_range(start=test_y.index[-1] + pd.DateOffset(months=1), periods=future_steps, freq='M')
    future_X = X.iloc[-future_steps:]  # Assumindo que você tenha dados futuros para as features

    # # Verifique e trate valores ausentes e infinitos em future_X
    # future_X = future_X.replace([np.inf, -np.inf], np.nan).fillna(0)

    forecast_future_best = model_best_fit.forecast(steps=future_steps, exog=future_X)

    # Combine previsões de teste e futuras
    all_forecast_best = np.concatenate([forecast_test_best, forecast_future_best])
    all_dates_best = test_y.index.append(future_dates)

    # Calcule as métricas de avaliação
    mae = mean_absolute_error(test_y, forecast_test_best)
    rmse = np.sqrt(mean_squared_error(test_y, forecast_test_best))
    mape = np.mean(np.abs((test_y - forecast_test_best) / test_y)) * 100
    r2 = r2_score(test_y, forecast_test_best)

    # Exiba as métricas
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    print(f"R-squared (R²): {r2:.2f}")

    # Plotando os valores reais, as previsões e a previsão futura
    plt.figure(figsize=(12, 6))
    plt.plot(test_y.index, test_y, label='Valores Reais')
    plt.plot(all_dates_best, all_forecast_best, label='Previsões', linestyle='--', color='orange')
    plt.axvline(x=test_y.index[-1], color='red', linestyle='--', label='Início da Previsão Futura')
    plt.xlabel('Data')
    plt.ylabel('Vl Liquido Final')
    plt.title(f'Valores Reais vs Previsões com Previsão Futura de 12 Meses - {name}')
    plt.legend()
    # graph_file_path = f"data/results/graphs/grafico_result.png"
    # plt.savefig(graph_file_path)
    
        # Crie um dicionário com as previsões futuras
        # Crie um dicionário com os últimos 12 meses analisados
    last_13_months_dict = {date.strftime('%Y-%m'): round(actual, 2) for date, actual in zip(test_y.index[-13:], test_y[-13:])}

    # Crie um dicionário com as previsões para os próximos 12 meses
    future_forecast_dict = {date.strftime('%Y-%m'): round(forecast, 2) for date, forecast in zip(future_dates, forecast_future_best)}

    # Combine os dois dicionários, sem sobrescrever as chaves
    combined_forecast_dict = last_13_months_dict.copy()  # Copia os últimos 13 meses
    for date, forecast in future_forecast_dict.items():
        if date in combined_forecast_dict:
            print(f"Aviso: O mês {date} já está presente no dicionário, ele será ignorado.")
        else:
            combined_forecast_dict[date] = forecast

    # Verifique o tamanho do dicionário combinado
    print(f"Tamanho do dicionário combinado: {len(combined_forecast_dict)}")

    # Exibir previsões para os próximos 12 meses
    print("Previsões para os próximos 12 meses:")
    for date, forecast in future_forecast_dict.items():
        print(f"{date}: {forecast:.2f}")

    # Crie o dicionário final com a estrutura desejada
    print("Criando o dicionário final...")
    result_dict = {
        "metricas": {
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
            "mape": mape
        },
        "lastmonths": last_13_months_dict,
        "forecast": future_forecast_dict,
    }
    print("Dicionário final criado com sucesso!")

    future_forecast_dict = pd.DataFrame(future_forecast_dict.items(), columns=['Data', 'Previsão'])
    print('pós dataframe')
    future_forecast_dict.to_excel('app/data/forecast.xlsx', index=False)
    print('pós excel')
    return result_dict