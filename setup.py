from cx_Freeze import setup, Executable

executables = [
    Executable('__main__.py')
]

setup(name='YTCutter', version='1.0', description='YouTube audio cutting tool', executables=executables)