import pandas as pd
import os

def count_unique_rider_ids():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    
    # 数据文件路径
    rider_info_path = os.path.join(original_data_dir, 'rider_information.xlsx')
    rider_behavior_path = os.path.join(original_data_dir, 'rider_daily_behavior.xlsx')
    merged_data_path = os.path.join(processed_data_dir, 'merged_data.csv')
    
    try:
        # 读取文件
        rider_info = pd.read_excel(rider_info_path)
        rider_behavior = pd.read_excel(rider_behavior_path)
        merged_data = pd.read_csv(merged_data_path)
        
        # 计算不重复的骑手ID数量
        unique_info = rider_info['rider_id'].nunique()
        unique_behavior = rider_behavior['rider_id'].nunique()
        unique_merged = merged_data['rider_id'].nunique()
        
        # 输出统计结果
        print(f"骑手信息表中不重复的骑手ID数量: {unique_info}")
        print(f"行为数据表中不重复的骑手ID数量: {unique_behavior}")
        print(f"合并数据表中不重复的骑手ID数量: {unique_merged}")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

if __name__ == "__main__":
    count_unique_rider_ids()