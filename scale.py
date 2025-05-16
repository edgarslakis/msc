import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data
samples = [1, 4, 9, 19, 26, 31]
total_hours = [12.9, 80.6, 170.4, 382.0, 219.4, 439.0]
hours_per_sample = [h / s for h, s in zip(total_hours, samples)]

# Create dataframe
df = pd.DataFrame({
    "Paraugi": samples,
    "Izpildes laiks (h)": total_hours,
    "Viena parauga izpildes laiks (h)": hours_per_sample
})

# Set style and color palette
sns.set_style("white")
palette = sns.color_palette("Set2")

# Create plot
fig, ax1 = plt.subplots(figsize=(8, 5))

# Plot total runtime
ln1 = ax1.plot(df["Paraugi"], df["Izpildes laiks (h)"], marker='o', color=palette[0], label="Izpildes laiks (h)")
ax1.set_ylabel("Izpildes laiks (h)", color=palette[0])
ax1.tick_params(axis='y', labelcolor=palette[0])

# Create second y-axis
ax2 = ax1.twinx()
ln2 = ax2.plot(df["Paraugi"], df["Viena parauga izpildes laiks (h)"], marker='s', color=palette[1], label="Viena parauga izpildes laiks (h)")
ax2.set_ylabel("Viena parauga izpildes laiks (h)", color=palette[1])
ax2.tick_params(axis='y', labelcolor=palette[1])

# Combine legends
# lns = ln1 + ln2
# labels = [l.get_label() for l in lns]
# ax1.legend(lns, labels, loc="upper left")	

# X-axis label
ax1.set_xlabel("Paraugu skaits")

# Clean look
sns.despine(right=False)
plt.tight_layout()
plt.savefig("runtime_combined_plot.png", dpi=300)
plt.close()
