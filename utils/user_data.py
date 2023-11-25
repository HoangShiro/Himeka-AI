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
            },
            {
                'id': 2,
                'used': -1,
                'qtt': 32,
            }
        ]

    async def get(self):
        user_data = await self._load_data()
        if str(self.uid) in user_data:
            user = user_data[str(self.uid)]
            for key, value in vars(self).items():
                setattr(self, key, user.get(key, value))
        else:
            user_data[str(self.uid)] = {key: value for key, value in vars(self).items()}
            await self._save_data(user_data)

    async def set(self, variable, new_value):
        if variable in self.__dict__:
            setattr(self, variable, new_value)
            user_data = await self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = new_value
            else:
                user_data[str(self.uid)] = {variable: new_value}
            await self._save_data(user_data)

    async def update(self, variable, value):
        await self.get()
        if variable in self.__dict__:
            current_value = getattr(self, variable)
            setattr(self, variable, current_value + value)
            user_data = await self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = current_value + value
            else:
                user_data[str(self.uid)] = {variable: current_value + value}
            await self._save_data(user_data)

    async def add_item(self, id, used=None, qtt=None):
        user_data = await self._load_data()

        if used is None:
            with open('user_files/items.json', 'r') as f:
                items_data = json.load(f)
            consumable_default = next((item['Consumable'] for item in items_data if item['id'] == id), None)
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
        user_data[self.uid] = {'items': self.items}
        await self._save_data(user_data)

    

    async def _load_data(self):
        try:
            with open('user_files/user_data.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            with open('user_files/user_data.json', 'w') as file:
                json.dump({}, file, indent=4)
            return {}

    async def _save_data(self, data):
        with open('user_files/user_data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
