import json
from collections import OrderedDict

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_of_val = frozen_params["divisor_of"]
    multiple_of_val = frozen_params["multiple_of"]
    
    question_text = r"""Find the number of integers that are both a multiple of {m} and a divisor of {d}.
In LaTeX format: Find the count of $x$ such that $x \mid d$ and $\exists k, x = km$. 
Input parameters: $\text{divisor\_of}=\{0\}$, $\text{multiple\_of}=\{1\}$.""" .format(m=multiple_of_val, d=divisor_of_val)
    
    gcd_result = divisor_of // multiple_of
    
    correct_answer_payload = json.dumps({"count": 3})

    return OrderedDict([("question_text", question_text), ("correct_answer", correct_answer_payload)])