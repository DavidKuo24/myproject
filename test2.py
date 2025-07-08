inventory = [
    {"name": "蘋果", "quantity": 10, "price": 5.0},
    {"name": "香蕉", "quantity": 5, "price": 3.5},
    {"name": "橘子", "quantity": 8, "price": 4.0},
]

print("---簡易庫存管理系統---")
print("初始庫存:")

# 顯示庫存
def display_inventory(current_inventory):
    for item in current_inventory:
        print(f"商品: {item['name']}，數量: {item['quantity']}，價格: {item['price']}")

# 新增或更新商品
def add_or_update_item(current_inventory, item_name, quantity_to_add, item_price):
    found_item = False

    for item in current_inventory:
        if item["name"] == item_name:
            item["quantity"] += quantity_to_add
            found_item = True
            break

    if not found_item:
        new_item = {"name": item_name, "quantity": quantity_to_add, "price": item_price}
        current_inventory.append(new_item)

# 計算總價值
def calculate_total_value(current_inventory):
    total_value = 0.0
    for item in current_inventory:
        total_value += item["quantity"] * item["price"]
    return total_value

# 測試顯示
display_inventory(inventory)
print("總價值：", calculate_total_value(inventory), "元")

# 測試新增商品
add_or_update_item(inventory, "葡萄", 12, 6.5)
print("\n新增葡萄後：")
display_inventory(inventory)
print("總價值：", calculate_total_value(inventory), "元")
