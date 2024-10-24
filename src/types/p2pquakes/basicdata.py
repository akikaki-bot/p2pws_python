


class BasicData:
    _id : str
    code : int
    time : str

    def __init__( self, data: dict ) -> None:
        self._id = data['_id']
        self.code = data['code']
        self.time = data['time']
