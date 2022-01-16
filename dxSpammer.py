from aiohttp.client import ClientSession
import sys, os, asyncio, shutil, colorama, encodings.idna, time, random
from colorama import Fore
from tasksio import TaskPool
from aiohttp import client_exceptions
from sys import exit

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)

colorama.init(convert=True)

clear = lambda: os.system("cls")
if sys.platform == "linux":
    clear = lambda: os.system("clear")

class dxSpammmer():
    def __init__(self):
        self.tokens = []

        
        self.checking = False
        self.checked = []
        self.totalChecked = []



        self.proxies = []
        self.proxyless = True


        self.center = shutil.get_terminal_size().columns
        for token in open("dx-data/tokens.txt"):
            if token != '':
                self.tokens.append(
                    token.replace("\n", "").replace('\r\n',
                                                    '').replace('\r', ''))
        print(Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED + '] ' +
               Fore.GREEN + 'Proxies? [Y,N]: ' + Fore.RESET, end='')
        resp = input()
        if resp.lower() == 'y':
            for proxy in open("dx-data/proxies.txt"):
                if proxy != '':
                    split = proxy.replace("\n", "").replace('\r\n',
                                                    '').replace('\r', '').split(":")
                    if len(split) == 2:
                        self.proxies.append(f"http://{split[0]}:{split[1]}")
                    elif len(split) == 4:
                        self.proxies.append(f"http://{split[2]}:{split[3]}@{split[0]}:{split[1]}")

    async def start(self):

        clear()
        self.sendText()
        print((Fore.RED + '[' + Fore.GREEN + '1' + Fore.RED + '] ' +
               Fore.GREEN + 'Server Joiner' + Fore.RESET +
               '             ').center(self.center))
        print((Fore.RED + '[' + Fore.GREEN + '2' + Fore.RED + '] ' +
               Fore.GREEN + 'Server Leaver' + Fore.RESET +
               '             ').center(self.center))
        
        print((Fore.RED + '[' + Fore.GREEN + '3' + Fore.RED + '] ' +
               Fore.GREEN + 'Token Checker' + Fore.RESET +
               '             ').center(self.center))
        print(" ")

        async def askChoice():
            print('                                         ' + Fore.RED +
                  '[' + Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
                  '>>> ' + Fore.RESET + '',
                  end='')
            choice = input()
            if choice.__eq__('1'):
                await self.screen1()
            elif choice.__eq__('2'):
                await self.screen2()
            elif choice.__eq__('3'):
                await self.screen3()
            elif choice.__eq__('4'):
                await self.screen4()
                print('\n                                       ' + Fore.RED +
                      '[' + Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
                      "Thank you for using dx spammer")
                exit()
            else:
                print('\n                                       ' + Fore.RED +
                      '[' + Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
                      'Invalid Choice!\n')
                await askChoice()

        await askChoice()

    async def screen1(self):
        
        clear()
        self.sendText('screen1')
        print('\n                                       ' + Fore.RED + '[' +
              Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
              'Invite: ',
              end='')
        guildInv = input()
        if guildInv == '0':
            await self.start()
        print('\n                                       ' + Fore.RED + '[' +
              Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
              ' bypass rules ? [y/n]: ',
              end='')
        bypassRulesScreen = input()
        if bypassRulesScreen == '0':
            await self.start()
        if bypassRulesScreen.lower() == 'y':
            bypassRulesScreen = True
        else:
            bypassRulesScreen = False
        if 'discord.gg' in guildInv or 'discord.com' in guildInv:
            guildInv = guildInv.replace('https://discord.com/invite/',
                                        '').replace('https://discord.gg/',
                                                    '').replace(
                                                        'discord.gg/', '')

        async with TaskPool(5_000) as pool:
            for token in self.tokens:
                await pool.put(self.joinServer(token, guildInv, bypassRulesScreen))
        await asyncio.sleep(5)
        await self.start()

    async def joinServer(self, token, guildInv, bypassRuleScreen = False):
        headers = {
            "Authorization":
            token,
            "accept":
            "*/*",
            "accept-language":
            "en-US",
            "connection":
            "keep-alive",
            "cookie":
            f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT":
            "1",
            "origin":
            "https://discord.com",
            "sec-fetch-dest":
            "empty",
            "sec-fetch-mode":
            "cors",
            "sec-fetch-site":
            "same-origin",
            "referer":
            "https://discord.com/channels/@me",
            "TE":
            "Trailers",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties":
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }

        tk = token
        try:
            tk = token[:25] + "*" * 34
        except:
            tk = "*" * len(token)

        randomProxy = ''
        if self.proxyless == False:
            randomProxy = self.proxies[random.randint(0, len(self.proxies)-1)]

        async with ClientSession(headers=headers) as session:
            try:
                async with session.post("https://discord.com/api/v9/invites/%s" %
                                        (guildInv), proxy=randomProxy) as req:
                    if req.status == 429:
                        print('\n                                       ' +
                            Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                            '] ' + Fore.GREEN + f'{tk} rate limited!\n' +
                            Fore.RESET)
                    else:
                        try:
                            json = await req.json()
                            if 'message' in json:
                                if 'verify' in json['message']:
                                    print(
                                        '\n                                       ' +
                                        Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                        '] ' + Fore.GREEN +
                                        f'{tk} is unverified (mostly flagged)!\n'
                                        + Fore.RESET)
                                    if token in self.tokens:
                                        self.tokens.remove(token)
                                elif 'Unauthorized' in json['message']:
                                    print(
                                        '\n                                       ' +
                                        Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                        '] ' + Fore.GREEN +
                                        f'{tk} is not a real token idiot\n'
                                        + Fore.RESET)
                                    if token in self.tokens:
                                        self.tokens.remove(token)
                                elif 'banned' in json['message']:
                                    print('\n                                       ' +
                                        Fore.RED + '[' + Fore.GREEN + '/' +
                                        Fore.RED + '] ' + Fore.GREEN +
                                        f'{tk} is banned\n' +
                                        Fore.RESET)

                                else:
                                    print('\n                                       ' +
                                        Fore.RED + '[' + Fore.GREEN + '/' +
                                        Fore.RED + '] ' + Fore.GREEN +
                                        f'{tk} failed to join (mostly banned from server)\n' +
                                        Fore.RESET)
                            else:
                                json = await req.json()
                                print('\n                                       ' +
                                    Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                    '] ' + Fore.GREEN + f'{tk} joined \n' +
                                    Fore.RESET)
                                if bypassRuleScreen == True:
                                    async with session.get("https://discord.com/api/v9/guilds/"+json['guild']['id']+"/member-verification?with_guild=false&invite_code=" + guildInv) as req2:
                                        if req2.status == 200:
                                            j = await req2.json()
                                            async with session.put("https://discord.com/api/v9/guilds/"+json['guild']['id']+"/requests/@me", json=j) as req3:
                                                if req3.status == 201:
                                                    print('\n                                       ' +
                                                        Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                                        '] ' + Fore.GREEN + f'{tk} bypassed rules \n' +
                                                        Fore.RESET)
                                                else:
                                                    print('\n                                       ' +
                                                        Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                                        '] ' + Fore.GREEN + f'{tk} failed to bypass\n' +
                                                        Fore.RESET)
                                        else:
                                            print('\n                                       ' +
                                                Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                                '] ' + Fore.GREEN + f'{tk} failed to bypass \n' +
                                                Fore.RESET)
                        except client_exceptions.ContentTypeError:
                            pass
            except client_exceptions.ClientHttpProxyError:
                print('\n                                       ' +
                    Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                    '] ' + Fore.GREEN + f'{tk} failed to join the server, Proxy Error!\n' +
                    Fore.RESET)
                pass
            except client_exceptions.ClientConnectorError:
                print('\n                                       ' +
                    Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                    '] ' + Fore.GREEN + f'{tk} , err to connect to discord\n' +
                    Fore.RESET)
                pass

    async def screen2(self):

        clear()
        self.sendText('screen2')
        print('\n                                       ' + Fore.RED + '[' +
              Fore.GREEN + '/' + Fore.RED + '] ' + Fore.GREEN +
              'Server id: ',
              end='')
        guildId = input()
        if guildId == '0':
            await self.start()
      
        async with TaskPool(5_000) as pool:
            for token in self.tokens:
                await pool.put(self.leaveServer(token, guildId))
        await asyncio.sleep(5)
        await self.start()

    async def leaveServer(self, token, guildId):
        headers = {
            "Authorization":
            token,
            "accept":
            "*/*",
            "accept-language":
            "en-US",
            "connection":
            "keep-alive",
            "cookie":
            f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT":
            "1",
            "origin":
            "https://discord.com",
            "sec-fetch-dest":
            "empty",
            "sec-fetch-mode":
            "cors",
            "sec-fetch-site":
            "same-origin",
            "referer":
            "https://discord.com/channels/@me",
            "TE":
            "Trailers",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties":
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }

        tk = token
        try:
            tk = token[:25] + "*" * 34
        except:
            tk = "*" * len(token)

        randomProxy = ''
        if self.proxyless == False:
            randomProxy = self.proxies[random.randint(0, len(self.proxies)-1)]

        async with ClientSession(headers=headers) as session:
            async with session.delete(
                    "https://discord.com/api/v9/users/@me/guilds/%s" %
                (guildId), proxy=randomProxy) as req:
                if req.status == 429:
                    print('\n                                       ' +
                          Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                          '] ' + Fore.GREEN + f'{tk}  rate limited\n' +
                          Fore.RESET)
                elif req.status == 204:
                    print('\n                                       ' +
                          Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                          '] ' + Fore.GREEN + f'{tk} left the\n' +
                          Fore.RESET)
                else:
                    json = await req.json()
                    if 'message' in json:
                        if 'verify' in json['message']:
                            print(
                                '\n                                       ' +
                                Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                '] ' + Fore.GREEN +
                                f'{tk} is unverified (mostly flagged)\n'
                                + Fore.RESET)
                            if token in self.tokens:
                                self.tokens.remove(token)
                        elif 'Unauthorized' in json['message']:
                            print(
                                '\n                                       ' +
                                Fore.RED + '[' + Fore.GREEN + '/' + Fore.RED +
                                '] ' + Fore.GREEN +
                                f'{tk} is not a real token\n'
                                + Fore.RESET)
                            if token in self.tokens:
                                self.tokens.remove(token)
                        elif 'Unknown Guild' in json['message']:
                            pass
                        else:
                            print('\n                                       ' +
                                  Fore.RED + '[' + Fore.GREEN + '/' +
                                  Fore.RED + '] ' + Fore.GREEN +
                                  f'{tk} failed to leave \n' +
                                  Fore.RESET)

    
    async def screen3(self):

        clear()
        self.sendText('screen3')
        print(
            '                                       '
            + Fore.RED + '[' + Fore.GREEN + '/' +
            Fore.RED + '] ' + Fore.GREEN +
            f'Checking Tokens...' +
            Fore.RESET)

        async with TaskPool(5_000) as pool:
            for token in self.tokens:
                await pool.put(self.tokenChecker(token))
        while self.checked == False:
            pass
        else:
            print(
                '                                       '
                + Fore.RED + '[' + Fore.GREEN + '/' +
                Fore.RED + '] ' + Fore.GREEN +
                f'Checked tokens. Valid = {len(self.checked)} ~ Total = {len(self.totalChecked)}' +
                Fore.RESET)
            print(
                '                                       '
                + Fore.RED + '[' + Fore.GREEN + '/' +
                Fore.RED + '] ' + Fore.GREEN +
                f'Do you want to save them in separate file? [Y/N]: ' +
                Fore.RESET, end='')
            resp = input()
            if resp.lower() == 'y':
                added = 0
                with open('dx-data/checked.txt', 'w') as f:
                    for t in self.checked:
                        f.write(t + '\n')
                        added += 1
                while added != len(self.checked):
                    pass
                else:
                    print(
                        '                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'Saved new tokens in dx-data/checked.txt.' +
                        Fore.RESET)
                    print(
                        '                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'Do you want to go back? [Y/N]: ' +
                        Fore.RESET, end='')
                    r = input()
                    if r.lower() == 'y':
                        self.checked = []
                        self.totalChecked = []
                        await self.start()
                    else:
                        self.exit()
            else:
                added = 0
                open('dx-data/tokens.txt', 'w').close()
                with open('dx-data/tokens.txt', 'w') as f:
                    for t in self.checked:
                        f.write(t + '\n')
                        added += 1
                while added != len(self.checked):
                    pass
                else:
                    print(
                        '                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'Replaced with new tokens in tokens.txt.' +
                        Fore.RESET)
                    print(
                        '                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'go back? [Y/N]: ' +
                        Fore.RESET, end='')
                    r = input()
                    if r.lower() == 'y':
                        self.checked = []
                        self.totalChecked = []
                        await self.start()
                    else:
                        self.exit()
        
    async def tokenChecker(self, token):
        headers = {
            "Authorization":
            token,
            "accept":
            "*/*",
            "accept-language":
            "en-US",
            "connection":
            "keep-alive",
            "cookie":
            f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US',
            "DNT":
            "1",
            "origin":
            "https://discord.com",
            "sec-fetch-dest":
            "empty",
            "sec-fetch-mode":
            "cors",
            "sec-fetch-site":
            "same-origin",
            "referer":
            "https://discord.com/channels/@me",
            "TE":
            "Trailers",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties":
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        tk = token
        try:
            tk = token[:25] + "*" * 34
        except:
            tk = "*" * len(token)

        randomProxy = ''
        if self.proxyless == False:
            randomProxy = self.proxies[random.randint(0, len(self.proxies)-1)]

        self.totalChecked.append(token)
        async with ClientSession(headers=headers) as session:
            async with session.get(
                    "https://discord.com/api/v9/users/@me/library", proxy=randomProxy) as r:
                
                if r.status == 200:
                    print(
                        '\n                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'{tk} is valid!\n' +
                        Fore.RESET)
                    self.checked.append(token)
                elif r.status == 400:
                    print(
                        '\n                                       '
                        + Fore.RED + '[' + Fore.GREEN + '/' +
                        Fore.RED + '] ' + Fore.GREEN +
                        f'{tk} couldn\'t check!\n' +
                        Fore.RESET)
                else:
                    text = await r.text()
                    if "You need to verify your account" in text:
                        print(
                            '\n                                       '
                            + Fore.RED + '[' + Fore.GREEN + '/' +
                            Fore.RED + '] ' + Fore.GREEN +
                            f'{tk} is locked and removed from list!\n'
                            + Fore.RESET)
                        if token in self.tokens:
                            self.tokens.remove(token)
                    elif "Unauthorized" in text:
                        print(
                            '\n                                       '
                            + Fore.RED + '[' + Fore.GREEN + '/' +
                            Fore.RED + '] ' + Fore.GREEN +
                            f'{tk} is invalid and removed from list!\n'
                            + Fore.RESET)
                        if token in self.tokens:
                            self.tokens.remove(token)
                    else:
                        print(
                            '\n                                       '
                            + Fore.RED + '[' + Fore.GREEN + '/' +
                            Fore.RED + '] ' + Fore.GREEN +
                            f'{tk} failed to check!\n' +
                            Fore.RESET)


    os.system ('title Token Spammer by dx#1234')
    def sendText(self, screen='main'):
        print(Fore.GREEN, end='')
        print(f'''
░█▀▄░█░█░░░█▀▀░▄▀▀▄░█▀▀▄░█▀▄▀█░█▀▄▀█░█▀▀░█▀▀▄
░█░█░▄▀▄░░░▀▀▄░█▄▄█░█▄▄█░█░▀░█░█░▀░█░█▀▀░█▄▄▀
░▀▀░░▀░▀░░░▀▀▀░█░░░░▀░░▀░▀░░▒▀░▀░░▒▀░▀▀▀░▀░▀▀

                          

                                                         ''')
auth = dxSpammmer()
loop = asyncio.get_event_loop()
loop.run_until_complete(auth.start())
