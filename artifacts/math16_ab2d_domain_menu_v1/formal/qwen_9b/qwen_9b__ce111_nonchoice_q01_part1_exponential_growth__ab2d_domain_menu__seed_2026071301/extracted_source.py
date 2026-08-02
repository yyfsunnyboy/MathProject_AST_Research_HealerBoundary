from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    # Calculate total hours passed
    total_hours = IntegerOps.add(IntegerOps.mul(frozen_params["days"], 24), 0)
    
    # Calculate number of generations (integer division since partial generations don't complete the split rule as described for discrete steps in this context, or we assume continuous exponential modeled by integer k. 
    # The problem says "after 15 days", implying full cycles if strict, but usually these problems imply n = floor(total_time / cycle).
    # Let's calculate exact generations passed: total_hours // hours_per_generation
    
    num_generations = IntegerOps.sub(IntegerOps.div(IntegerOps.mul(frozen_params["days"], 24), frozen_params["hours_per_generation"]), 0)
    
    # The formula is initial * (split_factor ^ k). 
    # Since initial is 1, total cells = 4^k. We need to find k.
    # In this specific problem setup for Math16 generation tasks with IntegerOps.safe_eval:
    # We construct the expression that yields k directly if possible, or calculate it.
    # However, safe_eval returns int/float. 
    # The question asks for k such that total cells = 4^k.
    # Total hours = 15 * 24 = 360.
    # Hours per gen = 20.
    # Generations = 360 / 20 = 18.
    # So k should be 18.
    
    # We must use IntegerOps.safe_eval to compute the value of k based on the parameters provided in frozen_params logic, 
    # but strictly speaking we just need to return the integer result derived from these constants.
    # Let's build an expression that computes (days * 24) // hours_per_generation
    
    expr = f"({frozen_params['days']} * 24) // {frozen_params['hours_per_generation']}"
    
    k_value = IntegerOps.safe_eval(expr)
    
    return {
        "question_text": "從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。",
        "correct_answer": {"k": k_value},
        "oracle_payload": frozen_params
    }