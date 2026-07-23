import re
from .food_data import (ALL_FOODS, FRUITS, VEGETABLES, NUTRIENT_NAMES, NUTRIENT_SHORT,
                         DIET_TIPS, HEALTH_TIPS, ALIAS_TO_FOOD, DAILY_ADVICE)

def find_food(name):
    if name in ALL_FOODS:
        return name
    return ALIAS_TO_FOOD.get(name)

def get_nutrient_key(text):
    text = text.lower().strip()
    for key, val in NUTRIENT_SHORT.items():
        if key in text:
            return val
    return None

def find_diet_goal(text):
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
    is_daily = any(w in text for w in ["每天", "天天", "一天", "每日", "能不能吃", "可以吃吗", "好吗", "好不"])
    std_name = find_food(food_name)
    if not std_name:
        return None
    food = ALL_FOODS[std_name]
    source = "水果" if std_name in FRUITS else "蔬菜" if std_name in VEGETABLES else "其他"
    lines = [f"🍎 **{std_name}**（{source}）"]
    if is_daily and std_name in DAILY_ADVICE:
        lines.append(f"\n💡 **每天吃建议**：{DAILY_ADVICE[std_name]}")
    lines.append(f"\n📊 **营养含量（每100g）**")
    lines.append(f"  热量：{food['cal']}kcal")
    lines.append(f"  膳食纤维：{food['fiber']}g")
    for nk in ["vc", "va", "ve", "vk", "vb1", "vb2", "vb3", "vb6", "vb9", "vb12"]:
        if nk in food and food[nk] > 0:
            lines.append(f"  {NUTRIENT_NAMES[nk]}：{food[nk]}")
    if "protein" in food:
        lines.append(f"  蛋白质：{food['protein']}g")
    if "ca" in food:
        lines.append(f"  钙：{food['ca']}mg")
    if "omega3" in food:
        lines.append(f"  Omega-3：{food['omega3']}g")
    lines.append(f"\n✨ **功效**：{'、'.join(food['benefits'])}")
    return "\n".join(lines)

def handle_nutrient_query(text, nutrient_key):
    nk = nutrient_key
    nname = NUTRIENT_NAMES.get(nk, nk.upper())
    rich_fruits = [(name, data) for name, data in FRUITS.items() if nk in data and data[nk] > 0]
    rich_vegs = [(name, data) for name, data in VEGETABLES.items() if nk in data and data[nk] > 0]
    rich_others = [(name, data) for name, data in ALL_FOODS.items()
                   if name not in FRUITS and name not in VEGETABLES and nk in data and data[nk] > 0]
    rich_fruits.sort(key=lambda x: x[1].get(nk, 0), reverse=True)
    rich_vegs.sort(key=lambda x: x[1].get(nk, 0), reverse=True)
    lines = [f"🏷️ **富含{nname}的食物推荐**"]
    fruit_only = '水果' in text and '蔬菜' not in text
    veg_only = '蔬菜' in text and '水果' not in text
    if not veg_only and rich_fruits:
        lines.append(f"\n🍎 **水果类（按含量排序）**：")
        for i, (name, data) in enumerate(rich_fruits[:8]):
            lines.append(f"  {i+1}. {name}（{data[nk]}）")
    if not fruit_only and rich_vegs:
        lines.append(f"\n🥦 **蔬菜类**：")
        for i, (name, data) in enumerate(rich_vegs[:8]):
            lines.append(f"  {i+1}. {name}（{data[nk]}）")
    if rich_others:
        lines.append(f"\n其他食物：")
        for i, (name, data) in enumerate(rich_others[:5]):
            lines.append(f"  {i+1}. {name}（{data[nk]}）")
    return "\n".join(lines)

def handle_diet_query(text):
    goal = find_diet_goal(text)
    if not goal:
        return None
    foods = DIET_TIPS.get(goal, [])
    lines = [f"🎯 **{goal}饮食推荐**"]
    lines.append(f"\n推荐食物：{'、'.join(foods)}")
    if goal == "减脂":
        lines.append("\n💡 建议：控制总热量摄入，高蛋白+高纤维，少油少糖，多喝水。每天保证500g蔬菜。")
    elif goal == "增肌":
        lines.append("\n💡 建议：保证蛋白质摄入（每公斤体重1.6-2g），训练后及时补充碳水+蛋白。")
    elif goal == "减肥":
        lines.append("\n💡 建议：控制热量缺口300-500kcal，多吃高纤维食物，避免高糖高油。")
    elif goal == "补钙":
        lines.append("\n💡 建议：搭配维生素D帮助钙吸收，多晒太阳，每天喝杯牛奶。")
    elif goal == "补血":
        lines.append("\n💡 建议：搭配维生素C促进铁吸收（如橙子），避免茶和咖啡同时摄入。")
    return "\n".join(lines)

def handle_health_query(text):
    issue = find_health_issue(text)
    if not issue:
        return None
    tip = HEALTH_TIPS.get(issue, "")
    return f"💊 **{issue}饮食建议**\n\n{tip}"

def handle_general_help():
    return ("你好！我是你的AI饮食健康助手 🥗\n\n你可以问我：\n\n"
            "🍎 **关于食物**：\n  • 「蓝莓有什么作用？」\n  • 「西瓜每天吃好吗？」\n\n"
            "🥦 **关于营养素**：\n  • 「补充维生素C吃什么水果？」\n  • 「含维生素A的蔬菜有哪些？」\n\n"
            "🎯 **关于饮食目标**：\n  • 「减脂期吃什么好？」\n  • 「增肌推荐食物」\n\n"
            "💊 **关于健康问题**：\n  • 「便秘吃什么？」\n  • 「感冒了注意什么？」\n\n试试看吧！")

def chat(query):
     if not query or not query.strip():
         return "请输入你的问题"
     text = query.strip()
     if text in ["帮助", "help", "你好", "hi", "功能", "菜单"]:
         return handle_general_help()
     found = None
     for wl in [4,3,2]:
         for i in range(len(text)-wl+1):
             c = text[i:i+wl]
             if c in ALL_FOODS or c in ALIAS_TO_FOOD:
                 found = c; break
         if found: break
     if found:
         if found in ALIAS_TO_FOOD:
             found = ALIAS_TO_FOOD[found]
         r = handle_food_query(text, found)
         if r: return r
     nk = get_nutrient_key(text)
     if nk:
         r = handle_nutrient_query(text, nk)
         if r: return r
     r = handle_diet_query(text)
     if r: return r
     r = handle_health_query(text)
     if r: return r
     return ("抱歉，我暂时无法回答这个问题 😅\n\n"
             "你可以试试问：\n"
             "  \u2022 「蓝莓有什么作用？」\n"
             "  \u2022 「西瓜每天吃好吗？」\n"
             "  \u2022 「补充维生素C吃什么？」\n"
             "  \u2022 「减脂期吃什么好？」\n"
             "  \u2022 「便秘了吃什么？」")