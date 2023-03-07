import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import json

# Definir credenciais do serviço Computer Vision da Azure
endpoint = "https://imagens.cognitiveservices.azure.com/"
subscription_key = "799b51454e494fcf98a9dda3fb7528dd"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Criar janela
janela = tk.Tk()
janela.title("Análise de Imagens")
janela.geometry("800x600")

# Função para analisar a imagem
def analisar_imagem():
    # Obter caminho da imagem selecionada
    imagem_path = filedialog.askopenfilename()

    # Exibir a imagem selecionada na interface
    imagem = Image.open(imagem_path)
    imagem = imagem.resize((300, 300), Image.ANTIALIAS)
    imagem = ImageTk.PhotoImage(imagem)
    imagem_label.configure(image=imagem)
    imagem_label.image = imagem

    # Analisar a imagem selecionada
    with open(imagem_path, "rb") as imagem_arquivo:
        resultado = computervision_client.analyze_image_in_stream(imagem_arquivo, visual_features=["Categories", "Tags"])

    # Exibir resultado da análise na interface
    categorias_tree.delete(*categorias_tree.get_children())
    for categoria in resultado.categories:
        categorias_tree.insert("", "end", text=categoria.name, values=categoria.score)
    tags_tree.delete(*tags_tree.get_children())
    for tag in resultado.tags:
        tags_tree.insert("", "end", text=tag.name, values=tag.confidence)

# Criar botão para carregar a imagem
botao_carregar_imagem = tk.Button(janela, text="Carregar imagem", command=analisar_imagem)
botao_carregar_imagem.pack()

# Criar frame para exibir a imagem selecionada
imagem_frame = tk.Frame(janela)
imagem_frame.pack(side="left", fill="both", expand=True)

imagem_label = tk.Label(imagem_frame)
imagem_label.pack(fill="both", expand=True)

# Criar frame para exibir as informações de categorias e tags
info_frame = tk.Frame(janela)
info_frame.pack(side="right", fill="both", expand=True)

# Criar tabela para exibir as categorias
categorias_label = tk.Label(info_frame, text="Categorias")
categorias_label.pack()
categorias_tree = tk.ttk.Treeview(info_frame, columns=["Score"])
categorias_tree.heading("#0", text="Categoria")
categorias_tree.heading("Score", text="Score")
categorias_tree.pack(fill="both", expand=True)

# Criar tabela para exibir as tags
tags_label = tk.Label(info_frame, text="Tags")
tags_label.pack()
tags_tree = tk.ttk.Treeview(info_frame, columns=["Confidence"])
tags_tree.heading("#0", text="Tag")
tags_tree.heading("Confidence", text="Confidence")
tags_tree.pack(fill="both", expand=True)

# Iniciar a janela
janela.mainloop()
