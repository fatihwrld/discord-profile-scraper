import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from colorama import Fore, init

init()
load_dotenv()

def time_now():
    return datetime.now().strftime("%H:%M:%S")

bot_token = os.getenv("BOT_TOKEN")
if not bot_token:
    print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}Error: BOT_TOKEN not found. Please check the .env file.{Fore.RESET}")
    exit(1)

user_id = input(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.CYAN}[Enter User ID] > {Fore.RESET}").strip()
if not user_id or not user_id.isdigit():
    print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}Error: Enter a valid user ID.{Fore.RESET}")
    exit(1)

url = f"https://discord.com/api/v9/users/{user_id}"
headers = {"Authorization": f"Bot {bot_token}"}

def get_creation_date(user_id):
    DISCORD_EPOCH = 1420070400000
    timestamp = ((int(user_id) >> 22) + DISCORD_EPOCH) / 1000
    creation_date = datetime.fromtimestamp(timestamp, timezone.utc)
    return creation_date.strftime("%a, %d %b %Y %H:%M:%S %Z")

def get_avatar_url(user_id, avatar_hash):
    if avatar_hash:
        if avatar_hash.startswith('a_'):
            return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.gif?size=1024"
        return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=1024"
    return None

def get_banner_url(user_id, banner_hash):
    if banner_hash:
        if banner_hash.startswith('a_'):
            return f"https://cdn.discordapp.com/banners/{user_id}/{banner_hash}.gif?size=1024"
        return f"https://cdn.discordapp.com/banners/{user_id}/{banner_hash}.png?size=1024"
    return None

def get_user_info():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            creation_date = get_creation_date(user_data['id'])
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[Username] > {Fore.LIGHTWHITE_EX}{user_data['username']}{Fore.RESET}")
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[ID] > {Fore.LIGHTWHITE_EX}{user_data['id']}{Fore.RESET}")
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[Creation Date] > {Fore.LIGHTWHITE_EX}{creation_date}{Fore.RESET}")
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[Avatar URL] > {Fore.LIGHTWHITE_EX}{get_avatar_url(user_data['id'], user_data.get('avatar')) or 'This user has no avatar'}{Fore.RESET}")
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[Banner URL] > {Fore.LIGHTWHITE_EX}{get_banner_url(user_data['id'], user_data.get('banner')) or 'This user has no banner'}{Fore.RESET}")
            print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.GREEN}[Badges] > {Fore.LIGHTWHITE_EX}{user_flags(user_data.get('public_flags', 0))}{Fore.RESET}")
        else:
            if response.status_code == 404:
                print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}User not found.{Fore.RESET}")
            elif response.status_code == 403:
                print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}You do not have permission to access this user's information.{Fore.RESET}")
            elif response.status_code == 429:
                print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}Too many requests. Please try again later.{Fore.RESET}")
            else:
                print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}Error: {response.status_code} - An issue occurred.{Fore.RESET}")
    except Exception as e:
        print(f"[{Fore.LIGHTWHITE_EX}{time_now()}{Fore.RESET}] {Fore.RED}Error: {e}{Fore.RESET}")

def user_flags(flags_value):
    if not flags_value or flags_value == 0:
        return "This user has no badges."
    
    flags = {
        1 << 0: "Discord Staff",
        1 << 1: "Discord Partner",
        1 << 2: "HypeSquad Events Member",
        1 << 3: "Bug Hunter",
        1 << 6: "House Bravery Member",
        1 << 7: "House Brilliance Member",
        1 << 8: "House Balance Member",
        1 << 9: "Early Supporter",
        1 << 10: "Team Pseudo User",
        1 << 14: "Gold Bug Hunter",
        1 << 16: "Verified Bot",
        1 << 17: "Verified Bot Developer",
        1 << 18: "Certified Moderator",
        1 << 19: "Gold Bug Hunter",
        1 << 22: "Active Developer",
    }
    result = [flag_name for bit, flag_name in flags.items() if flags_value & bit]
    return ", ".join(result) if result else "Unknown Badges"

if __name__ == "__main__":
    print()
    get_user_info()