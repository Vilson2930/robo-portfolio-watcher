"""
ROBO GLOBAL - DIRECTIONAL + OPERATIONAL + BALANCEAMENTO
Versão: 1.0
Execução: Cloud / GitHub Actions / Colab
"""

# === IMPORTA MOTOR OPERACIONAL (AUXILIAR) ===
from auxiliar import motor_operacional

# ============================================================
# 1. MACRO ENGINE (DIRECIONAL DOMINANTE)
# ============================================================

def macro_engine(macro_score: float) -> dict:
    if macro_score >= 65:
        state = "BOM"
        bias = "RISCO"
    elif macro_score >= 45:
        state = "NEUTRO"
        bias = "MISTO"
    else:
        state = "RUIM"
        bias = "DEFENSIVO"

    return {
        "macro_score": macro_score,
        "macro_state": state,
        "macro_bias": bias
    }


# ============================================================
# 2. MARKET ENGINE (CONFIRMAÇÃO)
# ============================================================

MARKETS = {
    "SP500":  {"internal_score": 68},
    "EUROPA": {"internal_score": 62},
    "OURO":   {"internal_score": 35}
}

def market_engine(market: str, macro: dict) -> dict:
    internal_score = MARKETS[market]["internal_score"]

    final_score = (
        macro["macro_score"] * 0.7 +
        internal_score * 0.3
    )

    if final_score >= 60:
        decision = "COMPRA"
    elif final_score >= 45:
        decision = "MANTER"
    else:
        decision = "REDUZIR"

    return {
        "market": market,
        "internal_score": internal_score,
        "final_score": round(final_score, 1),
        "decision": decision
    }
# ==================================================
# 2. MOTOR OPERACIONAL (AUXILIAR)
# ==================================================

def executar_operacional(resultado_mercado: dict, peso_atual: float) -> dict:
    """
    Converte a decisão estratégica em ação operacional
    usando o motor auxiliar (auxiliar.py)
    """
    return motor_operacional(
        mercado=resultado_mercado["market"],
        score_final=resultado_mercado["final_score"],
        peso_atual=peso_atual
    )


# ============================================================
# 3. BALANCEAMENTO DE PORTFÓLIO
# ============================================================

TARGET_WEIGHTS = {
    "SP500": 0.40,
    "EUROPA": 0.30,
    "OURO": 0.20
}

def rebalance_portfolio(market_result: dict, current_weight: float) -> dict:
    decision = market_result["decision"]
    target = TARGET_WEIGHTS[market_result["market"]]

    if decision == "COMPRA":
        new_weight = min(current_weight + 0.05, target)
        action = "AUMENTAR"
    elif decision == "REDUZIR":
        new_weight = max(current_weight - 0.05, 0)
        action = "REDUZIR"
    else:
        new_weight = current_weight
        action = "MANTER"

    return {
        "market": market_result["market"],
        "decision": decision,
        "current_weight": current_weight,
        "target_weight": target,
        "new_weight": round(new_weight, 2),
        "action": action
    }


# ============================================================
# 4. EXECUÇÃO FINAL (OUTPUT DO ROBO)
# ============================================================

if __name__ == "__main__":

    # INPUT MACRO (vem do notebook direcional)
    macro_score = 70

    # PESOS ATUAIS DO PORTFÓLIO
    portfolio = {
        "SP500": 0.35,
        "EUROPA": 0.25,
        "OURO": 0.25
    }

    print("\n========== MACRO ==========")
    macro = macro_engine(macro_score)
    print(macro)

    print("\n====== DECISÃO POR MERCADO ======")
    market_results = {}
    for m in MARKETS:
        res = market_engine(m, macro)
        market_results[m] = res
        print(res)

    print("\n====== BALANCEAMENTO ======")
    for m in portfolio:
        reb = rebalance_portfolio(
            market_results[m],
            portfolio[m]
        )
        print(reb)

    print("\nROBO EXECUTADO COM SUCESSO.")
