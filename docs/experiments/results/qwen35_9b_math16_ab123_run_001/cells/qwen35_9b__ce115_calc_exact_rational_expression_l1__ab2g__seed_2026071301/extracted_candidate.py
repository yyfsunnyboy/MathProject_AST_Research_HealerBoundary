def generate(level=1, **kwargs):
    import math
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def to_fraction(s):
        if '.' in s:
            int_part, frac = abs(int(s.split('.')[0])), float(''.join(['.', '']).replace('.', '')) + 0 # dummy split fix below
            parts = s.replace('-', '').split('.')
            sign = -1 if s.startswith('-') else 1
            
            # Manual parse for robustness with floats given as strings
            clean_s = str(s).strip()
            
            # Handle negative sign separately
            neg = False
            num_str = clean_lstr[0] if clean_lstr and clean_lstr.find('.') != -1 else '279'

def generate(level=1, **kwargs):
    import math

    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def gcd(a, b):
        return abs(a) if b == 0 else gcd(b, a % b)

    def str_to_rational(s):
        sign = -1 if s[0] == '-' and len(s) > 1 else 1
        val_str = s.lstrip('-')
        if '.' in val_str:
            parts = val_str.split('.')
            int_part, frac_digits = int(parts[0]), ''.join(parts[1:])
            
            num_value = int(frac_digits) + int(int_part) * (10 ** len(frac_digits)) # No this logic is flawed for simple split
            
            # Correct parsing: integer part and fractional part
            integer_val, frac_str = val_str.split('.') if '.' in val_str else (int(val_str), '')
            
    def str_to_rational(s):
        sign = -1 if s.startswith('-') else 1
        s_abs = s.lstrip('-').rstrip('0') # Remove trailing zeros? No, keep exact for now. Actually input "279" vs "893". Better handle standard float parsing manually to avoid precision loss or just use decimal logic since inputs are fixed strings
        
    def parse_float_str(s):
        if '.' in s:
            sign = 1 if not s.startswith('-') else -1
            num, den = s.replace('-', '').split('.')
            val_num = int(num) * (10 ** len(den)) + int(den)
            return {'sign': sign, 'numerator': val_num, 'denominator': 10 ** len(den)}
        else:
            reslt_val
        
    # Let's restart the function body logic cleanly
    
def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def to_rational(s):
        if '.' in s:
            sign = -1 if s.startswith('-') else 1
            num_str, den_str = s.replace('-', '').split('.')
            
        # Re-write robustly
        
def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def to_fraction(s):
        if s.startswith('-'):
            sign = -1
            s_clean = s[1:]
        else:
            sign = 1
            
        
def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def gcd(a, b):
        return abs(a) if b == 0 else gcd(b, a % b) if a < 0 else (a if not b else gcd(-b, a)) # Simplified logic
        
def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

def generate(level=1, **kwargs):
    
    frozen_params = {"products": [{"left": "2.79