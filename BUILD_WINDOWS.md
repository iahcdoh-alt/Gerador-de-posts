# 🪟 Como Gerar Executável Windows (.exe)

Este guia mostra como transformar a aplicação Python em um executável Windows que pode ser executado sem precisar do Python instalado.

## 📋 Pré-requisitos

- Windows 10/11
- Python 3.8 ou superior instalado
- Acesso à internet (para baixar dependências)

## 🚀 Método 1: Build Automático (Recomendado)

### Passo a Passo

1. **Abra o Prompt de Comando ou PowerShell**
   - Navegue até a pasta do projeto

2. **Execute o script de build**
   ```cmd
   build_windows.bat
   ```

3. **Aguarde o processo**
   - O script vai:
     - Criar ambiente virtual
     - Instalar PyInstaller
     - Instalar todas as dependências
     - Gerar o executável
     - Copiar arquivos necessários

4. **Executável gerado**
   - Localização: `dist\GeradordePosts.exe`
   - Tamanho aproximado: 50-100 MB

## 🛠️ Método 2: Build Manual

Se preferir fazer manualmente:

### 1. Instalar Dependências de Build

```cmd
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

### 2. Gerar o Executável

```cmd
pyinstaller GeradordePosts.spec
```

### 3. Copiar Arquivos Necessários

```cmd
copy .env dist\.env
mkdir dist\generated_images
```

## 📦 Distribuir o Executável

Após gerar o executável, você terá a pasta `dist\` com:

```
dist/
├── GeradordePosts.exe    # Executável principal
├── .env                  # Configuração (adicione sua API key)
└── generated_images/     # Pasta para imagens geradas
```

### Como Distribuir

**Opção 1: Arquivo ZIP**
1. Comprima a pasta `dist\` em um arquivo ZIP
2. Compartilhe o ZIP
3. Quem receber deve:
   - Extrair o ZIP
   - Editar o arquivo `.env` e adicionar a API key
   - Executar `GeradordePosts.exe`

**Opção 2: Instalador (Avançado)**
- Use ferramentas como Inno Setup ou NSIS para criar um instalador profissional

## ⚙️ Configuração Após Build

### 1. Adicionar API Key

Edite o arquivo `dist\.env`:
```
OPENAI_API_KEY=sk-sua-chave-aqui
```

### 2. Executar

Simplesmente clique duas vezes em `GeradordePosts.exe`

## 🎨 Personalizar o Executável

### Adicionar Ícone

1. Crie ou baixe um ícone `.ico`
2. Salve como `icon.ico` na raiz do projeto
3. Edite `GeradordePosts.spec`:
   ```python
   icon='icon.ico',  # linha ~47
   ```
4. Execute o build novamente

### Mudar Nome do Executável

Edite `GeradordePosts.spec`:
```python
name='MeuGerador',  # linha ~28
```

## 🔍 Solução de Problemas

### Erro: "PyInstaller não encontrado"
```cmd
pip install pyinstaller
```

### Erro: "Módulo não encontrado"
```cmd
pip install -r requirements.txt
```

### Executável muito grande
O executável contém o Python e todas as bibliotecas. Para reduzir:
- Use UPX (já habilitado no .spec)
- Remova dependências não utilizadas

### Antivírus bloqueia o executável
- Executáveis gerados com PyInstaller podem ser marcados como suspeitos
- Adicione exceção no antivírus
- Ou assine digitalmente o executável (requer certificado)

## 📏 Tamanhos Esperados

- **Executável**: ~50-100 MB
- **Primeira execução**: Cria pasta `generated_images/`
- **Cada imagem**: ~1-5 MB

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Nunca compartilhe o executável com sua API key dentro
- Sempre distribua com `.env.example`
- Instrua usuários a adicionar suas próprias chaves

## 🎯 Distribuição Profissional

Para distribuição profissional:

1. **Crie um README.txt** para incluir na pasta `dist\`:
```text
GERADOR DE POSTS PARA INSTAGRAM

1. Edite o arquivo .env
2. Adicione sua chave OpenAI API
3. Execute GeradordePosts.exe

Visite: [seu-site] para mais informações
```

2. **Adicione LICENSE.txt** se necessário

3. **Crie instalador** com Inno Setup (opcional)

## 💡 Dicas

- O executável funciona em qualquer Windows 10/11
- Não precisa instalar Python no PC de destino
- Todas as bibliotecas estão embutidas
- O executável é standalone (independente)

## 🆘 Suporte

Se encontrar problemas:
1. Verifique se todas as dependências foram instaladas
2. Execute `pyinstaller` manualmente para ver erros detalhados
3. Consulte: https://pyinstaller.org/en/stable/

---

**Boa distribuição!** 🚀
