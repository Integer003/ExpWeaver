
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
import pandas
from pandas import DataFrame

import swanlab
from swanlab.api.types import ApiResponse, Experiment, Project
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
mcp = FastMCP()
@mcp.tool()
def fig_to_base64(fig) -> str:
    """matplotlib Figure -> base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

@mcp.tool()
async def plot_experiment_acc_loss(metrics_csv: str) -> dict:
    """
    从 SwanLab 实验的 CSV 数据绘制一张图，包含两张子图（Accuracy 和 Loss）。
    返回内容既包含 markdown 渲染，也包含可下载的文件。
    """
    df = pd.read_csv(io.StringIO(metrics_csv))
    df["step"] = range(len(df))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))  # 一行两列

    # --- Accuracy ---
    if "acc" in df.columns:
        ax = axes[0]
        ax.plot(df["step"], df["acc"], marker="o", linestyle="-", label="Accuracy")
        ax.set_xlabel("Step")
        ax.set_ylabel("Accuracy")
        ax.set_title("Training Accuracy")
        ax.grid(True)
        ax.legend()
    else:
        axes[0].axis("off")  # 如果没有数据就隐藏

    # --- Loss ---
    if "loss" in df.columns:
        ax = axes[1]
        ax.plot(df["step"], df["loss"], marker="s", linestyle="--", color="red", label="Loss")
        ax.set_xlabel("Step")
        ax.set_ylabel("Loss")
        ax.set_title("Training Loss")
        ax.grid(True)
        ax.legend()
    else:
        axes[1].axis("off")  # 如果没有数据就隐藏

    fig.tight_layout()
    b64 = fig_to_base64(fig)
    plt.close(fig)

    return {
        "merged_img": {
            "markdown": f"![Accuracy & Loss](data:image/png;base64,{b64})",
            "file": {
                "name": "accuracy_loss_curve.png",
                "base64": b64
            }
        }
    }

if __name__ == "__main__":
    mcp.run()