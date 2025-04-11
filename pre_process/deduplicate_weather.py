import os
import pandas as pd
from collections import Counter

def deduplicate_weather():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    original_data_dir = os.path.join(data_dir, 'original_data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')

    # 确保处理结果目录存在
    os.makedirs(processed_data_dir, exist_ok=True)

    # 原始数据文件路径
    weather_path = os.path.join(original_data_dir, 'weather.xlsx')
    output_path = os.path.join(processed_data_dir, 'deduplicated_weather.xlsx')

    # 读取Excel文件
    weather_data = pd.read_excel(weather_path)
    
    # 检查并记录原始数据行数
    original_rows = len(weather_data)
    print(f"原始数据行数: {original_rows}")
    
    # 按日期分组并处理每组数据
    deduplicated_rows = []
    for dt, group in weather_data.groupby('dt'):
        # 对每列取出现频率最高的值
        row = {'dt': dt}
        for col in group.columns:
            if col == 'dt':
                continue
            # 统计该列值的出现频率
            counter = Counter(group[col])
            # 取出现次数最多的值
            most_common = counter.most_common(1)[0][0]
            row[col] = most_common
        deduplicated_rows.append(row)
    
    # 转换为DataFrame
    deduplicated = pd.DataFrame(deduplicated_rows)
    
    # 检查并记录去重后数据行数
    deduplicated_rows_count = len(deduplicated)
    print(f"去重后数据行数: {deduplicated_rows_count}")
    print(f"共删除重复记录: {original_rows - deduplicated_rows_count}条")
    
    # 保存去重后的数据
    deduplicated.to_excel(output_path, index=False)
    print(f"去重后的数据已保存到: {output_path}")
    
    return deduplicated

if __name__ == '__main__':
    deduplicate_weather()