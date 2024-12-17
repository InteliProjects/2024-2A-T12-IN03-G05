import pandas as pd

def createDFbyUEN(originalData: pd.DataFrame, model: str) -> pd.DataFrame:
    print('inicio do createDFbyUEN')
    print(f'Quantidade de linhas no inicio de tudo: {originalData.shape[0]}')
    df_analise = originalData.drop(['Desconto R$', 'Desc %'], axis=1)
    
    df_analise_model = df_analise[df_analise['UEN'] == model]
    
    columns_to_convert = [
        'VL Tabela', 'Vl Bruto', 'Vl Liquido Final', 'IPCA BR', 'IPCA ES',
        'Taxa Ac. TRI % PIB', 'PMC - Número-índice (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice (2022=100) (Número-índice)/ BR',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'
    ]
    print(f'Quantidade de linhas antes do primeiro dropNA no createDF{df_analise_model.shape[0]}')
    for col in columns_to_convert:
        df_analise_model[col] = pd.to_numeric(df_analise_model[col], errors='coerce')
        df_analise_model.dropna(inplace=True)
    print(f'Quantidade de linhas antes do groupby Data, cliente, setor e veiculo: {df_analise_model.shape[0]}')

    df_analise_corr_agg = df_analise_model.groupby(
        [pd.Grouper(key='Data', freq='ME')]
    ).agg({
        'VL Tabela': 'sum',
        'Vl Bruto': 'sum',
        'Vl Liquido Final': 'sum',
        'Cliente': 'nunique',                 # Quantidade de clientes diferentes
        'Veiculo': 'nunique',                 # Quantidade de veículos diferentes
        'Origem': 'nunique',                     # Quantidade de UENs diferentes
        'Setor': 'nunique',                   # Quantidade de setores diferentes
        'IPCA BR': 'mean',
        'IPCA ES': 'mean',
        'Taxa Ac. TRI % PIB': 'mean',
        'PMC - Número-índice (2022=100) (Número-índice)/ ES': 'mean',
        'PMC - Número-índice (2022=100) (Número-índice)/ BR': 'mean',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES': 'mean',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR': 'mean',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES': 'mean',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR': 'mean'
    }).reset_index()

    df_analise_corr_agg.rename(columns={
        'Cliente': 'Clientes',
        'Veiculo': 'Veiculos',
        'UEN': 'UENs',
        'Setor': 'Setores'
    }, inplace=True)
    
    print(f'Quantidade de antes do segundo groupby {df_analise_corr_agg.shape[0]}')
    # df_analise_corr_agg = df_analise_corr_agg.groupby(pd.Grouper(key='Data', freq='M')).agg({
    #     'VL Tabela': 'sum',
    #     'Vl Bruto': 'sum',
    #     'Vl Liquido Final': 'sum',
    #     'IPCA BR': 'mean',
    #     'IPCA ES': 'mean',
    #     'Taxa Ac. TRI % PIB': 'mean',
    #     'PMC - Número-índice (2022=100) (Número-índice)/ ES': 'mean',
    #     'PMC - Número-índice (2022=100) (Número-índice)/ BR': 'mean',
    #     'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES': 'mean',
    #     'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR': 'mean',
    #     'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES': 'mean',
    #     'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR': 'mean'
    # }).reset_index()
    print(f'Quantidade de linhas depois de criar o df {df_analise_corr_agg.shape[0]}')
    if not isinstance(df_analise_corr_agg['Data'].iloc[0], pd.Timestamp):
        df_analise_corr_agg['Data'] = df_analise_corr_agg['Data'].dt.to_timestamp()
    df_analise_corr_agg.set_index('Data', inplace=True)

    return df_analise_corr_agg


def createDFbyOrigem(originalData: pd.DataFrame, model: str) -> pd.DataFrame:
    df = originalData
    df['AnoMes'] = df['Data'].dt.to_period('M')
    df_analise_origem = df.groupby(['AnoMes', 'Origem']).agg({
    'VL Tabela': 'sum',
    'Vl Bruto': 'sum',
    'Vl Liquido Final': 'sum',
    'Cliente': 'nunique',                 # Quantidade de clientes diferentes
    'Veiculo': 'nunique',                 # Quantidade de veículos diferentes
    'UEN': 'nunique',                     # Quantidade de UENs diferentes
    'Setor': 'nunique',                   # Quantidade de setores diferentes
    'IPCA BR': 'mean',
    'IPCA ES': 'mean',
    'Taxa Ac. TRI % PIB': 'mean',
    'PMC - Número-índice (2022=100) (Número-índice)/ ES': 'mean',
    'PMC - Número-índice (2022=100) (Número-índice)/ BR': 'mean',
    'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES': 'mean',
    'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR': 'mean',
    'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES': 'mean',
    'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR': 'mean',
}).reset_index()

    # Adicionar a contagem de contratos (ocorrências) para cada Origem
    df_analise_origem['Contratos'] = df.groupby(['AnoMes', 'Origem'])['Origem'].transform('count')

    # Renomear as colunas para deixar os nomes mais claros e evitar conflito de nome
    df_analise_origem.rename(columns={
        'Cliente': 'Clientes',
        'Veiculo': 'Veiculos',
        'UEN': 'UENs',
        'Setor': 'Setores'
    }, inplace=True)

    columns_to_convert = [
        'VL Tabela', 'Vl Bruto', 'Vl Liquido Final', 'IPCA BR', 'IPCA ES',
        'Taxa Ac. TRI % PIB', 'PMC - Número-índice (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice (2022=100) (Número-índice)/ BR',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'
    ]
    
    for col in columns_to_convert:
        df_analise_origem[col] = pd.to_numeric(df_analise_origem[col], errors='coerce')
        df_analise_origem.dropna(inplace=True)

    DFtoModel = df_analise_origem[df_analise_origem['Origem'] == model].reset_index(drop=True)
    if not isinstance(DFtoModel['AnoMes'].iloc[0], pd.Timestamp):
        DFtoModel['AnoMes'] = DFtoModel['AnoMes'].dt.to_timestamp()
    DFtoModel.set_index('AnoMes', inplace=True)
    DFtoModel.drop(columns=['Origem'], inplace=True)



    return DFtoModel
def createDfByGeral(originalData: pd.DataFrame, model: str)-> pd.DataFrame:
    print('inicio do createDfByGeral')
    df = originalData
    DFtoModel = df.groupby(['Data']).agg({
    'VL Tabela': 'sum',
    'Vl Bruto': 'sum',
    'Vl Liquido Final': 'sum',
    'Cliente': 'nunique',                 # Quantidade de clientes diferentes
    'Veiculo': 'nunique',                 # Quantidade de veículos diferentes
    'UEN': 'nunique',                     # Quantidade de UENs diferentes
    'Setor': 'nunique',                   
    'Origem': 'nunique',                  
    'IPCA BR': 'mean',
    'IPCA ES': 'mean',
    'Taxa Ac. TRI % PIB': 'mean',
    'PMC - Número-índice (2022=100) (Número-índice)/ ES': 'mean',
    'PMC - Número-índice (2022=100) (Número-índice)/ BR': 'mean',
    'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES': 'mean',
    'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR': 'mean',
    'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES': 'mean',
    'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR': 'mean',
    }).reset_index()
    # Renomear as colunas para deixar os nomes mais claros e evitar conflito de nome
    DFtoModel.rename(columns={
        'Cliente': 'Clientes',
        'Veiculo': 'Veiculos',
        'UEN': 'UENs',
        'Setor': 'Setores'
    }, inplace=True)
    columns_to_convert = [
        'VL Tabela', 'Vl Bruto', 'Vl Liquido Final', 'IPCA BR', 'IPCA ES',
        'Taxa Ac. TRI % PIB', 'PMC - Número-índice (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice (2022=100) (Número-índice)/ BR',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'
    ]
    
    for col in columns_to_convert:
        DFtoModel[col] = pd.to_numeric(DFtoModel[col], errors='coerce')
        DFtoModel.dropna(inplace=True)
    print('Finalizei o createDfByGeral')
    return DFtoModel