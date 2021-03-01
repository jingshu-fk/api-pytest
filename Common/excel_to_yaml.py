import yaml
from apiPytest.Common.read_data import ReadExcel

"""
模块功能：实现从excel用例数据写到yaml文件。
"""


class WriteToYaml:

    def __init__(self):
        pass

    # 从excel用例写入到yaml文件，一个excel的所有sheet都会写入到同一个yaml
    @staticmethod
    def write_yaml():
        from apiPytest.Common.read_conf import ReadConfig
        conf = ReadConfig()
        # 获取到测试用例数据，以及输出的yaml文件名
        excel_file = conf.read_info('file_path', 'excel_file')
        out_yaml = conf.read_info('file_path', 'output_yaml_bak')

        test2 = ReadExcel(excel_file)
        case_3 = test2.read_excel_2()
        print(case_3, type(case_3))

        try:
            with open(out_yaml, 'w', encoding='utf-8') as f:
                # sort_keys可以使写入数据正确排序，allow_unicode避免中文写入乱码
                yaml.dump(data=case_3, stream=f, allow_unicode=True, sort_keys=False)
        except Exception as e:
            print('写入测试数据失败')
            raise e
        else:
            print('写入测试数据成功')

    # 一个excel文件有多个sheet表单，这个方法功能：一个sheet写入一个yaml文件里，有多少个sheet就写到多少个yaml，
    # 不过这些要输出的yaml得在配置文件配置好。sheet的个数得和yaml文件的个数一样才可以。
    @staticmethod
    def pos():
        from apiPytest.Common.read_conf import ReadConfig
        conf = ReadConfig()
        # 获取到测试用例数据，以及输出的yaml文件名
        excel_file = conf.read_info('file_path', 'excel_file')
        out_yamls = conf.read_info('file_path', 'output_yaml')
        out_yaml = out_yamls.split(',')  # 得到的是个列表

        test2 = ReadExcel(excel_file)
        case_3 = test2.read_excel_3()
        print(case_3)

        for i in list(zip(case_3, out_yaml)):
            sheet, ot_yaml = i  # 得到每个sheet和yaml的对子
            try:
                with open(ot_yaml, 'w', encoding='utf-8') as f:
                    # sort_keys可以使写入数据正确排序，allow_unicode避免中文写入乱码
                    yaml.dump(data=sheet, stream=f, allow_unicode=True, sort_keys=False)
            except Exception as e:
                print('写入测试数据失败')
                raise e
            else:
                print('写入测试数据成功')

if __name__ == '__main__':
    rd = WriteToYaml()
    # rd.pos()
    rd.write_yaml()