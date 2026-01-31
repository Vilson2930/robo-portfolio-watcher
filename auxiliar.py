# auxiliar.py

BANDA = 5
DELTA = 0.05
PESO_MIN = 0.05
PESO_MAX = 0.40


def motor_operacional(mercado, score_final, peso_atual):
    # decisão com banda
    if score_final >= 65 + BANDA:
        decisao = "COMPRA"
        ajuste = DELTA
    elif score_final <= 45 - BANDA:
        decisao = "VENDA"
        ajuste = -DELTA
    else:
        decisao = "MANTER"
        ajuste = 0.0

    novo_peso = peso_atual + ajuste
    novo_peso = max(PESO_MIN, min(PESO_MAX, novo_peso))

    return {
        "mercado": mercado,
        "decisao": decisao,
        "ajuste": ajuste,
        "novo_peso": round(novo_peso, 2)
    }
