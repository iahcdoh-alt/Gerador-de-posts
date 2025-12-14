#!/usr/bin/env python3
"""
Gerador de Posts para Instagram - Versão GUI
Interface gráfica usando Tkinter
"""

import os
import sys
import threading
from tkinter import *
from tkinter import ttk, messagebox, scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
from dotenv import load_dotenv
from openai_service import OpenAIService

# Configurar DPI awareness para Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


class GeradorPostsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Posts para Instagram")

        # Configurar geometria com valores seguros
        try:
            self.root.geometry("900x700")
        except:
            self.root.geometry("800x600")

        self.root.resizable(True, True)

        # Variáveis
        self.tipo_post = StringVar(value="feed")
        self.nicho = StringVar()
        self.tom = StringVar(value="sério")
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

    def criar_interface(self):
        """Cria toda a interface gráfica"""

        # Frame principal com scroll
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # ===== TÍTULO =====
        titulo_frame = Frame(main_frame, bg="#2c3e50", relief=RAISED, borderwidth=2)
        titulo_frame.pack(fill=X, pady=(0, 10))

        Label(
            titulo_frame,
            text="📱 GERADOR DE POSTS PARA INSTAGRAM",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        ).pack()

        Label(
            titulo_frame,
            text="Crie imagens, legendas e hashtags com IA",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1",
            pady=(0, 10)
        ).pack()

        # ===== CONTAINER PRINCIPAL COM DUAS COLUNAS =====
        container = Frame(main_frame, bg="#f0f0f0")
        container.pack(fill=BOTH, expand=True)

        # COLUNA ESQUERDA - Formulário
        left_frame = Frame(container, bg="#f0f0f0")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

        # COLUNA DIREITA - Preview e Resultados
        right_frame = Frame(container, bg="#f0f0f0")
        right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))

        # ===== FORMULÁRIO (COLUNA ESQUERDA) =====

        # Tipo de Post
        self.criar_secao_tipo_post(left_frame)

        # Nicho
        self.criar_secao_nicho(left_frame)

        # Tom da Legenda
        self.criar_secao_tom(left_frame)

        # Botões de Ação
        self.criar_botoes_acao(left_frame)

        # Barra de Progresso
        self.criar_barra_progresso(left_frame)

        # ===== PREVIEW E RESULTADOS (COLUNA DIREITA) =====

        # Preview da Imagem
        self.criar_preview_imagem(right_frame)

        # Legenda e Hashtags
        self.criar_area_resultados(right_frame)

        # Status Bar
        self.criar_status_bar()

    def criar_secao_tipo_post(self, parent):
        """Cria seção de seleção do tipo de post"""
        frame = LabelFrame(
            parent,
            text="📌 Tipo de Post",
            font=("Arial", 11, "bold"),
            bg="white",
            relief=GROOVE,
            borderwidth=2
        )
        frame.pack(fill=X, pady=5)

        inner = Frame(frame, bg="white")
        inner.pack(padx=10, pady=10)

        Radiobutton(
            inner,
            text="📸 Feed (Post quadrado)",
            variable=self.tipo_post,
            value="feed",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=W, pady=2)

        Radiobutton(
            inner,
            text="🎥 Reel (Vídeo vertical)",
            variable=self.tipo_post,
            value="reel",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=W, pady=2)

        Radiobutton(
            inner,
            text="📱 Stories (História temporária)",
            variable=self.tipo_post,
            value="stories",
            font=("Arial", 10),
            bg="white"
        ).pack(anchor=W, pady=2)

    def criar_secao_nicho(self, parent):
        """Cria seção de entrada do nicho"""
        frame = LabelFrame(
            parent,
            text="🎯 Nicho do Conteúdo",
            font=("Arial", 11, "bold"),
            bg="white",
            relief=GROOVE,
            borderwidth=2
        )
        frame.pack(fill=X, pady=5)

        inner = Frame(frame, bg="white")
        inner.pack(padx=10, pady=10, fill=X)

        Label(
            inner,
            text="Digite o nicho do seu post:",
            font=("Arial", 9),
            bg="white",
            fg="#555"
        ).pack(anchor=W, pady=(0, 5))

        entry = Entry(
            inner,
            textvariable=self.nicho,
            font=("Arial", 11),
            relief=SOLID,
            borderwidth=1
        )
        entry.pack(fill=X, pady=(0, 5))

        Label(
            inner,
            text="Exemplos: Fitness, Moda, Tecnologia, Culinária, Viagens...",
            font=("Arial", 8),
            bg="white",
            fg="#888"
        ).pack(anchor=W)

    def criar_secao_tom(self, parent):
        """Cria seção de seleção do tom"""
        frame = LabelFrame(
            parent,
            text="🎭 Tom da Legenda",
            font=("Arial", 11, "bold"),
            bg="white",
            relief=GROOVE,
            borderwidth=2
        )
        frame.pack(fill=X, pady=5)

        inner = Frame(frame, bg="white")
        inner.pack(padx=10, pady=10)

        tons = [
            ("💼 Sério (Profissional)", "sério"),
            ("🎉 Divertido (Animado)", "divertido"),
            ("😂 Engraçado (Humorístico)", "engraçado"),
            ("✨ Inspiracional (Motivador)", "inspiracional"),
            ("📚 Educativo (Informativo)", "educativo"),
            ("👑 Luxuoso (Sofisticado)", "luxuoso")
        ]

        for texto, valor in tons:
            Radiobutton(
                inner,
                text=texto,
                variable=self.tom,
                value=valor,
                font=("Arial", 10),
                bg="white"
            ).pack(anchor=W, pady=2)

    def criar_botoes_acao(self, parent):
        """Cria botões de ação"""
        frame = Frame(parent, bg="#f0f0f0")
        frame.pack(fill=X, pady=10)

        self.btn_gerar = Button(
            frame,
            text="🚀 GERAR POST",
            command=self.gerar_post,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief=RAISED,
            borderwidth=3,
            cursor="hand2",
            height=2
        )
        self.btn_gerar.pack(fill=X, pady=2)

        btn_frame = Frame(frame, bg="#f0f0f0")
        btn_frame.pack(fill=X, pady=5)

        Button(
            btn_frame,
            text="💾 Salvar Imagem",
            command=self.salvar_imagem,
            font=("Arial", 10),
            bg="#3498db",
            fg="white",
            relief=RAISED,
            cursor="hand2"
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 2))

        Button(
            btn_frame,
            text="📋 Copiar Texto",
            command=self.copiar_texto,
            font=("Arial", 10),
            bg="#9b59b6",
            fg="white",
            relief=RAISED,
            cursor="hand2"
        ).pack(side=RIGHT, fill=X, expand=True, padx=(2, 0))

    def criar_barra_progresso(self, parent):
        """Cria barra de progresso"""
        frame = Frame(parent, bg="#f0f0f0")
        frame.pack(fill=X, pady=5)

        self.progresso = ttk.Progressbar(
            frame,
            mode='indeterminate',
            length=300
        )
        self.progresso.pack(fill=X)

        self.label_status = Label(
            frame,
            text="Pronto para gerar!",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#555"
        )
        self.label_status.pack(pady=5)

    def criar_preview_imagem(self, parent):
        """Cria área de preview da imagem"""
        frame = LabelFrame(
            parent,
            text="🖼️ Preview da Imagem",
            font=("Arial", 11, "bold"),
            bg="white",
            relief=GROOVE,
            borderwidth=2
        )
        frame.pack(fill=BOTH, expand=True, pady=(0, 5))

        self.canvas_imagem = Canvas(
            frame,
            bg="#e0e0e0",
            highlightthickness=0
        )
        self.canvas_imagem.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Placeholder
        self.canvas_imagem.create_text(
            200, 150,
            text="A imagem aparecerá aqui",
            font=("Arial", 11),
            fill="#888"
        )

    def criar_area_resultados(self, parent):
        """Cria área de exibição de resultados"""
        frame = LabelFrame(
            parent,
            text="📝 Legenda e Hashtags",
            font=("Arial", 11, "bold"),
            bg="white",
            relief=GROOVE,
            borderwidth=2
        )
        frame.pack(fill=BOTH, expand=True, pady=(5, 0))

        self.texto_resultado = scrolledtext.ScrolledText(
            frame,
            font=("Arial", 10),
            wrap=WORD,
            height=10,
            relief=SOLID,
            borderwidth=1
        )
        self.texto_resultado.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.texto_resultado.insert(1.0, "A legenda e hashtags aparecerão aqui após a geração...")
        self.texto_resultado.config(state=DISABLED)

    def criar_status_bar(self):
        """Cria barra de status"""
        self.status_bar = Label(
            self.root,
            text="Desenvolvido com ❤️ usando OpenAI",
            relief=SUNKEN,
            anchor=W,
            font=("Arial", 8),
            bg="#34495e",
            fg="white"
        )
        self.status_bar.pack(side=BOTTOM, fill=X)

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
        self.btn_gerar.config(state=DISABLED)
        self.progresso.start(10)
        self.label_status.config(text="Gerando conteúdo... Por favor, aguarde...")

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

            # Gerar imagem
            self.root.after(0, lambda: self.label_status.config(text="🎨 Gerando imagem..."))
            self.imagem_gerada = self.openai_service.gerar_imagem(tipo, nicho, tom)

            # Gerar legenda
            self.root.after(0, lambda: self.label_status.config(text="✍️ Gerando legenda..."))
            self.legenda_gerada = self.openai_service.gerar_legenda(tipo, nicho, tom)

            # Gerar hashtags
            self.root.after(0, lambda: self.label_status.config(text="#️⃣ Gerando hashtags..."))
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

                # Redimensionar para caber no canvas
                canvas_width = self.canvas_imagem.winfo_width()
                canvas_height = self.canvas_imagem.winfo_height()

                img.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)

                self.photo = ImageTk.PhotoImage(img)

                self.canvas_imagem.delete("all")
                self.canvas_imagem.create_image(
                    canvas_width // 2,
                    canvas_height // 2,
                    image=self.photo,
                    anchor=CENTER
                )
            except Exception as e:
                print(f"Erro ao exibir imagem: {e}")

        # Exibir texto
        texto_completo = f"{self.legenda_gerada}\n\n"
        texto_completo += " ".join(self.hashtags_geradas)

        self.texto_resultado.config(state=NORMAL)
        self.texto_resultado.delete(1.0, END)
        self.texto_resultado.insert(1.0, texto_completo)
        self.texto_resultado.config(state=DISABLED)

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
        self.progresso.stop()
        self.btn_gerar.config(state=NORMAL)
        self.label_status.config(text="Pronto para gerar!")

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
    root = Tk()
    app = GeradorPostsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
