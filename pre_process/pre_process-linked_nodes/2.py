import networkx as nx
from pyvis.network import Network

# 创建图对象
G = nx.Graph()

# 定义三个中心节点
datasets = [
    ("Order_Basic", "运单基础信息"),
    ("Merchant_Business", "商家与业务信息"),
    ("Delivery_Time", "配送与时间信息")
]

# 添加中心节点
for dataset in datasets:
    G.add_node(dataset[0], label=f"{dataset[0]}\n({dataset[1]})",
               title=dataset[1], group=dataset[0], level=0)

# 定义字段关系
fields = {
    "Order_Basic": [
        ("owaybill_id", "运单ID"),
        ("orider_id", "骑手ID"),
        ("odt", "日期"),
        ("oweek_id", "周开始日期"),
        ("ois_weekend", "是否周末")
    ],
    "Merchant_Business": [
        ("opoi_id", "商家id"),
        ("opoi_name", "商家名称"),
        ("opoi_first_tag_name", "商家一级品类name"),
        ("opoi_second_tag_name", "商家二级品类name"),
        ("opoi_third_tag_name", "商家三级品类name"),
        ("ois_qike_poi", "是否企客商家"),
        ("obusi_source", "商家业务来源"),
        ("obusi_source_second_level", "商家二级业务来源"),
        ("oorder_source", "订单来源"),
        ("oservice_pkg_type", "sla服务包类型"),
        ("ois_prebook", "是否预定单"),
        ("opkg_value", "包裹原价"),
        ("opkg_price", "包裹优惠后价格")
    ],
    "Delivery_Time": [
        ("odelivery_distance", "配送导航距离"),
        ("opushmeal_poi_confirm_interval", "商户出餐时长"),
        ("odelivery_total_interval", "配送总时长"),
        ("ois_grab", "是否骑手接单"),
        ("ois_grab_after_push_in_5_min", "是否5分钟内接单"),
        ("ois_arrived", "是否配送完成单"),
        ("ois_reject", "是否拒绝单"),
        ("ois_delivery_ontime", "是否相对准时单"),
        ("ois_phf_order", "是否拼好饭订单"),
        ("ois_phf_team_order", "是否拼好饭且成团订单"),
        ("ois_grab_badweather", "是否恶劣天气接单"),
        ("ograb_weather_grade", "接单时天气等级"),
        ("odispatch_time", "调度时间"),
        ("orecipient_lat", "取点纬度"),
        ("orecipient_lng", "取点经度"),
        ("osender_lat", "送点纬度"),
        ("osender_lng", "送点经度")
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
nt.show("delivery_matching_optimized.html")