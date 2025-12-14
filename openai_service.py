"""
Serviço para integração com OpenAI API
Responsável pela geração de imagens, legendas e hashtags
"""

import os
import requests
from openai import OpenAI
from datetime import datetime


class OpenAIService:
    def __init__(self, api_key):
        """
        Inicializa o serviço OpenAI

        Args:
            api_key (str): Chave da API OpenAI
        """
        self.client = OpenAI(api_key=api_key)
        self.output_dir = "generated_images"

        # Criar diretório de saída se não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def gerar_imagem(self, tipo_post, nicho, tom, estilo="realista"):
        """
        Gera uma imagem usando DALL-E 3

        Args:
            tipo_post (str): Tipo de post (feed, reel, stories)
            nicho (str): Nicho do conteúdo
            tom (str): Tom da comunicação
            estilo (str): Estilo da imagem (realista ou artistico)

        Returns:
            str: Caminho do arquivo da imagem gerada
        """
        # Definir dimensões baseado no tipo de post
        dimensoes = {
            "feed": "1024x1024",      # Post quadrado
            "reel": "1024x1792",      # Formato vertical 9:16
            "stories": "1024x1792"    # Formato vertical 9:16
        }

        size = dimensoes.get(tipo_post, "1024x1024")

        # Criar prompt para geração de imagem
        prompt = self._criar_prompt_imagem(nicho, tom, tipo_post, estilo)

        print(f"\n🎨 Gerando imagem para {tipo_post}...")
        print(f"📝 Prompt: {prompt[:100]}...")

        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

            # Baixar e salvar a imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/{tipo_post}_{nicho.replace(' ', '_')}_{timestamp}.png"

            img_data = requests.get(image_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            print(f"✅ Imagem salva em: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Erro ao gerar imagem: {e}")
            return None

    def gerar_legenda(self, tipo_post, nicho, tom):
        """
        Gera uma legenda para o post usando GPT-4

        Args:
            tipo_post (str): Tipo de post (feed, reel, stories)
            nicho (str): Nicho do conteúdo
            tom (str): Tom da comunicação

        Returns:
            str: Legenda gerada
        """
        print(f"\n✍️  Gerando legenda com tom {tom}...")

        prompt = self._criar_prompt_legenda(tipo_post, nicho, tom)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um especialista em marketing digital e copywriting para Instagram. Crie legendas engajadoras e otimizadas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )

            legenda = response.choices[0].message.content.strip()
            print("✅ Legenda gerada com sucesso!")
            return legenda

        except Exception as e:
            print(f"❌ Erro ao gerar legenda: {e}")
            return None

    def gerar_hashtags(self, nicho, tipo_post):
        """
        Gera entre 10 e 15 hashtags relevantes

        Args:
            nicho (str): Nicho do conteúdo
            tipo_post (str): Tipo de post

        Returns:
            list: Lista de hashtags
        """
        print(f"\n#️⃣  Gerando hashtags para o nicho '{nicho}'...")

        prompt = f"""
        Gere exatamente 12 hashtags relevantes e estratégicas para um post de Instagram sobre {nicho}.

        Tipo de post: {tipo_post}

        As hashtags devem incluir:
        - 3-4 hashtags populares (alto volume de busca)
        - 4-5 hashtags de médio alcance (nicho específico)
        - 3-4 hashtags de baixo volume (bem específicas)

        Retorne APENAS as hashtags, uma por linha, sem numeração ou explicações.
        Formato: #exemplo
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um especialista em estratégia de hashtags para Instagram."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [linha.strip() for linha in hashtags_text.split('\n') if linha.strip().startswith('#')]

            # Garantir que temos entre 10 e 15 hashtags
            if len(hashtags) < 10:
                print("⚠️  Menos de 10 hashtags geradas, gerando mais...")
                return self.gerar_hashtags(nicho, tipo_post)

            hashtags = hashtags[:15]  # Limitar a 15

            print(f"✅ {len(hashtags)} hashtags geradas com sucesso!")
            return hashtags

        except Exception as e:
            print(f"❌ Erro ao gerar hashtags: {e}")
            return []

    def _criar_prompt_imagem(self, nicho, tom, tipo_post, estilo_imagem="realista"):
        """Cria prompt otimizado para geração de imagem"""

        estilos_tom = {
            "sério": "professional, clean, minimalist, corporate style",
            "divertido": "colorful, vibrant, playful, energetic style",
            "engraçado": "humorous, cartoon-like, fun, lighthearted style",
            "inspiracional": "inspiring, uplifting, dreamy, motivational style",
            "educativo": "clear, informative, educational, illustrative style",
            "luxuoso": "elegant, premium, sophisticated, high-end style"
        }

        estilo_tom_texto = estilos_tom.get(tom.lower(), "modern, engaging style")

        tipo_contexto = {
            "feed": "Instagram feed post",
            "reel": "Instagram Reel thumbnail",
            "stories": "Instagram Stories"
        }

        contexto = tipo_contexto.get(tipo_post, "Instagram post")

        # Definir estilo de renderização baseado na escolha do usuário
        if estilo_imagem == "realista":
            estilo_render = """
            Ultra-realistic, high-definition photography style.
            Shot with professional camera, perfect lighting, sharp focus.
            Photorealistic, hyper-detailed, 8K quality, RAW photo quality.
            Natural colors, professional composition, magazine-quality photography.
            """
        else:  # artistico
            estilo_render = """
            Artistic illustration, creative design, digital art style.
            Vibrant colors, artistic interpretation, stylized composition.
            Modern graphic design, creative illustration, artistic rendering.
            Unique visual style, creative expression, designer quality.
            """

        prompt = f"""
        Create a visually stunning image for {contexto} about {nicho}.

        Rendering Style: {estilo_render}

        Mood/Tone: {estilo_tom_texto}

        The image should be eye-catching, professional, and perfect for social media.
        No text or watermarks in the image.
        High quality composition.
        """

        return prompt

    def _criar_prompt_legenda(self, tipo_post, nicho, tom):
        """Cria prompt otimizado para geração de legenda"""

        tamanhos = {
            "feed": "uma legenda completa de 2-3 parágrafos",
            "reel": "uma legenda curta e impactante de 1-2 parágrafos",
            "stories": "uma legenda muito breve e direta (máximo 2-3 linhas)"
        }

        tamanho = tamanhos.get(tipo_post, "uma legenda apropriada")

        prompt = f"""
        Crie {tamanho} para um post de Instagram do tipo {tipo_post} sobre o nicho: {nicho}.

        Tom da legenda: {tom}

        Requisitos:
        - Seja autêntico e engajador
        - Use emojis estrategicamente (mas sem exageros)
        - Inclua uma chamada para ação (CTA) no final
        - NÃO inclua hashtags (elas serão adicionadas separadamente)
        - Mantenha o tom {tom} durante toda a legenda
        - Para {tipo_post}, ajuste o tamanho apropriadamente

        Retorne APENAS a legenda, sem títulos ou explicações adicionais.
        """

        return prompt
