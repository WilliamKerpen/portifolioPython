import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import pandas as pd
from datetime import datetime

# Função para buscar a temperatura e umidade
def buscar_temperatura():
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=-23.5505&longitude=-46.6333"
            "&current_weather=true"
            "&hourly=relative_humidity_2m"
            "&timezone=America/Sao_Paulo"
        )
        response = requests.get(url)
        data = response.json()

        temperatura = data["current_weather"]["temperature"]
        hora_atual = datetime.now().strftime("%Y-%m-%dT%H:00")  # formato exato da API para hora
        hora_legivel = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Procurar a umidade na lista de horas
        horarios = data["hourly"]["time"]
        umidades = data["hourly"]["relative_humidity_2m"]

        if hora_atual in horarios:
            indice = horarios.index(hora_atual)
            umidade = umidades[indice]
        else:
            umidade = "N/D"

        texto_resultados.insert(tk.END,
            f"São Paulo - Temperatura: {temperatura}°C | Umidade: {umidade}% | Data e Hora: {hora_legivel}\n"
        )

        resultados.append({
            "Local": "São Paulo",
            "Temperatura (°C)": temperatura,
            "Umidade (%)": umidade,
            "Data e Hora": hora_legivel
        })

    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível buscar os dados: {e}")

# Função para exportar os dados para Excel
def exportar_excel():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Arquivo Excel", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(resultados)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Dados exportados para '{file_path}'")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível exportar os dados: {e}")

# Lista para armazenar os resultados
resultados = []

# Interface Tkinter
janela = tk.Tk()
janela.title("Temperatura e Umidade - São Paulo")

botao_buscar = tk.Button(janela, text="Buscar Dados", command=buscar_temperatura)
botao_buscar.pack(pady=10)

texto_resultados = tk.Text(janela, width=60, height=15)
texto_resultados.pack(pady=10)

botao_exportar = tk.Button(janela, text="Exportar para Excel", command=exportar_excel)
botao_exportar.pack(pady=10)

janela.mainloop()
