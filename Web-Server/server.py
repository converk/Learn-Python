import os,sys   #处理静态页面需要用到的
import subprocess  #调用cgi程序的时候用到
from http.server import BaseHTTPRequestHandler,HTTPServer


class ServerException(Exception):
    #服务器内部错误,交给Exception实现
    pass

#将所有文件的可能情况分开写成一个类
class root_url_file(object):   #当访问根url的时候,返回相应的界面 
    def home_path(self, requesthandler):
        return os.path.join(requesthandler.full_path,'home.html')

    def test(self,requesthandler):
        #要判断full_path是文件夹而不是一个文件,并且要确定,响应的是一个文件
        return os.path.isdir(requesthandler.full_path) and os.path.isfile(self.home_path(requesthandler))

    def act(self,requesthandler):
        requesthandler.handle_file(self.home_path(requesthandler))

class cgi_file(object): #利用cgi程序来显示到浏览器上

    def test(self,requesthandler):
        return os.path.isfile(requesthandler.full_path) and requesthandler.full_path.endswith('.py')

    def act(self,requesthandler):
        requesthandler.run_cgi(requesthandler.full_path)

class file_not_exist(object):   #文件不存在
    def test(self, requesthandler):  # 动态调用,requesthandle是RequestHandler的实例
        return not os.path.exists(requesthandler.full_path)

    def act(self,requesthandler):
        raise ServerException("'{0}' not found".format(requesthandler.path))

class file_is_exist(object):    #路径存在且为文件
    def test(self,requesthandler):
        return os.path.isfile(requesthandler.full_path)
    
    def act(self,requesthandler):
        requesthandler.handle_file(requesthandler.full_path)


class other_cases(object):     #路径存在但不是文件
    def test(self,requesthandler):
        return True

    def act(self,requesthandler):
        raise ServerException(
            "Unknown object '{0}'".format(requesthandler.full_path))


class RequestHandler(BaseHTTPRequestHandler):
    #这里是响应文本的模板,这里面的内容都是请求信息

    ErrorPage='''\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>

    '''
    # 三种可能的情况,当每次出现一个新情况的时候,只需要新写一个类,并且把它加到cases里面就行
    #不需要更改do_GET里面的源码
    #对于文件类型,先判断是不是可执行文件,再判断是不是一般文件
    cases = [root_url_file(),cgi_file(),file_not_exist(), file_is_exist(), other_cases()]  

    # 模块的 BaseHTTPRequestHandler 类会帮我们处理对请求的解析，
    # 并通过确定请求的方法来调用其对应的函数，比如方法是 GET ,该类就会调用名为 do_GET 的方法
    #RequestHandler 继承了 BaseHTTPRequestHandler 并重写了 do_GET 方法，
    # 其效果如代码所示是返回 Page 的内容。 
    # Content-Type 告诉了客户端要以处理html文件的方式处理返回的内容。
    # end_headers 方法会插入一个空白行
    def do_GET(self):    #将两个方法分开写,最后使用一个处理get请求的函数调用
        try:
            self.full_path=os.getcwd()+'/Web-Server'+self.path  #self.path保存了请求的相对路径

            for case in self.cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:   #捕获上面case出错时raise出来的错误
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content=reader.read()
            self.creat_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self,msg):
        content=self.ErrorPage.format(path=self.path,msg=msg)
        #转码为二进制,这样在creat_content里面就不用转码了,并且返回404状态吗
        self.creat_content(content.encode('utf-8'),404)    

    #处理请求的子进程
    def run_cgi(self,full_path):
        data=subprocess.check_output(['python3',full_path],shell=False)
        self.creat_content(data)

    def creat_content(self, page,status=200):  # 这个要按照HTTP请求的响应格式来写
        self.send_response(status)  # 响应状态码
        self.send_header('Content-type', "text/html")  # 两个header field name
        self.send_header('Content-Length', str(len(page)))
        self.end_headers()  # 一定要结束header field name的声明
        self.wfile.write(page)  # 这是最后的body文本部分,输出流

def start_server(port):  #port为端口号
    server=HTTPServer(('',int(port)),RequestHandler)   #函数接受的是字符串,要转换成数字
    server.serve_forever()   #持续监听端口,并一直接受请求

if __name__=='__main__':
    start_server(8080)
