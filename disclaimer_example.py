"""
免责声明功能示例代码
演示如何在 CustomTkinter 应用中集成免责声明弹窗
"""

import customtkinter as ctk


class DisclaimerExample:
    """免责声明功能示例类"""
    
    def __init__(self):
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("免责声明功能示例")
        self.root.geometry("500x300")
        
        # 设置语言（可以是 'zh' 或 'en'）
        self.current_language = 'zh'
        self.lang = self.get_language_dict()
        
        # 创建界面
        self.create_ui()
    
    def get_language_dict(self):
        """获取语言字典"""
        languages = {
            'zh': {
                'title': '免责声明示例',
                'view_disclaimer': '📜 查看免责声明',
                'disclaimer_title': '⚠️ 免责声明',
                'close': '关闭',
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

4. "As-Is" Software: This software is provided "as is" and free of charge. The developer provides no warranties regarding permanent availability, failures due to third-party API changes, or any potential data loss incurred during usage."""
            },
            'en': {
                'title': 'Disclaimer Example',
                'view_disclaimer': '📜 View Disclaimer',
                'disclaimer_title': '⚠️ Disclaimer',
                'close': 'Close',
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

4. 按"原样"提供：本软件按"原样"免费提供。开发者不对软件的永久可用性、第三方接口变动造成的失效、或使用过程中可能发生的数据丢失承担任何连带法律责任。"""
            }
        }
        return languages.get(self.current_language, languages['zh'])
    
    def create_ui(self):
        """创建用户界面"""
        # 标题
        title_label = ctk.CTkLabel(
            self.root,
            text=self.lang['title'],
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=40)
        
        # 说明文本
        info_label = ctk.CTkLabel(
            self.root,
            text="点击下方按钮查看免责声明弹窗效果",
            font=("Arial", 14)
        )
        info_label.pack(pady=20)
        
        # 查看免责声明按钮
        disclaimer_btn = ctk.CTkButton(
            self.root,
            text=self.lang['view_disclaimer'],
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#FF6B6B",
            hover_color="#FF5252",
            command=self.show_disclaimer
        )
        disclaimer_btn.pack(pady=30)
    
    def show_disclaimer(self):
        """
        显示免责声明窗口
        
        功能特点：
        1. 使用 CTkToplevel 创建置顶子窗口
        2. 窗口自动居中显示
        3. 使用 CTkTextbox 展示文本，支持滚轮滚动
        4. 文本框设置为只读状态（state="disabled"）
        5. 模态窗口效果（grab_set），锁定焦点
        """
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
        
        # 置顶并模态（锁定焦点，用户必须先关闭此窗口才能操作主窗口）
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
        # wrap="word" 表示按单词换行
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
        
        # 设置为只读状态，禁止用户编辑
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
    
    def run(self):
        """运行应用"""
        self.root.mainloop()


if __name__ == "__main__":
    # 设置外观模式
    ctk.set_appearance_mode("system")  # 可选: "light", "dark", "system"
    ctk.set_default_color_theme("blue")  # 可选: "blue", "green", "dark-blue"
    
    # 创建并运行应用
    app = DisclaimerExample()
    app.run()
