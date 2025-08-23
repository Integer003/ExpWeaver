from mcp.server.fastmcp import FastMCP

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
mcp = FastMCP()

import io
import base64

@mcp.tool()
def fig_to_base64(fig) -> str:
    """matplotlib Figure -> base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

@mcp.tool()
async def plot_experiment_acc_loss(metrics_csv: str, columns: list = None) -> dict:
    """
    从 SwanLab 实验的 CSV 数据绘制一张图，用户可指定要画的列名列表。
    返回内容既包含 markdown 渲染，也包含可下载的文件。
    Args:
        metrics_csv: CSV 字符串
        columns(可选): 要画的列名列表，默认自动检测所有数值列
    """
    df = pd.read_csv(io.StringIO(metrics_csv))
    df["step"] = range(len(df))
    # 自动检测数值列
    if columns is (None or []):
        columns = [col for col in df.columns if col not in ("step",) and pd.api.types.is_numeric_dtype(df[col])]
    n = len(columns)
    fig, axes = plt.subplots(1, n, figsize=(6*n, 4))
    if n == 1:
        axes = [axes]
    for i, col in enumerate(columns):
        ax = axes[i]
        if col in df.columns:
            ax.plot(df["step"], df[col], marker="o", linestyle="-", label=col)
            ax.set_xlabel("Step")
            ax.set_ylabel(col)
            ax.set_title(col)
            ax.grid(True)
            ax.legend()
        else:
            ax.axis("off")
    fig.tight_layout()
    b64 = fig_to_base64(fig)
    plt.close(fig)
    return {
        "merged_img": {
            "markdown": f"![Curve](data:image/png;base64,{b64})",
            "file": {
                "name": "curve.png",
                "base64": b64
            }
        }
    }

@mcp.tool()
async def plot_contrast_experiments(summary_dict_list: list[dict], param_names: list[str] = None) -> dict:
    """
    对比多个实验的多个参数的 value 字段，绘制热力图。
    Args:
        summary_dict_list: List[dict]，每个实验的 summary dict
        param_names（可选）: List[str]，要对比的参数名（如 acc、loss、f1、auc 等），可选，默认取所有实验参数的并集
    Returns:
        dict: 包含热力图的 markdown 和 base64 文件
    """
    import numpy as np
    # 自动收集所有参数名
    if param_names is (None or []):
        param_set = set()
        for summary_dict in summary_dict_list:
            param_set.update(summary_dict.keys())
        param_names = sorted(param_set)
    summary = []
    for summary_dict in summary_dict_list:
        row = []
        for p in param_names:
            val = summary_dict.get(p, {}).get("value", np.nan)
            row.append(val)
        summary.append(row)

    summary_df = pd.DataFrame(summary, columns=param_names)
    summary_df.index = [f"Exp{i+1}" for i in range(len(summary_dict_list))]

    plt.figure(figsize=(1.2*len(param_names), 1+len(summary_dict_list)))
    ax = sns.heatmap(summary_df, annot=True, fmt=".3g", cmap="YlGnBu")
    plt.title("Experiment Parameter Comparison (value)")
    plt.tight_layout()

    b64 = fig_to_base64(plt.gcf())
    plt.close(plt.gcf())
    return {
        "heatmap_img": {
            "markdown": f"![Param Heatmap](data:image/png;base64,{b64})",
            "file": {
                "name": "param_heatmap.png",
                "base64": b64
            }
        }
    }

if __name__ == "__main__":
    mcp.run()
