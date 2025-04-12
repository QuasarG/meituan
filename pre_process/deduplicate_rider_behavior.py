import os
import pandas as pd

def find_duplicate_rider_behavior():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    rider_behavior_path = os.path.join(original_data_dir, 'rider_daily_behavior.xlsx')
    
    try:
        # 读取文件
        rider_behavior = pd.read_excel(rider_behavior_path)
        
        # 检查同一rider_id同一天dt是否有不同情况
        duplicates = rider_behavior.duplicated(subset=['rider_id', 'dt'], keep=False)
        duplicate_data = rider_behavior[duplicates]
        
        # 统计重复情况
        duplicate_counts = duplicate_data.groupby(['rider_id', 'dt']).size().reset_index(name='count')
        
        print(f"发现 {len(duplicate_counts)} 组骑手ID和日期的重复记录")
        return duplicate_data
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None

def deduplicate_rider_behavior():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    rider_behavior_path = os.path.join(original_data_dir, 'rider_daily_behavior.xlsx')
    output_path = os.path.join(processed_data_dir, 'deduplicated_rider_behavior.xlsx')
    
    try:
        # 读取文件
        rider_behavior = pd.read_excel(rider_behavior_path)
        
        # 对每个字段统计出现频率并取最高频的值
        def get_most_frequent_value(series):
            if series.empty:
                return None
            value_counts = series.value_counts()
            if value_counts.empty:
                return None
            return value_counts.idxmax()
            
        # 首先删除完全重复的行
        rider_behavior = rider_behavior.drop_duplicates()
        
        # 直接对数据进行排序
        deduplicated = rider_behavior.sort_values(by=['dt', 'rider_id'], ascending=[True, True])
        
        # 保存结果
        deduplicated.to_excel(output_path, index=False)
        print(f"去重后的骑手行为数据已保存到: {output_path}")
        
        return deduplicated
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    # 查找重复记录
    duplicate_data = find_duplicate_rider_behavior()
    
    # 无论是否有重复记录都执行排序
    deduplicated = deduplicate_rider_behavior()
    if deduplicated is not None:
        print("骑手行为数据排序完成")