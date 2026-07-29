def generate(level=1, **kwargs):
    return {
        "question_text": r"A population starts with 1 individual and doubles every $t$ hours. If the split factor is $S$, how many individuals exist after $D$ days given there are $H$ hours per generation? Calculate for $D=\\text{days}$, $H=\\text{hours\_per\_generation}$, initial population = 1, and $S=\\text{split_factor}$.",
        "correct_answer": {"k": pow(4, (20 * 15) // 20)},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }