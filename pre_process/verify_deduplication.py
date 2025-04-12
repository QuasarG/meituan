import pandas as pd
import os

def verify_deduplication():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    deduplicated_path = os.path.join(processed_data_dir, 'deduplicated_rider_behavior.xlsx')
    
    try:
        # 读取文件
        deduplicated_data = pd.read_excel(deduplicated_path)
        
        # 计算不重复骑手ID数量
        unique_ids = deduplicated_data['rider_id'].nunique()
        
        # 计算每个骑手的工作天数总和
        work_days_per_rider = deduplicated_data.groupby('rider_id').size()
        total_work_days = work_days_per_rider.sum()
        
        # 验证公式
        is_correct = total_work_days == len(deduplicated_data)
        
        # 输出结果
        print(f"去重后数据总行数: {len(deduplicated_data)}")
        print(f"不重复骑手ID数量: {unique_ids}")
        print(f"所有骑手工作天数总和: {total_work_days}")
        print(f"验证结果: {'通过' if is_correct else '不通过'}")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

if __name__ == "__main__":
    verify_deduplication()