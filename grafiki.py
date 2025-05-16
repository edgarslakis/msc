import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Variant caller performance data
data = {
    "Tool": ["Strelka", "FreeBayes", "DeepVariant", "HaplotypeCaller"],
    "Runtime (sec)": [149, 130, 231, 159],
    "Peak RSS (GB)": [0.029, 0.0085, 5.36, 0.353],
    "Disk I/O (MB)": [52.3, 2.5, 783.5, 100.0]
}

df = pd.DataFrame(data)

# Choose a modern, aesthetic palette
palette = sns.color_palette("Set2", n_colors=4)

# Plotting function
def plot_metric(metric, ylabel, filename):
    plt.figure(figsize=(7, 4))
    ax = sns.barplot(x="Tool", y=metric, data=df, palette=palette)

    # Remove gridlines and spines for minimalism
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', which='both', bottom=False)

    # Add bar labels below bars
    for bar, label in zip(ax.patches, df["Tool"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            -0.05 * df[metric].max(),  # Adjust vertical position
            label,
            ha='center', va='top', fontsize=10
        )

    # Remove x-tick labels (we already added them manually)
    ax.set_xticklabels([""] * len(df["Tool"]))

    plt.tight_layout()
    plt.savefig(f"{filename}.png", dpi=300)
    plt.close()

# Generate charts
plot_metric("Runtime (sec)", "Time (sec)", "runtime_comparison")
plot_metric("Peak RSS (GB)", "Peak RSS (GB)", "memory_comparison")
plot_metric("Disk I/O (MB)", "Disk I/O (MB)", "disk_io_comparison")
