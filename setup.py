# coding: utf-8
# cx_Freeze 用セットアップファイル

import sys
from cx_Freeze import setup, Executable

name = "S2A"
version = '0.3'
description = 'Arduino Extention for Scratch2.0 Offline Editor'
author = '@okiroyuki'
url = 'http://okhiroyuki.github.io/S2A/'

# 変更しない
upgrade_code = '{2648A2D6-AAFB-3E05-BC7A-2BC86636CDC9}'

# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------

build_exe_options = {"packages": ["os"]}
bdist_msi_options = {'upgrade_code': upgrade_code}

options = {
    'build_exe': build_exe_options,
    'bdist_msi': bdist_msi_options
}

# exeの情報
base = 'Win32GUI' if sys.platform == 'win32' else None
icon = 'images/app_icon.ico'

includefiles = ['json/','images/']
excludes = []
packages = []

# exe にしたい python ファイルを指定
exe = Executable(script = 's2a.py',
                 base = base,
                 icon = icon,
                 shortcutName="S2A",
                 shortcutDir="DesktopFolder",
                 tergetDir=TARGETDIR
                 )

# セットアップ
setup(name = name,
      version = version,
      author=author,
      url=url,
      description = description,
      options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
      executables = [exe]
      )
