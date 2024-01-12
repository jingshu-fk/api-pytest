from Common.exec_database import DBHandler
from Common.source_log import MyLogger


logger = MyLogger().create_logger()


class DealDepend(object):
    def __init__(self):
        pass

    @staticmethod
    def treat_data(is_db, change_word, sql, body, case_id, depend, sr, db_init):
        # 判断depend字段是否为字典类型，不是就转成字典
        if isinstance(depend, dict):
            pass
        else:
            depend = eval(depend)

        # 判断body字段是否为字典类型，不是就转成字典
        if isinstance(body, dict):
            pass
        elif isinstance(body, list):
            pass
        else:
            if body is not None:
                body = eval(body)
        # sr = Save_depend_data()

        # 【判断依赖类型】
        # 1 是否数据库依赖
        if is_db == 1:
            # 依赖字段是否为空，说明只执行sql
            if change_word is None:
                db_init.select_data(sql)
                # operate_db(db_init,sql)
                logger.info('已执行SQL：%s', sql)
            else:
                # 把excel的change_word字段分割
                update_words = change_word.split(',')
                # 从数据库取到的字段值,可能有多个字段的值
                msg = db_init.select_data(sql)
                # msg = operate_db(db_init, sql)
                # 遍历每个字段
                for field in range(len(msg)):
                    # 判断body的类型是dict还是list
                    if isinstance(body, list):
                        body[0][update_words[field]] = msg[field]
                        # body[0][change_word] = msg
                    elif isinstance(body, dict):
                        body[update_words[field]] = msg[field]
            # 保存修改后的实际请求body
            logger.info('用例%s请求值为%s：' % (case_id, body))
            # sr.save_body(case_id, body)
        # 2 是否接口依赖
        elif {} != depend:
            temp = sr.read_depend_data(depend)
            # 合并字典
            body = dict(body, **temp)
            logger.info('用例%s请求值为%s：' % (case_id, body))
            # 保存实际的请求body
            # sr.save_body(case_id, body)
        else:
            # 3 没有依赖，不需要修改body
            logger.info('用例%s请求值为%s：' % (case_id, body))
            # sr.save_body(case_id, body)
        return body
