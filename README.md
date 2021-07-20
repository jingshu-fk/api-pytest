# API-pytest-func

接口自动化测试框架

读取excel测试用例，转为yml，接口数据依赖处理，然后发送请求得到结果断言。

技术选型：Python+Pytest+request+allure+jenkins

整个框架的目录架构如下：

![image](https://user-images.githubusercontent.com/65322530/126270234-c60c1105-193f-44f6-9e57-91429e9d21d8.png)


Common：

  --assert_re.py：封装断言方法
  
  --clean.py：清除掉原来的测试报告数据
  
  --read_conf.py：读取配置文件
  
  --dealrely.py：封装处理接口依赖
  
  --excel_to_yaml.py：excel用例数据转换为yaml格式
  
  --exec_database.py：封装操作数据库
  
  --requ_met.py：封装请求
  
  --save_su_re.py：封装保存请求和响应
  
  --source_log.py：封装日志
  
Log：

  -- 日志文件
  
Data：

  --config.yml：配置文件
  
Report：

  --data：测试结果数据
  
  --html：测试报告
  
TestExcel：

  -- 用例存放目录
  
test_run:

  --test_centre.py：程序运行主入口

自动化主体逻辑：

![image](https://user-images.githubusercontent.com/65322530/126269181-10f4c46b-cee0-4a6f-b7bd-ea53979a6401.png)



用法参考:

