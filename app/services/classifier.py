import re


# 中文分类关键词映射
CATEGORY_KEYWORDS_ZH = {
    "科技": ["AI", "人工智能", "算法", "数据", "软件", "硬件", "编程", "代码",
             "芯片", "互联网", "云", "机器学习", "深度学习", "区块链", "元宇宙",
             "机器人", "5G", "自动驾驶", "VR", "AR", "数字"],
    "财经": ["股票", "基金", "投资", "金融", "银行", "保险", "经济", "市场",
             "股市", "理财", "涨跌", "利润", "营收", "财报", "GDP", "通胀",
             "贸易", "关税", "汇率", "债券"],
    "教育": ["教育", "学校", "大学", "考试", "学习", "课程", "老师", "学生",
             "培训", "学位", "考研", "高考", "留学", "课堂", "教材", "作业",
             "知识", "教学", "毕业"],
    "体育": ["足球", "篮球", "比赛", "冠军", "奥运", "世界杯", "NBA", "中超",
             "运动员", "教练", "进球", "决赛", "金牌", "赛季", "联赛",
             "C罗", "梅西", "詹姆斯", "F1", "网球"],
    "娱乐": ["电影", "音乐", "综艺", "明星", "演员", "导演", "歌手", "演唱会",
             "电视剧", "票房", "视频", "游戏", "抖音", "快手", "直播",
             "艺人", "微博", "热搜", "粉丝", "偶像", "综艺"],
    "健康": ["健康", "医疗", "医院", "医生", "药物", "疫苗", "手术", "疾病",
             "中医", "养生", "健身", "运动", "营养", "饮食", "心理",
             "睡眠", "体检", "康复", "癌症", "糖尿病"],
    "时政": ["政策", "政府", "法律", "立法", "议会", "总统", "选举", "外交",
             "军事", "国防", "改革", "宪法", "法院", "条约", "制裁",
             "议会", "部长", "总理", "主席", "谈判"],
}

# 英文分类关键词映射
CATEGORY_KEYWORDS_EN = {
    "Tech": ["AI", "artificial intelligence", "algorithm", "software", "code",
             "chip", "internet", "cloud", "machine learning", "blockchain",
             "robot", "data", "programming", "startup", "digital", "app",
             "computer", "innovation", "cyber"],
    "Finance": ["stock", "fund", "investment", "bank", "finance", "market",
                "trading", "profit", "revenue", "GDP", "inflation", "trade",
                "tariff", "bond", "crypto", "bitcoin", "economy", "tax"],
    "Education": ["education", "school", "university", "college", "exam",
                  "study", "course", "teacher", "student", "degree",
                  "research", "learning", "classroom", "scholarship"],
    "Sports": ["football", "soccer", "basketball", "game", "champion",
               "Olympic", "player", "coach", "goal", "final", "medal",
               "season", "league", "tennis", "race", "NBA", "FIFA"],
    "Entertainment": ["movie", "music", "film", "actor", "singer", "concert",
                      "TV", "show", "game", "video", "streaming", "celebrity",
                      "Hollywood", "award", "drama", "album", "song"],
    "Health": ["health", "medical", "hospital", "doctor", "drug", "vaccine",
               "surgery", "disease", "fitness", "nutrition", "mental",
               "sleep", "cancer", "therapy", "wellness", "medicine"],
    "Politics": ["policy", "government", "law", "parliament", "president",
                 "election", "diplomacy", "military", "defense", "reform",
                 "court", "treaty", "sanction", "minister", "vote"],
}


def classify(text: str, lang: str = "zh") -> dict:
    """基于关键词匹配的文本分类"""
    keywords_map = CATEGORY_KEYWORDS_ZH if lang == "zh" else CATEGORY_KEYWORDS_EN
    text_lower = text.lower()

    scores = {}
    for category, keywords in keywords_map.items():
        score = 0
        for kw in keywords:
            pattern = re.compile(re.escape(kw), re.IGNORECASE)
            matches = pattern.findall(text_lower)
            score += len(matches)
        if score > 0:
            scores[category] = score

    if not scores:
        return {"category": "其他", "confidence": 0.0}

    best_category = max(scores, key=scores.get)
    total = sum(scores.values())
    confidence = round(scores[best_category] / total, 4)

    return {"category": best_category, "confidence": confidence}
