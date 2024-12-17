import pandas as pd
import re

def clean(data: pd.DataFrame, pmc: pd.DataFrame) -> pd.DataFrame:
    print('inicio do clean')
    data = data.drop(columns=['Mês/ano', 'CONCATENAR', '% Ating. Meta'])
    data = data.rename(columns={'Ano': 'ano'})
    data.at[36839, 'Setor'] = 'COMERC.P/ AUTOMOTIVO'
    data.at[45332, 'Setor'] = 'LOJA VAREJISTA/ATAC'
    data = data.sort_values(by=['ano', 'Mês'])
    data = data.fillna(method='ffill')

    cols_to_string = ['Desc %', 'Vl Liquido Final', 'Vl Bruto', 'Desconto R$', 'VL Tabela', 'IPCA ES', 'IPCA BR', 'Taxa Ac. TRI % PIB']
    data[cols_to_string] = data[cols_to_string].astype(str)
    print('convertido para string')

    data['Desc %'] = data['Desc %'].str.replace('-', '')
    
    for col in ['Vl Liquido Final', 'Vl Bruto', 'Desconto R$', 'VL Tabela']:
        data[col] = data[col].str.replace('.', '').str.replace(',', '.')

    data['IPCA ES'] = data['IPCA ES'].str.replace(',', '.')
    data['IPCA BR'] = data['IPCA BR'].str.replace(',', '.')
    data['Taxa Ac. TRI % PIB'] = data['Taxa Ac. TRI % PIB'].str.replace(',', '.')
    data['Desc %'] = data['Desc %'].str.replace('%', '')

    print('antes do to_numeric')
    # # Convertendo colunas para numérico
    cols_to_numeric = ['Vl Liquido Final', 'Vl Bruto', 'Desconto R$', 'VL Tabela', 'IPCA ES', 'IPCA BR', 'Taxa Ac. TRI % PIB', 'Desc %']
    data[cols_to_numeric] = data[cols_to_numeric].apply(pd.to_numeric, errors='coerce')

    data['Desc %'] = data['Desc %'] / 100
    data['ano'] = pd.to_numeric(data['ano'])
    data['Mês'] = pd.to_numeric(data['Mês'])
    data['Dia'] = 1

    # Criando a coluna Data
    data_to_time = data[['ano', 'Mês', 'Dia']].rename(columns={'ano': 'year', 'Mês': 'month', 'Dia': 'day'})
    data['Data'] = pd.to_datetime(data_to_time)
    data.drop(columns=['ano', 'Mês', 'Dia'], inplace=True)
    data.sort_values(by=['Data'])
    print('criou a coluna data')

    data.drop(columns=['Segmento'], inplace=True)
    data = data.dropna(subset=['Setor', 'Desc %'])
    data.drop_duplicates(inplace=True)

   

    # Dados Externos
    pmc = pmc[pmc['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)'] != '...']
    meses_map = {
    'jan.': 'Jan',
    'fev.': 'Feb',
    'mar.': 'Mar',
    'abr.': 'Apr',
    'mai.': 'May',
    'jun.': 'Jun',
    'jul.': 'Jul',
    'ago.': 'Aug',
    'set.': 'Sep',
    'out.': 'Oct',
    'nov.': 'Nov',
    'dez.': 'Dec'
}
    # Converter a coluna de data
    pmc['Data'] = pd.to_datetime(pmc['Mês'].replace(meses_map, regex=True).str.replace(r'(\w+)-(\d+)', 
                                                       lambda m: f"01-{m.group(1)}-20{m.group(2)}",
                                                       regex=True),
                            format='%d-%b-%Y', errors='coerce')
    pmc['Data'] = pmc['Data'].dt.strftime('%Y-%m-%d')

    df_pmc_br = pmc[pmc['Brasil e Unidade da Federação'] == 'Brasil']
    df_pmc_es = pmc[pmc['Brasil e Unidade da Federação'] == 'Espírito Santo']
    df_pmc_es = df_pmc_es.drop(columns=['Brasil e Unidade da Federação', 'Tipos de índice', 'Mês'])
    df_pmc_br = df_pmc_br.drop(columns=['Brasil e Unidade da Federação', 'Tipos de índice', 'Data', 'Mês'])

    # Renomeando colunas
    df_pmc_es.rename(columns={
        'PMC - Número-índice (2022=100) (Número-índice)': 'PMC - Número-índice (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)': 'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)': 'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES'
    }, inplace=True)

    df_pmc_br.rename(columns={
        'PMC - Número-índice (2022=100) (Número-índice)': 'PMC - Número-índice (2022=100) (Número-índice)/ BR',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)': 'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)': 'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'
    }, inplace=True)

    df_pmc_es = df_pmc_es.reset_index()
    df_pmc_br = df_pmc_br.reset_index()
    df_combined = pd.concat([df_pmc_es, df_pmc_br], axis=1).drop(columns=['index'])


    df_combined = df_combined[['PMC - Número-índice (2022=100) (Número-índice)/ ES',
                               'PMC - Número-índice (2022=100) (Número-índice)/ BR',
                               'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
                               'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
                               'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES',
                               'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR',
                               'Data']]

    pmc = df_combined
    pmc['Data'] = pd.to_datetime(pmc['Data'])

    # Verificar quantos valores nulos existem em df_combined
    null_counts = pmc.isnull().sum()
    print(f'Quantidade de valores nulos em df_combined:\n{null_counts}')

    # Merge cleaned internal data with external PMC data
    cleaned = pd.merge(data, pmc, on='Data', how='left')

    # Remove commas and convert to numeric for PMC columns
    columns_to_fix = [
        'PMC - Número-índice (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice (2022=100) (Número-índice)/ BR',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ ES',
        'PMC - Número-índice com ajuste sazonal (2022=100) (Número-índice)/ BR',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES',
        'PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'
    ]
    def fun(var):
        var_str = str(var)
        result = ''
        found_comma = False

        for char in var_str:
            if char == ',':
                result += '.'
                found_comma = True
            elif char == '.' and not found_comma:
                continue
            else:
                result += char

        return result

    for col in columns_to_fix:
        cleaned[col] = cleaned[col].apply(fun)
        cleaned[col] = cleaned[col].astype(float)

    # cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES'] = cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES'].str.replace(',', '.')
    # cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'] = cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'].str.replace(',', '.')   
    # cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES'] = pd.to_numeric(cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ ES'], errors='coerce')
    # cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'] = pd.to_numeric(cleaned['PMC - Variação mês/mês imediatamente anterior, com ajuste sazonal (M/M-1) (%)/ BR'], errors='coerce')
    

    print(f'Quantidade de linhas em cleaned: {cleaned.shape[0]}')
    return cleaned
