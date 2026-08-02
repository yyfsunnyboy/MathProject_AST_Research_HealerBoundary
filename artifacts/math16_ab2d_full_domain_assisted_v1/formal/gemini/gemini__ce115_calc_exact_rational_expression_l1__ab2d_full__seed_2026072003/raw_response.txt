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
    
    term1 = FractionOps.mul(FractionOps.create(p1["left"]), FractionOps.create(p1["right"]))
    if p1["sign"] == -1:
        term1 = FractionOps.sub(FractionOps.create(0), term1)
        
    term2 = FractionOps.mul(FractionOps.create(p2["left"]), FractionOps.create(p2["right"]))
    if p2["sign"] == -1:
        term2 = FractionOps.sub(FractionOps.create(0), term2)
        
    result = FractionOps.add(term1, term2)
    
    exact_val = FractionOps.to_exact(result)
    value_str = str(exact_val)
    canonical_latex = FractionOps.to_latex(result)
    
    question_text = "精確計算\n\\[\n2.79\\times 89.3-\\left(-0.21\\times 89.3\\right).\n\\]\n答案不得使用近似值。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "value": value_str,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }