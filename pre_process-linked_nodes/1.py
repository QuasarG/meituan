import networkx as nx
from pyvis.network import Network

# 创建图对象
G = nx.Graph()

# 定义三个中心节点
datasets = [
    ("Rider_Info", "骑手数据"),
    ("Rider_Behavior", "骑手行为数据"),
    ("Weather_Data", "天气数据")
]

# 添加中心节点
for dataset in datasets:
    G.add_node(dataset[0], label=f"{dataset[0]}\n({dataset[1]})",
               title=dataset[1], group=dataset[0], level=0)

# 定义字段关系（保留原始字段对应关系）
fields = {
    "Rider_Info": [
        ("orider_id", "骑手ID"),
        ("ogender", "性别"),
        ("oage", "年龄"),
        ("oeducation_description", "学历"),
        ("oborn_province", "籍贯-省份"),
        ("oregist_date", "注册时间"),
        ("omarriage_status_description", "婚姻状况"),
        ("ochildren_num_description", "子女数")
    ],
    "Rider_Behavior": [
        ("orider_id", "骑手ID"),
        ("odt", "日期"),
        ("ocnt_waybill", "完成单量"),
        ("ocnt_waybill_reject", "拒绝单量"),
        ("ocnt_waybill_ontime", "准时单量"),
        ("ointerval_work", "开工时长"),
        ("ointerval_waybill", "有单时长")
    ],
    "Weather_Data": [
        ("odt", "日期"),
        ("oweight_weather_level", "天气等级"),
        ("otemperature_range", "温度范围"),
        ("oreal_feel_range", "体感温度范围"),
        ("ohumidity_range", "湿度范围"),
        ("owind_grade_range", "风速等级范围"),
        ("owind_range", "风速范围"),
        ("orain_intensity_range", "降水强度范围")
    ]
}

# 创建全局字段节点集合
field_nodes = {}

# 添加字段节点和连接关系（处理共用字段）
for dataset, field_list in fields.items():
    for field in field_list:
        field_name = field[0]
        if field_name not in field_nodes:
            # 创建新节点
            node_id = field_name
            field_nodes[field_name] = node_id
            G.add_node(node_id, label=f"{field_name}\n({field[1]})",
                       title=field[1], group="field", level=1)
        # 建立连接（允许重复连接）
        G.add_edge(dataset, field_nodes[field_name])

# 创建Pyvis网络
nt = Network(
    height='800px',
    width='100%',
    notebook=True,
    bgcolor="white",
    font_color="black",
    cdn_resources='remote'
)

# 将NetworkX图转为Pyvis网络
nt.from_nx(G)

# 设置可视化选项
nt.force_atlas_2based(
    gravity=-30,
    central_gravity=0.02,
    spring_length=120,
    spring_strength=0.1,
    damping=0.9
)

# 显示控制按钮和图谱
nt.show_buttons(filter_=['physics'])
nt.show("dataset_relationship_optimized.html")