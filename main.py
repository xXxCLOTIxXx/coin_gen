import asyncio
import random
import time
import os
from threading import Thread

try:
    from aminofix import asyncfix, exceptions
    from colorama import Fore
    from flask import Flask
except ModuleNotFoundError:
    os.system('pip install amino.fix colorama flask')
    from aminofix import asyncfix, exceptions
    from colorama import Fore
    from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def fuck():
    return 'farm_system'


def generate_tz():
    localhour = time.strftime("%H", time.gmtime())
    localminute = time.strftime("%M", time.gmtime())
    UTC = {"GMT0": '+0', "GMT1": '+60', "GMT2": '+120', "GMT3": '+180', "GMT4": '+240', "GMT5": '+300', "GMT6": '+360',
           "GMT7": '+420', "GMT8": '+480', "GMT9": '+540', "GMT10": '+600', "GMT11": '+660', "GMT12": '+720',
           "GMT13": '+780', "GMT-1": '-60', "GMT-2": '-120', "GMT-3": '-180', "GMT-4": '-240', "GMT-5": '-300',
           "GMT-6": '-360', "GMT-7": '-420', "GMT-8": '-480', "GMT-9": '-540', "GMT-10": '-600', "GMT-11": '-660'};
    hour = [localhour, localminute]
    if hour[0] == "00": tz = UTC["GMT-1"];return int(tz)
    if hour[0] == "01": tz = UTC["GMT-2"];return int(tz)
    if hour[0] == "02": tz = UTC["GMT-3"];return int(tz)
    if hour[0] == "03": tz = UTC["GMT-4"];return int(tz)
    if hour[0] == "04": tz = UTC["GMT-5"];return int(tz)
    if hour[0] == "05": tz = UTC["GMT-6"];return int(tz)
    if hour[0] == "06": tz = UTC["GMT-7"];return int(tz)
    if hour[0] == "07": tz = UTC["GMT-8"];return int(tz)
    if hour[0] == "08": tz = UTC["GMT-9"];return int(tz)
    if hour[0] == "09": tz = UTC["GMT-10"];return int(tz)
    if hour[0] == "10": tz = UTC["GMT13"];return int(tz)
    if hour[0] == "11": tz = UTC["GMT12"];return int(tz)
    if hour[0] == "12": tz = UTC["GMT11"];return int(tz)
    if hour[0] == "13": tz = UTC["GMT10"];return int(tz)
    if hour[0] == "14": tz = UTC["GMT9"];return int(tz)
    if hour[0] == "15": tz = UTC["GMT8"];return int(tz)
    if hour[0] == "16": tz = UTC["GMT7"];return int(tz)
    if hour[0] == "17": tz = UTC["GMT6"];return int(tz)
    if hour[0] == "18": tz = UTC["GMT5"];return int(tz)
    if hour[0] == "19": tz = UTC["GMT4"];return int(tz)
    if hour[0] == "20": tz = UTC["GMT3"];return int(tz)
    if hour[0] == "21": tz = UTC["GMT2"];return int(tz)
    if hour[0] == "22": tz = UTC["GMT1"];return int(tz)
    if hour[0] == "23": tz = UTC["GMT0"];return int(tz)


def generate_timers():
    return [{'start': int(time.time()), 'end': int(time.time()) + 300} for _ in range(50)]


async def main():
    try:
        accounts = open('accounts.txt').read().split('\n')
        random.shuffle(accounts)
    except FileNotFoundError:
        print(
            f'{Fore.LIGHTYELLOW_EX}> {Fore.RESET}СОЗДАЙТЕ ФАЙЛ С {Fore.LIGHTYELLOW_EX} АККАУНТАМИ {Fore.RESET} С ИМЕНЕМ {Fore.LIGHTYELLOW_EX}"accounts.txt"{Fore.RESET}.')
        return
    comId, objectId = None, None
    try:
        link = open('link.txt').read()
    except FileNotFoundError:
        link = input(
            f'{Fore.LIGHTYELLOW_EX}> {Fore.RESET} ВВЕДИТЕ {Fore.LIGHTYELLOW_EX} ССЫЛКУ {Fore.RESET}: ')
        open('link.txt', 'w').write(link)
        print()
    while True:
        try:
            this_account = accounts[0]
            accounts.remove(this_account)
            accounts.append(this_account)
            email, password, device_id = this_account.split()
            client = asyncfix.Client(deviceId=device_id)
            await client.login(email, password)
            print(
                f'{Fore.LIGHTYELLOW_EX}> {Fore.RESET}ЗАЛОГИНИЛИ {Fore.LIGHTYELLOW_EX}{email.upper()}{Fore.RESET}.')
            if not objectId or not comId:
                link_info = await client.get_from_code(link)
                comId, objectId = link_info.comIdPost, link_info.objectId
            await client.join_community(comId=comId)
            sub_client = asyncfix.SubClient(comId=comId, profile=client.profile)
            try:
                for _ in range(1, 25):
                    await sub_client.send_active_obj(timers=generate_timers(), tz=generate_tz())
                    print(
                        f'{Fore.LIGHTYELLOW_EX}> {Fore.RESET}ОТПРАВЛЕН {Fore.LIGHTYELLOW_EX}ACTIVE-OBJ {Fore.RESET}- {Fore.LIGHTYELLOW_EX}[{Fore.RESET}{_}{Fore.LIGHTYELLOW_EX} ИЗ {Fore.RESET}24{Fore.LIGHTYELLOW_EX}]{Fore.RESET}.')
                    time.sleep(2.5)
            except exceptions.AccountLimitReached or exceptions.TooManyRequests:
                pass
            coins = (await client.get_wallet_info()).totalCoins
            if coins > 500:
                for _ in range(coins // 500):
                    await sub_client.send_coins(coins=500, blogId=objectId)
            if coins:
                await sub_client.send_coins(coins=coins % 500, blogId=objectId)
            print(
                f'{Fore.LIGHTYELLOW_EX}> {Fore.RESET}ОТПРАВЛЕНО {Fore.LIGHTYELLOW_EX}{coins} МОНЕТ{Fore.RESET}.')
        except exceptions.AccountLimitReached or exceptions.TooManyRequests:
            print(f'{Fore.LIGHTRED_EX}> {Fore.RESET}СЛИШКОМ МНОГО ЗАПРОСОВ {Fore.RED}{email.upper()}{Fore.RESET}.')
            continue
        except exceptions.AccountDisabled:
            print(f'{Fore.LIGHTRED_EX}> {Fore.RESET}ЗАБАНИЛИ АКК {Fore.RED}{email.upper()}{Fore.RESET}.')
            continue
        except exceptions.CommunityLimit:
            print(f'{Fore.LIGHTRED_EX}> {Fore.RESET}СЛИШКОМ МНОГО СОО {Fore.RED}{email.upper()}{Fore.RESET}.')
            for elem in (await client.sub_clients()).comId:
                try:
                    await client.leave_community(elem)
                except:
                    pass
        except exceptions.ActionNotAllowed:
            print(f'{Fore.LIGHTRED_EX}> {Fore.RESET}ЗАБАНИЛИ АКК {Fore.RED}{email.upper()}{Fore.RESET}.')
            continue
        except exceptions.IpTemporaryBan:
            print(f'{Fore.LIGHTRED_EX}> {Fore.RESET}ЗАБАНИЛИ ПО {Fore.RED}АЙПИ{Fore.RESET}.')
            time.sleep(360)
            continue


if __name__ == '__main__':
    Thread(target=app.run).start()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
