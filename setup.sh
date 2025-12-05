#!/bin/bash

echo "=========================================="
echo "  INSTALAÇÃO - GERADOR DE POSTS INSTAGRAM"
echo "=========================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "✅ Ambiente virtual criado com sucesso!"
else
    echo "❌ Erro ao criar ambiente virtual"
    exit 1
fi

echo ""

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

echo ""

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo de configuração..."
    cp .env.example .env
    echo "✅ Arquivo .env criado!"
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua chave da API OpenAI"
    echo ""
else
    echo "ℹ️  Arquivo .env já existe"
    echo ""
fi

# Criar diretório para imagens geradas
if [ ! -d "generated_images" ]; then
    mkdir generated_images
    echo "✅ Diretório 'generated_images' criado!"
fi

echo ""
echo "=========================================="
echo "  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Edite o arquivo .env e adicione sua API Key da OpenAI:"
echo "   nano .env"
echo ""
echo "2. Ative o ambiente virtual:"
echo "   source venv/bin/activate"
echo ""
echo "3. Execute a aplicação:"
echo "   python main.py"
echo ""
echo "=========================================="
