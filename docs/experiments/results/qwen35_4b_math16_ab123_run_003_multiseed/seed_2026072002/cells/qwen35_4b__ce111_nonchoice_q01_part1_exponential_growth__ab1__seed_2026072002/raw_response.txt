def generate(level=1, **kwargs):
    question_text = r"An initial population of 1 individual splits into 4 individuals each generation. If there are 20 hours per generation and the total time available is $t$ days, how many generations occur? Calculate the final integer count using the exponential growth formula where the number of generations depends on the elapsed time."
    correct_answer = {"k": 15}
    oracle_payload = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }