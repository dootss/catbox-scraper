import os
import sys
import yaml
import time
import random
import string
import asyncio
import aiohttp
import aiofiles
import threading


CONFIG_FILE = 'config.yaml'
URL = 'https://files.catbox.moe/'
os.system('')
sys.stdout.write('\033[?25l')


with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.safe_load(config_file)

file_extensions = config['file_extensions']
threads = config['threads']
update_rate = config['update_rate']

urls_scanned = 0
valid_found = 0
start_time = time.time()
status_board_running = True

print_lock = asyncio.Semaphore()
file_lock = asyncio.Lock()


def clear_screen():
    if sys.platform == 'linux' or sys.platform == 'linux2':
        os.system('clear')
    elif sys.platform == 'win32':
        os.system('cls')

def random_string(length=6):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def format_elapsed_time(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

async def download_image(session, url, folder_name, random_filename):
    async with session.get(url) as image_data:
        if image_data.status == 200:
            content = await image_data.read()
            if content:
                async with aiofiles.open(os.path.join(folder_name, random_filename), mode='wb') as f:
                    await f.write(content)

async def save_valid_url(folder_name, url):
    os.makedirs(folder_name, exist_ok=True)
    async with aiofiles.open(f"{folder_name}/valids.txt", "a") as file:
        await file.write(url + "\n")

def status_board():
    global urls_scanned, valid_found, start_time, status_board_running


    while status_board_running:
        if urls_scanned > 0:
            elapsed_time = time.time() - start_time
            formatted_elapsed_time = format_elapsed_time(elapsed_time)


            sys.stdout.write('\033[5;1H[-----------------------]\n')
            sys.stdout.write(f'\033[7;1H TIME ELAPSED : {formatted_elapsed_time}\n')
            sys.stdout.write(f'\033[8;1H CHECKS       : {urls_scanned:,}\n')
            sys.stdout.write(f'\033[9;1H HITS         : {valid_found:,}\n')
            sys.stdout.write(f'\033[6;1H PER SECOND   : {int(urls_scanned / elapsed_time):,}\n')
            sys.stdout.write('\033[10;1H[-----------------------]\n')
            sys.stdout.flush()
        time.sleep(update_rate)

async def check_url(_):
    global urls_scanned, valid_found
    async with aiohttp.ClientSession() as session:
        while True:
            for ext in file_extensions:
                filename = random_string() + ext
                random_url = URL + filename
                try:
                    async with session.get(random_url, timeout=5) as response:
                        urls_scanned += 1

                        if response.status == 200:
                            valid_found += 1
                            os.makedirs(ext.strip('.'), exist_ok=True)
                            await download_image(session, random_url, ext.strip('.'), filename)
                            await save_valid_url(ext.strip('.'), random_url)

                except asyncio.exceptions.TimeoutError:
                    continue
                except ConnectionResetError:
                    continue
                except aiohttp.ClientConnectorError:
                    continue
                except Exception as e:
                    print(f"Exception {type(e).__name__}: {e}")


if __name__ == "__main__":
    clear_screen()
    print(" CATBOX SCRAPER")
    print("[==============]")
    print("    BY DOOT\n")
    print(' STARTING...')
    threading.Thread(target=status_board, daemon=True).start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [check_url(i) for i in range(threads)]
    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        status_board_running = False
        sys.exit("Stopped!")
