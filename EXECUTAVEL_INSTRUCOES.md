# 🎯 Como Criar o Executável (.EXE)

## 📋 Pré-requisitos

- Windows 10/11
- Python 3.8+ instalado
- Conexão com internet

---

## 🚀 Passo a Passo

### **Método 1: Script Automático (RECOMENDADO)**

1. **Duplo clique em:** `build_exe.bat`
2. **Aguarde:** 5-10 minutos (PyInstaller compila tudo)
3. **Pronto!** O executável estará em: `dist\Instagram_Post_Generator.exe`

---

### **Método 2: Manual via PowerShell**

```powershell
# 1. Instalar PyInstaller
pip install pyinstaller

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar executável
pyinstaller Instagram_Post_Generator.spec

# 4. Copiar .env.example para dist
copy .env.example dist\.env.example
```

---

## 📦 Estrutura Após Build

```
dist/
├── Instagram_Post_Generator.exe  ← EXECUTÁVEL
└── .env.example                  ← Configure suas chaves aqui
```

---

## ⚙️ Configurar e Executar

### **1. Configure as Chaves de API**

Na pasta `dist\`:
```bash
# Renomeie .env.example para .env
ren .env.example .env

# Abra .env no Notepad e configure:
OPENAI_API_KEY=sk-sua_chave_aqui
REPLICATE_API_TOKEN=r8_sua_chave_aqui
```

### **2. Execute**

Duplo clique em: `Instagram_Post_Generator.exe`

---

## 📊 Tamanho do Executável

- **Executável:** ~80-120 MB
- **Motivo:** Contém Python + todas as bibliotecas embutidas
- **Vantagem:** Não precisa instalar Python no PC destino

---

## 🔧 Resolver Problemas

### **Erro: "VCRUNTIME140.dll não encontrado"**
- Instale: https://aka.ms/vs/17/release/vc_redist.x64.exe

### **Antivírus bloqueia o executável**
- Normal para executáveis criados com PyInstaller
- Adicione exceção no antivírus ou
- Execute como administrador

### **App não abre**
- Verifique se `.env` está na mesma pasta do .exe
- Verifique se as chaves de API estão corretas

---

## 📤 Distribuir o Executável

Para enviar para outras pessoas:

1. **Copie a pasta `dist\` completa**
2. **Inclua:**
   - `Instagram_Post_Generator.exe`
   - `.env.example` (para elas configurarem)
3. **Instrua:**
   - Renomear `.env.example` para `.env`
   - Configurar chaves de API
   - Executar o .exe

---

## ✅ Pronto!

Após executar `build_exe.bat`, você terá um executável standalone que roda em qualquer Windows sem precisar instalar Python!

**Tamanho final:** ~100 MB
**Tempo de build:** 5-10 minutos
**Compatibilidade:** Windows 10/11 (64-bit)

---

**Desenvolvido por Integrius Automações • 2025**
