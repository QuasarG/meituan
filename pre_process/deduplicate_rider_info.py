import pandas as pd
import os

def find_duplicate_rider_ids():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    rider_info_path = os.path.join(original_data_dir, 'rider_information.xlsx')
    
    try:
        # 读取文件
        rider_info = pd.read_excel(rider_info_path)
        
        # 统计每个riderid出现的次数
        riderid_counts = rider_info['rider_id'].value_counts()
        
        # 筛选出出现次数大于1的riderid
        duplicate_ids = riderid_counts[riderid_counts > 1].index.tolist()
        
        # 输出结果
        print(f"重复的骑手ID数量: {len(duplicate_ids)}")
        print("重复的骑手ID列表:", duplicate_ids)
        
        return duplicate_ids
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return []
        
def deduplicate_rider_info():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    rider_info_path = os.path.join(original_data_dir, 'rider_information.xlsx')
    output_path = os.path.join(processed_data_dir, 'deduplicated_rider_info.xlsx')
    
    try:
        # 读取文件
        rider_info = pd.read_excel(rider_info_path)
        
        # 对每个字段统计出现频率并取最高频的值
        def get_most_frequent_value(series):
            if series.empty:
                return None
            value_counts = series.value_counts()
            if value_counts.empty:
                return None
            return value_counts.idxmax()
            
        # 按rider_id分组，对每个字段取最高频的值
        deduplicated = rider_info.groupby('rider_id').agg(get_most_frequent_value).reset_index()
        
        # 保存结果
        deduplicated.to_excel(output_path, index=False)
        print(f"去重后的骑手信息已保存到: {output_path}")
        
        return deduplicated
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    find_duplicate_rider_ids()
    deduplicate_rider_info()