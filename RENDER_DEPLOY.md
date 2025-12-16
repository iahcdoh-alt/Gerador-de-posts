# 🚀 Deploy no Render - Instagram Post Generator

## 📱 Mais Simples que Railway!

O Render é mais fácil e direto. Vamos deployar em **5 minutos**!

---

## ✨ PASSO 1: Criar Conta no Render

1. **Acesse:** https://render.com
2. **Clique em:** "Get Started" ou "Sign Up"
3. **Escolha:** "Sign up with GitHub"
4. **Autorize** o Render no GitHub

✅ **Conta criada!**

---

## 📦 PASSO 2: Criar Web Service

1. No dashboard do Render, clique em: **"New +"** (canto superior direito)
2. Escolha: **"Web Service"**
3. **Conecte** seu repositório GitHub:
   - Se ainda não conectou, clique "Connect GitHub"
   - Procure: `Gerador-de-posts`
   - Clique em **"Connect"**

✅ **Repositório conectado!**

---

## ⚙️ PASSO 3: Configurar o Service

Preencha os campos:

### **Informações Básicas:**
- **Name:** `instagram-post-generator` (ou qualquer nome)
- **Region:** Deixe o padrão (Oregon)
- **Branch:** `claude/instagram-post-generator-gT38p`

### **Build & Deploy:**
- **Root Directory:** (deixe vazio)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements-web.txt`
- **Start Command:** `uvicorn main_web:app --host 0.0.0.0 --port $PORT`

### **Plano:**
- Escolha: **"Free"** (totalmente grátis!)

✅ **Configurações OK!**

---

## 🔑 PASSO 4: Adicionar Variáveis de Ambiente (CRÍTICO!)

**ANTES de clicar em "Create Web Service":**

1. Role até a seção **"Environment Variables"**
2. Clique em **"Add Environment Variable"**
3. Adicione estas 2 variáveis:

**Variável 1:**
```
Key: OPENAI_API_KEY
Value: sk-sua_chave_real_openai_aqui
```

**Variável 2:**
```
Key: REPLICATE_API_TOKEN
Value: r8_sua_chave_real_replicate_aqui
```

**Variável 3 (Opcional):**
```
Key: PYTHON_VERSION
Value: 3.10.0
```

✅ **Variáveis configuradas!**

---

## 🚀 PASSO 5: Deploy!

1. **Clique no botão:** "Create Web Service" (no final da página)
2. **Aguarde** 3-5 minutos enquanto o Render:
   - Faz o build
   - Instala dependências
   - Inicia o servidor

3. **Acompanhe os logs** em tempo real na tela

✅ **Deploy em andamento!**

---

## ✅ PASSO 6: Acessar Seu App

Quando aparecer **"Live"** com bolinha verde:

1. No topo da página, você verá a URL:
   - `https://instagram-post-generator-XXXX.onrender.com`
2. **Clique na URL** ou copie e abra no navegador

✅ **App online!**

---

## 🎉 PRONTO!

Seu app está no ar! Teste:

1. ✅ Página carrega bonita
2. ✅ Dark/Light mode funciona
3. ✅ Gere um post de teste

---

## 💰 CUSTOS

### **Render Free Plan:**
- ✅ **100% GRÁTIS**
- ✅ Sem limite de tempo
- ✅ 750 horas/mês
- ⚠️ Pode "dormir" após 15 min sem uso (demora 30s para "acordar")

### **Render Paid Plan ($7/mês):**
- ✅ Sem "dormir"
- ✅ Mais recursos
- ✅ Builds mais rápidos

---

## 🔄 REDEPLOY (Atualizar App)

**Automático:**
- Qualquer push no GitHub dispara redeploy automático

**Manual:**
1. No dashboard do Render
2. Clique em **"Manual Deploy"**
3. Escolha **"Deploy latest commit"**

---

## 🐛 RESOLVER PROBLEMAS

### **App não inicia:**
- Clique em **"Logs"** no menu esquerdo
- Veja o erro
- Verifique se as variáveis de ambiente estão corretas

### **Erro 503:**
- Normal se o app estava "dormindo"
- Aguarde 30 segundos e recarregue

### **Erro ao gerar imagem:**
- Verifique `REPLICATE_API_TOKEN` em **Environment**
- Settings → Environment → Edit

### **Erro ao gerar texto:**
- Verifique `OPENAI_API_KEY` em **Environment**
- Confirme créditos na OpenAI

---

## ⚙️ CONFIGURAÇÕES ÚTEIS

### **Domínio Personalizado:**
1. Settings → Custom Domains
2. Clique "Add Custom Domain"
3. Siga instruções

### **Ver Logs em Tempo Real:**
1. Menu esquerdo → **"Logs"**
2. Logs aparecem automaticamente

### **Métricas:**
1. Menu esquerdo → **"Metrics"**
2. Veja CPU, memória, requisições

---

## 📊 COMPARAÇÃO: Render vs Railway

| Característica | Render | Railway |
|----------------|--------|---------|
| **Plano Grátis** | ✅ Ilimitado | ❌ $5 crédito/mês |
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Interface** | ✅ Simples | ❌ Complexa |
| **Cold Start** | ~30s | ~10s |
| **Logs** | ✅ Excelentes | ✅ Bons |
| **Suporte** | ✅ Muito bom | ✅ Bom |

---

## ✅ CHECKLIST COMPLETO

- [ ] Criar conta no Render
- [ ] Conectar repositório GitHub
- [ ] Configurar Web Service
- [ ] Adicionar variáveis de ambiente
- [ ] Clicar "Create Web Service"
- [ ] Aguardar deploy
- [ ] Acessar URL gerada
- [ ] Testar geração de post

---

## 🎯 PRÓXIMOS PASSOS

Depois do deploy:

1. ✅ Salve a URL do seu app
2. ✅ Teste todas funcionalidades
3. ✅ Compartilhe com sua equipe
4. ✅ Configure domínio personalizado (opcional)

---

## 📞 SUPORTE

**Precisa de ajuda?**
- Me mostre os logs
- Me diga qual erro apareceu
- Tire screenshot se necessário

---

**Desenvolvido por Integrius Automações • 2025**

**Boa sorte com o Render! É muito mais fácil! 🚀**
