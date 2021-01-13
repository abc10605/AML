from py import SQL, Accounts, SDN_Crawler, Analyze
import time

def main(sql):
    if sql.query("SELECT * FROM SDN LIMIT 1") == []:
        SDN_Crawler.run(sql)
    trans = Analyze.Analyze(sql)
    acc = Accounts.Accounts(sql)
    time.sleep(.1)
    trans.start()
    acc.start()
    while True:
        print(
            f'\rGenerated Accounts: {acc.count}   Transactions: {trans.id}   SQL errors: {sql.errors}',
            end='',
            flush=True
        )


if __name__ == '__main__':
    sql = SQL.SQL('db_test')
    main(sql)
