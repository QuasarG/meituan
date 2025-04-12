import pandas as pd
import os

def calculate_missing_values():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    input_path = os.path.join(processed_data_dir, 'merged_data.csv')
    
    # 读取CSV文件
    df = pd.read_csv(input_path)
    
    # 统一处理缺失值 - 将空字符串和'信息缺失'文本都转换为NaN
    df = df.replace(['', '信息缺失'], pd.NA)
    
    # 计算每列缺失值比例
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    
    # 输出结果
    print("各列缺失值比例(%):")
    print(missing_percentage.round(2))
    
    # 保存结果到文件
    output_path = os.path.join(processed_data_dir, 'missing_values_report.txt')
    with open(output_path, 'w') as f:
        f.write("各列缺失值比例(%):\n")
        f.write(missing_percentage.round(2).to_string())
    print(f"\n缺失值统计报告已保存到: {output_path}")

if __name__ == "__main__":
    calculate_missing_values()