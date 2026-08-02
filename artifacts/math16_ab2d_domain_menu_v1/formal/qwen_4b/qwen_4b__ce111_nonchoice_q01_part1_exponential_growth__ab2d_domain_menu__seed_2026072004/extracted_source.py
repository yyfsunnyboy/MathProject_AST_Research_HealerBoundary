from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "days": 15,
        "hours_per_generation": 20,
        "initial": 1,
        "split_factor": 4
    }

    # Calculate total hours: 15 days * 20 hours/day = 300 hours
    total_hours = IntegerOps.add(IntegerOps.mul(frozen_params["days"], frozen_params["hours_per_generation"]), 0)

    # Determine number of generations (k): each generation takes 20 hours, starting from hour 0 to end at 300.
    # Generations occur at t=20, 40, ..., up to <= total_hours. 
    # Since the process starts with cell count = split_factor^0 and multiplies by split_factor each generation:
    # After n generations (each taking hours_per_generation), time elapsed is n * hours_per_generation.
    # We need max k such that k * 20 <= 300 => k <= 15. So k=15? Wait, let's re-read carefully.

    # Re-reading: "每經過 20 小時，每個細胞分裂成 4 個" -> every 20 hours, split by factor 4.
    # Start at t=0 with count = initial (which is 1). 
    # After first generation (t=20): count becomes 1 * 4^1? Or does it mean after each interval of 20h the population multiplies by 4? Yes, that's standard exponential growth.
    
    # Number of generations = total_hours // hours_per_generation if we consider full cycles completed within time frame. 
    # But wait: "經過 15 天後" -> at exactly t=300 (since 15*24=360? No, problem says each generation takes 20h).
    # Wait, the example uses days and hours_per_generation separately. So time = days * 24? Or is "days" just a unit for counting generations if hours_per_generation was per day? 
    # Let's re-read: "每經過 20 小時...". This implies the cycle length is fixed at 20h regardless of whether we count in days or not.
    
    # However, usually these problems imply that 'days' and 'hours_per_generation' are parameters to compute total time. 
    # If it says "after 15 days", does it mean t = 15 * 24 hours? Or is the problem saying there are 15 generations because each takes 20h but we stop at day boundary?
    
    # Actually, looking at typical Math16 problems: 
    # If they say "after X days" and give a generation time in hours, then total_time = X * 24. Then number of generations = floor(total_time / gen_hours).
    # BUT here the problem says "每經過 20 小時...". It defines the mechanism. Then it asks after 15 days. 
    # So we must convert 15 days to hours: 15 * 24 = 360 hours? Or is there a trick where 'days' in frozen_params means something else?
    
    # Let's look at the parameters again: "hours_per_generation": 20. This suggests one generation takes 20h. 
    # If we have 15 days, and each day has 24 hours... then total time = 360 hours. 
    # Number of generations k such that k * 20 <= 360? Then k=18.
    
    # Wait, maybe the problem implies something simpler: "after 15 days" might be a distractor if the generation count is derived differently? 
    # Or perhaps 'days' in frozen_params isn't calendar days but just an integer representing generations directly? No, that would make hours_per_generation redundant.
    
    # Let's assume standard interpretation: Total time = 15 * 24 hours. Generation cycle = 20h. k = floor(360 / 20) = 18. 
    # But wait! The problem says "從 1 個細胞開始...". If initial is 1, and after k generations it's 4^k.
    
    # Is there any chance the 'days' parameter in frozen_params actually represents the number of generations directly? 
    # Let's check if the math works out nicely with days=15 as generations. Then answer would be 15. 
    # If we calculate via time: k = floor(360/20) = 18. Which one is intended?
    
    # Re-reading carefully: "每經過 20 小時...". This defines the rate. "經過 15 天後" -> this sets the duration. 
    # Unless 'days' in frozen_params means something else, we must convert days to hours using standard calendar (24h/day).
    
    # However, sometimes these generated problems have a quirk where they define their own time unit or skip conversion if context implies otherwise? 
    # Let's assume strict interpretation: 15 days = 360 hours. k = floor(360 / 20) = 18.
    
    # Wait, could it be that the problem intends for us to use 'days' as generations directly because of how these datasets are often constructed? 
    # Let's try to infer from similar problems or common patterns in Math16 generation tasks. Often they simplify: "after N days" where each day is a unit step if not specified otherwise, but here hours_per_generation IS specified.
    
    # Actually, looking at the wording again: "每經過 20 小時...". If I have 15 days, and generations happen every 20h... 
    # Maybe the intended logic is simply k = frozen_params["days"]? That would be too simple given 'hours_per_generation' exists.
    
    # Let's calculate both ways mentally:
    # Option A (Time conversion): Total hours = 15 * 24 = 360. Generations = floor(360 / 20) = 18. Answer k=18.
    # Option B (Direct mapping): Generations = days = 15. Answer k=15. 
    # Why would they provide 'hours_per_generation' if not to use it? If the answer was just days, hours_per_generation is unused info. In Math16 generation tasks, usually all frozen_params are used unless specified otherwise (like distractors).
    
    # Therefore, Option A seems more robust: Use time conversion. 
    # k = floor((days * 24) / hours_per_generation)
    # Let's verify if there is any ambiguity about "day". In biology/math problems involving cell division, a day is always 24h unless specified (e.g., circadian rhythm). Here no special context given. 
    # So k = floor(360 / 20) = 18.
    
    total_hours_calc = IntegerOps.mul(frozen_params["days"], 24)
    generations_k = IntegerOps.floor_div(total_hours_calc, frozen_params["hours_per_generation"])

    question_text = f"從 \(1\) 個細胞開始培養。每經過 {frozen_params['hours_per_generation']} 小時，每個細胞分裂成 {frozen_params['split_factor']} 個，且新細胞仍依相同規則繼續分裂。經過 {frozen_params['days']} 天後，細胞總數可寫成 \(4^k\)，求 \(k\)。"
    
    correct_answer = {"k": int(generations_k)}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params.copy()
    }
