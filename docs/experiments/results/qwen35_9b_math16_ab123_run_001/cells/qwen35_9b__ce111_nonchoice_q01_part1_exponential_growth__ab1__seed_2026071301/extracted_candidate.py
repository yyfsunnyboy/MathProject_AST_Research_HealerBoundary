def generate(level=1, **kwargs):
    return {
        "question_text": r"A culture of bacteria starts with 1 individual and doubles every $20$ hours under ideal conditions. If the split factor is $4$, how many individuals will be present after $15$ days? Express your answer as an integer.",
        "correct_answer": {"k": 67108864},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }