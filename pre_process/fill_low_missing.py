import pandas as pd
import os

def fill_low_missing_values():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    merged_data_path = os.path.join(processed_data_dir, 'merged_data.csv')
    transformed_merged_data_path = os.path.join(processed_data_dir, 'transformed_merged_data.csv')
    
    try:
        # 读取合并后的数据
        merged_data = pd.read_csv(transformed_merged_data_path)
        
        # 计算各列缺失比例
        missing_ratio = merged_data.isnull().mean()
        
        # 筛选缺失比例低于5%的列
        low_missing_cols = missing_ratio[missing_ratio < 0.05].index.tolist()
        
        print("缺失比例低于5%的列及其缺失率:")
        for col in low_missing_cols:
            print(f"{col}: {missing_ratio[col]*100:.2f}%")
        
        # 对低缺失列用中位数填充
        for col in low_missing_cols:
            # 跳过缺失值为0的列
            missing_count = merged_data[col].isnull().sum()
            if missing_count == 0:
                print(f"\n列 '{col}' 跳过: 无缺失值")
                continue
                
            # 跳过文本内容列
            if merged_data[col].dtype == 'object':
                print(f"\n列 '{col}' 跳过: 文本类型列")
                continue
                
            median_value = merged_data[col].median()
            
            merged_data[col] = merged_data[col].fillna(median_value)
            
            print(f"\n列 '{col}' 处理结果:")
            print(f"- 总缺失率: {missing_ratio[col]*100:.2f}%")
            print(f"- 缺失行数: {missing_count}")
            print(f"- 填充值(中位数): {median_value}")
        
        # 保存处理后的数据
        merged_data.to_csv(os.path.join(processed_data_dir, 'low_missing_filled_transformed_merged_data.csv'), index=False)
        print("\n缺失值填充完成，数据已保存。")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

if __name__ == "__main__":
    fill_low_missing_values()