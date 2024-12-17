import React, { useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine, Label,
} from 'recharts';
import './App.css';
import Header from './components/Header';
import Dropdown from './components/Dropdown';
import atena from './assets/images/atena.svg';
import ButtonUpload from './components/ButtonUpload.jsx';
import ButtonConfirm from './components/ButtonConfirm.jsx';

function App() {
  const [externalFile, setExternalFile] = useState(null);
  const [internalFile, setInternalFile] = useState(null);
  const [selectedModel, setSelectedModel] = useState('');
  const [selectedSecondModel, setSelectedSecondModel] = useState('');
  const [selectedThirdModel, setSelectedThirdModel] = useState('');
  const [chartData, setChartData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [notification, setNotification] = useState({ message: '', visible: false, fadeOut: false });
  const [progress, setProgress] = useState(100);
  const [externalUploaded, setExternalUploaded] = useState(false);
  const [internalUploaded, setInternalUploaded] = useState(false);
  const [downloadAvailable, setDownloadAvailable] = useState(false);
  const [secondDropdownOptions, setSecondDropdownOptions] = useState([]);

  const options1 = [
    { label: 'Geral', value: 'Geral' },
    { label: 'UEN', value: 'UEN' },
    { label: 'Origem', value: 'Origem' },
  ];

  const options3 = [
    { label: 'Rádio', value: 'Rádio' },
    { label: 'Digital', value: 'Digital' },
    { label: 'Televisão', value: 'Televisão' },
  ];

  const options4 = [
    { label: 'Vitória', value: 'Vitória' },
    { label: 'Cachoeiro', value: 'Cachoeiro' },
    { label: 'Colatina', value: 'Colatina' },
    { label: 'Linhares', value: 'Linhares' },
    { label: 'Mídia Programática', value: 'Mídia Programática' },
    { label: 'Mercado Nacional', value: 'Mercado Nacional' },
  ];

  const options5 = [
    { label: 'Sarimax', value: 'Sarimax' },
    { label: 'Xgboost', value: 'Xgboost' },
  ];

  const handleExternalFileChange = (event) => {
    const file = event.target.files[0];
    console.log('External file selected:', file);
    setExternalFile(file);
    setExternalUploaded(true);
    showNotification(`O arquivo ${file.name} teve o upload com sucesso.`);
  };

  const handleInternalFileChange = (event) => {
    const file = event.target.files[0];
    console.log('Internal file selected:', file);
    setInternalFile(file);
    setInternalUploaded(true);
    showNotification(`O arquivo ${file.name} teve o upload com sucesso.`);
  };

  const handleModelChange = (event) => {
    console.log('Model selected:', event.target.value);
    setSelectedModel(event.target.value);

    // Atualiza as opções do segundo dropdown com base na seleção do primeiro dropdown
    switch (event.target.value) {
      case 'Geral':
        setSecondDropdownOptions([]);
        setSelectedSecondModel('Geral'); // Define 'Geral' automaticamente
        break;
      case 'UEN':
        setSecondDropdownOptions(options3);
        setSelectedSecondModel('');
        break;
      case 'Origem':
        setSecondDropdownOptions(options4);
        setSelectedSecondModel('');
        break;
      default:
        setSecondDropdownOptions([]);
        setSelectedSecondModel('');
    }
  };

  const handleSecondModelChange = (event) => {
    console.log('Second model selected:', event.target.value);
    setSelectedSecondModel(event.target.value);
  };

  const handleThirdModelChange = (event) => {
    console.log('Third model selected:', event.target.value);
    setSelectedThirdModel(event.target.value);
  };

  const handleConfirmClick = async () => {
    console.log('Confirm button clicked');
    console.log('External file:', externalFile);
    console.log('Internal file:', internalFile);
    console.log('Selected model:', selectedSecondModel);
    console.log('Prediction model:', selectedThirdModel);

    if (!externalFile || !internalFile || !selectedThirdModel || (!selectedSecondModel && selectedModel !== 'Geral')) {
      alert('Por favor, selecione os arquivos e o modelo.');
      return;
    }

    const formData = new FormData();
    formData.append('pmc_file', externalFile);
    formData.append('data_file', internalFile);
    formData.append('model', selectedSecondModel);
    formData.append('type_model', selectedThirdModel);

    try {
      const response = await fetch('http://localhost:8000/process-data/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Erro na requisição');
      }

      const result = await response.json();
      console.log('Resultado:', result);

      const lastMonthsData = Object.keys(result.lastmonths).map((key) => ({
        date: key,
        lastmonths: result.lastmonths[key],
        forecast: null,
      }));

      const forecastData = Object.keys(result.forecast).map((key) => ({
        date: key,
        lastmonths: null,
        forecast: result.forecast[key],
      }));

      const combinedData = [...lastMonthsData, ...forecastData];

      if (combinedData.length > 0) {
        setChartData(combinedData);
        setMetrics(result.metricas);
        setDownloadAvailable(true);
      } else {
        console.error('Erro: dados de resposta inválidos.');
      }
    } catch (error) {
      console.error('Erro:', error);
    }
  };

  const showNotification = (message) => {
    setNotification({ message, visible: true, fadeOut: false });
    setProgress(100);
    let interval = setInterval(() => {
      setProgress((prev) => {
        if (prev <= 0) {
          clearInterval(interval);
          fadeOutNotification();
          return 0;
        }
        return prev - 1;
      });
    }, 30);
  };

  const fadeOutNotification = () => {
    setNotification((prevState) => ({ ...prevState, fadeOut: true }));
    setTimeout(() => {
      setNotification({ message: '', visible: false, fadeOut: false });
    }, 1000);
  };

  const closeNotification = () => {
    fadeOutNotification();
    setProgress(0);
  };

  const handleDownloadClick = () => {
    window.location.href = 'http://localhost:8000/download-forecast';
  };

  return (
    <div className="App">
      <Header />
      {notification.visible && (
        <div className={`notification ${notification.fadeOut ? 'fade-out' : ''}`}>
          <span>{notification.message}</span>
          <button className="close-btn" onClick={closeNotification}>X</button>
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
        </div>
      )}
      <div className="content-container">
        <div className="shape left-shape">
          <div className="left-shape-container">
            <img src={atena} alt="Atena" className="atena-image" />
            <Dropdown
              options={options1}
              placeholder="Selecione o tipo de modelo"
              label="Tipo"
              onChange={handleModelChange}
            />
            {secondDropdownOptions.length > 0 && (
              <Dropdown
                options={secondDropdownOptions}
                placeholder="Selecione o modelo"
                label="Modelo"
                onChange={handleSecondModelChange}
              />
            )}
            <Dropdown
              options={options5}
              placeholder="Selecione o tipo de previsão"
              label="Previsão"
              onChange={handleThirdModelChange}
            />
            <ButtonUpload
              label="Upload dados externos"
              onFileChange={handleExternalFileChange}
              inputId="external-file-upload"
              uploaded={externalUploaded}
            />
            <ButtonUpload
              label="Upload dados internos"
              onFileChange={handleInternalFileChange}
              inputId="internal-file-upload"
              uploaded={internalUploaded}
            />
            <ButtonConfirm label="Fazer a previsão" onClick={handleConfirmClick} />
          </div>
        </div>
        <div className="shape right-shape">
            {chartData.length > 0 ? (
              <div className="scrollable-container">
                <div>
                  <h3 style={{ textAlign: 'center', marginBottom: '20px', color: 'white' }}>
                    {selectedModel ? `Valores Reais vs Previsões ${selectedModel}` : 'Valores Reais vs Previsões'}
                  </h3>
                  
                  <ResponsiveContainer width={1000} height={400}>
                    <LineChart data={chartData}>
                      <defs>
                        {/* Filtro de sombra azul */}
                        <filter id="blueShadow" x="-50%" y="-50%" width="200%" height="200%">
                          <feDropShadow dx="0" dy="0" stdDeviation="5" floodColor="#007BFF" />
                        </filter>
                        {/* Filtro de sombra laranja */}
                        <filter id="yellowShadow" x="-50%" y="-50%" width="200%" height="200%">
                          <feDropShadow dx="0" dy="0" stdDeviation="5" floodColor="#FFA500" />
                        </filter>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#ccc" />
                      <XAxis dataKey="date">
                        <Label value="Data" position="insideBottomRight" offset={-5} />
                      </XAxis>
                      <YAxis>
                        <Label value="Valor" angle={0} position="insideLeft" dy={-10} />
                      </YAxis>
                      <Tooltip />
                      <Legend verticalAlign="top" height={36} />
                      <Line
                        type="monotone"
                        dataKey="lastmonths"
                        stroke="#007BFF"
                        strokeWidth={3}
                        strokeOpacity={1}
                        activeDot={{ r: 8 }}
                        filter="url(#blueShadow)"
                        name="Últimos Meses"
                      />
                      <Line
                        type="monotone"
                        dataKey="forecast"
                        stroke="#FFA500"
                        strokeWidth={3}
                        strokeOpacity={1}
                        activeDot={{ r: 8 }}
                        filter="url(#yellowShadow)"
                        name="Previsão"
                      />
                      <ReferenceLine x="2024-04" stroke="red" strokeDasharray="3 3" label="" />
                    </LineChart>

                    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', marginRight: '20px', color: 'white' }}>
                        <span style={{ color: "#007BFF", marginRight: '5px' }}>●</span>
                        <span>Últimos Meses</span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', color: 'white' }}>
                        <span style={{ color: "#FFA500", marginRight: '5px' }}>●</span>
                        <span>Previsão</span>
                      </div>
                    </div>
                  </ResponsiveContainer>
                </div>
                {metrics && (
                  <div className="metrics-table">
                    <table>
                      <thead>
                        <tr>
                          <th className="no-data-message">Métrica</th>
                          <th className="no-data-message">Valor</th>
                        </tr>
                      </thead>
                      <tbody className="no-data-message">
                        <tr>
                          <td>R²</td>
                          <td>{metrics.r2.toFixed(2)}</td>
                        </tr>
                        <tr>
                          <td>MAPE</td>
                          <td>{metrics.mape.toFixed(2)}</td>
                        </tr>
                        <tr>
                          <td>RMSE</td>
                          <td>{metrics.rmse.toFixed(2)}</td>
                        </tr>
                        <tr>
                          <td>MAE</td>
                          <td>{metrics.mae.toFixed(2)}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                )}
                {downloadAvailable && (
                  <button className="download-button" onClick={handleDownloadClick}>Baixar Previsões</button>
                )}
              </div>
            ) : (
              <p className="no-data-message">Sem dados disponíveis para o gráfico.</p>
            )}

        </div>
      </div>
    </div>
  );
}

export default App;
