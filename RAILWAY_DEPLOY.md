# 🚀 Deploy no Railway - Instagram Post Generator

## 📱 Web App Completo

Versão web do Gerador Profissional de Posts para Instagram com:
- ✅ Interface moderna e responsiva
- ✅ Dark/Light Mode
- ✅ FastAPI backend
- ✅ Flux.1 para imagens hiper-realistas
- ✅ GPT-4 para textos profissionais

---

## 🎯 Deploy em 5 Minutos

### **1. Criar Conta no Railway**

1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em "New Project"

---

### **2. Conectar Repositório**

1. Escolha "Deploy from GitHub repo"
2. Selecione o repositório: `iahcdoh-alt/Gerador-de-posts` (ou Post-Gen2.0)
3. Branch: `claude/instagram-post-generator-gT38p`

---

### **3. Configurar Variáveis de Ambiente**

No Railway, vá em **Variables** e adicione:

```bash
OPENAI_API_KEY=sk-sua_chave_real_aqui
REPLICATE_API_TOKEN=r8_sua_chave_real_aqui
```

**Importante:** Use suas chaves REAIS!

---

### **4. Configurar Build**

O Railway detecta automaticamente o `railway.toml`, mas você pode configurar manualmente:

**Settings → Deploy:**
- **Build Command:** (deixe em branco, usa default)
- **Start Command:** `uvicorn main_web:app --host 0.0.0.0 --port $PORT`

---

### **5. Deploy Automático**

1. Railway faz deploy automaticamente
2. Aguarde 3-5 minutos
3. Clique em "View Deployment" para ver o app

---

## 📊 Estrutura de Arquivos

```
/
├── main_web.py              ← Backend FastAPI
├── openai_service.py        ← Serviço de APIs
├── templates/
│   └── index.html           ← Interface web
├── static/
│   ├── css/
│   │   └── style.css        ← Estilos
│   └── js/
│       └── script.js        ← JavaScript
├── railway.toml             ← Config Railway
├── Procfile                 ← Alternativa de config
├── requirements-web.txt     ← Dependências Python
└── .env.example             ← Exemplo de variáveis
```

---

## ⚙️ Configurações do Railway

### **Variáveis de Ambiente Obrigatórias:**

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `OPENAI_API_KEY` | Chave OpenAI GPT-4 | `sk-proj-...` |
| `REPLICATE_API_TOKEN` | Chave Replicate Flux.1 | `r8_...` |
| `PORT` | Porta (auto) | `8000` |

### **Recursos Recomendados:**

- **Memory:** 512 MB (mínimo)
- **CPU:** Shared (grátis) ou dedicado
- **Disk:** 1 GB

---

## 🌐 Acessar o App

Após o deploy:

1. Railway gera URL automática: `https://seu-app.railway.app`
2. Acesse a URL
3. Configure suas chaves se ainda não fez
4. Comece a gerar posts!

---

## 🔧 Comandos Úteis

### **Rodar Localmente:**

```bash
# Instalar dependências
pip install -r requirements-web.txt

# Configurar .env
cp .env.example .env
# Edite .env com suas chaves

# Rodar servidor
uvicorn main_web:app --reload --port 8000

# Acessar
http://localhost:8000
```

### **Ver Logs no Railway:**

1. No dashboard do projeto
2. Clique em "View Logs"
3. Acompanhe em tempo real

---

## 📱 Funcionalidades Web

### **Aba 1: Posts Normais**
- Feed (1:1)
- Reel (9:16)
- Stories (9:16)
- 5 tons de comunicação
- 6 tipos de CTA

### **Aba 2: Bom Dia Motivacional**
- Formato 1:1 fixo
- 8 categorias motivacionais
- Subtema opcional
- Cenas do cotidiano incluídas

### **Recursos:**
- ✅ Dark/Light mode (salvo no navegador)
- ✅ Preview de imagens
- ✅ Copiar texto
- ✅ Baixar imagem
- ✅ Interface responsiva

---

## 💰 Custos

### **Railway (Hospedagem):**
- **Grátis:** $5 de crédito/mês
- **Pro:** $20/mês (unlimited)

### **APIs:**
- **OpenAI:** ~$0.03 por post
- **Replicate:** ~$0.04 por imagem

**Total por post:** ~$0.07

---

## 🐛 Troubleshooting

### **App não inicia:**
- Verifique as variáveis de ambiente
- Veja os logs: railway logs

### **Erro 502:**
- Aguarde alguns segundos (cold start)
- Verifique se o build terminou

### **Imagem não gera:**
- Verifique REPLICATE_API_TOKEN
- Veja console do navegador (F12)

### **Texto não gera:**
- Verifique OPENAI_API_KEY
- Confira se tem créditos na OpenAI

---

## 📚 Documentação

- **FastAPI:** https://fastapi.tiangolo.com
- **Railway:** https://docs.railway.app
- **OpenAI:** https://platform.openai.com/docs
- **Replicate:** https://replicate.com/docs

---

## 🔒 Segurança

**IMPORTANTE:**
- ✅ Nunca commite o arquivo `.env`
- ✅ Use variáveis de ambiente no Railway
- ✅ Proteja suas chaves de API
- ✅ `.env` está no `.gitignore`

---

## 🚀 Próximos Passos

Depois do deploy:

1. **Teste todas as funcionalidades**
2. **Configure domínio personalizado** (Railway Settings)
3. **Monitore uso de créditos** (OpenAI + Replicate)
4. **Compartilhe o link** com sua equipe

---

## 📞 Suporte

**Desenvolvido por:** Integrius Automações
**Ano:** 2025
**Licença:** Todos os direitos reservados

---

**Boa sorte com seu deploy! 🎉**
