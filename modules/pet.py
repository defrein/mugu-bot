class Pet:
    def __init__(self, level=1):
        self.level = level
        
    def get_ascii(self):
        # Different ASCII art for different levels
        if self.level == 1:
            return "(｡･ω･｡)"
        elif self.level == 2:
            return "ʕ•ᴥ•ʔ"
        elif self.level == 3:
            return "ʕ•̀ω•́ʔ✧"
        elif self.level >= 4:
            return "ʕ ꈍᴥꈍʔ♡"
        
    def get_name(self):
        names = {
            1: "Baby Pet",
            2: "Growing Pet",
            3: "Teenage Pet",
            4: "Adult Pet",
            5: "Master Pet"
        }
        if self.level in names:
            return names[self.level]
        return "Ultimate Pet"