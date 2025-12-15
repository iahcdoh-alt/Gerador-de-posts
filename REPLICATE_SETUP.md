# 🎨 Como Obter sua Chave da API Replicate

Para usar o Flux.1 (geração de imagens), você precisa de uma chave da API Replicate.

## 📝 Passo a Passo:

### 1. Criar Conta no Replicate

Acesse: https://replicate.com/

Clique em **"Sign Up"** e crie sua conta (pode usar GitHub ou Google)

### 2. Obter API Key

1. Após fazer login, clique no seu perfil (canto superior direito)
2. Clique em **"API tokens"** ou acesse: https://replicate.com/account/api-tokens
3. Clique em **"Create token"**
4. Copie o token (começa com `r8_...`)

### 3. Adicionar no .env

Abra o arquivo `.env` e adicione:

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
REPLICATE_API_KEY=r8_xxxxxxxxxxxxx
```

**Substitua os `xxx` pelas suas chaves reais!**

## 💰 Preços Replicate (Flux.1):

- **Flux.1.1 Pro**: ~$0.0032 por imagem
- **Muito mais barato que DALL-E 3** (~$0.040)
- Pague apenas pelo que usar
- Sem mensalidade

## 🎯 O que a aplicação usa:

- **Imagens**: Replicate Flux.1.1 Pro (qualidade superior!)
- **Legendas**: OpenAI GPT-4
- **Hashtags**: OpenAI GPT-4

## ❓ FAQ:

**P: Preciso das duas chaves?**
R: Sim! OpenAI para texto e Replicate para imagens.

**P: Quanto vou gastar?**
R: Depende do uso. Exemplo:
- 100 posts = ~$0.32 (Replicate) + ~$0.50 (OpenAI) = ~$0.82 total

**P: Posso voltar para DALL-E?**
R: Sim! Basta alterar o provider no código para "openai".

**P: Tenho créditos grátis?**
R: Replicate dá $5 de crédito inicial grátis! (~1500 imagens)

## ✅ Verificar se está tudo certo:

Depois de configurar o `.env`, teste executando:

```cmd
python main_gui.py
```

Se as chaves estiverem corretas, a aplicação abrirá sem erros!

---

**Qualquer dúvida, consulte a documentação oficial:**
- Replicate: https://replicate.com/docs
- OpenAI: https://platform.openai.com/docs
