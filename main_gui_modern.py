#!/usr/bin/env python3
"""
Gerador de Posts para Instagram - Versão Moderna com CustomTkinter
Interface gráfica moderna com Material Design
"""

import os
import sys
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from dotenv import load_dotenv
from openai_service import OpenAIService

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")  # Modos: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"


class GeradorPostsModerno(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.title("Gerador de Posts para Instagram")
        self.geometry("1100x850")
        self.minsize(1000, 750)

        # Variáveis
        self.tipo_post = ctk.StringVar(value="feed")
        self.nicho = ctk.StringVar()
        self.tom = ctk.StringVar(value="sério")
        self.estilo_imagem = ctk.StringVar(value="realista")
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
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

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
            self.destroy()
            sys.exit(1)

        try:
            self.openai_service = OpenAIService(api_key)
        except Exception as e:
            messagebox.showerror(
                "Erro de Conexão",
                f"Erro ao conectar com OpenAI:\n{str(e)}"
            )
            self.destroy()
            sys.exit(1)

    def criar_interface(self):
        """Cria toda a interface gráfica"""

        # ===== HEADER =====
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray85", "gray20"))
        header_frame.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            header_frame,
            text="📱 GERADOR DE POSTS PARA INSTAGRAM",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            header_frame,
            text="Crie imagens, legendas e hashtags com IA",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray70")
        ).pack(pady=(0, 15))

        # Switch de Tema
        theme_switch = ctk.CTkSwitch(
            header_frame,
            text="🌙 Modo Escuro",
            command=self.alternar_tema,
            font=ctk.CTkFont(size=12)
        )
        theme_switch.pack(pady=(0, 10))
        theme_switch.select()  # Iniciar com dark mode ativo

        # ===== CONTAINER PRINCIPAL =====
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Configurar grid 2 colunas
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # COLUNA ESQUERDA - Formulário
        left_frame = ctk.CTkFrame(main_container, corner_radius=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

        # COLUNA DIREITA - Preview e Resultados
        right_frame = ctk.CTkFrame(main_container, corner_radius=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        # ===== CRIAR SEÇÕES =====
        self.criar_formulario(left_frame)
        self.criar_preview_e_resultados(right_frame)

        # ===== RODAPÉ =====
        footer = ctk.CTkFrame(self, corner_radius=0, height=35, fg_color=("gray80", "gray15"))
        footer.pack(fill="x", side="bottom")

        ctk.CTkLabel(
            footer,
            text="Desenvolvido com ❤️ usando OpenAI",
            font=ctk.CTkFont(size=11)
        ).pack(pady=8)

    def criar_formulario(self, parent):
        """Cria o formulário de entrada"""

        # Scrollable frame para o formulário
        scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Tipo de Post
        ctk.CTkLabel(
            scroll_frame,
            text="📌 Tipo de Post",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(5, 10))

        tipos_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        tipos_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkRadioButton(
            tipos_frame,
            text="📸 Feed (Post quadrado)",
            variable=self.tipo_post,
            value="feed",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)

        ctk.CTkRadioButton(
            tipos_frame,
            text="🎥 Reel (Vídeo vertical)",
            variable=self.tipo_post,
            value="reel",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)

        ctk.CTkRadioButton(
            tipos_frame,
            text="📱 Stories (História temporária)",
            variable=self.tipo_post,
            value="stories",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color=("gray70", "gray30")).pack(fill="x", pady=15)

        # Nicho
        ctk.CTkLabel(
            scroll_frame,
            text="🎯 Nicho do Conteúdo",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        self.entry_nicho = ctk.CTkEntry(
            scroll_frame,
            textvariable=self.nicho,
            placeholder_text="Ex: Fitness, Moda, Tecnologia, Culinária...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.entry_nicho.pack(fill="x", pady=(0, 15))

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color=("gray70", "gray30")).pack(fill="x", pady=15)

        # Estilo da Imagem
        ctk.CTkLabel(
            scroll_frame,
            text="🎨 Estilo da Imagem",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        estilo_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        estilo_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkRadioButton(
            estilo_frame,
            text="📸 Fotografia Ultra Realista em HD",
            variable=self.estilo_imagem,
            value="realista",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)

        ctk.CTkRadioButton(
            estilo_frame,
            text="🎨 Criação Artística / Ilustração",
            variable=self.estilo_imagem,
            value="artistico",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=3)

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color=("gray70", "gray30")).pack(fill="x", pady=15)

        # Tom da Legenda
        ctk.CTkLabel(
            scroll_frame,
            text="🎭 Tom da Legenda",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        tom_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        tom_frame.pack(fill="x", pady=(0, 15))

        tons = [
            ("💼 Sério (Profissional)", "sério"),
            ("🎉 Divertido (Animado)", "divertido"),
            ("😂 Engraçado (Humorístico)", "engraçado"),
            ("✨ Inspiracional (Motivador)", "inspiracional"),
            ("📚 Educativo (Informativo)", "educativo"),
            ("👑 Luxuoso (Sofisticado)", "luxuoso")
        ]

        for texto, valor in tons:
            ctk.CTkRadioButton(
                tom_frame,
                text=texto,
                variable=self.tom,
                value=valor,
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", pady=3)

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color=("gray70", "gray30")).pack(fill="x", pady=15)

        # Botões de Ação
        self.btn_gerar = ctk.CTkButton(
            scroll_frame,
            text="🚀 GERAR POST",
            command=self.gerar_post,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#2ecc71", "#27ae60"),
            hover_color=("#27ae60", "#229954")
        )
        self.btn_gerar.pack(fill="x", pady=(0, 10))

        # Barra de Progresso
        self.progress_bar = ctk.CTkProgressBar(scroll_frame, mode="indeterminate")
        self.progress_bar.pack(fill="x", pady=(0, 5))
        self.progress_bar.set(0)

        self.label_status = ctk.CTkLabel(
            scroll_frame,
            text="Pronto para gerar!",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.label_status.pack(pady=(0, 15))

        # Botões Secundários
        btn_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkButton(
            btn_frame,
            text="💾 Salvar Tudo",
            command=self.salvar_tudo,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226")
        ).pack(fill="x", pady=(0, 8))

        btn_row = ctk.CTkFrame(btn_frame, fg_color="transparent")
        btn_row.pack(fill="x")

        ctk.CTkButton(
            btn_row,
            text="💾 Salvar Imagem",
            command=self.salvar_imagem,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#21618c")
        ).pack(side="left", fill="x", expand=True, padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text="📋 Copiar Texto",
            command=self.copiar_texto,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color=("#9b59b6", "#8e44ad"),
            hover_color=("#8e44ad", "#7d3c98")
        ).pack(side="right", fill="x", expand=True, padx=(4, 0))

    def criar_preview_e_resultados(self, parent):
        """Cria a área de preview e resultados"""

        # Container com scroll
        scroll_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Preview da Imagem
        ctk.CTkLabel(
            scroll_frame,
            text="🖼️ Preview da Imagem",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(5, 10))

        self.image_label = ctk.CTkLabel(
            scroll_frame,
            text="",
            fg_color=("gray85", "gray25"),
            corner_radius=10,
            height=350
        )
        self.image_label.pack(fill="x", pady=(0, 20))

        # Placeholder
        placeholder = ctk.CTkLabel(
            self.image_label,
            text="📷\nA imagem aparecerá aqui",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray60")
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # Separador
        ctk.CTkFrame(scroll_frame, height=2, fg_color=("gray70", "gray30")).pack(fill="x", pady=15)

        # Legenda e Hashtags
        ctk.CTkLabel(
            scroll_frame,
            text="📝 Legenda e Hashtags",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 10))

        self.texto_resultado = ctk.CTkTextbox(
            scroll_frame,
            height=250,
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.texto_resultado.pack(fill="both", expand=True)
        self.texto_resultado.insert("1.0", "A legenda e hashtags aparecerão aqui após a geração...")
        self.texto_resultado.configure(state="disabled")

    def alternar_tema(self):
        """Alterna entre tema claro e escuro"""
        modo_atual = ctk.get_appearance_mode()
        novo_modo = "light" if modo_atual == "Dark" else "dark"
        ctk.set_appearance_mode(novo_modo)

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
        self.progress_bar.start()
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
            self.after(0, lambda: self.label_status.configure(text="🎨 Gerando imagem..."))
            self.imagem_gerada = self.openai_service.gerar_imagem(tipo, nicho, tom, estilo)

            # Gerar legenda
            self.after(0, lambda: self.label_status.configure(text="✍️ Gerando legenda..."))
            self.legenda_gerada = self.openai_service.gerar_legenda(tipo, nicho, tom)

            # Gerar hashtags
            self.after(0, lambda: self.label_status.configure(text="#️⃣ Gerando hashtags..."))
            self.hashtags_geradas = self.openai_service.gerar_hashtags(nicho, tipo)

            # Atualizar interface
            self.after(0, self.exibir_resultados)

        except Exception as e:
            self.after(0, lambda: self.mostrar_erro(str(e)))
        finally:
            self.after(0, self.finalizar_geracao)

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

                photo = ctk.CTkImage(
                    light_image=img,
                    dark_image=img,
                    size=(img.width, img.height)
                )

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
        self.progress_bar.set(0)
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

        self.clipboard_clear()
        self.clipboard_append(texto)

        messagebox.showinfo(
            "Copiado! 📋",
            "Legenda e hashtags copiadas para a área de transferência!\n\n"
            "Cole no Instagram com Ctrl+V"
        )


def main():
    """Função principal"""
    app = GeradorPostsModerno()
    app.mainloop()


if __name__ == "__main__":
    main()
