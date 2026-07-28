def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    from core.prompts.domain_function_library import IntegerOps
    
    total_hours = kwargs.get("total_hours", hours_per_generation * level) if 'hours_per_generation' in kwargs else frozen_params["hours_per_generation"] * (frozen_params["days"] // 15 + 1)
    # Re-evaluating based on standard exponential growth problem structure: 
    # Population P(t) = P0 * r^t. Here, split_factor is the rate per generation step if we consider generations over days?
    # Given "hours_per_generation" and "days", let's assume a discrete time model where t represents number of steps or hours scaled to base 2 (binary fission implied by splitting).
    # Standard interpretation for ce111_nonchoice_q01_part1: P = initial * split_factor ** days.
    
    total_days = frozen_params["days"]
    p0 = IntegerOps.safe_eval(str(frozen_params["initial"]))
    r = IntegerOps.safe_eval(str(frozen_params["split_factor"]))
    
    # Calculate final population after 'total_days' generations/steps assuming binary splitting logic per day as implied by context of exponential growth with split factor 4 (often meaning doubling then more, or direct power). 
    # Given the parameters and typical problem type: P = initial * r^days.
    result_p = IntegerOps.safe_eval(str(p0) + "*" + str(r) + "**" + str(total_days))
    
    correct_answer_dict = {"k": int(result_p)}
    
    question_text = f"What is the final population after {total_days} days given an initial population of 1 and a split factor of 4? The growth follows exponential function $P(t) = P_0 \\cdot r^t$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }