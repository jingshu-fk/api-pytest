# -!- coding: utf-8 -!-
# 清除掉原来的测试报告数据
import shutil
import os
"""
入参：指定目录
逻辑：遍历该目录下的文件和文件夹，一一删除
"""


class PreDo:
    @staticmethod
    def remove_allure(*args):
        for ar in args:
            print(ar)
            for f in os.listdir(ar):
                filepath = os.path.join(ar, f)
                if os.path.isfile(filepath):
                    os.remove(filepath)
            #  模板文件都是json格式的
                elif os.path.isdir(filepath):
            # if 'json' or 'attachment' in i:
            #     os.remove(content + '/' + filepath)
                    shutil.rmtree(filepath)

    # 搬移excel用例到备份目录
    @staticmethod
    def mv_file(dri_path):
        for f in os.listdir(dri_path):
            file = os.path.join(dri_path, f)
            if os.path.isfile(file):
                s = 'mv ' + file + ' ' + '../backup'
                os.system(s)


# PreDo.remove_allure('../Report/data/', '../run_yaml/')
#PreDo.mv_file('../TestExcel')


