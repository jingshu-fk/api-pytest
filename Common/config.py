from configparser import ConfigParser


class MyConfSe:
    def __init__(self, filename, encoding='utf8'):
        """
                :rtype: object
                """
        self.filename = filename
        self.encoding = encoding
        self.conf = ConfigParser()
        self.conf.read(filename, encoding)

    def get_str(self, section, option):
        return self.conf.get(section, option)

    def get_int(self, section, option):
        return self.conf.getint(section, option)

    # def write_data(self,section,option,value):
    #         self.conf.set(section,option,value)
    #         self.conf.write(open(self.filename,'a',encoding=self.encoding)


if __name__ == '__main__':
    conf1 = MyConfSe(r'E:\mywork\API_TEST\apiPytest\data\config.yaml')
    print(conf1.get_str('basic_info', 'token'))
