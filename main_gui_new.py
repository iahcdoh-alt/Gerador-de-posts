#!/usr/bin/env python3
"""
Gerador de Posts para Instagram - Versão Moderna com TTKBootstrap
Interface gráfica moderna com suporte a temas dark/light
"""

import os
import sys
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog, Canvas, CENTER
from tkinter import scrolledtext as tkscrolledtext
from PIL import Image, ImageTk
from dotenv import load_dotenv
from openai_service import OpenAIService


class GeradorPostsModerno:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Posts para Instagram - Integrius Automações")
        self.root.geometry("1100x850")
        self.root.minsize(1000, 750)

        # Variáveis
        self.tipo_post = ttk.StringVar(value="feed")
        self.nicho = ttk.StringVar()
        self.tom = ttk.StringVar(value="sério")
        self.estilo_imagem = ttk.StringVar(value="realista")
        self.tema_atual = ttk.StringVar(value="darkly")  # Tema inicial: dark

        self.openai_service = None
        self.imagem_gerada = None
        self.legenda_gerada = ""
        self.hashtags_geradas = []

        # Carregar e inicializar OpenAI
        self.inicializar_openai()

        # Criar interface
        self.criar_interface()

        # Centralizar janela
        self.centralizar_janela()

    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def inicializar_openai(self):
        """Inicializa o serviço OpenAI"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key or api_key == "sua_chave_api_aqui":
            messagebox.showerror(
                "Erro de Configuração",
                "Chave da API OpenAI não encontrada!\n\n"
                "Por favor:\n"
                "1. Abra o arquivo .env\n"
                "2. Adicione sua chave da OpenAI\n"
                "3. Reinicie a aplicação"
            )
            self.root.destroy()
            sys.exit(1)

        try:
            self.openai_service = OpenAIService(api_key)
        except Exception as e:
            messagebox.showerror(
                "Erro de Conexão",
                f"Erro ao conectar com OpenAI:\n{str(e)}"
            )
            self.root.destroy()
            sys.exit(1)

    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        novo_tema = "flatly" if self.tema_atual.get() == "darkly" else "darkly"
        self.tema_atual.set(novo_tema)
        self.root.style.theme_use(novo_tema)

    def criar_interface(self):
        """Cria toda a interface gráfica"""

        # ===== HEADER =====
        header_frame = ttk.Frame(self.root, bootstyle="dark")
        header_frame.pack(fill=X, padx=0, pady=0)

        ttk.Label(
            header_frame,
            text="📱 GERADOR DE POSTS PARA INSTAGRAM",
            font=("Segoe UI", 20, "bold"),
            bootstyle="inverse-dark"
        ).pack(pady=(15, 5))

        ttk.Label(
            header_frame,
            text="Crie imagens, legendas e hashtags com IA",
            font=("Segoe UI", 11),
            bootstyle="inverse-dark"
        ).pack(pady=(0, 10))

        # Botão de tema
        btn_tema = ttk.Checkbutton(
            header_frame,
            text="🌙 Modo Escuro",
            bootstyle="dark-round-toggle",
            command=self.alternar_tema
        )
        btn_tema.pack(pady=(0, 15))
        btn_tema.invoke()  # Iniciar com dark mode ativo

        # ===== CONTAINER PRINCIPAL =====
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Configurar grid 2 colunas
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # COLUNA ESQUERDA - Formulário
        left_frame = ttk.Frame(main_container, bootstyle="secondary")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # COLUNA DIREITA - Preview e Resultados
        right_frame = ttk.Frame(main_container, bootstyle="secondary")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # ===== CRIAR SEÇÕES =====
        self.criar_formulario(left_frame)
        self.criar_preview_e_resultados(right_frame)

        # ===== RODAPÉ =====
        footer = ttk.Frame(self.root, bootstyle="dark")
        footer.pack(fill=X, side=BOTTOM)

        ttk.Label(
            footer,
            text="Desenvolvido com ❤️ usando OpenAI",
            font=("Segoe UI", 10),
            bootstyle="inverse-dark"
        ).pack(pady=(8, 2))

        ttk.Label(
            footer,
            text="Desenvolvido por Integrius Automações - Copyright 2025 - Todos os direitos reservados",
            font=("Segoe UI", 9),
            bootstyle="inverse-dark"
        ).pack(pady=(0, 8))

    def criar_formulario(self, parent):
        """Cria o formulário de entrada"""

        # Scrollable frame para o formulário
        canvas = Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Tipo de Post
        ttk.Label(
            scroll_frame,
            text="📌 Tipo de Post",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(10, 10))

        ttk.Radiobutton(
            scroll_frame,
            text="📸 Feed (Post quadrado)",
            variable=self.tipo_post,
            value="feed",
            bootstyle="primary"
        ).pack(anchor="w", pady=3)

        ttk.Radiobutton(
            scroll_frame,
            text="🎥 Reel (Vídeo vertical)",
            variable=self.tipo_post,
            value="reel",
            bootstyle="primary"
        ).pack(anchor="w", pady=3)

        ttk.Radiobutton(
            scroll_frame,
            text="📱 Stories (História temporária)",
            variable=self.tipo_post,
            value="stories",
            bootstyle="primary"
        ).pack(anchor="w", pady=3)

        # Separador
        ttk.Separator(scroll_frame).pack(fill=X, pady=15)

        # Nicho
        ttk.Label(
            scroll_frame,
            text="🎯 Nicho do Conteúdo",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.entry_nicho = ttk.Entry(
            scroll_frame,
            textvariable=self.nicho,
            font=("Segoe UI", 12)
        )
        self.entry_nicho.pack(fill=X, pady=(0, 5))

        ttk.Label(
            scroll_frame,
            text="Ex: Fitness, Moda, Tecnologia, Culinária...",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(0, 10))

        # Separador
        ttk.Separator(scroll_frame).pack(fill=X, pady=15)

        # Estilo da Imagem
        ttk.Label(
            scroll_frame,
            text="🎨 Estilo da Imagem",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        ttk.Radiobutton(
            scroll_frame,
            text="📸 Fotografia Ultra Realista em HD",
            variable=self.estilo_imagem,
            value="realista",
            bootstyle="success"
        ).pack(anchor="w", pady=3)

        ttk.Radiobutton(
            scroll_frame,
            text="🎨 Criação Artística / Ilustração",
            variable=self.estilo_imagem,
            value="artistico",
            bootstyle="success"
        ).pack(anchor="w", pady=3)

        # Separador
        ttk.Separator(scroll_frame).pack(fill=X, pady=15)

        # Tom da Legenda
        ttk.Label(
            scroll_frame,
            text="🎭 Tom da Legenda",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        tons = [
            ("💼 Sério (Profissional)", "sério"),
            ("🎉 Divertido (Animado)", "divertido"),
            ("😂 Engraçado (Humorístico)", "engraçado"),
            ("✨ Inspiracional (Motivador)", "inspiracional"),
            ("📚 Educativo (Informativo)", "educativo"),
            ("👑 Luxuoso (Sofisticado)", "luxuoso")
        ]

        for texto, valor in tons:
            ttk.Radiobutton(
                scroll_frame,
                text=texto,
                variable=self.tom,
                value=valor,
                bootstyle="info"
            ).pack(anchor="w", pady=3)

        # Separador
        ttk.Separator(scroll_frame).pack(fill=X, pady=15)

        # Botões de Ação
        self.btn_gerar = ttk.Button(
            scroll_frame,
            text="🚀 GERAR POST",
            command=self.gerar_post,
            bootstyle="success",
            width=30
        )
        self.btn_gerar.pack(fill=X, pady=(0, 10))

        # Barra de Progresso
        self.progress_bar = ttk.Progressbar(
            scroll_frame,
            bootstyle="success-striped",
            mode="indeterminate"
        )
        self.progress_bar.pack(fill=X, pady=(0, 5))

        self.label_status = ttk.Label(
            scroll_frame,
            text="Pronto para gerar!",
            font=("Segoe UI", 10)
        )
        self.label_status.pack(pady=(0, 15))

        # Botões Secundários
        ttk.Button(
            scroll_frame,
            text="💾 Salvar Tudo",
            command=self.salvar_tudo,
            bootstyle="danger",
            width=30
        ).pack(fill=X, pady=(0, 8))

        btn_frame = ttk.Frame(scroll_frame)
        btn_frame.pack(fill=X)

        ttk.Button(
            btn_frame,
            text="💾 Salvar Imagem",
            command=self.salvar_imagem,
            bootstyle="primary"
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 4))

        ttk.Button(
            btn_frame,
            text="📋 Copiar Texto",
            command=self.copiar_texto,
            bootstyle="secondary"
        ).pack(side=RIGHT, fill=X, expand=True, padx=(4, 0))

    def criar_preview_e_resultados(self, parent):
        """Cria a área de preview e resultados"""

        # Canvas para preview
        canvas = Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Preview da Imagem
        ttk.Label(
            scroll_frame,
            text="🖼️ Preview da Imagem",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(10, 10))

        self.image_frame = ttk.Frame(scroll_frame, height=350)
        self.image_frame.pack(fill=X, pady=(0, 20))

        self.image_label = ttk.Label(
            self.image_frame,
            text="📷\nA imagem aparecerá aqui",
            font=("Segoe UI", 14),
            anchor=CENTER
        )
        self.image_label.pack(expand=True, fill=BOTH)

        # Separador
        ttk.Separator(scroll_frame).pack(fill=X, pady=15)

        # Legenda e Hashtags
        ttk.Label(
            scroll_frame,
            text="📝 Legenda e Hashtags",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.texto_resultado = tkscrolledtext.ScrolledText(
            scroll_frame,
            height=15,
            font=("Segoe UI", 11),
            wrap="word"
        )
        self.texto_resultado.pack(fill=BOTH, expand=True)
        self.texto_resultado.insert("1.0", "A legenda e hashtags aparecerão aqui após a geração...")
        self.texto_resultado.configure(state="disabled")

    def validar_dados(self):
        """Valida os dados do formulário"""
        if not self.nicho.get().strip():
            messagebox.showwarning(
                "Campo Obrigatório",
                "Por favor, digite o nicho do conteúdo!"
            )
            return False

        if len(self.nicho.get().strip()) < 3:
            messagebox.showwarning(
                "Nicho Inválido",
                "O nicho deve ter pelo menos 3 caracteres!"
            )
            return False

        return True

    def gerar_post(self):
        """Inicia a geração do post em thread separada"""
        if not self.validar_dados():
            return

        # Confirmação
        tipo = self.tipo_post.get().upper()
        nicho = self.nicho.get()
        tom = self.tom.get().capitalize()

        resposta = messagebox.askyesno(
            "Confirmar Geração",
            f"Gerar post com os seguintes dados?\n\n"
            f"📱 Tipo: {tipo}\n"
            f"🎯 Nicho: {nicho}\n"
            f"🎭 Tom: {tom}\n\n"
            f"A geração pode levar alguns minutos."
        )

        if not resposta:
            return

        # Desabilitar botão e iniciar progresso
        self.btn_gerar.configure(state="disabled")
        self.progress_bar.start(10)
        self.label_status.configure(text="Gerando conteúdo... Por favor, aguarde...")

        # Executar em thread separada
        thread = threading.Thread(target=self.executar_geracao)
        thread.daemon = True
        thread.start()

    def executar_geracao(self):
        """Executa a geração do post (roda em thread separada)"""
        try:
            tipo = self.tipo_post.get()
            nicho = self.nicho.get()
            tom = self.tom.get()
            estilo = self.estilo_imagem.get()

            # Gerar imagem
            self.root.after(0, lambda: self.label_status.configure(text="🎨 Gerando imagem..."))
            self.imagem_gerada = self.openai_service.gerar_imagem(tipo, nicho, tom, estilo)

            # Gerar legenda
            self.root.after(0, lambda: self.label_status.configure(text="✍️ Gerando legenda..."))
            self.legenda_gerada = self.openai_service.gerar_legenda(tipo, nicho, tom)

            # Gerar hashtags
            self.root.after(0, lambda: self.label_status.configure(text="#️⃣ Gerando hashtags..."))
            self.hashtags_geradas = self.openai_service.gerar_hashtags(nicho, tipo)

            # Atualizar interface
            self.root.after(0, self.exibir_resultados)

        except Exception as e:
            self.root.after(0, lambda: self.mostrar_erro(str(e)))
        finally:
            self.root.after(0, self.finalizar_geracao)

    def exibir_resultados(self):
        """Exibe os resultados na interface"""
        # Exibir imagem
        if self.imagem_gerada and os.path.exists(self.imagem_gerada):
            try:
                img = Image.open(self.imagem_gerada)

                # Redimensionar mantendo proporção
                max_width = 450
                max_height = 350
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(img)

                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Manter referência

            except Exception as e:
                print(f"Erro ao exibir imagem: {e}")

        # Exibir texto
        texto_completo = f"{self.legenda_gerada}\n\n"
        texto_completo += " ".join(self.hashtags_geradas)

        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto_completo)
        self.texto_resultado.configure(state="disabled")

        # Mensagem de sucesso
        messagebox.showinfo(
            "Sucesso! 🎉",
            f"Post gerado com sucesso!\n\n"
            f"🖼️ Imagem: {os.path.basename(self.imagem_gerada)}\n"
            f"#️⃣ Hashtags: {len(self.hashtags_geradas)}\n\n"
            f"Use os botões para salvar ou copiar."
        )

    def mostrar_erro(self, erro):
        """Mostra mensagem de erro"""
        messagebox.showerror(
            "Erro na Geração",
            f"Ocorreu um erro ao gerar o post:\n\n{erro}\n\n"
            f"Verifique sua conexão e tente novamente."
        )

    def finalizar_geracao(self):
        """Finaliza o processo de geração"""
        self.progress_bar.stop()
        self.btn_gerar.configure(state="normal")
        self.label_status.configure(text="Pronto para gerar!")

    def salvar_tudo(self):
        """Salva imagem e texto completo em uma pasta"""
        if not self.imagem_gerada or not os.path.exists(self.imagem_gerada):
            messagebox.showwarning(
                "Sem Conteúdo",
                "Nenhum conteúdo foi gerado ainda!\n\nGere um post primeiro."
            )
            return

        # Pedir pasta de destino
        pasta = filedialog.askdirectory(
            title="Escolha a pasta para salvar o post completo"
        )

        if not pasta:
            return

        try:
            import shutil
            from datetime import datetime

            # Nome base dos arquivos
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            tipo = self.tipo_post.get()
            nicho = self.nicho.get().replace(" ", "_")
            base_nome = f"post_{tipo}_{nicho}_{timestamp}"

            # Salvar imagem
            extensao_img = os.path.splitext(self.imagem_gerada)[1]
            caminho_img = os.path.join(pasta, f"{base_nome}{extensao_img}")
            shutil.copy(self.imagem_gerada, caminho_img)

            # Salvar texto
            caminho_txt = os.path.join(pasta, f"{base_nome}.txt")
            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("GERADOR DE POSTS PARA INSTAGRAM\n")
                f.write("=" * 70 + "\n\n")

                f.write(f"Tipo de Post: {tipo.upper()}\n")
                f.write(f"Nicho: {self.nicho.get()}\n")
                f.write(f"Tom: {self.tom.get().capitalize()}\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

                f.write("=" * 70 + "\n")
                f.write("LEGENDA\n")
                f.write("=" * 70 + "\n")
                f.write(f"{self.legenda_gerada}\n\n")

                f.write("=" * 70 + "\n")
                f.write(f"HASHTAGS ({len(self.hashtags_geradas)})\n")
                f.write("=" * 70 + "\n")
                f.write(" ".join(self.hashtags_geradas) + "\n\n")

                f.write("=" * 70 + "\n")
                f.write("LEGENDA COMPLETA COM HASHTAGS\n")
                f.write("=" * 70 + "\n")
                f.write(f"{self.legenda_gerada}\n\n")
                f.write(" ".join(self.hashtags_geradas) + "\n")

            messagebox.showinfo(
                "Sucesso! 🎉",
                f"Post completo salvo em:\n\n"
                f"📂 Pasta: {pasta}\n\n"
                f"📄 Arquivos:\n"
                f"• {os.path.basename(caminho_img)}\n"
                f"• {os.path.basename(caminho_txt)}"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivos:\n{e}")

    def salvar_imagem(self):
        """Salva a imagem em local escolhido pelo usuário"""
        if not self.imagem_gerada or not os.path.exists(self.imagem_gerada):
            messagebox.showwarning(
                "Sem Imagem",
                "Nenhuma imagem foi gerada ainda!"
            )
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
                messagebox.showinfo("Sucesso", f"Imagem salva em:\n{arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar imagem:\n{e}")

    def copiar_texto(self):
        """Copia legenda e hashtags para área de transferência"""
        if not self.legenda_gerada:
            messagebox.showwarning(
                "Sem Conteúdo",
                "Nenhum texto foi gerado ainda!"
            )
            return

        texto = f"{self.legenda_gerada}\n\n"
        texto += " ".join(self.hashtags_geradas)

        self.root.clipboard_clear()
        self.root.clipboard_append(texto)

        messagebox.showinfo(
            "Copiado! 📋",
            "Legenda e hashtags copiadas para a área de transferência!\n\n"
            "Cole no Instagram com Ctrl+V"
        )


def main():
    """Função principal"""
    # Tema inicial: darkly (escuro) - pode ser flatly (claro), cosmo, etc.
    root = ttk.Window(themename="darkly")
    app = GeradorPostsModerno(root)
    root.mainloop()


if __name__ == "__main__":
    main()
