import openpyxl
import yaml
import ast

"""
模块功能：
    1、实现从excel里读取用例数据，供PyTest使用或者excel_to_yaml模块使用
    2、实现从ORACLE数据库里读取用例数据，供PyTest使用
    3、实现从yaml文件里读取用例数据，供PyTest使用
"""


# 从excel里读取用例数据
class ReadExcel:
    # 传入excel文件名
    def __init__(self, file_name):
        self.file_name = file_name
        # 定义打开excel的对象
        self.wb = openpyxl.load_workbook(self.file_name)
        # self.sheet_name = sheet_name

    def get_sheets(self):
        # self.sh = self.wb[self.sheet_name]
        # 获取到所用的表单名
        sheet_names = self.wb.sheetnames

        return sheet_names

    def close(self):
        self.wb.close()

    def read_data(self):
        """遍历excel的每一个sheet表单，每个表单按行读取数据，最后返回一个存储元组的列表，每个元组即是一行用例数据"""
        # 得到所有的表单名
        sheets = self.get_sheets()
        cases = []
        # 遍历每个表单
        for i in sheets:
            # 定义操作excel表单对象
            self.sh = self.wb[i]
            # 获取该表单的行数
            rows = list(self.sh.rows)
            titles = []
            # 把第一行的字段添加到列表
            for t in rows[0]:
                title = t.value
                titles.append(title)
            # case = []
            # 对后面的每一行遍历
            for row in rows[1:]:
                case = []
                # 遍历每一行的每个字段
                for r in row:
                    case.append(r.value)
                # 转化为PyTest参数化需要的元组数据，每一个为一条用例的所有字段。
                module_name = i
                case.append(module_name)
                case2 = tuple(case)
                # print(case)
                # cases.append(dict(zip(titles, case)))  # 通过zip聚合打包用例的标题和数据
                # 遍历一行的每个字段后，把该元组添加到列表cases。
                cases.append(case2)
        self.close()
        return cases

    def read_excel_2(self):
        """遍历excel的每一个sheet表单，每个表单按行读取数据，最后返回一个字典，每个value是一个列表，即一行的用例数据，列表里是一个字典，里面是每个字段的key，value"""
        # 得到所有的表单名
        sheets = self.get_sheets()
        # 遍历每个表单
        terminal_cases = {}

        # 用例编号初始化
        case_sequence = 0
        for i in sheets:
            # 定义操作excel表单对象
            self.sh = self.wb[i]
            # 获取该表单的行数
            rows = list(self.sh.rows)
            titles = []
            # 把第一行的字段添加到列表
            for t in rows[0]:
                title = t.value
                titles.append(title)

            for row in rows[1:]:
                # case = []
                # 遍历每一行的每个字段
                num = 0
                dict_cases = {}  # 用来存放一行用例数据
                cases = []
                # 一行的用例数据处理完成，得到列表，里面是字典（具体到每个字段）
                for r in row:
                    temp_1 = r.value
                    # 判断字段是否是属于字典类型的，
                    if titles[num] in ['body', 'excepted', 'headers', 'depend']:
                        # 如果该字段的值不是空，就把该字段值转为字典
                        if r.value is not None:
                            temp_2 = ast.literal_eval(r.value)
                            dict_cases[titles[num]] = temp_2
                        # 为空的话，就直接添加到字典dict_cases里
                        else:
                            dict_cases[titles[num]] = temp_1
                    # 不是属于字典类型的，直接添加到字典dict_cases里
                    else:
                        dict_cases[titles[num]] = temp_1
                    num += 1
                # 一条用例处理完成，得到列表
                cases.append(dict_cases)

                # 用例编号递增
                case_sequence += 1

                # 最终得到所有sheets的一个字典，key为case,value为列表，里面是字典，一个字典里是一条用例：
                # {'case1': [{'case_id': 'case_001', 'interface':'任务查询',....}], 'case2':['']}
                terminal_cases['case' + str(case_sequence)] = cases
        self.close()
        return terminal_cases

    def read_excel_3(self):
        """
        遍历excel的每一个sheet表单，每个表单里的按行遍历数据，一个sheet的写到字典middle_cases里，key为用例编号，value为列表cases，
        里面是字典dict_cases，字典里面是具体每个字段的key，value
        最后把每个sheet的字典，都会添加到列表terminal_cases
        """
        # 得到所有的表单名
        sheets = self.get_sheets()

        # 把每个sheet的用例数据添加进来
        terminal_cases = []
        # 用例编号初始化
        case_sequence = 0
        for i in sheets:
            # 用来存储单个sheet的用例数据
            middle_cases = {}

            # 定义操作excel表单对象
            self.sh = self.wb[i]
            # 获取该表单的行数
            rows = list(self.sh.rows)
            titles = []
            # 把第一行的字段添加到列表
            for t in rows[0]:
                title = t.value
                titles.append(title)

            for row in rows[1:]:
                # case = []
                # 遍历每一行的每个字段
                num = 0
                dict_cases = {}  # 用来存放一行用例数据
                cases = []
                # 一行的用例数据处理完成，得到列表，里面是字典（具体到每个字段）
                for r in row:
                    temp_1 = r.value
                    # 判断字段是否是属于字典类型的，
                    if titles[num] in ['body', 'excepted', 'headers', 'depend']:
                        # 如果该字段的值不是空，就把该字段值转为字典
                        if r.value is not None:
                            temp_2 = ast.literal_eval(r.value)
                            dict_cases[titles[num]] = temp_2
                        # 为空的话，就直接添加到字典dict_cases里
                        else:
                            dict_cases[titles[num]] = temp_1
                    # 不是属于字典类型的，直接添加到字典dict_cases里
                    else:
                        dict_cases[titles[num]] = temp_1
                    num += 1
                # 一条用例处理完成，得到列表
                cases.append(dict_cases)

                # 用例编号递增
                case_sequence += 1

                # 最终得到所有sheets的一个字典，key为case,value为列表，里面是字典，一个字典里是一条用例：
                # {'case1': [{'case_id': 'case_001', 'interface':'任务查询',....}], 'case2':['']}
                middle_cases['case' + str(case_sequence)] = cases
            terminal_cases.append(middle_cases)
        self.close()
        return terminal_cases


# 从数据库表读取用例数据
class ReadDatabase:
    def __init__(self, db_init, sql):
        self.db_init = db_init
        self.sql = sql

    def get_data(self):
        # 执行sql
        self.db_init.execute(self.sql)
        # 返回的就是一个列表，里面每个元素是个元组
        result = self.db_init.fetchall()

        return result


# 从yaml文件读取用例数据,供pytest参数化使用
class ReadYaml:
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def get_yaml_data(self):
        cases = []
        print(self.data)
        for k, v in self.data.items():
            for value in v:
                case = []
                for zi_key, zi_value in value.items():
                    case.append(zi_value)
                case2 = tuple(case)
                cases.append(case2)

        return cases


if __name__ == '__main__':
    # test2 = ReadExcel('../TestExcel/应急云化任务查询.xlsx')
    # test2 = ReadExcel('../TestExcel/新华快讯demo.xlsx')
    # test2.write_data(2, 8, 'pass')
    # res2 = test2.read_data()  # 最后返回一个存储字典的列表
    # print(res2)
    # print(len(res2))
    # ---------------------------------------------------------------------------
    # db = cx_Oracle.connect('xhkx_test', 'czty_xhkx123', '192.168.150.116:1521/pdbtest')
    # cr = db.cursor()
    # test3 = ReadDatabase(cr, sql='select * from t_xhkx_data')
    # print(test3.get_data())
    #
    # # --------------------------------------------------------------------------------
    # ry = ReadYaml('../TestExcel/yjqf_yh.yaml')
    # print(ry.get_yaml_data())
    # if ry.get_yaml_data() == test3.get_data():
    #     print('pass')


    test2 = ReadExcel('../TestExcel/新华快讯功能接口用例.xlsx')
    print(test2.read_excel_3())

    # rd = WriteYaml()
    # rd.pos()
