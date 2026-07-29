import json
from core.prompts.domain_function_library import IntegerOps.safe_eval, IntegerOps.fmt_num


def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }

    total_hours = IntegerOps.safe_eval(f"{frozen_params['days']} * {frozen_params['hours_per_generation']}")
    generations_count = IntegerOps.safe_eval(total_hours // frozen_params['hours_per_generation'])
    
    # Calculate final population using exponential growth formula: P_final = P_initial * (split_factor ^ generations)
    exponent_expr = f"{generations_count}"
    multiplier_expr = f"{frozen_params['split_factor']}**{exponent_expr}"
    power_result = IntegerOps.safe_eval(multiplier_expr)
    
    final_population = IntegerOps.safe_eval(f"{power_result} * {frozen_params['initial']}")

    question_text = r"""A bacteria culture starts with 1 cell. Every generation, the population splits into $4$ times its previous size. If each generation takes $20$ hours and a total of $15$ days elapse, what is the final number of cells? Express your answer as an integer."""

    correct_answer = {
        "k": int(final_population)
    }

    oracle_payload = frozen_params.copy()

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }