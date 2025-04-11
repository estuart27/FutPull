import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from PIL import Image, ImageTk, ImageDraw
import tempfile
import webbrowser
import json

class FootballDataCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("Coletor de Dados de Futebol")
        self.root.geometry("720x720")
        self.root.minsize(600, 650)
        self.root.configure(bg="#f5f5f7")
        
        # Permitir redimensionamento
        self.root.resizable(True, True)
        
        # Variáveis que serão expostas para uso externo
        self.time = tk.StringVar()
        self.adicional_manual = tk.StringVar()
        self.urls = []
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_interface()
    
    def setup_styles(self):
        # Configurar estilo moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores principais
        bg_color = '#f5f5f7'
        primary_color = '#3772ff'  # Azul mais moderno
        accent_color = '#f45b69'   # Cor de destaque para botões importantes
        text_color = '#2d3142'     # Texto escuro mas não totalmente preto
        
        # Configurações gerais
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color, font=('Segoe UI', 11))
        self.style.configure('Header.TLabel', background=bg_color, foreground=text_color, font=('Segoe UI', 14, 'bold'))
        self.style.configure('Subheader.TLabel', background=bg_color, foreground=text_color, font=('Segoe UI', 12))
        
        # Botões padrão
        self.style.configure('TButton', 
                          font=('Segoe UI', 11),
                          background=primary_color, 
                          foreground='white')
        self.style.map('TButton', 
                    background=[('active', '#2952cc'), ('pressed', '#193a8f')],
                    foreground=[('pressed', 'white')])
        
        # Botão de enviar (finalizar)
        self.style.configure('Finish.TButton', 
                          font=('Segoe UI', 12, 'bold'),
                          background=accent_color, 
                          foreground='white')
        self.style.map('Finish.TButton', 
                    background=[('active', '#e64559'), ('pressed', '#d6314a')],
                    foreground=[('pressed', 'white')])
        
        # Botão de adicionar
        self.style.configure('Add.TButton', 
                          font=('Segoe UI', 11),
                          background='#2ecc71', 
                          foreground='white')
        self.style.map('Add.TButton', 
                    background=[('active', '#27ae60'), ('pressed', '#1e8449')],
                    foreground=[('pressed', 'white')])
        
        # Entradas de texto
        self.style.configure('TEntry', fieldbackground='white', borderwidth=1)
        
    def create_interface(self):
        # Container principal com scroll 
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas com scrollbar para conteúdo
        self.canvas = tk.Canvas(main_container, bg="#f5f5f7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.content_frame = ttk.Frame(self.canvas)
        
        # Configurar scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Criar janela no canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor=tk.NW)
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Habilitar rolagem com a roda do mouse
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        # Criar elementos da interface
        self.create_header()
        self.create_form()
        self.create_footer()
        
    def on_frame_configure(self, event):
        # Atualizar região de rolagem para acomodar todo o conteúdo
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        # Ajustar a largura da janela interna ao redimensionar
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def on_mousewheel(self, event):
        # Rolagem com o mouse (Windows/Linux)
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_header(self):
        # Frame do cabeçalho
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Criar logo circular
        logo_size = 80
        logo_image = Image.new('RGBA', (logo_size, logo_size), (255, 0, 0, 0))
        draw = ImageDraw.Draw(logo_image)
        
        # Desenhar círculo gradiente
        for i in range(logo_size):
            # Criar efeito de gradiente do centro para a borda
            radius = logo_size/2
            distance = abs(i - radius)
            opacity = int(255 * (1 - distance/radius))
            
            # Círculo externo com gradiente
            draw.ellipse((i/2, i/2, logo_size-i/2, logo_size-i/2), 
                        fill=(55, 114, 255, opacity))
        
        # Desenhar círculo interno
        inner_margin = 15
        draw.ellipse((inner_margin, inner_margin, 
                    logo_size - inner_margin, logo_size - inner_margin), 
                    fill="#f5f5f7")
        
        # Desenhar linhas de um campo de futebol estilizado
        draw.line([(logo_size/2, inner_margin), 
                  (logo_size/2, logo_size - inner_margin)], 
                  fill="#3772ff", width=2)
        
        # Desenhar círculo central
        center_circle_size = 12
        draw.ellipse((logo_size/2 - center_circle_size/2, 
                     logo_size/2 - center_circle_size/2, 
                     logo_size/2 + center_circle_size/2, 
                     logo_size/2 + center_circle_size/2), 
                     outline="#3772ff", width=2)
        
        # Converter para PhotoImage
        self.logo_img = ImageTk.PhotoImage(logo_image)
        
        # Layout do cabeçalho com logo e texto
        logo_label = ttk.Label(header_frame, image=self.logo_img, background='#f5f5f7')
        logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Frame para textos do cabeçalho
        header_text_frame = ttk.Frame(header_frame)
        header_text_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        # Título e subtítulo
        title_label = ttk.Label(header_text_frame, 
                             text="Coletor de Dados de Futebol", 
                             style='Header.TLabel')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(header_text_frame, 
                                text="Coleta e analisa dados estatísticos de partidas",
                                style='Subheader.TLabel')
        subtitle_label.pack(anchor=tk.W)
        
    def create_form(self):
        # Container para o formulário
        form_frame = ttk.Frame(self.content_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Nome do time (opcional)
        self.create_team_section(form_frame)
        
        # Informações adicionais (opcional)
        self.create_additional_info_section(form_frame)
        
        # URLs (obrigatório)
        self.create_urls_section(form_frame)
        
    def create_team_section(self, parent):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=15)
        
        # Label com ícone
        header_frame = ttk.Frame(section_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        team_label = ttk.Label(header_frame, 
                            text="Nome do Time", 
                            font=('Segoe UI', 12, 'bold'))
        team_label.pack(side=tk.LEFT)
        
        optional_label = ttk.Label(header_frame, 
                                text="(opcional)", 
                                foreground="#888888")
        optional_label.pack(side=tk.LEFT, padx=5)
        
        # Campo de entrada com estilo
        team_entry = ttk.Entry(section_frame, 
                            textvariable=self.time, 
                            font=('Segoe UI', 11))
        team_entry.pack(fill=tk.X, ipady=8)
        
    def create_additional_info_section(self, parent):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=15)
        
        # Label com ícone
        header_frame = ttk.Frame(section_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_label = ttk.Label(header_frame, 
                            text="Informações Adicionais", 
                            font=('Segoe UI', 12, 'bold'))
        info_label.pack(side=tk.LEFT)
        
        optional_label = ttk.Label(header_frame, 
                                text="(opcional)", 
                                foreground="#888888")
        optional_label.pack(side=tk.LEFT, padx=5)
        
        # Área de texto
        self.info_text = tk.Text(section_frame, 
                              height=4, 
                              wrap=tk.WORD, 
                              font=('Segoe UI', 11), 
                              bd=1, 
                              relief=tk.SOLID)
        self.info_text.pack(fill=tk.X, pady=5)
        self.info_text.config(bg='white', highlightbackground="#e0e0e0", highlightthickness=1)
        
        # Função para atualizar a variável quando o texto for alterado
        def update_info(*args):
            self.adicional_manual.set(self.info_text.get("1.0", tk.END).strip())
        
        self.info_text.bind("<KeyRelease>", update_info)
        
    def create_urls_section(self, parent):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill=tk.X, pady=15)
        
        # Header
        header_frame = ttk.Frame(section_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        urls_label = ttk.Label(header_frame, 
                            text="URLs das Partidas", 
                            font=('Segoe UI', 12, 'bold'))
        urls_label.pack(side=tk.LEFT)
        
        required_label = ttk.Label(header_frame, 
                                text="(obrigatório)", 
                                foreground="#e74c3c")
        required_label.pack(side=tk.LEFT, padx=5)
        
        # Campo para adicionar URLs
        input_frame = ttk.Frame(section_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.new_url = tk.StringVar()
        url_entry = ttk.Entry(input_frame, 
                           textvariable=self.new_url, 
                           font=('Segoe UI', 11))
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        add_button = ttk.Button(input_frame, 
                             text="Adicionar URL", 
                             style='Add.TButton',
                             command=self.add_url)
        add_button.pack(side=tk.RIGHT, padx=(10, 0), ipadx=5, ipady=5)
        
        # Container para a lista de URLs
        list_container = ttk.Frame(section_frame)
        list_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Usar Frame com Canvas para scrollable
        self.urls_canvas = tk.Canvas(list_container, 
                                 bg="#f5f5f7", 
                                 highlightthickness=0,
                                 height=150)
        url_scrollbar = ttk.Scrollbar(list_container, 
                                   orient=tk.VERTICAL, 
                                   command=self.urls_canvas.yview)
        
        # Frame para conter URLs
        self.urls_list_frame = ttk.Frame(self.urls_canvas)
        
        # Configurar scrollbar para a lista de URLs
        self.urls_canvas.configure(yscrollcommand=url_scrollbar.set)
        self.urls_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        url_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.urls_canvas.create_window((0, 0), 
                                   window=self.urls_list_frame, 
                                   anchor=tk.NW,
                                   tags="self.urls_list_frame")
        
        self.urls_list_frame.bind("<Configure>", 
                              lambda e: self.urls_canvas.configure(
                                  scrollregion=self.urls_canvas.bbox("all")
                              ))
        
        # Exemplos de URLs
        examples_frame = ttk.Frame(section_frame)
        examples_frame.pack(fill=tk.X, pady=10)
        
        examples_label = ttk.Label(examples_frame, 
                                text="URLs de Exemplo:", 
                                font=('Segoe UI', 11, 'bold'))
        examples_label.pack(anchor=tk.W, pady=(0, 5))
        
        examples = [
            {"name": "FotMob", "url": "https://www.fotmob.com/"},
            {"name": "SofaScore", "url": "https://www.sofascore.com/"},
            {"name": "WhoScored", "url": "https://1xbet.whoscored.com/"},
        ]
        
        # Criar botões de exemplo lado a lado
        examples_buttons_frame = ttk.Frame(examples_frame)
        examples_buttons_frame.pack(fill=tk.X)
        
        for i, example in enumerate(examples):
            ex_btn = ttk.Button(examples_buttons_frame, 
                             text=example["name"], 
                             command=lambda e=example: self.load_example(e))
            ex_btn.pack(side=tk.LEFT, padx=(0 if i == 0 else 5, 5), fill=tk.X, expand=True)
    
    def create_footer(self):
        footer_frame = ttk.Frame(self.content_frame)
        footer_frame.pack(fill=tk.X, padx=30, pady=20)
        
        # Espaço para mensagens de status
        self.status_var = tk.StringVar()
        status_label = ttk.Label(footer_frame, 
                              textvariable=self.status_var, 
                              foreground="#666666")
        status_label.pack(fill=tk.X, pady=10)
        
        # Botão de finalizar
        finish_button = ttk.Button(footer_frame, 
                                text="FINALIZAR E SALVAR DADOS", 
                                style='Finish.TButton',
                                command=self.finalize_data)
        finish_button.pack(fill=tk.X, ipady=12)
        
    def add_url(self):
        url = self.new_url.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
            return
        
        # Verificação básica de formato de URL
        url_pattern = re.compile(r'^https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        if not url_pattern.match(url):
            messagebox.showerror("Erro", "URL inválida. A URL deve começar com http:// ou https://")
            return
        
        # Adicionar URL à lista
        self.urls.append(url)
        self.new_url.set("")  # Limpar o campo
        
        # Atualizar a lista visual
        self.update_url_list()
        
        self.status_var.set(f"{len(self.urls)} URL(s) adicionada(s)")
    
    def update_url_list(self):
        # Limpar a lista atual
        for widget in self.urls_list_frame.winfo_children():
            widget.destroy()
        
        # Adicionar cada URL à lista
        for i, url in enumerate(self.urls):
            url_entry_frame = ttk.Frame(self.urls_list_frame)
            url_entry_frame.pack(fill=tk.X, pady=2)
            
            # Número do índice
            index_label = ttk.Label(url_entry_frame, 
                                 text=f"{i+1}.", 
                                 width=3)
            index_label.pack(side=tk.LEFT)
            
            # Mostrar apenas parte da URL se for muito longa
            display_url = url[:50] + "..." if len(url) > 50 else url
            url_label = ttk.Label(url_entry_frame, text=display_url)
            url_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Botões de ação
            button_frame = ttk.Frame(url_entry_frame)
            button_frame.pack(side=tk.RIGHT)
            
            # Botão para visualizar
            view_button = ttk.Button(button_frame, 
                                  text="👁️", 
                                  width=3,
                                  command=lambda u=url: webbrowser.open(u))
            view_button.pack(side=tk.LEFT, padx=2)
            
            # Botão para remover
            remove_button = ttk.Button(button_frame, 
                                    text="❌", 
                                    width=3,
                                    command=lambda idx=i: self.remove_url(idx))
            remove_button.pack(side=tk.LEFT, padx=2)
        
        # Atualizar o scrollregion
        self.urls_list_frame.update_idletasks()
        self.urls_canvas.configure(scrollregion=self.urls_canvas.bbox("all"))
    
    def remove_url(self, index):
        if 0 <= index < len(self.urls):
            del self.urls[index]
            self.update_url_list()
            self.status_var.set(f"{len(self.urls)} URL(s) restante(s)")
    
    def load_example(self, example):
        # Carregar URL do exemplo
        self.new_url.set(example["url"])
    
    def finalize_data(self):
        # Validar se há pelo menos uma URL
        if not self.urls:
            messagebox.showerror("Erro", "Por favor, adicione pelo menos uma URL.")
            return
        
        # Coletar dados finais
        time_value = self.time.get()
        adicional_manual_value = self.adicional_manual.get()
        urls_value = self.urls.copy()
        
        # Confirmar com o usuário
        confirm_msg = f"Os seguintes dados serão salvos:\n\n"
        confirm_msg += f"Time: {time_value if time_value else '(não especificado)'}\n\n"
        confirm_msg += f"Informações adicionais: {adicional_manual_value if adicional_manual_value else '(não especificado)'}\n\n"
        confirm_msg += f"URLs ({len(urls_value)}):\n"
        for i, url in enumerate(urls_value):
            if i < 3:  # Mostrar apenas as 3 primeiras URLs
                confirm_msg += f"- {url}\n"
            elif i == 3:
                confirm_msg += f"- E mais {len(urls_value) - 3} URL(s)...\n"
        
        confirm = messagebox.askyesno("Confirmar Dados", confirm_msg + "\nDeseja finalizar e salvar estes dados?")
        
        if confirm:
            # Salvar os dados e finalizar
            self.save_data(time_value, adicional_manual_value, urls_value)
            
            # Mostrar mensagem de sucesso
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            
            # Fechar a janela
            self.root.destroy()
    
    def save_data(self, time_value, adicional_manual_value, urls_value):
        """
        Salva os dados nas variáveis globais.
        Na aplicação real, isto seria integrado com o restante do código.
        """
        # Aqui fazemos a ponte entre a interface e as variáveis globais
        global time, adicional_manual, URL
        
        # Atualizar as variáveis globais com os valores coletados
        time = time_value
        adicional_manual = adicional_manual_value
        URL = urls_value
        
        # Para depuração e verificação, podemos salvar em um arquivo também
        data = {
            "time": time_value,
            "adicional_manual": adicional_manual_value,
            "URL": urls_value
        }
        
        try:
            with open("football_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print("Dados salvos localmente em football_data.json para verificação")
        except Exception as e:
            print(f"Erro ao salvar arquivo local: {e}")
        
        # Log dos valores para verificação
        print("\n=== DADOS COLETADOS ===")
        print(f"time = '{time}'")
        print(f"adicional_manual = '{adicional_manual}'")
        print(f"URL = {URL}")
        print("======================\n")

def collect_football_data():
    """
    Função principal para iniciar a coleta de dados.
    Esta função deve ser chamada pelo código principal.
    """
    root = tk.Tk()
    app = FootballDataCollector(root)
    root.mainloop()
    
    # Após o fechamento da interface, as variáveis globais já estarão atualizadas
    # E podem ser usadas pelo resto do programa

# Se este arquivo for executado diretamente, inicia a coleta
if __name__ == "__main__":
    # Definir variáveis globais que serão preenchidas pela interface
    time = ""
    adicional_manual = ""
    URL = []
    
    # Iniciar a interface de coleta
    collect_football_data()
    
    # Após a coleta, as variáveis estarão disponíveis para uso
    print("\n=== RESULTADO FINAL ===")
    print(f"time = '{time}'")
    print(f"adicional_manual = '{adicional_manual}'")
    print(f"URL = {URL}")