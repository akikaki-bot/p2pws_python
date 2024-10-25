

class ClientOptions:
    isSandBox : bool
    isDebug : bool

    def __init__(self, isSandBox: bool, isDebug: bool):
        self.isSandBox = isSandBox
        self.isDebug = isDebug