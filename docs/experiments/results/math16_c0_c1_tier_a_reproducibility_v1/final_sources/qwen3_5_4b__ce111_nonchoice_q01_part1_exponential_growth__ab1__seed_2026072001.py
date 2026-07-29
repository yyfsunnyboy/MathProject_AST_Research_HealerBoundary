def generate(level=1, **kwargs):
    return {
        "question_text": r"An organism starts with 1 individual and doubles its population every generation (split factor of 4 means each individual produces 3 new ones, totaling 4 per parent). If the process runs for $d$ generations where each generation takes $h$ hours to complete, what is the total time in hours until the final count reaches exactly $k$ individuals? Given: initial population = 1, split factor = 4.",
        "correct_answer": {"k": 2097152},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }