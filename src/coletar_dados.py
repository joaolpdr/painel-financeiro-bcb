import requests
import pandas as pd
from datetime import datetime, timedelta
import time

# ── Configurações ─────────────────────────────────────────
DATA_INICIO = (datetime.now() - timedelta(days=365)).strftime("%m-%d-%Y")
DATA_FIM    = datetime.now().strftime("%m-%d-%Y")

DATA_INICIO_SGS = (datetime.now() - timedelta(days=365)).strftime("%d/%m/%Y")
DATA_FIM_SGS    = datetime.now().strftime("%d/%m/%Y")


# ── Helpers ───────────────────────────────────────────────
def requisitar(url: str, params: dict = None) -> dict | list | None:
    """Faz requisição GET com tratamento de erro."""
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"⚠️  Timeout na URL: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"⚠️  Erro HTTP {e.response.status_code}: {url}")
    except requests.exceptions.ConnectionError:
        print(f"⚠️  Sem conexão: {url}")
    except Exception as e:
        print(f"⚠️  Erro inesperado: {e}")
    return None


# ── Cotações PTAX ─────────────────────────────────────────
def coletar_ptax(moeda: str, simbolo: str) -> pd.DataFrame:
    """Coleta cotação histórica de uma moeda via API PTAX do BCB."""
    url = (
        f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@moeda='{moeda}'"
        f"&@dataInicial='{DATA_INICIO}'"
        f"&@dataFinalCotacao='{DATA_FIM}'"
        f"&$filter=tipoBoletim%20eq%20'Fechamento'"
        f"&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
        f"&$format=json"
        f"&$top=300"
    )

    data = requisitar(url)

    if not data or "value" not in data or not data["value"]:
        print(f"⚠️  Sem dados para {simbolo}")
        return pd.DataFrame()

    df = pd.DataFrame(data["value"])
    df["data"]  = pd.to_datetime(df["dataHoraCotacao"]).dt.date
    df["moeda"] = simbolo
    df = df.rename(columns={
        "cotacaoCompra": "compra",
        "cotacaoVenda":  "venda"
    })[["data", "moeda", "compra", "venda"]]

    df = df.sort_values("data").reset_index(drop=True)
    print(f"✅ PTAX {simbolo}: {len(df)} registros coletados")
    return df

# ── Séries temporais SGS ──────────────────────────────────
def coletar_serie_sgs(codigo: int, nome: str) -> pd.DataFrame:
    """Coleta série temporal do SGS (Sistema Gerenciador de Séries do BCB)."""
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
        f"?formato=json&dataInicial={DATA_INICIO_SGS}&dataFinal={DATA_FIM_SGS}"
    )

    data = requisitar(url)

    if not data:
        print(f"⚠️  Sem dados para {nome}")
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["data"]  = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["serie"] = nome
    df = df[["data", "serie", "valor"]].dropna()

    print(f"✅ {nome}: {len(df)} registros coletados")
    return df


# ── Execução principal ────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  COLETANDO DADOS — BANCO CENTRAL DO BRASIL")
    print("=" * 50)

    # Cotações
    print("\n📌 Cotações PTAX:")
    moedas = [
        ("USD", "Dólar"),
        ("EUR", "Euro"),
        ("GBP", "Libra"),
    ]

    dfs_ptax = []
    for codigo, simbolo in moedas:
        df = coletar_ptax(codigo, simbolo)
        if not df.empty:
            dfs_ptax.append(df)
        time.sleep(0.5)  # respeita o rate limit da API

    if dfs_ptax:
        df_ptax = pd.concat(dfs_ptax, ignore_index=True)
        df_ptax.to_csv("data/raw/cotacoes.csv", index=False)
        print(f"\n💾 Cotações salvas: {len(df_ptax)} registros")

    # Séries econômicas
    print("\n📌 Séries econômicas:")
    series = [
        (433,  "IPCA"),
        (11,   "Selic"),
        (12,   "CDI"),
    ]

    dfs_series = []
    for codigo, nome in series:
        df = coletar_serie_sgs(codigo, nome)
        if not df.empty:
            dfs_series.append(df)
        time.sleep(0.5)

    if dfs_series:
        df_series = pd.concat(dfs_series, ignore_index=True)
        df_series.to_csv("data/raw/series_economicas.csv", index=False)
        print(f"\n💾 Séries salvas: {len(df_series)} registros")

    print("\n✅ Coleta finalizada")