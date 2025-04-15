"""
特征工程处理脚本

功能：
1. 从原始数据文件读取骑手信息、行为数据和天气数据
2. 进行基础特征提取和衍生特征计算
3. 处理缺失值并合并特征
4. 分析特征相关性并进行特征选择
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取原始数据文件
# 输入：Excel格式的原始数据文件
# 输出：三个DataFrame分别存储天气、骑手行为和骑手信息数据
weather_path = r"data\original_data\weather.xlsx"
behavior_path = r"data\original_data\rider_daily_behavior.xlsx"
info_path = r"data\original_data\rider_information.xlsx"

weather_df = pd.read_excel(weather_path)
behavior_df = pd.read_excel(behavior_path)
info_df = pd.read_excel(info_path)

# 打印每列的不同信息数量
# 功能：统计并显示DataFrame中每列的唯一值数量，用于数据探索
# 输入：DataFrame和文件名
# 输出：打印每列的唯一值统计信息
def print_unique_counts(df, file_name):
    print(f"File: {file_name}")
    for col in df.columns:
        unique_count = df[col].nunique()
        print(f"{col}: {unique_count} unique values")
    print("\n")

print_unique_counts(weather_df, "weather.xlsx")
print_unique_counts(behavior_df, "rider_daily_behavior.xlsx")
print_unique_counts(info_df, "rider_information.xlsx")

# 基础特征提取
# 功能：从骑手信息中提取基础特征，包括计算司龄等
# 输入：原始骑手信息DataFrame
# 输出：包含基础特征的DataFrame
info_df['regist_date'] = pd.to_datetime(info_df['regist_date'], format='%Y%m%d', errors='coerce')
# 计算司龄：当前日期与注册日期的差值转换为年数
info_df['seniority'] = (pd.Timestamp.now() - info_df['regist_date']).dt.days // 365
# 选择基础特征列
info_features = info_df[['gender', 'age', 'seniority']]

# 行为衍生特征提取
# 功能：从骑手行为数据中提取特征，保留rider_id用于合并但后续不加入特征矩阵
# 输入：原始骑手行为DataFrame
# 输出：去除日期列后的行为特征DataFrame
behavior_features = behavior_df.drop(columns=['dt'])

# 确保rider_id列存在
if 'rider_id' not in behavior_df.columns:
    raise ValueError("行为数据中缺少'rider_id'列，请检查原始数据文件")

# 场景衍生特征提取
# 功能：从天气数据中提取数值型特征，将范围字符串拆分为最小最大值
# 输入：原始天气DataFrame
# 输出：包含数值型天气特征的DataFrame
weather_features = weather_df.drop(columns=['dt'])

# 温度范围处理：将'10°~20°'格式拆分为最小和最大值
weather_features['temperature_range_min'] = weather_features['temperature_range'].str.split('~').str[0].str.replace('°', '').astype(float)
weather_features['temperature_range_max'] = weather_features['temperature_range'].str.split('~').str[1].str.replace('°', '').astype(float)

# 体感温度范围处理
weather_features['real_feel_range_min'] = weather_features['real_feel_range'].str.split('~').str[0].str.replace('°', '').astype(float)
weather_features['real_feel_range_max'] = weather_features['real_feel_range'].str.split('~').str[1].str.replace('°', '').astype(float)

# 湿度范围处理
weather_features['humidity_range_min'] = weather_features['humidity_range'].str.split('~').str[0].astype(float)
weather_features['humidity_range_max'] = weather_features['humidity_range'].str.split('~').str[1].astype(float)

# 风力等级处理
weather_features['wind_grade_range_min'] = weather_features['wind_grade_range'].str.split('~').str[0].str.replace('级', '').astype(float)
weather_features['wind_grade_range_max'] = weather_features['wind_grade_range'].str.split('~').str[1].str.replace('级', '').astype(float)

# 风速范围处理
weather_features['wind_range_min'] = weather_features['wind_range'].str.split('~').str[0].astype(float)
weather_features['wind_range_max'] = weather_features['wind_range'].str.split('~').str[1].astype(float)

# 降雨强度范围处理
weather_features['rain_intensity_range_min'] = weather_features['rain_intensity_range'].str.split('~').str[0].astype(float)
weather_features['rain_intensity_range_max'] = weather_features['rain_intensity_range'].str.split('~').str[1].astype(float)

# 合并特征
# 功能：将行为特征、骑手基础特征和天气特征合并为一个DataFrame
# 方法：
# 1. 先通过rider_id合并行为特征和骑手基础特征
# 2. 再通过索引合并天气特征
# 3. 最后移除rider_id列
# 输出：包含所有特征的合并DataFrame
merged_features = pd.merge(behavior_features, info_features, on='rider_id', how='left')
merged_features = pd.merge(merged_features, weather_features, left_index=True, right_index=True, how='left')
merged_features = merged_features.drop(columns=['rider_id'])

# 检查缺失值
# 功能：统计并显示合并后特征的缺失值情况
# 输出：打印每列的缺失值数量
print("Missing values before processing:")
missing_values_before = merged_features.isnull().sum()
print(missing_values_before)

# 处理缺失值
# 数值型特征处理：用中位数填充缺失值
# 原理：中位数对异常值不敏感，适合数值型特征
# 输出：填充后的数值型特征DataFrame
numeric_features = merged_features.select_dtypes(include=[np.number])
print("\nFilling numeric features with median:")
for col in numeric_features.columns:
    if numeric_features[col].isnull().any():
        fill_value = numeric_features[col].median()
        print(f"Filling column '{col}' with median value: {fill_value}")
        numeric_features[col] = numeric_features[col].fillna(fill_value)

# 类别型特征处理：用众数填充缺失值
# 原理：类别型特征最常见的值通常最具代表性
# 输出：填充后的类别型特征DataFrame
categorical_features = merged_features.select_dtypes(include=['object'])
print("\nFilling categorical features with mode:")
for col in categorical_features.columns:
    if categorical_features[col].isnull().any():
        fill_value = categorical_features[col].mode().iloc[0]
        print(f"Filling column '{col}' with mode value: {fill_value}")
        categorical_features[col] = categorical_features[col].fillna(fill_value)

# 合并处理后的特征
# 功能：将填充后的数值型和类别型特征重新合并
# 输出：处理完缺失值的完整特征DataFrame
processed_features = pd.concat([numeric_features, categorical_features], axis=1)

# 再次检查缺失值
# 功能：验证缺失值处理效果
# 输出：处理后每列的缺失值数量
print("\nMissing values after processing:")
missing_values_after = processed_features.isnull().sum()
print(missing_values_after)

# 特征相关性分析
# 功能：计算数值型特征之间的相关系数矩阵
# 输出：相关系数矩阵和热力图可视化
correlation_matrix = numeric_features.corr()

# 绘制热力图
# 功能：可视化特征相关性，帮助识别高度相关特征
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
plt.title("Feature Correlation Heatmap")
plt.show()

# 核心特征优选 - Lasso回归特征选择
# 原理：Lasso回归通过L1正则化将不重要特征的系数压缩为0，实现特征选择
# 步骤：
# 1. 标准化特征数据
# 2. 训练Lasso模型
# 3. 选择系数不为0的特征
# 输出：被选中的重要特征列表
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler

# 准备特征矩阵和目标变量
X = numeric_features.drop(columns=['cnt_waybill_ontime'], errors='ignore')  # 假设目标变量是准时运单数
y = numeric_features['cnt_waybill_ontime']

# 特征标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 训练Lasso模型
lasso = Lasso(alpha=0.01)  # alpha控制正则化强度
lasso.fit(X_scaled, y)

# 获取被选择的特征
selected_features = X.columns[lasso.coef_ != 0]
print("\nSelected Features:", selected_features)

# 构建最终特征矩阵
# 功能：根据特征选择结果构建最终的特征矩阵
# 输出：包含重要特征的DataFrame
final_feature_matrix = processed_features[selected_features]
print("\nFinal Feature Matrix:")
print(final_feature_matrix.head())