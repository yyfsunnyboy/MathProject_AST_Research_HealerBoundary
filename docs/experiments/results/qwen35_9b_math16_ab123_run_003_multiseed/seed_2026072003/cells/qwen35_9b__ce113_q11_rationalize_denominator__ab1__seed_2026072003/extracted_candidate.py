def generate(level=1, **kwargs):
    return {
        "question_text": r"The rational form of $\frac{9}{4-\sqrt{7}}$ is $a + \sqrt{b}$ where $a,b\in\mathbb{Q}$. Find the value of $a+b+c+d$ if this expression can be written as $\frac{c+\sqrt{d}}{e}$ with integers $c,d,e>0$ and $d$ square-free.",
        "correct_answer": 19,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }