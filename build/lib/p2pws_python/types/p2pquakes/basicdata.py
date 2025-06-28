


class BasicData:
    """
    基本になるデータを格納するデータクラス
    """
    _id : str
    """
    情報を一意に識別するID
    """
    code : int
    time : str
    """
    受信日時。形式は 2006/01/02 15:04:05.999 です。
    """

    def __init__( self, data: dict ) -> None:
        self._id = data['_id']
        self.code = data['code']
        self.time = data['time']
