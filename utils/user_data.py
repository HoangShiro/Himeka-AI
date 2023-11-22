import json


class ULore:
    def __init__(self):
        self.lv1 = "Khách du lịch thăm quan IW."
        self.lv2 = "Công dân IW."
        self.lv3 = "Kỹ sư IW."
        self.lv4 = "Sở hữu công ty tại IW."
        self.lv5 = "Lãnh đạo cấp cao tại IW."
        self.lvs = "Thành viên hội đồng quản trị ISTAR."

    async def get(self, vname):
        if vname == 1:
            return getattr(self, 'lv1', None)
        elif vname == 2:
            return getattr(self, 'lv2', None)
        elif vname == 3:
            return getattr(self, 'lv3', None)
        elif vname == 4:
            return getattr(self, 'lv4', None)
        elif vname == 5:
            return getattr(self, 'lv5', None)
        else:
            return getattr(self, 'lvs', None)

class UFrom:
    def __init__(self):
        self.fr_earth = "Earth 🌏"
        self.fr_catalia = "Catalia 😺"
        self.fr_astria = "Astria 🪐"
        self.fr_iw = "IW 🛰️"
        self.fr_orion = "Orion 🌑"

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
        #self.u_avatar = "https://cdn.discordapp.com/attachments/1096933532032581693/1176470799008399450/iw_logo.png"
        self.u_achv = "Newcomer"
        self.u_lv = 1
        self.u_from = None
        self.u_home = None
        self.u_joindate = 0
        self.u_fame = 0
        self.u_techs = "🔹"
        self.u_blc = 1000 # Ira

    async def get(self):
        user_data = await self._load_data()
        if str(self.uid) in user_data:
            user = user_data[str(self.uid)]
            for key, value in vars(self).items():
                setattr(self, key, user.get(key, value))
        else:
            # Nếu uid không có trong dữ liệu, lưu giá trị mặc định vào file
            user_data[str(self.uid)] = {key: value for key, value in vars(self).items()}
            await self._save_data(user_data)

    async def set(self, variable, new_value):
        if variable in self.__dict__:
            setattr(self, variable, new_value)
            user_data = await self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = new_value
            else:
                # Nếu uid không tồn tại, tạo một bản ghi mới
                user_data[str(self.uid)] = {variable: new_value}
            await self._save_data(user_data)

    async def update(self, variable, value):
        await self.get()  # Load existing data
        if variable in self.__dict__:
            current_value = getattr(self, variable)
            setattr(self, variable, current_value + value)
            user_data = await self._load_data()
            if str(self.uid) in user_data:
                user_data[str(self.uid)][variable] = current_value + value
            else:
                # Nếu uid không tồn tại, tạo một bản ghi mới
                user_data[str(self.uid)] = {variable: current_value + value}
            await self._save_data(user_data)

    async def _load_data(self):
        try:
            with open('user_files/user_data.json', 'r', encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            # Create a new file if not found
            with open('user_files/user_data.json', 'w') as file:
                json.dump({}, file, indent=4)
            return {}

    async def _save_data(self, data):
        with open('user_files/user_data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
