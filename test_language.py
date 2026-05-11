"""
测试语言功能
"""
import json

# 读取配置文件
with open('wallhaven_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print("当前配置:")
print(json.dumps(config, indent=2, ensure_ascii=False))

# 检查语言设置
if 'language' in config:
    print(f"\n✅ 语言设置已添加: {config['language']}")
    if config['language'] == 'en':
        print("✅ 默认语言为英文 (en)")
    else:
        print(f"⚠️ 当前语言为: {config['language']}")
else:
    print("\n❌ 配置文件中缺少语言设置")

# 检查其他必要的设置
required_keys = ['appearance_mode', 'language']
for key in required_keys:
    if key in config:
        print(f"✅ {key}: {config[key]}")
    else:
        print(f"❌ 缺少 {key}")
