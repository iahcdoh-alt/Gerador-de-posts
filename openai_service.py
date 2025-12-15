"""
Serviço para integração com APIs de geração de conteúdo
Suporta OpenAI (DALL-E, GPT-4) e Replicate (Flux.1)
"""

import os
import requests
from openai import OpenAI
import replicate
from datetime import datetime


class OpenAIService:
    def __init__(self, api_key, replicate_key=None, provider="replicate"):
        """
        Inicializa o serviço de geração

        Args:
            api_key (str): Chave da API OpenAI (para texto)
            replicate_key (str): Chave da API Replicate (para imagens)
            provider (str): Provedor de imagens: "openai" ou "replicate"
        """
        self.client = OpenAI(api_key=api_key)
        self.replicate_key = replicate_key
        self.provider = provider
        self.output_dir = "generated_images"

        # Configurar Replicate se disponível
        if replicate_key:
            os.environ["REPLICATE_API_TOKEN"] = replicate_key

        # Criar diretório de saída se não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def gerar_imagem(self, tipo_post, nicho, tom, estilo="realista"):
        """
        Gera uma imagem usando o provedor configurado (Replicate Flux.1 ou OpenAI DALL-E)

        Args:
            tipo_post (str): Tipo de post (feed, reel, stories)
            nicho (str): Nicho do conteúdo
            tom (str): Tom da comunicação
            estilo (str): Estilo da imagem (realista ou artistico)

        Returns:
            str: Caminho do arquivo da imagem gerada
        """
        if self.provider == "replicate" and self.replicate_key:
            return self._gerar_imagem_replicate(tipo_post, nicho, tom, estilo)
        else:
            return self._gerar_imagem_openai(tipo_post, nicho, tom, estilo)

    def _gerar_imagem_replicate(self, tipo_post, nicho, tom, estilo):
        """Gera imagem usando Replicate Flux.1"""
        # Definir dimensões baseado no tipo de post
        dimensoes = {
            "feed": {"width": 1024, "height": 1024},      # Post quadrado
            "reel": {"width": 1024, "height": 1792},      # Formato vertical 9:16
            "stories": {"width": 1024, "height": 1792}    # Formato vertical 9:16
        }

        dims = dimensoes.get(tipo_post, {"width": 1024, "height": 1024})

        # Criar prompt para geração de imagem
        prompt = self._criar_prompt_imagem(nicho, tom, tipo_post, estilo)

        print(f"\n🎨 Gerando imagem com Flux.1 para {tipo_post}...")
        print(f"📝 Prompt: {prompt[:100]}...")

        try:
            output = replicate.run(
                "black-forest-labs/flux-1.1-pro",
                input={
                    "prompt": prompt,
                    "width": dims["width"],
                    "height": dims["height"],
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                }
            )

            # Output é uma URL da imagem
            image_url = output if isinstance(output, str) else output[0]

            # Baixar e salvar a imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/{tipo_post}_{nicho.replace(' ', '_')}_{timestamp}.png"

            img_data = requests.get(image_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            print(f"✅ Imagem Flux.1 salva em: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Erro ao gerar imagem com Flux.1: {e}")
            raise Exception(f"Erro ao conectar com Replicate: {str(e)}")

    def _gerar_imagem_openai(self, tipo_post, nicho, tom, estilo):
        """Gera imagem usando OpenAI DALL-E 3"""
        # Definir dimensões baseado no tipo de post
        dimensoes = {
            "feed": "1024x1024",      # Post quadrado
            "reel": "1024x1792",      # Formato vertical 9:16
            "stories": "1024x1792"    # Formato vertical 9:16
        }

        size = dimensoes.get(tipo_post, "1024x1024")

        # Criar prompt para geração de imagem
        prompt = self._criar_prompt_imagem(nicho, tom, tipo_post, estilo)

        print(f"\n🎨 Gerando imagem com DALL-E 3 para {tipo_post}...")
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

            print(f"✅ Imagem DALL-E salva em: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Erro ao gerar imagem com DALL-E: {e}")
            raise Exception(f"Erro ao conectar com OpenAI: {str(e)}")

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

    # ===== MÉTODOS ESPECIALIZADOS PARA MARKETING PROFISSIONAL =====

    def gerar_imagem_marketing(self, tipo_post, nicho, tema, tom, formato="normal"):
        """
        Gera imagem com foco em marketing profissional
        Todas as imagens são fotográficas hiper-realistas
        """
        # Definir dimensões
        if formato == "bomdia" or tipo_post == "feed":
            dimensoes = {"width": 1024, "height": 1024}  # 1:1
        else:
            dimensoes = {
                "feed": {"width": 1024, "height": 1024},
                "reel": {"width": 1024, "height": 1792},
                "stories": {"width": 1024, "height": 1792}
            }.get(tipo_post, {"width": 1024, "height": 1024})

        # Criar prompt profissional de fotografia
        prompt = self._criar_prompt_fotografia_profissional(nicho, tema, tom, tipo_post)

        print(f"\n📸 Gerando imagem hiper-realista com Flux.1...")
        print(f"📝 Tema: {tema}")

        try:
            output = replicate.run(
                "black-forest-labs/flux-1.1-pro",
                input={
                    "prompt": prompt,
                    "width": dimensoes["width"],
                    "height": dimensoes["height"],
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                }
            )

            image_url = output if isinstance(output, str) else output[0]

            # Salvar imagem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/{tipo_post}_{nicho.replace(' ', '_')}_{timestamp}.png"

            img_data = requests.get(image_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            print(f"✅ Imagem profissional salva: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Erro ao gerar imagem: {e}")
            raise Exception(f"Erro ao conectar com Replicate: {str(e)}")

    def gerar_legenda_marketing(self, tipo_post, nicho, tema, tom, cta):
        """
        Gera legenda profissional com perfil de gerente de marketing
        """
        print(f"\n✍️  Gerando legenda profissional...")

        tamanhos = {
            "feed": "2-3 parágrafos bem estruturados",
            "reel": "1-2 parágrafos curtos e impactantes",
            "stories": "2-3 linhas diretas e objetivas"
        }

        tamanho = tamanhos.get(tipo_post, "tamanho apropriado")

        ctas_texto = {
            "comentar": "Peça para comentarem com suas opiniões ou experiências",
            "curtir": "Incentive a curtir se concordam ou se foi útil",
            "compartilhar": "Peça para compartilhar com alguém que precisa ver isso",
            "seguir": "Convide para seguir para mais conteúdo valioso",
            "salvar": "Sugira salvar o post para consultar depois",
            "link_bio": "Direcione para o link na bio para mais informações"
        }

        cta_instrucao = ctas_texto.get(cta, "Inclua uma boa chamada para ação")

        prompt = f"""
        Você é um GERENTE DE MARKETING ESPECIALIZADO EM REDES SOCIAIS com vasta experiência em criar conteúdo viral e engajador para Instagram.

        Crie uma legenda profissional de {tamanho} para um post do tipo {tipo_post}.

        INFORMAÇÕES DO POST:
        - Nicho: {nicho}
        - Tema específico: {tema}
        - Tom: {tom}

        DIRETRIZES PROFISSIONAIS:
        1. ABERTURA IMPACTANTE: Comece com algo que prenda a atenção nos primeiros segundos
        2. VALOR REAL: Forneça informações úteis, insights ou inspiração genuína
        3. STORYTELLING: Se apropriado, use uma narrativa envolvente
        4. CONEXÃO EMOCIONAL: Fale diretamente com seu público, crie empatia
        5. EMOJIS ESTRATÉGICOS: Use 3-5 emojis bem posicionados (não exagere)
        6. QUEBRAS DE LINHA: Use espaçamento para facilitar leitura
        7. CALL TO ACTION: {cta_instrucao}

        IMPORTANTE:
        - NÃO inclua hashtags (serão adicionadas separadamente)
        - Mantenha tom {tom} mas sempre profissional
        - Foque em INFORMAR e ATRAIR SEGUIDORES (objetivo principal)
        - Seja autêntico, evite clichês genéricos

        Retorne APENAS a legenda pronta para publicação.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um gerente de marketing digital sênior, especialista em redes sociais e copywriting para Instagram. Seu objetivo é criar conteúdo que informa, engaja e atrai seguidores de forma autêntica e profissional."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=600
            )

            legenda = response.choices[0].message.content.strip()
            print("✅ Legenda profissional gerada!")
            return legenda

        except Exception as e:
            print(f"❌ Erro ao gerar legenda: {e}")
            raise

    def gerar_hashtags_marketing(self, nicho, tipo_post):
        """
        Gera hashtags estratégicas com foco em marketing
        """
        print(f"\n#️⃣  Gerando hashtags estratégicas...")

        prompt = f"""
        Como especialista em estratégia de hashtags para Instagram, crie exatamente 12 hashtags ESTRATÉGICAS para um post sobre {nicho}.

        Tipo de post: {tipo_post}

        ESTRATÉGIA DE DISTRIBUIÇÃO:
        - 3 hashtags de ALTO VOLUME (100k+ posts) - para alcance máximo
        - 5 hashtags de MÉDIO VOLUME (10k-100k posts) - nicho específico
        - 4 hashtags de BAIXO VOLUME (<10k posts) - públicos muito segmentados

        CRITÉRIOS:
        - Todas em português do Brasil
        - Relevantes para o nicho {nicho}
        - Mix de hashtags gerais e específicas
        - Evite hashtags banidas ou com spam
        - Foco em engajamento genuíno

        Retorne APENAS as hashtags, uma por linha, formato: #exemplo
        Sem numeração, sem explicações, sem categorias.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em estratégia de hashtags do Instagram com conhecimento profundo sobre algoritmo e engajamento."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [linha.strip() for linha in hashtags_text.split('\n') if linha.strip().startswith('#')]

            if len(hashtags) < 10:
                print("⚠️  Regenerando hashtags...")
                return self.gerar_hashtags_marketing(nicho, tipo_post)

            hashtags = hashtags[:12]
            print(f"✅ {len(hashtags)} hashtags estratégicas geradas!")
            return hashtags

        except Exception as e:
            print(f"❌ Erro ao gerar hashtags: {e}")
            return []

    # ===== MÉTODOS PARA BOM DIA MOTIVACIONAL =====

    def gerar_imagem_bomdia(self, categoria, subtema=""):
        """
        Gera imagem motivacional para Bom Dia (formato 1:1)
        Sempre fotografia hiper-realista inspiradora
        """
        print(f"\n🌅 Gerando imagem motivacional...")

        prompt = self._criar_prompt_bomdia_imagem(categoria, subtema)

        try:
            output = replicate.run(
                "black-forest-labs/flux-1.1-pro",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024,  # Sempre 1:1
                    "num_inference_steps": 28,
                    "guidance_scale": 3.5
                }
            )

            image_url = output if isinstance(output, str) else output[0]

            # Salvar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/bomdia_{categoria}_{timestamp}.png"

            img_data = requests.get(image_url).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            print(f"✅ Imagem motivacional salva: {filename}")
            return filename

        except Exception as e:
            print(f"❌ Erro ao gerar imagem: {e}")
            raise

    def gerar_mensagem_bomdia(self, categoria, subtema=""):
        """
        Gera mensagem motivacional de Bom Dia
        """
        print(f"\n💬 Gerando mensagem motivacional...")

        prompt = f"""
        Você é um GERENTE DE MARKETING especializado em conteúdo motivacional e inspirador para redes sociais.

        Crie uma mensagem de BOM DIA motivacional e inspiradora.

        CATEGORIA: {categoria}
        {"SUBTEMA: " + subtema if subtema else ""}

        DIRETRIZES:
        1. Inicie com "Bom dia" de forma criativa
        2. Mensagem CURTA: 2-4 parágrafos no máximo
        3. Seja GENUINAMENTE inspirador, não clichê
        4. Use 2-4 emojis estrategicamente posicionados
        5. Termine com uma frase de impacto positivo
        6. Tom: caloroso, motivador, mas não exagerado
        7. Deve fazer a pessoa querer começar o dia bem

        FOCO: Criar conexão emocional genuína e inspirar ação positiva.

        NÃO inclua hashtags.
        Retorne APENAS a mensagem pronta.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em criar mensagens motivacionais autênticas e inspiradoras que realmente tocam as pessoas e geram engajamento genuíno."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,
                max_tokens=400
            )

            mensagem = response.choices[0].message.content.strip()
            print("✅ Mensagem motivacional gerada!")
            return mensagem

        except Exception as e:
            print(f"❌ Erro ao gerar mensagem: {e}")
            raise

    def gerar_hashtags_bomdia(self, categoria):
        """
        Gera hashtags para posts de Bom Dia
        """
        print(f"\n#️⃣  Gerando hashtags motivacionais...")

        prompt = f"""
        Crie exatamente 12 hashtags para um post de BOM DIA MOTIVACIONAL sobre {categoria}.

        REQUISITOS:
        - Todas em português do Brasil
        - Mix de hashtags motivacionais gerais e específicas
        - Incluir hashtags relacionadas a "bom dia", "motivação", "{categoria}"
        - 3 de alto volume, 5 médio, 4 baixo volume

        Retorne APENAS as hashtags, uma por linha, formato: #exemplo
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é especialista em hashtags motivacionais."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            hashtags_text = response.choices[0].message.content.strip()
            hashtags = [linha.strip() for linha in hashtags_text.split('\n') if linha.strip().startswith('#')]

            if len(hashtags) < 10:
                return self.gerar_hashtags_bomdia(categoria)

            hashtags = hashtags[:12]
            print(f"✅ {len(hashtags)} hashtags geradas!")
            return hashtags

        except Exception as e:
            print(f"❌ Erro: {e}")
            return []

    # ===== PROMPTS PROFISSIONAIS DE FOTOGRAFIA =====

    def _criar_prompt_fotografia_profissional(self, nicho, tema, tom, tipo_post):
        """
        Cria prompt para fotografia hiper-realista profissional
        """
        tons_visuales = {
            "profissional": "clean corporate aesthetic, minimalist professional setting, business environment",
            "inspiracional": "uplifting atmosphere, dreamy golden hour lighting, aspirational lifestyle",
            "educativo": "clear and focused composition, well-lit educational setting, informative visual",
            "entusiasta": "vibrant energetic colors, dynamic composition, exciting atmosphere",
            "premium": "luxury aesthetic, elegant composition, sophisticated high-end styling"
        }

        tom_visual = tons_visuales.get(tom, "modern professional aesthetic")

        prompt = f"""
        ULTRA-REALISTIC PROFESSIONAL PHOTOGRAPHY

        Subject: {tema} related to {nicho}
        Style: {tom_visual}

        CAMERA & TECHNICAL SPECS:
        - Shot on professional DSLR camera (Canon EOS R5 or Sony A7R IV)
        - Prime lens with shallow depth of field (f/1.8-2.8)
        - 8K ultra high resolution, RAW quality
        - Perfect sharp focus on main subject
        - Natural bokeh background blur

        LIGHTING (CRITICAL):
        - Professional studio lighting OR perfect natural golden hour light
        - Soft diffused key light, subtle fill light
        - Professional color grading and color correction
        - Proper exposure, perfect white balance
        - Cinematic lighting techniques

        COMPOSITION:
        - Rule of thirds, professional framing
        - Magazine-quality composition
        - Clean, uncluttered background
        - Professional art direction

        PHOTOGRAPHY STYLE:
        - Hyper-realistic, photojournalistic quality
        - Natural colors, authentic feel
        - Professional commercial photography standard
        - Could be published in high-end magazines

        MOOD: {tom_visual}

        IMPORTANT:
        - NO text, NO watermarks, NO graphics overlay
        - 100% photographic realism
        - Looks like a real professional photograph
        - NOT illustration, NOT digital art, NOT 3D render
        """

        return prompt

    def _criar_prompt_bomdia_imagem(self, categoria, subtema):
        """
        Cria prompt para imagens motivacionais de Bom Dia
        """
        cenarios = {
            "sucesso": "golden sunrise over mountain peak, achievement metaphor, inspiring vista",
            "forca": "powerful ocean waves, strong tree, resilience imagery",
            "positividade": "bright sunny morning, blooming flowers, joyful nature scene",
            "foco": "clear path forward, focused beam of light, zen meditation setting",
            "amor_proprio": "peaceful self-care scene, cozy morning routine, self-love imagery",
            "metas": "arrow hitting target, clear road ahead, achievement visualization",
            "esperanca": "rainbow after storm, new dawn, fresh beginning",
            "paz": "calm lake reflection, peaceful zen garden, tranquil morning"
        }

        cenario = cenarios.get(categoria, "inspiring sunrise scene")

        prompt = f"""
        ULTRA-REALISTIC INSPIRATIONAL MORNING PHOTOGRAPHY

        Scene: {cenario}
        {f"Additional theme: {subtema}" if subtema else ""}

        PHOTOGRAPHY REQUIREMENTS:
        - Shot during GOLDEN HOUR (early morning sunrise)
        - Professional DSLR camera, 8K resolution
        - Perfect natural lighting, warm tones
        - Photorealistic, magazine quality
        - Inspiring and uplifting composition

        LIGHTING:
        - Warm golden morning light
        - Soft sunbeams, natural glow
        - Perfect color temperature for morning
        - Cinematic quality lighting

        MOOD:
        - Inspirational and uplifting
        - Peaceful yet energizing
        - Hope and positivity
        - Perfect for morning motivation

        COMPOSITION:
        - Wide inspiring vista OR intimate meaningful detail
        - Professional rule of thirds
        - Natural, authentic, not staged
        - Could be National Geographic cover

        CRITICAL:
        - 100% photographic realism
        - NO text, NO graphics, NO overlays
        - Real photograph quality
        - Inspiring but authentic, not cheesy

        Perfect for Instagram motivational post.
        """

        return prompt
