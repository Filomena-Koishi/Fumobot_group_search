import json
import re

with open('group_list.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

extra_pattern = r"\{\{QQ群扩展\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|?([^|]*)\|?(?:图片=(\w+))?\|?(?:链接=(https?://[^\}]+))?\}\}"
pattern_new   = r"\{\{QQ群扩展\|([^|]+)\|\[\[([^\]]+)\]\]\|(\d+)\|([^\}]+)\|([^\}]+)\}\}"

pattern_x = r"\{\{QQ群\|\s*(\[\[[^\]]+\]\]\s*x\s*\[\[[^\]]+\]\])\|(\d+)\|([^\|]+)\|([^\}]+)\}\}"
pattern_special = r"\{\{QQ群\|([^\|]+(?:\[\[[^\]]+\]\](?:，\[\[[^\]]+\]\])*)+)\|(\d+)\|([^\|]+)\|([^\}]+)\}\}"
bar_pattern = r"\{\{QQ群\|([^|]+吧)\|(\d+)\|([^|]+)\|([^\}]+)\}\}"
pattern = r"\{\{QQ群\|([^|]+)\|(\d+)\|([^|]+)\|([^\}]+)\}\}"
pattern_at_least= r"\{\{QQ群\|([^|]+)\|(\d+)\|([^}]+)?\}\}"

group_list = []
for group in data["templates"]:
    if '列表' in group:
        continue
    
    if match := re.match(extra_pattern, group):
        city = match.group(1)
        group = match.group(2)
        gid = match.group(3)
        name = match.group(4)
        try:
            group_description = match.group(5)
        except Exception:
            group_description = '暂无'

        matched_group = {
            '群组类型': '校群或其他',
            '城市或类型': city,
            '所属机构': group,
            '群名': name,
            '群号': gid,
            '群描述': group_description
        }

        group_list.append(matched_group)

    elif match := re.match(pattern_new, group):
        group_type = match.group(1) 
        group_id = match.group(3)   
        group_name = match.group(2)
        real_name = match.group(4)
        try:
            group_description = match.group(5)
        except Exception:
            group_description = '暂无'
        matched_group = {
            '群组类型': '组织',
            '组织类型': group_type,
            '群号': group_id,
            '组织名': group_name,
            '群名': real_name,
            '群描述': group_description
        }

        group_list.append(matched_group)

    elif match := re.match(pattern_x, group):
        group_type = match.group(1) 
        group_id = match.group(2)   
        group_name = match.group(3) 
        group_description = match.group(4)

        matched_group = {
            '群组类型': 'CP',
            '喜好CP': group_type,
            '群号': group_id,
            '群名': group_name,
            '群描述': group_description
        }

        group_list.append(matched_group)

    if match := re.match(pattern_special, group):
        group_type = match.group(1) 
        group_id = match.group(2)   
        group_name = match.group(3) 
        group_description = match.group(4)

        matched_group = {
            '群组类型': '角色',
            '喜好角色': group_type,
            '群号': group_id,
            '群名': group_name,
            '群描述': group_description
        }

        group_list.append(matched_group)

    

    elif match := re.match(bar_pattern, group):
        group_type = match.group(1)  # 群组类型
        group_id = match.group(2)    # 群号
        group_name = match.group(3)  # 群名称
        group_description = match.group(4)  # 群描述

        matched_group = {
            '群组类型': '贴吧',
            '吧名': group_type,
            '群号': group_id,
            '群名': group_name,
            '群描述': group_description
        }

        group_list.append(matched_group)


    elif match := re.match(pattern, group):
        group_type = match.group(1)  # 群组类型
        group_id = match.group(2)    # 群号
        group_name = match.group(3)  # 群名称
        group_description = match.group(4)  # 群描述

        matched_group = {
            '群组类型': '地方或其他',
            '群聊类型': group_type,
            '群号': group_id,
            '群名': group_name,
            '群描述': group_description
        }

        group_list.append(matched_group)

    elif match := re.match(pattern_at_least, group):
        city = match.group(1)       # 城市名称
        group_id = match.group(2)   # 群号
        group_name = match.group(3) # 群名称

        matched_group = {
            '群组类型': '地方',
            '城市': city,
            '群号': group_id,
            '群名': group_name,
        }

        group_list.append(matched_group)    
    

def search(keyword):
    matched_groups = []  # 初始化匹配的群组列表

    # 将关键词转换为小写进行大小写不敏感的匹配
    keyword = keyword.strip().lower()

    # 遍历所有群组，查找匹配的群组
    for group in group_list:
        # 对每个群组字段进行小写处理并去除前后空格
        if (keyword in group.get('群名', '').strip().lower() or
            keyword in group.get('吧名', '').strip().lower() or
            keyword in group.get('群描述', '').strip().lower() or
            keyword in group.get('喜好CP', '').strip().lower() or
            keyword in group.get('喜好角色', '').strip().lower() or
            keyword in group.get('城市或类型', '').strip().lower() or
            keyword in group.get('所属机构', '').strip().lower() or
            keyword in group.get('组织名', '').strip().lower()):
            
            matched_groups.append(group)  # 如果匹配，加入结果列表

    # 如果有匹配的群组，进行分类输出
    if matched_groups:
        # result = [f">>> {keyword} 的结果如下:\n"]
        result = []
        
        categories = ['校群或其他', '组织', 'CP', '角色', '贴吧', '地方', '地方或其他']
        
        # 遍历各个群组类型，输出相应的群组信息
        for category in categories:
            category_groups = [group for group in matched_groups if group['群组类型'] == category]
            
            if category_groups:  # 只有当该类型有匹配的群组时，才输出
                result.append(f"以下是 {category}: ")
                number = 1

                for group in category_groups:
                    
                    # 根据群组类型格式化输出相应的信息
                    if category == '校群或其他':
                        result.append(f"# {number}城市或类型: {group.get('城市或类型', '')}\n所属机构: {group.get('所属机构', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")
                    elif category == '组织':
                        result.append(f"# {number}组织类型: {group.get('组织类型', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")
                    elif category == 'CP':
                        result.append(f"# {number}喜好CP: {group.get('喜好CP', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")
                    elif category == '角色':
                        result.append(f"# {number}喜好角色: {group.get('喜好角色', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")
                    elif category == '贴吧':
                        result.append(f"# {number}吧名: {group.get('吧名', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")
                    elif category == '地方':
                        result.append(f"# {number}群聊类型: {group.get('城市', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n")
                    elif category == '地方或其他':
                        result.append(f"# {number}群聊类型: {group.get('群聊类型', '')}\n群名: {group.get('群名', '')}\n群号: {group.get('群号', '')}\n描述: {group.get('群描述', '')}\n")

                    number += 1

        return result
    else:
        return "没有找到匹配的群组。"