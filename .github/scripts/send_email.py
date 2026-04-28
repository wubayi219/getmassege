#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本
Email Sending Script
"""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

def read_daily_report():
    """读取每日报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = Path("docs/daily-reports") / f"{today}-report.md"
    
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            return f.read()
    
    return None

def send_email(recipient_email, subject, body, is_html=False):
    """
    发送邮件
    Send email notification
    
    参数:
        recipient_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件内容
        is_html: 是否为 HTML 格式
    """
    
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    
    if not sender_email or not password:
        print("⚠️ 未配置邮箱凭证，跳过邮件发送")
        print("💡 提示: 请在 GitHub Secrets 中配置 EMAIL_ADDRESS 和 EMAIL_PASSWORD")
        return
    
    try:
        # 创建邮件
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # 转换 Markdown 为纯文本或 HTML
        if is_html:
            body_part = MIMEText(body, "html", "utf-8")
        else:
            body_part = MIMEText(body, "plain", "utf-8")
        
        message.attach(body_part)
        
        # 连接到 SMTP 服务器并发送
        # 这里使用 Gmail 示例，可根据需要修改
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        print(f"✅ 邮件发送成功: {recipient_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ 邮件认证失败，请检查邮箱和密码")
        return False
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def create_email_body():
    """创建邮件正文"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    body = f"""🌿 山茶油每日信息摘要 - {today}

亲爱的用户，

本邮件包含今天收集到的山茶油相关信息整理。

═══════════════════════════════════════

📊 今日更新摘要
- ✨ 知识库内容审查
- 🔄 营养信息更新  
- 📖 健康益处补充
- 🛍️ 选购建议更新
- 🧴 护肤方法完善
- 🍳 烹饪指南补充

═══════════════════════════════════════

🎯 推荐阅读

1. 山茶油的营养成分
   特别推荐阅读：高单不饱和脂肪酸含量
   关键数据：80-85% 油酸，维生素E 50-70mg/100g

2. 烹饪应用
   最佳方法：凉拌和低温炒菜
   烟点范围：210-252°C
   每日用量：1-2 汤匙

3. 护肤秘诀
   使用时间：早晚护肤时使用
   用量指导：面部 2-5 滴
   吸收时间：5-10 分钟

═══════════════════════════════════════

💡 本周核心知识

✅ 成分认识
- 山茶油主要成分是单不饱和脂肪酸
- 与橄榄油营养成分相似
- 维生素E 含量高于一般油品

✅ 健康益处
- 支持心血管健康
- 具有抗氧化作用
- 具有抗炎特性

✅ 实用建议
- 选择冷压未精炼油最佳
- 深色玻璃瓶保存效果好
- 冷藏存储可延长保质期

═══════════════════════════════════════

📈 统计数据
- 知识库章节数: 10
- 常见问题数: 15+
- 护肤应用数: 7+
- 烹饪方法数: 7
- 总信息量: 50,000+ 字

═══════════════════════════════════════

🔗 相关链接
📖 完整知识库: https://github.com/wubayi219/getmassege/blob/main/docs/camellia-oil-knowledge-base.md
📋 每日报告: https://github.com/wubayi219/getmassege/tree/main/docs/daily-reports
💬 问题反馈: https://github.com/wubayi219/getmassege/issues

═══════════════════════════════════════

⏰ 下次更新
- 下一次每日更新: 明天 09:00 UTC
- 下一周报汇总: 下周一

感谢关注！

---
山茶油知识库系统
https://github.com/wubayi219/getmassege
"""
    
    return body

def main():
    """主函数"""
    recipient_email = os.getenv("EMAIL_ADDRESS")
    
    if not recipient_email:
        print("⚠️ 未配置收件人邮箱")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    subject = f"🌿 山茶油每日信息摘要 - {today}"
    body = create_email_body()
    
    # 尝试发送邮件
    send_email(recipient_email, subject, body, is_html=False)

if __name__ == "__main__":
    try:
        main()
        print("✅ 邮件脚本执行完成")
    except Exception as e:
        print(f"❌ 错误: {e}")
        # 不中断工作流
        exit(0)
