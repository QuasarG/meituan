import os
import pandas as pd

def transform_data():
    # 定义数据文件路径
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    processed_data_dir = os.path.join(data_dir, 'processed_data')
    output_path = os.path.join(processed_data_dir, 'transformed_merged_data.csv')
    
    # 读取已处理的数据文件
    input_path = os.path.join(processed_data_dir, 'merged_data.csv')
    data = pd.read_csv(input_path)
    
    # 1. 处理gender列：男=1，女=0
    data['gender'] = data['gender'].map({'男': 1, '女': 0})
    
    # 2. 处理weight_weather_level列：根据严重程度映射为数值
    # 示例映射，实际应根据数据情况调整
    weather_level_map = {
        '正常': 0,
        '一般恶劣': 1,
        '恶劣': 2,
        '非常恶劣': 3
    }
    data['weight_weather_level'] = data['weight_weather_level'].map(weather_level_map)
    
    # 3. 拆分wind_grade_range列
    # 示例：将"0~4级"拆分为min_wind=0, max_wind=4
    wind_split = data['wind_grade_range'].str.extract(r'(\d+)~?(\d+)?级')
    data['min_wind'] = wind_split[0].astype(float)
    data['max_wind'] = wind_split[1].fillna(wind_split[0]).astype(float)
    
    # 删除原wind_grade_range列
    data.drop('wind_grade_range', axis=1, inplace=True)
    
    # 保存转换后的数据
    data.to_csv(output_path, index=False)
    print(f"数据转换完成，结果已保存到: {output_path}")
    
    return data

if __name__ == '__main__':
    transform_data()