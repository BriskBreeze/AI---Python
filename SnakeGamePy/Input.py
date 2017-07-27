class Input:

    def __init__(self):
        self.keys = {}
        
    # @staticmethod
    def ChangeState(self, Key, state):
        self.keys[Key] = state
    
    # @staticmethod
    def Pressed(self, Key):
        if self.keys.get(Key) == None:
            return False
        return bool(self.keys[Key]) 