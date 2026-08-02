from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    question_text = "精確計算\n\\[\n2.79\\times 89.3-\\left(-0.21\\times 89.3\\right).\n\\]\n答案不得使用近似值。"
    
    oracle_payload = {
      "products": [
        {
          "left": "2.79",
          "right": "89.3",
          "sign": 1
        },
        {
          "left": "-0.21",
          "right": "89.3",
          "sign": -1
        }
      ]
    }
    
    p1 = oracle_payload["products"][0]
    p2 = oracle_payload["products"][1]
    
    left1 = FractionOps.create(p1["left"])
    right1 = FractionOps.create(p1["right"])
    term1 = FractionOps.mul(left1, right1)
    
    left2 = FractionOps.create(p2["left"])
    right2 = FractionOps.create(p2["right"])
    term2 = FractionOps.mul(left2, right2)
    
    # Since sign of term2 is -1, we subtract it: term1 - term2
    result = FractionOps.sub(term1, term2)
    
    exact_val = FractionOps.to_exact(result)
    value_str = str(exact_val)
    canonical_latex = FractionOps.to_latex(result)
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }