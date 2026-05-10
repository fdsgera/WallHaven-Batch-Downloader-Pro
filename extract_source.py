import sys
import os
import importlib.util

# 加载 .pyc 文件
spec = importlib.util.spec_from_file_location("wallhaven_gui", "wallhaven_gui.cpython-314.pyc")
module = importlib.util.module_from_spec(spec)

try:
    spec.loader.exec_module(module)
    
    # 尝试获取源代码
    import inspect
    
    # 获取所有类和函数
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            print(f"\n{'='*80}")
            print(f"Name: {name}")
            print(f"Type: {type(obj)}")
            try:
                source = inspect.getsource(obj)
                print(f"Source:\n{source}")
            except:
                print("Source not available")
                # 打印方法签名
                if inspect.isclass(obj):
                    print(f"Methods: {[m for m in dir(obj) if not m.startswith('_')]}")
                    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
