from cx_Freeze import setup, Executable

executables = [Executable('Snake.py',
               targetName='Snake.exe',
               base='Win32GUI',
               icon='icon.ico')]


includes = ['tkinter', 'random']

zip_include_packages = ['tkinter', 'random']

include_files = []

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='Snake',
      version='4.0',
      description='My masterpiece.',
      executables=executables,
      options=options)
