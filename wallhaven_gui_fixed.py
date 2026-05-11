"""
WallHaven 批量下载器 - 修复版
修复了下载日志和图片预览不同步的问题
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
import json
import threading
import time
from pathlib import Path
from deep_translator import GoogleTranslator
import re
import sys


# 语言字典
LANGUAGES = {
    'en': {
        'title': '🖼️ Wallhaven Batch Downloader',
        'settings': '⚙️ Settings',
        'keyword': 'Search Keyword:',
        'keyword_placeholder': 'e.g.: anime, landscape',
        'count': 'Download Count:',
        'count_placeholder': 'e.g.: 100',
        'save_path': 'Save Location:',
        'browse': 'Browse',
        'category': 'Categories:',
        'general': 'General',
        'anime': 'Anime',
        'people': 'People',
        'purity': 'Content Rating:',
        'sfw': 'SFW',
        'sketchy': 'Sketchy',
        'nsfw': 'NSFW',
        'api_key': 'API Key (Optional):',
        'api_key_placeholder': 'For NSFW content',
        'save_config': '💾 Save Config',
        'start_download': '🚀 Start Download',
        'stop_download': '⏸️ Stop Download',
        'download_log': '📋 Download Log',
        'image_preview': '🖼️ Image Preview',
        'waiting': 'Waiting for download...',
        'prev': '⬅️ Previous',
        'refresh': '🔄 Refresh',
        'next': 'Next ➡️',
        'autoplay': '▶️ Auto Play',
        'stop_autoplay': '⏸️ Stop Auto',
        'settings_title': '⚙️ Settings',
        'display': 'Display',
        'appearance': 'Appearance Mode:',
        'light_mode': 'Light Mode',
        'dark_mode': 'Dark Mode',
        'system_mode': 'Follow System',
        'language': 'Language:',
        'apply': 'Apply',
        'close': 'Close',
        'error': 'Error',
        'warning': 'Warning',
        'success': 'Success',
        'config_saved': '💾 Configuration saved!',
        'enter_keyword': 'Please enter search keyword!',
        'invalid_count': 'Please enter valid download count (positive integer)!',
        'select_path': 'Please select save location!',
        'select_category': 'Please select at least one category!',
        'select_purity': 'Please select at least one content rating!',
        'nsfw_need_key': 'Accessing NSFW content requires API Key!\n\nVisit wallhaven.cc to register and get API Key.',
        'previewing': 'Previewing: Image',
        'loading': 'Loading...',
        'load_failed': 'Load failed:',
        'theme_switched': '✅ Switched to {} mode',
        'theme_failed': '❌ Theme switch failed:',
        'language_switched': '✅ Language switched to {}',
    },
    'zh': {
        'title': '🖼️ Wallhaven 批量下载器',
        'settings': '⚙️ 设置',
        'keyword': '搜索关键词:',
        'keyword_placeholder': '例如: anime, landscape',
        'count': '下载数量:',
        'count_placeholder': '例如: 100',
        'save_path': '保存位置:',
        'browse': '浏览',
        'category': '图片分类:',
        'general': '常规',
        'anime': '动漫',
        'people': '人物',
        'purity': '内容分级:',
        'sfw': '安全',
        'sketchy': '擦边',
        'nsfw': '限制',
        'api_key': 'API Key (可选):',
        'api_key_placeholder': '用于访问 NSFW 内容',
        'save_config': '💾 保存配置',
        'start_download': '🚀 开始下载',
        'stop_download': '⏸️ 停止下载',
        'download_log': '📋 下载日志',
        'image_preview': '🖼️ 图片预览',
        'waiting': '等待下载开始...',
        'prev': '⬅️ 上一张',
        'refresh': '🔄 刷新',
        'next': '下一张 ➡️',
        'autoplay': '▶️ 自动播放',
        'stop_autoplay': '⏸️ 停止自动',
        'settings_title': '⚙️ 设置',
        'display': '显示',
        'appearance': '外观模式:',
        'light_mode': '浅色模式',
        'dark_mode': '深色模式',
        'system_mode': '跟随系统',
        'language': '语言:',
        'apply': '应用',
        'close': '关闭',
        'error': '错误',
        'warning': '警告',
        'success': '成功',
        'config_saved': '💾 配置已保存！',
        'enter_keyword': '请输入搜索关键词！',
        'invalid_count': '请输入有效的下载数量（正整数）！',
        'select_path': '请选择保存位置！',
        'select_category': '请至少选择一个图片分类！',
        'select_purity': '请至少选择一个内容分级！',
        'nsfw_need_key': '访问限制级 (NSFW) 内容需要提供 API Key！\n\n访问 wallhaven.cc 注册账号并获取 API Key。',
        'previewing': '正在预览：第',
        'loading': '加载中...',
        'load_failed': '加载失败:',
        'theme_switched': '✅ 已切换到{}模式',
        'theme_failed': '❌ 切换主题失败:',
        'language_switched': '✅ 语言已切换为{}',
    }
}


# 语言配置字典
LANGUAGES = {
    'en': {
        'title': 'Wallhaven Batch Downloader',
        'settings': 'Settings',
        'keyword': 'Search Keyword:',
        'keyword_placeholder': 'e.g.: anime, landscape',
        'count': 'Download Count:',
        'count_placeholder': 'e.g.: 100',
        'save_path': 'Save Location:',
        'browse': 'Browse',
        'category': 'Image Category:',
        'category_general': 'General',
        'category_anime': 'Anime',
        'category_people': 'People',
        'purity': 'Content Rating:',
        'purity_sfw': 'SFW',
        'purity_sketchy': 'Sketchy',
        'purity_nsfw': 'NSFW',
        'api_key': 'API Key (Optional):',
        'api_key_placeholder': 'For NSFW content access',
        'save_config': '💾 Save Config',
        'start_download': '🚀 Start Download',
        'stop_download': '⏸️ Stop Download',
        'download_log': '📋 Download Log',
        'image_preview': '🖼️ Image Preview',
        'waiting': 'Waiting for download to start...',
        'waiting_metadata': 'Waiting for metadata collection...',
        'previous': '⬅️ Previous',
        'refresh': '🔄 Refresh',
        'next': 'Next ➡️',
        'settings_title': '⚙️ Settings',
        'display': 'Display',
        'appearance_mode': 'Appearance Mode:',
        'light_mode': 'Light Mode',
        'dark_mode': 'Dark Mode',
        'system_mode': 'Follow System',
        'language': 'Language:',
        'language_english': 'English',
        'language_chinese': '简体中文',
        'apply': 'Apply',
        'close': 'Close',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'error_keyword': 'Please enter a search keyword!',
        'error_count': 'Please enter a valid download count (positive integer)!',
        'error_path': 'Please select a save location!',
        'error_category': 'Please select at least one image category!',
        'error_purity': 'Please select at least one content rating!',
        'warning_nsfw': 'Accessing NSFW content requires an API Key!\n\nVisit wallhaven.cc to register and get your API Key.',
        'config_saved': '💾 Configuration saved!',
        'theme_changed': '✅ Switched to {mode} mode',
        'language_changed': '✅ Language changed to {lang}',
        'loading_config': '📂 Loading last saved configuration...',
        'preview_enabled': '✅ Preview feature enabled!',
        'previewing': 'Previewing: Image {index}/{total}',
        'loading_preview': 'Loading... ({index}/{total})',
        'load_failed': 'Load failed: {error}',
        'autoplay': '▶️ Auto Play',
        'stop_autoplay': '⏸️ Stop Auto',
        'debug_mode': 'Debug Mode',
        'debug_enabled': '✅ Debug mode enabled',
        'debug_disabled': '✅ Debug mode disabled',
        'age_confirm_title': 'Age Confirmation',
        'age_confirm_message': 'I confirm that I am 18 years or older',
        'age_confirm_button': 'Confirm and Enter',
        'view_disclaimer': '📜 View Disclaimer',
        'disclaimer_title': '⚠️ Disclaimer',
        'disclaimer_content': """### ⚠️ Disclaimer

【English Version】

1. Copyright Notice: This project is developed solely as an educational and utility tool. All downloaded images are the copyrighted property of their respective creators and Wallhaven.cc. Users must strictly adhere to copyright laws. Commercial use of images downloaded via this software is strictly prohibited.

2. Account & Network Risks: While request throttling is implemented, excessive high-frequency batch downloading may still trigger Wallhaven's anti-bot mechanisms, potentially resulting in IP or account bans. The developer assumes no responsibility for any bans or restrictions caused by the misuse of this software.

3. Content Warning: Access to certain rated content (e.g., NSFW) requires the user's personal API key. Users are solely responsible for ensuring their usage complies with their local laws and regulations, and confirm they are of legal age to access such content.

4. "As-Is" Software: This software is provided "as is" and free of charge. The developer provides no warranties regarding permanent availability, failures due to third-party API changes, or any potential data loss incurred during usage.

---

【中文版】

1. 版权声明：本项目仅作为技术交流与辅助工具开发。所有下载的图片版权均归原作者及 Wallhaven.cc 所有。请用户严格遵守相关版权法规，严禁将使用本软件下载的图像用于任何商业用途。

2. 账号与网络风险：尽管本软件内置了限流机制，但极高频率的批量请求仍可能触发 Wallhaven 的反爬虫机制，导致您的 IP 地址或账号被封禁。由于滥用本软件造成的任何封禁或网络限制，开发者概不负责。

3. 内容警告：软件涉及的特定分级内容（如 NSFW）需用户自行提供 API 密钥方可访问。用户必须确保其行为完全符合所在国家/地区的法律法规，并承诺已达到访问此类内容的法定年龄。

4. 按"原样"提供：本软件按"原样"免费提供。开发者不对软件的永久可用性、第三方接口变动造成的失效、或使用过程中可能发生的数据丢失承担任何连带法律责任。""",
    },
    'zh': {
        'title': 'Wallhaven 壁纸下载器',
        'settings': '⚙️ 设置',
        'keyword': '搜索关键词:',
        'keyword_placeholder': '例如: anime, landscape',
        'count': '下载数量:',
        'count_placeholder': '例如: 100',
        'save_path': '保存位置:',
        'browse': '浏览',
        'category': '图片分类:',
        'category_general': '常规',
        'category_anime': '动漫',
        'category_people': '人物',
        'purity': '内容分级:',
        'purity_sfw': '安全',
        'purity_sketchy': '擦边',
        'purity_nsfw': '限制',
        'api_key': 'API Key (可选):',
        'api_key_placeholder': '用于访问 NSFW 内容',
        'save_config': '💾 保存配置',
        'start_download': '🚀 开始下载',
        'stop_download': '⏸️ 停止下载',
        'download_log': '📋 下载日志',
        'image_preview': '🖼️ 图片预览',
        'waiting': '等待下载开始...',
        'waiting_metadata': '等待元数据收集...',
        'previous': '⬅️ 上一张',
        'refresh': '🔄 刷新',
        'next': '下一张 ➡️',
        'settings_title': '⚙️ 设置',
        'display': '显示',
        'appearance_mode': '外观模式:',
        'light_mode': '浅色模式',
        'dark_mode': '深色模式',
        'system_mode': '跟随系统',
        'language': '语言:',
        'language_english': 'English',
        'language_chinese': '简体中文',
        'apply': '应用',
        'close': '关闭',
        'error': '错误',
        'success': '成功',
        'warning': '警告',
        'error_keyword': '请输入搜索关键词！',
        'error_count': '请输入有效的下载数量（正整数）！',
        'error_path': '请选择保存位置！',
        'error_category': '请至少选择一个图片分类！',
        'error_purity': '请至少选择一个内容分级！',
        'warning_nsfw': '访问限制级 (NSFW) 内容需要提供 API Key！\n\n访问 wallhaven.cc 注册账号并获取 API Key。',
        'config_saved': '💾 配置已保存！',
        'theme_changed': '✅ 已切换到{mode}模式',
        'language_changed': '✅ 语言已切换为{lang}',
        'loading_config': '📂 加载上次保存的配置...',
        'preview_enabled': '✅ 预览功能已启用！',
        'previewing': '正在预览：第 {index}/{total} 张',
        'loading_preview': '加载中... ({index}/{total})',
        'load_failed': '加载失败: {error}',
        'autoplay': '▶️ 自动播放',
        'stop_autoplay': '⏸️ 停止自动',
        'debug_mode': '调试模式',
        'debug_enabled': '✅ 调试模式已开启',
        'debug_disabled': '✅ 调试模式已关闭',
        'age_confirm_title': '年龄确认',
        'age_confirm_message': '我保证我已满18岁',
        'age_confirm_button': '确定进入',
        'view_disclaimer': '📜 查看免责声明',
        'disclaimer_title': '⚠️ 免责声明',
        'disclaimer_content': """### ⚠️ 免责声明 / Disclaimer

【中文版】

1. 版权声明：本项目仅作为技术交流与辅助工具开发。所有下载的图片版权均归原作者及 Wallhaven.cc 所有。请用户严格遵守相关版权法规，严禁将使用本软件下载的图像用于任何商业用途。

2. 账号与网络风险：尽管本软件内置了限流机制，但极高频率的批量请求仍可能触发 Wallhaven 的反爬虫机制，导致您的 IP 地址或账号被封禁。由于滥用本软件造成的任何封禁或网络限制，开发者概不负责。

3. 内容警告：软件涉及的特定分级内容（如 NSFW）需用户自行提供 API 密钥方可访问。用户必须确保其行为完全符合所在国家/地区的法律法规，并承诺已达到访问此类内容的法定年龄。

4. 按"原样"提供：本软件按"原样"免费提供。开发者不对软件的永久可用性、第三方接口变动造成的失效、或使用过程中可能发生的数据丢失承担任何连带法律责任。

---

【English Version】

1. Copyright Notice: This project is developed solely as an educational and utility tool. All downloaded images are the copyrighted property of their respective creators and Wallhaven.cc. Users must strictly adhere to copyright laws. Commercial use of images downloaded via this software is strictly prohibited.

2. Account & Network Risks: While request throttling is implemented, excessive high-frequency batch downloading may still trigger Wallhaven's anti-bot mechanisms, potentially resulting in IP or account bans. The developer assumes no responsibility for any bans or restrictions caused by the misuse of this software.

3. Content Warning: Access to certain rated content (e.g., NSFW) requires the user's personal API key. Users are solely responsible for ensuring their usage complies with their local laws and regulations, and confirm they are of legal age to access such content.

4. "As-Is" Software: This software is provided "as is" and free of charge. The developer provides no warranties regarding permanent availability, failures due to third-party API changes, or any potential data loss incurred during usage.""",
    }
}


class ConfigManager:
    """配置管理器"""
    CONFIG_FILE = "wallhaven_config.json"
    
    @staticmethod
    def save_config(config_data):
        """保存配置到文件"""
        with open(ConfigManager.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    @staticmethod
    def load_config():
        """从文件加载配置"""
        if os.path.exists(ConfigManager.CONFIG_FILE):
            try:
                with open(ConfigManager.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    @staticmethod
    def add_search_history(keyword):
        """添加搜索历史（保留最近3条）"""
        config = ConfigManager.load_config()
        history = config.get('search_history', [])
        
        # 移除重复项
        if keyword in history:
            history.remove(keyword)
        
        # 添加到开头
        history.insert(0, keyword)
        
        # 只保留最近3条
        config['search_history'] = history[:3]
        
        ConfigManager.save_config(config)
    
    @staticmethod
    def get_search_history():
        """获取搜索历史"""
        config = ConfigManager.load_config()
        return config.get('search_history', [])


class WallhavenDownloader:
    """Wallhaven 下载器核心类"""
    
    # 专有名词字典（不翻译）
    PROPER_NOUNS = {
        # 游戏名称
        '原神': 'genshin impact',
        '崩坏星穹铁道': 'honkai star rail',
        '星穹铁道': 'honkai star rail',
        
        # 原神角色 - 蒙德
        '琴': 'jean genshin',
        '丽莎': 'lisa genshin',
        '芭芭拉': 'barbara genshin',
        '迪卢克': 'diluc',
        '雷泽': 'razor genshin',
        '温迪': 'venti',
        '可莉': 'klee',
        '班尼特': 'bennett',
        '诺艾尔': 'noelle',
        '菲谢尔': 'fischl',
        '砂糖': 'sucrose',
        '莫娜': 'mona',
        '迪奥娜': 'diona',
        '阿贝多': 'albedo',
        '罗莎莉亚': 'rosaria',
        '优菈': 'eula',
        '米卡': 'mika genshin',
        
        # 原神角色 - 璃月
        '凝光': 'ningguang',
        '香菱': 'xiangling',
        '北斗': 'beidou',
        '行秋': 'xingqiu',
        '魈': 'xiao',
        '重云': 'chongyun',
        '七七': 'qiqi',
        '刻晴': 'keqing',
        '钟离': 'zhongli',
        '辛焱': 'xinyan',
        '甘雨': 'ganyu',
        '胡桃': 'hu tao',
        '烟绯': 'yanfei',
        '云堇': 'yun jin',
        '申鹤': 'shenhe',
        '夜兰': 'yelan',
        '瑶瑶': 'yaoyao',
        '闲云': 'xianyun',
        '嘉明': 'gaming',
        
        # 原神角色 - 稻妻
        '枫原万叶': 'kaedehara kazuha',
        '万叶': 'kazuha',
        '神里绫华': 'kamisato ayaka',
        '绫华': 'ayaka',
        '宵宫': 'yoimiya',
        '早柚': 'sayu',
        '雷电将军': 'raiden shogun',
        '雷神': 'raiden shogun',
        '珊瑚宫心海': 'sangonomiya kokomi',
        '心海': 'kokomi',
        '托马': 'thoma',
        '五郎': 'gorou',
        '荒瀧一斗': 'arataki itto',
        '一斗': 'itto',
        '八重神子': 'yae miko',
        '神子': 'yae miko',
        '鹿野院平藏': 'shikanoin heizou',
        '平藏': 'heizou',
        '神里绫人': 'kamisato ayato',
        '绫人': 'ayato',
        '久岐忍': 'kuki shinobu',
        '忍': 'shinobu',
        '绮良良': 'kirara',
        '千织': 'chiori',
        
        # 原神角色 - 须弥
        '提纳里': 'tighnari',
        '柯莱': 'collei',
        '多莉': 'dori',
        '赛诺': 'cyno',
        '妮露': 'nilou',
        '纳西妲': 'nahida',
        '莱依拉': 'layla',
        '流浪者': 'wanderer',
        '散兵': 'scaramouche',
        '国崩': 'wanderer',
        '珐露珊': 'faruzan',
        '艾尔海森': 'alhaitham',
        '海森': 'alhaitham',
        '迪希雅': 'dehya',
        '卡维': 'kaveh',
        '白术': 'baizhu',
        '坎蒂丝': 'candace',
        '瑟提': 'sethos',
        
        # 原神角色 - 枫丹
        '琳妮特': 'lynette',
        '林尼': 'lyney',
        '菲米尼': 'freminet',
        '那维莱特': 'neuvillette',
        '莱欧斯利': 'wriothesley',
        '芙宁娜': 'furina',
        '夏洛蒂': 'charlotte',
        '娜维娅': 'navia',
        '夏沃蕾': 'chevreuse',
        '克洛琳德': 'clorinde',
        '阿蕾奇诺': 'arlecchino',
        '希格雯': 'sigewinne',
        '艾梅莉埃': 'emilie',
        
        # 原神角色 - 至冬
        '达达利亚': 'tartaglia',
        '公子': 'childe',
        
        # 原神角色 - 其他
        '旅行者': 'traveler',
        '空': 'aether',
        '荧': 'lumine',
        '安柏': 'amber',
        '凯亚': 'kaeya',
        
        # 崩坏星穹铁道角色 - 5星
        '姬子': 'himeko star rail',
        '瓦尔特': 'welt',
        '布洛妮娅': 'bronya',
        '杰帕德': 'gepard',
        '克拉拉': 'clara',
        '彦卿': 'yanqing',
        '白露': 'bailu',
        '卡芙卡': 'kafka',
        '刃': 'blade star rail',
        '丹恒·饮月': 'dan heng imbibitor lunae',
        '饮月': 'imbibitor lunae',
        '景元': 'jing yuan',
        '罗刹': 'luocha',
        '银狼': 'silver wolf',
        '符玄': 'fu xuan',
        '玲可': 'lynx',
        '托帕': 'topaz',
        '藏宝': 'numby',
        '托帕&账账': 'topaz and numby',
        '镜流': 'jingliu',
        '阮·梅': 'ruan mei',
        '真理医生': 'dr ratio',
        '雪衣': 'xueyi',
        '砂金': 'aventurine',
        '黑天鹅': 'black swan',
        '花火': 'sparkle',
        '加拉赫': 'gallagher',
        '知更鸟': 'robin',
        '波提欧': 'boothill',
        '流萤': 'firefly',
        '翡翠': 'jade',
        '云璃': 'yunli',
        '椒丘': 'jiaoqiu',
        '飞霄': 'feixiao',
        '灵砂': 'lingsha',
        '莫泽': 'moze',
        '三月七·巡猎': 'march 7th hunt',
        '阿兰': 'arlan',
        '星': 'trailblazer',
        '穹': 'trailblazer',
        '开拓者': 'trailblazer',
        
        # 崩坏星穹铁道角色 - 4星
        '三月七': 'march 7th',
        '丹恒': 'dan heng',
        '艾丝妲': 'asta',
        '黑塔': 'herta',
        '希儿': 'seele',
        '虎克': 'hook',
        '娜塔莎': 'natasha',
        '佩拉': 'pela',
        '桑博': 'sampo',
        '希露瓦': 'serval',
        '停云': 'tingyun',
        '素裳': 'sushang',
        '卢卡': 'luka',
        '青雀': 'qingque',
        '银枝': 'argenti',
        '寒鸦': 'hanya',
        '米沙': 'misha',
        '桂乃芬': 'guinaifen',
        
        # 蔚蓝档案角色
        '蔚蓝档案': 'blue archive',
        # 阿拜多斯
        '小鸟游星野': 'takanashi hoshino',
        '星野': 'hoshino blue archive',
        '白洲梓': 'shirasu azusa',
        '梓': 'azusa blue archive',
        '黑见芹香': 'kuromi serika',
        '芹香': 'serika',
        '奥空绫音': 'okusora ayane',
        '绫音': 'ayane blue archive',
        '十六夜野宫': 'izayoi nonomi',
        '野宫': 'nonomi',
        # 格黑娜
        '阿慈谷日富美': 'ajitani hifumi',
        '日富美': 'hifumi',
        '伊落玛丽': 'igusa mari',
        '玛丽': 'mari blue archive',
        '伊草遥香': 'ikuta haruka',
        '遥香': 'haruka blue archive',
        '火宫千夏': 'hinomiya chinatsu',
        '千夏': 'chinatsu',
        '阿库': 'aru',
        '陆八魔亚瑠': 'rikuhachima aru',
        '春原心奈': 'sunohara kokona',
        '心奈': 'kokona',
        '和泉元': 'izumi noa',
        '元': 'noa blue archive',
        '羽川莲见': 'hanekawa hasumi',
        '莲见': 'hasumi',
        '才羽桃井': 'saiba momoi',
        '桃井': 'momoi',
        '才羽绿': 'saiba midori',
        '绿': 'midori blue archive',
        '飞鸟马时': 'asuma toki',
        '时': 'toki',
        '伊原木好美': 'ibaraki ibuki',
        '好美': 'ibuki',
        '下江小春': 'shimoe koharu',
        '小春': 'koharu',
        # 千年
        '天童爱丽丝': 'tendou alice',
        '爱丽丝': 'alice blue archive',
        '圣园未花': 'misono mika',
        '未花': 'mika blue archive',
        '久田泉': 'hisada izumi',
        '泉': 'izumi blue archive',
        '药子': 'yakumo',
        '鬼方佳世子': 'onigata kayoko',
        '佳世子': 'kayoko',
        '各务千寻': 'kakudate chihiro',
        '千寻': 'chihiro',
        '室笠朱音': 'murokasa akane',
        '朱音': 'akane blue archive',
        '早濑优香': 'hayase yuuka',
        '优香': 'yuuka',
        '和乐': 'wakamo',
        '狐坂和乐': 'kitsune wakamo',
        '丰见小玉': 'toyomi kotama',
        '小玉': 'kotama',
        '久田伊织': 'hisada iori',
        '伊织': 'iori',
        '空崎日奈': 'sorasaki hina',
        '日奈': 'hina',
        '柚鸟': 'yuzu',
        '花冈柚子': 'hanaoka yuzu',
        # 三一
        '栗村爱莉': 'kurimura airi',
        '爱莉': 'airi',
        '羽沼真理': 'hanuma mari',
        '真理': 'mari trinity',
        '桐藤渚': 'kiritou nagisa',
        '渚': 'nagisa',
        '剑先鹤': 'kenzaki tsurugi',
        '鹤': 'tsurugi',
        '下仓梅': 'shimokura megu',
        '梅': 'megu',
        '美甘尼禄': 'mikamo neru',
        '尼禄': 'neru',
        '桐生枫': 'kiryuu kaede',
        '枫': 'kaede blue archive',
        '白石心': 'shiraishi kokoro',
        '心': 'kokoro',
        '天雨亚子': 'amau ako',
        '亚子': 'ako',
        '生盐诺亚': 'ikushio noa',
        '诺亚': 'noa trinity',
        '圣娅': 'seia',
        # 山海经
        '陆八魔爱露': 'rikuhachima aru',
        '爱露': 'aru',
        '春日椿': 'kasuga tsubaki',
        '椿': 'tsubaki',
        '伊吹': 'ibuki',
        '宇泽瑠美': 'uze rumi',
        '瑠美': 'rumi',
        '狮子堂泉奈': 'shishidou izuna',
        '泉奈': 'izuna',
        '美游': 'miyu',
        '花冈柚子': 'hanaoka yuzu',
        '柚子': 'yuzu',
        # 其他
        '阿罗娜': 'arona',
        '普拉娜': 'plana',
        '老师': 'sensei blue archive',
        
        # 明日方舟角色
        '明日方舟': 'arknights',
        # 6星干员
        '阿米娅': 'amiya',
        '银灰': 'silverash',
        '艾雅法拉': 'eyjafjalla',
        '伊芙利特': 'ifrit',
        '闪灵': 'shining',
        '夜莺': 'nightingale',
        '星熊': 'hoshiguma',
        '塞雷娅': 'saria',
        '能天使': 'exusiai',
        '推进之王': 'siege',
        '陈': 'chen',
        '赫拉格': 'hellagur',
        '麦哲伦': 'magallan',
        '莫斯提马': 'mostima',
        '布洛卡': 'blaze',
        '煌': 'aak',
        '年': 'nian',
        '刻俄柏': 'ceobe',
        '巴格派普': 'bagpipe',
        '森蚺': 'eunectes',
        '泥岩': 'mudrock',
        '瑕光': 'blemishine',
        '铃兰': 'suzuran',
        'W': 'w arknights',
        '温蒂': 'weedy',
        '史尔特尔': 'surtr',
        '山': 'mountain',
        '卡涅利安': 'carnelian',
        '帕拉斯': 'pallas',
        '灰烬': 'ash',
        '凯尔希': 'kal\'tsit',
        '歌蕾蒂娅': 'gladiia',
        '斯卡蒂': 'skadi',
        '浊心斯卡蒂': 'skadi alter',
        '陈·星': 'chen alter',
        '焰影苇草': 'saileach',
        '耀骑士临光': 'nearl alter',
        '号角': 'horn',
        '菲亚梅塔': 'fiammetta',
        '伊内丝': 'irene',
        '多萝西': 'dorothy',
        '琴柳': 'chongyue',
        '玲': 'ling',
        '李': 'lee',
        '焰尾': 'flametail',
        '空弦': 'archetto',
        '水月': 'mizuki',
        '帕拉斯': 'pallas',
        '灰烬': 'ash',
        '提丰': 'typhon',
        '霍恩洛厄': 'hoederer',
        '阿斯卡纶': 'ascalon',
        '缪尔赛思': 'muelsyse',
        '仇白': 'qiubai',
        '归溟幽灵鲨': 'specter alter',
        '黄金船': 'goldenglow',
        '伺夜': 'shu',
        '焰尾': 'flametail',
        '澄闪': 'aurora',
        '琴柳': 'chongyue',
        '玲': 'ling',
        '李': 'lee',
        '帕拉斯': 'pallas',
        '灰烬': 'ash',
        '提丰': 'typhon',
        '霍恩洛厄': 'hoederer',
        '阿斯卡纶': 'ascalon',
        '缪尔赛思': 'muelsyse',
        '仇白': 'qiubai',
        '归溟幽灵鲨': 'specter alter',
        '黄金船': 'goldenglow',
        '伺夜': 'shu',
        '维什戴尔': 'virtuosa',
        '瓦伊凡': 'wis\'adel',
        '乌有': 'logos',
        '佩佩': 'pepe',
        '特蕾西娅': 'theresa',
        # 5星干员
        '德克萨斯': 'texas',
        '幽灵鲨': 'specter',
        '蓝毒': 'blue poison',
        '白金': 'platinum',
        '陨星': 'meteorite',
        '梅尔': 'mayer',
        '赫默': 'silence',
        '华法琳': 'warfarin',
        '临光': 'nearl',
        '雷蛇': 'liskarm',
        '红': 'projekt red',
        '槐琥': 'waai fu',
        '格劳克斯': 'glaucus',
        '送葬人': 'executor',
        '食铁兽': 'hung',
        '守林人': 'beeswax',
        '巫恋': 'folinic',
        '苇草': 'reed',
        '布洛卡': 'broca',
        '格雷伊': 'greythroat',
        '慑砂': 'shamare',
        '石棉': 'asbestos',
        '莱恩哈特': 'leonhardt',
        '安德切尔': 'andreana',
        '艾丽妮': 'elysium',
        '刻刀': 'cutter',
        '图耶': 'tuye',
        '卡夫卡': 'kafka arknights',
        '贾维': 'jaye',
        '月见夜': 'tsukinogi',
        '惊蛰': 'leizi',
        '槐琥': 'waai fu',
        '阿消': 'aosta',
        '四月': 'april',
        '奥斯塔': 'aosta',
        '鞭刃': 'whislash',
        '月禾': 'whisperain',
        '罗宾': 'robin arknights',
        '卡涅利安': 'carnelian',
        '灰喉': 'greythroat',
        '极境': 'kjera',
        '野鬃': 'wildmane',
        '灰毫': 'greyy',
        '提丰': 'typhon',
        '黑键': 'blacknight',
        '琴柳': 'chongyue',
        '澄闪': 'aurora',
        '焰尾': 'flametail',
        '灰烬': 'ash',
        '霍恩洛厄': 'hoederer',
        '阿斯卡纶': 'ascalon',
        '缪尔赛思': 'muelsyse',
        '仇白': 'qiubai',
        '归溟幽灵鲨': 'specter alter',
        '黄金船': 'goldenglow',
        '伺夜': 'shu',
        '维什戴尔': 'virtuosa',
        '瓦伊凡': 'wis\'adel',
        '乌有': 'logos',
        '佩佩': 'pepe',
        # 常见干员
        '凯尔希': 'kal\'tsit',
        '博士': 'doctor arknights',
        '阿米娅': 'amiya',
        '德克萨斯': 'texas',
        '拉普兰德': 'lappland',
        '能天使': 'exusiai',
        '德克萨斯': 'texas',
        '空爆': 'firewatch',
        '陈': 'chen',
        '斯卡蒂': 'skadi',
        '幽灵鲨': 'specter',
        '银灰': 'silverash',
        '艾雅法拉': 'eyjafjalla',
        '伊芙利特': 'ifrit',
        '闪灵': 'shining',
        '夜莺': 'nightingale',
        '星熊': 'hoshiguma',
        '塞雷娅': 'saria',
    }
    
    def __init__(self, keyword, save_dir, target, callback, 
                 category_general=True, category_anime=True, category_people=False,
                 purity_sfw=True, purity_sketchy=True, purity_nsfw=False,
                 api_key=None, preview_ready_callback=None):
        self.keyword = keyword
        self.save_dir = save_dir
        self.target = target
        self.callback = callback
        self.preview_ready_callback = preview_ready_callback
        
        self.category_general = category_general
        self.category_anime = category_anime
        self.category_people = category_people
        self.purity_sfw = purity_sfw
        self.purity_sketchy = purity_sketchy
        self.purity_nsfw = purity_nsfw
        self.api_key = api_key
        
        self.running = False
        self.metadata = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        self.base_url = 'https://wallhaven.cc/api/v1/search'
    
    def contains_chinese(self, text):
        """检查文本是否包含中文字符"""
        return bool(re.search(r'[\u4e00-\u9fff]', text))
    
    def translate_to_english(self, text):
        """将中文翻译成英文"""
        # 先检查是否在专有名词字典中
        if text in self.PROPER_NOUNS:
            self.log(f"🔤 使用专有名词翻译: {text} -> {self.PROPER_NOUNS[text]}")
            return self.PROPER_NOUNS[text], True
        
        # 如果不包含中文，直接返回
        if not self.contains_chinese(text):
            return text, False
        
        try:
            translator = GoogleTranslator(source='zh-CN', target='en')
            translated = translator.translate(text)
            self.log(f"🔤 翻译关键词: {text} -> {translated}")
            return translated, True
        except Exception as e:
            self.log(f"⚠️ 翻译失败，使用原关键词: {e}")
            return text, False
    
    def log(self, message):
        """输出日志信息到 GUI"""
        if self.callback:
            self.callback(message)
    
    def collect_metadata(self):
        """收集图片元数据"""
        self.log("📋 开始收集图片元数据...")
        
        # 翻译关键词
        original_keyword = self.keyword
        translated_keyword, was_translated = self.translate_to_english(self.keyword)
        
        if was_translated:
            self.log(f"🌐 使用翻译后的关键词搜索: {translated_keyword}")
        
        # 构建分类参数 (General=1, Anime=1, People=1)
        category_str = ''
        category_str += '1' if self.category_general else '0'
        category_str += '1' if self.category_anime else '0'
        category_str += '1' if self.category_people else '0'
        
        # 构建纯度参数 (SFW=1, Sketchy=1, NSFW=1)
        purity_str = ''
        purity_str += '1' if self.purity_sfw else '0'
        purity_str += '1' if self.purity_sketchy else '0'
        purity_str += '1' if self.purity_nsfw else '0'
        
        page = 1
        collected = 0
        
        while collected < self.target and self.running:
            params = {
                'q': translated_keyword,
                'categories': category_str,
                'purity': purity_str,
                'page': page
            }
            
            if self.api_key:
                params['apikey'] = self.api_key
            
            try:
                resp = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                
                if 'data' not in data or not data['data']:
                    self.log(f"⚠️ 第 {page} 页没有更多结果")
                    break
                
                items = data['data']
                for item in items:
                    if collected >= self.target:
                        break
                    
                    img_url = item['path']
                    thumb_url = item.get('thumbs', {}).get('large', item['path'])
                    ext = os.path.splitext(img_url)[1]
                    
                    self.metadata.append({
                        'url': img_url,
                        'thumb': thumb_url,
                        'ext': ext,
                        'index': collected + 1
                    })
                    collected += 1
                
                self.log(f"📊 已收集 {collected}/{self.target} 张图片元数据")
                page += 1
                time.sleep(0.5)
                
            except Exception as e:
                self.log(f"❌ 收集元数据失败: {e}")
                break
        
        self.log(f"✅ 元数据收集完成！共 {len(self.metadata)} 张")
        
        # 通知预览功能已就绪
        if self.preview_ready_callback:
            self.preview_ready_callback()
    
    def start(self):
        """开始下载"""
        self.running = True
        
        # 先收集元数据
        self.collect_metadata()
        
        if not self.metadata:
            self.log("❌ 没有找到图片")
            return
        
        # 创建保存目录
        Path(self.save_dir).mkdir(parents=True, exist_ok=True)
        self.log(f"📁 保存目录: {self.save_dir}")
        
        # 开始下载
        self.log("🚀 开始下载图片...")
        
        try:
            for meta in self.metadata:
                if not self.running:
                    self.log("⏸️ 下载已停止")
                    break
                
                img_url = meta['url']
                ext = meta['ext']
                index = meta['index']
                filename = f"{index:04d}{ext}"
                filepath = os.path.join(self.save_dir, filename)
                
                try:
                    img_resp = requests.get(img_url, headers=self.headers, stream=True, timeout=30)
                    img_resp.raise_for_status()
                    
                    with open(filepath, 'wb') as f:
                        for chunk in img_resp.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    progress = (index / len(self.metadata)) * 100
                    self.log(f"✅ [{index:04d}/{len(self.metadata):04d}] ({progress:.1f}%) {filename}")
                    
                    time.sleep(1)  # 防封机制
                    
                except Exception as e:
                    self.log(f"❌ 下载失败 {filename}: {e}")
                    continue
            
            if self.running:
                self.log("🎉 所有图片下载完成！")
                self.running = False  # 下载完成后重置状态
        
        except Exception as e:
            self.log(f"❌ 下载过程出错: {e}")
            self.running = False  # 出错后也重置状态
    
    def stop(self):
        """停止下载"""
        self.running = False


class WallhavenGUI:
    """Wallhaven GUI 主界面"""
    
    def __init__(self):
        # 加载配置
        config = ConfigManager.load_config()
        
        # 加载语言设置
        self.current_language = config.get('language', 'en')
        self.lang = LANGUAGES.get(self.current_language, LANGUAGES['en'])
        
        # 加载主题设置
        appearance_mode = config.get('appearance_mode', 'system')
        ctk.set_appearance_mode(appearance_mode)
        ctk.set_default_color_theme("blue")
        
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title(self.lang['title'])
        self.root.geometry("900x1100")
        self.root.resizable(True, True)
        
        # 下载器实例
        self.downloader = None
        self.download_thread = None
        
        # 预览相关
        self.current_preview_index = 0
        self.preview_cache = {}
        self.metadata = None  # 修复：添加元数据引用
        self.autoplay_enabled = False  # 自动播放状态
        self.autoplay_timer = None  # 自动播放定时器
        
        # 调试模式
        self.debug_mode = False
        
        # UI控件引用（用于动态更新语言）
        self.ui_widgets = {}
        
        # 构建UI
        self.build_ui()
        
        # 加载上次配置
        self.load_last_config()
        
        # 绑定键盘快捷键
        self.root.bind('<Left>', lambda e: self.show_previous_image())
        self.root.bind('<Right>', lambda e: self.show_next_image())
        self.root.bind('<Up>', lambda e: self.show_previous_image())
        self.root.bind('<Down>', lambda e: self.show_next_image())
    
    def build_ui(self):
        """构建用户界面"""
        # 顶部框架（标题和设置按钮）
        top_frame = ctk.CTkFrame(self.root)
        top_frame.pack(pady=10, fill="x", padx=20)
        
        # 标题
        self.ui_widgets['title_label'] = ctk.CTkLabel(
            top_frame,
            text=self.lang['title'],
            font=("Arial", 24, "bold")
        )
        self.ui_widgets['title_label'].pack(side="left", padx=10)
        
        # 设置按钮
        self.ui_widgets['settings_btn'] = ctk.CTkButton(
            top_frame,
            text=self.lang['settings'],
            width=80,
            height=32,
            command=self.open_settings
        )
        self.ui_widgets['settings_btn'].pack(side="right", padx=10)
        
        # 输入区域
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # 关键词（使用下拉框支持历史记录）
        self.ui_widgets['keyword_label'] = ctk.CTkLabel(input_frame, text=self.lang['keyword'])
        self.ui_widgets['keyword_label'].grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # 获取搜索历史
        search_history = ConfigManager.get_search_history()
        self.keyword_combobox = ctk.CTkComboBox(
            input_frame,
            width=300,
            values=search_history if search_history else [""],
            state="normal"
        )
        self.keyword_combobox.grid(row=0, column=1, padx=10, pady=5)
        if search_history:
            self.keyword_combobox.set(search_history[0])
        
        # 下载数量
        self.ui_widgets['count_label'] = ctk.CTkLabel(input_frame, text=self.lang['count'])
        self.ui_widgets['count_label'].grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.count_entry = ctk.CTkEntry(input_frame, width=300, placeholder_text=self.lang['count_placeholder'])
        self.count_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # 保存路径
        self.ui_widgets['path_label'] = ctk.CTkLabel(input_frame, text=self.lang['save_path'])
        self.ui_widgets['path_label'].grid(row=2, column=0, padx=10, pady=5, sticky="w")
        path_container = ctk.CTkFrame(input_frame)
        path_container.grid(row=2, column=1, padx=10, pady=5)
        self.path_entry = ctk.CTkEntry(path_container, width=220)
        self.path_entry.pack(side="left", padx=(0, 5))
        self.ui_widgets['browse_btn'] = ctk.CTkButton(path_container, text=self.lang['browse'], width=70, command=self.browse_folder)
        self.ui_widgets['browse_btn'].pack(side="left")
        
        # 图片分类
        self.ui_widgets['category_label'] = ctk.CTkLabel(input_frame, text=self.lang['category'])
        self.ui_widgets['category_label'].grid(row=3, column=0, padx=10, pady=5, sticky="w")
        category_container = ctk.CTkFrame(input_frame)
        category_container.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.category_general_var = ctk.BooleanVar(value=True)
        self.category_anime_var = ctk.BooleanVar(value=True)
        self.category_people_var = ctk.BooleanVar(value=False)
        self.ui_widgets['category_general_cb'] = ctk.CTkCheckBox(category_container, text=self.lang['category_general'], variable=self.category_general_var)
        self.ui_widgets['category_general_cb'].pack(side="left", padx=5)
        self.ui_widgets['category_anime_cb'] = ctk.CTkCheckBox(category_container, text=self.lang['category_anime'], variable=self.category_anime_var)
        self.ui_widgets['category_anime_cb'].pack(side="left", padx=5)
        self.ui_widgets['category_people_cb'] = ctk.CTkCheckBox(category_container, text=self.lang['category_people'], variable=self.category_people_var)
        self.ui_widgets['category_people_cb'].pack(side="left", padx=5)
        
        # 内容分级
        self.ui_widgets['purity_label'] = ctk.CTkLabel(input_frame, text=self.lang['purity'])
        self.ui_widgets['purity_label'].grid(row=4, column=0, padx=10, pady=5, sticky="w")
        purity_container = ctk.CTkFrame(input_frame)
        purity_container.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.purity_sfw_var = ctk.BooleanVar(value=True)
        self.purity_sketchy_var = ctk.BooleanVar(value=True)
        self.purity_nsfw_var = ctk.BooleanVar(value=False)
        self.ui_widgets['purity_sfw_cb'] = ctk.CTkCheckBox(purity_container, text=self.lang['purity_sfw'], variable=self.purity_sfw_var)
        self.ui_widgets['purity_sfw_cb'].pack(side="left", padx=5)
        self.ui_widgets['purity_sketchy_cb'] = ctk.CTkCheckBox(purity_container, text=self.lang['purity_sketchy'], variable=self.purity_sketchy_var)
        self.ui_widgets['purity_sketchy_cb'].pack(side="left", padx=5)
        self.ui_widgets['purity_nsfw_cb'] = ctk.CTkCheckBox(purity_container, text=self.lang['purity_nsfw'], variable=self.purity_nsfw_var)
        self.ui_widgets['purity_nsfw_cb'].pack(side="left", padx=5)
        
        # API Key
        self.ui_widgets['api_key_label'] = ctk.CTkLabel(input_frame, text=self.lang['api_key'])
        self.ui_widgets['api_key_label'].grid(row=5, column=0, padx=10, pady=5, sticky="w")
        api_key_container = ctk.CTkFrame(input_frame)
        api_key_container.grid(row=5, column=1, padx=10, pady=5)
        self.api_key_entry = ctk.CTkEntry(api_key_container, width=220, placeholder_text=self.lang['api_key_placeholder'], show="*")
        self.api_key_entry.pack(side="left", padx=(0, 5))
        self.ui_widgets['save_api_btn'] = ctk.CTkButton(api_key_container, text=self.lang['save_config'], width=70, command=self.save_current_config)
        self.ui_widgets['save_api_btn'].pack(side="left")
        
        # 控制按钮
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(padx=20, pady=10, fill="x")
        self.start_btn = ctk.CTkButton(control_frame, text=self.lang['start_download'], command=self.start_download, height=40)
        self.start_btn.pack(side="left", padx=10, expand=True, fill="x")
        self.stop_btn = ctk.CTkButton(control_frame, text=self.lang['stop_download'], command=self.stop_download, height=40, state="disabled")
        self.stop_btn.pack(side="left", padx=10, expand=True, fill="x")
        
        # 分割区域
        split_frame = ctk.CTkFrame(self.root)
        split_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # 左侧：日志区域
        left_frame = ctk.CTkFrame(split_frame)
        left_frame.pack(side="left", padx=(0, 5), fill="both", expand=True)
        self.ui_widgets['log_label'] = ctk.CTkLabel(left_frame, text=self.lang['download_log'], font=("Arial", 14, "bold"))
        self.ui_widgets['log_label'].pack(pady=5)
        self.log_text = ctk.CTkTextbox(left_frame, width=400, height=500)
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)
        
        # 右侧：预览区域
        right_frame = ctk.CTkFrame(split_frame)
        right_frame.pack(side="left", padx=(5, 0), fill="both", expand=True)
        self.ui_widgets['preview_title'] = ctk.CTkLabel(right_frame, text=self.lang['image_preview'], font=("Arial", 14, "bold"))
        self.ui_widgets['preview_title'].pack(pady=5)
        
        # 预览状态标签（显示在图片上方）
        self.preview_status_label = ctk.CTkLabel(right_frame, text=self.lang['waiting'], font=("Arial", 12))
        self.preview_status_label.pack(pady=(0, 5))
        
        # 图片显示区域
        self.preview_label = ctk.CTkLabel(right_frame, text="", width=400, height=400)
        self.preview_label.pack(padx=10, pady=5)
        
        # 预览控制按钮
        preview_control_frame = ctk.CTkFrame(right_frame)
        preview_control_frame.pack(pady=10)
        self.prev_btn = ctk.CTkButton(preview_control_frame, text=self.lang['previous'], width=100, height=40,
                                      command=self.show_previous_image, state="disabled")
        self.prev_btn.pack(side="left", padx=5)
        self.refresh_btn = ctk.CTkButton(preview_control_frame, text=self.lang['refresh'], width=80, height=40,
                                         command=self.refresh_current_image, state="disabled")
        self.refresh_btn.pack(side="left", padx=5)
        self.next_btn = ctk.CTkButton(preview_control_frame, text=self.lang['next'], width=100, height=40,
                                      command=self.show_next_image, state="disabled")
        self.next_btn.pack(side="left", padx=5)
        
        # 自动播放按钮
        self.autoplay_btn = ctk.CTkButton(preview_control_frame, text=self.lang['autoplay'], width=120, height=40,
                                          command=self.toggle_autoplay, state="disabled")
        self.autoplay_btn.pack(side="left", padx=5)
    
    def browse_folder(self):
        """浏览文件夹"""
        initial_dir = self.path_entry.get() or os.path.expanduser("~")
        folder = filedialog.askdirectory(title=self.lang['save_path'], initialdir=initial_dir)
        if folder:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, folder)
    
    def log_message(self, message):
        """在日志窗口显示信息（线程安全）"""
        self.root.after(0, lambda: self._log_message_impl(message))
    
    def _log_message_impl(self, message):
        """实际的日志显示实现"""
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
    
    def show_age_confirmation(self, callback):
        """显示年龄确认窗口"""
        confirm_window = ctk.CTkToplevel(self.root)
        confirm_window.title(self.lang['age_confirm_title'])
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        
        # 置顶并模态
        confirm_window.transient(self.root)
        confirm_window.grab_set()
        
        # 设置橙色背景
        confirm_window.configure(fg_color="#FF8C00")
        
        # 消息标签（白色文字）
        message_label = ctk.CTkLabel(
            confirm_window,
            text=self.lang['age_confirm_message'],
            font=("Arial", 18, "bold"),
            text_color="white",
            fg_color="#FF8C00"
        )
        message_label.pack(pady=50)
        
        # 确认按钮
        def on_confirm():
            confirm_window.destroy()
            if callback:
                callback()
        
        confirm_btn = ctk.CTkButton(
            confirm_window,
            text=self.lang['age_confirm_button'],
            font=("Arial", 14, "bold"),
            width=150,
            height=40,
            fg_color="white",
            text_color="#FF8C00",
            hover_color="#F0F0F0",
            command=on_confirm
        )
        confirm_btn.pack(pady=20)
        
        # 等待窗口关闭
        confirm_window.wait_window()
    
    def show_disclaimer(self):
        """显示免责声明窗口"""
        # 创建置顶子窗口
        disclaimer_window = ctk.CTkToplevel(self.root)
        disclaimer_window.title(self.lang['disclaimer_title'])
        disclaimer_window.geometry("700x550")
        
        # 窗口居中显示
        disclaimer_window.update_idletasks()
        width = disclaimer_window.winfo_width()
        height = disclaimer_window.winfo_height()
        x = (disclaimer_window.winfo_screenwidth() // 2) - (width // 2)
        y = (disclaimer_window.winfo_screenheight() // 2) - (height // 2)
        disclaimer_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # 置顶并模态（锁定焦点）
        disclaimer_window.transient(self.root)
        disclaimer_window.grab_set()
        
        # 标题标签
        title_label = ctk.CTkLabel(
            disclaimer_window,
            text=self.lang['disclaimer_title'],
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=(20, 10))
        
        # 创建文本框显示免责声明内容
        textbox = ctk.CTkTextbox(
            disclaimer_window,
            width=650,
            height=400,
            font=("Arial", 12),
            wrap="word"
        )
        textbox.pack(padx=20, pady=10, fill="both", expand=True)
        
        # 插入免责声明文本
        textbox.insert("1.0", self.lang['disclaimer_content'])
        
        # 设置为只读状态
        textbox.configure(state="disabled")
        
        # 关闭按钮
        close_btn = ctk.CTkButton(
            disclaimer_window,
            text=self.lang['close'],
            width=120,
            height=35,
            font=("Arial", 14, "bold"),
            command=disclaimer_window.destroy
        )
        close_btn.pack(pady=(10, 20))
        
        # 确保窗口获得焦点
        disclaimer_window.focus_set()
    
    def save_current_config(self):
        """保存当前配置"""
        keyword = self.keyword_combobox.get()
        count = self.count_entry.get()
        save_path = self.path_entry.get()
        category_general = self.category_general_var.get()
        category_anime = self.category_anime_var.get()
        category_people = self.category_people_var.get()
        purity_sfw = self.purity_sfw_var.get()
        purity_sketchy = self.purity_sketchy_var.get()
        purity_nsfw = self.purity_nsfw_var.get()
        api_key = self.api_key_entry.get()
        
        # 检查是否选择了NSFW并且有API Key
        if purity_nsfw and api_key:
            # 显示年龄确认窗口
            def save_after_confirm():
                config = {
                    'keyword': keyword,
                    'count': count,
                    'save_path': save_path,
                    'category_general': category_general,
                    'category_anime': category_anime,
                    'category_people': category_people,
                    'purity_sfw': purity_sfw,
                    'purity_sketchy': purity_sketchy,
                    'purity_nsfw': purity_nsfw,
                    'api_key': api_key
                }
                
                # 保存主题和语言设置
                current_config = ConfigManager.load_config()
                config['appearance_mode'] = current_config.get('appearance_mode', 'system')
                config['language'] = current_config.get('language', 'en')
                
                ConfigManager.save_config(config)
                messagebox.showinfo(self.lang['success'], self.lang['config_saved'])
            
            self.show_age_confirmation(save_after_confirm)
        else:
            # 直接保存
            config = {
                'keyword': keyword,
                'count': count,
                'save_path': save_path,
                'category_general': category_general,
                'category_anime': category_anime,
                'category_people': category_people,
                'purity_sfw': purity_sfw,
                'purity_sketchy': purity_sketchy,
                'purity_nsfw': purity_nsfw,
                'api_key': api_key
            }
            
            # 保存主题和语言设置
            current_config = ConfigManager.load_config()
            config['appearance_mode'] = current_config.get('appearance_mode', 'system')
            config['language'] = current_config.get('language', 'en')
            
            ConfigManager.save_config(config)
            messagebox.showinfo(self.lang['success'], self.lang['config_saved'])
    
    def open_settings(self):
        """打开设置窗口"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title(self.lang['settings_title'])
        settings_window.geometry("400x500")
        settings_window.resizable(False, False)
        
        # 使窗口置顶（不使用grab_set避免阻塞）
        settings_window.transient(self.root)
        
        # 标题
        title = ctk.CTkLabel(settings_window, text=self.lang['settings_title'], font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # 创建滚动框架
        scrollable_frame = ctk.CTkScrollableFrame(settings_window, width=360, height=320)
        scrollable_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # 显示设置区域
        display_frame = ctk.CTkFrame(scrollable_frame)
        display_frame.pack(padx=10, pady=10, fill="x")
        
        display_label = ctk.CTkLabel(display_frame, text=self.lang['display'], font=("Arial", 16, "bold"))
        display_label.pack(pady=10, anchor="w", padx=10)
        
        # 主题选择
        theme_label = ctk.CTkLabel(display_frame, text=self.lang['appearance_mode'])
        theme_label.pack(pady=(5, 0), anchor="w", padx=20)
        
        # 获取当前主题
        config = ConfigManager.load_config()
        current_theme = config.get('appearance_mode', 'system')
        
        theme_var = ctk.StringVar(value=current_theme)
        
        theme_options = [
            (self.lang['light_mode'], "light"),
            (self.lang['dark_mode'], "dark"),
            (self.lang['system_mode'], "system")
        ]
        
        for text, value in theme_options:
            radio = ctk.CTkRadioButton(
                display_frame,
                text=text,
                variable=theme_var,
                value=value
            )
            radio.pack(pady=5, anchor="w", padx=40)
        
        # 语言选择
        language_label = ctk.CTkLabel(display_frame, text=self.lang['language'])
        language_label.pack(pady=(10, 0), anchor="w", padx=20)
        
        # 获取当前语言
        current_language = config.get('language', 'en')
        
        language_var = ctk.StringVar(value=current_language)
        
        language_options = [
            (self.lang['language_english'], "en"),
            (self.lang['language_chinese'], "zh")
        ]
        
        for text, value in language_options:
            radio = ctk.CTkRadioButton(
                display_frame,
                text=text,
                variable=language_var,
                value=value
            )
            radio.pack(pady=5, anchor="w", padx=40)
        
        # 调试模式开关
        debug_label = ctk.CTkLabel(display_frame, text=self.lang['debug_mode'])
        debug_label.pack(pady=(10, 0), anchor="w", padx=20)
        
        debug_switch = ctk.CTkSwitch(
            display_frame,
            text="",
            command=self.toggle_debug_mode
        )
        if self.debug_mode:
            debug_switch.select()
        debug_switch.pack(pady=5, anchor="w", padx=40)
        
        # 按钮容器（固定在底部）
        button_frame = ctk.CTkFrame(settings_window)
        button_frame.pack(pady=10, fill="x")
        
        # 查看免责声明按钮（放在最上面，优先级最高）
        disclaimer_btn = ctk.CTkButton(
            button_frame,
            text=self.lang['view_disclaimer'],
            width=180,
            height=35,
            font=("Arial", 13, "bold"),
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            command=self.show_disclaimer
        )
        disclaimer_btn.pack(pady=(5, 10))
        
        # 应用按钮
        apply_btn = ctk.CTkButton(
            button_frame,
            text=self.lang['apply'],
            width=100,
            command=lambda: self.apply_settings(theme_var.get(), language_var.get(), settings_window)
        )
        apply_btn.pack(pady=(5, 5))
        
        # 关闭按钮
        close_btn = ctk.CTkButton(
            button_frame,
            text=self.lang['close'],
            width=100,
            command=settings_window.destroy
        )
        close_btn.pack(pady=(5, 5))
    
    def apply_settings(self, theme_mode, language, settings_window):
        """应用设置"""
        try:
            # 保存设置
            config = ConfigManager.load_config()
            config['appearance_mode'] = theme_mode
            config['language'] = language
            ConfigManager.save_config(config)
            
            # 应用主题
            ctk.set_appearance_mode(theme_mode)
            
            # 应用语言
            old_language = self.current_language
            self.current_language = language
            self.lang = LANGUAGES.get(language, LANGUAGES['en'])
            
            # 如果语言改变，更新界面
            if old_language != language:
                self.update_ui_language()
                mode_names = {'en': 'English', 'zh': '简体中文'}
                self.log_message(self.lang['language_changed'].format(lang=mode_names.get(language, language)))
            
            # 显示主题切换提示
            mode_names = {
                'light': self.lang['light_mode'],
                'dark': self.lang['dark_mode'],
                'system': self.lang['system_mode']
            }
            self.log_message(self.lang['theme_changed'].format(mode=mode_names.get(theme_mode, theme_mode)))
            
            # 关闭设置窗口
            settings_window.destroy()
            
        except Exception as e:
            self.log_message(f"❌ {self.lang['error']}: {e}")
    
    def change_theme(self, mode):
        """切换主题（已弃用，保留兼容性）"""
        try:
            ctk.set_appearance_mode(mode)
            
            # 保存主题设置
            config = ConfigManager.load_config()
            config['appearance_mode'] = mode
            ConfigManager.save_config(config)
            
            # 显示成功提示
            mode_names = {
                'light': self.lang['light_mode'],
                'dark': self.lang['dark_mode'],
                'system': self.lang['system_mode']
            }
            self.log_message(self.lang['theme_changed'].format(mode=mode_names.get(mode, mode)))
        except Exception as e:
            self.log_message(f"❌ {self.lang['error']}: {e}")
    
    def update_ui_language(self):
        """更新界面语言"""
        # 更新窗口标题
        self.root.title(self.lang['title'])
        
        # 更新所有UI控件的文本
        try:
            # 顶部区域
            self.ui_widgets['title_label'].configure(text=self.lang['title'])
            self.ui_widgets['settings_btn'].configure(text=self.lang['settings'])
            
            # 输入区域标签
            self.ui_widgets['keyword_label'].configure(text=self.lang['keyword'])
            self.ui_widgets['count_label'].configure(text=self.lang['count'])
            self.ui_widgets['path_label'].configure(text=self.lang['save_path'])
            self.ui_widgets['browse_btn'].configure(text=self.lang['browse'])
            
            # 分类标签和复选框
            self.ui_widgets['category_label'].configure(text=self.lang['category'])
            self.ui_widgets['category_general_cb'].configure(text=self.lang['category_general'])
            self.ui_widgets['category_anime_cb'].configure(text=self.lang['category_anime'])
            self.ui_widgets['category_people_cb'].configure(text=self.lang['category_people'])
            
            # 分级标签和复选框
            self.ui_widgets['purity_label'].configure(text=self.lang['purity'])
            self.ui_widgets['purity_sfw_cb'].configure(text=self.lang['purity_sfw'])
            self.ui_widgets['purity_sketchy_cb'].configure(text=self.lang['purity_sketchy'])
            self.ui_widgets['purity_nsfw_cb'].configure(text=self.lang['purity_nsfw'])
            
            # API Key
            self.ui_widgets['api_key_label'].configure(text=self.lang['api_key'])
            self.ui_widgets['save_api_btn'].configure(text=self.lang['save_config'])
            
            # 控制按钮
            self.start_btn.configure(text=self.lang['start_download'])
            self.stop_btn.configure(text=self.lang['stop_download'])
            
            # 日志和预览区域
            self.ui_widgets['log_label'].configure(text=self.lang['download_log'])
            self.ui_widgets['preview_title'].configure(text=self.lang['image_preview'])
            
            # 预览控制按钮
            self.prev_btn.configure(text=self.lang['previous'])
            self.refresh_btn.configure(text=self.lang['refresh'])
            self.next_btn.configure(text=self.lang['next'])
            # 更新自动播放按钮文本
            if self.autoplay_enabled:
                self.autoplay_btn.configure(text=self.lang['stop_autoplay'])
            else:
                self.autoplay_btn.configure(text=self.lang['autoplay'])
            
            # 更新预览状态（如果没有正在预览）
            if not self.metadata:
                self.preview_status_label.configure(text=self.lang['waiting'])
            
            # 更新输入框占位符（需要重新创建Entry控件才能更新placeholder）
            # 这里我们只能在下次重启时生效
            
        except Exception as e:
            self.log_message(f"❌ {self.lang['error']}: {e}")
    
    def load_last_config(self):
        """加载上次保存的配置"""
        config = ConfigManager.load_config()
        if config:
            self.log_message(self.lang['loading_config'])
            # 不再自动填充关键词，使用历史记录
            self.count_entry.insert(0, config.get('count', ''))
            self.path_entry.insert(0, config.get('save_path', ''))
            self.category_general_var.set(config.get('category_general', True))
            self.category_anime_var.set(config.get('category_anime', True))
            self.category_people_var.set(config.get('category_people', False))
            self.purity_sfw_var.set(config.get('purity_sfw', True))
            self.purity_sketchy_var.set(config.get('purity_sketchy', True))
            self.purity_nsfw_var.set(config.get('purity_nsfw', False))
            api_key = config.get('api_key', '')
            if api_key:
                self.api_key_entry.insert(0, api_key)
                # 如果有API Key且选择了NSFW，启动时显示年龄确认
                if config.get('purity_nsfw', False):
                    self.root.after(500, lambda: self.show_age_confirmation(None))
    
    def start_download(self):
        """开始下载"""
        keyword = self.keyword_combobox.get().strip()
        target = self.count_entry.get().strip()
        save_dir = self.path_entry.get().strip()
        
        # 验证输入
        if not keyword:
            messagebox.showerror(self.lang['error'], self.lang['error_keyword'])
            return
        
        try:
            target = int(target)
            if target <= 0:
                raise ValueError()
        except:
            messagebox.showerror(self.lang['error'], self.lang['error_count'])
            return
        
        if not save_dir:
            messagebox.showerror(self.lang['error'], self.lang['error_path'])
            return
        
        # 检查分类
        category_general = self.category_general_var.get()
        category_anime = self.category_anime_var.get()
        category_people = self.category_people_var.get()
        if not (category_general or category_anime or category_people):
            messagebox.showerror(self.lang['error'], self.lang['error_category'])
            return
        
        # 检查分级
        purity_sfw = self.purity_sfw_var.get()
        purity_sketchy = self.purity_sketchy_var.get()
        purity_nsfw = self.purity_nsfw_var.get()
        if not (purity_sfw or purity_sketchy or purity_nsfw):
            messagebox.showerror(self.lang['error'], self.lang['error_purity'])
            return
        
        # 检查 NSFW
        api_key = self.api_key_entry.get().strip() or None
        if purity_nsfw and not api_key:
            messagebox.showwarning(self.lang['warning'], self.lang['warning_nsfw'])
            return
        
        # 保存搜索历史
        ConfigManager.add_search_history(keyword)
        
        # 更新下拉框选项
        search_history = ConfigManager.get_search_history()
        self.keyword_combobox.configure(values=search_history)
        
        # 停止旧的下载器（如果存在）
        if self.downloader:
            self.downloader.stop()
            # 等待旧线程结束
            if self.download_thread and self.download_thread.is_alive():
                self.download_thread.join(timeout=2)
        
        # 停止自动播放
        self.stop_autoplay()
        
        # 清空日志和预览
        self.log_text.delete('1.0', 'end')
        self.preview_status_label.configure(text=self.lang['waiting_metadata'])
        self.preview_label.configure(image=None)
        self.current_preview_index = 0
        self.preview_cache.clear()  # 清空缓存
        self.metadata = None  # 重置元数据引用
        
        # 禁用预览按钮
        self.prev_btn.configure(state="disabled")
        self.refresh_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.autoplay_btn.configure(state="disabled")
        
        # 创建新的下载器
        self.downloader = WallhavenDownloader(
            keyword=keyword,
            save_dir=save_dir,
            target=target,
            callback=self.log_message,
            category_general=category_general,
            category_anime=category_anime,
            category_people=category_people,
            purity_sfw=purity_sfw,
            purity_sketchy=purity_sketchy,
            purity_nsfw=purity_nsfw,
            api_key=api_key,
            preview_ready_callback=self.enable_preview
        )
        
        # 启动下载线程
        self.download_thread = threading.Thread(target=self._download_wrapper, daemon=True)
        self.download_thread.start()
        
        # 更新按钮状态
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
    
    def _download_wrapper(self):
        """下载包装器，用于在下载完成后重置按钮状态"""
        try:
            self.downloader.start()
        finally:
            # 下载完成或出错后，在主线程中重置按钮状态
            self.root.after(0, self._reset_buttons_after_download)
    
    def _reset_buttons_after_download(self):
        """下载完成后重置按钮状态"""
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def stop_download(self):
        """停止下载"""
        if self.downloader:
            self.downloader.stop()
            self.log_message("⏸️ 正在停止下载...")
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def toggle_debug_mode(self):
        """切换调试模式"""
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.log_message(self.lang['debug_enabled'])
        else:
            self.log_message(self.lang['debug_disabled'])
    
    def debug_log(self, message):
        """调试日志（仅在调试模式下显示）"""
        if self.debug_mode:
            self.log_message(f"🔍 {message}")
    
    def enable_preview(self):
        """启用预览功能（元数据收集完成后调用）"""
        def _enable():
            try:
                # 修复：保存元数据引用，确保预览使用最新的元数据
                if self.downloader and self.downloader.metadata:
                    self.debug_log(f"收到预览回调，元数据数量：{len(self.downloader.metadata)}")
                    self.metadata = self.downloader.metadata
                    self.current_preview_index = 0
                    self.preview_cache.clear()  # 使用clear()而不是重新赋值
                    self.prev_btn.configure(state="normal")
                    self.refresh_btn.configure(state="normal")
                    self.next_btn.configure(state="normal")
                    self.autoplay_btn.configure(state="normal")
                    self.debug_log(f"准备显示第一张图片")
                    self.show_current_image()
                    self.log_message(self.lang['preview_enabled'])
                else:
                    error_msg = f"预览回调失败 - downloader存在: {self.downloader is not None}, metadata存在: {self.downloader.metadata if self.downloader else 'N/A'}"
                    self.debug_log(error_msg)
            except Exception as e:
                import traceback
                error_detail = traceback.format_exc()
                self.log_message(f"❌ enable_preview异常:\n{error_detail}")
        
        self.root.after(0, _enable)
    
    def show_current_image(self):
        """显示当前索引的图片（使用缩略图）"""
        try:
            # 修复：使用保存的元数据引用而不是 downloader.metadata
            metadata = self.metadata
            if not metadata:
                self.debug_log(f"metadata为空，无法显示图片")
                return
            
            if not (0 <= self.current_preview_index < len(metadata)):
                self.debug_log(f"索引越界 - 当前索引: {self.current_preview_index}, 总数: {len(metadata)}")
                return
            
            current_meta = metadata[self.current_preview_index]
            thumb_url = current_meta.get('thumb', '')
            
            # 修复：使用实际索引而不是元数据中的索引
            index = self.current_preview_index + 1
            total = len(metadata)
            
            self.debug_log(f"准备显示图片 {index}/{total}, URL: {thumb_url[:50]}...")
            
            # 检查缓存
            if self.current_preview_index in self.preview_cache:
                photo = self.preview_cache[self.current_preview_index]
                self.preview_status_label.configure(text=self.lang['previewing'].format(index=index, total=total))
                self.preview_label.configure(image=photo)
                self.debug_log(f"从缓存加载图片 {index}/{total}")
                # 预加载下一张
                self._preload_adjacent_images()
                return
            
            # 异步加载图片
            self.preview_status_label.configure(text=self.lang['loading_preview'].format(index=index, total=total))
            # 清除图片但不设置text，避免TclError
            self.preview_label.configure(image=None)
            # 传递当前索引，避免异步加载时索引变化
            cache_index = self.current_preview_index
            self.debug_log(f"启动异步加载线程")
            threading.Thread(target=self._load_image_async, args=(thumb_url, index, total, cache_index), daemon=True).start()
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.log_message(f"❌ show_current_image异常:\n{error_detail}")
    
    def _load_image_async(self, thumb_url, index, total, cache_index):
        """异步加载图片"""
        try:
            self.debug_log(f"开始下载图片 {index}/{total}")
            response = requests.get(thumb_url, timeout=10)
            response.raise_for_status()
            
            self.debug_log(f"图片下载成功，开始处理")
            img = Image.open(BytesIO(response.content))
            
            # 缩放图片以适应预览区域
            max_width, max_height = 400, 400
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # 缓存图片 - 使用传入的索引而不是当前索引
            self.preview_cache[cache_index] = photo
            self.debug_log(f"图片已缓存 {index}/{total}")
            
            # 在主线程更新UI - 使用functools.partial避免闭包问题
            from functools import partial
            self.root.after(0, partial(self._update_preview_ui, photo, index, total, cache_index))
            
            # 预加载相邻图片
            self._preload_adjacent_images()
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            self.log_message(f"❌ _load_image_async异常 {index}/{total}:\n{error_detail}")
            from functools import partial
            self.root.after(0, partial(self._update_preview_error, str(e)))
    
    def _update_preview_ui(self, photo, index, total, cache_index):
        """更新预览UI"""
        # 只有当前索引与缓存索引一致时才更新UI，避免显示错误的图片
        if self.current_preview_index == cache_index:
            self.preview_status_label.configure(text=self.lang['previewing'].format(index=index, total=total))
            self.preview_label.configure(image=photo)
    
    def _update_preview_error(self, error_msg):
        """更新预览错误信息"""
        self.preview_status_label.configure(text=self.lang['load_failed'].format(error=error_msg))
        self.preview_label.configure(image=None)
    
    def _preload_adjacent_images(self):
        """预加载相邻的图片（前后各2张）"""
        if not self.metadata:
            return
        
        # 预加载范围
        preload_range = 2
        total = len(self.metadata)
        
        for offset in range(1, preload_range + 1):
            # 预加载后面的图片
            next_idx = self.current_preview_index + offset
            if next_idx < total and next_idx not in self.preview_cache:
                threading.Thread(target=self._preload_image, args=(next_idx,), daemon=True).start()
            
            # 预加载前面的图片
            prev_idx = self.current_preview_index - offset
            if prev_idx >= 0 and prev_idx not in self.preview_cache:
                threading.Thread(target=self._preload_image, args=(prev_idx,), daemon=True).start()
    
    def _preload_image(self, idx):
        """预加载指定索引的图片"""
        if not self.metadata or idx in self.preview_cache:
            return
        
        try:
            thumb_url = self.metadata[idx].get('thumb', '')
            response = requests.get(thumb_url, timeout=5)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            max_width, max_height = 400, 400
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_cache[idx] = photo
            
        except:
            pass  # 预加载失败不影响主流程
    
    def show_previous_image(self):
        """显示上一张图片"""
        if not self.metadata:
            return
        
        # 手动切换时停止自动播放
        if self.autoplay_enabled:
            self.stop_autoplay()
        
        if self.current_preview_index > 0:
            self.current_preview_index -= 1
            self.show_current_image()
    
    def show_next_image(self):
        """显示下一张图片"""
        if not self.metadata:
            return
        
        # 手动切换时停止自动播放
        if self.autoplay_enabled:
            self.stop_autoplay()
        
        if self.current_preview_index < len(self.metadata) - 1:
            self.current_preview_index += 1
            self.show_current_image()
    
    def refresh_current_image(self):
        """刷新当前图片（清除缓存重新加载）"""
        if not self.metadata:
            return
        
        # 清除当前图片的缓存
        if self.current_preview_index in self.preview_cache:
            del self.preview_cache[self.current_preview_index]
        
        # 重新加载
        self.show_current_image()
    
    def toggle_autoplay(self):
        """切换自动播放状态"""
        if self.autoplay_enabled:
            self.stop_autoplay()
        else:
            self.start_autoplay()
    
    def start_autoplay(self):
        """开始自动播放"""
        if not self.metadata:
            return
        
        self.autoplay_enabled = True
        self.autoplay_btn.configure(text=self.lang['stop_autoplay'])
        self.log_message("▶️ 自动播放已开启（5秒/张）" if self.current_language == 'zh' else "▶️ Auto play enabled (5s/image)")
        self._schedule_next_image()
    
    def stop_autoplay(self):
        """停止自动播放"""
        self.autoplay_enabled = False
        if self.autoplay_timer:
            self.root.after_cancel(self.autoplay_timer)
            self.autoplay_timer = None
        self.autoplay_btn.configure(text=self.lang['autoplay'])
    
    def _schedule_next_image(self):
        """调度下一张图片"""
        if not self.autoplay_enabled:
            return
        
        # 5秒后切换到下一张
        self.autoplay_timer = self.root.after(5000, self._autoplay_next)
    
    def _autoplay_next(self):
        """自动播放下一张"""
        if not self.autoplay_enabled or not self.metadata:
            return
        
        # 如果到达最后一张，循环到第一张
        if self.current_preview_index >= len(self.metadata) - 1:
            self.current_preview_index = 0
        else:
            self.current_preview_index += 1
        
        self.show_current_image()
        self._schedule_next_image()
    
    def run(self):
        """启动主循环"""
        self.root.mainloop()


if __name__ == "__main__":
    app = WallhavenGUI()
    app.run()
