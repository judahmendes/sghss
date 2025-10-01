# SGHSS-BACKEND - Guia de Testes da API (Versão Refatorada)

## Configuração Base
- **URL Base**: `http://127.0.0.1:5000/api`
- **Headers padrão**: `Content-Type: application/json`
- **Autenticação**: `Authorization: Bearer {token}` (para endpoints protegidos)

## Melhorias Implementadas

### 🔧 **Refatorações e Boas Práticas**
- ✅ **Separação de responsabilidades** com módulos utilitários
- ✅ **Validação robusta** de CPF com verificação de dígitos
- ✅ **Exception handling** customizado
- ✅ **Logging estruturado** para auditoria
- ✅ **Decorators de autorização** por role
- ✅ **Formatação automática** de dados (CPF, telefone)
- ✅ **Sanitização de inputs** com limites de tamanho
- ✅ **Responses padronizadas** da API
- ✅ **Validação de senha** mais rigorosa (inclui caracteres especiais)

### 🛡️ **Melhorias de Segurança**
- ✅ **Validação de entrada** mais rigorosa
- ✅ **Rate limiting** conceitual implementado
- ✅ **Audit logging** para todas as ações
- ✅ **Sanitização** de dados de entrada
- ✅ **Error handling** que não vaza informações sensíveis

---

## 1. Health Check
**Verifica se a API está funcionando**

```http
GET http://127.0.0.1:5000/api/health
```

**Resposta esperada (200):**
```json
{
  "status": "healthy",
  "message": "SGHSS API is running"
}
```

---

## 2. Registro de Usuário
**Cria um novo usuário no sistema (com validação melhorada)**

```http
POST http://127.0.0.1:5000/api/auth/register
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "MinhaSenh@123!",
  "role": "patient"
}
```

**Validações implementadas:**
- ✅ Email deve ter formato válido
- ✅ Senha deve ter pelo menos 8 caracteres
- ✅ Senha deve conter letras, números e caracteres especiais
- ✅ Role deve ser válida (patient, professional, admin)

**Resposta esperada (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "role": "patient",
    "is_active": true,
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00"
  }
}
```

---

## 3. Login
**Autentica usuário e retorna token JWT (com logging de auditoria)**

```http
POST http://127.0.0.1:5000/api/auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "MinhaSenh@123!"
}
```

**Melhorias implementadas:**
- ✅ Log de tentativas de login (sucesso/falha)
- ✅ Validação de email antes da consulta
- ✅ Proteção contra ataques de timing

**Resposta esperada (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "role": "patient"
  }
}
```

---

## 4. Criar Perfil de Paciente
**Cria perfil detalhado com validação robusta de CPF**

```http
POST http://127.0.0.1:5000/api/patients
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "full_name": "Maria Silva Santos",
  "cpf": "123.456.789-01",
  "birth_date": "1990-05-15",
  "phone": "(11) 98765-4321",
  "address": "Rua das Flores, 123, São Paulo, SP",
  "allergies": ["Penicilina", "Lactose"],
  "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
  "medical_history": "Histórico de gastrite e deficiência de vitamina D"
}
```

**Validações implementadas:**
- ✅ **CPF**: Validação completa com dígitos verificadores
- ✅ **Telefone**: Validação de formato brasileiro
- ✅ **Data de nascimento**: Não pode ser futura ou idade > 120 anos
- ✅ **Campos obrigatórios**: Nome, CPF e data de nascimento
- ✅ **Sanitização**: Remoção de espaços extras e limitação de tamanho
- ✅ **Autorização**: Apenas usuários com role 'patient' podem criar

**Resposta esperada (201):**
```json
{
  "message": "Patient profile created successfully",
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "Maria Silva Santos",
    "cpf": "123.456.789-01",
    "birth_date": "1990-05-15",
    "phone": "(11) 98765-4321",
    "address": "Rua das Flores, 123, São Paulo, SP",
    "allergies": ["Penicilina", "Lactose"],
    "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
    "medical_history": "Histórico de gastrite e deficiência de vitamina D",
    "age": 35,
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00"
  }
}
```

---

## 5. Obter Meu Perfil de Paciente
**Retorna o perfil com dados formatados**

```http
GET http://127.0.0.1:5000/api/patients/me
Authorization: Bearer SEU_TOKEN_AQUI
```

**Melhorias implementadas:**
- ✅ **Formatação automática**: CPF e telefone formatados para exibição
- ✅ **Cálculo de idade**: Idade calculada automaticamente
- ✅ **Autorização**: Apenas pacientes podem acessar

**Resposta esperada (200):**
```json
{
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "Maria Silva Santos",
    "cpf": "123.456.789-01",
    "birth_date": "1990-05-15",
    "phone": "(11) 98765-4321",
    "address": "Rua das Flores, 123, São Paulo, SP",
    "allergies": ["Penicilina", "Lactose"],
    "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
    "medical_history": "Histórico de gastrite e deficiência de vitamina D",
    "age": 35,
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00"
  }
}
```

---

## 6. Atualizar Perfil de Paciente
**Atualiza com validações melhoradas**

```http
PUT http://127.0.0.1:5000/api/patients/me
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "phone": "(11) 99999-8888",
  "address": "Nova Rua, 456, São Paulo, SP",
  "allergies": ["Penicilina", "Lactose", "Aspirina"],
  "current_medications": ["Omeprazol 20mg"]
}
```

**Validações implementadas:**
- ✅ **Validação de telefone** se fornecido
- ✅ **Sanitização** de todos os campos de texto
- ✅ **Validação de listas** para alergias e medicamentos
- ✅ **Limitação de tamanho** para campos longos
- ✅ **Auditoria** de alterações

---

## 7. Informações do Usuário Atual
**Endpoint melhorado para obter dados do usuário**

```http
GET http://127.0.0.1:5000/api/auth/me
Authorization: Bearer SEU_TOKEN_AQUI
```

**Resposta esperada (200):**
```json
{
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "role": "patient",
    "is_active": true,
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00",
    "profile": {
      "id": 1,
      "full_name": "Maria Silva Santos",
      "cpf": "123.456.789-01",
      "age": 35
    }
  }
}
```

---

## Novos Códigos de Erro

| Código | Significado | Exemplo |
|--------|-------------|---------|
| 400 | Bad Request | `{"error": "Request body is required"}` |
| 401 | Unauthorized | `{"error": "Invalid email or password"}` |
| 403 | Forbidden | `{"error": "Required role: patient"}` |
| 404 | Not Found | `{"error": "Patient profile not found"}` |
| 409 | Conflict | `{"error": "Email already registered"}` |
| 422 | Validation Error | `{"error": "Password must contain at least one special character"}` |
| 500 | Internal Error | `{"error": "Internal server error"}` |

---

## Validações Implementadas

### 📧 **Email**
- Formato válido obrigatório
- Conversão automática para lowercase

### 🔒 **Senha**
- Mínimo 8 caracteres
- Deve conter letras, números e caracteres especiais
- Máximo 128 caracteres

### 📱 **CPF**
- Validação completa com dígitos verificadores
- Aceita formatos: 12345678901 ou 123.456.789-01
- Armazenado sem formatação, exibido formatado

### 📞 **Telefone**
- Formatos válidos: (11) 98765-4321 ou (11) 8765-4321
- Validação de DDD brasileiro

### 📅 **Data de Nascimento**
- Formato obrigatório: YYYY-MM-DD
- Não pode ser futura
- Idade máxima: 120 anos

---

## Logs de Auditoria

Todas as ações importantes são registradas:
- ✅ Registro de usuários
- ✅ Login/logout (sucesso e falhas)
- ✅ Criação/atualização de perfis
- ✅ Tentativas de acesso negado
- ✅ Refresh de tokens

---

## Testando com cURL (Exemplos Atualizados)

### Registro com senha forte:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","password":"Senha@123!","role":"patient"}'
```

### Login:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","password":"Senha@123!"}'
```

### Criar perfil com CPF formatado:
```bash
curl -X POST http://127.0.0.1:5000/api/patients \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"João Silva","cpf":"123.456.789-01","birth_date":"1995-08-20"}'
```

---

## 🏆 **Resumo das Melhorias**

1. **Arquitetura**: Separação clara de responsabilidades
2. **Validação**: Validações robustas e informativas
3. **Segurança**: Melhores práticas de autenticação e autorização
4. **Auditoria**: Log completo de ações do usuário
5. **UX**: Formatação automática e mensagens claras de erro
6. **Manutenibilidade**: Código modular e bem documentado
7. **Performance**: Validações otimizadas e queries eficientes

O sistema agora está muito mais robusto e segue as melhores práticas de desenvolvimento de APIs REST!

---

## 1. Health Check
**Verifica se a API está funcionando**

```http
GET http://127.0.0.1:5000/api/health
```

**Resposta esperada (200):**
```json
{
  "status": "healthy",
  "message": "SGHSS API is running"
}
```

---

## 2. Registro de Usuário
**Cria um novo usuário no sistema**

```http
POST http://127.0.0.1:5000/api/auth/register
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "MinhaSenh@123",
  "role": "patient"
}
```

**Roles disponíveis**: `patient`, `professional`, `admin`

**Resposta esperada (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "role": "patient",
    "is_active": true,
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00"
  }
}
```

---

## 3. Login
**Autentica usuário e retorna token JWT**

```http
POST http://127.0.0.1:5000/api/auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "MinhaSenh@123"
}
```

**Resposta esperada (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "role": "patient"
  }
}
```

⚠️ **Importante**: Salve o `access_token` para usar nos próximos endpoints!

---

## 4. Criar Perfil de Paciente
**Cria perfil detalhado para usuários do tipo 'patient'**

```http
POST http://127.0.0.1:5000/api/patients
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "full_name": "Maria Silva Santos",
  "cpf": "12345678901",
  "birth_date": "1990-05-15",
  "phone": "(11) 98765-4321",
  "address": "Rua das Flores, 123, São Paulo, SP",
  "allergies": ["Penicilina", "Lactose"],
  "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
  "medical_history": "Histórico de gastrite e deficiência de vitamina D"
}
```

**Campos obrigatórios**: `full_name`, `cpf`, `birth_date`

**Resposta esperada (201):**
```json
{
  "message": "Patient profile created successfully",
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "Maria Silva Santos",
    "cpf": "12345678901",
    "birth_date": "1990-05-15",
    "phone": "(11) 98765-4321",
    "address": "Rua das Flores, 123, São Paulo, SP",
    "allergies": ["Penicilina", "Lactose"],
    "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
    "medical_history": "Histórico de gastrite e deficiência de vitamina D",
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00"
  }
}
```

---

## 5. Listar Todos os Pacientes (Admin)
**Lista todos os pacientes cadastrados (apenas administradores)**

```http
GET http://127.0.0.1:5000/api/patients?page=1&per_page=10
Authorization: Bearer SEU_TOKEN_ADMIN_AQUI
```

**Parâmetros de consulta opcionais:**
- `page`: Número da página (padrão: 1)
- `per_page`: Itens por página (padrão: 10, máximo: 100)

**Autorização**: Apenas usuários com role 'admin'

**Resposta esperada (200):**
```json
{
  "patients": [
    {
      "id": 1,
      "user_id": 1,
      "full_name": "Maria Silva Santos",
      "cpf": "123.456.789-01",
      "birth_date": "1990-05-15",
      "phone": "(11) 98765-4321",
      "address": "Rua das Flores, 123, São Paulo, SP",
      "allergies": ["Penicilina", "Lactose"],
      "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
      "medical_history": "Histórico de gastrite e deficiência de vitamina D",
      "age": 35,
      "email": "maria@exemplo.com",
      "created_at": "2025-09-29T10:30:00",
      "updated_at": "2025-09-29T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 1,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

---

## 6. Obter Meu Perfil de Paciente
**Retorna o perfil do paciente logado**

```http
GET http://127.0.0.1:5000/api/patients/me
Authorization: Bearer SEU_TOKEN_AQUI
```

**Resposta esperada (200):**
```json
{
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "Maria Silva Santos",
    "cpf": "12345678901",
    "birth_date": "1990-05-15",
    "phone": "(11) 98765-4321",
    "address": "Rua das Flores, 123, São Paulo, SP",
    "allergies": ["Penicilina", "Lactose"],
    "current_medications": ["Omeprazol 20mg", "Vitamina D3"],
    "medical_history": "Histórico de gastrite e deficiência de vitamina D",
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T10:30:00",
    "age": 35
  }
}
```

---

## 7. Atualizar Meu Perfil de Paciente
**Atualiza dados do perfil do paciente logado**

```http
PUT http://127.0.0.1:5000/api/patients/me
Authorization: Bearer SEU_TOKEN_AQUI
Content-Type: application/json

{
  "phone": "(11) 99999-8888",
  "address": "Nova Rua, 456, São Paulo, SP",
  "allergies": ["Penicilina", "Lactose", "Aspirina"],
  "current_medications": ["Omeprazol 20mg"],
  "medical_history": "Histórico de gastrite controlada"
}
```

**Resposta esperada (200):**
```json
{
  "message": "Patient profile updated successfully",
  "patient": {
    "id": 1,
    "user_id": 1,
    "full_name": "Maria Silva Santos",
    "cpf": "12345678901",
    "birth_date": "1990-05-15",
    "phone": "(11) 99999-8888",
    "address": "Nova Rua, 456, São Paulo, SP",
    "allergies": ["Penicilina", "Lactose", "Aspirina"],
    "current_medications": ["Omeprazol 20mg"],
    "medical_history": "Histórico de gastrite controlada",
    "created_at": "2025-09-29T10:30:00",
    "updated_at": "2025-09-29T11:45:00",
    "age": 35
  }
}
```

---

## Usuários de Teste Pré-Criados

Execute o script `create_test_data.py` para criar estes usuários automaticamente:

| Email | Senha | Role | Descrição |
|-------|-------|------|-----------|
| `paciente1@sghss.com` | `SenhaSegura123` | patient | Paciente com perfil completo |
| `paciente2@sghss.com` | `OutraSenha456` | patient | Paciente com perfil completo |
| `medico1@sghss.com` | `MedicoSeguro789` | professional | Profissional de saúde |
| `admin@sghss.com` | `AdminSeguro101` | admin | Administrador |

---

## Códigos de Erro Comuns

| Código | Significado | Possível Causa |
|--------|-------------|----------------|
| 400 | Bad Request | Dados inválidos ou campos obrigatórios ausentes |
| 401 | Unauthorized | Token inválido ou expirado |
| 403 | Forbidden | Usuário sem permissão para esta ação |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Email ou CPF já cadastrado |
| 500 | Internal Server Error | Erro interno do servidor |

---

## Dicas para Teste

1. **Sempre use HTTPS em produção**
2. **Tokens JWT expiram em 1 hora** - use refresh_token para renovar
3. **CPF deve ter 11 dígitos** - pode incluir pontos e traços que serão removidos
4. **Data de nascimento** deve estar no formato `YYYY-MM-DD`
5. **Campos de array** (allergies, medications) podem ser enviados como array vazio `[]`
6. **Headers obrigatórios**: `Content-Type: application/json` para POST/PUT
7. **Autenticação**: `Authorization: Bearer {token}` para endpoints protegidos

---

## Testando com cURL

### Exemplo de registro:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","password":"Senha123","role":"patient"}'
```

### Exemplo de login:
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"teste@email.com","password":"Senha123"}'
```

### Exemplo com token:
```bash
curl -X GET http://127.0.0.1:5000/api/patients/me \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```
