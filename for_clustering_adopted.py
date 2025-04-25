import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

# Excelファイルから読み込む
file_path = "C:/Users/Ando/Desktop/list.xlsx"
df = pd.read_excel(file_path, sheet_name="list", index_col=0)

# カラム名をインデックスにして左右対象に揃える
df.columns = df.index

# NaNを0で埋める（距離行列の対角など）
df = df.fillna(0)

# squareformで距離ベクトル化
dist_vec = squareform(df)

# linkageで階層クラスタリング
link = linkage(dist_vec, method="ward")

# ヒートマップ＋クラスタリングを描画
sns.clustermap(
    df,
    row_linkage=link,
    col_linkage=link,
    cmap="viridis",
    figsize=(10, 8),
    xticklabels=True,
    yticklabels=True
)

plt.show()


