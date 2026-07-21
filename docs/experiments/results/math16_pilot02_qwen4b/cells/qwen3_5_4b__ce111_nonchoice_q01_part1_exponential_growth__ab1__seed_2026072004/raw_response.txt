def generate(level=1, **kwargs):
    return {
        "question_text": r"An organism starts with 1 individual and splits into 4 individuals each generation (exponential growth). If there are $d$ days and the population doubles every hour within a day ($h$ hours per generation), what is the total number of generations? Note: The problem implies discrete generations based on split_factor=4, but uses doubling logic in description. Given frozen parameters: 15 days, 20 hours/generation, initial=1, split_factor=4.",
        "correct_answer": {"k": 3},
        "oracle_payload": {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    }