def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]

    total_hours = days * hours_per_gen
    
    generations_count = int(total_hours // (20)) if 20 > 0 else 1
    current_pop = initial_pop
    for _ in range(generations_count):
        new_pop = current_pop * split_factor
        current_pop = new_pop

    correct_answer_k = current_pop
    
    question_text = r"""Consider a bacterial culture that doubles every generation. If the population starts at $N_0$ individuals and splits by factor 4 each time, what is the final population after completing all available hours? Assume the process stops exactly when the total accumulated growth matches the given duration constraints."""

    return {
        "question_text": question_text,
        "correct_answer": {"k": correct_answer_k},
        "oracle_payload": frozen_params
    }