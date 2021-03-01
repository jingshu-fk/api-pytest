# -!- coding: utf-8 -!-
import requests
import json
import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)


# response = requests.put('http://192.168.150.142:8095/business/company/auth', data=json.dumps({'companyId': 33, 'companyStutas': 0, 'parentId': 124, 'parentName': '让腾惹他', 'remark': ''},cls=DateEncoder), headers={'Accept': 'application/json, text/plain, */*', 'Connection': 'keep-alive', 'Content-Type': 'application/json;charset=UTF-8', 'Authorization': 'eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjQ5NDAxODZlLWNhMzQtNGQyNy05MDUzLTNkNmU3Y2NjNWQwZSJ9.fCfGNvvoFu0In2geOLpoCVzoZG0xfaDvbKe25zxX55M1-BoeMq7z5XoZTDWK3wlqEpMndWu-BFIpctanlU5eDA'})

"""
上传文件、图片的post方法
"""
# files={'licenseFile':('6578db9ad9f80f86e51f4f37e075b225.jpeg',open(r'D:\6578db9ad9f80f86e51f4f37e075b225.jpeg','rb'),'image/jpeg')}
# dat = {
#         "address":"KFJFEJUfffe",
#         "companyName":"济阳县金兴家政服务中心	",
#         "industryId":"5",
#         "phone":"13900103241",
#         "trusCode": "92370125MA3DDMUG71",
#         "userName": "LFIEff",
# }
# # print(type(dat))
# response = requests.post(url='http://192.168.150.142:8095/business/company/add',data=dat, files=files, headers={'Accept': 'application/json, text/plain, */*','Connection': 'keep-alive'})
# print(response.json())


name = input('你的名字是啥：')
print(name)
