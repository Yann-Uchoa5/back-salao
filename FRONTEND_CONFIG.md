# Configuração da URL do Backend para o Frontend

## URLs da API

### Desenvolvimento Local
Se o frontend estiver rodando localmente (fora do Docker):
```env
VITE_BACKEND_API_URL=http://localhost:8000/api/v1
```

### Desenvolvimento com Docker
Se o frontend estiver rodando no mesmo Docker Compose:
```env
VITE_BACKEND_API_URL=http://backend:8000/api/v1
```

### Produção
Quando você hospedar o backend em produção, use o domínio do servidor:
```env
VITE_BACKEND_API_URL=http://api.salao.com/api/v1
# ou
VITE_BACKEND_API_URL=https://api.salao.com/api/v1
```

## Estrutura da API

Todos os endpoints estão prefixados com `/api/v1/`:

- **Autenticação**: `/api/v1/auth/`
  - `POST /api/v1/auth/login` - Login (form-data, usa email no campo username)
  - `POST /api/v1/auth/login/json` - Login (JSON com email e senha)
  - `POST /api/v1/auth/registro` - Registrar usuário
  - `GET /api/v1/auth/me` - Obter usuário atual
  - `GET /api/v1/auth/test-auth` - Testar autenticação

- **Clientes**: `/api/v1/clientes/`
  - `GET /api/v1/clientes` - Listar clientes
  - `POST /api/v1/clientes` - Criar cliente (requer admin)
  - `GET /api/v1/clientes/{id}` - Obter cliente
  - `GET /api/v1/clientes/{id}/historico` - Obter cliente com histórico
  - `PUT /api/v1/clientes/{id}` - Atualizar cliente (requer admin)
  - `DELETE /api/v1/clientes/{id}` - Deletar cliente (requer admin)
  - `POST /api/v1/clientes/{id}/foto` - Upload foto (requer admin)
  - `GET /api/v1/clientes/{id}/foto` - Visualizar foto

- **Procedimentos**: `/api/v1/procedimentos/`
  - `GET /api/v1/procedimentos` - Listar procedimentos
  - `POST /api/v1/procedimentos` - Criar procedimento (requer autenticação)
  - `GET /api/v1/procedimentos/{id}` - Obter procedimento
  - `PUT /api/v1/procedimentos/{id}` - Atualizar procedimento (requer autenticação)
  - `DELETE /api/v1/procedimentos/{id}` - Deletar procedimento (requer autenticação)

## Exemplo de uso no Frontend

### Arquivo `.env.development`
```env
VITE_BACKEND_API_URL=http://localhost:8000/api/v1
```

### Arquivo `.env.production`
```env
VITE_BACKEND_API_URL=https://api.salao.com/api/v1
```

### Exemplo de chamada API (JavaScript/TypeScript)
```javascript
const API_URL = import.meta.env.VITE_BACKEND_API_URL;

// Login (usa email e senha)
const response = await fetch(`${API_URL}/auth/login/json`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'usuario@email.com',
    password: 'senha'
  })
});

const { access_token } = await response.json();

// Criar procedimento
const procedimentoResponse = await fetch(`${API_URL}/procedimentos`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    cliente_id: 1,
    data_procedimento: '2024-01-15',
    tipo_procedimento: 'Coloração',
    valor_procedimento: 150.00
  })
});
```

## CORS

Se você estiver usando um frontend separado, precisará configurar CORS no FastAPI. Adicione no `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Adicione as origens do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

