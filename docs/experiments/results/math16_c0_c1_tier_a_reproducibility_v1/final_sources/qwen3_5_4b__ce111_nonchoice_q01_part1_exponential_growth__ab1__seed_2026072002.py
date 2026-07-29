def generate(level=1, **kwargs):
    return {
        "question_text": r"An organism starts with 1 individual and splits into 4 individuals each generation. If there are $d$ generations, how many total organisms exist at the end? Given: days = 15, hours\_per\_generation = 20, initial = 1, split\_factor = 4.",
        "correct_answer": {"k": 3},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }