import json
import jsonpath
from Common.source_log import MyLogger


# 调用日志模块
# output_log = '../Log/' + 'save_depend_data.log'
logger = MyLogger().create_logger()


class SaveSuRe(object):

    def __init__(self):
        # 初始化保存请求和相应的两个字典
        self.actual_body_1 = {}
        self.actual_body_2 = {}

    # 保存请求方法
    def save_body(self,case_id, actual_body):
        """
               :param case_id:用例编号
               :param actual_result:对应用例编号的实际响应
        """
        # 添加一个键值对到字典
        self.actual_body_1[case_id] = actual_body
        # print('第%s的body字典值是：%s' % (case_id, actual_body))
        # logger.info('第%s的body字典值是：%s' % (case_id, actual_body))

    # 保存请求返回的实际响应方法
    def save_response(self,case_id, actual_result):
        self.actual_body_2[case_id] = actual_result
        # print(self.actual_body_2)

    def read_depend_data(self, depend):
        """
               :param depend: 需要依赖数据字典{"case_001":"['jsonpaht表达式1', 'jsonpaht表达式2']"}
               :return:
        """
        # 定义一个函数返回的修改后的字典
        depend_dict = {}

        if isinstance(depend, dict):
            pass
        else:
            # 字典转为json格式的字符串
            temp = json.dumps(depend)
            # json格式字符串转为字典
            depend = json.loads(temp)

        # 判断depend字典里面是否有body字段，有说明需要从之前的body上取，修改body
        if 'body' in depend:
            # 对depend字典的每个键值对遍历
            for k,v in depend.items():
                try:
                    # 如果键是body，就不用处理
                    if k == 'body':
                        # print('不处理')
                        pass
                    else:
                        # 对每个value遍历
                        for value in v:
                            # print('body字典的值为: %s' % self.actual_body_1)
                            logger.info('body字典的值为: %s' % self.actual_body_1)
                            # 根据这个value的key，到保存请求的字典actual_body_1找对应的value
                            actual = self.actual_body_1[k]
                            # 切片
                            d_k = value.split('.')[-1]
                            # 找到的value值添加到depend_dict字典里
                            depend_dict[d_k] = jsonpath.jsonpath(actual,value)[0]
                except TypeError as e:
                    logger.error(f'实际body中无法正常使用该表达式提取到任何内容，发现异常{e}')
        else:
            for k,v in depend.items():
                try:
                    for value in v:
                        # print('body字典的值为: %s' % self.actual_body_2)
                        logger.info('body字典的值为: %s' % self.actual_body_2)
                        actual = self.actual_body_2[k]
                        # 返回依赖数据的key
                        d_k = value.split('.')[-1]
                        # 添加到依赖数据字典并返回
                        depend_dict[d_k] = jsonpath.jsonpath(actual, value)[0]
                except TypeError as e:
                    logger.error(f'实际响应结果中无法正常使用该表达式提取到任何内容，发现异常{e}')

        return depend_dict


if __name__ == '__main__':
    sr = SaveSuRe()
    sr.save_body("8", {"id":302,"sensitiveWord":"马"})
    # sr.save_response("case_008", {"msg": "操作成功", "code": 200})
    sr.save_body('9',{"sensitiveWord":"应急下发测试短信请及"})
    # sr.save_response('case _009',{"msg":"操作成功","code":200})

    print(sr.save_body, type(sr.save_body))
    depned_str = {"8": ["$.id"],"body":1}

    result = sr.read_depend_data(depned_str)
    dict1 = {"sensitiveWord":"应急下发测试短信请及"}
    print(result, type(result))
    print(dict(dict1, **result))