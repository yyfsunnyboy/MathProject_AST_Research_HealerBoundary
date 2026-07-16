def generate(level=1, **kwargs):
    radicand_input = kwargs.get("radicand", 27)
    
    import math
    coefficient = 1
    radicand_output = radicand_input
    for i in range(int(math.isqrt(radicand_input)), 0, -1):
        if radicand_input % (i * i) == 0:
            coefficient = i
            radicand_output = radicand_input // (i * i)
            break
            
    return {
        "question_text": f"Simplify the radical: \\sqrt{{{radicand_input}}}",
        "correct_answer": {
            "coefficient": coefficient,
            "radicand": radicand_output
        },
        "oracle_payload": {
            "radicand": radicand_input
        }
    }