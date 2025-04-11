import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
from datetime import datetime
from tkinter import filedialog

# Função para buscar a temperatura
def buscar_temperatura():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-23.5505&longitude=-46.6333&current_weather=true"
        response = requests.get(url)
        data = response.json()
        temperatura = data["current_weather"]["temperature"]
        hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Adicionar os dados ao texto exibido
        texto_resultados.insert(tk.END, f"São Paulo - Temperatura: {temperatura}°C | Data e Hora: {hora_atual}\n")
        resultados.append({"Local": "São Paulo", "Temperatura": temperatura, "Data e Hora": hora_atual})
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível buscar os dados: {e}")

# Função para exportar os dados para Excel
def exportar_excel():
    try:
        # Abrir o diálogo para escolher a pasta e salvar o arquivo
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Arquivo Excel", "*.xlsx")])
        if file_path:  # Caso o usuário tenha selecionado um caminho
            df = pd.DataFrame(resultados)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Dados exportados para '{file_path}'")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível exportar os dados: {e}")

# Lista para armazenar os resultados
resultados = []

# Interface Tkinter
janela = tk.Tk()
janela.title("Temperatura de São Paulo")

botao_buscar = tk.Button(janela, text="Buscar Temperatura", command=buscar_temperatura)
botao_buscar.pack(pady=10)

texto_resultados = tk.Text(janela, width=50, height=15)
texto_resultados.pack(pady=10)

botao_exportar = tk.Button(janela, text="Exportar para Excel", command=exportar_excel)
botao_exportar.pack(pady=10)

janela.mainloop()
