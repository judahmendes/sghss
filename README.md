# SGHSS - Sistema de Gestão Hospitalar e de Serviços de Saúde (Versão 1.0)

## 📋 Descrição

O SGHSS é um sistema de back-end robusto desenvolvido em Flask para gerenciar serviços hospitalares e de saúde. O sistema oferece funcionalidades para cadastro e autenticação de usuários, gestão de pacientes, profissionais de saúde, consultas e prontuários médicos, seguindo as melhores práticas de desenvolvimento e segurança.

## 🎯 **Funcionalidades Implementadas (Conforme Especificação)**

### � **Sistema de Autenticação Completo**
- ✅ **Registro de usuários** com validação rigorosa de senha (8+ caracteres, letras, números e símbolos)
- ✅ **Login com JWT** - tokens de acesso (1h) e refresh (30 dias)
- ✅ **Renovação automática de tokens** via refresh token
- ✅ **Sistema de logout** com auditoria
- ✅ **Controle de acesso por roles** (patient, professional, admin)

### � **Gestão de Pacientes Avançada**
- ✅ **Cadastro completo** com validação de CPF (dígitos verificadores)
- ✅ **Perfil pessoal** - dados básicos, alergias, medicações
- ✅ **Histórico médico** básico integrado
- ✅ **Validações específicas** - telefone brasileiro, idade máxima 120 anos
- ✅ **Formatação automática** - CPF, telefone e cálculo de idade
- ✅ **Listagem paginada** (apenas para administradores)

### 🛡️ **Segurança e Conformidade LGPD**
- ✅ **Hash seguro de senhas** com bcrypt e salt automático
- ✅ **Validação de CPF completa** com algoritmo de dígitos verificadores
- ✅ **Sanitização automática** de todos os inputs
- ✅ **Sistema de auditoria** para rastreabilidade LGPD
- ✅ **Controle granular de acesso** baseado em roles
- ✅ **Logs estruturados** para debugging e conformidade

### �️ **Interface Web Moderna**
- ✅ **Dashboard interativo** para teste de todos os endpoints
- ✅ **Autenticação integrada** com armazenamento local seguro
- ✅ **Renovação automática** de tokens expirados
- ✅ **Design responsivo** para desktop e mobile
- ✅ **Feedback visual** em tempo real

## 🛠️ Tecnologias Utilizadas

### **Core**
- **Flask 3.1.1**: Framework web Python
- **SQLAlchemy 2.0.41**: ORM para banco de dados
- **Flask-JWT-Extended 4.7.1**: Autenticação JWT
- **Flask-CORS 6.0.0**: Suporte a CORS

### **Segurança**
- **bcrypt 5.0.0**: Hash de senhas
- **PyJWT 2.10.1**: Tokens JWT

### **Utilitários**
- **python-dotenv 1.0.1**: Gerenciamento de variáveis de ambiente
- **marshmallow 4.0.1**: Serialização e validação
- **marshmallow-sqlalchemy 1.4.2**: Integração SQLAlchemy

### **Banco de Dados**
- **SQLite**: Desenvolvimento
- **PostgreSQL**: Produção futura (recomendado)

## 📁 Estrutura do Projeto

```
sghss-backend/
├── src/
│   ├── models/                 # Modelos de dados
│   │   ├── __init__.py
│   │   ├── user.py            # Modelo de usuário melhorado
│   │   ├── patient.py         # Modelo de paciente
│   │   ├── professional.py    # Modelo de profissional
│   │   ├── appointment.py     # Modelo de consulta
│   │   ├── medical_record.py  # Modelo de prontuário
│   │   ├── prescription.py    # Modelo de receita
│   │   └── audit_log.py       # Modelo de auditoria
│   ├── routes/                 # Rotas da API
│   │   ├── __init__.py
│   │   ├── auth.py            # Autenticação refatorada
│   │   └── patient.py         # Rotas de paciente melhoradas
│   ├── utils/                  # Utilitários (NOVO)
│   │   ├── __init__.py
│   │   ├── validators.py      # Validadores robustos
│   │   ├── exceptions.py      # Exceções customizadas
│   │   └── helpers.py         # Funções auxiliares
│   ├── config.py              # Configurações melhoradas
│   ├── constants.py           # Constantes do sistema (NOVO)
│   └── main.py                # Aplicação principal
├── logs/                       # Logs do sistema (NOVO)
├── database/                   # Banco de dados
├── requirements.txt           # Dependências organizadas
├── .env.example              # Exemplo de variáveis
├── .gitignore                # Git ignore completo
├── API_TESTING_GUIDE.md      # Guia de testes atualizado
└── README.md                 # Esta documentação
```

## 🚀 Instalação e Execução

### 📋 **Pré-requisitos**
- Python 3.11+
- pip

### 🔧 **Passos para execução**

1. **Clone o repositório**
```bash
git clone <repository-url>
cd sghss-backend
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute a aplicação**
```bash
python src/main.py
```

A API estará disponível em `http://127.0.0.1:5000`

## 🧪 Testando a API

### **Usuários Pré-criados**
| Email | Senha | Role | 
|-------|-------|------|
| `paciente1@sghss.com` | `Senha$egura123` | patient |
| `paciente2@sghss.com` | `Outra$enha456` | patient |
| `medico1@sghss.com` | `Medico$eguro789` | professional |
| `admin@sghss.com` | `Admin$eguro101` | admin |

Para testar a API, use ferramentas como Postman ou Insomnia com os endpoints elencados neste arquivo.

### **Documentação Completa**
Consulte o [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md) para exemplos detalhados.

## 🔒 Validações Implementadas

### **Email**
- Formato RFC válido
- Conversão automática para lowercase
- Verificação de duplicatas

### **Senha**
- Mínimo 8 caracteres
- Deve conter: letras, números e caracteres especiais
- Máximo 128 caracteres
- Hash bcrypt com salt

### **CPF**
- Validação completa com dígitos verificadores
- Aceita formatos: `12345678901` ou `123.456.789-01`
- Verificação de duplicatas
- Formatação automática na resposta

### **Telefone**
- Formatos brasileiros: `(11) 98765-4321` ou `(11) 8765-4321`
- Validação de DDD
- Formatação automática

### **Data de Nascimento**
- Formato obrigatório: `YYYY-MM-DD`
- Não pode ser futura
- Idade máxima: 120 anos
- Cálculo automático de idade

## 📊 Endpoints da API

### **Autenticação**
- `POST /api/auth/register` - Registro de usuário
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Dados do usuário atual
- `POST /api/auth/logout` - Logout

### **Pacientes**
- `POST /api/patients` - Criar perfil de paciente
- `GET /api/patients/me` - Obter meu perfil
- `PUT /api/patients/me` - Atualizar meu perfil

### **Sistema**
- `GET /api/health` - Health check

## 📝 Logs e Auditoria

O sistema registra automaticamente:
- ✅ Tentativas de login (sucesso/falha)
- ✅ Criação e atualização de perfis
- ✅ Ações administrativas
- ✅ Erros do sistema
- ✅ Acessos negados

Logs são salvos em `logs/sghss.log` com rotação automática.

## 🔧 Configuração

### **Variáveis de Ambiente**
```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DEV_DATABASE_URL=sqlite:///database/app.db
DATABASE_URL=postgresql://user:pass@localhost/sghss_db

# CORS (produção)
CORS_ORIGINS=https://yourdomain.com
```

### **Configurações por Ambiente**
- **Development**: Debug ativo, SQLite, logs detalhados
- **Testing**: Banco em memória, logs reduzidos
- **Production**: PostgreSQL, logs otimizados, segurança máxima

## 🛡️ Segurança

### **Implementações**
- ✅ Hash bcrypt para senhas
- ✅ Tokens JWT com expiração
- ✅ Validação rigorosa de entrada
- ✅ Sanitização de dados
- ✅ Rate limiting conceitual
- ✅ Logs de auditoria
- ✅ Error handling seguro

### **Recomendações para Produção**
- Use HTTPS exclusivamente
- Configure CORS adequadamente
- Implemente rate limiting
- Use banco PostgreSQL
- Configure backup automático
- Monitore logs de segurança

## 🚀 Deploy em Produção

### **Usando Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.main:app"
```

### **Usando Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "src.main:app"]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Email: judahmendes388@gmail.com
- Documentação: [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- Issues: Use o GitHub Issues para reportar bugs

---

**Desenvolvido com ❤️ para a área da saúde**

## Funcionalidades Implementadas

### Autenticação e Autorização
- Sistema de registro e login com JWT
- Controle de acesso baseado em roles (paciente, profissional, admin)
- Tokens de acesso e refresh para segurança
- Validação de email e senha

### Gestão de Pacientes
- Cadastro completo de pacientes
- Visualização e atualização de dados pessoais
- Histórico médico e consultas
- Controle de acesso (pacientes só veem seus próprios dados)

### Modelos de Dados
- **User**: Usuários do sistema com autenticação
- **Patient**: Dados pessoais e médicos dos pacientes
- **Professional**: Informações dos profissionais de saúde
- **Appointment**: Agendamento de consultas
- **MedicalRecord**: Prontuários médicos
- **Prescription**: Receitas médicas
- **AuditLog**: Logs de auditoria para conformidade LGPD

## Tecnologias Utilizadas

- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para banco de dados
- **Flask-JWT-Extended**: Autenticação JWT
- **Flask-CORS**: Suporte a CORS
- **bcrypt**: Hash de senhas
- **SQLite**: Banco de dados (desenvolvimento)

## Instalação e Execução

### Pré-requisitos
- Python 3.11+
- pip

### Passos para execução

1. **Clone o repositório**
```bash
git clone <repository-url>
cd sghss-backend
```

2. **Ative o ambiente virtual**
  - **Linux/Mac**
```bash
source venv/bin/activate
```
  - **Windows**
```bash
venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python src/main.py
```

A aplicação estará disponível em `http://localhost:5000`

## Endpoints da API

### Autenticação (`/api/auth`)

#### POST /api/auth/register
Registra um novo usuário no sistema.

**Corpo da requisição:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123",
  "role": "patient"
}
```

**Resposta de sucesso (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "usuario@email.com",
    "role": "patient",
    "is_active": true,
    "created_at": "2025-01-01T10:00:00",
    "updated_at": "2025-01-01T10:00:00"
  }
}
```

#### POST /api/auth/login
Autentica um usuário e retorna tokens JWT.

**Corpo da requisição:**
```json
{
  "email": "usuario@email.com",
  "password": "senha123"
}
```

**Resposta de sucesso (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "user": {
    "id": 1,
    "email": "usuario@email.com",
    "role": "patient"
  }
}
```

#### POST /api/auth/refresh
Renova o token de acesso usando o refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Resposta de sucesso (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn..."
}
```

#### GET /api/auth/me
Retorna informações do usuário atual.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de sucesso (200):**
```json
{
  "user": {
    "id": 1,
    "email": "usuario@email.com",
    "role": "patient",
    "profile": {
      "id": 1,
      "full_name": "João Silva",
      "cpf": "12345678900"
    }
  }
}
```

### Pacientes (`/api/patients`)

#### GET /api/patients
Lista todos os pacientes (apenas admin/profissional).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de sucesso (200):**
```json
{
  "patients": [
    {
      "id": 1,
      "user_id": 1,
      "full_name": "João Silva",
      "cpf": "12345678900",
      "birth_date": "1990-01-01",
      "phone": "11999999999",
      "address": "Rua das Flores, 123"
    }
  ]
}
```

#### POST /api/patients
Cria um novo perfil de paciente.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Corpo da requisição:**
```json
{
  "full_name": "João Silva",
  "cpf": "12345678900",
  "birth_date": "1990-01-01",
  "phone": "11999999999",
  "address": "Rua das Flores, 123",
  "allergies": ["penicilina"],
  "current_medications": ["paracetamol"]
}
```

**Resposta de sucesso (201):**
```json
{
  "message": "Patient created successfully",
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "João Silva",
    "cpf": "12345678900",
    "birth_date": "1990-01-01"
  }
}
```

#### GET /api/patients/{id}
Obtém dados de um paciente específico.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de sucesso (200):**
```json
{
  "patient": {
    "id": 1,
    "full_name": "João Silva",
    "cpf": "12345678900",
    "birth_date": "1990-01-01"
  }
}
```

#### PUT /api/patients/{id}
Atualiza dados de um paciente.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Corpo da requisição:**
```json
{
  "phone": "11888888888",
  "address": "Nova Rua, 456"
}
```

#### GET /api/patients/{id}/history
Obtém o histórico médico de um paciente.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Resposta de sucesso (200):**
```json
{
  "patient_id": 1,
  "medical_records": [],
  "appointments": []
}
```

### Health Check

#### GET /api/health
Verifica se a API está funcionando.

**Resposta de sucesso (200):**
```json
{
  "status": "healthy",
  "message": "SGHSS API is running"
}
```

## Estrutura do Projeto

```
sghss-backend/
├── src/
│   ├── models/          # Modelos de dados
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── professional.py
│   │   ├── appointment.py
│   │   ├── medical_record.py
│   │   ├── prescription.py
│   │   └── audit_log.py
│   ├── routes/          # Rotas da API
│   │   ├── auth.py
│   │   └── patient.py
│   ├── static/          # Arquivos estáticos
│   ├── database/        # Banco de dados SQLite
│   └── main.py          # Arquivo principal
├── venv/                # Ambiente virtual
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## Segurança

- Senhas são hasheadas com bcrypt
- Autenticação JWT com tokens de acesso e refresh
- Controle de acesso baseado em roles
- Validação de entrada de dados
- CORS configurado para desenvolvimento

## Conformidade LGPD

- Modelo AuditLog para rastreamento de operações
- Controle de acesso a dados pessoais
- Estrutura preparada para implementar direito ao esquecimento

## Desenvolvimento

Para adicionar novas funcionalidades:

1. Crie novos modelos em `src/models/`
2. Implemente rotas em `src/routes/`
3. Registre blueprints em `src/main.py`
4. Atualize `requirements.txt` se necessário

## Próximos Passos

- Implementar rotas para profissionais de saúde
- Adicionar sistema de agendamento de consultas
- Implementar prontuários médicos
- Adicionar testes automatizados
- Configurar deploy em produção