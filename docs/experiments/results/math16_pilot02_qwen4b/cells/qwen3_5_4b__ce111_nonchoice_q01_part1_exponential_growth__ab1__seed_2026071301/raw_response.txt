def generate(level=1, **kwargs):
    return {
        "question_text": r"An organism starts with 1 individual and splits into 4 individuals each generation. How many total individuals exist after $n$ generations? Given: days = 15, hours\_per\_generation = 20, initial = 1, split\_factor = 4.",
        "correct_answer": {"k": 65},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }