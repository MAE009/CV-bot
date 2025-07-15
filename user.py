import json    
import os    
    
def save_user(user):    
    data = {}    
    if os.path.exists("users.json"):    
        with open("users.json", "r") as f:    
            data = json.load(f)    
        
    data[str(user.id)] = {    
        "username": user.username,    
        "first_name": user.first_name    
    }    
    
    with open("users.json", "w") as f:    
        json.dump(data, f, indent=2)    
    
    
def get_users_list_text():    
    with open("users.json", "r") as f:    
        data = json.load(f)    
    
    lines = ["📋 Liste des utilisateurs du bot :\n"]    
    for i, (uid, info) in enumerate(data.items(), start=1):    
        username = f"@{info['username']}" if info['username'] else "Sans username"    
        name = info['first_name']    
        lines.append(f"{i}. {name} ({username}) - ID: {uid}")    
        
    return "\n".join(lines)  
