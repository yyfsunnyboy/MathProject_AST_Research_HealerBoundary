import json
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }

    from core.prompts.domain_function_library import IntegerOps
    
    days: int = kwargs.get("days", frozen_params["days"])
    hours_per_gen: int = kwargs.get("hours_per_generation", frozen_params["hours_per_generation"])
    initial: int = kwargs.get("initial", frozen_params["initial"])
    split_factor: float = kwargs.get("split_factor", frozen_params["split_factor"])

    total_generations: int = days * hours_per_gen
    
    final_value: Any = IntegerOps.safe_eval(str(initial) + "*" + str(split_factor)) ** (total_generations - 1) if initial > 0 else 0
    formatted_result: str = IntegerOps.fmt_num(final_value)

    question_text: str = r"""Calculate the value after $T$ generations starting from an initial amount of $I$, where each generation multiplies the current amount by a factor of $S$. Given $\text{days}=\text{15}$, $\text{hours\_per\_generation}=20$, $\text{initial}=1$, and $\text{split\_factor}=4$."""

    correct_answer: Dict[str, Any] = {"k": int(formatted_result)}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }