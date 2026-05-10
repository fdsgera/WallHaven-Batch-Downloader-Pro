import sys
import importlib.util
import inspect

# 加载 .pyc 文件
spec = importlib.util.spec_from_file_location("wallhaven_gui", "wallhaven_gui.cpython-314.pyc")
module = importlib.util.module_from_spec(spec)

try:
    spec.loader.exec_module(module)
    
    # 重点关注 WallhavenGUI 和 WallhavenDownloader 类
    for class_name in ['WallhavenGUI', 'WallhavenDownloader']:
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            print(f"\n{'='*80}")
            print(f"Class: {class_name}")
            print(f"{'='*80}\n")
            
            # 获取所有方法和属性
            for name in dir(cls):
                if not name.startswith('_'):
                    attr = getattr(cls, name)
                    print(f"\n{'-'*60}")
                    print(f"Name: {name}")
                    print(f"Type: {type(attr)}")
                    
                    if callable(attr):
                        try:
                            sig = inspect.signature(attr)
                            print(f"Signature: {sig}")
                        except:
                            pass
                        
                        # 尝试获取字节码
                        try:
                            if hasattr(attr, '__code__'):
                                code = attr.__code__
                                print(f"Code info:")
                                print(f"  - Arguments: {code.co_varnames[:code.co_argcount]}")
                                print(f"  - Local vars: {code.co_varnames}")
                                print(f"  - Constants: {code.co_consts[:10]}")  # 只显示前10个
                        except Exception as e:
                            print(f"  - Cannot extract code: {e}")
                    
            # 尝试创建实例来查看初始化
            print(f"\n{'='*80}")
            print(f"Trying to inspect {class_name}.__init__")
            print(f"{'='*80}")
            try:
                init_method = cls.__init__
                if hasattr(init_method, '__code__'):
                    code = init_method.__code__
                    print(f"__init__ parameters: {code.co_varnames[:code.co_argcount]}")
                    print(f"__init__ constants: {code.co_consts[:20]}")
            except Exception as e:
                print(f"Error: {e}")
                
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
