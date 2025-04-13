from tkinter import *
from tkinter import messagebox
import webbrowser

# -------------------------- FUNÇÕES -------------------------- #
def iniciar_analise():
    """Coletar os dados, salvar as variáveis e executar o Palpile_Pro."""
    partida = partida_entry.get().strip()
    complemento = complemento_text.get("1.0", END).strip()
    
    # Limpa a lista de URLs e coleta os links preenchidos
    URL.clear()
    for entry in entries:
        link = entry.get().strip()
        if link:
            URL.append(link)

    # Validação: pelo menos um link deve ser preenchido
    if not URL:
        messagebox.showerror("Erro", "É obrigatório preencher pelo menos um link!")
        return

    print("\n--- Análise Iniciada ---")
    
    if partida:
        print(f"Partida: {partida}")
    if complemento:
        print(f"Observações: {complemento}")
    
    print("Links de vídeos inseridos:")
    for i, link in enumerate(URL, 1):
        print(f"{i}. {link}")
    
    # Mensagem de sucesso para o usuário
    messagebox.showinfo("Sucesso", "Análise iniciada com sucesso!")
    
    # Fechar a janela
    janela.destroy()
    
    # Executar o modelo Palpile_Pro com as variáveis salvas
    import subprocess
    import sys
    import json
    
    # Salvar as variáveis em um arquivo temporário
    dados = {
        "partida": partida,
        "observacoes": complemento,
        "links": URL
    }
    
    with open("dados_analise.json", "w") as f:
        json.dump(dados, f)
    
    # Executar o Palpile_Pro
    try:
        subprocess.run([sys.executable, "Palpite_Pro.py"])
    except Exception as e:
        print(f"Erro ao executar Palpile_Pro: {e}")


def adicionar_link():
    """Adicionar dinamicamente um novo campo de entrada para link."""
    # Obter o número da próxima linha para o novo campo
    link_number = len(entries) + 1
    
    # Criar um novo frame para o link
    link_frame = Frame(links_container, bg=cor_bg)
    link_frame.pack(fill=X, pady=5)
    
    # Criar label com o número do link
    label = Label(link_frame, text=f"Link {link_number}:", bg=cor_bg, fg="white", 
                 font=("Arial", 11), width=8, anchor="e")
    label.pack(side=LEFT, padx=(5, 5))
    
    # Criar campo para entrada do link
    new_entry = Entry(link_frame, font=("Arial", 11), bg="#F0F0F0")
    new_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
    entries.append(new_entry)
    
    # Botão para remover esse link
    if link_number > 1:  # Não permitir remover o primeiro link
        remove_btn = Button(link_frame, text="×", bg="#B22222", fg="white", 
                          command=lambda f=link_frame, e=new_entry: remover_link(f, e),
                          width=2, font=("Arial", 10, "bold"))
        remove_btn.pack(side=LEFT)

def remover_link(frame, entry):
    """Remove um campo de link específico."""
    entries.remove(entry)  # Remover da lista de entries
    frame.destroy()        # Remover o frame do link
    
    # Renumerar os links restantes
    for i, entry_widget in enumerate(entries):
        # Encontrar o Label associado ao Entry (primeiro widget no frame pai)
        parent_frame = entry_widget.master
        label_widget = parent_frame.winfo_children()[0]
        label_widget.config(text=f"Link {i+1}:")

def mudar_cor_enter(event):
    """Muda a cor do botão quando o mouse passa por cima."""
    event.widget.config(bg=cor_hover)

def mudar_cor_leave(event):
    """Restaura a cor original do botão quando o mouse sai."""
    event.widget.config(bg=cor_botao)

def abrir_ajuda():
    """Exibe uma janela de ajuda com instruções."""
    ajuda = Toplevel(janela)
    ajuda.title("Ajuda - Análise Esportiva")
    ajuda.configure(bg=cor_bg)
    ajuda.geometry("500x300")
    
    texto_ajuda = """
    Como utilizar o sistema de análise esportiva:
    
    1. Preencha o nome da partida no campo 'Partida'
    2. Adicione observações pertinentes no campo 'Observações'
    3. Insira pelo menos um link da pagina que o agenteIA vai analisar (obrigatório)
    4. Use o botão 'Adicionar Link' para incluir mais links
    5. Clique em 'Iniciar Análise' quando estiver pronto
    
    Dicas:
    • Para adicionar mais links, clique em 'Adicionar Link' e preencha o novo campo
    • Para remover um link, clique no botão "×" ao lado do link desejado
    • Certifique-se de que os links estejam corretos e acessíveis
    • A ferramenta coletará todos os dados para análise posterior, então não se preocupe com detalhes técnicos

    """
    
    label = Label(ajuda, text=texto_ajuda, bg=cor_bg, fg="white", 
                 font=("Arial", 11), justify=LEFT, padx=20, pady=20)
    label.pack(fill=BOTH, expand=True)
    
    btn_fechar = Button(ajuda, text="Fechar", command=ajuda.destroy,
                      bg=cor_botao, fg="white", font=("Arial", 11))
    btn_fechar.pack(pady=10)
    btn_fechar.bind('<Enter>', mudar_cor_enter)
    btn_fechar.bind('<Leave>', mudar_cor_leave)

def limpar_campos():
    """Limpa todos os campos do formulário."""
    partida_entry.delete(0, END)
    complemento_text.delete("1.0", END)
    
    # Limpar a primeira entrada
    entries[0].delete(0, END)
    
    # Remover todas as entries adicionais
    for i in range(len(entries)-1, 0, -1):
        entries[i].master.destroy()
        entries.pop(i)
import pyperclip  # Adicione isso no início do seu código, junto com outros imports

# Função para copiar o prompt
def copiar_prompt():
    prompt_texto = "Analise o confronto entre [Time1] vs [Time2], incluindo: situação física e mental dos elencos (lesões confirmadas ou dúvidas, suspensões, ritmo físico, moral do time, clima no vestiário e pressão da diretoria/torcida); clima previsto e condições do estádio (chuva, vento, temperatura, tipo e estado do gramado, estrutura do estádio e impacto esperado); desempenho em bolas paradas ⭐⭐⭐⭐☆ (gols por escanteios, faltas diretas/indiretas, pênaltis, principais cobradores e jogadas ensaiadas); estatísticas disciplinares ⭐⭐⭐☆☆ (média de cartões recebidos e cometidos, jogadores propensos a punições); desempenho como mandante/visitante e contra times grandes/pequenos; estratégias táticas (formações, estilo de jogo, variações recentes e prováveis ajustes); análise do mercado de apostas (odds, movimentos de mercado, picos suspeitos e volume apostado); resumo dos últimos 5 jogos de cada equipe com resultados, destaques individuais e nível de atuação — tudo em linha única, direto, detalhado e com o mínimo de tokens."  # Substitua pelo texto desejado
    pyperclip.copy(prompt_texto)
    messagebox.showinfo("Sucesso", "Prompt copiado para a área de transferência!")

# Função para exibir janela de sugestões de links
def mostrar_sugestoes():
    """Abre uma janela com três links sugeridos para o usuário escolher qual copiar."""
    sugestoes_janela = Toplevel(janela)
    sugestoes_janela.title("Sugestões de Links")
    sugestoes_janela.configure(bg=cor_bg)
    sugestoes_janela.geometry("500x200")

    # Links sugeridos
    links_sugeridos = [
        "https://www.sofascore.com/",
        "https://1xbet.whoscored.com/livescores",
        "https://www.fotmob.com/pt-BR"
    ]

    # Função para copiar o link selecionado
    def copiar_link(link):
        pyperclip.copy(link)
        messagebox.showinfo("Sucesso", f"Link copiado: {link}")
        sugestoes_janela.destroy()

    # Exibir cada link com um botão para copiar
    for i, link in enumerate(links_sugeridos, 1):
        frame = Frame(sugestoes_janela, bg=cor_bg)
        frame.pack(fill=X, pady=5, padx=20)

        label = Label(frame, text=f"Link {i}: {link}", bg=cor_bg, fg="white",
                      font=("Arial", 11), anchor="w")
        label.pack(side=LEFT, fill=X, expand=True)

        copiar_btn = Button(frame, text="Copiar", command=lambda l=link: copiar_link(l),
                           bg=cor_botao, fg="white", font=("Arial", 10),
                           padx=10, pady=2)
        copiar_btn.pack(side=RIGHT)
        copiar_btn.bind('<Enter>', mudar_cor_enter)
        copiar_btn.bind('<Leave>', mudar_cor_leave)

    # Botão para fechar a janela
    fechar_btn = Button(sugestoes_janela, text="Fechar", command=sugestoes_janela.destroy,
                       bg=cor_botao, fg="white", font=("Arial", 11))
    fechar_btn.pack(pady=10)
    fechar_btn.bind('<Enter>', mudar_cor_enter)
    fechar_btn.bind('<Leave>', mudar_cor_leave)

# -------------------------- VARIÁVEIS -------------------------- #
URL = []                   # Lista para armazenar os links
entries = []               # Lista de Entry para links
cor_bg = "#1A2F4B"         # Cor de fundo principal
cor_botao = "#28548B"      # Cor dos botões
cor_hover = "#3A6BBF"      # Cor dos botões ao passar o mouse
cor_header = "#0F1E33"     # Cor do cabeçalho

# -------------------------- JANELA -------------------------- #
janela = Tk()
janela.title("Análise Esportiva")
janela.configure(bg=cor_bg)
janela.geometry("700x600")

# Configurar expansão da janela
janela.columnconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)

# -------------------------- HEADER -------------------------- #
header = Frame(janela, bg=cor_header, height=70)
header.grid(row=0, column=0, sticky="ew")
header.pack_propagate(False)

titulo = Label(
    header, 
    text="ANÁLISE ESPORTIVA",
    bg=cor_header, fg="white", 
    font=("Arial", 18, "bold")
)
titulo.pack(pady=15)

# -------------------------- MAIN CONTENT -------------------------- #
main_content = Frame(janela, bg=cor_bg)
main_content.grid(row=1, column=0, sticky="nsew")
main_content.columnconfigure(0, weight=1)
main_content.rowconfigure(2, weight=1)  # Links container expandível

# Aviso no topo
aviso_frame = Frame(main_content, bg=cor_bg, pady=10)
aviso_frame.grid(row=0, column=0, sticky="ew")

aviso_label = Label(
    aviso_frame, 
    text="* Obrigatório preencher pelo menos um link de vídeo para análise",
    bg=cor_bg, fg="#FFD700", 
    font=("Arial", 10, "italic")
)
aviso_label.pack(anchor="w", padx=20)

# Informações da partida
info_frame = Frame(main_content, bg=cor_bg, padx=20, pady=10)
info_frame.grid(row=1, column=0, sticky="ew")
info_frame.columnconfigure(1, weight=1)

# Partida
partida_label = Label(info_frame, text="Partida:", bg=cor_bg, fg="white", 
                     font=("Arial", 12, "bold"), width=10, anchor="e")
partida_label.grid(row=0, column=0, pady=5, sticky="e")

partida_entry = Entry(info_frame, font=("Arial", 12), bg="#F0F0F0")
partida_entry.grid(row=0, column=1, pady=5, sticky="ew", padx=(5, 0))

# Observações (antigo complemento)
obs_label = Label(info_frame, text="Observações:", bg=cor_bg, fg="white", 
                 font=("Arial", 12, "bold"), width=10, anchor="e")
obs_label.grid(row=1, column=0, pady=5, sticky="ne")

complemento_text = Text(info_frame, height=4, font=("Arial", 12), bg="#F0F0F0", wrap=WORD)
complemento_text.grid(row=1, column=1, pady=5, sticky="ew", padx=(5, 0))

# Container para links com barra de rolagem
links_frame = Frame(main_content, bg=cor_bg, padx=20, pady=10)
links_frame.grid(row=2, column=0, sticky="nsew")
links_frame.columnconfigure(0, weight=1)
links_frame.rowconfigure(1, weight=1)

links_label = Label(links_frame, text="Links das Paginas que serão analisadas:", bg=cor_bg, fg="white", 
                   font=("Arial", 12, "bold"))
links_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

# Canvas para rolagem
canvas = Canvas(links_frame, bg=cor_bg, highlightthickness=0)
canvas.grid(row=1, column=0, sticky="nsew")

scrollbar = Scrollbar(links_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)

# Frame dentro do canvas
links_container = Frame(canvas, bg=cor_bg)
canvas.create_window((0, 0), window=links_container, anchor="nw", width=canvas.winfo_reqwidth())
links_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Primeiro link (sempre presente)
link_frame = Frame(links_container, bg=cor_bg)
link_frame.pack(fill=X, pady=5)

link1_label = Label(link_frame, text="Link 1:", bg=cor_bg, fg="white", 
                   font=("Arial", 11), width=8, anchor="e")
link1_label.pack(side=LEFT, padx=(5, 5))

first_entry = Entry(link_frame, font=("Arial", 11), bg="#F0F0F0")
first_entry.pack(side=LEFT, fill=X, expand=True)
entries.append(first_entry)

# Frame para botões
buttons_frame = Frame(main_content, bg=cor_bg, padx=20, pady=15)
buttons_frame.grid(row=3, column=0, sticky="ew")

# Botão para adicionar link
add_button = Button(
    buttons_frame, 
    text="Adicionar Link", 
    command=adicionar_link,
    font=("Arial", 11), 
    bg=cor_botao, 
    fg="white",
    padx=15,
    pady=5
)
add_button.pack(side=LEFT, padx=(0, 10))
add_button.bind('<Enter>', mudar_cor_enter)
add_button.bind('<Leave>', mudar_cor_leave)

# Botão para limpar
limpar_button = Button(
    buttons_frame, 
    text="Limpar Campos", 
    command=limpar_campos,
    font=("Arial", 11), 
    bg="#8B0000", 
    fg="white",
    padx=15,
    pady=5
)
limpar_button.pack(side=LEFT, padx=(0, 10))
limpar_button.bind('<Enter>', lambda e: e.widget.config(bg="#C00000"))
limpar_button.bind('<Leave>', lambda e: e.widget.config(bg="#8B0000"))

# Botão para ajuda
ajuda_button = Button(
    buttons_frame, 
    text="Dicas e Ajuda", 
    command=abrir_ajuda,
    font=("Arial", 11), 
    bg="#006400", 
    fg="white",
    padx=15,
    pady=5
)
ajuda_button.pack(side=LEFT)
ajuda_button.bind('<Enter>', lambda e: e.widget.config(bg="#008800"))
ajuda_button.bind('<Leave>', lambda e: e.widget.config(bg="#006400"))

# Adicione este botão no buttons_frame, logo após o ajuda_button
prompt_button = Button(
    buttons_frame, 
    text="Prompts", 
    command=copiar_prompt,
    font=("Arial", 11), 
    bg=cor_botao, 
    fg="white",
    padx=15,
    pady=5
)
prompt_button.pack(side=LEFT, padx=(10, 0))
prompt_button.bind('<Enter>', mudar_cor_enter)
prompt_button.bind('<Leave>', mudar_cor_leave)


sugestoes_button = Button(
    buttons_frame, 
    text="Sugestões", 
    command=mostrar_sugestoes,
    font=("Arial", 11), 
    bg="#006400", 
    fg="white",
    padx=15,
    pady=5
)
sugestoes_button.pack(side=LEFT, padx=(10, 0))
sugestoes_button.bind('<Enter>', lambda e: e.widget.config(bg="#008800"))
sugestoes_button.bind('<Leave>', lambda e: e.widget.config(bg="#006400"))


# Botão principal
iniciar_button = Button(
    main_content, 
    text="INICIAR ANÁLISE", 
    command=iniciar_analise,
    font=("Arial", 12, "bold"), 
    bg="#1E4D8C", 
    fg="white",
    padx=20,
    pady=8
)
iniciar_button.grid(row=4, column=0, pady=15)
iniciar_button.bind('<Enter>', lambda e: e.widget.config(bg="#2E6DB6"))
iniciar_button.bind('<Leave>', lambda e: e.widget.config(bg="#1E4D8C"))

# Configurar a rolagem com o mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Função para redimensionar o canvas quando a janela for redimensionada
def resize_canvas(event):
    canvas_width = event.width - scrollbar.winfo_reqwidth() - 5
    canvas.itemconfig(1, width=canvas_width)  # 1 é o ID da janela criada

links_frame.bind("<Configure>", resize_canvas)

# Inicia o loop principal da janela
janela.mainloop()