import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import wandb
import os

mcp = FastMCP()

RUN_PATH = os.environ["WANDB_RUN_PATH"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
CHECK_INTERVAL = 30
SMTP_SERVER = os.environ["SMTP_SERVER"]
SMTP_PORT = 465  # SSL 端口
SENDER_EMAIL = os.environ["SENDER_EMAIL"]       # 发件人邮箱
SENDER_PASS = os.environ["SENDER_PASS"]     # 发件人邮箱的授权码，而不是登录密码


async def supervise_experiments(run_path:str, receiver_email: str):
    """
    监控指定路径下的实验，检查状态并发送通知。要求用户提供接受通知的邮箱地址。
    Args:
        run_path (str): 实验路径，格式为 "entity/project".
        receiver_email (str): 用户输入的收件人邮箱地址，用于接收实验状态通知。
        
    """
    prev_states = {}  # run.id -> state

    while True:
        api = wandb.Api()
        running_runs = api.runs(path=run_path)  # 获取所有实验，不只 RUNNING
        
        current_states = {run.id: run.state for run in running_runs}
        logging.info(f"当前轮询实验数量: {len(current_states)}")
        for run_id, state in current_states.items():
            logging.info(f"实验 {run_id} 状态: {state}")

        for run_id, state in current_states.items():
            prev_state = prev_states.get(run_id)
            # 状态从 RUNNING -> FINISHED, CRASHED, FAILED
            if prev_state == "running" and state in ["finished", "crashed", "failed"]:
                run_name = next(run.name for run in running_runs if run.id == run_id)
                logging.info(f"实验 {run_name} 已经结束: {state}")
                await send_notification(run_name, state, receiver_email)

        prev_states = current_states
        await asyncio.sleep(CHECK_INTERVAL)

async def send_notification(run_name: str, status: str, receiver_email: str):
    """
    通过邮件向用户发送实验状态通知

    Args:
        run_name (str): 实验名称
        status (str): 实验状态
        receiver_email (str): 用户输入的收件人邮箱地址
    """
    subject = f"W&B 实验 {run_name} 状态更新"
    body = f"🔔 实验 {run_name} 已经 {status}！"

    logging.info(f"准备发送邮件给 {receiver_email}: {body}")

    def send_email_sync():
        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["From"] = formataddr(("W&B Notifier", SENDER_EMAIL))
            msg["To"] = formataddr(("User", receiver_email))
            msg["Subject"] = Header(subject, "utf-8")

            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASS)
                server.sendmail(SENDER_EMAIL, [receiver_email], msg.as_string())

            logging.info("📧 邮件通知已发送成功！")
        except Exception as e:
            logging.error(f"❌ 邮件发送失败: {e}")

    await asyncio.to_thread(send_email_sync)

async def main():
    if not RUN_PATH or not RECEIVER_EMAIL or not SENDER_EMAIL or not SENDER_PASS:
        logging.error("请先设置环境变量 WANDB_RUN_PATH, RECEIVER_EMAIL, SENDER_EMAIL, EMAIL_PASS")
        return
    # 启动后台任务
    asyncio.create_task(supervise_experiments(RUN_PATH, RECEIVER_EMAIL))
    # 启动 MCP
    await mcp.run_sse_async()  # 注意：确保你的 FastMCP 支持 run_async()

if __name__ == "__main__":
    asyncio.run(main())