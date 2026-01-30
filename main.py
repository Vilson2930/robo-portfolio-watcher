# main.py
# Observador de Portfólio – NÃO operacional
# Executa leitura macro + ativos e imprime orientação

from datetime import datetime

def macro_dashboard(macro_output):
    score = macro_output["macro_score"]

    if score >= 60:
        state = "BOM"
        guidance = "Ambiente favorável a risco"
    elif score >= 40:
        state = "NEUTRO"
        guidance = "Ambiente misto / cautela"
    else:
        state = "RUIM"
        guidance = "Ambiente defensivo"

    return {
        "macro_score": score,
        "macro_state": state,
        "guidance": guidance
    }

def portfolio_watcher(asset, macro_score, asset_score, weight):
    if macro_score >= 60 and asset_score >= 60:
        action = "MANTER / AUMENTAR LEVEMENTE"
    elif asset_score < 60:
        action = "REDUZIR EXPOSIÇÃO"
    else:
        action = "MANTER"

    return {
        "ativo": asset,
        "macro_score": macro_score,
        "score_ativo": asset_score,
        "peso": weight,
        "orientacao": action
    }

# ===== EXECUÇÃO =====
macro_output = {"macro_score": 70}
macro = macro_dashboard(macro_output)

portfolio = [
    portfolio_watcher("SP500", macro["macro_score"], 70, 0.35),
    portfolio_watcher("EUROPA", macro["macro_score"], 70, 0.25),
    portfolio_watcher("OURO", macro["macro_score"], 58, 0.15),
]

print("==== MACRO ====")
print(macro)

print("\n==== PORTFÓLIO ====")
for p in portfolio:
    print(p)

print("\nExecutado em:", datetime.utcnow())
if __name__ == "__main__":
    macro_output = {"macro_score": 70}

    macro_res = macro_dashboard(macro_output)

    print("===== MACRO DASHBOARD =====")
    print(f"Macro score : {macro_res['macro_score']}")
    print(f"Macro state : {macro_res['macro_state']}")
    print(f"Orientação  : {macro_res['guidance']}")
