from py import SQL, Accounts, SDN_Crawler, Analyze


def main(sql):
    if sql.query("SELECT * FROM SDN LIMIT 1") == []:
        SDN_Crawler.run(sql)
    else:
        print('SDN_list exists.')
    trans = Analyze.Analyze(sql)
    acc = Accounts.Accounts(sql, init_acc=None)
    trans.start()
    acc.start()
    while True:
        print(
            f'\rGenerated \033[1m\033[34mAccounts: {acc.count}   \033[33mTransactions: {trans.id}   \033[31mSQL errors: {sql.errors}\033[0m',
            end='',
            flush=True
        )


if __name__ == '__main__':
    # 資料庫名稱
    sql = SQL.SQL('Final_db')
    main(sql)
