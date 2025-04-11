import pandas as pd
import os

def deduplicate_rider_info():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')

    # 确保处理结果目录存在
    os.makedirs(processed_data_dir, exist_ok=True)

    # 原始数据文件路径
    rider_info_path = os.path.join(original_data_dir, 'rider_information.xlsx')
    output_path = os.path.join(processed_data_dir, 'deduplicated_rider_info.xlsx')

    # 读取Excel文件
    rider_info = pd.read_excel(rider_info_path)
    
    # 检查并记录原始数据行数
    original_rows = len(rider_info)
    print(f"原始数据行数: {original_rows}")
    
    # 去重处理
    deduplicated = rider_info.drop_duplicates()
    
    # 检查并记录去重后数据行数
    deduplicated_rows = len(deduplicated)
    print(f"去重后数据行数: {deduplicated_rows}")
    print(f"共删除重复记录: {original_rows - deduplicated_rows}条")
    
    # 保存去重后的数据
    deduplicated.to_excel(output_path, index=False)
    print(f"去重后的数据已保存到: {output_path}")
    
    return deduplicated

if __name__ == '__main__':
    deduplicate_rider_info()