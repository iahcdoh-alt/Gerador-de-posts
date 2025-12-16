#!/usr/bin/env python3
"""
Gerador Profissional de Posts para Instagram
Versão Moderna com ttkbootstrap - Dark/Light Mode
Desenvolvido por Integrius Automações - 2025
"""

import os
import sys
import threading
import json
from datetime import datetime
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.toast import ToastNotification
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from dotenv import load_dotenv

from openai_service import OpenAIService


class InstagramPostGenerator(ttk.Window):
    """
    Aplicação principal do Gerador de Posts para Instagram
    Interface moderna com Dark/Light Mode e duas abas de funcionalidades
    """

    def __init__(self):
        super().__init__(themename="darkly")  # Tema inicial: dark

        # Configurações da janela principal
        self.title("Gerador Profissional de Posts - Instagram")
        self.geometry("1400x900")
        self.minsize(1200, 800)

        # Variáveis de controle
        self.current_theme = "darkly"
        self.openai_service = None
        self.is_generating = False

        # Variáveis de geração - Aba 1 (Posts Normais)
        self.tipo_post_normal = ttk.StringVar(value="feed")
        self.nicho_normal = ttk.StringVar()
        self.tema_post_normal = ttk.StringVar()
        self.tom_normal = ttk.StringVar(value="profissional")
        self.cta_normal = ttk.StringVar(value="comentar")

        # Variáveis de geração - Aba 2 (Bom Dia Motivacional)
        self.categoria_bomdia = ttk.StringVar(value="sucesso")
        self.subtema_bomdia = ttk.StringVar()

        # Resultados
        self.imagem_gerada = None
        self.legenda_gerada = ""
        self.hashtags_geradas = []
        self.current_tab_name = ""

        # Inicializar serviços
        self.inicializar_servicos()

        # Criar interface
        self.criar_interface()

        # Centralizar janela
        self.centralizar_janela()

    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def inicializar_servicos(self):
        """Inicializa conexões com APIs"""
        load_dotenv()

        # Verificar chaves de API
        openai_key = os.getenv("OPENAI_API_KEY")
        replicate_key = os.getenv("REPLICATE_API_TOKEN")

        if not openai_key or openai_key == "sua_chave_api_aqui":
            messagebox.showerror(
                "Configuração Necessária",
                "Chave da API OpenAI não encontrada!\n\n"
                "Por favor:\n"
                "1. Configure o arquivo .env\n"
                "2. Adicione OPENAI_API_KEY=sua_chave\n"
                "3. Reinicie a aplicação"
            )
            sys.exit(1)

        if not replicate_key or replicate_key == "sua_chave_replicate_aqui":
            messagebox.showerror(
                "Configuração Necessária",
                "Chave da API Replicate não encontrada!\n\n"
                "Por favor:\n"
                "1. Configure o arquivo .env\n"
                "2. Adicione REPLICATE_API_TOKEN=sua_chave\n"
                "3. Reinicie a aplicação"
            )
            sys.exit(1)

        try:
            self.openai_service = OpenAIService(
                api_key=openai_key,
                replicate_key=replicate_key,
                provider="replicate"
            )
        except Exception as e:
            messagebox.showerror(
                "Erro de Conexão",
                f"Erro ao inicializar serviços:\n{str(e)}"
            )
            sys.exit(1)

    def criar_interface(self):
        """Cria toda a interface gráfica"""

        # ===== HEADER =====
        header = ttk.Frame(self, bootstyle="dark")
        header.pack(fill=X, pady=0)

        # Título principal
        title_frame = ttk.Frame(header, bootstyle="dark")
        title_frame.pack(fill=X, padx=20, pady=(15, 5))

        ttk.Label(
            title_frame,
            text="📱 GERADOR PROFISSIONAL DE POSTS PARA INSTAGRAM",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-dark"
        ).pack()

        # Subtítulo
        ttk.Label(
            title_frame,
            text="Imagens Hiper-Realistas com Flux.1 • Textos Profissionais com OpenAI GPT-4",
            font=("Segoe UI", 11),
            bootstyle="secondary"
        ).pack(pady=(5, 10))

        # Barra de controles
        controls_frame = ttk.Frame(header, bootstyle="dark")
        controls_frame.pack(fill=X, padx=20, pady=(0, 15))

        # Botão Dark/Light Mode
        self.theme_btn = ttk.Button(
            controls_frame,
            text="☀️ Modo Claro",
            command=self.alternar_tema,
            bootstyle="warning-outline",
            width=15
        )
        self.theme_btn.pack(side=LEFT, padx=(0, 10))

        # Status de conexão
        status_frame = ttk.Frame(controls_frame, bootstyle="dark")
        status_frame.pack(side=RIGHT)

        ttk.Label(
            status_frame,
            text="✓ OpenAI conectado",
            font=("Segoe UI", 9),
            bootstyle="success"
        ).pack(side=LEFT, padx=5)

        ttk.Label(
            status_frame,
            text="✓ Flux.1 conectado",
            font=("Segoe UI", 9),
            bootstyle="success"
        ).pack(side=LEFT, padx=5)

        # ===== NOTEBOOK (ABAS) =====
        self.notebook = ttk.Notebook(self, bootstyle="dark")
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Criar abas
        self.criar_aba_posts_normais()
        self.criar_aba_bom_dia()

        # ===== FOOTER =====
        footer = ttk.Frame(self, bootstyle="dark")
        footer.pack(fill=X, side=BOTTOM)

        ttk.Label(
            footer,
            text="Desenvolvido por Integrius Automações • Copyright 2025 • Todos os direitos reservados",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(pady=12)

    def criar_aba_posts_normais(self):
        """Cria a aba de posts normais para Instagram"""

        # Frame principal da aba
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="📸 Posts Normais", sticky=NSEW)

        # Container principal com 2 colunas
        container = ttk.Frame(tab1)
        container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # ===== COLUNA ESQUERDA - Formulário =====
        left_frame = ttk.Labelframe(
            container,
            text="⚙️ Configurações do Post",
            bootstyle="primary",
            padding=15
        )
        left_frame.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))

        # Scrollable frame
        scroll_left = ScrolledFrame(left_frame, autohide=True)
        scroll_left.pack(fill=BOTH, expand=YES)

        # Tipo de Post
        ttk.Label(
            scroll_left,
            text="📌 Tipo de Post",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(5, 8))

        tipos = [
            ("📸 Feed (1080x1080 - Post Quadrado)", "feed"),
            ("🎥 Reel (1080x1920 - Vertical 9:16)", "reel"),
            ("📱 Stories (1080x1920 - História)", "stories")
        ]

        for texto, valor in tipos:
            ttk.Radiobutton(
                scroll_left,
                text=texto,
                variable=self.tipo_post_normal,
                value=valor,
                bootstyle="primary"
            ).pack(anchor=W, pady=3, padx=10)

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Nicho
        ttk.Label(
            scroll_left,
            text="🎯 Nicho/Segmento",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(0, 8))

        ttk.Entry(
            scroll_left,
            textvariable=self.nicho_normal,
            font=("Segoe UI", 11),
            bootstyle="primary"
        ).pack(fill=X, pady=(0, 5), ipady=8)

        ttk.Label(
            scroll_left,
            text="Ex: Fitness, Tecnologia, Moda, Gastronomia, Finanças...",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(anchor=W, pady=(0, 10))

        # Tema Específico
        ttk.Label(
            scroll_left,
            text="💡 Tema do Post",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(10, 8))

        ttk.Entry(
            scroll_left,
            textvariable=self.tema_post_normal,
            font=("Segoe UI", 11),
            bootstyle="primary"
        ).pack(fill=X, pady=(0, 5), ipady=8)

        ttk.Label(
            scroll_left,
            text="Ex: Dicas de produtividade, Benefícios do treino matinal...",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(anchor=W, pady=(0, 10))

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Tom da Comunicação
        ttk.Label(
            scroll_left,
            text="🎭 Tom da Comunicação",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(0, 8))

        tons = [
            ("💼 Profissional (Sério e corporativo)", "profissional"),
            ("✨ Inspiracional (Motivador e elevado)", "inspiracional"),
            ("📚 Educativo (Informativo e didático)", "educativo"),
            ("🎉 Entusiasta (Animado e energético)", "entusiasta"),
            ("👑 Premium (Sofisticado e exclusivo)", "premium")
        ]

        for texto, valor in tons:
            ttk.Radiobutton(
                scroll_left,
                text=texto,
                variable=self.tom_normal,
                value=valor,
                bootstyle="primary"
            ).pack(anchor=W, pady=3, padx=10)

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Call to Action
        ttk.Label(
            scroll_left,
            text="🎯 Call to Action (CTA)",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(0, 8))

        ctas = [
            ("💬 Comentar", "comentar"),
            ("❤️ Curtir", "curtir"),
            ("🔄 Compartilhar", "compartilhar"),
            ("👥 Seguir", "seguir"),
            ("💾 Salvar", "salvar"),
            ("🔗 Link na Bio", "link_bio")
        ]

        cta_frame = ttk.Frame(scroll_left)
        cta_frame.pack(fill=X, pady=(0, 15))

        for i, (texto, valor) in enumerate(ctas):
            ttk.Radiobutton(
                cta_frame,
                text=texto,
                variable=self.cta_normal,
                value=valor,
                bootstyle="primary"
            ).pack(anchor=W, pady=3, padx=10)

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Botões de Ação
        ttk.Button(
            scroll_left,
            text="🚀 GERAR POST PROFISSIONAL",
            command=lambda: self.gerar_post("normal"),
            bootstyle="success",
            width=40
        ).pack(fill=X, pady=(10, 5), ipady=10)

        # Progress bar
        self.progress_normal = ttk.Progressbar(
            scroll_left,
            mode="indeterminate",
            bootstyle="success-striped"
        )
        self.progress_normal.pack(fill=X, pady=5)

        self.status_label_normal = ttk.Label(
            scroll_left,
            text="Pronto para gerar seu post profissional!",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        )
        self.status_label_normal.pack(pady=5)

        # ===== COLUNA DIREITA - Preview e Resultados =====
        right_frame = ttk.Labelframe(
            container,
            text="📊 Preview e Resultados",
            bootstyle="info",
            padding=15
        )
        right_frame.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))

        # Scrollable frame
        scroll_right = ScrolledFrame(right_frame, autohide=True)
        scroll_right.pack(fill=BOTH, expand=YES)

        # Preview da Imagem
        ttk.Label(
            scroll_right,
            text="🖼️ Preview da Imagem",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(5, 10))

        self.image_preview_normal = ttk.Label(
            scroll_right,
            text="📷\n\nA imagem hiper-realista\naparecerá aqui",
            font=("Segoe UI", 14),
            bootstyle="secondary",
            anchor=CENTER
        )
        self.image_preview_normal.pack(fill=X, pady=(0, 15))
        self.image_preview_normal.configure(relief=SOLID, borderwidth=1)

        # Legenda e Hashtags
        ttk.Label(
            scroll_right,
            text="📝 Legenda Profissional",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(10, 10))

        self.text_result_normal = ttk.Text(
            scroll_right,
            height=15,
            font=("Segoe UI", 10),
            wrap=WORD
        )
        self.text_result_normal.pack(fill=BOTH, expand=YES, pady=(0, 15))
        self.text_result_normal.insert("1.0", "Aguardando geração do conteúdo profissional...")
        self.text_result_normal.configure(state=DISABLED)

        # Botões de ação
        btn_frame = ttk.Frame(scroll_right)
        btn_frame.pack(fill=X, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="💾 Salvar Tudo",
            command=lambda: self.salvar_tudo("normal"),
            bootstyle="danger",
            width=20
        ).pack(side=LEFT, padx=(0, 5), ipady=8)

        ttk.Button(
            btn_frame,
            text="🖼️ Salvar Imagem",
            command=lambda: self.salvar_imagem("normal"),
            bootstyle="info",
            width=20
        ).pack(side=LEFT, padx=5, ipady=8)

        ttk.Button(
            btn_frame,
            text="📋 Copiar Texto",
            command=lambda: self.copiar_texto("normal"),
            bootstyle="warning",
            width=20
        ).pack(side=LEFT, padx=(5, 0), ipady=8)

    def criar_aba_bom_dia(self):
        """Cria a aba de mensagens motivacionais de Bom Dia (1:1)"""

        # Frame principal da aba
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="🌅 Bom Dia Motivacional (1:1)", sticky=NSEW)

        # Container principal com 2 colunas
        container = ttk.Frame(tab2)
        container.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # ===== COLUNA ESQUERDA - Formulário =====
        left_frame = ttk.Labelframe(
            container,
            text="⚙️ Configurações da Mensagem",
            bootstyle="warning",
            padding=15
        )
        left_frame.grid(row=0, column=0, sticky=NSEW, padx=(0, 5))

        # Scrollable frame
        scroll_left = ScrolledFrame(left_frame, autohide=True)
        scroll_left.pack(fill=BOTH, expand=YES)

        # Informação sobre formato
        info_frame = ttk.Frame(scroll_left, bootstyle="info")
        info_frame.pack(fill=X, pady=(5, 15))

        ttk.Label(
            info_frame,
            text="ℹ️ Formato: Imagem Quadrada 1:1 (1080x1080)",
            font=("Segoe UI", 10, "bold"),
            bootstyle="info"
        ).pack(padx=10, pady=8)

        # Categoria Motivacional
        ttk.Label(
            scroll_left,
            text="🎯 Categoria Motivacional",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(10, 8))

        categorias = [
            ("🏆 Sucesso e Conquistas", "sucesso"),
            ("💪 Força e Determinação", "forca"),
            ("🌟 Positividade e Gratidão", "positividade"),
            ("🚀 Foco e Produtividade", "foco"),
            ("❤️ Amor Próprio e Autoestima", "amor_proprio"),
            ("🎯 Metas e Objetivos", "metas"),
            ("🌈 Esperança e Fé", "esperanca"),
            ("🧘 Paz e Equilíbrio", "paz")
        ]

        for texto, valor in categorias:
            ttk.Radiobutton(
                scroll_left,
                text=texto,
                variable=self.categoria_bomdia,
                value=valor,
                bootstyle="warning"
            ).pack(anchor=W, pady=3, padx=10)

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Subtema Opcional
        ttk.Label(
            scroll_left,
            text="💭 Subtema (Opcional)",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(0, 8))

        ttk.Entry(
            scroll_left,
            textvariable=self.subtema_bomdia,
            font=("Segoe UI", 11),
            bootstyle="warning"
        ).pack(fill=X, pady=(0, 5), ipady=8)

        ttk.Label(
            scroll_left,
            text="Ex: Segundas-feiras, Novos começos, Superação...",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        ).pack(anchor=W, pady=(0, 10))

        ttk.Separator(scroll_left).pack(fill=X, pady=15)

        # Informações sobre o estilo
        style_info = ttk.Frame(scroll_left, bootstyle="light", relief=SOLID, borderwidth=1)
        style_info.pack(fill=X, pady=(10, 15), padx=5)

        ttk.Label(
            style_info,
            text="🎨 Estilo Automático:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor=W, padx=10, pady=(10, 5))

        ttk.Label(
            style_info,
            text="• Imagens fotográficas ultra-realistas\n"
                 "• Cenários inspiradores (nascer do sol, natureza, cena do cotidiano)\n"
                 "• Cores vibrantes e profissionais\n"
                 "• Qualidade 8K, iluminação perfeita",
            font=("Segoe UI", 9),
            bootstyle="secondary",
            justify=LEFT
        ).pack(anchor=W, padx=20, pady=(0, 10))

        # Botões de Ação
        ttk.Button(
            scroll_left,
            text="🌅 GERAR BOM DIA MOTIVACIONAL",
            command=lambda: self.gerar_post("bomdia"),
            bootstyle="warning",
            width=40
        ).pack(fill=X, pady=(20, 5), ipady=10)

        # Progress bar
        self.progress_bomdia = ttk.Progressbar(
            scroll_left,
            mode="indeterminate",
            bootstyle="warning-striped"
        )
        self.progress_bomdia.pack(fill=X, pady=5)

        self.status_label_bomdia = ttk.Label(
            scroll_left,
            text="Pronto para criar uma mensagem inspiradora!",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        )
        self.status_label_bomdia.pack(pady=5)

        # ===== COLUNA DIREITA - Preview e Resultados =====
        right_frame = ttk.Labelframe(
            container,
            text="📊 Preview e Resultados",
            bootstyle="success",
            padding=15
        )
        right_frame.grid(row=0, column=1, sticky=NSEW, padx=(5, 0))

        # Scrollable frame
        scroll_right = ScrolledFrame(right_frame, autohide=True)
        scroll_right.pack(fill=BOTH, expand=YES)

        # Preview da Imagem
        ttk.Label(
            scroll_right,
            text="🖼️ Preview da Imagem (1:1)",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(5, 10))

        self.image_preview_bomdia = ttk.Label(
            scroll_right,
            text="🌅\n\nSua imagem motivacional\naparecerá aqui",
            font=("Segoe UI", 14),
            bootstyle="secondary",
            anchor=CENTER
        )
        self.image_preview_bomdia.pack(fill=X, pady=(0, 15))
        self.image_preview_bomdia.configure(relief=SOLID, borderwidth=1)

        # Mensagem Motivacional
        ttk.Label(
            scroll_right,
            text="💬 Mensagem Motivacional",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=W, pady=(10, 10))

        self.text_result_bomdia = ttk.Text(
            scroll_right,
            height=15,
            font=("Segoe UI", 10),
            wrap=WORD
        )
        self.text_result_bomdia.pack(fill=BOTH, expand=YES, pady=(0, 15))
        self.text_result_bomdia.insert("1.0", "Aguardando geração da mensagem motivacional...")
        self.text_result_bomdia.configure(state=DISABLED)

        # Botões de ação
        btn_frame = ttk.Frame(scroll_right)
        btn_frame.pack(fill=X, pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="💾 Salvar Tudo",
            command=lambda: self.salvar_tudo("bomdia"),
            bootstyle="danger",
            width=20
        ).pack(side=LEFT, padx=(0, 5), ipady=8)

        ttk.Button(
            btn_frame,
            text="🖼️ Salvar Imagem",
            command=lambda: self.salvar_imagem("bomdia"),
            bootstyle="info",
            width=20
        ).pack(side=LEFT, padx=5, ipady=8)

        ttk.Button(
            btn_frame,
            text="📋 Copiar Texto",
            command=lambda: self.copiar_texto("bomdia"),
            bootstyle="warning",
            width=20
        ).pack(side=LEFT, padx=(5, 0), ipady=8)

    def alternar_tema(self):
        """Alterna entre tema Dark e Light"""
        if self.current_theme == "darkly":
            self.style.theme_use("flatly")  # Tema claro
            self.current_theme = "flatly"
            self.theme_btn.configure(text="🌙 Modo Escuro")
        else:
            self.style.theme_use("darkly")  # Tema escuro
            self.current_theme = "darkly"
            self.theme_btn.configure(text="☀️ Modo Claro")

    def validar_dados(self, tipo_aba):
        """Valida os dados antes de gerar"""
        if tipo_aba == "normal":
            if not self.nicho_normal.get().strip():
                messagebox.showwarning(
                    "Campo Obrigatório",
                    "Por favor, informe o nicho/segmento!"
                )
                return False
            if not self.tema_post_normal.get().strip():
                messagebox.showwarning(
                    "Campo Obrigatório",
                    "Por favor, informe o tema do post!"
                )
                return False
        # Para Bom Dia não há validações obrigatórias (categoria tem valor padrão)
        return True

    def gerar_post(self, tipo_aba):
        """Inicia a geração do post"""
        if self.is_generating:
            messagebox.showwarning(
                "Geração em Andamento",
                "Aguarde a conclusão da geração atual!"
            )
            return

        if not self.validar_dados(tipo_aba):
            return

        self.current_tab_name = tipo_aba

        # Confirmação
        if tipo_aba == "normal":
            msg = (
                f"Gerar post profissional?\n\n"
                f"📱 Tipo: {self.tipo_post_normal.get().upper()}\n"
                f"🎯 Nicho: {self.nicho_normal.get()}\n"
                f"💡 Tema: {self.tema_post_normal.get()}\n"
                f"🎭 Tom: {self.tom_normal.get().title()}\n\n"
                f"A geração pode levar 2-3 minutos."
            )
        else:
            msg = (
                f"Gerar Bom Dia Motivacional?\n\n"
                f"🎯 Categoria: {self.categoria_bomdia.get().title()}\n"
                f"📐 Formato: 1:1 (Quadrado)\n\n"
                f"A geração pode levar 2-3 minutos."
            )

        resposta = messagebox.askyesno("Confirmar Geração", msg)
        if not resposta:
            return

        # Iniciar geração em thread separada
        self.is_generating = True

        if tipo_aba == "normal":
            self.progress_normal.start()
            self.status_label_normal.configure(text="⚙️ Iniciando geração...")
        else:
            self.progress_bomdia.start()
            self.status_label_bomdia.configure(text="⚙️ Iniciando geração...")

        thread = threading.Thread(target=self.executar_geracao, args=(tipo_aba,))
        thread.daemon = True
        thread.start()

    def executar_geracao(self, tipo_aba):
        """Executa a geração do post (em thread separada)"""
        try:
            if tipo_aba == "normal":
                self._gerar_post_normal()
            else:
                self._gerar_post_bomdia()

            # Atualizar interface
            self.after(0, self.exibir_resultados, tipo_aba)

        except Exception as e:
            self.after(0, self.mostrar_erro, str(e), tipo_aba)
        finally:
            self.after(0, self.finalizar_geracao, tipo_aba)

    def _gerar_post_normal(self):
        """Gera post normal"""
        tipo = self.tipo_post_normal.get()
        nicho = self.nicho_normal.get()
        tema = self.tema_post_normal.get()
        tom = self.tom_normal.get()
        cta = self.cta_normal.get()

        # Atualizar status
        self.after(0, lambda: self.status_label_normal.configure(
            text="🎨 Gerando imagem fotográfica hiper-realista com Flux.1..."
        ))

        # Gerar imagem com prompt otimizado para fotografia profissional
        self.imagem_gerada = self.openai_service.gerar_imagem_marketing(
            tipo_post=tipo,
            nicho=nicho,
            tema=tema,
            tom=tom,
            formato="normal"
        )

        # Atualizar status
        self.after(0, lambda: self.status_label_normal.configure(
            text="✍️ Gerando legenda profissional com GPT-4..."
        ))

        # Gerar legenda
        self.legenda_gerada = self.openai_service.gerar_legenda_marketing(
            tipo_post=tipo,
            nicho=nicho,
            tema=tema,
            tom=tom,
            cta=cta
        )

        # Atualizar status
        self.after(0, lambda: self.status_label_normal.configure(
            text="#️⃣ Gerando hashtags estratégicas..."
        ))

        # Gerar hashtags
        self.hashtags_geradas = self.openai_service.gerar_hashtags_marketing(
            nicho=nicho,
            tipo_post=tipo
        )

    def _gerar_post_bomdia(self):
        """Gera post de Bom Dia Motivacional"""
        categoria = self.categoria_bomdia.get()
        subtema = self.subtema_bomdia.get()

        # Atualizar status
        self.after(0, lambda: self.status_label_bomdia.configure(
            text="🌅 Gerando imagem motivacional hiper-realista..."
        ))

        # Gerar imagem motivacional
        self.imagem_gerada = self.openai_service.gerar_imagem_bomdia(
            categoria=categoria,
            subtema=subtema
        )

        # Atualizar status
        self.after(0, lambda: self.status_label_bomdia.configure(
            text="💬 Gerando mensagem motivacional..."
        ))

        # Gerar mensagem
        self.legenda_gerada = self.openai_service.gerar_mensagem_bomdia(
            categoria=categoria,
            subtema=subtema
        )

        # Atualizar status
        self.after(0, lambda: self.status_label_bomdia.configure(
            text="#️⃣ Gerando hashtags motivacionais..."
        ))

        # Gerar hashtags
        self.hashtags_geradas = self.openai_service.gerar_hashtags_bomdia(
            categoria=categoria
        )

    def exibir_resultados(self, tipo_aba):
        """Exibe os resultados na interface"""
        # Selecionar widgets corretos
        if tipo_aba == "normal":
            image_widget = self.image_preview_normal
            text_widget = self.text_result_normal
        else:
            image_widget = self.image_preview_bomdia
            text_widget = self.text_result_bomdia

        # Exibir imagem
        if self.imagem_gerada and os.path.exists(self.imagem_gerada):
            try:
                img = Image.open(self.imagem_gerada)

                # Redimensionar mantendo proporção
                max_size = 400
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)
                image_widget.configure(image=photo, text="")
                image_widget.image = photo  # Manter referência

            except Exception as e:
                print(f"Erro ao exibir imagem: {e}")

        # Exibir texto
        texto_completo = f"{self.legenda_gerada}\n\n"
        texto_completo += " ".join(self.hashtags_geradas)

        text_widget.configure(state=NORMAL)
        text_widget.delete("1.0", END)
        text_widget.insert("1.0", texto_completo)
        text_widget.configure(state=DISABLED)

        # Notificação de sucesso
        toast = ToastNotification(
            title="Sucesso!",
            message=f"Post gerado com sucesso! {len(self.hashtags_geradas)} hashtags criadas.",
            duration=3000,
            bootstyle="success"
        )
        toast.show_toast()

    def mostrar_erro(self, erro, tipo_aba):
        """Mostra erro"""
        messagebox.showerror(
            "Erro na Geração",
            f"Ocorreu um erro:\n\n{erro}\n\nVerifique sua conexão e tente novamente."
        )

    def finalizar_geracao(self, tipo_aba):
        """Finaliza o processo de geração"""
        self.is_generating = False

        if tipo_aba == "normal":
            self.progress_normal.stop()
            self.status_label_normal.configure(text="✅ Pronto para gerar!")
        else:
            self.progress_bomdia.stop()
            self.status_label_bomdia.configure(text="✅ Pronto para gerar!")

    def salvar_tudo(self, tipo_aba):
        """Salva imagem e texto"""
        if not self.imagem_gerada or not os.path.exists(self.imagem_gerada):
            messagebox.showwarning(
                "Sem Conteúdo",
                "Nenhum conteúdo foi gerado ainda!"
            )
            return

        pasta = filedialog.askdirectory(
            title="Escolha a pasta para salvar"
        )

        if not pasta:
            return

        try:
            import shutil

            # Nome base
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if tipo_aba == "normal":
                base_nome = f"post_{self.nicho_normal.get().replace(' ', '_')}_{timestamp}"
            else:
                base_nome = f"bomdia_{self.categoria_bomdia.get()}_{timestamp}"

            # Salvar imagem
            ext = os.path.splitext(self.imagem_gerada)[1]
            caminho_img = os.path.join(pasta, f"{base_nome}{ext}")
            shutil.copy(self.imagem_gerada, caminho_img)

            # Salvar texto
            caminho_txt = os.path.join(pasta, f"{base_nome}.txt")
            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("GERADOR PROFISSIONAL DE POSTS - INSTAGRAM\n")
                f.write("Integrius Automações - 2025\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                f.write("=" * 70 + "\n")
                f.write("LEGENDA\n")
                f.write("=" * 70 + "\n")
                f.write(f"{self.legenda_gerada}\n\n")
                f.write("=" * 70 + "\n")
                f.write(f"HASHTAGS ({len(self.hashtags_geradas)})\n")
                f.write("=" * 70 + "\n")
                f.write(" ".join(self.hashtags_geradas) + "\n")

            messagebox.showinfo(
                "Sucesso!",
                f"Arquivos salvos em:\n\n{pasta}"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def salvar_imagem(self, tipo_aba):
        """Salva apenas a imagem"""
        if not self.imagem_gerada or not os.path.exists(self.imagem_gerada):
            messagebox.showwarning("Sem Imagem", "Nenhuma imagem foi gerada!")
            return

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("Todos", "*.*")],
            initialfile=os.path.basename(self.imagem_gerada)
        )

        if arquivo:
            try:
                import shutil
                shutil.copy(self.imagem_gerada, arquivo)
                messagebox.showinfo("Sucesso", f"Imagem salva!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar:\n{e}")

    def copiar_texto(self, tipo_aba):
        """Copia texto para área de transferência"""
        if not self.legenda_gerada:
            messagebox.showwarning("Sem Conteúdo", "Nenhum texto foi gerado!")
            return

        texto = f"{self.legenda_gerada}\n\n"
        texto += " ".join(self.hashtags_geradas)

        self.clipboard_clear()
        self.clipboard_append(texto)

        toast = ToastNotification(
            title="Copiado!",
            message="Texto copiado para área de transferência!",
            duration=2000,
            bootstyle="info"
        )
        toast.show_toast()


def main():
    """Função principal"""
    app = InstagramPostGenerator()
    app.mainloop()


if __name__ == "__main__":
    main()
