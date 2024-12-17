# Inteli - Instituto de Tecnologia e Liderança 

<p align="center">
<a href= "https://www.inteli.edu.br/"><img src="assets/inteli.png" alt="Inteli - Instituto de Tecnologia e Liderança" border="0"></a>
</p>

# Athena

## Data 027

## :student: Integrantes: 
- <a href="https://www.linkedin.com/in/andre-dleizer/">Andre Dleizer</a> 
- <a href="https://www.linkedin.com/in/eduardo-rizk/">Eduardo Rizk</a>
- <a href="https://www.linkedin.com/in/leonardo-martins2005/">Leonardo Martins</a> 
- <a href="https://www.linkedin.com/in/marlos-do-carmo-guedes-366987250/">Marlos Guedes</a> 
- <a href="https://www.linkedin.com/in/pedro-haouli/">Pedro Haouli</a>
- <a href="https://www.linkedin.com/in/thiagovolcati/">Thiago Volcati</a>
- <a href="https://www.linkedin.com/in/raul-rezende-szpak-642079186//">Raul Szpak</a>

## :teacher: Professores:
### Orientador(a) 
- <a href="https://www.linkedin.com/in/marcelo-gon%C3%A7alves-phd-a550652/">Marcelo Gonçalves</a>
### Instrutores
- <a href="https://www.linkedin.com/in/filipe-gon%C3%A7alves-08a55015b/">Filipe Gonçalves</a>
- <a href="https://www.linkedin.com/in/fillipe-resina-b2211a22/">Fillipe Resina</a> 
- <a href="https://www.linkedin.com/in/francisco-escobar/">Francisco Escobar</a> 
- <a href="https://www.linkedin.com/in/jefferson-o-silva/">Jefferson Silva</a>
- <a href="https://www.linkedin.com/in/renato-penha/">Renato Penha</a> 
- <a href="https://www.linkedin.com/in/henrique-mohallem-paiva-6854b460/)">Henrique Paiva</a>
- <a href="https://www.linkedin.com/in/geraldo-magela-severino-vasconcelos-22b1b220/">Geraldo Vasconcelos</a> 


## 📝 Descrição

&nbsp;&nbsp;&nbsp;&nbsp;A Rede Gazeta do Espírito Santo, o maior grupo de comunicação do estado, enfrenta um desafio significativo na definição de metas de vendas de publicidade. Com suas metas baseadas apenas no desempenho do ano anterior e sem a consideração de fatores críticos como sazonalidade, desempenho dos setores dos clientes e eventos extraordinários, a empresa sofre com a imprecisão na definição das metas e a rentabilidade do negócio. Atualmente, ajustes são feitos com base no bom senso dos gestores, sem análise técnica ou quantitativa, e aspectos importantes como taxas de ocupação de inventário e descontos aplicados não são considerados adequadamente.

&nbsp;&nbsp;&nbsp;&nbsp;Para solucionar esse problema, propõe-se o desenvolvimento de um modelo preditivo de receitas publicitárias por setor econômico para a Rede Gazeta. Este modelo permitirá prever com maior precisão o potencial de receita futura, maximizando os resultados financeiros da empresa ao considerar variáveis críticas e dados históricos. O modelo analisará dados internos da Rede Gazeta juntamente com dados econômicos externos do Espírito Santo, fornecidos pelo Instituto Jones dos Santos Neves (IJSN). A solução visa gerar metas realistas, prever receitas futuras e diferenciar esses resultados por segmento de atuação da Rede Gazeta (TV, rádio, digital) e por região (Grande Vitória, Sul, Norte, Noroeste).

&nbsp;&nbsp;&nbsp;&nbsp;Ao incorporar fatores críticos que atualmente não são considerados, como sazonalidades, evolução de desempenho dos principais setores dos clientes e eventos extraordinários, o modelo proporcionará previsões mais assertivas. Além disso, levará em conta as taxas de ocupação do inventário e as taxas de desconto aplicadas, que impactam diretamente na receita total e na rentabilidade do negócio. Isso permitirá ajustes dinâmicos nas previsões ao longo do ano, respondendo rapidamente às mudanças no mercado e otimizando continuamente as estratégias de vendas e marketing.

&nbsp;&nbsp;&nbsp;&nbsp;Com a implementação deste modelo preditivo, a Rede Gazeta poderá alcançar uma previsão de crescimento de receita e definição de metas muito mais precisas, contribuindo significativamente para o planejamento financeiro da empresa. Além disso, o modelo ajudará na organização de parcerias futuras e na melhoria da eficiência operacional, pois ao prever demandas e tendências, a empresa poderá ajustar suas operações para melhorar a eficiência e reduzir desperdícios. Essa abordagem baseada em dados reais permitirá à Rede Gazeta tomar decisões mais inteligentes e otimizar suas estratégias econômicas e de marketing.


Link demonstrativo do modelo: <a href="https://youtu.be/Adi8tj1HJGQ"> Clique aqui</a>.

## 📁 Estrutura de pastas

Dentre os arquivos presentes na raiz do projeto, definem-se:

- <b>readme.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

- <b>assets</b>: todas as imagens e mídias utilizadas nos notebooks e documentação são posicionadas aqui.

- <b>documents</b>: aqui estarão todos os documentos do projeto. Há também uma pasta denominada <b>extras</b> onde estão presentes documentos complementares.

- <b>notebooks</b>: todos os Jupyter Notebooks criados para desenvolvimento do projeto.

- <b>backend</b>: O backend com o tratamento das tabelas e fazendo as previsões

- <b>athena</b>: O frontend feito em react

## 💻 Execução dos projetos

### Requisitos para execução dos notebooks localmente (VS Code) e no ambiente Google Colab

#### Localmente no VS Code:

1. **Instalação do Python e VS Code**:
   - Certifique-se de que o [Python](https://www.python.org/downloads/) esteja instalado em sua máquina (de preferência, versão 3.8 ou superior).
   - Baixe e instale o [Visual Studio Code (VS Code)](https://code.visualstudio.com/).
   - Instale a extensão "Python" no VS Code.

2. **Instalar dependências**:
   - Instale as bibliotecas necessárias:
     ```bash
     pip install pandas numpy matplotlib seaborn statsmodels scikit-learn xgboost sarimax optuna 
     ```

3. **Execução do Notebook**:
   - No VS Code, instale a extensão "Jupyter" se ainda não tiver instalada.
   - Abra o arquivo do notebook `.ipynb` diretamente no VS Code e clique em "Run All Cells" para executar.

### Interface com React e Backend com Uvicorn

1. **Frontend React**:
   - Navegue até a pasta `athena`.
   - No terminal, execute:
     ```bash
     npm install
     npm start
     ```

2. **Backend com FastAPI**:
   - Abra outro terminal e navegue até a pasta `backend`.
   - Execute:
     ```bash
     uvicorn app.main:app --reload
     ```
   - Acesse a interface de usuário React através do navegador no endereço [http://localhost:3000](http://localhost:3000) e a API FastAPI no [http://localhost:8000](http://localhost:8000).


## 🗃 Histórico de lançamentos

* 1.0.0 - 11/10/2024
    * [sprint 5] Lançamento da primeira versão do modelo preditivo com documentação.
* 0.6.0 - 27/09/2024
    * [sprint 4] Comparação de modelos preditivos
* 0.3.1 - 13/09/2024
    * [sprint 3] Preparação de dados e modelo preditivo preliminar
* 0.2.7 - 30/08/2024
    * [sprint 2] Análise exploratória e levantamento de hipóteses
* 0.1.3 - 16/08/2024
    * [sprint 1] Documentação de entendimento do negócio

## 📋 Licença/License

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Inteli-College/2024-2A-T12-IN03-G05.git">Data 027</a> by Inteli is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
