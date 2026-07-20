def generate(level=1, **kwargs):
    return {
        "question_text": r"A population of bacteria starts with 1 individual and splits into $4$ individuals every generation. If a new generation takes place every $20$ hours over a period of $15$ days, how many individuals are in the final population? Assume no deaths occur.",
        "correct_answer": {"k": 67108864},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }