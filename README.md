# pythonDemo

Python演练项目

# 1.python如何打包成可执行程序
	安装PyInstaller:pip install pyinstaller
# 2.使用PyInstaller打包Python脚本:
    此方法打包会有命令行窗口
	pyinstaller --onefile Pic.py
    
    此方法打包不显示命令行窗口
    这里的-F参数表示生成单个打包文件，-w参数表示不显示控制台窗口。
    pyinstaller -F -w openVideoWeb.py
# 3.