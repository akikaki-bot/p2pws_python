from typing import Union

from p2pws_python.types.p2pquakes.scale import Scale
from p2pws_python.types.p2pquakes.basicdata import BasicData

from p2pws_python.utils.convertMinus import convertMinusOne, convertValue

class Hypocenter:
    depth: int
    latitude: float | None
    longitude: float | None
    magnitude: float | None
    name : str | None

    def __init__( self, jsonObject: dict ) -> None:
        self.depth = convertMinusOne(jsonObject["depth"])
        self.latitude = convertValue(jsonObject["latitude"], -200, None)
        self.longitude = convertValue(jsonObject["longitude"], -200, None)
        self.magnitude = convertMinusOne(jsonObject["magnitude"])
        self.name = convertValue(jsonObject["name"], None, "調査中")

class Issue:
    correct: str
    source: str
    time: str
    type: str

    def __init__( self, jsonObject: dict ) -> None:
        self.correct = jsonObject["correct"]
        self.source = jsonObject["source"]
        self.time = jsonObject["time"]
        self.type = jsonObject["type"]

class Point:
    addr: str
    isArea: bool
    pref: str
    scale: Scale

    def __init__( self, jsonObject: dict ) -> None:
        self.addr = jsonObject["addr"]
        self.isArea = jsonObject["isArea"]
        self.pref = jsonObject["pref"]
        self.scale = jsonObject["scale"]

class Earthquake:
    domesticTsunami: str
    foreignTsunami: str
    hypocenter: Hypocenter
    maxScale: Union[Scale, None] 
    time: str

    def __init__( self, jsonObject: dict ) -> None:
        self.domesticTsunami = jsonObject["domesticTsunami"]
        self.foreignTsunami = jsonObject["foreignTsunami"]
        self.hypocenter = Hypocenter( jsonObject["hypocenter"] )
        self.maxScale = convertMinusOne( jsonObject["maxScale"] )
        self.time = jsonObject["time"]

class EarthquakeReports ( BasicData ):
    """
    The basic data, code: 551
    """
    _id : str
    """
    情報を一意に識別するID
    """
    code : int = 551
    """
    情報コード。常に551です。
    """
    earthquake : Earthquake
    issue : Issue
    points : list[ Point ]
    time: str
    user_agent: str
    ver: str

    def __init__( self, jsonObject: dict ) -> None:
        self._id = jsonObject["_id"]
        self.earthquake = Earthquake( jsonObject["earthquake"] )
        self.issue = Issue( jsonObject["issue"] )
        self.points = [ Point( point ) for point in jsonObject["points"] ]
        self.time = jsonObject["time"]
        self.user_agent = jsonObject["user_agent"]
        self.ver = jsonObject["ver"]