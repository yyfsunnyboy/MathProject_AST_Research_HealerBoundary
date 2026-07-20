def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    total_hours = sum(frozen_params["hours_per_generation"] for _ in range(frozen_params["days"]))
    initial_population = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    final_count = IntegerOps.safe_eval(str(initial_population * (split_factor ** int(total_hours / 20))))
    answer_k = int(final_count)
    
    return {
        "question_text": r"\text{A single bacterium divides into }4\text{ every }20\text{-hour generation. How many bacteria are there after }15\text{ days?}",
        "correct_answer": {"k": answer_k},
        "oracle_payload": frozen_params
    }