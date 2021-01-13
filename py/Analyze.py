import datetime
import random
import threading
import time


class Transactions():
    def __init__(self):
        self.__transactionType = tuple(
            ['CashDeposit', 'CashWithdraw', 'Transfer'])
        # 各交易區間出現的機率
        self.__amt = tuple(
            [100000] * 500 +
            [500000] * 100 +
            [1000000] * 10 +
            [5000000] * 5 +
            [10000000] * 2 +
            [50000000] * 1
        )

    def generate_transaction(self, id, orig_acc=None, dest_acc=None):
        _type = random.choice(self.__transactionType)
        # 從帳戶檔抓帳戶，或是亂數產生
        orig_acc = orig_acc if orig_acc is not None else f'{random.randint(1, 99999999999999):014d}'
        dest_acc = dest_acc if dest_acc is not None else f'{random.randint(1, 99999999999999):014d}'
        transaction = [id,
                       _type,
                       orig_acc,
                       dest_acc if _type == 'Transfer' else None,
                       # 金額
                       random.randint(1, random.choice(self.__amt)),
                       # 時間
                       datetime.datetime.now(),
                       # 標記
                       None
                       ]
        return transaction


class Analyze(threading.Thread):
    def __init__(self, sql):
        threading.Thread.__init__(self)
        self.__sql = sql
        self.__transaction = Transactions()
        # 抓交易檔數量（順序編號）
        self.id = self.__sql.query("SELECT COUNT(*) FROM TRANS")[0][0] + 1
        self.__from_acc = tuple([True] * 2 + [False] * 3)

    def run(self):
        while True:
            # 產生交易
            if random.choice(self.__from_acc):
                trans = self.__transaction.generate_transaction(
                    self.id,
                    self.__sql.query(
                        'SELECT acc FROM ACCOUNTS ORDER BY RANDOM() LIMIT 1')[0][0],
                    self.__sql.query(
                        'SELECT acc FROM ACCOUNTS ORDER BY RANDOM() LIMIT 1')[0][0]
                )
            else:
                trans = self.__transaction.generate_transaction(
                    self.id)

            # 金額分析
            trans = self.__amt_analysis(trans)
            try:
                self.__sql.insert_data('TRANS', trans)
                self.id += 1
            except:
                pass

    def __amt_analysis(self, trans):
        amt = trans[4]
        try:
            # 查詢該帳號平均交易金額
            avg_amt = self.__sql.query(
                f"SELECT AVG(Amount) FROM TRANS WHERE OrigAcc = {trans[2]}")
            avg_amt = float(avg_amt[0][0])
        except:
            avg_amt = 1000000000000000
        if amt >= 10000000:
            trans[-1] = 2
        elif amt >= 1000000 and amt >= avg_amt * 5:
            trans[-1] = 2
        elif amt >= 100000 and amt >= avg_amt * 10:
            trans[-1] = 1
        elif amt >= 500000:
            trans[-1] = 1
        else:
            # 查詢一個禮拜內的總交易額
            amt = self.__sql.query(f'''
                SELECT sum(Amount) FROM TRANS
                WHERE OrigAcc = {trans[2]} AND DT > date(\'now\', \'-7 day\')'''
                                   )[0][0]
            # 如果總交易額大於五十萬就標記 1
            if amt is not None and amt >= 500000:
                trans[-1] = 1
            else:
                trans[-1] = 0
        return trans

# ----------------------------------------------------------------


def sdn_acc(sql):
    # 先抓所有帳戶
    acc = sql.query('select * from ACCOUNTS')
    print("\nBelow are the accounts having the same name as the SDN list\n")
    time.sleep(2)
    for i in acc:
        if sql.query(f"select * from SDN where Name like '%{i[1]}%'") != []:
            print(i)


def kyc(sql):
    acc = sql.query('select * from ACCOUNTS ORDER BY RANDOM() LIMIT 10')
    browser = Browser()
    browser.open_browser()
    for i in acc:
        browser.search(f'https://www.google.com/search?q={i[1]}')
        time.sleep(1)
    browser.close_browser()


def same_address(sql):
    print('\nChecking for same address\n')
    addr = sql.query(
        '''
        SELECT * FROM ACCOUNTS
        WHERE address = (
            SELECT address FROM ACCOUNTS
            GROUP BY address
            HAVING COUNT(*) > 1
            )
        ''')
    if addr != []:
        for i in addr:
            print(i)
    else:
        print('\nNo same address found\n')


if __name__ == "__main__":
    from Browser import Browser
    from SQL import SQL

    sql = SQL('Final_db')
    proc = eval(input(
        "\nWhich process do you want to run?\n1) SDN_ACC\n2) KYC\n3) SAME_ADDRESS\nEnter: "))
    if proc == 1:
        sdn_acc(sql)
    elif proc == 2:
        kyc(sql)
    elif proc == 3:
        same_address(sql)
