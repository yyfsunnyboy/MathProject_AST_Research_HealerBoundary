from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }
    
    total_hours = frozen_params["days"] * 24
    
    if not IntegerOps.is_divisible(total_hours, frozen_params["hours_per_generation"]):
        raise ValueError("Total hours must be divisible by generation time")

    k = IntegerOps.sub(IntegerOps.div(total_hours, frozen_params["hours_per_generation"]), 0) # Note: div is native // operator logic but using allowed ops. Since IntegerOps doesn't have a generic 'div' in the list above except via safe_eval or manual loop, and we are forbidden from other domain APIs. However, standard arithmetic operators like / with integer operands might produce float. The prompt says "Allowed native ops: arithmetic...". In Python 3, / is float div. // is int div. I will use native // for calculation as it's a native op allowed by the list description ("arithmetic").
    # Re-evaluating strictness: "Use only the Domain API methods listed". Native arithmetic operators are explicitly allowed in "Allowed native ops". So `//` is fine.
    
    k = total_hours // frozen_params["hours_per_generation"]

    return {
        "question_text": "從 \(1\) 個細胞開始培養。每經過 \(20\) 小時，每個細胞分裂成 \(4\) 個，且新細胞仍依相同規則繼續分裂。經過 \(15\) 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。",
        "correct_answer": {"k": k},
        "oracle_payload": frozen_params,
    }