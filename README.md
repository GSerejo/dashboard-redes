Dashboard de Tráfego de Servidor (Tempo Real)
Visão Geral
Protótipo para capturar tráfego de/para um servidor específico e exibir janelas de 5s agregadas por cliente (IP). O dashboard oferece:

Gráfico Principal: Volume de tráfego de Entrada/Saída por Cliente (IP).

Drill Down Interativo: Ao clicar na barra do cliente, um modal exibe a quebra detalhada por protocolo (HTTP, FTP, SSH, SMTP, DNS, etc.).

Resumo de Protocolos: Seção com gráficos de rosca (Doughnut Charts) mostrando a distribuição percentual do tráfego total por protocolo.

Como Rodar (Ambiente Local)
Pré-requisitos
Python 3.x e Node.js instalados.

Windows: Instale o Npcap e marque a opção "Install Npcap in WinPcap API-compatible Mode" para que a captura de pacotes funcione.

1. Backend (API e Coletor de Pacotes)
Configuração do IP Alvo: Defina o endereço IP da máquina que você deseja monitorar.

Altere a variável SERVER_IP no arquivo backend/app.py para o IP real da sua máquina (ex: 192.168.0.22).

Instalar Dependências: Certifique-se de estar no diretório raiz do projeto e use seu ambiente virtual (.venv).

pip install -r backend/requirements.txt

Rodar a API:

# Execute a partir da pasta raiz do projeto
sudo uvicorn backend.app:app --host 0.0.0.0 --port 8000
# NOTA: O 'sudo' (ou permissões de administrador no Windows) é NECESSÁRIO 
# para que a Scapy consiga realizar a captura de pacotes na rede.

2. Frontend (Dashboard)
Instalar Dependências:

cd frontend 
npm install

Rodar o Servidor de Desenvolvimento (Vite):

npm run dev

Acessar: Abra o navegador em http://localhost:5173 (porta padrão do Vite).

Testes e Simulação de Carga
Para ver dados e testar todos os protocolos, certifique-se de que os serviços (HTTP, FTP, SMTP, DNS, SSH) estão rodando na máquina alvo (SERVER_IP).

Tráfego Misto: Use 5 ou mais máquinas clientes diferentes (ou clientes virtuais) para acessar o servidor simultaneamente, garantindo que o tráfego dos novos protocolos (SMTP, DNS, SSH) seja gerado.

Gere Carga: Baixe arquivos grandes via HTTP/FTP para criar picos de tráfego que o dashboard registrará.

Observações Técnicas
Gerenciamento de Estado: O frontend utiliza useState, useEffect e useMemo para garantir que o dashboard seja fluido, reativo e performático.

Em produção, prefira usar tshark ou capturadores em modo kernel para performance.

Para retenção a longo prazo, salve dados em Redis/InfluxDB.
