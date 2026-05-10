import sys
import traceback

try:
    print("正在导入模块...")
    import customtkinter as ctk
    print("✓ customtkinter 导入成功")
    
    from PIL import Image, ImageTk
    print("✓ PIL 导入成功")
    
    import requests
    print("✓ requests 导入成功")
    
    from deep_translator import GoogleTranslator
    print("✓ deep_translator 导入成功")
    
    print("\n正在启动程序...")
    import wallhaven_gui_fixed
    
    print("✓ 模块加载成功")
    print("\n启动GUI...")
    
    app = wallhaven_gui_fixed.WallhavenGUI()
    print("✓ GUI 初始化成功")
    
    app.run()
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    print("\n详细错误信息:")
    traceback.print_exc()
    input("\n按回车键退出...")
