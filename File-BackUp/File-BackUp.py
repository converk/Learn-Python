import os 
import time
import tkinter

#函数主体
def BackUP():
    global enter_source_dir
    global enter_target_dir
    source_dir = enter_source_dir.get()  # get()函数读到该控件的文本框信息
    target_dir=enter_target_dir.gets()

    today_dir=target_dir+time.strftime('%Y%m%d')
    #os.sep：根据系统的不同，os.sep也不同，在Linux和Mac下（也可以说是Unix和类Unix系统中），
    #os.sep的值为'/'，而在Windows系统中，os.sep的值为'\'。
    zip_file=today_dir+os.sep+time.strftime('%H%M%S')+'.zip'

    zip_command="zip -qr "+zip_file+' '+source_dir

    if os.path.exists(today_dir)==0:
        os.mkdir(today_dir)
    if os.system(zip_command)==0:  #执行压缩命令,执行成功返回0;
        print("zip Successful!")
    else:
        print("error!!")


#Tk界面控件
root=tkinter.Tk()
root.title("BackUp")  
root.geometry("200x200")  #设定界面大小,不是*
#第一行的控件
lb1_source=tkinter.Label(root,text='Source')  #第一行文本
lb1_source.grid(row=0,column=0)
enter_source_dir=tkinter.Entry(root)   #第一行输入框控件
enter_source_dir.grid(row=0,column=1)
#第二行的控件
lb1_target = tkinter.Label(root, text='Target')  # 第二行文本
lb1_target.grid(row=1, column=0)
enter_target_dir = tkinter.Entry(root)  # 第二行输入框控件
enter_target_dir.grid(row=1, column=1)
#第三行控件,一个按钮
run_backup = tkinter.Button(root, text="BackUp")
run_backup.grid(row=3,column=0)
run_backup['command'] = BackUP  # 将命令绑定在backup()函数上，当点击这个按钮时，就调用指定的backup()函数
#界面开始
root.mainloop()
