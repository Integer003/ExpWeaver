from mcp.server.fastmcp import FastMCP

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
mcp = FastMCP()

import io
import os
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
            try:
                val = summary_dict.get(p, {}).get("value", np.nan)
            except:
                val = summary_dict.get(p, {})
            row.append(val)
        summary.append(row)
    sns.set_theme()

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

@mcp.tool()
def plot_with_errorband_mcp(
    csv_list: list[str],
    x: str,
    y: str,
    labels: list[str] = None,
    ci: int = -1
) -> dict:
    """
    绘制带误差带的折线图（多组数据对比）。

    本函数接受多个 CSV 字符串，每个 CSV 视为一组数据，
    将它们合并后绘制在同一张折线图上，不同的组用不同颜色区分。

    参数
    ----------
    csv_list : List[str]
        多个 CSV 格式的字符串，每个字符串对应一组实验数据。
        每个 CSV 至少应包含 x, y 指定的列。
    x : str
        CSV 数据中的横坐标列名（通常是 step 或 timepoint）。
    y : str
        CSV 数据中的纵坐标列名（例如 accuracy, loss, signal）。
    labels : List[str], optional
        每个 CSV 数据对应的标签，用于图例显示（某几个 CSV 为一组，当且仅当他们编号一样）。
        如果未提供，则自动命名为 Group1, Group2, ...
    ci : {"sd", int, None}, default "sd"
        误差带显示方式：
        - -1 表示显示均值 ± 标准差；
        - 整数（如 95）表示 bootstrap 置信区间；
        - 0 表示不绘制误差带。

    返回
    -------
    dict
        返回 MCP 风格的 rich response 格式，包含：
        - markdown: 可直接渲染的图像
        - file: 包含图片文件名和 base64 编码内容

    示例
    -------
    >>> csv1 = df1.to_csv(index=False)
    >>> csv2 = df2.to_csv(index=False)
    >>> result = plot_with_errorband_mcp([csv1, csv2], x="timepoint", y="signal", labels=["ExpA", "ExpB"])
    >>> # result["lineplot_img"]["markdown"] 可在前端渲染图像
    """

    # 合并数据并标记分组
    dfs = []
    if ci == -1: ci = "sd"
    for i, csv_data in enumerate(csv_list):
        df = pd.read_csv(io.StringIO(csv_data))
        group_label = labels[i] if labels and i < len(labels) else f"Group{i+1}"
        df["__group__"] = group_label
        dfs.append(df)
    data_all = pd.concat(dfs, ignore_index=True)

    # 绘图
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=data_all, x=x, y=y, hue="__group__", ci=ci)
    plt.tight_layout()

    # 转 base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "lineplot_img": {
            "markdown": f"![Lineplot with Error Bands](data:image/png;base64,{b64})",
            "file": {"name": "lineplot_with_error_bands.png", "base64": b64}
        }
    }

if __name__ == "__main__":
    mcp.run()
