import requests
import json
import os

SYSTEM_SETTING = "You are a helpful assistant."

url = "http://localhost:11434/api/chat"
payload = {
    "model": "llama3:8b",
    "messages": [
        {
            
        }
    ],
    "stream": True
}
headers = {
    "Content-Type": "application/json"
}

def get_response(messages):
    # update payload with new messages
    payload['messages'] = messages
    response = requests.post(url, json=payload, headers=headers, stream=True)
    return response

# 初始messages
messages = [{'role': 'system', 'content': SYSTEM_SETTING}]
# Read messages from file

if os.path.exists('messages.txt'):
    with open('messages.txt', 'r', encoding='utf-8') as file:
        messages = json.load(file)
else:
    messages = [{'role': 'system', 'content': SYSTEM_SETTING}]

while True:
    user_input = input("\n请输入：")
    messages.append({'role': 'user', 'content': f"{user_input}"})
    assistant_output = ""
    
    # 检查响应状态码
    response = get_response(messages)
    if response.status_code == 200:
        # 逐块读取响应内容
        try:
            print("模型输出：",end="")
            for chunk in response.iter_lines():
                if chunk:
                    # 假设每个块都是一个独立的JSON对象
                    data = json.loads(chunk.decode('utf-8'))
                    # print(json.dumps(data, indent=2))
                    if 'message' in data and 'content' in data['message']:
                        assistant_message = data['message']['content']
                        print(assistant_message, end="")
                        
                        assistant_output += assistant_message                
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
    else:
        print(f"Request failed with status code {response.status_code}")

    
    messages.append({'role': 'assistant', 'content': assistant_output})
    

    # Save messages to a file
    with open('messages.txt', 'w', encoding='utf-8') as file:
        json.dump(messages, file, ensure_ascii=False)
    
