import base64
import datetime
import pickle
import random
import re
import shutil
import ssl
import string
import traceback

import capmonster_python
import cloudscraper
import requests
import warnings

import ua_generator

from utils.logger import logger
from utils.Check_mail import *

warnings.filterwarnings("ignore", category=DeprecationWarning)



class SpaceNation:

    def __init__(self, email, ePassword, proxy, private, address, twitter_auth, twitter_ct0,capKey, refCode = None, logger=None):
        self.logger = logger
        self.access_token = None
        self.refresh_token = None
        self.password_ = None
        self.refCode = refCode

        self.ua = self.generate_user_agent

        self.twitter_auth, self.twitter_ct0 = twitter_auth, twitter_ct0
        self.twitterHeaders = {'cookie': f'auth_token={self.twitter_auth}; ct0={self.twitter_ct0}',
                               'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                               'content-type': 'application/x-www-form-urlencoded',
                               'X-Csrf-Token': self.twitter_ct0,
                               'user-agent': self.ua
                               }

        self.private, self.address = private, address
        self.email, self.password, self.capKey = email, ePassword, capKey
        self.session = self._make_scraper
        self.proxy = proxy
        self.session.proxies = {"http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"user-agent": self.ua,
                                     'content-type': 'application/json'})

    def Registration(self):

        self.session.get('https://spacenation.online/share/DhHjOynq')

        payload = {"path":"/mfa/code/email",
                   "method":"POST",
                   "data":
                       {
                           "captcha":self.SolveCaptcha,
                           "email":self.email,
                           "type":"register"
                       }
                   }

        # print('Капча решена')

        with self.session.post(
                'https://spacenation.online/api/service',
                json=payload) as response:
            # print(response.text)
            ...

        code = check_mail(self.email, self.password, "noreply@spacenation.online")
        self.password_ = self.generate_password

        if code == None:
            return False
        # print(code)

        payload = {"path":"/account/create",
                   "method":"POST",
                   "data":
                       {
                           "birthday":f'\"{random.randint(1970,2006)}-0{random.randint(1,9)}-{random.randint(10,28)}T22:00:00.000Z\"',
                           "email":self.email,
                           "password":self.password_,
                           "repassword":self.password_,
                           "username":self.usernameGenerator,
                           "verifyCode": code,
                           "state":None,
                           "invitationCode":self.refCode,
                           "allowPush":False
                       }
                   }
        self.session.headers.update({'Referer': f'https://spacenation.online/login?type=register&code={self.refCode}'})

        # print(payload)
        #
        # print(self.email, self.password_)

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            # print(response.text)
            pass

        return True


    def Login(self, password=None):

        payload = {"path":"auth/login",
                   "method":"POST",
                   "data":
                       {
                           "email":self.email,
                           "password":self.password_ if password == None else password,
                           "state":None
                       }
                   }

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            self.access_token = response.json()['data']['access_token']
            self.refresh_token = response.json()['data']['refresh_token']
            self.expires_in = response.json()['data']['expires_in']
            self.uid = response.json()['data']['uid']

            # print(self.access_token,
            #       self.refresh_token)


        payload = {"uid":self.uid,
                   "token":
                       {
                           "access_token":self.access_token,
                           "expires_time":int(datetime.datetime.utcnow().timestamp())+self.expires_in,
                           "refresh_token":self.refresh_token
                       },"keep":False}

        with self.session.post("https://spacenation.online/api/session", json=payload) as response:

            # print(response.text)
            ...




        # payload = {"path": "/logistikos/quest/assets/validate", "method": "POST", "data": {"questId": "1002"}}
        #
        # with self.session.post("https://spacenation.online/api/service", json=payload) as response:
        #     print(response.text)



    def WalletConnect(self):

        payload = {"path":"wallet/connect",
                   "method":"POST",
                   "data":
                       {
                           "address":self.address
                       }
                   }

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            # print(response.text)
            ...
    @property
    def Reward_1001(self)->bool:

        payload = {"path":"/logistikos/quest/reward","method":"POST","data":{"questId":"1001"}}

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            if response.json()['err'] == "":
                return True
            else:
                return False

    def TwitterRewards(self):

        rewards = ["1002","1003","1047","1048","1004","1005", "1006","1007","1008","1009"]
        for reward in rewards:

            payload = {"path": "/logistikos/quest/assets/validate", "method": "POST", "data": {"questId": f"{reward}"}}

            with self.session.post("https://spacenation.online/api/service", json=payload) as response:
                # print(response.text)
                if response.json()['data']['pass'] == True or reward == "1003":

                    if reward == "1003":
                        self.session.get(response.json()['data']['redirectUrl'])
                        time.sleep(6)

                    ...
                else:

                    break

            payload = {"path": "/logistikos/quest/reward", "method": "POST", "data": {"questId": f"{reward}"}}

            with self.session.post("https://spacenation.online/api/service", json=payload) as response:
                if response.json()['err'] == "":
                    self.logger.success(f"{self.email} | Задание {reward} - выполнено")

            time.sleep(random.randint(delayQuests[0], delayQuests[1]))

    @property
    def GetRefCode(self)->str:

        payload = {"path":"/logistikos/invitations/code/apply","method":"POST","data":{}}

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            return response.json()['data']['code']

    def TwitterConnect(self):

        payload = {"path":"/logistikos/quest/assets/validate","method":"POST","data":{"questId":"1002"}}


        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            # print(response.text)
            ...

        payload = {"path": "oauth/twitter", "method": "GET", "data": None}

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            self.notifyUrl = response.json()['data']['notifyUrl']
            link = response.json()['data']['openUrl']

        with self.session.get(link, headers=self.twitterHeaders, allow_redirects=False) as response:
            link = response.headers['Location']

            with self.session.get(link.replace('https://twitter.com/i/oauth2/authorize?', 'https://twitter.com/i/api/2/oauth2/authorize?'), headers=self.twitterHeaders) as response:
                auth_code = response.json()['auth_code']

                payload = {'approval': 'true',
                           'code': auth_code}

                response = self.session.post(f'https://twitter.com/i/api/2/oauth2/authorize', data=payload, headers=self.twitterHeaders)

                with self.session.get(response.json()['redirect_uri']) as response:
                    # print(response.text)
                    ...



                payload = {"path":"/account/connect","method":"POST","data":{"state":self.notifyUrl.split("/")[-1]}}

                with self.session.post("https://spacenation.online/api/service", json=payload) as response:
                    # print(response.text)
                    ...

    @property
    def CheckTwitterConnection(self)->bool:

        payload = {"path":self.notifyUrl,"method":"GET","data":None}

        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            # print(response.text)
            if response.json()['err'] != 'WaitCallback':
                return True
            else:
                return False

    @property
    def GetLevelInfo(self)->[int, int]:

        payload = {"path":"/logistikos/level/info","method":"GET","data":None}
        '4200000000000000000'
        with self.session.post("https://spacenation.online/api/service", json=payload) as response:
            return response.json()['data']['level'], int(response.json()['data']['token'])/1000000000000000000

    @property
    def usernameGenerator(self)->str:
        # Расширенные списки слов для генерации никнейма
        adjectives = [
            "Furious", "Savage", "Wicked", "Lethal", "Ruthless",
            "Stealthy", "Swift", "Brave", "Mighty", "Epic",
            "Legendary", "Cosmic", "Galactic", "Mystic", "Ethereal"
        ]
        nouns = [
            "Dragon", "Ninja", "Ghost", "Slayer", "Hunter",
            "Phoenix", "Titan", "Valkyrie", "Sorcerer", "Warrior",
            "Goblin", "Wizard", "Ranger", "Cleric", "Paladin"
        ]

        # Случайный выбор элементов из каждого списка
        adj = random.choice(adjectives)
        noun = random.choice(nouns)

        # С маленькой вероятностью обрезаем слова
        if random.random() < 0.2:
            adj = adj[:random.randint(3, len(adj))]
        if random.random() < 0.2:
            noun = noun[:random.randint(3, len(noun))]

        # Комбинирование выбранных элементов для создания никнейма
        nickname = f"{adj}{noun}"

        self.username = nickname
        return nickname

    @property
    def generate_password(self):
        # Определение наборов символов для пароля
        letters = string.ascii_letters  # Английские буквы в обоих регистрах
        digits = string.digits  # Цифры
        special_chars = string.punctuation  # Специальные символы

        # Количество символов в пароле (случайным образом выбираем от 8 до 16)
        password_length = random.randint(8, 16)

        # Гарантированно включаем минимум по одному символу из каждого набора
        password = random.choice(letters.upper())  # 1 символ верхнего регистра
        password += random.choice(letters.lower())  # 1 символ нижнего регистра
        password += random.choice(digits)  # 1 цифра
        # password += random.choice(special_chars)  # 1 специальный символ

        # Генерируем остальные символы пароля
        for _ in range(password_length - 3):
            password += random.choice(letters + digits)

        # Перемешиваем символы пароля, чтобы обеспечить случайность
        password_list = list(password)
        random.shuffle(password_list)
        password = random.choice(letters.upper()) + ''.join(password_list)

        return password

    @property
    def SolveCaptcha(self):
        self.cap = capmonster_python.HCaptchaTask(self.capKey)
        tt = self.cap.create_task("https://spacenation.online", "abd29162-551c-4a01-87d5-b0740438977c")
        # print(f"Created Captcha Task {tt}")
        captcha = self.cap.join_task_result(tt)
        # print(captcha)
        captcha = captcha["gRecaptchaResponse"]
        return captcha

    @property
    def CheckAccount(self):
        payload = {"email": self.email,
                   "password": self.password,
                   "returnSecureToken": True}
        # print(1)
        with self.session.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyABU16fMP_LH45JHdtXM_N-wDtxuSgBkmE', json=payload) as response:
            return response.json()

    @property
    def generate_username(self) -> str:

        array = []
        with open('InputData/genereg_nicks.txt', 'r') as file:
            for i in file:
                array.append(i.rstrip())

        return random.choice(array)

    @property
    def generate_special_XClientVersion(self) -> str:
        platform = "iOS"
        sdk_version = "FirebaseSDK/10.7.0"
        library = "FirebaseCore-iOS"

        version = ".".join(str(random.randint(0, 9)) for _ in range(3))
        return f"{platform}/{sdk_version}/{version}/{library}"

    @property
    def generate_firebase_gmpid(self) -> str:
        random_hex = "".join(random.choice("0123456789abcdef") for _ in range(24))
        return f"1:451272859150:ios:{random_hex}"

    @property
    def generate_user_agent(self) -> str:
        return ua_generator.generate(platform="windows").text

    @property
    def _make_scraper(self):
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


def Thread_(list_):

    mainRefCode = refCode
    if mainRefCode == '':
        mainRefCode = None

    localRefCode = None
    startRefCount=0
    randomRefCount = None

    count = 0
    while count < len(list_):

        try:

            if localRefCode == None:
                randomRefCount = random.randint(refCount[0], refCount[1])
                startRefCount = 0

            email = list_[count][0][0]
            logger.success(f'{email} | Регистрация началась')

            acc = SpaceNation(email=list_[count][0][0],
                              ePassword=list_[count][0][1],
                              proxy=list_[count][1],
                              address=list_[count][2],
                              private=list_[count][3],
                              twitter_auth=list_[count][4][0],
                              twitter_ct0=list_[count][4][1],
                              capKey=capmonsterKey,
                              refCode=mainRefCode if localRefCode == None else localRefCode,
                              logger=logger)

            stat = acc.Registration()
            if stat == False:
                logger.error(f'{email} | Ошибка с почтой')
                continue

            logger.success(f'{email} | Регистрация успешно произведена')

            acc.Login()
            logger.success(f'{email} | Логинизация успешно произведена')

            acc.WalletConnect()
            logger.success(f'{email} | Кошелек успешно подключен')

            acc.Reward_1001
            logger.success(f'{email} | Задание 1001 выполнено')

            acc.TwitterConnect()
            dd = 0
            while not acc.CheckTwitterConnection and dd < 10:
                time.sleep(5)
                dd+=1

            if dd >= 10:
                logger.error(f'{email} | Не удалось подключить твиттер')

                time.sleep(random.randint(delayAccs[0], delayAccs[1]))
                logger.debug('')

                # input()
                count += 1

            acc.TwitterRewards()
            logger.success(f'{email} | Задания с твиттером выполнены')

            lvl, tokens = acc.GetLevelInfo
            logger.success(f'{email} | Работа с аккаунтом закончена, lvl: {lvl} | токенов: {tokens}')

            if localRefCode == None:
                localRefCode = acc.GetRefCode
                logger.success(f'Зарегистрирован рефовод. Код - {localRefCode}')
            else:

                startRefCount+=1
                logger.success(f'Реферал {startRefCount}/{randomRefCount} зарегистрирован')

            if startRefCount == randomRefCount:
                localRefCode = None

            with open('results.txt', 'a+') as file:
                file.write('{}|{}|{}|{}|{}\n'.format(acc.email, acc.password, acc.username, acc.password_, acc.proxy))


        except Exception as e:

            # traceback.print_exc()
            logger.error(f'{email} | Ошибка - {str(e)}')

        time.sleep(random.randint(delayAccs[0], delayAccs[1]))
        logger.debug('')

        # input()
        count += 1


def generate_random_lists(L, n, k):
    result_lists = []

    while len(L) >= k:
        sublist_length = random.randint(n, k)
        sublist = L[:sublist_length]
        result_lists.append(sublist)
        L = L[sublist_length:]

    if len(L) >= n:
        sublist_length = random.randint(n, len(L))
        sublist = L[:sublist_length]
        result_lists.append(sublist)

    return result_lists

if __name__ == '__main__':

    proxies = []
    emails = []
    addresses = []
    privates = []
    twitterData = []

    refCount = ''
    capmonsterKey = ''
    refCode = None
    delayAccs = (10, 30)
    delayQuests = (10, 15)

    try:
        with open('config', 'r', encoding='utf-8') as file:
            for i in file:
                if 'capmonsterKey=' in i.rstrip():
                    capmonsterKey = str(i.rstrip().split('capmonsterKey=')[-1].split('-')[0])
                if 'refCount=' in i.rstrip():
                    refCount = (int(i.rstrip().split('refCount=')[-1].split('-')[0]), int(i.rstrip().split('refCount=')[-1].split('-')[1]))
                if 'refCode=' in i.rstrip():
                    refCode = str(i.rstrip().split('refCode=')[-1].split('-')[0])
                if 'delayAccs=' in i.rstrip():
                    delayAccs = (int(i.rstrip().split('delayAccs=')[-1].split('-')[0]),
                                int(i.rstrip().split('delayAccs=')[-1].split('-')[1]))
                if 'delayQuests=' in i.rstrip():
                    delayQuests = (int(i.rstrip().split('delayQuests=')[-1].split('-')[0]),
                                int(i.rstrip().split('delayQuests=')[-1].split('-')[1]))

    except:
        # traceback.print_exc()
        print('Вы неправильно настроили конфигуратор, повторите попытку')
        input()
        exit(0)


    with open('InputData/Emails.txt', 'r') as file:
        for i in file:
            emails.append([i.rstrip().split(':')[0], i.rstrip().split(':')[1]])
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())
    with open('InputData/Addresses.txt', 'r') as file:
        for i in file:
            addresses.append(i.rstrip())
    with open('InputData/Privates.txt', 'r') as file:
        for i in file:
            privates.append(i.rstrip())
    with open('InputData/TwitterCookies.txt', 'r') as file:
        for i in file:
            twitterData.append([i.rstrip().split('auth_token=')[-1].split(';')[0], i.rstrip().split('ct0=')[-1].split(';')[0]])

    resultList = []
    for i in range(len(proxies)):
        resultList.append([emails[i], proxies[i], addresses[i], privates[i], twitterData[i]])

    result = generate_random_lists(resultList, refCount[0], refCount[1])

    for i in result:
        Thread_(i)

    input('Скрипт завершил работу...')


