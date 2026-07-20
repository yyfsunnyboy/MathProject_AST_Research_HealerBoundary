import json


def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    if level == 1:
        question_text = r"Calculate $(-3)^3$."
        correct_answer = -27
        
        oracle_payload = {"base": base, "exponent": exponent}
        
        return {
            "question_text": question_text,
            "correct_answer": correct_answer,
            "oracle_payload": json.dumps(oracle_payload)
        }