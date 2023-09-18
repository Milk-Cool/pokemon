__all__ = ["Pokemon"]


class Pokemon:
    def __init__(self, name, atk, df):
        self.name = name
        self.atk = atk
        self.df = df
        self.hp = 100

    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_def(self):
        return self.df

    def attack(self, target, self_copy=None, target_copy=None):
        if (self_copy == None):
            self_copy = self
        if (target_copy == None):
            target_copy = target
        if (self.hp == 0):
            return
        target.hp = max(
            0, target.hp - max(self_copy.get_atk() - target_copy.get_def(), 0))
