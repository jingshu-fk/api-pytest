import requests
import json

from Common.read_conf import ReadConfig

def get_task():

	# headers = {
    #           'Accept': 'application/json, text/plain, */*',
    #           'Connection': 'keep-alive',
    #           'Content-Type': 'application/json;charset=UTF-8',
    #         }
	url = 'http://192.168.150.131:8787/taskInfo/get'
	# params = {
    # 	"messageCode":"XHKX_DZ_CDX",
    # 	"beginsTime":"2020-08-05T01:57:00.000Z",
    # 	"engTime":"2020-08-05T07:57:00.000Z",
    # 	"areas":"570",
    # 	"content":"冒烟测试流程2"
	#   }
	params = {
		"startTime": "2020-03-26 00:00:00",
		"endTime": "2020-03-27 23:59:59"
	}
	# r = requests.post(url=url, data=json.dumps(params), headers=headers)
	# logger.info('响应的json为：%s' % (r.json()))
	r = requests.get(url, params=params)
	return r.json()

def dict_test():
	dict1 = {"msg":"操作成功","code":200}
	dict2 = {"msg":"操作成功","code":200}
	for k, v in dict1.items():
		print(k)
		print(v)
		if v == dict2[k]:
			print("bingo")


def run_test():
	conf = ReadConfig()
	out_yamls = conf.read_info('file_path', 'output_yaml')
	out_yaml = out_yamls.split(',')

	print(out_yaml)

def oop():
	a = ['a.yaml', 'b.yaml', 'c.yaml', 'd.yaml']
	b = ['sheet1', 'sheet2', 'sheet3', 'sheet4']
	for i in list(zip(a, b)):
		yaml, sheet = i
		print(yaml, sheet)

def ww():
	c = ['1-1', '2-1', '3-0', '5-0']

	for i in c:
		if i.split('-')[-1] == '0':
			c.remove(i)
		else:
			print('pass')
	print(c)





if __name__ == '__main__':
	# print(get_task())
	# dict_test()
	# print(oop())
	ww()