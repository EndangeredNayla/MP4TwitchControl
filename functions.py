import requests

def get_broadcaster_id(username, token):
    url = f"https://api.twitch.tv/helix/users?login={username}"
    
    headers = {
        'Client-ID': 'gp762nuuoqcoxypju8c569th9wz7q5',
        'Authorization': f'Bearer {token}',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id']
        else:
            print("User not found.")
            return None
    else:
        print(f"Failed to get user ID: {response.status_code} - {response.text}")
        return None
    
def create_channel_point_reward(username, title, cost, token, maxPerStream, maxPerUserPerStream, coolDown, maxPerStreamBool, pathToImage):
    url = f"https://api.twitch.tv/helix/channel_points/custom_rewards"
    
    headers = {
        'Client-ID': 'gp762nuuoqcoxypju8c569th9wz7q5',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "broadcaster_id": get_broadcaster_id(username, token),
        "title": title,
        "cost": int(cost),
        "is_enabled": True,
        "is_user_input_required": False,
        "max_per_stream": int(maxPerStream),
        "is_max_per_stream_enabled": True if maxPerStreamBool == "True" else False,
        "max_per_user_per_stream": int(maxPerUserPerStream),
        "global_cooldown_seconds": int(coolDown),
        "image": {
            "url_1x": pathToImage,
            "url_2x": pathToImage,
            "url_4x": pathToImage
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Channel point reward created successfully!")
    else:
        print(f"Failed to create reward: {response.status_code} - {response.text}")