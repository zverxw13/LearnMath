@echo off
echo Creating LearnMath.exe
echo ...
c:\Python34\python setup.py build
echo Copying necessary files
rem copy d:\Mirek\Priv\MyProjects\Utilities\MJ_Utils.py d:\Mirek\Priv\MyProjects\LearnMath\build\exe.win-amd64-3.4
xcopy d:\Mirek\Priv\MyProjects\LearnMath\ui_files d:\Mirek\Priv\MyProjects\LearnMath\build\exe.win-amd64-3.4\ui_files /s/I
xcopy d:\Mirek\Priv\MyProjects\LearnMath\resources d:\Mirek\Priv\MyProjects\LearnMath\build\exe.win-amd64-3.4\resources /s/I
xcopy c:\Python34\Lib\site-packages\PyQt5\plugins\audio d:\Mirek\Priv\MyProjects\LearnMath\build\exe.win-amd64-3.4\audio /s/I
echo ...
echo LearnMath.exe successfully created!