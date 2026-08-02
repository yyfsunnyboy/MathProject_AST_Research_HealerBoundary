from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
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
    
    p1 = frozen_params["products"][0]
    p2 = frozen_params["products"][1]
    
    left1 = FractionOps.create(p1["left"])
    right1 = FractionOps.create(p1["right"])
    prod1 = FractionOps.mul(left1, right1)
    
    left2 = FractionOps.create(p2["left"])
    right2 = FractionOps.create(p2["right"])
    prod2 = FractionOps.mul(left2, right2)
    
    # Since sign of p2 is -1, we subtract prod2
    result = FractionOps.sub(prod1, prod2)
    
    val_str = str(FractionOps.to_exact(result))
    latex_str = FractionOps.to_latex(result)
    
    question_text = "精確計算\n\\[\n2.79\\times 89.3-\\left(-0.21\\times 89.3\\right).\n\\]\n答案不得使用近似值。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": val_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }