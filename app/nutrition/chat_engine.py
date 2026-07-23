import re
from .food_data import (ALL_FOODS, FRUITS, VEGETABLES, NUTRIENT_NAMES, NUTRIENT_SHORT,
                         DIET_TIPS, HEALTH_TIPS, ALIAS_TO_FOOD)


def find_food(name):
    """通过名称或别名查找食物"""
    if name in ALL_FOODS:
        return name
    return ALIAS_TO_FOOD.get(name)


def get_nutrient_key(text):
    """从文本中提取营养素关键词"""
    text = text.lower().strip()
    for key, val in NUTRIENT_SHORT.items():
        if key in text:
            return val
    return None


def find_diet_goal(text):
    """从文本中提取饮食目标"""
    goals = {
        "减脂": "减脂", "减肥": "减肥", "瘦身": "减肥", "减重": "减脂",
        "增肌": "增肌", "长肌肉": "增肌", "健身": "增肌",
        "增重": "增重", "长胖": "增重", "养胖": "增重",
        "补钙": "补钙", "补血": "补血", "补铁": "补血",
        "抗氧化": "抗氧化", "抗衰老": "抗氧化",
        "护眼": "护眼", "明目": "护眼",
        "助眠": "助眠", "失眠": "助眠", "睡不好": "助眠",
        "通便": "通便", "便秘": "通便", "排便": "通便",
    }
    for key, val in goals.items():
        if key in text:
            return val
    return None


def find_health_issue(text):
    """从文本中提取健康问题"""
    issues = {
        "感冒": "感冒", "发烧": "感冒", "咳嗽": "感冒",
        "便秘": "便秘", "排便困难": "便秘",
        "失眠": "失眠", "睡不着": "失眠",
        "贫血": "贫血", "气血不足": "贫血", "头晕": "贫血",
        "高血压": "高血压", "血压高": "高血压",
        "高血脂": "高血脂", "血脂高": "高血脂", "胆固醇": "高血脂",
        "糖尿病": "糖尿病", "血糖高": "糖尿病", "血糖": "糖尿病",
        "胃不好": "胃不好", "胃痛": "胃不好", "胃病": "胃不好", "消化不良": "胃不好",
        "疲劳": "疲劳", "累": "疲劳", "没精神": "疲劳", "乏力": "疲劳",
    }
    for key, val in issues.items():
        if key in text:
            return val
    return None


def handle_food_query(text, food_name):
    """处理关于某种食物的查询"""
    std_name = find_food(food_name)
    if not std_name:
        return None
    food = ALL_FOODS[std_name]
    source = "水果" if std_name in FRUITS else "蔬菜" if std_name in VEGETABLES else "其他"
    lines = [f"🍎 **{std_name}**（{source}）"]
    lines.append(f"热量：{food['cal']}kcal/100g")
    lines.append(f"膳食纤维：{food['fiber']}g/100g")
    has_vitamin = False
    for nk in ["vc", "va", "ve", "vk", "vb1", "vb2", "vb3", "vb6", "vb9", "vb12"]:
        if nk in food and food[nk] > 0:
            lines.append(f"{NUTRIENT_NAMES[nk]}：{food[nk]}")
            has_vitamin = True
    if "protein" in food:
        lines.append(f"蛋白质：{food['protein']}g/100g")
    if "ca" in food:
        lines.append(f"钙：{food['ca']}mg/100g")
    if "omega3" in food:
        lines.append(f"Omega-3：{food['omega3']}g/100g")
    lines.append(f"\n功效：{'、'.join(food['benefits'])}")
    return "\n".join(lines)


def handle_nutrient_query(text, nutrient_key):
    """处理关于某种营养素的查询"""
    nk = nutrient_key
    nname = NUTRIENT_NAMES.get(nk, nk.upper())
    rich_fruits = [(name, data) for name, data in FRUITS.items() if nk in data and data[nk] > 0]
    rich_vegs = [(name, data) for name, data in VEGETABLES.items() if nk in data and data[nk] > 0]
    rich_others = [(name, data) for name, data in ALL_FOODS.items()
                   if name not in FRUITS and name not in VEGETABLES and nk in data and data[nk] > 0]
    rich_fruits.sort(key=lambda x: x[1].get(nk, 0), reverse=True)
    rich_vegs.sort(key=lambda x: x[1].get(nk, 0), reverse=True)
    lines = [f"🏷️ **富含{nname}的食物推荐**"]
    if re.search(r'水果|果', text) or not re.search(r'蔬菜|菜', text):
        if rich_fruits:
            lines.append(f"\n🍎 水果类（按含量排序）：")
            for i, (name, data) in enumerate(rich_fruits[:8]):
                lines.append(f"  {i+1}. {name}（{data[nk]}）")
    if re.search(r'蔬菜|菜', text) or not re.search(r'水果|果', text):
        if rich_vegs:
            lines.append(f"\n🥦 蔬菜类：")
            for i, (name, data) in enumerate(rich_vegs[:8]):
                lines.append(f"  {i+1}. {name}（{data[nk]}）")
    if rich_others:
        lines.append(f"\n其他食物：")
        for i, (name, data) in enumerate(rich_others[:5]):
            lines.append(f"  {i+1}. {name}（{data[nk]}）")
    return "\n".join(lines)


def handle_diet_query(text):
    """处理关于饮食目标的查询"""
    goal = find_diet_goal(text)
    if not goal:
        return None
    foods = DIET_TIPS.get(goal, [])
    lines = [f"🎯 **{goal}饮食推荐**"]
    lines.append(f"\n推荐食物：{'、'.join(foods)}")
    if goal == "减脂":
        lines.append("\n💡 建议：控制总热量摄入，高蛋白+高纤维，少油少糖，多喝水。")
    elif goal == "增肌":
        lines.append("\n💡 建议：保证蛋白质摄入，训练后及时补充，碳水+蛋白搭配。")
    elif goal == "减肥":
        lines.append("\n💡 建议：控制热量缺口，多吃高纤维食物，避免高糖高油。")
    elif goal == "补钙":
        lines.append("\n💡 建议：搭配维生素D帮助钙吸收，多晒太阳。")
    elif goal == "补血":
        lines.append("\n💡 建议：搭配维生素C促进铁吸收，避免茶和咖啡同时摄入。")
    return "\n".join(lines)


def handle_health_query(text):
    """处理关于健康问题的查询"""
    issue = find_health_issue(text)
    if not issue:
        return None
    tip = HEALTH_TIPS.get(issue, "")
    return f"💊 **{issue}饮食建议**\n\n{tip}"


def handle_general_help():
    """返回帮助信息"""
    return ("你好！我是你的AI饮食健康助手 🥗\n\n"
            "你可以问我以下问题：\n\n"
            "🍎 **关于食物**：\n"
            "  • 「蓝莓有什么作用？」\n"
            "  • 「橙子的营养价值」\n\n"
            "🥦 **关于营养素**：\n"
            "  • 「补充维生素C吃什么水果？」\n"
            "  • 「含维生素A的蔬菜有哪些？」\n\n"
            "🎯 **关于饮食目标**：\n"
            "  • 「减脂期吃什么好？」\n"
            "  • 「增肌推荐食物」\n\n"
            "💊 **关于健康问题**：\n"
            "  • 「便秘吃什么？」\n"
            "  • 「感冒了饮食注意什么？」\n\n试试看吧！")


def chat(query):
    """主函数：处理用户问题，返回回答"""
    if not query or not query.strip():
        return "请输入你的问题"
    text = query.strip()
    # 帮助
    if text in ["帮助", "help", "你好", "hi", "功能", "菜单"]:
        return handle_general_help()
    # 检查是否询问食物
    food_match = re.search(r'[（(]?([\u4e00-\u9fff]{2,4})[）)]?(?:的|有|含|作用|功效|营养|好处|价值)', text)
    if not food_match:
        food_match = re.search(r'([\u4e00-\u9fff]{2,4})(?:的益处|的好处|作用|功效|营养|热量|卡路里)', text)
    if not food_match:
        food_match = re.search(r'^(?:请问|我想问|告诉我|推荐)?([\u4e00-\u9fff]{2,4})[，,、]', text)
    if not food_match:
        food_match = re.search(r'([\u4e00-\u9fff]{2,4})是(?:什么|哪些|啥)', text)
    if food_match:
        candidate = food_match.group(1)
        if find_food(candidate):
            result = handle_food_query(text, candidate)
            if result:
                return result
    # 检查食物名称（直接出现在问题中）
    for wl in [4,3,2]:
        for i in range(len(text)-wl+1):
            c = text[i:i+wl]
            if c in ALL_FOODS or c in ALIAS_TO_FOOD:
                if c in ALIAS_TO_FOOD:
                    c = ALIAS_TO_FOOD[c]
                r = handle_food_query(text, c)
                if r:
                    return r
    # 检查营养素
    nk = get_nutrient_key(text)
    if nk:
        result = handle_nutrient_query(text, nk)
        if result:
            return result
    # 检查饮食目标
    result = handle_diet_query(text)
    if result:
        return result
    # 检查健康问题
    result = handle_health_query(text)
    if result:
        return result
    # 没匹配到，返回帮助
    return ("抱歉，我暂时无法回答这个问题 😅\n\n"
            "你可以试试问：\n"
            "• 「蓝莓有什么作用？」\n"
            "• 「补充维生素C吃什么？」\n"
            "• 「减脂期吃什么好？」\n"
            "• 「便秘了吃什么？」")
