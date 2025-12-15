# 📱 Gerador Profissional de Posts para Instagram

> **Versão Moderna e Completa** - Desenvolvido por Integrius Automações © 2025

## 🌟 Visão Geral

Aplicativo profissional desktop para Windows que gera posts completos para Instagram com:
- ✨ **Imagens Fotográficas Hiper-Realistas** usando Flux.1 (Replicate)
- 📝 **Textos Profissionais de Marketing** usando GPT-4 (OpenAI)
- 🎯 **Perfil de Gerente de Marketing** especializado em redes sociais
- 🎨 **Interface Moderna** com Dark/Light Mode (ttkbootstrap)

---

## 🚀 Funcionalidades Principais

### 📸 Aba 1: Posts Normais
Gere posts profissionais para seu negócio:
- **Formatos**: Feed (1:1), Reel (9:16), Stories (9:16)
- **Personalização**: Nicho, tema específico, tom de comunicação
- **Tom Profissional**: Profissional, Inspiracional, Educativo, Entusiasta, Premium
- **Call to Action**: Comentar, Curtir, Compartilhar, Seguir, Salvar, Link na Bio
- **Imagens**: Fotografia profissional hiper-realista com técnicas avançadas
- **Textos**: Legendas criadas por perfil de gerente de marketing
- **Hashtags**: 12 hashtags estratégicas (alto, médio e baixo volume)

### 🌅 Aba 2: Bom Dia Motivacional
Crie posts motivacionais em formato quadrado (1:1):
- **Categorias**: Sucesso, Força, Positividade, Foco, Amor Próprio, Metas, Esperança, Paz
- **Subtema Opcional**: Personalize ainda mais sua mensagem
- **Imagens**: Fotografias inspiradoras (nascer do sol, natureza, cenários motivacionais)
- **Mensagens**: Textos motivacionais autênticos e engajadores
- **Hashtags**: 12 hashtags motivacionais estratégicas

### 🎨 Recursos Visuais
- **Dark/Light Mode**: Alterne entre tema escuro e claro
- **Interface Moderna**: Design profissional com ttkbootstrap
- **Preview em Tempo Real**: Visualize imagens e textos antes de salvar
- **Multi-threading**: Geração sem travar a interface

---

## 📋 Requisitos

### Sistema
- **Windows 10/11** (64-bit)
- **Python 3.8+** instalado
- **Conexão com Internet** (para APIs)

### APIs Necessárias
1. **OpenAI API Key**
   - Para geração de textos com GPT-4
   - Obtenha em: https://platform.openai.com/api-keys
   - Custo aproximado: $0.03 por post completo

2. **Replicate API Token**
   - Para geração de imagens com Flux.1
   - Obtenha em: https://replicate.com/account/api-tokens
   - Custo aproximado: $0.04 por imagem

---

## 🔧 Instalação

### Passo 1: Instalar Dependências

```bash
# Instalar bibliotecas Python
pip install -r requirements.txt
```

### Passo 2: Configurar Chaves de API

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edite o arquivo `.env` com suas chaves:
   ```
   OPENAI_API_KEY=sk-...sua_chave_real_aqui
   REPLICATE_API_TOKEN=r8_...sua_chave_real_aqui
   ```

### Passo 3: Executar o Aplicativo

```bash
# Executar diretamente
python instagram_post_generator.py

# OU usar o script batch (Windows)
run_instagram_generator.bat
```

---

## 📖 Como Usar

### Gerando Posts Normais

1. **Selecione a Aba**: "📸 Posts Normais"

2. **Configure o Post**:
   - **Tipo**: Escolha Feed, Reel ou Stories
   - **Nicho**: Digite seu segmento (ex: "Tecnologia", "Fitness", "Moda")
   - **Tema**: Especifique o tema do post (ex: "Benefícios do treino matinal")
   - **Tom**: Selecione o tom da comunicação
   - **CTA**: Escolha a chamada para ação

3. **Gerar**: Clique em "🚀 GERAR POST PROFISSIONAL"

4. **Aguarde**: A geração leva 2-3 minutos (imagem + texto + hashtags)

5. **Resultados**:
   - Preview da imagem aparece na direita
   - Legenda e hashtags no campo de texto
   - Use os botões para salvar ou copiar

### Gerando Bom Dia Motivacional

1. **Selecione a Aba**: "🌅 Bom Dia Motivacional (1:1)"

2. **Configure**:
   - **Categoria**: Escolha a categoria motivacional
   - **Subtema** (opcional): Adicione um subtema específico

3. **Gerar**: Clique em "🌅 GERAR BOM DIA MOTIVACIONAL"

4. **Resultados**:
   - Imagem motivacional 1:1 (1080x1080)
   - Mensagem inspiradora
   - 12 hashtags motivacionais

---

## 🎨 Qualidade das Imagens

### Especificações Técnicas Fotográficas

Todas as imagens são geradas com:
- **Resolução**: 8K ultra-high-resolution
- **Câmeras Simuladas**: Canon EOS R5 / Sony A7R IV
- **Lentes**: Prime lens com f/1.8-2.8
- **Iluminação**: Golden hour natural ou estúdio profissional
- **Composição**: Regra dos terços, direção de arte profissional
- **Estilo**: Fotografia comercial de revista

### Técnicas Profissionais Aplicadas
- Shallow depth of field (desfoque de fundo natural)
- Bokeh natural e suave
- Color grading profissional
- White balance perfeito
- Exposição cinematográfica
- Qualidade RAW

---

## 💬 Qualidade dos Textos

### Perfil do Criador
**Gerente de Marketing Especializado em Redes Sociais**

Características:
- ✅ Experiência em conteúdo viral e engajador
- ✅ Foco em informar e atrair seguidores
- ✅ Copywriting profissional para Instagram
- ✅ Storytelling e conexão emocional
- ✅ CTAs estratégicas e efetivas

### Estrutura das Legendas
1. **Abertura Impactante**: Prende atenção nos primeiros segundos
2. **Valor Real**: Informações úteis, insights genuínos
3. **Storytelling**: Narrativa envolvente quando apropriado
4. **Conexão Emocional**: Empatia com o público
5. **Emojis Estratégicos**: 3-5 emojis bem posicionados
6. **Quebras de Linha**: Espaçamento para facilitar leitura
7. **Call to Action**: CTA clara e motivadora

---

## #️⃣ Estratégia de Hashtags

### Distribuição Inteligente (12 hashtags)
- **3 hashtags** de ALTO VOLUME (100k+ posts) - Alcance máximo
- **5 hashtags** de MÉDIO VOLUME (10k-100k posts) - Nicho específico
- **4 hashtags** de BAIXO VOLUME (<10k posts) - Público segmentado

### Critérios de Seleção
- ✅ Todas em português do Brasil
- ✅ Relevantes para o nicho específico
- ✅ Evita hashtags banidas ou spam
- ✅ Foco em engajamento genuíno
- ✅ Mix de hashtags gerais e específicas

---

## 💾 Salvando Conteúdo

### Opções de Salvamento

1. **💾 Salvar Tudo**
   - Salva imagem + arquivo de texto
   - Texto inclui legenda e hashtags
   - Nomes automáticos com timestamp

2. **🖼️ Salvar Imagem**
   - Salva apenas a imagem
   - Formato PNG de alta qualidade
   - Escolha o local de salvamento

3. **📋 Copiar Texto**
   - Copia legenda + hashtags
   - Direto para área de transferência
   - Cole no Instagram com Ctrl+V

---

## 🎨 Dark/Light Mode

Alterne entre tema escuro e claro:
- **Botão**: No topo da tela (☀️ Modo Claro / 🌙 Modo Escuro)
- **Preferências**: Salvas automaticamente
- **Interface**: Muda cores instantaneamente

---

## 🔍 Boas Práticas Implementadas

### Código Python
- ✅ **PEP 8**: Código segue padrões Python
- ✅ **Type Hints**: Anotações de tipo quando apropriado
- ✅ **Docstrings**: Documentação completa
- ✅ **Error Handling**: Tratamento robusto de erros
- ✅ **Multi-threading**: Operações assíncronas
- ✅ **Separação de Responsabilidades**: Classes e módulos bem estruturados

### Interface
- ✅ **Responsiva**: Redimensionável
- ✅ **Acessível**: Feedback visual claro
- ✅ **Moderna**: Design profissional com ttkbootstrap
- ✅ **Intuitiva**: Fluxo de uso simples

### Segurança
- ✅ **API Keys**: Armazenadas em .env (nunca no código)
- ✅ **Validação**: Inputs validados antes de processar
- ✅ **.gitignore**: Arquivos sensíveis não vão para Git

---

## 📊 Estrutura de Arquivos

```
Gerador-de-posts/
│
├── instagram_post_generator.py   # Aplicativo principal
├── openai_service.py              # Serviços de API (OpenAI + Replicate)
│
├── .env                           # Suas chaves de API (NÃO commitar)
├── .env.example                   # Exemplo de configuração
│
├── requirements.txt               # Dependências Python
├── README_INSTAGRAM_GENERATOR.md  # Esta documentação
│
├── run_instagram_generator.bat    # Script para executar (Windows)
│
└── generated_images/              # Pasta criada automaticamente
    └── (imagens geradas)
```

---

## 🐛 Solução de Problemas

### Erro: "Chave da API não encontrada"
**Solução**: Verifique se criou o arquivo `.env` e adicionou as chaves corretas.

### Erro: "Erro ao conectar com OpenAI/Replicate"
**Solução**:
1. Verifique sua conexão com internet
2. Confirme que as chaves de API estão corretas
3. Verifique se tem créditos nas contas

### Imagem não aparece no preview
**Solução**: A geração pode levar 2-3 minutos. Aguarde a mensagem de sucesso.

### Interface não responde
**Solução**: A geração roda em thread separada, mas pode demorar. Não feche o app.

---

## 💡 Dicas de Uso

1. **Seja Específico**: Quanto mais detalhado o tema do post, melhores os resultados
2. **Teste Tons**: Experimente diferentes tons para ver qual funciona melhor
3. **Revise Hashtags**: Você pode editar hashtags antes de publicar
4. **Salve Tudo**: Sempre salve para ter backup do conteúdo gerado
5. **Variação**: Use subtemas diferentes para criar variações

---

## 📞 Suporte

**Desenvolvido por**: Integrius Automações
**Ano**: 2025
**Copyright**: Todos os direitos reservados

---

## 📝 Changelog

### Versão 1.0.0 (2025-01-15)
- ✨ Lançamento inicial
- 📸 Suporte para Posts Normais (Feed, Reel, Stories)
- 🌅 Suporte para Bom Dia Motivacional (1:1)
- 🎨 Dark/Light Mode
- 🖼️ Integração com Flux.1 (Replicate)
- 📝 Integração com GPT-4 (OpenAI)
- 💾 Sistema de salvamento completo
- 🎯 Perfil de gerente de marketing profissional

---

## 📄 Licença

**Propriedade de**: Integrius Automações
**Uso**: Restrito conforme acordo de licenciamento

**Copyright © 2025 Integrius Automações. Todos os direitos reservados.**

---

## 🎉 Aproveite!

Este é um gerador profissional de posts para Instagram. Use com responsabilidade e criatividade para criar conteúdo incrível que informa, engaja e atrai seguidores!

**Boa sorte com suas criações! 🚀📱✨**
