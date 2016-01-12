import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["uuid", "wave", "PyQt5.QtNetwork", "PyQt5.QtMultimedia"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "LearnMath",
        version = "0.1",
        description = "My Math application!",
        options = {"build_exe": build_exe_options},
		data_files = [("audio", ".\\qtaudio_windows.dll")],
        executables = [Executable("LearnMath.py", base=base)])