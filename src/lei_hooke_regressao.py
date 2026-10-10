"""
Determinacao Experimental da Constante Elastica de uma Mola (Lei de Hooke).
Ajuste linear por Minimos Quadrados: F = k * x + b
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def carregar_dados(caminho_json: Path) -> tuple[np.ndarray, np.ndarray]:
    with open(caminho_json, "r", encoding="utf-8") as f:
        conteudo = json.load(f)
    
    alongamentos = [item["alongamento_m"] for item in conteudo["dados"]]
    forcas = [item["forca_N"] for item in conteudo["dados"]]
    return np.array(alongamentos), np.array(forcas)

def executar_regressao(x: np.ndarray, F: np.ndarray):
    # Ajuste linear (Regressão Linear de grau 1: F = k*x + b)
    coeficientes = np.polyfit(x, F, 1)
    k = coeficientes[0] # Constante elástica (inclinação da reta em N/m)
    b = coeficientes[1] # Intercepto em N
    return k, b

def gerar_grafico(x: np.ndarray, F: np.ndarray, k: float, b: float, caminho_saida: Path):
    linha_tendencia = k * x + b
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    
    # Plotagem dos pontos e linha de ajuste
    ax.scatter(x, F, color='#00FFFF', s=70, label='Dados Experimentais', zorder=5)
    ax.plot(x, linha_tendencia, color='#FF6B00', linewidth=2, label=f'Ajuste MMQ: $F = {k:.2f}x {b:+.4f}$')
    
    # Estilização
    ax.set_title('Lei de Hooke: Força vs. Alongamento', fontsize=14, pad=15, fontweight='bold')
    ax.set_xlabel(r'Alongamento $\Delta x$ (m)', fontsize=12)
    ax.set_ylabel('Força $F$ (N)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.legend(fontsize=11)
    
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(caminho_saida, bbox_inches='tight')
    plt.close()
    print(f"Gráfico salvo com sucesso em: {caminho_saida}")

def main():
    diretorio_raiz = Path(__file__).resolve().parent.parent
    caminho_json = diretorio_raiz / "data" / "dados_hooke.json"
    caminho_grafico = diretorio_raiz / "assets" / "grafico_lei_hooke.png"
    
    x, F = carregar_dados(caminho_json)
    k, b = executar_regressao(x, F)
    
    print("=" * 55)
    print("  RESULTADOS DA REGRESSÃO LINEAR - LEI DE HOOKE")
    print("=" * 55)
    print(f"Constante elástica da mola (k): {k:.2f} N/m")
    print(f"Intercepto da reta (b):        {b:.4f} N")
    print(f"Equação da Força:              F(x) = {k:.2f} * x {b:+.4f}")
    print("=" * 55)
    
    gerar_grafico(x, F, k, b, caminho_grafico)

if __name__ == "__main__":
    main()
