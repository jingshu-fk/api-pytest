# import cx_Oracle


# db_init为数据库连接的初始配置
def db_init():
    import cx_Oracle
    from apiPytest.Common.read_conf import ReadConfig
    conf = ReadConfig()
    username, password, url = conf.read_xhkx_data('xhkx_database', 'username', 'password', 'url')
    db = cx_Oracle.connect(username, password, url)
    cr = db.cursor()

    return cr


def operate_db(db, sql):
    # 操作数据库，执行sql，返回字符串
    # db = cx_Oracle.connect('xhkx_test', 'czty_xhkx123', '192.168.150.116:1521/pdbtest')
    # cr = db.cursor()
    db.execute(sql)

    if 'truncate' not in sql:
        result = db.fetchone()
        for i in result:
            actual_result = i
            return actual_result


if __name__ == '__main__':
    sql = "select id from T_MESSAGE_TASK"
    db_init()
    print(operate_db(db_init(), sql))
