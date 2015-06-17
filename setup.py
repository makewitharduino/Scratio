# coding=utf-8

import sys
import json
import os
from cx_Freeze import setup, Executable

def getVersion():
    json_path = os.path.abspath("setting.json")
    f = open(json_path, 'r')
    jsonData = json.load(f)
    return jsonData['version']


name = "Scratio"
version = getVersion()
description = 'Arduino Extention for Scratch2.0 Offline Editor'
author = '@okiroyuki'
url ='http://okhiroyuki.github.io/Scratio/'

# 変更しない
upgrade_code = '{2648A2D6-AAFB-3E05-BC7A-2BC86636CDC9}'

# ----------------------------------------------------------------
# セットアップ
# ----------------------------------------------------------------
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Scratio",                    # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]\Scratio.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",              # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

build_exe_options = {"packages": ["os"],
                    "excludes": [],
                    "includes": [],
                    "include_files": ['setting.json','images/'],
                    "packages": [],
                    "compressed": True
}

bdist_msi_options = {'upgrade_code': upgrade_code,
                    'add_to_path': False,
                    'data': msi_data
}

bdist_mac_options = {"iconfile": 'images/icon.icns'}

options = {
    'build_exe': build_exe_options,
    'bdist_msi': bdist_msi_options,
    'bdist_mac': bdist_mac_options
}

# exeの情報
base = 'Win32GUI' if sys.platform == 'win32' else None
icon = 'images/icon_256x256.ico'

# exe にしたい python ファイルを指定
exe = Executable(script = 'scratio.py',
                 base = base,
                 icon = icon,
                 copyDependentFiles = True
                 )

# セットアップ
setup(name = name,
      version = version,
      author=author,
      url=url,
      description = description,
      options = options,
      executables = [exe]
      )
