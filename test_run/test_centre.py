import sys

print(sys.path)
import pytest
import allure
from apiPytest.Common.read_data import *
from apiPytest.Common.source_log import MyLogger
from apiPytest.Common.dealrely import DealDepend
from apiPytest.Common.read_conf import ReadConfig
from apiPytest.Common.requ_met import request_me
from apiPytest.Common.save_su_re import SaveSuRe
from apiPytest.Common.assert_re import AssertRe
from apiPytest.Common.exec_database import *

# 读取excel的数据 ---------------------------------------------------------------------------------------------1
# test2 = ReadExcel('../TestExcel/应急云化任务查询.xlsx')
# test2 = ReadExcel('../TestExcel/新华快讯demo.xlsx')
# cases = test2.read_data()

# 实例化数据依赖模块
deal_depend = DealDepend()
# 实例化配置文件模块
# 从配置文件conf.yml获取token, host, sql
conf = ReadConfig()
token = conf.read_info('basic_info', 'token')
host = conf.read_info('file_path', 'host')
run_sql = conf.read_info('xhkx_database', 'sql')
yaml_file = conf.read_info('file_path', 'output_yaml')

# 定义测试报告输出目录
report_data = conf.read_server('file_path', 'Report')
report_generate = conf.read_server('file_path', 'Result')

# 数据库初始化
db_init = db_init()
# 读取数据库表测试数据 ------------------------------------------------------------------------------------------2
# test3 = ReadDatabase(db_init, run_sql)
# cases = test3.get_data()

# 从yaml文件读取用例数据-----------------------------------------------------------------------------------------3
ry = ReadYaml(yaml_file)
cases = ry.get_yaml_data()

# 实例化日志模块
logger = MyLogger().create_logger()
logger.info('cases的值为：%s ' % cases)
# 实例化保存body和响应的模块
sr = SaveSuRe()

# 实例化断言的模块
ase = AssertRe()


# 添加项目名称
@allure.epic('新华快讯项目')
class TestApiAuto(object):

    @staticmethod
    def run_test():
        import os
        logger.info('计数器次数')
        # 执行产生测试结果数据
        pytest.main(args=[f'--alluredir={report_data}'])
        # 从现有的测试结果生成报告
        # os.system(f'pytest --alluredir={report_data}')
        os.system(f'allure generate {report_data} -o {report_generate} --clean')
        logger.info('测试报告已生成！')

    # 每行用例读取到，调用请求方法发起请求，断言，写结果
    @allure.testcase('https://www.cnblogs.com/jinggs/', '我的博客')
    # 用例优先级
    @allure.severity('critical')
    @pytest.mark.parametrize('case_id, interface, title, method, path, header, header_change, body, excepted,'
                             'depend, is_db, sql, change_word', cases)
    def test_main(self, case_id, interface, title, method, path, header, header_change, body, excepted, depend, is_db,
                  sql, change_word):
        """
        :param case_id: 用例编号
        :param interface: 接口信息
        :param title: 用例标题
        :param method: 请求方法
        :param path: 请求路径
        :param header: 请求头
        :param header_change: 请求头修改字段
        :param body: 请求体
        :param excepted: 预期结果
        :param depend: 依赖字段
        :param is_db: 是否执行SQL
        :param sql: SQL语句
        :param change_word: 数据库依赖字段名
        :param module_name: 模块名
        :return:
        """
        # 动态添加模块
        # allure.dynamic.feature(module_name)
        # 添加动态用例描述
        allure.dynamic.description(interface)
        # 动态添加用例标题
        allure.dynamic.title(title)
        logger.info('执行用例%s——', case_id)

        with allure.step('处理数据依赖，修改body'):
            # 第一步，处理数据依赖，是否修改请求body，判断依赖类型，处理依赖
            body = deal_depend.treat_data(is_db, change_word, sql, body, case_id, depend, sr, db_init)
            # 保存实际的请求body
            sr.save_body(case_id, body)
        with allure.step('发送请求，得到响应'):
            # 第二步，发送请求,得到实际的结果
            test_result = request_me(token, host, path, body, method, header, header_change)
            logger.info('实际响应为：%s' % test_result)
        with allure.step('与预期结果比较断言'):
            # 第三步，预期结果的每个key的value值跟实际响应的对应key的value比较断言，有1个断言失败就认为该用例执行失败。
            # assert test_result == eval(excepted)
            if isinstance(excepted, dict):
                ase.assert_job(test_result, excepted)
            else:
                ase.assert_job(test_result, eval(excepted))
        with allure.step('保存响应结果'):
            # 第五步，保存响应
            sr.save_response(case_id, test_result)
        # with allure.step('写入测试结果'):
        #     # 写是否通过，pass后者false
        #     test2.write_data(int(case_id) + 1, 8, 'pass')
        #     actual_result = json.dumps(test_result, ensure_ascii=False)
        #     test2.write_data(int(case_id) + 1, 9, actual_result)


TestApiAuto().run_test()

if __name__ == '__main__':
    TestApiAuto().run_test()
