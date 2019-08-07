# -*- mode: python -*-

block_cipher = None

a = Analysis(['sh2msg/__main__.py'],
             datas=[ ('./sh2msg/table/data/*.txt', './sh2msg/table/data/') ],
             pathex=['.'],
             binaries=[],
             hiddenimports=['sh2msg'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['./test/*'],
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
          name='sh2msg',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
