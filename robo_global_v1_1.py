"""
ROBO GLOBAL – DIRECTIONAL + OPERATIONAL + BALANCEAMENTO + RISCO
Versão: 1.1 (ROBÔ 10/10)
Execução: GitHub Actions / Colab / Cloud
"""

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

BANDA_DECISAO = 5          # banda anti-ruído
MAX_WEIGHT = 0.40         # peso máximo por ativo
MIN_WEIGHT = 0.05         # peso mínimo por ativo

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
# 2. MOTOR POR MERCADO (OPERACIONAL)
# ============================================================

def market_engine(market: str, internal_score: float, macro: dict) -> dict:
    macro_score = macro["macro_score"]

    # Score final ponderado
    final_score = round(0.7 * macro_score + 0.3 * internal_score, 1)

    # Decisão com banda
    if final_score >= 65 + BANDA_DECISAO:
        decision = "COMPRA"
    elif final_score <= 45 - BANDA_DECISAO:
        decision = "VENDA"
    else:
        decision = "MANTER"

    # Confiança
    if abs(final_score - macro_score) <= 5:
        confidence = "ALTA"
    else:
        confidence = "MEDIA"

    return {
        "market": market,
        "internal_score": internal_score,
        "final_score": final_score,
        "decision": decision,
        "confidence": confidence
    }

# ============================================================
# 3. BALANCEAMENTO COM PERCENTUAL CLARO
# ============================================================

def portfolio_balance(result: dict, current_weight: float) -> dict:
    decision = result["decision"]

    if decision == "COMPRA":
        delta = 0.05
    elif decision == "VENDA":
        delta = -0.05
    else:
        delta = 0.0

    new_weight = round(current_weight + delta, 2)
    new_weight = min(MAX_WEIGHT, max(MIN_WEIGHT, new_weight))

    return {
        "market": result["market"],
        "decision": decision,
        "current_weight": current_weight,
        "new_weight": new_weight,
        "action": "AUMENTAR" if delta > 0 else "REDUZIR" if delta < 0 else "MANTER"
    }

# ============================================================
# 4. EXECUÇÃO FINAL (EXEMPLO REAL)
# ============================================================

def run_bot():
    print("\n======== MACRO ========")
    macro = macro_engine(70)
    print(macro)

    print("\n===== DECISÃO POR MERCADO =====")
    sp = market_engine("SP500", 68, macro)
    eu = market_engine("EUROPA", 62, macro)
    ou = market_engine("OURO", 35, macro)

    print(sp)
    print(eu)
    print(ou)

    print("\n===== BALANCEAMENTO =====")
    print(portfolio_balance(sp, 0.35))
    print(portfolio_balance(eu, 0.25))
    print(portfolio_balance(ou, 0.25))

    print("\nROBÔ EXECUTADO COM SUCESSO.")

# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    run_bot()
