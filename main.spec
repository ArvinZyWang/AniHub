# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 添加您的资源文件夹路径
added_files = [
    ('res', 'res'),  # 将res目录下的所有文件复制到打包结果的res目录下
    ('gui', 'gui'),  # 将gui目录下的所有文件复制到打包结果的gui目录下
    ('lib', 'lib'),  # 将lib目录下的所有文件复制到打包结果的lib目录下
    ('data', 'data') # 将data目录下的所有文件复制到打包结果的data目录下
]

a = Analysis(['main.py'],
             pathex=['D:\Python\Projects\Dmhy_Manager'],
             binaries=[],
             datas=added_files,
             hiddenimports=['lxml', 'pyperclip', 'requests'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='AniHub',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,  # 设置为False以隐藏控制台窗口
          icon='res/logo.ico', # 指定程序图标
          noarchive=True)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AniHub',
)
