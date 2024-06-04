import requests
from requests.structures import CaseInsensitiveDict
import time
import datetime
from colorama import init, Fore, Style
init(autoreset=True)

def get_new_token(query_id):
    import json
    # Header for HTTP request
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://telegram.blum.codes",
        "priority": "u=1, i",
        "referer": "https://telegram.blum.codes/"
    }

    # Data to be sent in the POST request
    data = json.dumps({"query": query_id})

    # URL endpoint
    url = "https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"

    # Trying to get a token up to 3 times
    for attempt in range(3):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Getting token...", end="", flush=True)
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            print(f"\r{Fore.GREEN+Style.BRIGHT}Token successfully created", end="", flush=True)
            response_json = response.json()
            return response_json['token']['refresh']
        else:
            print(response.json())
            print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token, attempt {attempt + 1}", flush=True)
    # If all attempts fail

    print(f"\r{Fore.RED+Style.BRIGHT}Failed to get token after 3 attempts.", flush=True)
    return None

# Function to get user information
def get_user_info(token):

    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://gateway.blum.codes/v1/user/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        hasil = response.json()
        if hasil['message'] == 'Token is invalid':
            print(f"{Fore.RED+Style.BRIGHT}Invalid token, getting a new token...")
            # Getting a new token
            new_token = get_new_token()
            if new_token:
                print(f"{Fore.GREEN+Style.BRIGHT}New token obtained, trying again...")
                return get_user_info(new_token)  # Recursively call the function with the new token
            else:
                print(f"{Fore.RED+Style.BRIGHT}Failed to get a new token.")
                return None
        else:
            print(f"{Fore.RED+Style.BRIGHT}Failed to get user information")
            return None

# Function to get balance
def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
    return response.json()

# Function to play the game
def play_game(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers)
    return response.json()

# Function to claim game rewards
def claim_game(token, game_id, points):
    url = "https://game-domain.blum.codes/api/v1/game/claim"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["authorization"] = "Bearer "+token
    headers["content-type"] = "application/json"
    headers["origin"] = "https://telegram.blum.codes"

    headers["priority"] = "u=1, i"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    data = '{"gameId":"'+game_id+'","points":'+str(points)+'}'

    resp = requests.post(url, headers=headers, data=data)
    return resp  # Return the response object, not the text


def claim_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/farming/claim', headers=headers)
    return response.json()

# Function to start farming
def start_farming(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-length': '0',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/farming/start', headers=headers)
    return response.json()

def refresh_token(old_refresh_token):
    url = 'https://gateway.blum.codes/v1/auth/refresh'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'referer': 'https://telegram.blum.codes/'
    }
    data = {
        'refresh': old_refresh_token
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED+Style.BRIGHT}Failed to refresh token for: {old_refresh_token}")
        return None  # or return the response for further handling

def check_balance_friend(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://gateway.blum.codes/v1/friends/balance', headers=headers)
    balance_info = response.json()
    return balance_info

# Function to claim friend's balance
def claim_balance_friend(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post('https://gateway.blum.codes/v1/friends/claim', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim friend's balance: {response.status_code}")
        return None

def check_daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers)
    try:
        return response.json()
    except ValueError:  # Catch error if json cannot be parsed
        print(f"{Fore.RED+Style.BRIGHT}Failed to claim daily")
        return None

# Main loop
with open('tgwebapp.txt', 'r') as file:
    query_ids = file.read().splitlines()
while True:
    for query_id in query_ids:
        token = get_new_token(query_id)  # Get new token
        user_info = get_user_info(token)
        if user_info is None:
            continue
        print(f"{Fore.BLUE+Style.BRIGHT}\r==================[{Fore.WHITE+Style.BRIGHT}{user_info['username']}{Fore.BLUE+Style.BRIGHT}]==================")  
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Getting Info....", end="", flush=True)
        balance_info = get_balance(token)
        print(f"\r{Fore.YELLOW+Style.BRIGHT}[Balance]: {balance_info['availableBalance']}", flush=True)
        print(f"{Fore.RED+Style.BRIGHT}[Game Tickets]: {balance_info['playPasses']}")
        # Check if 'farming' is in balance_info before accessing it
        farming_info = balance_info.get('farming')
        if farming_info:
            end_time_ms = farming_info['endTime']
            end_time_s = end_time_ms / 1000.0
            end_utc_date_time = datetime.datetime.fromtimestamp(end_time_s, datetime.timezone.utc)
            current_utc_time = datetime.datetime.now(datetime.timezone.utc)
            time_difference = end_utc_date_time - current_utc_time
            hours_remaining = int(time_difference.total_seconds() // 3600)
            minutes_remaining = int((time_difference.total_seconds() % 3600) // 60)
            print(f"Claim Time: {hours_remaining} hours {minutes_remaining} minutes | Balance: {farming_info['balance']}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}Farming information not available")
        # Check daily reward
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Checking daily reward...", end="", flush=True)
        daily_reward_response = check_daily_reward(token)
        if daily_reward_response is None:
            print(f"\r{Fore.RED+Style.BRIGHT}Failed to check daily reward, trying again...", flush=True)
        else:
            if daily_reward_response['message'] == 'same day':
                print(f"\r{Fore.RED+Style.BRIGHT}Daily reward already claimed today", flush=True)
            elif daily_reward_response['message'] == 'OK':
                print(f"\r{Fore.GREEN+Style.BRIGHT}Daily reward successfully claimed!", flush=True)
        # print(daily_reward_response)

        if hours_remaining < 0:
            print(f"\r{Fore.GREEN+Style.BRIGHT}Claiming balance...", end="", flush=True)
            claim_response = claim_balance(token)
            if claim_response:
                print(f"\r{Fore.GREEN+Style.BRIGHT}Claimed: {claim_response['availableBalance']}                ", flush=True)
                print(f"\r{Fore.GREEN+Style.BRIGHT}Starting farming...", end="", flush=True)
                start_response = start_farming(token)
                if start_response:
                    print(f"\r{Fore.GREEN+Style.BRIGHT}Farming started.", flush=True)
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}Failed to start farming", start_response.status_code, flush=True)
            else:
                print(f"\r{Fore.RED+Style.BRIGHT}Failed to claim", claim_response.status_code, flush=True)
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Checking referral balance...", end="", flush=True)
        friend_balance = check_balance_friend(token)
        if friend_balance:
            if friend_balance['canClaim']:
                print(f"\r{Fore.GREEN+Style.BRIGHT}Referral Balance: {friend_balance['amountForClaim']}", flush=True)
                print(f"\n\r{Fore.GREEN+Style.BRIGHT}Claiming referral balance.....", flush=True)
                claim_friend_balance = claim_balance_friend(token)
                if claim_friend_balance:
                    claimed_amount = claim_friend_balance['claimBalance']
                    print(f"\r{Fore.GREEN+Style.BRIGHT}Successfully claimed total: {claimed_amount}", flush=True)
                else:
                    print(f"\r{Fore.RED+Style.BRIGHT}Failed to claim referral balance", flush=True)
            else:
                # Check if 'canClaimAt' exists before accessing it
                can_claim_at = friend_balance.get('canClaimAt')
                if can_claim_at:
                    claim_time = datetime.datetime.fromtimestamp(int(can_claim_at) / 1000)
                    current_time = datetime.datetime.now()
                    time_diff = claim_time - current_time
                    hours, remainder = divmod(int(time_diff.total_seconds()), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    print(f"{Fore.RED+Style.BRIGHT}\rReferral Balance: Claim in {hours} hours {minutes} minutes", flush=True)
                else:
                    print(f"{Fore.RED+Style.BRIGHT}\rReferral Balance: No referrals on the account", flush=True)
        else:
            print(f"{Fore.RED+Style.BRIGHT}\rFailed to check referral balance", flush=True)
        while balance_info['playPasses'] > 0:
            print(f"{Fore.CYAN+Style.BRIGHT}Playing game...")
            game_response = play_game(token)
            print(f"\r{Fore.CYAN+Style.BRIGHT}Checking game...", end="", flush=True)
            time.sleep(1)
            claim_response = claim_game(token, game_response['gameId'], 2000)
            if claim_response is None:
                print(f"\r{Fore.RED+Style.BRIGHT}Failed to claim game, trying again...", flush=True)
            while True:
                if claim_response.text == '{"message":"game session not finished"}':
                    time.sleep(1)  # Wait a moment before trying again
                    print(f"\r{Fore.RED+Style.BRIGHT}Game not finished yet.. trying again", flush=True)
                    claim_response = claim_game(token, game_response['gameId'], 2000)
                    if claim_response is None:
                        print(f"\r{Fore.RED+Style.BRIGHT}Failed to claim game, trying again...", flush=True)
                elif claim_response.text == '{"message":"game session not found"}':
                    print(f"\r{Fore.RED+Style.BRIGHT}Game has ended", flush=True)
                    break
                elif 'message' in claim_response and claim_response['message'] == 'Token is invalid':
                    print(f"{Fore.RED+Style.BRIGHT}Token is invalid, getting new token...")
                    token = get_new_token(query_id)  # Assume query_id is available in this scope
                    continue  # Return to the start of the loop to try again with a new token
                else:
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}Game finished: {claim_response.text}", flush=True)
                    break
            # After claiming the game, check the number of tickets again
            balance_info = get_balance(token)  # Refresh balance information to get the latest tickets
            if balance_info['playPasses'] > 0:
                print(f"\r{Fore.GREEN+Style.BRIGHT}Tickets still available, playing game again...", flush=True)
                continue  # Continue loop to play game again
            else:
                print(f"\r{Fore.RED+Style.BRIGHT}No tickets left.", flush=True)
                break

        
    print(f"\n{Fore.GREEN+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}All accounts processed successfully{Fore.GREEN+Style.BRIGHT}=========", end="", flush=True)
    print(f"\r\n\n{Fore.GREEN+Style.BRIGHT}Refreshing token...", end="", flush=True)
    import sys
    wait_time = 30  # 5 minutes in seconds
    for seconds in range(wait_time, 0, -1):
        sys.stdout.write(f"\r{Fore.CYAN}Waiting for the next claim time in {Fore.CYAN}{Fore.WHITE}{seconds // 60} minutes {Fore.WHITE}{seconds % 60} seconds")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rNext claim time has arrived!                                                          \n")


