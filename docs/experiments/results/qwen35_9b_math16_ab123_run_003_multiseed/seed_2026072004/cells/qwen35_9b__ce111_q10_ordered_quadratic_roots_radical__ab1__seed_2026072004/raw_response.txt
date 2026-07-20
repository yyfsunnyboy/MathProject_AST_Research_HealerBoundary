def generate(level=1, **kwargs):
    return {
        "question_text": r"Given the equation $(x-2)^2=3$, find $a$ and $b$ such that the roots are $\frac{4+a\sqrt{r}}{2}$ and $\frac{4+b\sqrt{r}}{2}$ where $|a|>|b|$ and $r>0$. Calculate the value of $2a+b$.",
        "correct_answer": {
            "result": 6,
            "radical_coefficient": -1,
            "radicand": 3,
            "canonical_latex": "-\\sqrt{3}"
        },
        "oracle_payload": {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    }