import pathlib
import random
import threading
import time

import faker
import progressbar
from faker_credit_score import CreditScore


class Accounts(threading.Thread):
    def __init__(self, sql):
        threading.Thread.__init__(self)
        self.__sql = sql
        self.__locale = []
        for i in open(f'{pathlib.Path(__file__).parent.parent}/data/locale.txt', 'r').readlines():
            if i == '\n':
                pass
            else:
                self.__locale.append(i.replace('\n', ''))
        self.__locale = tuple(self.__locale)
        self.__sdn_bool = tuple([True] + [False] * 499)
        init_acc = 50
        print('\nGenerating initial accounts')
        for i in progressbar.progressbar(range(init_acc)):
            self.__generate_account(random.choice(self.__locale))

    def run(self):
        while True:
            self.__generate_account(random.choice(self.__locale))
            #print('accounts generated')
            time.sleep(random.random() * 3)

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
            faker.Faker().country(),
            fk.credit_score()
        )
        # if sdn:
        #    print(f'sdn: {self.__account}')
        self.__sql.insert_data('ACCOUNTS', self.__account)
