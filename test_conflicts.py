''''

# Simple test: Does user configuration have problems?
user_wants = {
    'setting_A': 'some value',    # vcpu affinity
    'setting_B': 'some value'     # numa affinity  
}

# My simple rule check:
if user_has_setting_A AND user_has_setting_B:
    print("ERROR: You cannot use both settings together!")
    print("SOLUTION: Pick one or the other")
    
'''