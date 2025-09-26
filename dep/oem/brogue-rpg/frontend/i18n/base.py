class string:
    def __init__(self, en_US: str, zh_CN: str = ''):
        self.en_US = en_US
        self.zh_CN = zh_CN

    def __str__(self):
        if current_game().locale == "zh_CN":
            return self.zh_CN or self.en_US
        return self.en_US
    
    def __repr__(self):
        return f"string({self.en_US!r}, {self.zh_CN!r})"
    
    def __reduce__(self):
        return type(self), (self.en_US, self.zh_CN)

