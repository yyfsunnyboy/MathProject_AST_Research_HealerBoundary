import json
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num


def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}

    total_hours = kwargs.get("total_hours", hours_per_generation * days) if "days" in kwargs else None
    
    # Calculate final population using exponential growth formula: P(t) = P(0) * r^t
    # Here t is number of generations, r is split_factor
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    total_generations = kwargs.get("total_generations", 15) if "days" in kwargs else None
    
    final_population = safe_eval(f"{initial_pop} * {split_factor} ** {total_generations}")
    
    question_text = f"The initial population is $P_0$. Each generation, the population splits into four times its previous size. After ${total_generations}$ generations, what is the final population? Express your answer as an integer."
    
    correct_answer_dict = {"k": int(final_population)}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }