# 🚨 Vigilant API

API em **Python + Flask** para monitoramento de **sites, APIs e URLs**.  
Ela é o “motor” do sistema Vigilant: executa as verificações em background, salva métricas no banco e disponibiliza os dados via JSON para o frontend em PHP.

---

## ✨ Funcionalidades

- ✅ Cadastro de alvos (sites/APIs/URLs)
- 🔁 Verificação automática de status (cron/worker)
- ⏱️ Medição de tempo de resposta
- 📊 Histórico de métricas por alvo
- 🔐 Autenticação via API Key
- 🌐 Endpoints REST (JSON)
- 🩺 Health check para monitoramento do serviço

---

## 🧱 Arquitetura


[ Vigilant API (Flask) ]
↓ JSON
[ Frontend PHP (InfinityFree) ]


A API roda em um host separado (ex: Render) e o frontend PHP consome os dados via HTTP.

---

## ⚙️ Tecnologias

- Python 3
- Flask
- Gunicorn
- MySQL
- Requests

---

## 📦 Instalação local

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/vigilant-api.git
cd vigilant-api
