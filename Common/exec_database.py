import cx_Oracle
import pymysql
from Common.source_log import MyLogger
"""
1、是否写个类
2、包含数据库初始化、清除表数据、插入表数据、关闭连接
"""
logger = MyLogger().create_logger()


class DBHandler:
    def __init__(self, url_as, db_type):
        self.url_as = url_as
        self.db_type = db_type
        from apiPytest.Common.read_conf import ReadConfig
        conf = ReadConfig()

        username, password, sid = conf.read_xhkx_data(self.url_as, 'username', 'password', 'sid')
        if self.db_type == 'oracle':
            self.conn = cx_Oracle.connect(username, str(password), sid)
            self.cr = self.conn.cursor()
        elif self.db_type == 'mysql':
            host = sid.split(':')[0]
            temp = sid.split(':')[1]
            port = int(temp.split('/')[0])
            db_name = sid.split('/')[1]
            self.conn = pymysql.connect(host=host, port=port, user=username, password=str(password), db=db_name)
            self.cr = self.conn.cursor()

    # 查询数据库表数据
    def select_data(self, sq):
        try:
            self.cr.execute(sq)
            if 'truncate' not in sq:
                result = self.cr.fetchone()
                return result
        except Exception as e:
            logger.info(e)

    # 插入数据
    def insert_data(self, sq):
        try:
            self.cr.execute(sq)
            self.conn.commit()
            logger.info("执行成功")
        except Exception as e:
            logger.info(e)

    # 关闭连接
    def close_db(self):
        self.cr.close()
        self.conn.close()


# db_init为数据库连接的初始配置, 如何判定是oracle，是mysql: 用sheet页名字作标志位
# def db_init(url_as, db_type):
#     from apiPytest.Common.read_conf import ReadConfig
#     conf = ReadConfig()
#
#     cr = None
#     conn = None
#     username, password, sid = conf.read_xhkx_data(url_as, 'username', 'password', 'sid')
#     if db_type == 'oracle':
#         conn = cx_Oracle.connect(username, str(password), sid)
#         cr = conn.cursor()
#     elif db_type == 'mysql':
#         host = sid.split(':')[0]
#         temp = sid.split(':')[1]
#         port = int(temp.split('/')[0])
#         db_name = sid.split('/')[1]
#         conn = pymysql.connect(host=host, port=port, user=username, password=str(password), db=db_name)
#         cr = conn.cursor()
#
#     return cr, conn


# def operate_db(db, sq):
#     # 操作数据库，执行sql，返回字符串
#     db.execute(sq)
#     if 'truncate' not in sq:
#         result = db.fetchone()
#         # db.close()
#         # for i in result:
#         #     actual_result = i
#         #     return actual_result
#         return result


if __name__ == '__main__':
    sql = "select * from T_MESSAGE_INFO"
    table_name = 'execute_record'
    table_data = {'form_name': '任务查询-1-yiji_host-oracle',
                  'case_id': 'case_001',
                  'interface': '任务查询-冒烟',
                  'title': 'startTime、endTime当天时间',
                  'result': "{'code': 0,'msg': '成功'}",
                  'actual_result': "{'code': 0,'msg': '成功'}",
                  'batch': '1',
                  'create_time': '2021-01-20 10:00:00'}
    for i in table_data:
        table_data[i] = "'" + str(table_data[i]) + "'"

    key = '(' + ','.join(table_data.keys()) + ')'
    value = "(" + ",".join(table_data.values()) + ")"
    insert_sql = "insert into {0} {1} values {2}".format(table_name, key, value)
    # pt_test = 'insert into `execute_record` (`form_name`, `case_id`, `interface`, `title`, `result`, ' \
    #           '`actual_result`, `batch`, `create_time`) values ({values})'.format(values=values)
    # sql = 'select a.COMPANY_ID, a.COMPANY_STUTAS, b.dept_id, b.dept_name from T_RCS_COMPANY a,sys_dept b ' \
    #       'where a.COMPANY_STUTAS = 0 and b.status = 0 and b.dept_id = 124 limit 1'
    # print(db_init('5G_host', 'mysql'))
    # print(operate_db(db_init('5G_host', 'mysql'), sql))
    # print(operate_db(db_init("yiji_host", "oracle"), sql))
    db_do = DBHandler("result_base", "mysql")
    db_do.insert_data(insert_sql)
    db_do.close_db()

