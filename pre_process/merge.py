import pandas as pd
import os
from tqdm import tqdm

def merge_data():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')

    # 确保处理结果目录存在
    os.makedirs(processed_data_dir, exist_ok=True)

    # 原始数据文件路径
    rider_info_path = os.path.join(original_data_dir, 'rider_information.xlsx')
    rider_behavior_path = os.path.join(original_data_dir, 'rider_daily_behavior.xlsx')
    weather_path = os.path.join(original_data_dir, 'weather.xlsx')

    # 读取Excel文件
    rider_info = pd.read_excel(rider_info_path)
    rider_behavior = pd.read_excel(rider_behavior_path)
    weather = pd.read_excel(weather_path)
    
    # 合并骑手信息和行为数据
    try:
        merged = pd.merge(rider_info, rider_behavior, on='rider_id', how='outer')
        print(f"成功合并骑手信息和行为数据，共{len(merged)}条记录")
        
        # 检查未匹配的骑手ID
        info_only = rider_info[~rider_info['rider_id'].isin(rider_behavior['rider_id'])]
        behavior_only = rider_behavior[~rider_behavior['rider_id'].isin(rider_info['rider_id'])]
        
        # 输出统计信息
        print(f"\n只在骑手信息表中存在的骑手ID数量: {len(info_only)}")
        print(f"只在行为数据表中存在的骑手ID数量: {len(behavior_only)}")
        
        if not info_only.empty or not behavior_only.empty:
            print("\n警告: 发现无法匹配的骑手ID")
            print("1. 骑手信息表中存在但行为数据表中不存在的骑手ID")
            print("2. 行为数据表中存在但骑手信息表中不存在的骑手ID")
        else:
            print("\n所有骑手ID在两个表格中都能匹配")
            
        # 合并天气数据
        final_merged = pd.merge(merged, weather, on='dt', how='left')
        
        # 新增：统计某一列不重复元素数量（例如统计rider_id列）
        unique_count = final_merged['rider_id'].nunique()
        print(f"\n不重复的骑手ID数量: {unique_count}")

        # 检查天气数据合并情况
        weather_unmatched = final_merged[final_merged['dt'].isna() | final_merged[weather.columns].isnull().any(axis=1)]
        if not weather_unmatched.empty:
            print(f"警告: 发现{len(weather_unmatched)}条记录缺少天气数据")
        
        # 保存合并后的数据（分块处理）
        output_path = os.path.join(processed_data_dir, 'merged_data.csv')
        
        # 分块写入CSV
        chunk_size = 50000
        header = True  # 只在第一次写入时包含表头
        for i in tqdm(range(0, len(final_merged), chunk_size), desc="正在写入CSV"):
            chunk = final_merged.iloc[i:i + chunk_size]
            chunk.to_csv(output_path, mode='a', index=False, header=header)
            header = False  # 后续写入不包含表头
            # 内存监控
            if i % (chunk_size * 5) == 0:
                import psutil
                mem = psutil.virtual_memory()
                print(f"当前内存使用情况: 已用{mem.used/1024/1024:.2f}MB, 可用{mem.available/1024/1024:.2f}MB")
        
        print(f"数据已成功保存到{output_path}")
        
    except Exception as e:
        import traceback
        print(f"\n合并过程中发生错误: {str(e)}")
        print("错误详细信息:")
        print(traceback.format_exc())
        print("\n当前数据文件状态:")
        print(f"骑手信息表行数: {len(rider_info) if 'rider_info' in locals() else '未加载'}")
        print(f"行为数据表行数: {len(rider_behavior) if 'rider_behavior' in locals() else '未加载'}")
        print(f"天气表行数: {len(weather) if 'weather' in locals() else '未加载'}")
        return None
    
    return final_merged

if __name__ == '__main__':
    merged_data = merge_data()
    print("数据合并完成，共合并", len(merged_data), "条记录")