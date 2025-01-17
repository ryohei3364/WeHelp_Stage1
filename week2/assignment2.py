# Task 1
def find_and_print(messages, current_station):
    # 1. 建立捷運路線dict
    route = {'main': ['Songshan', 'Najing Sanmin', 'Taipei Arena', 'Nanjing Fuxing', 'Songjiang Najing', 'Zhongshan', 'Beimen', 'Ximen', 
                      'Xiaonanmen', 'Chiang Kai-Shek Memorial Hall', 'Guting', 'Taipower Building', 'Gongguan', 'Wanlong', 'Jingmei', 
                      'Dapinglin', 'Qizhang', 'Xindian City Hall', 'Xindian'],
             'sub': ['Qizhang', 'Xiaobitan']}

    # 2. 建立freind_in_main_index和freind_in_sub_index，格式為 {name: index} {'Leslie': 3, 'Bob': 2, 'Amber': 7}
    friend_in_main_index = {}
    friend_in_sub_index = {}
    for name, message in messages.items():
        for line, stations in route.items():
            if line == "sub":
                for index, station in enumerate(stations):
                    if station in message:
                        friend_in_sub_index[name] = index
            if line == "main":
                for index, station in enumerate(stations):
                    if station in message:
                        friend_in_main_index[name] = index

    # 3. 建立station_list 格式為 {'station':{"main": index, "sub": index}}
    station_index = {}
    # 主線
    for index, station in enumerate(route['main']):
        if station not in station_index:
            station_index[station] = {}
        station_index[station]['main'] = index  
    # 支線
    for index, station in enumerate(route['sub']):
        if station not in station_index:
            station_index[station] = {}
        station_index[station]['sub'] = index  

    # 4. current_index_in_main and current_index_in_sub 
    current_index_in_main = float('inf')
    current_index_in_sub = float('inf')

    if 'main' in station_index[current_station]:
        current_index_in_main = station_index[current_station]['main']
    if 'sub' in station_index[current_station]:
        current_index_in_sub = station_index[current_station]['sub']

    # 5. 建立freind_in_main_distance and freind_in_sub_distance，格式為 {name: distance} {'Leslie': 3, 'Bob': 2, 'Amber': 7}
    friend_in_main_distance = {}
    friend_in_sub_distance = {}
    main_min_distance = float('inf')
    sub_min_distance = float('inf')

    for name, index in friend_in_main_index.items():
        friend_in_main_distance[name] = abs(index - current_index_in_main)
    for name, index in friend_in_sub_index.items():
        friend_in_sub_distance[name] = abs(index - current_index_in_sub)

    main_min_distance = min(friend_in_main_distance.values())
    sub_min_distance = min(friend_in_sub_distance.values())

    # 6. 把friend_in_main_distance的key, value調換，讓value可以作為key查詢dict
    reversed_friend_in_main_distance = {v: k for k, v in friend_in_main_distance.items()}
    reversed_friend_in_sub_distance = {v: k for k, v in friend_in_sub_distance.items()}

    if main_min_distance < sub_min_distance:
        return reversed_friend_in_main_distance[main_min_distance]
    else:
        return reversed_friend_in_sub_distance[sub_min_distance]
    
messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
}
print("=== Task 1 ===")
print(find_and_print(messages, "Wanlong")) # print Mary
print(find_and_print(messages, "Songshan")) # print Copper
print(find_and_print(messages, "Qizhang")) # print Leslie
print(find_and_print(messages, "Ximen")) # print Bob
print(find_and_print(messages, "Xindian City Hall")) # print Vivian

# Task 2
def book(consultants, hour, duration, criteria):
    # 2. 建立評價標準
    if criteria == 'price':
        sorted_consultants = sorted(consultants, key=lambda x: x["price"]) # Jenny, John, Bob
    else:  
        sorted_consultants = sorted(consultants, key=lambda x: x["rate"], reverse=True) # John, Jenny, Bob

    # 3. 依照 sorted_consultants 順序，依序確認時程是否為空的時段
    for consultant in sorted_consultants:
        name = consultant['name']
        if all(h in schedule[name] for h in range(hour, hour + duration)):
            # 從時程中移除該顧問已被預約的時間段
            for h in range(hour, hour + duration):
                schedule[name].remove(h)
            return name
            break
        # 利用三個顧問的時程聯集確認是否沒有空的時段，沒有就pirnt "No Service"
        elif hour not in (schedule['Jenny']|schedule['John']|schedule['Bob']):
            return 'No Service'
            break
         
consultants = [
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]
# 1. 建立consultants schedule
schedule = {consultant['name']:set(range(8, 23)) for consultant in consultants}
# [x for x in range(8, 23)] 可以替換成 set(range(8, 23))

print("=== Task 2 ===")
print(book(consultants, 15, 1, "price")) # Jenny
print(book(consultants, 11, 2, "price")) # Jenny
print(book(consultants, 10, 2, "price")) # John
print(book(consultants, 20, 2, "rate")) # John
print(book(consultants, 11, 1, "rate")) # Bob
print(book(consultants, 11, 2, "rate")) # No Service
print(book(consultants, 14, 3, "price")) # John

# Task 3
def func(*data):
    words = {}
    for name in data:
        if len(name) == 2 or len(name) == 3:
            words[name[1]] = words.get(name[1], 0) + 1
        elif len(name) == 4 or len(name) == 5:
            words[name[2]] = words.get(name[2], 0) + 1

    min_char = min(words, key=words.get) # 找到出現次數最少的字
    count_of_ones = sum(1 for value in words.values() if value == 1) # 檢查出現次數為1的key的數量

    if count_of_ones == 1:  # 如果有兩個或更多鍵的值為1
        result_name = [name for name in data if min_char in name]
        return result_name[0]
    else:
        return "沒有"

print("=== Task 3 ===")
print(func("彭大牆", "陳王明雅", "吳明")) # 彭大牆
print(func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")) # 林花花
print(func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")) # 沒有
print(func("郭宣雅", "夏曼藍波安", "郭宣恆")) # 夏曼藍波安

# Task 4
# sequence = [0, 4, 8, 7, 11, 15, 14, 18, 22, 21, 25, ...]
def get_number(index):
    sequence = [0, 4, 8]

    for i in range(3, index + 1):
        # 每3個數分別加7
        sequence.append(sequence[i - 3] + 7)
    return sequence[index]

print("=== Task 4 ===")
print(get_number(1)) # 4
print(get_number(5))# 15
print(get_number(10)) # 25
print(get_number(30)) # 70
