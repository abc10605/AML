import pathlib
import random
import threading
import time

import faker
from faker_credit_score import CreditScore


class Accounts(threading.Thread):
    def __init__(self, sql, init_acc=None):
        threading.Thread.__init__(self)
        self.__sql = sql
        self.__locale = tuple(
            map(
                lambda x: x.replace('\n', ''),
                open(
                    f'{pathlib.Path(__file__).parent.parent}/data/locale.txt',
                    'r'
                    ).readlines()
                )
            )
        self.__sdn_bool = tuple([True] + [False] * 499)
        self.__faker = faker.Faker(self.__locale)
        self.count = sql.query('SELECT count(*) FROM ACCOUNTS')[0][0]
        if init_acc is not None:
            for i in range(init_acc):
                self.__generate_account()
                print(f'\rGenerating initial accounts...{i:>{len(str(init_acc))}}/{init_acc}', end='', flush=True)
            print(f'\r\033[KGenerating initial accounts...\033[33mFinished!\033[0m', end='\n', flush=True)
        else:
            print('No initial account to generate.')

    def run(self):
        while True:
            self.__generate_account()
            time.sleep(random.random())

    def __generate_account(self):
        fk = self.__faker[random.choice(self.__locale)]
        fk.add_provider(CreditScore)
        profile = fk.simple_profile()
        acc = fk.numerify(text="##############")
        sdn = random.choice(self.__sdn_bool)
        if sdn:
            name = None
            while name is None:
                name = random.choice(
                    self.__sql.query(
                        'SELECT name FROM SDN ORDER BY RANDOM() LIMIT 1'
                    )[0][0].split('\n')
                )
        else:
            name = profile['name']
        account = (
            acc,
            name,
            fk.date_between('-50y', '-20y'),
            profile['address'],
            profile['mail'],
            fk.company(),
            fk.job(),
            self.__faker['en_US'].country(),
            fk.credit_score()
        )
        self.__sql.insert_data('ACCOUNTS', account)
        self.count += 1
        