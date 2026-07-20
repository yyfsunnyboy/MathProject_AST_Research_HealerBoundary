def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify \(\sqrt{27}\) into its simplest radical form \(a\sqrt[b]{c}\). Find the coefficient $a$, radicand $b$ (as part of the root index), and simplified integer radicand $c$. Express your final answer as a list [coefficient, radicand_index, simple_radicand].",
        "correct_answer": "[3, 2, 3]",
        "oracle_payload": {"radicand": 27}
    }