from py import SQL, Accounts, SDN_Crawler, Analyze


def main(sql):
    if sql.query("SELECT * FROM SDN LIMIT 1") == []:
        SDN_Crawler.SDN_Crawler(sql)
    trans = Analyze.Analyze(sql)
    acc = Accounts.Accounts(sql)
    trans.start()
    acc.start()
    trans.join()
    acc.join()
    sql.close()


if __name__ == '__main__':
    sql = SQL.SQL('db_test2')
    main(sql)
