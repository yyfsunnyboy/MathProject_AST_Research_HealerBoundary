def generate(level=1, **kwargs):
    return {
        "question_text": r"A population of bacteria starts with $initial$ cells and doubles every generation. If the split factor is $split\_factor$, how many generations occur in $days$ days given that each generation takes $hours\_per\_generation$ hours? Calculate the final count using exponential growth formula.",
        "correct_answer": {"k": 1},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }