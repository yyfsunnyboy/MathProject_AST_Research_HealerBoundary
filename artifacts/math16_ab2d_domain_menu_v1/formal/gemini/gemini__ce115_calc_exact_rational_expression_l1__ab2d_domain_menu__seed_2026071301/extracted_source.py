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
    
    p1_left = FractionOps.create(frozen_params["products"][0]["left"])
    p1_right = FractionOps.create(frozen_params["products"][0]["right"])
    p1 = FractionOps.mul(p1_left, p1_right)
    
    p2_left = FractionOps.create(frozen_params["products"][1]["left"])
    p2_right = FractionOps.create(frozen_params["products"][1]["right"])
    p2 = FractionOps.mul(p2_left, p2_right)
    
    result = FractionOps.sub(p1, p2)
    
    val_str = str(FractionOps.to_exact(result))
    latex_str = FractionOps.to_latex(result)
    
    return {
        "question_text": "精確計算\n\\[\n2.79\\times 89.3-\\left(-0.21\\times 89.3\\right).\n\\]\n答案不得使用近似值。",
        "correct_answer": {
            "value": val_str,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }