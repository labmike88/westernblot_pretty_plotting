import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Ensure editable text in SVG
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['DejaVu Sans']

def plot_dotplot(df, df_name="dataset", value_col='ratio', group_col='sample'):
    
    # Make sure that it fits A4 1/8 size for Illustrator handling
    fig_width = 4.13
    fig_height = 2.92
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.set(style="whitegrid")

    # Plot stripplot 
    ax = sns.stripplot(data=df, x=group_col, y=value_col,
                       jitter=True, size=5, color='black', alpha=0.7, ax=ax)

    # Get the actual category order used on the x-axis
    categories = [t.get_text() for t in ax.get_xticklabels()]
    category_to_position = {cat: i for i, cat in enumerate(categories)}

    # Compute summary stats
    summary = df.groupby(group_col)[value_col].agg(['mean', 'std']).reset_index()

    # Add error bars 
    for _, row in summary.iterrows():
        xpos = category_to_position[row[group_col]]
        ax.errorbar(x=xpos, y=row['mean'], yerr=row['std'],
                    fmt='o', color='red', capsize=3, markersize=5)

    # Labels for blots normalized on TBP
    ax.set_title(f'{value_col} levels grouped by {group_col}', fontsize=6)
    ax.set_xlabel(group_col, fontsize=6)
    ax.set_ylabel(f'α-{df_name} normalized on α-TBP', fontsize=6)
    ax.tick_params(axis='both', labelsize=6)

    # Robust y-limits
    y_max = df[value_col].max()
    ax.set_ylim(0, y_max * 1.1 if y_max > 0 else 1)

    # Tighten x spacing
    n_groups = len(categories)
    ax.set_xlim(-0.3, n_groups - 0.7)

    plt.tight_layout()
    fig.savefig(f"{df_name}_dotplot.svg", format="svg")
    plt.show()
    