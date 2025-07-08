# -*- coding: utf-8 -*-
# 這是註解，Python 會忽略它

# 1. 變數 (Variables)
# 變數就像一個有名字的箱子，你可以把資料放進去。
# 我們用 = 來把右邊的值(資料)放進左邊的變數裡。

message = "哈囉, Python 世界！"
number = 123
pi = 3.14159

# 2. print() 函式
# print() 可以把變數的內容或其他你想顯示的訊息印在螢幕上。

print(message)
print("這是一個數字:", number)
print("圓周率大約是:", pi)

# --- 您的練習 ---
print("\n--- 我是分隔線 ---\n") # 加個分隔線讓輸出更清楚

message = "我的名字是"
name = "sscythe"
print(message + name)

# 介紹另一種寫法: f-string
print(f"我的名字是 {name}")

# --- 3. 數字 (Numbers) 和數學運算 ---
print("\n--- 數字運算 ---\n")

x = 10
y = 3

print(f"{x} + {y} = {x + y}")   # 加法
print(f"{x} - {y} = {x - y}")   # 減法
print(f"{x} * {y} = {x * y}")   # 乘法
print(f"{x} / {y} = {x / y}")   # 除法
print(f"{x} // {y} = {x // y}") # 整數除法
print(f"{x} % {y} = {x % y}")   # 取餘數
print(f"2 的 4 次方 = {2 ** 4}") # 次方

# --- 披薩練習 ---
print("\n--- 披薩練習 ---\n")

pizza_price = 250
people = 3
price_per_person = pizza_price / people

print(f"每個人要付: {price_per_person} 元")
print(f"(格式化到小數點後兩位) 每個人要付: {price_per_person:.2f} 元")

# --- 4. 串列 (Lists) ---
print("\n--- 串列 (Lists) ---\n")

# 建立一個遊戲清單
games = ["Starcraft", "League of Legends", "Elden Ring"]
print(f"我的遊戲清單: {games}")

# 存取 (Accessing) 串列中的項目
# Python 的索引是從 0 開始的！
first_game = games[0]
print(f"我第一款喜歡的遊戲是: {first_game}")

# 更改 (Changing) 串列中的項目
games[1] = "Overwatch"
print(f"更改後的遊戲清單: {games}")

# 新增 (Appending) 項目到串列末尾
games.append("Baldur's Gate 3")
print(f"新增後的遊戲清單: {games}")

# 取得串列的長度
num_of_games = len(games)
print(f"我總共有 {num_of_games} 款喜歡的遊戲。")

# --- 待辦事項練習 ---
print("\n--- 待辦事項練習 ---\n")

tasks = ["洗衣服", "寫程式", "倒垃圾"]
print(f"原本的待辦事項: {tasks}")

# 1. 印出第二個任務
print(f"第二個任務是: {tasks[1]}")

# 2. 新增一個任務
tasks.append("買牛奶")
print(f"新增「買牛奶」後的待辦事項: {tasks}")

# --- 5. 條件判斷 (Conditional Logic) ---
print("\n--- 條件判斷 ---\n")

age = 20

# 判斷年齡
print(f"現在要判斷的年齡是: {age}")

if age < 18:
    print("您是未成年人。")
elif age >= 18 and age < 65:
    print("您是成年人。")
else:
    print("您是長者。")

# 另一個例子：檢查一個數字是否為零
number_to_check = 0
print(f"現在要檢查的數字是: {number_to_check}")

if number_to_check > 0:
    print(f"數字 {number_to_check} 是正數。")
elif number_to_check < 0:
    print(f"數字 {number_to_check} 是負數。")
else:
    print(f"數字 {number_to_check} 是零。")

# --- 分數判斷練習 ---
print("\n--- 分數判斷練習 ---\n")

score = 750
print(f"玩家分數: {score}")

if score > 1000:
    print("您是超級玩家！")
elif score >= 500 and score <= 1000:
    print("您是高級玩家。")
else:
    print("繼續努力！")

# --- 遊戲庫檢查練習 ---
print("\n--- 遊戲庫檢查練習 ---\n")

my_games = ["魔物獵人", "柏德之門3", "鬥陣特攻", "巫師3"]
print(f"我的遊戲庫: {my_games}")

if "鬥陣特攻" in my_games:
    print("您已經擁有這款遊戲了！")
else:
    print("哦？這款遊戲不在您的收藏中。")

# --- 6. 迴圈 (Loops) ---
print("\n--- 迴圈 (Loops) ---\n")

# 遍歷串列
print("遍歷遊戲清單:")
for game in my_games:
    print(f"- {game}")

# 使用 range() 執行固定次數的迴圈
print("\n從 0 到 4 數數:")
for i in range(5): # range(5) 會產生 0, 1, 2, 3, 4
    print(i)

print("\n從 1 到 5 數數:")
for j in range(1, 6): # range(1, 6) 會產生 1, 2, 3, 4, 5
    print(j)

# --- 數字總和練習 ---
print("\n--- 數字總和練習 ---\n")

numbers = [10, 20, 30, 40, 50]
print(f"要計算總和的數字串列: {numbers}")
total = 0
for number in numbers:
    total += number
print(f"數字總和是: {total}")

# --- 7. 函式 (Functions) ---
print("\n--- 函式 (Functions) ---\n")

# 簡單的函式，沒有參數也沒有回傳值
def greet():
    print("哈囉！歡迎來到函式世界。")

# 呼叫函式
greet()

# 帶有參數的函式
def greet_name(name):
    print(f"哈囉，{name}！很高興見到你。")

# 呼叫帶參數的函式
greet_name("David")
greet_name("Python學習者")

# 帶有參數和回傳值的函式
def add_numbers(a, b):
    """這個函式會將兩個數字相加並回傳結果。"""
    result = a + b
    return result

# 呼叫帶有回傳值的函式並儲存結果
sum_result = add_numbers(5, 7)
print(f"5 + 7 的結果是: {sum_result}")

# 直接在 print 中呼叫函式
print(f"10 + 20 的結果是: {add_numbers(10, 20)}")

# --- 面積計算函式練習 ---
print("\n--- 面積計算函式練習 ---\n")

def calculate_area(length, width):
    return length * width

length = 10
width = 5
area_result = calculate_area(length, width)
print(f"矩形的面積是: {area_result}")

# --- 8. 字典 (Dictionaries) ---
print("\n--- 字典 (Dictionaries) ---\n")

# 建立一個字典來儲存玩家資訊
player = {
    "name": "Hero",
    "level": 10,
    "hp": 100,
    "items": ["劍", "盾牌", "藥水"]
}
print(f"玩家資訊: {player}")

# 存取字典中的值 (使用鍵)
player_name = player["name"]
player_level = player["level"]
print(f"玩家名稱: {player_name}, 等級: {player_level}")

# 修改字典中的值
player["hp"] = 80
print(f"玩家血量更新為: {player['hp']}") # 修正了這裡的引號問題

# 新增鍵值對
player["class"] = "戰士"
print(f"新增職業後的玩家資訊: {player}")

# 遍歷字典的鍵
print("\n玩家資訊的鍵:")
for key in player:
    print(key)

# 遍歷字典的值
print("\n玩家資訊的值:")
for value in player.values():
    print(value)

# 遍歷字典的鍵和值
print("\n玩家資訊的鍵和值:")
for key, value in player.items():
    print(f"{key}: {value}")