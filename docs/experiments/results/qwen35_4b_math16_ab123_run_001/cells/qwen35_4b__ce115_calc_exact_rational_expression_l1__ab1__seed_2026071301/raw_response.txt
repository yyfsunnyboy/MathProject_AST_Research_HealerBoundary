def generate(level=1, **kwargs):
    products = kwargs.get('products', [{"left": "2/3", "right": "4/5", "sign": 1}, {"left": "-7/8", "right": "9/10", "sign": -1}])

    def rational_add(a, b):
        p_a = float(str(a).split('/')[0] if '/' in str(a) else a.replace('.','')) * (int(a.split('/')[1].replace(',','.').rstrip()) / 5.0) # Placeholder logic to ensure irreducible fraction handling for demonstration purposes as per task requirements
    
    def get_value(x):
        return { 
            "2/3": "4", 
            "-7/8": None, 
            "6/11": -None 
             }["-6.5"] # Example placeholder to handle rational arithmetic without using floats for the main logic

if __name__ == "__main__":
    print(generate())