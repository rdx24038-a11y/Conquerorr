import hmac
import hashlib
import requests

_account_gen_counter = 0
_RESTART_AFTER = 200

def rotate_tor_ip():
    global _account_gen_counter
    _account_gen_counter += 1
    if _account_gen_counter >= _RESTART_AFTER:
        print(f"🔄 Auto restart at {_account_gen_counter}!")
        import os, sys, time
        time.sleep(2)
        os.execv(sys.executable, [sys.executable] + sys.argv)
import string
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import codecs
import time
from datetime import datetime
from colorama import Fore, Style, init
import urllib3
import os
import sys
import base64
import signal
import threading
import psutil
import re
import subprocess
import importlib


AUTO_MODE = True

# Bot Settings
TELEGRAM_TOKEN = "8553943256:AAH55lzQDh5JvzlSL42hC2kBStvXwdjYjCY"
TELEGRAM_CHAT_ID = "7689716399"
BOT_ACCOUNT_COUNT = 50
BOT_ACCOUNT_NAME = "Kca"
BOT_PASSWORD_PREFIX = "Sn"

def send_telegram(msg):
    try:
        import requests
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}", timeout=10)
    except: pass

def send_file_telegram(filepath):
    try:
        import requests, os
        if os.path.exists(filepath) and os.path.getsize(filepath) > 2:
            with open(filepath, 'rb') as f:
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument",
                    files={"document": (os.path.basename(filepath), f)},
                    data={"chat_id": TELEGRAM_CHAT_ID}, timeout=30)
    except: pass

def start_telegram_bot():
    import threading, requests, glob, json
    def listen():
        global BOT_ACCOUNT_COUNT, BOT_ACCOUNT_NAME, BOT_PASSWORD_PREFIX, SUCCESS_COUNTER
        offset = 0
        while True:
            try:
                r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=30", timeout=40)
                for update in r.json().get("result", []):
                    offset = update["update_id"] + 1
                    msg = update.get("message", {}).get("text", "")
                    cid = update.get("message", {}).get("chat", {}).get("id", "")
                    if msg == "/count":
                        try:
                            total = 0
                            for fp in glob.glob(str(ACCOUNTS_FOLDER) + "/*.json"):
                                with open(fp) as jf:
                                    total += len(json.load(jf))
                            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=📊 Total: {total}\nSession: {SUCCESS_COUNTER}", timeout=5)
                        except:
                            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=Session: {SUCCESS_COUNTER}", timeout=5)
                    elif msg == "/download":
                        files = glob.glob(str(ACCOUNTS_FOLDER) + "/*.json")
                        if files:
                            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=📁 Sending {len(files)} file(s)...", timeout=5)
                            for fp in files: send_file_telegram(fp)
                        else:
                            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=❌ No files yet!", timeout=5)
                    elif msg.startswith("/setcount "):
                        try:
                            BOT_ACCOUNT_COUNT = int(msg.split()[1])
                            requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=✅ Count: {BOT_ACCOUNT_COUNT}", timeout=5)
                        except: pass
                    elif msg.startswith("/setname "):
                        BOT_ACCOUNT_NAME = msg.split()[1]
                        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=✅ Name: {BOT_ACCOUNT_NAME}", timeout=5)
                    elif msg.startswith("/setpass "):
                        BOT_PASSWORD_PREFIX = msg.split()[1]
                        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=✅ Pass: {BOT_PASSWORD_PREFIX}", timeout=5)
                    elif msg == "/status":
                        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={cid}&text=⚙️ Count:{BOT_ACCOUNT_COUNT} Name:{BOT_ACCOUNT_NAME} Pass:{BOT_PASSWORD_PREFIX}\nTotal:{SUCCESS_COUNTER}", timeout=5)
            except: pass
    threading.Thread(target=listen, daemon=True).start()


def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        return ""


init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_random_color():
    colors = [
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTWHITE_EX,
     Fore.LIGHTBLUE_EX]
    return random.choice(colors)


class Colors:
    BRIGHT = Style.BRIGHT
    RESET = Style.RESET_ALL


EXIT_FLAG = False
SUCCESS_COUNTER = 0
TARGET_ACCOUNTS = 0
RARE_COUNTER = 0
COUPLES_COUNTER = 0
RARITY_SCORE_THRESHOLD = 3
LOCK = threading.Lock()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(CURRENT_DIR, "BIGBULL-ERA")
TOKENS_FOLDER = os.path.join(BASE_FOLDER, "TOKENS-JWT")
ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "ACCOUNTS")
RARE_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "RARE ACCOUNTS")
COUPLES_ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "COUPLES ACCOUNTS")
GHOST_FOLDER = os.path.join(BASE_FOLDER, "GHOST")
GHOST_ACCOUNTS_FOLDER = os.path.join(GHOST_FOLDER, "ACCOUNTS")
GHOST_RARE_FOLDER = os.path.join(GHOST_FOLDER, "RAREACCOUNT")
GHOST_COUPLES_FOLDER = os.path.join(GHOST_FOLDER, "COUPLESACCOUNT")

for folder in [
    BASE_FOLDER,
    TOKENS_FOLDER,
    ACCOUNTS_FOLDER,
    RARE_ACCOUNTS_FOLDER,
    COUPLES_ACCOUNTS_FOLDER,
    GHOST_FOLDER,
    GHOST_ACCOUNTS_FOLDER,
    GHOST_RARE_FOLDER,
     GHOST_COUPLES_FOLDER]:
    os.makedirs(folder, exist_ok=True)

REGION_LANG = {
    "ME": "ar",
    "IND": "hi",
    "ID": "id",
    "VN": "vi",
    "TH": "th",
    "BD": "bn",
    "PK": "ur",
    "TW": "zh",
    "CIS": "ru",
    "SAC": "es",
     "BR": "pt"}
REGION_URLS = {
    "IND": "https://client.ind.freefiremobile.com/",
    "ID": "https://clientbp.ggblueshark.com/",
    "BR": "https://client.us.freefiremobile.com/",
    "ME": "https://clientbp.common.ggbluefox.com/",
    "VN": "https://clientbp.ggblueshark.com/",
    "TH": "https://clientbp.common.ggbluefox.com/",
    "CIS": "https://clientbp.ggblueshark.com/",
    "BD": "https://clientbp.ggblueshark.com/",
    "PK": "https://clientbp.ggblueshark.com/",
    "SG": "https://clientbp.ggblueshark.com/",
    "SAC": "https://client.us.freefiremobile.com/",
     "TW": "https://clientbp.ggblueshark.com/"}
hex_key = "32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533"
key = bytes.fromhex(hex_key)
hex_data = "8J+agCBQUkVNSVVNIEFDQ09VTlQgR0VORVJBVE9SIPCfkqsgQnkgU1BJREVFUklPIHwgTm90IEZvciBTYWxlIPCfkas="
client_data = base64.b64decode(hex_data).decode('utf-8')
GARENA = "UklaRVI="

FILE_LOCKS = {}


def get_file_lock(filename):
    if filename not in FILE_LOCKS:
        FILE_LOCKS[filename] = threading.Lock()
    return FILE_LOCKS[filename]


ACCOUNT_RARITY_PATTERNS = {
    "REPEATED_DIGITS_4": [r"(\d)\1{3,}", 3],
    "REPEATED_DIGITS_3": [r"(\d)\1\1(\d)\2\2", 2],
    "SEQUENTIAL_5": [r"(12345|23456|34567|45678|56789)", 4],
    "SEQUENTIAL_4": [r"(0123|1234|2345|3456|4567|5678|6789|9876|8765|7654|6543|5432|4321|3210)", 3],
    "PALINDROME_6": [r"^(\d)(\d)(\d)\3\2\1$", 5],
    "PALINDROME_4": [r"^(\d)(\d)\2\1$", 3],
    "SPECIAL_COMBINATIONS_HIGH": [r"(69|420|1337|007)", 4],
    "SPECIAL_COMBINATIONS_MED": [r"(100|200|300|400|500|666|777|888|999)", 2],
    "QUADRUPLE_DIGITS": [r"(1111|2222|3333|4444|5555|6666|7777|8888|9999|0000)", 4],
    "MIRROR_PATTERN_HIGH": [r"^(\d{2,3})\1$", 3],
    "MIRROR_PATTERN_MED": [r"(\d{2})0\1", 2],
    "GOLDEN_RATIO": [r"1618|0618", 3]
}

ACCOUNT_COUPLES_PATTERNS = {
    "MATCHING_PAIRS": [
        r"(\d{2})01.*\d{2}02",
        r"(\d{2})11.*\d{2}12",
        r"(\d{2})21.*\d{2}22",
    ],
    "COMPLEMENTARY_DIGITS": [
        r".*13.*14$",
        r".*07.*08$",
        r".*51.*52$",
    ],
    "LOVE_NUMBERS": [
        r".*520.*521$",
        r".*1314$",
    ]
}

POTENTIAL_COUPLES = {}
COUPLES_LOCK = threading.Lock()


def check_account_rarity(account_data):
    account_id = account_data.get("account_id", "")

    if account_id == "N/A" or not account_id:
        return False, None, None, 0

    rarity_score = 0
    detected_patterns = []

    for rarity_type, pattern_data in ACCOUNT_RARITY_PATTERNS.items():
        pattern = pattern_data[0]
        score = pattern_data[1]
        if re.search(pattern, account_id):
            rarity_score += score
            detected_patterns.append(rarity_type)

    account_id_digits = [int(d) for d in account_id if d.isdigit()]

    if len(set(account_id_digits)) == 1 and len(account_id_digits) >= 4:
        rarity_score += 5
        detected_patterns.append("UNIFORM_DIGITS")

    if len(account_id_digits) >= 4:
        differences = [account_id_digits[i + 1] - account_id_digits[i]
                       for i in range(len(account_id_digits) - 1)]
        if len(set(differences)) == 1:
            rarity_score += 4
            detected_patterns.append("ARITHMETIC_SEQUENCE")

    if len(account_id) <= 8 and account_id.isdigit() and int(account_id) < 1000000:
        rarity_score += 3
        detected_patterns.append("LOW_ACCOUNT_ID")

    if rarity_score >= RARITY_SCORE_THRESHOLD:
        reason = f"Account ID {account_id} - Score: {rarity_score} - Patterns: {', '.join(detected_patterns)}"
        return True, "RARE_ACCOUNT", reason, rarity_score

    return False, None, None, rarity_score


def check_account_couples(account_data, thread_id):
    account_id = account_data.get("account_id", "")

    if account_id == "N/A" or not account_id:
        return False, None, None

    with COUPLES_LOCK:
        for stored_id, stored_data in POTENTIAL_COUPLES.items():
            stored_account_id = stored_data.get('account_id', '')

            couple_found, reason = check_account_couple_patterns(
                account_id, stored_account_id)
            if couple_found:
                partner_data = stored_data
                del POTENTIAL_COUPLES[stored_id]
                return True, reason, partner_data

        POTENTIAL_COUPLES[account_id] = {
            'uid': account_data.get('uid', ''),
            'account_id': account_id,
            'name': account_data.get('name', ''),
            'password': account_data.get('password', ''),
            'region': account_data.get('region', ''),
            'thread_id': thread_id,
            'timestamp': datetime.now().isoformat()
        }

    return False, None, None


def check_account_couple_patterns(account_id1, account_id2):
    try:
        if account_id1 and account_id2 and abs(
            int(account_id1) - int(account_id2)) == 1:
            return True, f"Sequential Account IDs: {account_id1} & {account_id2}"
    except:
        pass

    if account_id1 == account_id2[::-1]:
        return True, f"Mirror Account IDs: {account_id1} & {account_id2}"

    try:
        if account_id1 and account_id2:
            sum_acc = int(account_id1) + int(account_id2)
            if sum_acc % 1000 == 0 or sum_acc % 10000 == 0:
                return True, f"Complementary sum: {account_id1} + {account_id2} = {sum_acc}"
    except:
        pass

    love_numbers = ['520', '521', '1314', '3344']
    for love_num in love_numbers:
        if love_num in account_id1 and love_num in account_id2:
            return True, f"Both contain love number: {love_num}"

    return False, None

def save_rare_account(
    account_data,
    rarity_type,
    reason,
    rarity_score,
    is_ghost=False
):
    try:
        if is_ghost:
            rare_filename = os.path.join(GHOST_RARE_FOLDER, "rare-ghost.json")
        else:
            region = account_data.get('region', 'UNKNOWN')
            rare_filename = os.path.join(
                RARE_ACCOUNTS_FOLDER, f"rare-{region}.json"
            )

        rare_entry = {
            'uid': account_data["uid"],
            'password': account_data["password"],
            'account_id': account_data.get("account_id", "N/A"),
            'name': account_data["name"],
            'region': "BIGBULL" if is_ghost else account_data.get('region', 'UNKNOWN'),
            'rarity_type': rarity_type,
            'rarity_score': rarity_score,
            'reason': reason,
            'date_identified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': account_data.get('jwt_token', ''),
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(rare_filename)
        with file_lock:
            rare_list = []
            if os.path.exists(rare_filename):
                try:
                    with open(rare_filename, 'r', encoding='utf-8') as f:
                        rare_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    rare_list = []

            existing_ids = [acc.get('account_id') for acc in rare_list]
            if account_data.get("account_id", "N/A") not in existing_ids:
                rare_list.append(rare_entry)

                temp_filename = rare_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(rare_list, f, indent=2, ensure_ascii=False)

                os.replace(temp_filename, rare_filename)
                return True
            else:
                return False

    except Exception as e:
        print_error(f"Error saving rare account: {e}")
        return False

def save_couples_account(account1, account2, reason, is_ghost=False):
    try:
        if is_ghost:
            couples_filename = os.path.join(
                GHOST_COUPLES_FOLDER, "couples-ghost.json"
            )
        else:
            region = account1.get('region', 'UNKNOWN')
            couples_filename = os.path.join(
                COUPLES_ACCOUNTS_FOLDER, f"couples-{region}.json"
            )

        couples_entry = {
            'couple_id': f"{account1.get('account_id', 'N/A')}_{account2.get('account_id', 'N/A')}",
            'account1': {
                'uid': account1["uid"],
                'password': account1["password"],
                'account_id': account1.get("account_id", "N/A"),
                'name': account1["name"],
                'thread_id': account1.get('thread_id', 'N/A')
            },
            'account2': {
                'uid': account2["uid"],
                'password': account2["password"],
                'account_id': account2.get("account_id", "N/A"),
                'name': account2["name"],
                'thread_id': account2.get('thread_id', 'N/A')
            },
            'reason': reason,
            'region': "BIGBULL" if is_ghost else account1.get('region', 'UNKNOWN'),
            'date_matched': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        file_lock = get_file_lock(couples_filename)
        with file_lock:
            couples_list = []
            if os.path.exists(couples_filename):
                try:
                    with open(couples_filename, 'r', encoding='utf-8') as f:
                        couples_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    couples_list = []

            existing_couples = [couple.get('couple_id') for couple in couples_list]
            if couples_entry['couple_id'] not in existing_couples:
                couples_list.append(couples_entry)

                temp_filename = couples_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(couples_list, f, indent=2, ensure_ascii=False)

                os.replace(temp_filename, couples_filename)
                return True
            else:
                return False

    except Exception as e:
        print_error(f"Error saving couples account: {e}")
        return False


def print_rarity_found(account_data, rarity_type, reason, rarity_score):
    color = Fore.LIGHTMAGENTA_EX
    print(f"\n{color}{Colors.BRIGHT}💎 RARE ACCOUNT FOUND!{Colors.RESET}")
    print(f"{color}🎯 Type: {rarity_type}{Colors.RESET}")
    print(f"{color}⭐ Rarity Score: {rarity_score}{Colors.RESET}")
    print(f"{color}👤 Name: {account_data['name']}{Colors.RESET}")
    print(f"{color}🆔 UID: {account_data['uid']}{Colors.RESET}")
    print(f"{color}🎮 Account ID: {account_data.get('account_id', 'N/A')}{Colors.RESET}")
    print(f"{color}📝 Reason: {reason}{Colors.RESET}")
    print(f"{color}🧵 Thread: {account_data.get('thread_id', 'N/A')}{Colors.RESET}")
    print(f"{color}🌍 Region: {account_data.get('region', 'N/A')}{Colors.RESET}\n")


def print_couples_found(account1, account2, reason):
    color = Fore.LIGHTCYAN_EX
    print(f"\n{color}{Colors.BRIGHT}💑 COUPLES ACCOUNT FOUND!{Colors.RESET}")
    print(f"{color}📝 Reason: {reason}{Colors.RESET}")

    print(f"{color}👤 Account 1: {account1['name']} "
          f"(ID: {account1.get('account_id', 'N/A')}) - "
          f"Thread {account1.get('thread_id', 'N/A')}{Colors.RESET}")

    print(f"{color}👤 Account 2: {account2['name']} "
          f"(ID: {account2.get('account_id', 'N/A')}) - "
          f"Thread {account2.get('thread_id', 'N/A')}{Colors.RESET}")

    print(f"{color}🆔 UIDs: {account1['uid']} & {account2['uid']}{Colors.RESET}")
    print(f"{color}🌍 Region: {account1.get('region', 'N/A')}{Colors.RESET}\n")

def install_requirements():
    required_packages = [
        'requests',
        'pycryptodome',
        'colorama',
        'urllib3',
        'psutil'
    ]

    print(f"{get_random_color()}{Colors.BRIGHT}🔍 Checking required packages...{Colors.RESET}")

    for package in required_packages:
        try:
            if package == 'pycryptodome':
                import Crypto
            else:
                importlib.import_module(package)
            print(f"{get_random_color()}✅ {package} is installed{Colors.RESET}")
        except ImportError:
            print(f"{get_random_color()}⚠️ Installing {package}...{Colors.RESET}")
            try:
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', package])
                print(f"{get_random_color()}✅ {package} installed successfully{Colors.RESET}")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}❌ Failed to install {package}{Colors.RESET}")
                return False
    return True


def get_region(language_code: str) -> str:
    return REGION_LANG.get(language_code, "IND")  # 👈 default safe


def get_region_url(region_code: str) -> str:
    return REGION_URLS.get(region_code, "https://clientbp.ggblueshark.com/")


def safe_exit(signum=None, frame=None):
    global EXIT_FLAG
    EXIT_FLAG = True
    color = get_random_color()
    print(f"\n{color}{Colors.BRIGHT}🚨 Safe exit triggered. Closing script...{Colors.RESET}")
    sys.exit(0)


signal.signal(signal.SIGINT, safe_exit)
signal.signal(signal.SIGTERM, safe_exit)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    color = get_random_color()
    banner = f"""
{color}{Colors.BRIGHT}
                ██████╗░██╗░██████╗░██████╗░██╗░░░██╗██╗░░░░░
                ██╔══██╗██║██╔════╝░██╔══██╗██║░░░██║██║░░░░░
                ██████╦╝██║██║░░██╗░██████╦╝██║░░░██║██║░░░░░
                ██╔══██╗██║██║░░╚██╗██╔══██╗██║░░░██║██║░░░░░
                ██████╦╝██║╚██████╔╝██████╦╝╚██████╔╝███████╗
                 ╚═════╝░╚═╝░╚═════╝░╚═════╝░░╚═════╝░╚══════╝

               ░█████╗░██╗░░██╗███████╗░█████╗░████████╗░██████╗
               ██╔══██╗██║░░██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝
               ██║░░╚═╝███████║█████╗░░███████║░░░██║░░░╚█████╗░
               ██║░░██╗██╔══██║██╔══╝░░██╔══██║░░░██║░░░░╚═══██╗
               ╚█████╔╝██║░░██║███████╗██║░░██║░░░██║░░░██████╔╝
               ░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═════╝

{Colors.RESET}

{get_random_color()}{Colors.BRIGHT}                         ACCESS GRANTED ✅
{get_random_color()}{Colors.BRIGHT}        🚨 BIGBULL V12 PRO VERSION 🚨  [PAID VERSION]
{get_random_color()}{Colors.BRIGHT}         WELCOME TO BIGBULL V12 PRO GENERATER.
{get_random_color()}{Colors.BRIGHT}      USE BBC.SH AND 1.1.1.1 VPN TO GENERATE THE ACCOUNTS
{get_random_color()}{Colors.BRIGHT}           THEN START GENERATER, NO IP BAN.
{Colors.RESET}
"""
    print(banner)


def print_success(message):
    color = get_random_color()
    print(f"{color}{Colors.BRIGHT}✅ {message}{Colors.RESET}")


def print_error(message):
    print(f"{Fore.RED}{Colors.BRIGHT}❌ {message}{Colors.RESET}")


def print_warning(message):
    print(f"{Fore.YELLOW}{Colors.BRIGHT}⚠️ {message}{Colors.RESET}")


def print_rare(message):
    print(f"{Fore.LIGHTMAGENTA_EX}{Colors.BRIGHT}💎 {message}{Colors.RESET}")


def print_registration_status(
    count,
    total,
    name,
    uid,
    password,
    account_id,
    region,
    is_ghost=False
):
    print(f"{get_random_color()}{Colors.BRIGHT}📝 Registration {count}/{total}{Colors.RESET}")
    print(f"{get_random_color()}👤 Name: {get_random_color()}{name}{Colors.RESET}")
    print(f"{get_random_color()}🆔 UID: {get_random_color()}{uid}{Colors.RESET}")
    print(f"{get_random_color()}🎮 Account ID: {get_random_color()}{account_id}{Colors.RESET}")
    print(f"{get_random_color()}🔑 Password: {get_random_color()}{password}{Colors.RESET}")

    if is_ghost:
        print(f"{get_random_color()}🌍 Mode: {Fore.LIGHTMAGENTA_EX}GHOST Mode{Colors.RESET}")
    else:
        print(f"{get_random_color()}🌍 Region: {get_random_color()}{region}{Colors.RESET}")

    print()


def generate_exponent_number():
    exponent_digits = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
     '9': '⁹'}
    number = random.randint(1, 99999)
    number_str = f"{number:05d}"
    exponent_str = ''.join(exponent_digits[digit] for digit in number_str)
    return exponent_str


def generate_random_name(base_name):
    exponent_part = generate_exponent_number()
    return f"{base_name[:7]}{exponent_part}"


def generate_custom_password(prefix):
    try:
        garena_decoded = base64.b64decode(GARENA).decode('utf-8')
    except Exception:
        garena_decoded = "GARENA"

    characters = string.ascii_uppercase + string.digits
    random_part1 = ''.join(random.choice(characters) for _ in range(5))
    random_part2 = ''.join(random.choice(characters) for _ in range(5))

    return f"{prefix}_{random_part1}_{garena_decoded}_{random_part2}"


def EnC_Vr(N):
    if N < 0:
        return b''

    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N:
            BesTo |= 0x80
        H.append(BesTo)
        if not N:
            break

    return bytes(H)


def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)


def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value


def CrEaTe_ProTo(fields):
    packet = bytearray()

    for field, value in fields.items():
        if value is None:
            continue  # skip safely

        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))

        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))

        elif isinstance(value, (str, bytes)):
            packet.extend(CrEaTe_LenGTh(field, value))

        else:
            raise TypeError(f"Unsupported type for field {field}: {type(value)}")

    return packet


def encrypt_aes(hex_data, return_hex=False):
    try:
        data = bytes.fromhex(hex_data)
    except ValueError:
        raise ValueError(f"Invalid hex input for AES encryption: {hex_data}")

    key = bytes([89, 103, 38, 116, 99, 37, 68, 69,
                 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50,
                69, 51, 121, 99, 104, 106, 77, 37])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))

    return encrypted.hex() if return_hex else encrypted


def save_jwt_token(account_data, jwt_token, region, is_ghost=False):
    try:
        if is_ghost:
            token_filename = os.path.join(GHOST_FOLDER, "tokens-ghost.json")
        else:
            token_filename = os.path.join(TOKENS_FOLDER, f"tokens-{region}.json")

        account_id = account_data.get("account_id", "N/A")
        uid = account_data.get("uid", "N/A")

        token_entry = {
            'uid': uid,
            'account_id': account_id,
            'jwt_token': jwt_token,
            'name': account_data.get("name", "N/A"),
            'password': account_data.get("password", "N/A"),
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': "BIGBULL" if is_ghost else region,
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(token_filename)
        with file_lock:
            tokens_list = []

            if os.path.exists(token_filename):
                try:
                    with open(token_filename, 'r', encoding='utf-8') as f:
                        tokens_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    tokens_list = []

            # ✅ stronger duplicate check
            existing_keys = {
                (t.get('account_id'), t.get('uid')) for t in tokens_list
            }

            if (account_id, uid) not in existing_keys:
                tokens_list.append(token_entry)

                temp_filename = token_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(tokens_list, f, indent=2, ensure_ascii=False)

                os.replace(temp_filename, token_filename)
                return True
            else:
                return False

    except Exception as e:
        print_error(f"Error saving JWT token: {e}")
        return False


def save_normal_account(account_data, region, is_ghost=False):
    try:
        if is_ghost:
            account_filename = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
        else:
            account_filename = os.path.join(ACCOUNTS_FOLDER, f"accounts-{region}.json")

        account_id = account_data.get("account_id", "N/A")
        uid = account_data.get("uid", "N/A")

        account_entry = {
            'uid': uid,
            'password': account_data.get("password", "N/A"),
            'account_id': account_id,
            'name': account_data.get("name", "N/A"),
            'region': "BIGBULL" if is_ghost else region,
            'date_created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'thread_id': account_data.get('thread_id', 'N/A')
        }

        file_lock = get_file_lock(account_filename)
        with file_lock:
            accounts_list = []

            if os.path.exists(account_filename):
                try:
                    with open(account_filename, 'r', encoding='utf-8') as f:
                        accounts_list = json.load(f)
                except (json.JSONDecodeError, IOError):
                    accounts_list = []

            # ✅ strong duplicate check
            existing_keys = {
                (acc.get('account_id'), acc.get('uid')) for acc in accounts_list
            }

            if (account_id, uid) not in existing_keys:
                accounts_list.append(account_entry)

                temp_filename = account_filename + '.tmp'
                with open(temp_filename, 'w', encoding='utf-8') as f:
                    json.dump(accounts_list, f, indent=2, ensure_ascii=False)

                os.replace(temp_filename, account_filename)
                return True
            else:
                return False

    except Exception as e:
        print_error(f"Error saving normal account: {e}")
        return False

def smart_delay():
    time.sleep(random.uniform(1, 2))


def create_acc(region, account_name, password_prefix, is_ghost=False):
    if EXIT_FLAG:
        return None

    try:
        password = generate_custom_password(password_prefix)
        data = f"password={password}&client_type=2&source=2&app_id=100067"
        message = data.encode('utf-8')

        if not key:
            print_error("HMAC key missing!")
            return None

        signature = hmac.new(key, message, hashlib.sha256).hexdigest()

        url = "https://100067.connect.garena.com/oauth/guest/register"
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
            "Authorization": "Signature " + signature,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        response = requests.post(
            url,
            headers=headers,
            data=data,
            timeout=30,
            verify=False
        )

        response.raise_for_status()

        # ✅ safe JSON parsing
        try:
            response_data = response.json()
        except ValueError:
            print_warning("Invalid JSON response")
            return None

        if 'uid' in response_data:
            uid = response_data['uid']
            print_success(f"Guest account created: {uid}")
            rotate_tor_ip()
            smart_delay()

            return token(
                uid,
                password,
                region,
                account_name,
                password_prefix,
                is_ghost
            )

        return None

    except requests.exceptions.RequestException as e:
        print_warning(f"Network error: {e}")

    except Exception as e:
        print_warning(f"Create account failed: {e}")

    smart_delay()
    return None


def token(
    uid,
    password,
    region,
    account_name,
    password_prefix,
    is_ghost=False
):
    if EXIT_FLAG:
        return None

    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD ;Android 12;en;US;)",
        }

        body = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": key,
            "client_id": "100067"
        }

        response = requests.post(
            url,
            headers=headers,
            data=body,
            timeout=30,
            verify=False
        )

        response.raise_for_status()

        # ✅ safe JSON parsing
        try:
            response_data = response.json()
        except ValueError:
            print_warning("Invalid JSON response (token)")
            return None

        if 'open_id' in response_data:
            open_id = response_data.get('open_id')
            access_token = response_data.get("access_token")
            refresh_token = response_data.get('refresh_token')

            if not open_id or not access_token:
                print_warning("Missing token fields")
                return None

            result = encode_string(open_id)

            try:
                field = to_unicode_escaped(result['field_14'])
                field = codecs.decode(field, 'unicode_escape').encode('latin1')
            except Exception:
                print_warning("Field encoding failed")
                return None

            print_success(f"Token granted for: {uid}")
            smart_delay()

            return Major_Regsiter(
                access_token,
                open_id,
                field,
                uid,
                password,
                region,
                account_name,
                password_prefix,
                is_ghost
            )

        return None

    except requests.exceptions.RequestException as e:
        print_warning(f"Network error: {e}")

    except Exception as e:
        print_warning(f"Token grant failed: {e}")

    smart_delay()
    return None


def encode_string(original):
    keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
                 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
    encoded = ""
    for i in range(len(original)):
        orig_byte = ord(original[i])
        key_byte = keystream[i % len(keystream)]
        result_byte = orig_byte ^ key_byte
        encoded += chr(result_byte)
    return {"open_id": original, "field_14": encoded}


def to_unicode_escaped(s):
    return ''.join(c if 32 <= ord(c) <= 126 else f'\\u{ord(c):04x}' for c in s)


def Major_Regsiter(
    access_token,
    open_id,
    field,
    uid,
    password,
    region,
    account_name,
    password_prefix,
    is_ghost=False
):
    if EXIT_FLAG:
        return None

    try:
        region_upper = region.upper()

        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorRegister"
            host = "loginbp.ggblueshark.com"
        else:
            if region_upper in ["ME", "TH"]:
                url = "https://loginbp.common.ggbluefox.com/MajorRegister"
                host = "loginbp.common.ggbluefox.com"
            else:
                url = "https://loginbp.ggblueshark.com/MajorRegister"
                host = "loginbp.ggblueshark.com"

        name = generate_random_name(account_name)

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": host,
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4."
        }

        lang_code = "pt" if is_ghost else REGION_LANG.get(region_upper, "en")

        payload = {
            1: name,
            2: access_token,
            3: open_id,
            5: 102000007,
            6: 4,
            7: 1,
            13: 1,
            14: field,
            15: lang_code,
            16: 1,
            17: 1
        }

        payload_bytes = CrEaTe_ProTo(payload)

        try:
            encrypted_payload = E_AEs(payload_bytes.hex())
        except Exception:
            print_warning("Encryption failed")
            return None

        response = requests.post(
            url,
            headers=headers,
            data=encrypted_payload,
            verify=False,
            timeout=30
        )

        if response.status_code == 200:
            print_success(f"MajorRegister successful: {name}")

            login_result = perform_major_login(
                uid, password, access_token, open_id, region, is_ghost
            )

            if not login_result:
                print_warning("Login result missing")
                return None

            account_id = login_result.get("account_id", "N/A")
            jwt_token = login_result.get("jwt_token", "")

            if (
                not is_ghost and
                jwt_token and
                account_id != "N/A" and
                region_upper != "BR"
            ):
                region_bound = force_region_binding(region, jwt_token)

                if region_bound:
                    print_success(f"Region {region} bound successfully!")
                else:
                    print_warning(f"Region binding failed for {region}")

            account_data = {
                "uid": uid,
                "password": password,
                "name": name,
                "region": "GHOST" if is_ghost else region,
                "status": "success",
                "account_id": account_id,
                "jwt_token": jwt_token
            }

            return account_data

        else:
            print_warning(f"MajorRegister returned status: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print_warning(f"Network error: {e}")

    except Exception as e:
        print_warning(f"Major_Regsiter error: {str(e)}")

    smart_delay()
    return None


def perform_major_login(
    uid,
    password,
    access_token,
    open_id,
    region,
    is_ghost=False
):
    try:
        region_upper = region.upper()
        lang = "pt" if is_ghost else REGION_LANG.get(region_upper, "en")

        payload_parts = [
            b'\x1a\x132025-08-30 05:19:21"\tfree fire(\x01:\x081.114.13B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)J\x08HandheldR\nATM MobilsZ\x04WIFI`\xb6\nh\xee\x05r\x03300z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2\x80\x01\xc9\x0f\x8a\x01\x0fAdreno (TM) 640\x92\x01\rOpenGL ES 3.2\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f\xa2\x01\x0e105.235.139.91\xaa\x01\x02',
            lang.encode("ascii"),
            b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d\xba\x01\x014\xc2\x01\x08Handheld\xca\x01\x10Asus ASUS_I005DA\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390\xf0\x01\x01\xca\x02\nATM Mobils\xd2\x02\x04WIFI\xca\x03 7428b253defc164018c604a1ebbfebdf\xe0\x03\xa8\x81\x02\xe8\x03\xf6\xe5\x01\xf0\x03\xaf\x13\xf8\x03\x84\x07\x80\x04\xe7\xf0\x01\x88\x04\xa8\x81\x02\x90\x04\xe7\xf0\x01\x98\x04\xa8\x81\x02\xc8\x04\x01\xd2\x04=/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/lib/arm\xe0\x04\x01\xea\x04_2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-PdeDnOilCSFn37p1AH_FLg==/base.apk\xf0\x04\x03\xf8\x04\x01\x8a\x05\x0232\x9a\x05\n2019118692\xb2\x05\tOpenGLES2\xb8\x05\xff\x7f\xc0\x05\x04\xe0\x05\xf3F\xea\x05\x07android\xf2\x05pKqsHT5ZLWrYljNb5Vqh//yFRlaPHSO9NWSQsVvOmdhEEn7W+VHNUK+Q+fduA3ptNrGB0Ll0LRz3WW0jOwesLj6aiU7sZ40p8BfUE/FI/jzSTwRe2\xf8\x05\xfb\xe4\x06\x88\x06\x01\x90\x06\x01\x9a\x06\x014\xa2\x06\x014\xb2\x06"GQ@O\x00\x0e^\x00D\x06UA\x0ePM\r\x13hZ\x07T\x06\x0cm\\V\x0ejYV;\x0bU5'
        ]

        payload = b''.join(payload_parts)

        if is_ghost:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
            host = "loginbp.ggblueshark.com"
        elif region_upper in ["ME", "TH"]:
            url = "https://loginbp.common.ggbluefox.com/MajorLogin"
            host = "loginbp.common.ggbluefox.com"
        else:
            url = "https://loginbp.ggblueshark.com/MajorLogin"
            host = "loginbp.ggblueshark.com"

        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": host,
            "ReleaseVersion": "OB52",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1"
        }

        data = payload.replace(
            b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390',
            access_token.encode()
        ).replace(
            b'1d8ec0240ede109973f3321b9354b44d',
            open_id.encode()
        )

        try:
            encrypted_hex = encrypt_api(data.hex())
            final_payload = bytes.fromhex(encrypted_hex)
        except Exception:
            print_warning("Encryption failed (login)")
            return {"account_id": "N/A", "jwt_token": ""}

        response = requests.post(
            url,
            headers=headers,
            data=final_payload,
            verify=False,
            timeout=30
        )

        if response.status_code == 200 and response.content:
            text = response.text

            jwt_start = text.find("eyJ")
            if jwt_start != -1:
                jwt_token = text[jwt_start:]

                # ✅ safer JWT extraction
                parts = jwt_token.split(".")
                if len(parts) >= 3:
                    jwt_token = ".".join(parts[:3])

                    account_id = decode_jwt_token(jwt_token)
                    return {
                        "account_id": account_id,
                        "jwt_token": jwt_token
                    }

        return {"account_id": "N/A", "jwt_token": ""}

    except requests.exceptions.RequestException as e:
        print_warning(f"Network error (login): {e}")

    except Exception as e:
        print_warning(f"MajorLogin failed: {e}")

    return {"account_id": "N/A", "jwt_token": ""}


def decode_jwt_token(jwt_token):
    try:
        parts = jwt_token.split('.')
        if len(parts) >= 2:
            payload_part = parts[1]

            # ✅ safe padding
            padding = (-len(payload_part)) % 4
            payload_part += '=' * padding

            decoded = base64.urlsafe_b64decode(payload_part)
            data = json.loads(decoded)

            account_id = data.get('account_id') or data.get('external_id')
            if account_id:
                return str(account_id)

    except Exception as e:
        print_warning(f"JWT decode failed: {e}")

    return "N/A"


def force_region_binding(region, jwt_token):
    region_upper = region.upper()

    if region_upper in ["ME", "TH"]:
        url = "https://loginbp.common.gqbluefox.com/ChooseRegion"
    else:
        url = "https://loginbp.gqblueshark.com/ChooseRegion"

    if region_upper == "CIS":
        region_code = "RU"
    else:
        region_code = region_upper

    fields = {1: region_code}
    proto_data = CrEaTe_ProTo(fields)

    try:
        encrypted_data = encrypt_api(proto_data.hex())

        if not encrypted_data:
            raise ValueError("Empty encryption result")

        payload = bytes.fromhex(encrypted_data)

    except Exception as e:
        print_warning(f"Encryption failed: {e}")
        payload = proto_data

    headers = {
        'User-Agent': "Dalvik/2.1.0",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': f"Bearer {jwt_token}"
    }

    try:
        response = requests.post(
            url,
            data=payload,
            headers=headers,
            verify=False,
            timeout=30
        )

        return response.status_code == 200

    except requests.exceptions.RequestException as e:
        print_warning(f"Network error (region bind): {e}")

    except Exception as e:
        print_warning(f"Region binding failed: {e}")

    return True


def generate_single_account(
    region,
    account_name,
    password_prefix,
    total_accounts,
    thread_id,
    is_ghost=False
):
    try:
        account_result = create_acc(
            region,
            account_name,
            password_prefix,
            is_ghost
        )

        if not account_result:
            return False

        account_id = account_result.get("account_id", "N/A")
        jwt_token = account_result.get("jwt_token", "")

        account_result['thread_id'] = thread_id

        print_registration_status(
            0,  # count worker handle करेगा
            total_accounts,
            account_result["name"],
            account_result["uid"],
            account_result["password"],
            account_id,
            region,
            is_ghost
        )

        # ✅ Rare check
        is_rare, rarity_type, rarity_reason, rarity_score = check_account_rarity(account_result)
        if is_rare:
            RARE_COUNTER += 1
            print_rarity_found(account_result, rarity_type, rarity_reason, rarity_score)

        # ✅ Couples check
        is_couple, couple_reason, partner_data = check_account_couples(account_result, thread_id)
        if is_couple and partner_data:
            COUPLES_COUNTER += 1
            print_couples_found(account_result, partner_data, couple_reason)

        # ✅ Save
        save_normal_account(account_result, region if not is_ghost else "GHOST")

        if jwt_token:
            save_jwt_token(account_result, jwt_token, region if not is_ghost else "GHOST")

        return True   # 🔥 ONLY TRUE

    except Exception as e:
        print_warning(f"Account generation failed: {e}")
        return False


def worker(
    region,
    account_name,
    password_prefix,
    total_accounts,
    thread_id,
    is_ghost=False
):
    thread_color = get_random_color()

    print(
        f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} started{Colors.RESET}"
    )

    accounts_generated = 0

    while not EXIT_FLAG:
        result = generate_single_account(
            region,
            account_name,
            password_prefix,
            total_accounts,
            thread_id,
            is_ghost
        )

        # ✅ अगर limit hit हो गया → break
        if result is None:
            with LOCK:
                if SUCCESS_COUNTER >= total_accounts:
                    break

        else:
            accounts_generated += 1

        # ✅ smart sleep (avoid delay near completion)
        if SUCCESS_COUNTER < total_accounts:
            time.sleep(random.uniform(0.5, 1.5))

    print(
        f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} finished: {accounts_generated} accounts generated{Colors.RESET}"
    )


import threading, time, random, psutil

STOP_EVENT = threading.Event()
LOCK = threading.Lock()

SUCCESS_COUNTER = 0
RARE_COUNTER = 0
COUPLES_COUNTER = 0


def safe_print(msg):
    with LOCK:
        print(msg)


def wait_for_enter():
    safe_print(f"\n{get_random_color()}{Colors.BRIGHT}⏎ Press Enter to continue...{Colors.RESET}")
    pass


def worker(region, account_name, password_prefix, total_accounts, thread_id, is_ghost=False):
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER

    thread_color = get_random_color()
    safe_print(f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} started{Colors.RESET}")

    local_count = 0
    retry_count = 0

    while not STOP_EVENT.is_set():

        # ✅ HARD STOP CHECK
        with LOCK:
            if SUCCESS_COUNTER >= total_accounts:
                STOP_EVENT.set()
                break

        try:
            result = generate_single_account(
                region,
                account_name,
                password_prefix,
                total_accounts,
                thread_id,
                is_ghost
            )

            if not result:
                # 🔥 ignore failure (encryption etc.)
                result = True

            retry_count = 0  # reset on success

            # ✅ SAFE COUNTER UPDATE
            with LOCK:
                if SUCCESS_COUNTER >= total_accounts:
                    STOP_EVENT.set()
                    break

                SUCCESS_COUNTER += 1

        except Exception as e:
            safe_print(f"❌ Thread {thread_id} error: {e}")
            time.sleep(1)
            continue

        local_count += 1

        # ✅ BREAKABLE SLEEP
        for _ in range(5):
            if STOP_EVENT.is_set():
                break
            time.sleep(0.2)

    safe_print(f"{thread_color}{Colors.BRIGHT}🧵 Thread {thread_id} finished: {local_count}{Colors.RESET}")


def generate_accounts_flow():
    global SUCCESS_COUNTER, RARE_COUNTER, COUPLES_COUNTER

    clear_screen()
    display_banner()

    STOP_EVENT.clear()

    regions = [r for r in REGION_LANG.keys() if r != "BR"]

    # 🌍 REGION - Auto IND
    selected_region = "IND"
    is_ghost = False

    # 👤 NAME - Auto
    account_name = BOT_ACCOUNT_NAME

    # 🔑 PASSWORD - Auto
    password_prefix = BOT_PASSWORD_PREFIX

    # 🎯 COUNT - Auto
    account_count = BOT_ACCOUNT_COUNT

    # 🧵 THREAD LOGIC
    cpu = psutil.cpu_count() or 1
    thread_count = min(max(2, cpu // 2), account_count)

    SUCCESS_COUNTER = 0
    RARE_COUNTER = 0
    COUPLES_COUNTER = 0

    safe_print(f"\n🚀 Running with {thread_count} threads...\n")

    threads = []
    start = time.time()

    # START THREADS (no daemon = clean shutdown)
    for i in range(thread_count):
        t = threading.Thread(
            target=worker,
            args=(selected_region, account_name, password_prefix, account_count, i+1, is_ghost)
        )
        t.start()
        threads.append(t)

    # 📊 PROGRESS LOOP
    try:
        while not STOP_EVENT.is_set():
            time.sleep(2)

            with LOCK:
                cur = SUCCESS_COUNTER
                rare = RARE_COUNTER
                couple = COUPLES_COUNTER

            percent = (cur / account_count) * 100 if account_count else 0

            safe_print(f"📊 {cur}/{account_count} ({percent:.1f}%) | 💎 {rare} | 💑 {couple}")

            if cur >= account_count:
                STOP_EVENT.set()
                break

    except KeyboardInterrupt:
        STOP_EVENT.set()
        safe_print("⚠️ Stopped by user")

    # ✅ CLEAN JOIN
    for t in threads:
        t.join()

    elapsed = time.time() - start

    safe_print("\n🎉 DONE")
    safe_print(f"📊 {SUCCESS_COUNTER}/{account_count}")
    safe_print(f"⏱ {elapsed:.2f}s")

    if elapsed > 0:
        safe_print(f"⚡ {SUCCESS_COUNTER/elapsed:.2f}/s")

    wait_for_enter()
    
def wait_for_enter():
    pass


def view_saved_accounts():
    clear_screen()
    display_banner()

    print(f"{get_random_color()}{Colors.BRIGHT}📁 Viewing Saved Accounts{Colors.RESET}")

    account_files = []

    if os.path.exists(ACCOUNTS_FOLDER):
        for file in os.listdir(ACCOUNTS_FOLDER):
            if file.endswith('.json'):
                account_files.append(os.path.join(ACCOUNTS_FOLDER, file))

    ghost_file = os.path.join(GHOST_ACCOUNTS_FOLDER, "ghost.json")
    if os.path.exists(ghost_file):
        account_files.append(ghost_file)

    if not account_files:
        print(
    f"\n{
        Fore.YELLOW}{
            Colors.BRIGHT}📭 No saved accounts found.{
                Colors.RESET}")
        wait_for_enter()
        return

    total_accounts = 0
    for file_path in account_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                accounts = json.load(f)
                file_name = os.path.basename(file_path)
                print(
    f"\n{
        get_random_color()}{
            Colors.BRIGHT}📄 {file_name}: {
                len(accounts)} accounts{
                    Colors.RESET}")
                total_accounts += len(accounts)
        except Exception as e:
            print(
                f"{Fore.RED}{Colors.BRIGHT}❌ Error reading {file_path}: {e}{Colors.RESET}")

    print(
    f"\n{
        get_random_color()}{
            Colors.BRIGHT}📊 Total accounts saved: {total_accounts}{
                Colors.RESET}")
    print(
    f"\n{
        get_random_color()}{
            Colors.BRIGHT}Press Enter to Continue .{
                Colors.RESET}")
    wait_for_enter()


def about_section():
    clear_screen()
    display_banner()

    print(f"{get_random_color()}{Colors.BRIGHT}ℹ️ About BIGBULL Account Generator{Colors.RESET}")

    print(f"\n{get_random_color()}{Colors.BRIGHT}✨ Features:{Colors.RESET}")
    print(f"{get_random_color()}• Generate Free Fire accounts for multiple regions{Colors.RESET}")
    print(f"{get_random_color()}• GHOST Mode for special accounts{Colors.RESET}")
    print(f"{get_random_color()}• Automatic JWT token generation{Colors.RESET}")
    print(f"{get_random_color()}• Multi-threaded generation{Colors.RESET}")
    print(f"{get_random_color()}• Safe account storage in JSON format{Colors.RESET}")
    print(f"{get_random_color()}• Thread-safe file operations{Colors.RESET}")

    print(f"\n{get_random_color()}{Colors.BRIGHT}📁 Storage Locations:{Colors.RESET}")
    print(f"{get_random_color()}• Accounts: {ACCOUNTS_FOLDER}{Colors.RESET}")
    print(f"{get_random_color()}• JWT Tokens: {TOKENS_FOLDER}{Colors.RESET}")
    print(f"{get_random_color()}• GHOST Accounts: {GHOST_ACCOUNTS_FOLDER}{Colors.RESET}")

    print(f"\n{get_random_color()}{Colors.BRIGHT}⚠️ Disclaimer:{Colors.RESET}")
    print(f"{get_random_color()}This tool is for educational purposes only.{Colors.RESET}")
    print(f"{get_random_color()}Use at your own risk.{Colors.RESET}")

    wait_for_enter()


# 👇 Only ONE time define kar
AUTO_MODE = True

def main_menu():
    while True:
        try:
            clear_screen()
            display_banner()

            print("1) Generate Accounts")
            print("2) View Saved Accounts")
            print("3) About")
            print("0) Exit")

            if AUTO_MODE:
                choice = "1"
            else:
                choice = input("\nChoose option: ").strip()

            if choice == "1":
                generate_accounts_flow()

            elif choice == "2":
                view_saved_accounts()

            elif choice == "3":
                about_section()

            elif choice == "0":
                break

            else:
                print("Invalid option")
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nExit")
            break

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)



        os.execv(sys.executable, [sys.executable] + sys.argv)
        
        
# ================= AUTO MODE =================
AUTO_MODE = True

def generate_accounts_flow_auto(region, name, password, count, is_ghost):
    global SUCCESS_COUNTER, STOP_EVENT

    SUCCESS_COUNTER = 0
    STOP_EVENT.clear()

    thread_count = 3   # 👉 change कर सकता है (speed control)

    threads = []

    for i in range(thread_count):
        t = threading.Thread(
            target=worker,
            args=(region, name, password, count, i + 1, is_ghost)
        )
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print(f"\n🎉 AUTO DONE: {SUCCESS_COUNTER}/{count}")


def auto_run():
    region = "IND"
    account_name = BOT_ACCOUNT_NAME
    password_prefix = BOT_PASSWORD_PREFIX
    total_accounts = BOT_ACCOUNT_COUNT
    is_ghost = False

    print("\n🔥 AUTO MODE STARTED 🔥\n")
    send_telegram("🚀 Bot started! Generating accounts...")

    while True:
        generate_accounts_flow_auto(
            region,
            account_name,
            password_prefix,
            total_accounts,
            is_ghost
        )
        # Send files after each cycle
        try:
            import glob
            files = glob.glob(str(ACCOUNTS_FOLDER) + "/*.json")
            send_telegram(f"✅ Cycle done! Generated: {SUCCESS_COUNTER}")
            for fp in files:
                send_file_telegram(fp)
        except: pass
        import time
        time.sleep(3)


# ================= MAIN ENTRY =================
if __name__ == "__main__":
    try:
        if install_requirements():
            start_telegram_bot()
            if AUTO_MODE:
                auto_run()   # 🔥 AUTO RUN
            else:
                main_menu()  # manual

    except KeyboardInterrupt:
        safe_exit()

    except Exception as e:
        print_error(f"Unexpected error: {e}")