from aiohttp.client_exceptions import ClientConnectorError
from aiohttp_requests import requests
from colorama import Fore, Style
from datetime import datetime
from time import time
import http.client
import asyncio
import sys


def coloring(text, color):
    colors = {'r': Fore.RED, 'g': Fore.GREEN, 'b': Fore.BLUE, 'c': Fore.LIGHTCYAN_EX}
    try:
        return colors[color] + text + Style.RESET_ALL
    except KeyError:
        return text


def get_ip():
    connection = http.client.HTTPConnection("ifconfig.me")
    connection.request("GET", "/ip")
    ip = str(connection.getresponse().read())[2:-1]
    return ip


async def ping(domain):
    ip = get_ip()
    while True:
        try:
            start = time()
            response = await requests.get(f'https://{domain}')
            stop = time()

            response = str(response)
            status = coloring(response[response.find('['): response.find(']') + 1], 'b')
            url = coloring('https://' + domain, 'g')
            interval = round((stop - start) * 1000)

            log = f'Response {status} from {url} to {ip} for {interval} ms'
            if len(sys.argv) >= 3 and sys.argv[2] == '-t':
                log = f'[{coloring(datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "c")}] ' + log
            print(log)

            await asyncio.sleep(1 - interval / 1000)
        except ClientConnectorError:
            sys.exit(f'{coloring("Connection failed with", "r")} {coloring(domain, "g")}')


if __name__ == '__main__':
    start = time()
    try:
        asyncio.run(ping(sys.argv[1]))
    except KeyboardInterrupt:
        print(f'\nPing stopped after {round((time() - start) * 1000)} ms')
