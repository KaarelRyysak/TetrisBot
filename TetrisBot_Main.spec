# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['TetrisBot_main.py'],
             pathex=['D:\\tetrisBot'],
             binaries=[],
             datas=[('red.png', '.'), ('green.png', '.'), ('yellow.png', '.'), ('orange.png', '.'), ('teal.png', '.'), ('purple.png', '.'), ('blue.png', '.'), ('hold.png', '.'), ('next.png', '.'), ('play.png', '.'), ('mudel.h5', '.')],
             hiddenimports=[],
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
          [],
          name='TetrisBot_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
