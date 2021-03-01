"""
封装断言方法

思路：
#1 遍历返回结果的每个key，
#2 根据key去预期结果找对应值
#3 比较两个结果值是否相等
"""


class AssertRe:

    def __init__(self):
        # self.test_result = test_result
        # self.excepted = excepted
        pass

    @staticmethod
    def assert_job(test_result, excepted):
        # 遍历返回结果的键值，每个值断言
        for k, v in excepted.items():
            assert v == test_result[k]

        return None


if __name__ == '__main__':
    AssertRe().assert_job({
    "code": 0,
    "data": [],
    "msg": "成功"
}, {
    "code": 1,
    "msg": "成功"
})

