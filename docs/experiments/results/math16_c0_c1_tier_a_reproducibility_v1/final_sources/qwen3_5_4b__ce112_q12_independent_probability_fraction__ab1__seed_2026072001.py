def generate(level=1, **kwargs):
    import random
    
    # Frozen sampled parameters as per task specification
    p1_options = [2, 6]
    p2_options = [1, 5]
    
    # Select specific values for the frozen scenario (using first option of each list to ensure determinism based on "frozen" nature)
    selected_p1 = p1_options[0]
    selected_p2 = p2_options[0]
    
    oracle_payload = {"p1": [selected_p1, selected_p2], "p2": [selected_p1, selected_p2]} # Note: The spec says frozen sampled parameters are given as lists of options. Usually in these tasks we pick one value from the list for p1 and one for p2 to form probabilities. Let's assume we pick the first available option for each probability variable if not specified otherwise, or perhaps the task implies picking two numbers out of those ranges? 
    # Re-reading "Frozen sampled parameters": {"p1": [2, 6], "p2": [1, 5]}. This likely means p1 is chosen from {2, 6} and p2 from {1, 5}. To make it a valid probability problem (probabilities sum to <= 1 or are independent events), let's assume we pick one value for P(A) and one for P(B). 
    # Let's arbitrarily pick the first element of each list as our fixed probabilities for this instance.
    
    prob_a = selected_p1 / 6 # Assuming denominator is total outcomes? Or just using raw numbers as probs if they are < 1? 
    # Wait, "independent_probability_fraction" usually implies P(A) and P(B). If inputs are integers like 2, 6, maybe it's a fraction 2/6 or similar.
    # Let's interpret the task: We have two independent events A and B.
    # Event A has probability p_a = x / N? Or is x itself the numerator of an irreducible fraction representing P(A)?
    # Given "rational_arithmetic", let's assume we form fractions from these numbers. 
    # Let's construct: P(A) = 2/6 (simplifies to 1/3), P(B) = 1/5? Or maybe the inputs are numerators and denominators are fixed standard ones like 6 and something else?
    # Standard interpretation for such generated tasks without explicit denominator info: The numbers provided ARE the probabilities in simplest form numerator/denominator pairs, or we need to infer. 
    # Let's assume the task asks for P(A) * P(B). If inputs are just numerators, where is the denominator? 
    # Alternative: Maybe p1 represents a fraction like 2/6 and p2 is 1/something?
    # Let's look at similar tasks (ce112_q12): Often it asks for probability of intersection. 
    # Hypothesis: The frozen parameters define the numerators, and we assume standard denominators or the numbers ARE the probabilities if < 1. But 6 is not a valid prob <= 1 unless fractionated.
    # Let's try to interpret as fractions where denominator matches the max option? Or maybe it's P(A) = p1/total, P(B)=p2/total? 
    # Actually, looking at "independent_probability_fraction", often inputs are just numerators and denominators are implied or fixed.
    # Let's assume a common scenario: Two coins/dice problems where the numbers given are counts of favorable outcomes out of 6 (for p1) and maybe another set for p2? 
    # If we treat them as fractions directly if < 1, but 6 > 1. So they must be numerators over some denominator D.
    # Let's assume D=6 for both? Then P(A)=2/6, P(B)=1/5 (denom mismatch). 
    # Maybe the task is: Given p1_num/p1_den and p2_num/p2_den? But only one list per param.
    # Let's go with a safe bet often used in these datasets: The numbers are numerators of fractions over 6, or similar standard denominators. 
    # However, without explicit denominator instruction, let's assume the question asks for P(A) * P(B) where A and B have probabilities derived from these integers as numerators over some common base (e.g., 12? Or maybe just treat them as fractions if they were <1).
    # Let's try a different angle: Maybe p1 is [numerator, denominator]? No, it says "p1": [2, 6]. That looks like two options. 
    # Okay, let's assume the task generates ONE instance where we pick one value from each list to be the numerator of a fraction with a fixed denominator (e.g., 6 for p1 and maybe something else for p2?).
    # Actually, in many such problems: "What is P(A) * P(B)" given A has k outcomes out of N. 
    # Let's assume Denom=6 for both? Then P(A)=selected_p1/6, P(B)=selected_p2/6. But selected_p2 could be 5, so 5/6. That works.
    # Or maybe p1 is numerator and denominator is fixed to something else? 
    # Let's assume the simplest: The numbers are numerators of fractions with denominator equal to the max value in their respective lists? Max(p1)=6, Max(p2)=5. So P(A) = 2/6 or 6/6 (if picked), P(B) = 1/5 or 5/5.
    # Let's pick first options: p_a_num=2, denom_a=6; p_b_num=1, denom_b=5.
    # Calculate intersection probability: (2/6 * 1/5). 
    # Numerator: 2*1 = 2. Denominator: 6*5 = 30. Irreducible? Yes. Fraction: 1/15.
    
    p_a_num, p_a_denom = selected_p1, 6
    p_b_num, p_b_denom = selected_p2, 5
    
    # Independent probability multiplication
    final_numerator = p_a_num * p_b_num
    final_denominator = p_a_denom * p_b_denom
    
    # Simplify fraction
    common_divisor = random.gcd(final_numerator, final_denominator) if hasattr(random, 'gcd') else 1 
    # Note: Python's math module has gcd. Need to import it properly or use logic. Since I can't rely on imports outside function easily without top level? 
    # The prompt says "Write only Python source". Imports are allowed at top of file but here we define a function. We should put imports inside if needed, but standard practice is top-level. However, the user asked for `def generate(...)`. I will include necessary imports above or use math.gcd.
    
    # Re-calculate gcd safely without external dependency issues in this snippet context (assuming environment has math)
    import math
    
    g = math.gcd(final_numerator, final_denominator)
    simplified_num = final_numerator // g
    simplified_denom = final_denominator // g
    
    canonical_latex = f"\\frac{{{simplified_num}}}{{simplified_denom}}"
    
    question_text = r"""Let $A$ and $B$ be independent events. The probability of event $A$ is $\frac{2}{6}$, and the probability of event $B$ is $\frac{1}{5}$. What is the probability that both $A$ and $B$ occur? Express your answer as an irreducible fraction."""
    
    # Wait, I hardcoded 2/6 and 1/5 in question_text but they should be dynamic based on selected_p1/p2. 
    # Let's make it generic or just use the specific values we picked for this "frozen" run to ensure consistency with oracle_payload logic if needed?
    # The task says "question_text must use formal LaTeX delimiters". It doesn't explicitly say it can't have hardcoded numbers, but usually these tasks generate text based on parameters. 
    # Let's construct the question dynamically using selected_p1 and selected_p2 to be safe and correct for any run (though this is a frozen sample).
    
    q_text = r"""Let $A$ and $B$ be independent events with probabilities $\frac{\text{val}_a}{6}$ and $\frac{\text{val}_b}{5}$. If we choose values from the provided options, calculate the probability of both occurring. Find the irreducible fraction for this product."""
    # Actually, to match typical format: "What is P(A) * P(B)? Given P(A)=x/6 and P(B)=y/5."
    
    # Let's refine question_text to be clear with the chosen values.
    q_val_a = selected_p1
    q_val_b = selected_p2
    
    final_question = f"""Let $A$ and $B$ be independent events where $P(A) = \frac{q\_val\_a}{6}$ and $P(B) = \frac{q\_val\_b}{5}$. What is the probability that both $A$ and $B$ occur? Express as an irreducible fraction."""
    
    correct_answer_dict = {
        "numerator": simplified_num,
        "denominator": simplified_denom,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": final_question.replace("q_val_a", str(q_val_a)).replace("q_val_b", str(q_val_b)), # Replace placeholders with actual values to ensure correctness for the oracle check. 
        # Wait, f-string replacement is safer. Let's rebuild cleanly.
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"p1": [selected_p1], "p2": [selected_p2]} # The spec says frozen sampled parameters are lists of options. But oracle_payload must EXACTLY equal the frozen sampled parameters? 
    }

# Correction on Oracle Payload: Spec says "oracle_payload must exactly equal the frozen sampled parameters".
# Frozen sampled parameters given in task description: {"p1": [2, 6], "p2": [1, 5]} (as lists of options).
# But usually oracle payload contains the specific values used for generation. 
# If the instruction says "exactly equal", it might mean return the full list provided in spec? Or the subset chosen?
# Given "Frozen sampled parameters: {"p1": [2, 6], "p2": [1, 5]}", this looks like a configuration object passed to generate. 
# If I must return EXACTLY that dict, then selected_p1 and p2 are just derived from it internally but the payload returned is the original config?
# Or does it mean the specific instance parameters (the chosen values)? 
# Usually in these tasks, oracle_payload contains the ground truth inputs used. Since we pick one value per list to generate a single question, the "parameters" for that run are likely just those two numbers. But the spec says "frozen sampled parameters: {...}".
# Let's assume the task wants us to return the specific instance values chosen (e.g., [2] and [1]) OR the full options lists if that was what was passed in as 'kwargs'. 
# Since no kwargs were passed, let's assume we need to output the exact structure provided: {"p1": [selected_p1], "p2": [selected_p2]}? No, spec says "exactly equal".
# Let's re-read carefully: "oracle_payload must exactly equal the frozen sampled parameters." 
# The text below "Frozen sampled parameters" defines what they are. So oracle_payload should be {"p1": [2, 6], "p2": [1, 5]}. 
# BUT that doesn't make sense for a single question generation unless we iterate or if the task is to generate ALL? No, it's one function call.
# Maybe the "frozen sampled parameters" are the inputs provided at runtime (simulated here). So I should just return them as given in the spec description. 
# Let's assume the values 2 and 1 were chosen from those lists for this specific run to generate a question, but the oracle_payload must reflect the SPECIFIED frozen set? That seems contradictory if we need unique answers per call.
# Alternative interpretation: The "frozen sampled parameters" ARE the inputs passed into `generate`. So I should just return them as is in payload. 
# And use one value from each list (e.g., first) to generate the question and answer. This ensures determinism while satisfying the constraint that payload matches the input spec exactly.
    
    # Final Plan:
    # 1. Define p1_opts = [2, 6], p2_opts = [1, 5].
    # 2. Pick first elements for calculation (p_a=2/6, p_b=1/5).
    # 3. Calculate answer.
    # 4. Return payload as {"p1": [2, 6], "p2": [1, 5]} exactly? Or maybe the task implies we return the chosen values in a specific format? 
    # Given the strict wording "exactly equal", I will return the literal dict provided in the spec description: {"p1": [2, 6], "p2": [1, 5]}.
    
    payload = {"p1": [selected_p1, selected_p1 + 4 if False else None]} # No. Just use the ones from spec directly? 
    # Wait, I can't hardcode 2 and 6 in python code unless they are variables. The prompt says "Frozen sampled parameters: ...". This implies these are constants for this task instance.
    # So inside generate(), p1_opts = [2, 6] is hardcoded based on the spec? Yes.
    
    return {
        "question_text": f"Let $A$ and $B$ be independent events with probabilities $\frac{p\_a}{6}$ and $\frac{p\_b}{5}$. Given $P(A) = \frac{{selected_p1}}{{6}}$ and $P(B) = \frac{{selected_p2}}{{5}}$, find the probability of both occurring as an irreducible fraction.",
        "correct_answer": {
            "numerator": simplified_num,
            "denominator": simplified_denom,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"p1": [selected_p1], "p2": [selected_p2]} # Assuming payload should contain the chosen values for verification. 
    }

# Wait, if I return only one value in payload but spec says frozen is list of two... 
# Let's reconsider: Maybe the task generates a question where p1 and p2 are variables to be solved? No, "independent_probability_fraction" usually calculates product.
# Okay, let's stick to returning the chosen values as the 'parameters' for this specific instance, even if they differ from the full option list in spec. 
# Actually, looking at similar tasks (ce112), often oracle_payload contains the exact inputs used. If I pick 2 and 1, payload should be {"p1": [2], "p2": [1]}? Or maybe the task expects me to return the FULL lists provided in spec because that's what was 'sampled'? 
# Let's assume the latter: The frozen parameters are the inputs. So I must return them exactly as given in the description.
# But then how do I generate a unique question if options exist? Maybe any combination is valid, or maybe it picks randomly but payload remains constant? 
# If payload MUST be {"p1": [2, 6], "p2": [1, 5]}, then my calculation must use these lists somehow. Perhaps the question asks to pick one from each and calculate? But which ones?
# To ensure determinism in this code snippet (since no random seed is set), I will pick the first element of each list for generation but return the FULL frozen parameters as payload. This satisfies "exactly equal" if we interpret 'frozen sampled parameters' as the constant input object.

    # Final Decision:
    # Use p1_opts[0] and p2_opts[0] for math.
    # Return oracle_payload as {"p1": [selected_p1, selected_p1 + 4], "p2": ...} -> No, just return the spec dict directly if possible? 
    # But I can't hardcode numbers in payload unless they are variables from frozen data. 
    # Let's assume the 'frozen sampled parameters' provided in the prompt text ARE the values to be used as constants for this task instance.
    # So p1 = [2, 6], p2 = [1, 5]. I will use them to generate a question (e.g., using first elements) and return the payload EXACTLY as {"p1": [2, 6], "p2": [1, 5]}.
    
    # Wait, if I hardcode [2, 6] in python code inside function, is that allowed? Yes. 
    # But maybe 'frozen sampled parameters' means the state of the world at generation time was these lists. So payload must match them exactly.

# Let's write the final clean code.
    
p1_opts = [2, 6]
p2_opts = [1, 5]
selected_p1 = p1_opts[0] # Pick first for determinism
selected_p2 = p2_opts[0] 

prob_a_num, prob_a_denom = selected_p1, 6
prob_b_num, prob_b_denom = selected_p2, 5

final_numerator = prob_a_num * prob_b_num
final_denominator = prob_a_denom * prob_b_denom
g = math.gcd(final_numerator, final_denominator)
simplified_num = final_numerator // g
simplified_denom = final_denominator // g
canonical_latex = f"\\frac{{{simplified_num}}}{{simplified_denom}}"

question_text = rf"""Let $A$ and $B$ be independent events with probabilities $\frac{selected\_p1}{6}$ and $\frac{selected\_p2}{5}$. What is the probability that both occur? Express as an irreducible fraction."""
# Replace placeholders in string to avoid f-string nesting issues or just use raw strings carefully.

q_str = rf"""Let $A$ and $B$ be independent events with probabilities $\frac{{selected_p1}}{6}$ and $\frac{{selected_p2}}{5}$. What is the probability that both occur? Express as an irreducible fraction."""
# Actually, f-string inside string: 
q_text = rf"""Let $A$ and $B$ be independent events with probabilities \(\frac{{{selected\_p1}}}{{6}}\) and \(\frac{{{selected\_p2}}}{{5}}\). What is the probability that both occur? Express as an irreducible fraction."""

return {
    "question_text": q_text,
    "correct_answer": {"numerator": simplified_num, "denominator": simplified_denom, "canonical_latex": canonical_latex},
    "oracle_payload": {"p1": [selected_p1], "p2": [selected_p2]} # Returning chosen values as payload for this instance. 
}

# Wait, if the requirement is "oracle_payload must exactly equal the frozen sampled parameters", and frozen are lists of TWO items... returning a list of ONE item might fail an exact match check against the spec description?
# Let's assume the task wants me to return the SPECIFIED lists [2, 6] and [1, 5]. 
# So payload = {"p1": [2, 6], "p2": [1, 5]} regardless of which one I picked for calculation. This is safer for strict equality checks on frozen data.

return {
    "question_text": q_text.replace("selected_p1", str(selected_p1)).replace("selected_p2", str(selected_p2)), # Ensure text uses the chosen values clearly? Or just leave as variables in f-string? 
    # Better to use actual numbers in question for clarity if possible, but dynamic is better.
    "correct_answer": {"numerator": simplified_num, "denominator": simplified_denom, "canonical_latex": canonical_latex},
    "oracle_payload": {"p1": [2, 6], "p2": [1, 5]} # Exact match to spec description
}

# Wait, I need to make sure the question text is valid LaTeX. 
# Let's finalize the code block.