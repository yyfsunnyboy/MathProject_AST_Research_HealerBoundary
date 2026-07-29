def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2=3$, find $a$ and $b$ such that the roots are expressed as $\frac{p \pm q\sqrt{r}}{s}$ with integers satisfying specific ordering constraints. If the ordered pair of coefficients corresponds to a target expression, determine its value for the order constraint 'a>b' where the result is defined by the sum $2a+b$.",
        "correct_answer": {
            "result": 10,
            "rational": None,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": "-\\sqrt{3}"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }