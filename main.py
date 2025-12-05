#!/usr/bin/env python3
"""
Gerador de Posts para Instagram
Automatiza a criação de conteúdo com imagens, legendas e hashtags usando OpenAI
"""

import os
import sys
from dotenv import load_dotenv
from openai_service import OpenAIService


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')


def exibir_banner():
    """Exibe o banner do aplicativo"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        📱 GERADOR DE POSTS PARA INSTAGRAM 📱              ║
    ║                                                           ║
    ║           Automação com Inteligência Artificial          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def escolher_tipo_post():
    """
    Solicita ao usuário o tipo de post

    Returns:
        str: Tipo de post escolhido
    """
    print("\n📌 TIPO DE POST")
    print("-" * 50)
    print("1. Feed (Post no feed)")
    print("2. Reel (Vídeo curto)")
    print("3. Stories (História temporária)")
    print("-" * 50)

    while True:
        escolha = input("\n👉 Escolha o tipo de post (1-3): ").strip()

        opcoes = {
            "1": "feed",
            "2": "reel",
            "3": "stories"
        }

        if escolha in opcoes:
            return opcoes[escolha]
        else:
            print("❌ Opção inválida! Digite 1, 2 ou 3.")


def escolher_nicho():
    """
    Solicita ao usuário o nicho do conteúdo

    Returns:
        str: Nicho escolhido
    """
    print("\n🎯 NICHO DO CONTEÚDO")
    print("-" * 50)
    print("Exemplos: Fitness, Moda, Tecnologia, Culinária, Viagens,")
    print("          Marketing Digital, Motivação, Educação, etc.")
    print("-" * 50)

    while True:
        nicho = input("\n👉 Digite o nicho do seu conteúdo: ").strip()

        if len(nicho) >= 3:
            return nicho
        else:
            print("❌ Por favor, digite um nicho válido (mínimo 3 caracteres).")


def escolher_tom():
    """
    Solicita ao usuário o tom da legenda

    Returns:
        str: Tom escolhido
    """
    print("\n🎭 TOM DA LEGENDA")
    print("-" * 50)
    print("1. Sério (Profissional e formal)")
    print("2. Divertido (Animado e alegre)")
    print("3. Engraçado (Humorístico e descontraído)")
    print("4. Inspiracional (Motivador e inspirador)")
    print("5. Educativo (Informativo e didático)")
    print("6. Luxuoso (Sofisticado e premium)")
    print("-" * 50)

    while True:
        escolha = input("\n👉 Escolha o tom da legenda (1-6): ").strip()

        opcoes = {
            "1": "sério",
            "2": "divertido",
            "3": "engraçado",
            "4": "inspiracional",
            "5": "educativo",
            "6": "luxuoso"
        }

        if escolha in opcoes:
            return opcoes[escolha]
        else:
            print("❌ Opção inválida! Digite um número entre 1 e 6.")


def confirmar_dados(tipo_post, nicho, tom):
    """
    Exibe os dados e solicita confirmação

    Args:
        tipo_post (str): Tipo de post
        nicho (str): Nicho
        tom (str): Tom da legenda

    Returns:
        bool: True se confirmado, False caso contrário
    """
    print("\n" + "=" * 50)
    print("📋 CONFIRMAÇÃO DOS DADOS")
    print("=" * 50)
    print(f"📱 Tipo de Post: {tipo_post.upper()}")
    print(f"🎯 Nicho: {nicho}")
    print(f"🎭 Tom: {tom.capitalize()}")
    print("=" * 50)

    confirmacao = input("\n👉 Confirma os dados? (s/n): ").strip().lower()
    return confirmacao == 's' or confirmacao == 'sim'


def exibir_resultado(imagem_path, legenda, hashtags):
    """
    Exibe o resultado final

    Args:
        imagem_path (str): Caminho da imagem gerada
        legenda (str): Legenda gerada
        hashtags (list): Lista de hashtags
    """
    print("\n" + "=" * 70)
    print("🎉 POST GERADO COM SUCESSO!")
    print("=" * 70)

    if imagem_path:
        print(f"\n🖼️  IMAGEM: {imagem_path}")

    if legenda:
        print(f"\n📝 LEGENDA:")
        print("-" * 70)
        print(legenda)
        print("-" * 70)

    if hashtags:
        print(f"\n#️⃣  HASHTAGS ({len(hashtags)}):")
        print("-" * 70)
        print(" ".join(hashtags))
        print("-" * 70)

    print("\n💡 Dica: Copie a legenda e as hashtags para usar no seu post!")
    print("=" * 70)


def salvar_post_completo(tipo_post, nicho, tom, imagem_path, legenda, hashtags):
    """
    Salva todas as informações do post em um arquivo de texto

    Args:
        tipo_post (str): Tipo de post
        nicho (str): Nicho
        tom (str): Tom
        imagem_path (str): Caminho da imagem
        legenda (str): Legenda gerada
        hashtags (list): Lista de hashtags
    """
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_images/post_{tipo_post}_{timestamp}.txt"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("GERADOR DE POSTS PARA INSTAGRAM\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Tipo de Post: {tipo_post.upper()}\n")
            f.write(f"Nicho: {nicho}\n")
            f.write(f"Tom: {tom.capitalize()}\n")
            f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

            f.write("=" * 70 + "\n")
            f.write("IMAGEM\n")
            f.write("=" * 70 + "\n")
            f.write(f"{imagem_path}\n\n")

            f.write("=" * 70 + "\n")
            f.write("LEGENDA\n")
            f.write("=" * 70 + "\n")
            f.write(f"{legenda}\n\n")

            f.write("=" * 70 + "\n")
            f.write(f"HASHTAGS ({len(hashtags)})\n")
            f.write("=" * 70 + "\n")
            f.write(" ".join(hashtags) + "\n\n")

            f.write("=" * 70 + "\n")
            f.write("LEGENDA COMPLETA COM HASHTAGS\n")
            f.write("=" * 70 + "\n")
            f.write(f"{legenda}\n\n")
            f.write(" ".join(hashtags) + "\n")

        print(f"\n💾 Post salvo em: {filename}")

    except Exception as e:
        print(f"\n⚠️  Não foi possível salvar o arquivo: {e}")


def main():
    """Função principal do aplicativo"""

    # Carregar variáveis de ambiente
    load_dotenv()

    limpar_tela()
    exibir_banner()

    # Verificar API Key
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("\n❌ ERRO: Chave da API OpenAI não encontrada!")
        print("\n📝 Instruções:")
        print("1. Copie o arquivo .env.example para .env")
        print("2. Adicione sua chave da API OpenAI no arquivo .env")
        print("3. Execute o programa novamente")
        sys.exit(1)

    # Inicializar serviço OpenAI
    try:
        openai_service = OpenAIService(api_key)
        print("✅ Conexão com OpenAI estabelecida com sucesso!\n")
    except Exception as e:
        print(f"\n❌ Erro ao conectar com OpenAI: {e}")
        sys.exit(1)

    # Loop principal
    while True:
        # Coletar informações do usuário
        tipo_post = escolher_tipo_post()
        nicho = escolher_nicho()
        tom = escolher_tom()

        # Confirmar dados
        if not confirmar_dados(tipo_post, nicho, tom):
            print("\n🔄 Vamos recomeçar...")
            continue

        # Gerar conteúdo
        print("\n" + "=" * 70)
        print("🚀 GERANDO SEU CONTEÚDO...")
        print("=" * 70)
        print("\n⏳ Isso pode levar alguns segundos. Por favor, aguarde...")

        try:
            # Gerar imagem
            imagem_path = openai_service.gerar_imagem(tipo_post, nicho, tom)

            # Gerar legenda
            legenda = openai_service.gerar_legenda(tipo_post, nicho, tom)

            # Gerar hashtags
            hashtags = openai_service.gerar_hashtags(nicho, tipo_post)

            # Exibir resultado
            exibir_resultado(imagem_path, legenda, hashtags)

            # Salvar post completo
            if imagem_path and legenda and hashtags:
                salvar_post_completo(tipo_post, nicho, tom, imagem_path, legenda, hashtags)

        except Exception as e:
            print(f"\n❌ Erro ao gerar conteúdo: {e}")
            print("⚠️  Por favor, verifique sua conexão e tente novamente.")

        # Perguntar se deseja gerar outro post
        print("\n" + "=" * 70)
        continuar = input("\n👉 Deseja gerar outro post? (s/n): ").strip().lower()

        if continuar != 's' and continuar != 'sim':
            print("\n👋 Obrigado por usar o Gerador de Posts para Instagram!")
            print("💡 Não se esqueça de seguir as melhores práticas do Instagram!")
            print("\n✨ Até a próxima!\n")
            break

        limpar_tela()
        exibir_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
        sys.exit(0)
