import json, re

class UItem:
    def __init__(self):
        self.items = []
        self.load_items()

    def load_items(self):
        try:
            with open('user_files/items.json', 'r', encoding="utf-8") as file:
                self.items = json.load(file)
        except FileNotFoundError:
            # Không tìm thấy file, tạo một danh sách trống
            self.items = []
        except Exception as e:
            print("Error while load items: ", str(e))
            with open('user_files/items.json', 'w', encoding="utf-8") as file:
                json.dump(self.items, file, indent=2)

    def save_items(self):
        with open('user_files/items.json', 'w', encoding="utf-8") as file:
            json.dump(self.items, file, indent=2)

        self.load_items()
        
    async def get(self, identifier):
        self.load_items()
        for item in self.items:
            if str(item['ID']) == str(identifier) or re.search(str(identifier), item['Name'].lower(), re.IGNORECASE):
                return item
        return None

    async def set(self, name, type_, spd, skl, tech, lore, stack, consu, sellable, lv, cp):
        taken_ids = [item['ID'] for item in self.items]
        new_id = 1
        while new_id in taken_ids:
            new_id += 1
        new_item = {
            'ID': new_id,
            'Name': name,
            'Type': type_,
            'Spd': spd,
            'Skl': skl,
            'Tech': tech,
            'Lore': lore,
            'Stackable': stack,
            'Consumable': consu,
            'Sellable': sellable,
            'Level': lv,
            'CP': cp
        }
        self.items.append(new_item)
        self.save_items()

    async def update(self, item_id, **kwargs):
        for item in self.items:
            if item['ID'] == item_id:
                for key, value in kwargs.items():
                    if key in item:
                        item[key] = value
                self.save_items()
                return True
        return False
    
    async def delete(self, item_id):
        for item in self.items:
            if item['ID'] == item_id:
                self.items.remove(item)
                self.save_items()
                return True
        return False

class ULore:
    def __init__(self):
        self.levels = {
            1: "Khách du lịch thăm quan IW.",
            2: "Công dân IW.",
            3: "Kỹ sư IW.",
            4: "Sở hữu công ty tại IW.",
            5: "Lãnh đạo cấp cao tại IW.",
            6: "Thành viên hội đồng quản trị ISTAR."
        }

    async def get(self, vname):
        return self.levels.get(vname, None)

class UFrom:
    def __init__(self):
        self.fr_earth = "Earth 🌏"
        self.fr_catalia = "Catalia 😺"
        self.fr_astria = "Astria 🪐"
        self.fr_orion = "Orion 🌑"
        #self.fr_iw = "IW 🛰️"

    async def get(self, vname):
        return getattr(self, vname, None)

class UHome:
    def __init__(self):
        self.ho_iw = "IW 🛰️"
        self.ho_libra = "Libra ♎"

    async def get(self, vname):
        return getattr(self, vname, None)

class UserData:
    def __init__(self, uid):
        self.uid = uid
        self.u_name = "IW Citizen"
        self.u_achv = "Newcomer"
        self.u_lv = 1
        self.u_from = None
        self.u_home = None
        self.u_joindate = 0
        self.u_fame = 0
        self.u_techs = "🔹"
        self.u_blc = 1000
        self.u_tech_st = 1
        self.u_speed_st = 1
        self.u_skl_st = 1

        self.items = [
            {
                'id': 8,
                'used': 2,
                'qtt': 5,
            }
        ]

    async def get(self):
        user_data = await self._load_data()
        if str(self.uid) in user_data:
            user = user_data[str(self.uid)]
            for key, value in vars(self).items():
                setattr(self, key, user.get(key, value))
        else:
            await self._save_data()

    async def set(self, variable, new_value):
        await self.get()
        if variable in self.__dict__:
            setattr(self, variable, new_value)
            await self._save_data()

    async def update(self, variable, value):
        await self.get()
        if variable in self.__dict__:
            current_value = getattr(self, variable)
            setattr(self, variable, current_value + value)
            await self._save_data()

    async def add_item(self, id, qtt=None, used=None):
        ie = UItem()
        ex = await ie.get(id)
        if not ex:
            print(f"Lỗi khi add item: ID {id} không tồn tại.")
            return f"Lỗi khi add item: ID {id} không tồn tại."

        await self.get()
        existing_item_index = next((index for index, item in enumerate(self.items) if item['id'] == id), None)
        if existing_item_index is not None:
            if qtt is None:
                return f"Item ID {id} đã tồn tại, hãy thêm số lượng hoặc dùng lệnh 'Cập nhật' thay thế."
            else:
                self.items[existing_item_index]['qtt'] += qtt
        else:
            if used is None:
                with open('user_files/items.json', 'r') as f:
                    items_data = json.load(f)
                consumable_default = next((item['Consumable'] for item in items_data if item['ID'] == id), None)
                if consumable_default is not None:
                    if consumable_default == 0:
                        used = -1
                    else:
                        used = consumable_default
            qtt = qtt if qtt is not None else 1
            self.items.append({
                'id': id,
                'used': used,
                'qtt': qtt,
            })
        await self._save_data()

    async def update_item(self, item_index, value, sell=False):
        await self.get()
        if item_index < 0 or item_index >= len(self.items):
            print("Sai vị trí item cần update.")
            return "Sai vị trí item cần update."

        item = self.items[item_index]

        if value > 0:
            item['qtt'] += value
        elif value < 0:
            if item['used'] > 0 and not sell:
                item['used'] -= min(item['used'], abs(value))
                if item['used'] == 0:
                    ie = UItem()
                    ie = await ie.get(item['id'])
                    item['used'] = ie['Consumable']
                    item['qtt'] -= 1
                    if item['qtt'] == 0:
                        await self.remove_item(item_index)

            elif item['used'] == -1 or item['used'] > 0 and sell:
                item['qtt'] -= min(item['qtt'], abs(value))
                if item['qtt'] == 0:
                    await self.remove_item(item_index)

        await self._save_data()
    
    async def get_item(self, item_index=None):
        await self.get()

        if item_index is not None:
            if 0 <= item_index < len(self.items):
                return self.items[item_index]
            else:
                print("User không có item này.")
                return None
        else:
            return self.items

    async def remove_item(self, item_index):
        self.items.pop(item_index)
        await self._save_data()
        return
    
    async def _load_data(self):
        try:
            with open('user_files/user_data.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            with open('user_files/user_data.json', 'w') as file:
                json.dump({}, file, indent=4)
            return {}

    async def _save_data(self):
        user_data = await self._load_data()
        user_data[str(self.uid)] = vars(self)
        with open('user_files/user_data.json', 'w', encoding="utf-8") as file:
            json.dump(user_data, file, indent=4)
