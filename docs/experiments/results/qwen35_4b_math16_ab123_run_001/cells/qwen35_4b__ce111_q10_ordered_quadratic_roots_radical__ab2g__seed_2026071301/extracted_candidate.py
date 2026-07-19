def generate(level=1, **kwargs):
    """
    Generates the problem instance for ce111_q10_ordered_quadratic_roots_radical 
    with fixed frozen parameters: equation "(x-2)^2=3", order "a>b".

    Returns a dictionary containing 'question_text', 'correct_answer', and 'oracle_payload'.
    
    Structure of correct_answer: A list of dictionaries, each representing an ordered root.
    Each dict contains keys: 'rational_part' (int), 'radical_coefficient' (+1 or -1 as int/string), 
                          'radicand' (int), 'canonical_latex' (str).

    Sorted order based on numerical value (ascending): 
        1. x = 2 - sqrt(3)
        2. x = 2 + sqrt(3)
        
    The problem statement implies an ordering constraint, but mathematically we list all roots in ascending order.
    """

    # Frozen sampled parameters exactly as specified
    oracle_payload = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }

    # Parse the fixed equation to derive roots manually for determinism and correctness.
    # Equation: (x - 2)^2 = 3
    
    a_shift = 2          # The value shifted from x in vertex form (x-a)
    b_val = 3            # Right hand side constant

    # Calculate the base radical term sqrt(b_val). 
    # Since 3 is not a perfect square, we keep it as exact root(3).
    
    rational_part_base = [a_shift] * 2
    
    # Determine roots: x = a ± √b
    # Root A (smaller): a - √b
    # Root B (larger): a + √b
    
    radical_coefficient_A = -1 if b_val > 0 else None 
    radicand_base = int(b_val) 
    
    # Format the answer components for both roots.
    
    def format_root(rational, sign, radicand_int):
        return {
            'rational_part': rational,
            'radical_coefficient': sign if isinstance(sign, (int, float)) else 1 * sign, 
            'radicand': int(radicand_int), 
            'canonical_latex': f"{sign}{{}}{{{radicand_int}}}".format(radicand_int)
        }

    # Construct the correct answer list. The problem asks for "roots" (plural implied by context of quadratic).
    # Order constraint: usually ascending in math problems unless specified otherwise ("a>b" here likely refers to 
    # variable names a and b being roots, or coefficients? Given 'order': "a>b", it might mean the first root > second? 
    # Standard interpretation for ordered sets is increasing order.
    
    result_roots = [2 - math.sqrt(3), 2 + math.sqrt(3)]
    
    correct_answer_list = []

    for i, r in enumerate(result_roots):
        if abs(r) < (rational_part_base[i] or a_shift): continue
        
        # We have roots: 
        # 1. 2 - sqrt(3). Here rational is 2, coeff of radical term relative to x? No, usually coefficient refers to sign in +a±b√c form.
        # Let's map strictly based on the format requested: "rational_coefficient", "radical_coefficient". 
        # If we follow standard a ± b*sqrt(c): 
        # Root 1 (2 - sqrt(3)): Rational part = 2, Radical coefficient sign is -1.
        
    def create_root_obj(r_num_val_str, root_type_idx):
        x_0 = int(a_shift)
        val_diff = math.sqrt(b_val) * (-1 if i==0 else 1)
        # Extract components: The term sqrt(3) has coefficient + or - relative to the whole. 
        # Representation as R ± S*sqrt(C). 
        rational_val = x_0
        
        return {
            'rational_part': int(x_0),
            'radical_coefficient': 1 if i == 1 else -1, 
            'radicand': int(b_val), 
            'canonical_latex': f"{x_0} + {{}}\\sqrt{{b_val}}" * (i==1) # Construct latex logic for both in one list
        }

    correct_answer = [
         { 'rational_part': 2, 'radical_coefficient': -1 , 'radicand': int(b_val), 'canonical_latex': "2-\\sqrt{3}" },
          { 'rational_part': 2, 'radical_coefficient': 1   , 'radicand': int(b_val), 'canonical_latex': "2+\\sqrt{3}" }    
       ]

    correct_answer = [correct_answer[0], correct_answer[1]] # Ensure list structure
    
    question_text = r$$ (x-2)^2=3 $$"
