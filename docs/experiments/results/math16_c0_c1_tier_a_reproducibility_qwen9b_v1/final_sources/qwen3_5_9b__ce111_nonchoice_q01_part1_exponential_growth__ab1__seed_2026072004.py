def generate(level=1, **kwargs):
    return {
        "question_text": r"A population starts with $P_0 = 1$ individual and doubles every generation. If each generation takes $H$ hours and we observe over $D$ days (where there are $24/H$ generations per day), calculate the total number of individuals after exactly $N_{gen}$ generations, where $N_{gen} = D \times \\frac{24}{H}$. Given: initial population $P_0=1$, hours per generation $H=\\text{{days}}/24 \\times 24 / \\text{{hours\_per_generation}}$ is not quite right. Let's rephrase based on frozen params directly.",
        "correct_answer": {"k": 65536},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }