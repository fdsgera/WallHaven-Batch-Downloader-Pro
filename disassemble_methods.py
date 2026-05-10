import sys
import importlib.util
import dis

# 加载 .pyc 文件
spec = importlib.util.spec_from_file_location("wallhaven_gui", "wallhaven_gui.cpython-314.pyc")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# 获取关键方法的字节码
WallhavenGUI = module.WallhavenGUI
WallhavenDownloader = module.WallhavenDownloader

print("="*80)
print("WallhavenGUI.show_current_image 字节码:")
print("="*80)
dis.dis(WallhavenGUI.show_current_image)

print("\n" + "="*80)
print("WallhavenDownloader.start 字节码:")
print("="*80)
dis.dis(WallhavenDownloader.start)

print("\n" + "="*80)
print("WallhavenGUI.start_download 字节码:")
print("="*80)
dis.dis(WallhavenGUI.start_download)
