# 📦 Como Criar o Instalador

Este guia explica como criar um instalador profissional para o Gerador de Posts Instagram.

## 🎯 Pré-requisitos

### 1. Baixar e Instalar o Inno Setup

1. Acesse: https://jrsoftware.org/isdl.php
2. Baixe a versão mais recente (ex: `innosetup-6.3.3.exe`)
3. Execute o instalador
4. Aceite todas as opções padrão
5. Instale normalmente

**💡 Importante:** O Inno Setup é gratuito e open-source!

### 2. Ter o Executável Compilado

Certifique-se de que você já compilou o executável:

```powershell
# No PowerShell do Windows
cd \\wsl$\Ubuntu\home\hans\Gerador-de-posts
pyinstaller --clean GeradordePosts_GUI.spec
```

Deve existir o arquivo: `dist\GeradordePosts_GUI.exe`

## 🚀 Criar o Instalador

### Método Automático (Recomendado)

No PowerShell do Windows:

```powershell
cd \\wsl$\Ubuntu\home\hans\Gerador-de-posts
.\build_installer.bat
```

O instalador será criado em: `installer_output\GeradordePosts_Installer.exe`

### Método Manual

1. Abra o Inno Setup Compiler
2. Vá em: **File → Open...**
3. Selecione o arquivo: `installer_setup.iss`
4. Clique em: **Build → Compile** (ou pressione F9)
5. Aguarde a compilação
6. O instalador estará em: `installer_output\GeradordePosts_Installer.exe`

## ✨ Recursos do Instalador

O instalador criado inclui:

### Durante a Instalação

- ✅ Assistente em Português
- ✅ Escolha do diretório de instalação
- ✅ Criação automática do arquivo `.env`
- ✅ Opção de inserir a chave da API durante instalação
- ✅ Criação de atalho no Menu Iniciar
- ✅ Opção de criar atalho na Área de Trabalho
- ✅ Opção de executar o programa após instalação

### Após a Instalação

- 📁 Aplicativo instalado em: `C:\Program Files\Gerador de Posts Instagram\`
- 🖼️ Pasta para imagens: `generated_images\`
- ⚙️ Arquivo de configuração: `.env`
- 🔗 Atalhos no Menu Iniciar

### Durante a Desinstalação

- ❓ Pergunta se deseja manter imagens geradas e configurações
- 🗑️ Limpeza completa se optar por remover tudo
- ✅ Remoção dos atalhos automaticamente

## 📝 Personalizar o Instalador (Opcional)

Edite o arquivo `installer_setup.iss` para personalizar:

### Informações Básicas

```pascal
#define MyAppName "Gerador de Posts Instagram"
#define MyAppVersion "1.0"          // Altere a versão aqui
#define MyAppPublisher "Seu Nome"   // Altere seu nome/empresa
```

### Adicionar Ícone Personalizado

1. Crie ou baixe um ícone (.ico)
2. Salve como `icon.ico` na pasta do projeto
3. O instalador usará automaticamente

Se não tiver ícone, comente a linha no .iss:

```pascal
; SetupIconFile=icon.ico
```

### Adicionar Arquivos Extras

Na seção `[Files]`, adicione:

```pascal
Source: "manual.pdf"; DestDir: "{app}"; Flags: ignoreversion
Source: "licenca.txt"; DestDir: "{app}"; Flags: ignoreversion
```

## 🎨 Criar um Ícone para o Aplicativo

### Opção 1: Usar Gerador Online

1. Acesse: https://favicon.io/favicon-converter/
2. Faça upload de uma imagem (PNG/JPG)
3. Baixe o favicon.ico gerado
4. Renomeie para `icon.ico`
5. Coloque na pasta do projeto

### Opção 2: Usar Conversor Local

No Windows, use o IcoFX (gratuito) ou similar.

### Opção 3: Sem Ícone

O instalador funcionará sem ícone, usando o ícone padrão do Windows.

## 🌐 Distribuir o Instalador

Após criar `GeradordePosts_Installer.exe`, você pode:

### Distribuição Direta

- Envie por email
- Compartilhe via Google Drive, Dropbox, etc.
- Hospede em seu site

### Informações para os Usuários

Envie junto com o instalador:

```
📦 GERADOR DE POSTS INSTAGRAM - INSTALADOR
===========================================

Instruções de Instalação:
1. Execute: GeradordePosts_Installer.exe
2. Siga o assistente de instalação
3. Quando solicitado, insira sua chave da API OpenAI
   (ou configure depois no arquivo .env)
4. Conclua a instalação

Requisitos:
- Windows 10 ou superior
- Conexão com internet
- Chave da API OpenAI (obtenha em: https://platform.openai.com/api-keys)

Após Instalação:
- Execute pelo atalho no Menu Iniciar
- Se não configurou a API durante instalação:
  1. Vá em: C:\Program Files\Gerador de Posts Instagram
  2. Edite o arquivo .env
  3. Adicione sua chave da API
```

## 🛠️ Solução de Problemas

### Erro: "Inno Setup não encontrado"

- Certifique-se de instalar o Inno Setup
- Caminho padrão: `C:\Program Files (x86)\Inno Setup 6\`
- Se instalou em outro local, edite `build_installer.bat`

### Erro: "Executável não encontrado"

- Execute primeiro: `pyinstaller --clean GeradordePosts_GUI.spec`
- Verifique se existe: `dist\GeradordePosts_GUI.exe`

### Instalador não executa

- Execute como Administrador
- Desative temporariamente o antivírus
- Verifique se o Windows SmartScreen não bloqueou

### Alterar Local de Instalação Padrão

No arquivo `installer_setup.iss`, altere:

```pascal
DefaultDirName={autopf}\{#MyAppName}
```

Para:

```pascal
DefaultDirName={userdocs}\{#MyAppName}    ; Meus Documentos
; ou
DefaultDirName={userappdata}\{#MyAppName}  ; AppData
```

## 📊 Comparação: EXE vs MSI

| Recurso | Inno Setup (EXE) | MSI (Windows Installer) |
|---------|------------------|-------------------------|
| Facilidade | ⭐⭐⭐⭐⭐ Muito fácil | ⭐⭐ Complexo |
| Gratuito | ✅ Sim | ✅ Sim (WiX Toolset) |
| Customização | ⭐⭐⭐⭐⭐ Completa | ⭐⭐⭐ Moderada |
| Tamanho | Pequeno | Maior |
| GPO Deploy | ❌ Não | ✅ Sim |
| Corporativo | ⭐⭐⭐ OK | ⭐⭐⭐⭐⭐ Preferido |
| Usuários Home | ⭐⭐⭐⭐⭐ Perfeito | ⭐⭐⭐ OK |

**Recomendação:** Para distribuição pessoal ou pequenas empresas, o Inno Setup (EXE) é perfeito!

## 🔐 Se Precisar de MSI Verdadeiro

Se realmente precisar de arquivo .msi (para deploy corporativo com GPO):

### Usar WiX Toolset

1. Baixe WiX: https://wixtoolset.org/
2. Instale o WiX Toolset
3. Eu posso criar um script .wxs para você

**Nota:** WiX é mais complexo e requer conhecimento de XML. Para maioria dos casos, o Inno Setup é suficiente.

## 📞 Suporte

Se tiver problemas:

1. Verifique se seguiu todos os passos
2. Confira os logs do Inno Setup
3. Teste o instalador em uma máquina limpa
4. Verifique permissões de execução

## ✅ Checklist Antes de Distribuir

- [ ] Executável compilado e testado
- [ ] Inno Setup instalado
- [ ] Instalador criado com sucesso
- [ ] Testou instalador em outra máquina
- [ ] Configuração da API funciona
- [ ] Atalhos criados corretamente
- [ ] Desinstalação funciona
- [ ] Documentação para usuários pronta
