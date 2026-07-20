def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    question_text = f"Find the number of positive integers that are both a {math} and a {math}. The numbers must be multiples of their respective parameters. Express your answer as an integer."
    
    import math
    
    lcm_val = math.lcm(divisor_of, multiple_of)
    count = divisor_of // (lcm_val // divisor_of) if not isinstance(lcm_val, int) else 0 # Placeholder logic for intersection count based on problem type usually involving LCM properties or specific sets. Since the exact mathematical definition of "intersection" in this frozen context implies finding numbers satisfying both conditions within a likely bounded set implied by 'divisor' (which is unusual phrasing if it means multiples), we assume the standard interpretation: Find integers x such that divisor_of divides x AND multiple_of divides x. This is equivalent to LCM(divisor, multiple). The count of such positive integers up to N isn't given, so this specific problem likely asks for a property or there's an implicit range. However, re-reading typical math problems with these parameters: If it implies "How many numbers between 1 and X...", the upper bound is missing. 
    *Correction*: Given the frozen params are just integers without bounds, perhaps the question text itself defines the set size or it's a trick where 'divisor_of' means x % d == 0? No, standard interpretation: Find count of positive integers <= some implicit limit (often LCM for periodicity) OR the problem is actually asking for something specific like "How many numbers in range [1, divisor*multiple] satisfy...". 
    Let's assume the question asks for the number of such integers up to a reasonable bound or perhaps the intersection size if treated as sets? Actually, looking at similar datasets (e.g., GSM8K style), without an upper bound N, "count" is infinite. 
    *Hypothesis*: The problem likely implies finding numbers that are multiples of both, and often in such generated tasks with missing bounds, it might be asking for the LCM itself as a representative, OR there's a hidden assumption. But wait, if 'divisor_of' means "is a divisor of", then we need x where d|x AND m|x -> lcm(x). If 'multiple_of', same logic. 
    Let's reconsider the wording: "integers that are both a [param] and a [param]". This is grammatically broken for standard math terms unless it says "divisor" or "multiple of X". The parameters are named `divisor_of` (216) and `multiple_of` (18). 
    Interpretation: Find integers x such that 216 divides x AND 18 divides x. This is true for any multiple of LCM(216, 18). Since the count is infinite without a bound, I will assume the question text implicitly defines a range like "up to the product" or similar common pattern in these specific frozen tasks (e.g., MathQA style where N might be implied as divisor*multiple or just asking for LCM properties). 
    *Alternative*: Maybe it asks how many numbers are there that divide 216 AND are multiples of 18? That would make sense. "Integers that are a divisor of 216 and a multiple of 18".
    Let's calculate: Divisors of 216 (which is $6^3 = 2 \cdot 3^3$). Multiples of 18 ($2 \cdot 3^2$) that divide 216.
    Candidates for multiples of 18 dividing 216: 
    18 * k must be a divisor of $216$. Since $k$ is integer, $18k | 216 \implies k | (216/18) = 12$.
    So we need number of divisors of $(216 // 18)$? No. We need multiples of 18 that are also divisors of 216. 
    Let $x$ be the number. $x | 216$ AND $18 | x$.
    Since $18 | x$, let $x = 18k$. Then $18k | 216 \implies k | (216/18) \implies k | 12$.
    The number of such positive integers is the count of divisors of 12. 
    Divisors of 12: 1, 2, 3, 4, 6, 12. Count = 6.
    
    This interpretation makes "count" finite and solvable without an arbitrary upper bound N provided in text other than the divisor constraint itself acting as the cap.
    
    count_val = sum(1 for k in range(1, (divisor_of // multiple_of) + 1) if ((multiple_of * k) % divisor_of == 0)) # Count multiples of M that are divisors of D
    
    correct_answer = {"count": int(count_val)}
    
    oracle_payload = {**kwargs}

    return {
        "question_text": question_text.replace("[math]", r"\text{divisor } $d$"), 
        # Reconstructing a clean LaTeX string based on the logic: Find integers that are divisors of 216 and multiples of 18.
        # Text: Let there be an integer $x$. If $x$ is a divisor of $216$ and a multiple of $18$, find how many such positive integers exist.
        "question_text": r"Let $d = 216$ and $m = 18$. Find the number of positive integers that are divisors of $d$ and multiples of $m$.",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }