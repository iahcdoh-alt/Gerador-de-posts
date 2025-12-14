# 📱 Gerador de Posts para Instagram

Aplicação de automação para geração de posts para Instagram usando Inteligência Artificial (OpenAI).

Gere automaticamente **imagens**, **legendas** e **hashtags** otimizadas para diferentes tipos de conteúdo do Instagram!

## ✨ Funcionalidades

- 🖼️ **Geração de Imagens** com DALL-E 3
  - Posts para Feed (1024x1024)
  - Reels (1024x1792 - formato vertical)
  - Stories (1024x1792 - formato vertical)

- ✍️ **Criação de Legendas** com GPT-4
  - 6 tons diferentes: Sério, Divertido, Engraçado, Inspiracional, Educativo, Luxuoso
  - Adaptadas para cada tipo de post
  - Com emojis estratégicos e CTA (Call-to-Action)

- #️⃣ **Geração de Hashtags Inteligentes**
  - Entre 10 e 15 hashtags por post
  - Mix estratégico: hashtags populares, médio alcance e específicas
  - Otimizadas para o nicho escolhido

- 💾 **Salvamento Automático**
  - Imagens em alta qualidade
  - Arquivo .txt com legenda completa e hashtags
  - Organização por data e hora

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave da API OpenAI ([Obtenha aqui](https://platform.openai.com/api-keys))

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Gerador-de-posts
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure a API Key**
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave
# OPENAI_API_KEY=sk-sua-chave-aqui
```

## 💻 Como Usar

### Execução Básica

```bash
python main.py
```

### Fluxo de Uso

1. **Escolha o tipo de post**
   - Feed (post no feed)
   - Reel (vídeo curto)
   - Stories (história temporária)

2. **Digite o nicho do conteúdo**
   - Exemplos: Fitness, Moda, Tecnologia, Culinária, Viagens, Marketing Digital, etc.

3. **Selecione o tom da legenda**
   - Sério (Profissional e formal)
   - Divertido (Animado e alegre)
   - Engraçado (Humorístico e descontraído)
   - Inspiracional (Motivador e inspirador)
   - Educativo (Informativo e didático)
   - Luxuoso (Sofisticado e premium)

4. **Confirme os dados**

5. **Aguarde a geração**
   - A IA gerará sua imagem, legenda e hashtags
   - Os arquivos serão salvos automaticamente na pasta `generated_images/`

### Exemplo de Uso

```
📌 TIPO DE POST
1. Feed (Post no feed)
2. Reel (Vídeo curto)
3. Stories (História temporária)

👉 Escolha o tipo de post (1-3): 1

🎯 NICHO DO CONTEÚDO
👉 Digite o nicho do seu conteúdo: Marketing Digital

🎭 TOM DA LEGENDA
1. Sério
2. Divertido
3. Engraçado
4. Inspiracional
5. Educativo
6. Luxuoso

👉 Escolha o tom da legenda (1-6): 5
```

## 🪟 Versão Windows (Executável .exe)

Você pode gerar um executável Windows standalone que não precisa do Python instalado!

### Gerar Executável

**Método Rápido:**
```cmd
build_windows.bat
```

Isso criará `dist\GeradordePosts.exe` que pode ser executado em qualquer Windows 10/11.

### Documentação Completa

Para instruções detalhadas sobre como gerar e distribuir o executável Windows, consulte:
📖 **[BUILD_WINDOWS.md](BUILD_WINDOWS.md)**

### Vantagens do Executável

- ✅ Não precisa instalar Python
- ✅ Executável standalone (~50-100 MB)
- ✅ Fácil de distribuir
- ✅ Interface idêntica à versão Python
- ✅ Funciona em qualquer Windows 10/11

## 📁 Estrutura do Projeto

```
Gerador-de-posts/
├── main.py                 # Aplicação principal (interface CLI)
├── openai_service.py       # Serviço de integração com OpenAI
├── requirements.txt        # Dependências do projeto
├── requirements-dev.txt    # Dependências para build (PyInstaller)
├── .env.example           # Exemplo de arquivo de configuração
├── .env                   # Suas configurações (não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
├── README.md             # Documentação principal
├── BUILD_WINDOWS.md      # Guia para build Windows
├── setup.sh              # Script de instalação Linux/Mac
├── setup.bat             # Script de instalação Windows
├── build_windows.bat     # Script para gerar .exe
├── GeradordePosts.spec   # Configuração PyInstaller
└── generated_images/     # Pasta com imagens e posts gerados
    ├── *.png            # Imagens geradas
    └── *.txt            # Posts completos (legenda + hashtags)
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **OpenAI API** - Geração de imagens (DALL-E 3) e textos (GPT-4)
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Pillow** - Processamento de imagens
- **Requests** - Requisições HTTP

## 💡 Dicas de Uso

1. **Qualidade das Imagens**
   - As imagens são geradas em alta qualidade
   - Para Reels e Stories, o formato é vertical (9:16)
   - Para Feed, o formato é quadrado (1:1)

2. **Legendas**
   - Adapte a legenda gerada conforme sua necessidade
   - Adicione detalhes específicos do seu negócio
   - Revise sempre antes de publicar

3. **Hashtags**
   - Use todas as hashtags geradas ou selecione as mais relevantes
   - O Instagram permite até 30 hashtags, mas 10-15 é o ideal
   - Varie as hashtags entre posts para maior alcance

4. **Custos da API**
   - DALL-E 3: ~$0.040 por imagem (qualidade standard)
   - GPT-4: ~$0.03 por 1K tokens
   - Monitore seu uso em: https://platform.openai.com/usage

## ⚠️ Limitações e Considerações

- É necessário ter créditos na conta OpenAI
- A geração de cada post consome créditos da API
- As imagens são geradas pela IA e podem precisar de ajustes
- Sempre revise o conteúdo antes de publicar

## 🔒 Segurança

- **NUNCA** compartilhe seu arquivo `.env`
- **NUNCA** faça commit da sua API Key
- Mantenha suas credenciais seguras
- O arquivo `.gitignore` já está configurado para proteger informações sensíveis

## 🐛 Solução de Problemas

### Erro: "Chave da API OpenAI não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que a variável `OPENAI_API_KEY` está configurada corretamente

### Erro ao gerar imagem
- Verifique se você tem créditos suficientes na OpenAI
- Confirme sua conexão com a internet
- Verifique se a API Key está válida

### Imagens não sendo salvas
- Verifique se você tem permissão de escrita na pasta
- Confirme que a pasta `generated_images/` existe

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal e comercial.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Enviar pull requests

## 📧 Suporte

Para dúvidas ou suporte, abra uma issue no repositório.

## 🎯 Próximas Funcionalidades

- [ ] Suporte para múltiplas imagens
- [ ] Geração de carrosséis
- [ ] Templates personalizados
- [ ] Agendamento de posts
- [ ] Integração direta com Instagram API
- [ ] Interface web (GUI)
- [ ] Banco de dados para histórico de posts

---

**Desenvolvido com ❤️ usando OpenAI**

*Gere conteúdo incrível para o Instagram em segundos!* 🚀
