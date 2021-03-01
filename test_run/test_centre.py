import sys
import os

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
from apiPytest.Common.excel_to_yaml import WriteToYaml
from apiPytest.Common.clean import PreDo

# 读取excel的数据 ---------------------------------------------------------------------------------------------
# test2 = ReadExcel('../TestExcel/应急云化任务查询.xlsx')
# test2 = ReadExcel('../TestExcel/新华快讯demo.xlsx')
# cases = test2.read_data()

# 实例化配置文件模块
conf = ReadConfig()

# 获取配置文件目录下的excel文件
excel_file_path = conf.read_info('file_path', 'excel_file')  # 输入：用例数据excel
excel_file = None
for fe in os.listdir(excel_file_path):
    excel_file = os.path.join(excel_file_path, fe)
    if os.path.isfile(excel_file):
        logger.info('excel文件名为%s' % excel_file)

create_yml = conf.read_info('file_path', 'output_yaml')  # 这是个目录，动态生成yaml文件存放地址
# 初始化用例数据，把excel用例转为yaml文件存储
rd = WriteToYaml()
url_as, dbs = rd.dynamic_yaml(excel_file, create_yml)

# 实例化数据依赖模块
deal_depend = DealDepend()

# 从配置文件conf.yml获取token, host, sql

token = conf.read_info('basic_info', 'token')

host = conf.read_info('file_path', url_as)
# run_sql = conf.read_info('xhkx_database', 'sql')


# 定义测试报告输出目录
report_data = conf.read_info('file_path', 'Report')
report_generate = conf.read_info('file_path', 'Result')

# 数据库初始化
#db_init = DBHandler(url_as, dbs)
db_init = None
# db_init = db_init(url_as, dbs)
# 测试结果要写入的数据库
#url_db = conf.read_info('file_path', 'result_base')
#result_db = DBHandler(url_db, 'mysql')
# 读取数据库表测试数据 ------------------------------------------------------------------------------------------2
# test3 = ReadDatabase(db_init, run_sql)
# cases = test3.get_data()

# 从yaml文件读取用例数据： 可能会有多个yaml文件-----------------------------------------------------------------------------------------3
folders = os.listdir(create_yml)
cases = []
for folder in folders:
    ry = ReadYaml(create_yml + folder)
    cases.extend(ry.get_yaml_data())  # 把out_yamls目录的yaml文件汇总起来

# cases = ry.get_yaml_data()

# 实例化日志模块
logger = MyLogger().create_logger()
logger.info('cases的值为：%s ' % cases)
# 实例化保存body和响应的模块
sr = SaveSuRe()

# 实例化断言的模块
ase = AssertRe()
titles = []
# 清除之前的测试报告数据
PreDo.remove_allure(report_data, create_yml)


# 添加项目名称
@allure.epic('5G')
class TestApiAuto(object):

    @staticmethod
    def run_test():
        import os
        logger.info('计数器次数')
        # 执行产生测试结果数据
        pytest.main(args=[f'--alluredir={report_data}'])
        # 从现有的测试结果生成报告
        os.system(f'allure generate {report_data} -o {report_generate} --clean')
        logger.info('测试报告已生成！')

    @allure.testcase('https://www.cnblogs.com/jinggs/', '我的博客')
    # 用例优先级
    @allure.severity('critical')
    @pytest.mark.parametrize('case_id, interface, title, method, path, header, header_change, body, excepted,'
                             'depend, is_db, sql, change_word, is_exec, module_name', cases)
    # @pytest.mark.parametrize("test_input, expected", [
    #     ("3+5", 8),
    #     pytest.param("6*9", 54, marks=pytest.mark.xfail, id="this case -- xfail"),
    # ])
    def test_main(self, case_id, interface, title, method, path, header, header_change, body, excepted, depend, is_db,
                  sql, change_word, is_exec, module_name):
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
        :param is_exec: 该条用例是否需要执行标志位
        :param module_name: 模块名
        :return:
        """
        # 动态添加自定义字段
        allure.dynamic.feature(module_name)
        allure.dynamic.description(interface)
        allure.dynamic.title(title)

        # 判断用例是否执行过，执行过就pass掉【根据title名称】
        if title not in titles:
            titles.append(title)
            logger.info('执行用例%s——', case_id)

            with allure.step('处理数据依赖，修改body'):
                body = deal_depend.treat_data(is_db, change_word, sql, body, case_id, depend, sr, db_init)
                sr.save_body(case_id, body)
            with allure.step('发送请求，得到响应'):
                test_result = request_me(token, host, path, body, method, header, header_change)
                logger.info('实际响应为：%s' % test_result)
            with allure.step('与预期结果比较断言'):
                if isinstance(excepted, dict):
                    ase.assert_job(test_result, excepted)
                else:
                    ase.assert_job(test_result, eval(excepted))
            with allure.step('保存响应结果'):
                # 第五步，保存响应
                sr.save_response(case_id, test_result)
                # logger.info("%d批次插入数据成功" % batch)
        #     # 写是否通过，pass后者false
        #     test2.write_data(int(case_id) + 1, 8, 'pass')
        #     actual_result = json.dumps(test_result, ensure_ascii=False)
        #     test2.write_data(int(case_id) + 1, 9, actual_result)


TestApiAuto().run_test()
#result_db.close_db() # 关闭数据库连接
#db_init.close_db()
PreDo.mv_file('../TestExcel')
# if __name__ == '__main__':
#     TestApiAuto().run_test()
