def generate(level=1, **kwargs):
    return {
        "question_text": r"An organism starts with $initial$ cells and divides every $hours\_per\_generation$ hours by a factor of $split\_factor$. How many cells exist after $days$ days? Use the formula: $N = initial \times (split\_factor)^{total\_generations}$, where $total\_generations = 24 \times days / hours\_per\_generation$",
        "correct_answer": {"k": 1073741824},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }