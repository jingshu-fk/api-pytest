import yaml


# with open(r'E:\mywork\Pyprojects\work\api_pytest\data\config.yml', 'r', encoding='utf8') as f:
#     context = yaml.load(f, Loader=yaml.FullLoader)
#
#     print('读取内容', context, type(context))
#     print(context['file_path'], type(context['file_path']))
#     print(context['basic_info'], type(context['basic_info']))
#     print(context['file_path']['host'], type(context['file_path']['host']))

class ReadConfig:
    data = None

    def __init__(self):
        with open('../data/config.yml', 'r', encoding='utf-8') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

    def read_info(self, point, info):
        return self.data[point][info]

    def read_server(self, point, server_name):
        return self.data[point][server_name]

    def read_token(self, point, token_path):
        return self.data[point][token_path]

    def read_xhkx_data(self, point, username, passwd, url):
        return self.data[point][username], self.data[point][passwd], self.data[point][url]

    def read_xhkx_sql(self, point, sql):
        return self.data[point][sql]


if __name__ == '__main__':
    conf = ReadConfig()
    # print(conf.read_server('file_path', 'host'))
    # print(conf.read_token('basic_info', 'token'))
    # username, password, url = conf.read_xhkx_data('xhkx_database', 'username', 'password', 'url')
    # print(username, password, url)
    # print(isinstance(username, str))
    print(conf.read_info('file_path', 'excel_file'))