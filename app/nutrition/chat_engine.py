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
        "鍑忚剛": "鍑忚剛", "鍑忚偉": "鍑忚偉", "鐦﹁韩": "鍑忚偉", "鍑忛噸": "鍑忚剛",
        "澧炶倢": "澧炶倢", "闀胯倢鑲?: "澧炶倢", "鍋ヨ韩": "澧炶倢",
        "澧為噸": "澧為噸", "闀胯儢": "澧為噸", "鍏昏儢": "澧為噸",
        "琛ラ挋": "琛ラ挋", "琛ヨ": "琛ヨ", "琛ラ搧": "琛ヨ",
        "鎶楁哀鍖?: "鎶楁哀鍖?, "鎶楄“鑰?: "鎶楁哀鍖?,
        "鎶ょ溂": "鎶ょ溂", "鏄庣洰": "鎶ょ溂",
        "鍔╃湢": "鍔╃湢", "澶辩湢": "鍔╃湢", "鐫′笉濂?: "鍔╃湢",
        "閫氫究": "閫氫究", "渚跨": "閫氫究", "鎺掍究": "閫氫究",
    }
    for key, val in goals.items():
        if key in text:
            return val
    return None

def find_health_issue(text):
    issues = {
        "鎰熷啋": "鎰熷啋", "鍙戠儳": "鎰熷啋", "鍜冲椊": "鎰熷啋",
        "渚跨": "渚跨", "鎺掍究鍥伴毦": "渚跨",
        "澶辩湢": "澶辩湢", "鐫′笉鐫€": "澶辩湢",
        "璐": "璐", "姘旇涓嶈冻": "璐", "澶存檿": "璐",
        "楂樿鍘?: "楂樿鍘?, "琛€鍘嬮珮": "楂樿鍘?,
        "楂樿鑴?: "楂樿鑴?, "琛€鑴傞珮": "楂樿鑴?, "鑳嗗浐閱?: "楂樿鑴?,
        "绯栧翱鐥?: "绯栧翱鐥?, "琛€绯栭珮": "绯栧翱鐥?, "琛€绯?: "绯栧翱鐥?,
        "鑳冧笉濂?: "鑳冧笉濂?, "鑳冪棝": "鑳冧笉濂?, "鑳冪梾": "鑳冧笉濂?, "娑堝寲涓嶈壇": "鑳冧笉濂?,
        "鐤插姵": "鐤插姵", "绱?: "鐤插姵", "娌＄簿绁?: "鐤插姵", "涔忓姏": "鐤插姵",
    }
    for key, val in issues.items():
        if key in text:
            return val
    return None

def handle_food_query(text, food_name):
    is_daily = any(w in text for w in ["姣忓ぉ", "澶╁ぉ", "涓€澶?, "姣忔棩", "鑳戒笉鑳藉悆", "鍙互鍚冨悧", "濂藉悧", "濂戒笉"])
    std_name = find_food(food_name)
    if not std_name:
        return None
    food = ALL_FOODS[std_name]
    source = "姘存灉" if std_name in FRUITS else "钄彍" if std_name in VEGETABLES else "鍏朵粬"
    lines = [f"馃崕 **{std_name}**锛坽source}锛?]
    if is_daily and std_name in DAILY_ADVICE:
        lines.append(f"\n馃挕 **姣忓ぉ鍚冨缓璁?*锛歿DAILY_ADVICE[std_name]}")
    lines.append(f"\n馃搳 **钀ュ吇鍚噺锛堟瘡100g锛?*")
    lines.append(f"  鐑噺锛歿food['cal']}kcal")
    lines.append(f"  鑶抽绾ょ淮锛歿food['fiber']}g")
    for nk in ["vc", "va", "ve", "vk", "vb1", "vb2", "vb3", "vb6", "vb9", "vb12"]:
        if nk in food and food[nk] > 0:
            lines.append(f"  {NUTRIENT_NAMES[nk]}锛歿food[nk]}")
    if "protein" in food:
        lines.append(f"  铔嬬櫧璐細{food['protein']}g")
    if "ca" in food:
        lines.append(f"  閽欙細{food['ca']}mg")
    if "omega3" in food:
        lines.append(f"  Omega-3锛歿food['omega3']}g")
    lines.append(f"\n鉁?**鍔熸晥**锛歿'銆?.join(food['benefits'])}")
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
    lines = [f"馃彿锔?**瀵屽惈{nname}鐨勯鐗╂帹鑽?*"]
    fruit_only = '姘存灉' in text and '钄彍' not in text
    veg_only = '钄彍' in text and '姘存灉' not in text
    if not veg_only and rich_fruits:
        lines.append(f"\n馃崕 **姘存灉绫伙紙鎸夊惈閲忔帓搴忥級**锛?)
        for i, (name, data) in enumerate(rich_fruits[:8]):
            lines.append(f"  {i+1}. {name}锛坽data[nk]}锛?)
    if not fruit_only and rich_vegs:
        lines.append(f"\n馃ウ **钄彍绫?*锛?)
        for i, (name, data) in enumerate(rich_vegs[:8]):
            lines.append(f"  {i+1}. {name}锛坽data[nk]}锛?)
    if rich_others:
        lines.append(f"\n鍏朵粬椋熺墿锛?)
        for i, (name, data) in enumerate(rich_others[:5]):
            lines.append(f"  {i+1}. {name}锛坽data[nk]}锛?)
    return "\n".join(lines)

def handle_diet_query(text):
    goal = find_diet_goal(text)
    if not goal:
        return None
    foods = DIET_TIPS.get(goal, [])
    lines = [f"馃幆 **{goal}楗鎺ㄨ崘**"]
    lines.append(f"\n鎺ㄨ崘椋熺墿锛歿'銆?.join(foods)}")
    if goal == "鍑忚剛":
        lines.append("\n馃挕 寤鸿锛氭帶鍒舵€荤儹閲忔憚鍏ワ紝楂樿泲鐧?楂樼氦缁达紝灏戞补灏戠硸锛屽鍠濇按銆傛瘡澶╀繚璇?00g钄彍銆?)
    elif goal == "澧炶倢":
        lines.append("\n馃挕 寤鸿锛氫繚璇佽泲鐧借川鎽勫叆锛堟瘡鍏枻浣撻噸1.6-2g锛夛紝璁粌鍚庡強鏃惰ˉ鍏呯⒊姘?铔嬬櫧銆?)
    elif goal == "鍑忚偉":
        lines.append("\n馃挕 寤鸿锛氭帶鍒剁儹閲忕己鍙?00-500kcal锛屽鍚冮珮绾ょ淮椋熺墿锛岄伩鍏嶉珮绯栭珮娌广€?)
    elif goal == "琛ラ挋":
        lines.append("\n馃挕 寤鸿锛氭惌閰嶇淮鐢熺礌D甯姪閽欏惛鏀讹紝澶氭檼澶槼锛屾瘡澶╁枬鏉墰濂躲€?)
    elif goal == "琛ヨ":
        lines.append("\n馃挕 寤鸿锛氭惌閰嶇淮鐢熺礌C淇冭繘閾佸惛鏀讹紙濡傛瀛愶級锛岄伩鍏嶈尪鍜屽挅鍟″悓鏃舵憚鍏ャ€?)
    return "\n".join(lines)

def handle_health_query(text):
    issue = find_health_issue(text)
    if not issue:
        return None
    tip = HEALTH_TIPS.get(issue, "")
    return f"馃拪 **{issue}楗寤鸿**\n\n{tip}"

def handle_general_help():
    return ("浣犲ソ锛佹垜鏄綘鐨凙I楗鍋ュ悍鍔╂墜 馃\n\n浣犲彲浠ラ棶鎴戯細\n\n"
            "馃崕 **鍏充簬椋熺墿**锛歕n  鈥?銆岃摑鑾撴湁浠€涔堜綔鐢紵銆峔n  鈥?銆岃タ鐡滄瘡澶╁悆濂藉悧锛熴€峔n\n"
            "馃ウ **鍏充簬钀ュ吇绱?*锛歕n  鈥?銆岃ˉ鍏呯淮鐢熺礌C鍚冧粈涔堟按鏋滐紵銆峔n  鈥?銆屽惈缁寸敓绱燗鐨勮敩鑿滄湁鍝簺锛熴€峔n\n"
            "馃幆 **鍏充簬楗鐩爣**锛歕n  鈥?銆屽噺鑴傛湡鍚冧粈涔堝ソ锛熴€峔n  鈥?銆屽鑲屾帹鑽愰鐗┿€峔n\n"
            "馃拪 **鍏充簬鍋ュ悍闂**锛歕n  鈥?銆屼究绉樺悆浠€涔堬紵銆峔n  鈥?銆屾劅鍐掍簡娉ㄦ剰浠€涔堬紵銆峔n\n璇曡瘯鐪嬪惂锛?)

def chat(query):
     if not query or not query.strip():
         return "璇疯緭鍏ヤ綘鐨勯棶棰?
     text = query.strip()
     if text in ["甯姪", "help", "浣犲ソ", "hi", "鍔熻兘", "鑿滃崟"]:
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
     return ("鎶辨瓑锛屾垜鏆傛椂鏃犳硶鍥炵瓟杩欎釜闂 馃槄\n\n"
             "浣犲彲浠ヨ瘯璇曢棶锛歕n"
             "  \u2022 銆岃摑鑾撴湁浠€涔堜綔鐢紵銆峔n"
             "  \u2022 銆岃タ鐡滄瘡澶╁悆濂藉悧锛熴€峔n"
             "  \u2022 銆岃ˉ鍏呯淮鐢熺礌C鍚冧粈涔堬紵銆峔n"
             "  \u2022 銆屽噺鑴傛湡鍚冧粈涔堝ソ锛熴€峔n"
             "  \u2022 銆屼究绉樹簡鍚冧粈涔堬紵銆?)