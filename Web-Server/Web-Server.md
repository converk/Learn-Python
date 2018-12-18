# Python3实现一个简易web服务器

## 了解HTTP

## 了解CGI与FastCGI

**CGI**是外部应用程序(CGI程序)与web服务器之间的接口,是在**CGI程序**和**Web服务器**之间传递信息的规程  
**CGI**让wb服务器执行外部程序,并把结果发送给**web浏览器**  
CGI就是一座桥,把把网页和web服务器中的执行程序连接起来  
CGI方式在遇到连接请求（用户请求）先要创建cgi的子进程，激活一个CGI进程，然后处理请求，处理完后结束这个子进程。这就是fork-and-execute模式。所以用cgi方式的服务器有多少连接请求就会有多少cgi子进程  
工作流程:

1. 浏览器通过HTML表单或超链接请求指向一个CGI应用程序的URL。
2. 服务器收发到请求。
3. 服务器执行所指定的CGI应用程序。
4. CGI应用程序执行所需要的操作，通常是基于浏览者输入的内容。
5. CGI应用程序把结果格式化为网络服务器和浏览器能够理解的文档（通常是HTML网页）。
6. 网络服务器把结果返回到浏览器中。

**FastCGI**是一个可伸缩地、高速地在HTTP server和动态脚本语言间通信的接口
FastCGI是从CGI发展改进而来的。传统CGI接口方式的主要缺点是性能很差，因为每次HTTP服务器遇到动态程序时都需要重新启动脚本解析器来执行解析，然后结果被返回给HTTP服务器。这在处理高并发访问时，几乎是不可用的。FastCGI像是一个常驻(long-live)型的CGI，它可以一直执行着，只要激活后，不会每次都要花费时间去fork一次(这是CGI最为人诟病的fork-and-execute 模式)。CGI 就是所谓的短生存期应用程序，FastCGI 就是所谓的长生存期应用程序。由于 FastCGI 程序并不需要不断的产生新进程，可以大大降低服务器的压力并且产生较高的应用效率

FastCGI是语言无关的、可伸缩架构的CGI开放扩展，其主要行为是将CGI解释器进程保持在内存中并因此获得较高的性能。众所周知，CGI解释器的反复加载是CGI性能低下的主要原因，如果CGI解释器保持在内存中并接受FastCGI进程管理器调度，则可以提供良好的性能、伸缩性、Fail-Over特性等等。FastCGI接口方式采用C/S结构，可以将HTTP服务器和脚本解析服务器分开，同时在脚本解析服务器上启动一个或者多个脚本解析守护进程。当HTTP服务器每次遇到动态程序时，可以将其直接交付给FastCGI进程来执行，然后将得到的结果返回给浏览器。这种方式可以让HTTP服务器专一地处理静态请求或者将动态脚本服务器的结果返回给客户端，这在很大程度上提高了整个应用系统的性能。

FastCGI的工作流程:

Web Server启动时载入FastCGI进程管理器（PHP-CGI或者PHP-FPM或者spawn-cgi)
FastCGI进程管理器自身初始化，启动多个CGI解释器进程(可见多个php-cgi)并等待来自Web Server的连接。
当客户端请求到达Web Server时，FastCGI进程管理器选择并连接到一个CGI解释器。Web server将CGI环境变量和标准输入发送到FastCGI子进程php-cgi。
FastCGI子进程完成处理后将标准输出和错误信息从同一连接返回Web Server。当FastCGI子进程关闭连接时，请求便告处理完成。FastCGI子进程接着等待并处理来自FastCGI进程管理器(运行在Web Server中)的下一个连接。 在CGI模式中，php-cgi在此便退出。

## 步骤

1. 等待某个人连接我们的服务器并向我们发送一个HTTP请求
2. 解析该请求
3. 了解该请求希望请求的内容
4. 服务器根据请求抓取需要的数据（从服务器本地文件中读取或者程序动态生成）
5. 将数据格式化为请求需要的格式
6. 返回HTTP响应

对于步骤1,2,6,对于所有的web应用都是一样的,这部分内容Python标准库中的 `BaseHTTPServer` 模块可以帮助我们处理

## BaseHTTPServer模块

`BaseHTTPServer`：提供基本的Web服务和处理器类，分别是HTTPServer及BaseHTTPRequestHandler；

### BaseHTTPRequestHandler

`BaseHTTPRequestHandler`在HTTP请求到达时进行处理，但其自身并不能对请求作出相应，由另一个**派生类**来处理每一个请求方法。`BaseHTTPRequestHandler`为子集提供许多类**变量、实例变量和方法**，其分析请求对象和请求头部，并根据请求类型调用相应的方法。一般这个模块不被直接使用，而是被用来作为构建功能性Web服务器的一个`基类`。

#### 一些常用的方法和属性

```.py
BaseHTTPRequestHandler.path                    #包含的请求路径和GET请求的数据
BaseHTTPRequestHandler.command                 #请求类型GET、POST...
BaseHTTPRequestHandler.client_address          #为客户端的主机地址和端口号
BaseHTTPRequestHandler.date_time_string()      #请求发送时间
BaseHTTPRequestHandler.request_version         #请求的协议类型HTTP/1.0、HTTP/1.1
BaseHTTPRequestHandler.headers                 #请求的头
BaseHTTPRequestHandler.responses               #HTTP错误代码及对应错误信息的字典
BaseHTTPRequestHandler.handle()                #用于处理某一连接对象的请求，调用handle_one_request方法处理
BaseHTTPRequestHandler.handle_one_request()    #根据请求类型调用do_XXX()方法，XXX为请求类型
BaseHTTPRequestHandler.do_XXX()                #处理请求
BaseHTTPRequestHandler.send_error()            #发送并记录一个完整的错误回复到客户端,内部调用send_response()方法实现
BaseHTTPRequestHandler.send_response()         #发送一个响应头并记录已接收的请求
BaseHTTPRequestHandler.send_header()           #发送一个指定的HTTP头到输出流。 keyword 应该指定头关键字，value 指定它的值
BaseHTTPRequestHandler.end_headers()           #发送一个空白行，标识发送HTTP头部结束
BaseHTTPRequestHandler.wfile    #self.connection.makefile('rb', self.wbufsize) self.wbufsize = -1 应答的HTTP文本流对象，可写入应答信息
BaseHTTPRequestHandler.rfile    #self.connection.makefile('wb', self.rbufsize) self.rbufsize = 0  请求的HTTP文本流对象，可读取请求信息
```

## 处理静态页面

处理静态页面就是根据请求的页面名得到磁盘上的页面文件并返回  
没有找到相应的文件返回`error`界面也是在这里完成