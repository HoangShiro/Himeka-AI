import json, sys, datetime, pytz

def correct_role(role):
    # Chỉ chấp nhận "user" hoặc "assistant", chuyển đổi thành chữ thường để so sánh không phân biệt chữ hoa chữ thường
    return "user" if role.lower() == "user" else "assistant" if role.lower() == "assistant" else None

def get_schat(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines

def getIdentity(identityPath):  
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return identityContext

def getprompt_normal(identityPath):  
    with open(identityPath, "r", encoding="utf-8") as f:
        identityContext = f.read()
    return {"role": "assistant", "content": identityContext}

def vals_open(file_name):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        conversation = []
        history = {"history": conversation}
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {str(e)}") 

def getPrompt_task(case):
    prompt = []
    if case.startswith("3"):
        case = case[1:]
        si = case.find("[")
        ei = case.find("]")
        o_prompt = case[si + 1:ei]
        n_prompt = case[ei + 2:-1]
        rq = f"Correct the above sentence according to the following description: [{n_prompt}]"
        prompt.append({"role": "user", "content": o_prompt})
        prompt.append({"role": "system", "content": rq})

    return prompt