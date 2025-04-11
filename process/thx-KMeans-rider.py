# 导入必要的库
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import os

# 构建相对路径
rider_info_path = r"data/original_data/rider_information.xlsx"  # 骑手信息文件路径
rider_behavior_path = r"data/original_data/rider_daily_behavior.xlsx"  # 骑手行为数据文件路径

# 设置 Matplotlib 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

# 检查文件是否存在
if not os.path.exists(rider_info_path):
    print(f"错误: 文件未找到: {rider_info_path}")
    exit()
if not os.path.exists(rider_behavior_path):
    print(f"错误: 文件未找到: {rider_behavior_path}")
    exit()

# 加载数据
try:
    rider_info = pd.read_excel(rider_info_path)  # 读取骑手信息
    rider_behavior = pd.read_excel(rider_behavior_path)  # 读取骑手行为数据
except FileNotFoundError as e:
    print(f"错误: 文件未找到: {e}")
    exit()
except Exception as e:
    print(f"读取Excel文件错误: {e}")
    exit()

# 数据清洗和预处理
# --- 骑手信息 ---
# 处理缺失值（将'信息缺失'替换为NaN）
rider_info = rider_info.replace('信息缺失', np.nan)

# 将'regist_date'转换为日期格式（处理可能的错误）
try:
    rider_info['regist_date'] = pd.to_datetime(rider_info['regist_date'], format='%Y%m%d', errors='coerce')
except ValueError:
    print("警告: 无法将'regist_date'转换为日期格式。请检查格式。")
    # 选项1：删除列（如果不可用）
    # rider_info = rider_info.drop('regist_date', axis=1)
    # 选项2：用默认日期填充（如果合适）
    rider_info['regist_date'] = pd.to_datetime('1900-01-01') # 或其他合适的默认值

# 将性别转换为数值（0表示女性，1表示男性）
rider_info['gender'] = rider_info['gender'].map({'男': 1, '女': 0})

# 处理缺失的性别值（用众数填充）
rider_info['gender'] = rider_info['gender'].fillna(rider_info['gender'].mode()[0])

# --- 骑手行为数据 ---
# 将'dt'转换为日期格式（处理可能的错误）
try:
    rider_behavior['dt'] = pd.to_datetime(rider_behavior['dt'], format='%Y%m%d', errors='coerce')
except ValueError:
    print("警告: 无法将'dt'转换为日期格式。请检查格式。")
    # 选项1：删除列（如果不可用）
    # rider_behavior = rider_behavior.drop('dt', axis=1)
    # 选项2：用默认日期填充（如果合适）
    rider_behavior['dt'] = pd.to_datetime('1900-01-01') # 或其他合适的默认值

# 特征工程和聚合
# 聚合骑手行为数据（计算每个骑手的平均值）
rider_behavior_agg = rider_behavior.groupby('rider_id').agg({
    'cnt_waybill': 'mean',  # 平均运单数
    'cnt_waybill_reject': 'mean',  # 平均拒单数
    'cnt_waybill_ontime': 'mean',  # 平均准时单数
    'interval_waybill': 'mean',  # 平均接单间隔
    'interval_work': 'mean'  # 平均工作时间间隔
}).reset_index()

# 合并两个数据框
rider_data = pd.merge(rider_info, rider_behavior_agg, on='rider_id', how='inner')

# 选择用于聚类的特征
features = ['gender', 'age', 'cnt_waybill', 'cnt_waybill_reject', 
            'cnt_waybill_ontime', 'interval_waybill', 'interval_work']
rider_data = rider_data.dropna(subset=features)  # 删除选定特征中的缺失值
X = rider_data[features]

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用肘部法则确定最佳聚类数量
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)  # 显式设置n_init
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

# 计算斜率变化
slope_changes = []
for i in range(1, len(inertia)):
    slope_changes.append(abs(inertia[i] - inertia[i-1]))

# 找到斜率变化显著减小的点
optimal_k = 2  # 默认值
for i in range(1, len(slope_changes)):
    if slope_changes[i] < slope_changes[i-1] * 0.5:  # 斜率变化减小超过50%
        optimal_k = i + 1
        break

optimal_k = 3

# 绘制肘部法则图
plt.plot(range(1, 11), inertia, marker='o')
plt.title('肘部法则确定最佳k值')
plt.xlabel('聚类数量')
plt.ylabel('惯性值')
plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'最佳聚类数: {optimal_k}')
plt.legend()
plt.show()

# 执行K-means聚类
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)  # 显式设置n_init
rider_data['cluster'] = kmeans.fit_predict(X_scaled)

# 输出各个聚类的占比
cluster_counts = rider_data['cluster'].value_counts(normalize=True)
print("\n各个聚类占比:")
print(cluster_counts)

# 可视化聚类结果（使用两个特征简化展示）
# 选择两个特征进行可视化（例如'cnt_waybill'和'interval_work'）
feature1 = 'cnt_waybill'
feature2 = 'interval_work'

plt.figure(figsize=(8, 6))
for cluster in range(optimal_k):
    cluster_data = rider_data[rider_data['cluster'] == cluster]
    plt.scatter(cluster_data[feature1], cluster_data[feature2], label=f'聚类 {cluster}')

plt.title('骑手聚类结果')
plt.xlabel(feature1)
plt.ylabel(feature2)
plt.legend()
plt.show()

# 分析聚类结果（计算每个聚类的特征平均值）
cluster_analysis = rider_data.groupby('cluster')[features].mean()
print("\n聚类分析结果:")
print(cluster_analysis)

# 将聚类分析结果保存为CSV文件
cluster_analysis.to_csv(r"E:\竞赛\美团\data_analysis\data\cluster_analysis.csv", index=False)
print("\n聚类分析结果已保存为 cluster_analysis.csv")