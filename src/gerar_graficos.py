import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ── Configurações visuais ─────────────────────────────────
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.figsize"] = (11, 5)

CORES_MOEDAS = {
    "Dólar": "#2980b9",
    "Euro":  "#2ecc71",
    "Libra": "#e74c3c",
}

os.makedirs("output", exist_ok=True)


def formatar_eixo_data(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")


# ── Gráfico 1 — Evolução das cotações ────────────────────
def grafico_cotacoes(df_ptax):
    fig, ax = plt.subplots()

    for moeda, grupo in df_ptax.groupby("moeda"):
        grupo = grupo.copy()
        grupo["data"] = pd.to_datetime(grupo["data"])
        ax.plot(
            grupo["data"],
            grupo["venda"],
            label=moeda,
            color=CORES_MOEDAS.get(moeda, "#888"),
            linewidth=2
        )

    formatar_eixo_data(ax)
    ax.set_title("Evolução das Cotações — Últimos 12 Meses", fontsize=14, fontweight="bold")
    ax.set_xlabel("Data")
    ax.set_ylabel("Cotação (R$)")
    ax.legend(title="Moeda")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/01_evolucao_cotacoes.png", dpi=150)
    plt.close()
    print("✅ 01_evolucao_cotacoes.png")


# ── Gráfico 2 — Variação percentual mensal por moeda ─────
def grafico_variacao_mensal(df_ptax):
    fig, ax = plt.subplots()

    for moeda, grupo in df_ptax.groupby("moeda"):
        grupo = grupo.copy()
        grupo["data"] = pd.to_datetime(grupo["data"])
        grupo = grupo.set_index("data").resample("ME")["venda"].last()
        variacao = grupo.pct_change() * 100

        ax.plot(
            variacao.index,
            variacao.values,
            label=moeda,
            color=CORES_MOEDAS.get(moeda, "#888"),
            linewidth=2,
            marker="o",
            markersize=4
        )

    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    formatar_eixo_data(ax)
    ax.set_title("Variação Mensal das Cotações (%)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Variação (%)")
    ax.legend(title="Moeda")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/02_variacao_mensal.png", dpi=150)
    plt.close()
    print("✅ 02_variacao_mensal.png")


# ── Gráfico 3 — Selic e CDI ──────────────────────────────
def grafico_selic_cdi(df_series):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, serie, cor in [
        (axes[0], "Selic", "#2980b9"),
        (axes[1], "CDI",   "#e74c3c")
    ]:
        grupo = df_series[df_series["serie"] == serie].copy()
        grupo["data"] = pd.to_datetime(grupo["data"])
        ax.plot(grupo["data"], grupo["valor"], color=cor, linewidth=2)
        ax.set_title(f"Evolução da {serie} — Últimos 12 Meses", fontsize=12, fontweight="bold")
        ax.set_xlabel("Data")
        ax.set_ylabel("Taxa (% a.m.)")
        ax.grid(axis="y", alpha=0.3)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")

        # Valor atual no final da linha
        ultimo = grupo.iloc[-1]
        ax.annotate(
            f"{ultimo['valor']:.4f}%",
            xy=(ultimo["data"], ultimo["valor"]),
            xytext=(10, 0),
            textcoords="offset points",
            fontsize=9,
            color=cor,
            fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig("output/03_selic_cdi.png", dpi=150)
    plt.close()
    print("✅ 03_selic_cdi.png")

# ── Gráfico 4 — IPCA acumulado ────────────────────────────
def grafico_ipca(df_series):
    ipca = df_series[df_series["serie"] == "IPCA"].copy()
    ipca["data"] = pd.to_datetime(ipca["data"])
    ipca = ipca.sort_values("data")
    ipca["acumulado"] = ipca["valor"].cumsum()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Mensal
    axes[0].bar(
        ipca["data"],
        ipca["valor"],
        color="#f39c12",
        width=20,
        edgecolor="white"
    )
    axes[0].set_title("IPCA Mensal (%)", fontsize=13, fontweight="bold")
    axes[0].set_xlabel("Mês")
    axes[0].set_ylabel("Variação (%)")
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=30, ha="right")
    axes[0].grid(axis="y", alpha=0.3)

    # Acumulado
    axes[1].plot(
        ipca["data"],
        ipca["acumulado"],
        color="#e74c3c",
        linewidth=2,
        marker="o",
        markersize=4
    )
    axes[1].set_title("IPCA Acumulado (%)", fontsize=13, fontweight="bold")
    axes[1].set_xlabel("Mês")
    axes[1].set_ylabel("Acumulado (%)")
    axes[1].xaxis.set_major_formatter(mdates.DateFormatter("%b/%y"))
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=30, ha="right")
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/04_ipca.png", dpi=150)
    plt.close()
    print("✅ 04_ipca.png")


# ── Execução ──────────────────────────────────────────────
if __name__ == "__main__":
    df_ptax   = pd.read_csv("data/raw/cotacoes.csv")
    df_series = pd.read_csv("data/raw/series_economicas.csv")

    print("📊 Gerando gráficos...\n")
    grafico_cotacoes(df_ptax)
    grafico_variacao_mensal(df_ptax)
    grafico_selic_cdi(df_series)
    grafico_ipca(df_series)

    print("\n✅ Todos os gráficos gerados em output/")