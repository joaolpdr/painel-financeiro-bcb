# 🏦 Painel Financeiro — Banco Central do Brasil

Pipeline em Python que consome dados reais via APIs públicas do Banco Central
do Brasil, analisa indicadores econômicos e gera um relatório Excel completo
e formatado automaticamente.

---

## 🎯 Problema de negócio

Profissionais de finanças, contabilidade e gestão precisam monitorar
indicadores econômicos como câmbio, Selic e inflação de forma rápida e
confiável. Consultar manualmente cada fonte consome tempo e aumenta o risco
de erro.

---

## 💡 Solução

Pipeline automatizado que com um único comando:
1. Consome dados reais das APIs públicas do BCB
2. Coleta cotações históricas de Dólar, Euro e Libra
3. Coleta evolução da Selic, CDI e IPCA
4. Gera gráficos de evolução e variação
5. Entrega relatório Excel formatado e pronto para uso

---

## 🔌 APIs utilizadas

| API | Dados | Autenticação |
|---|---|---|
| BCB PTAX | Cotações Dólar, Euro e Libra | Não necessária |
| BCB SGS | Selic, CDI e IPCA | Não necessária |

Todas as APIs são públicas, gratuitas e oficiais do Banco Central do Brasil.

---

## 📊 O que o relatório contém

| Aba | Conteúdo |
|---|---|
| Resumo Executivo | Cotações atuais, taxas e variações |
| Cotações | Histórico diário PTAX por moeda |
| Séries Econômicas | Selic, CDI e IPCA históricos |
| Gráficos | 4 painéis visuais embutidos |

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem principal |
| requests | Consumo das APIs REST |
| pandas | Tratamento e análise dos dados |
| matplotlib | Geração dos gráficos |
| openpyxl | Geração do relatório Excel |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## 📁 Estrutura do projeto

```
painel-financeiro-bcb/
│
├── data/
│   ├── raw/                      # Dados brutos coletados das APIs
│   └── processed/                # Dados tratados
│
├── src/
│   ├── coletar_dados.py          # Consumo das APIs do BCB
│   ├── gerar_graficos.py         # Geração dos gráficos
│   └── gerar_relatorio.py        # Geração do relatório Excel
│
├── output/                       # Gráficos e relatório final
├── .env.example                  # Template de variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## 🚀 Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/joaolpdr/painel-financeiro-bcb.git
cd painel-financeiro-bcb
```

**2. Crie e ative o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure o ambiente**
```bash
cp .env.example .env
```

**5. Colete os dados**
```bash
python src/coletar_dados.py
```

**6. Gere os gráficos**
```bash
python src/gerar_graficos.py
```

**7. Gere o relatório Excel**
```bash
python src/gerar_relatorio.py
```

---

## 🔒 Segurança

Nenhuma credencial é exposta no repositório.
O arquivo `.env` está listado no `.gitignore` e nunca é versionado.
O `.env.example` serve como template público sem dados sensíveis.

---

## 👤 Autor

**João Lucas do Prado Ribeiro**
Analista de Governança de Dados | Desenvolvedor Python
[LinkedIn](https://linkedin.com/in/joaolprd) • [GitHub](https://github.com/joaolpdr)