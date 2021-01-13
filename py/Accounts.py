import pathlib
import random
import threading
import time

import faker
from faker_credit_score import CreditScore


class Accounts(threading.Thread):
    def __init__(self, sql, init_acc=50):
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
        self.count = sql.query('SELECT count(*) FROM ACCOUNTS')[0][0]
        print('\n')
        for i in range(init_acc):
            self.__generate_account(random.choice(self.__locale))
            print(f'\rGenerating initial accounts.....{i}/50', end='', flush=True)
        print(f'\rGenerating initial accounts.....Finished', end='\n', flush=True)

    def run(self):
        while True:
            self.__generate_account(random.choice(self.__locale))
            time.sleep(random.random())

    def __generate_account(self, locale):
        fk = faker.Faker(locale)
        fk.add_provider(CreditScore)
        profile = fk.simple_profile()
        acc = fk.numerify(text="##############")
        sdn = random.choice(self.__sdn_bool)
        if sdn:
            name = ''
            while name == '':
                name = random.choice(
                    self.__sql.query(
                        'SELECT * FROM SDN ORDER BY RANDOM() LIMIT 1'
                    )[0][1].split('\n')
                )
        else:
            name = profile['name']
        self.__account = (
            acc,
            name,
            fk.date_between('-50y', '-20y'),
            profile['address'],
            profile['mail'],
            fk.company(),
            fk.job(),
            fk.country(),
            fk.credit_score()
        )
        self.__sql.insert_data('ACCOUNTS', self.__account)
        self.count += 1
