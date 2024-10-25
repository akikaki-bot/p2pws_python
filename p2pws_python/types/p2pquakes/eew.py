
from types.p2pquakes.basicdata import BasicData
from utils.convertMinus import convertMinusOne, convertValue
from typing import NewType, Union, Optional
from enum import Enum

class EEWHypocenter:
    name: str
    """
        震源地名
    """
    reduceName: str
    """
        短縮用震央地名
    """
    latitude: Optional[ float ]
    """
        緯度
    """
    longitude: Optional[ float ]
    """
        経度
    """
    depth: Optional[ float ]
    """
        深さ
    """
    magnitude: Optional[ float ]
    """
        マグニチュード
    """

    def __init__( self, jsonObject: dict ) -> None:
        self.name = jsonObject["name"]
        self.reduceName = jsonObject["reduceName"]
        self.latitude = convertValue(jsonObject["latitude"], -200, None)
        self.longitude = convertValue(jsonObject["longitude"], -200, None)
        self.depth = convertMinusOne( convertValue(jsonObject["depth"], 0, -1 ) )
        self.magnitude = convertMinusOne( jsonObject["magnitude"] )

class EEWIssue:
    time: str
    eventId: str
    serial: str

    def __init__( self, jsonObject: dict ) -> None:
        self.time = jsonObject["time"]
        self.eventId = jsonObject["eventId"]
        self.serial = jsonObject["serial"]

class EEWDetail:
    originTime: str
    arrivalTime: str
    condition: str
    hypocenter: EEWHypocenter 
    
    def __init__( self, jsonObject: dict ) -> None:
        self.originTime = jsonObject["originTime"]
        self.arrivalTime = jsonObject["arrivalTime"]
        self.condition = jsonObject["condition"]
        self.hypocenter = EEWHypocenter( jsonObject["hypocenter"] )


class KindCode( Enum ):
    SecondaryUnReached = "10"
    """
    主要動未到達
    """
    SecondaryReached = "11"
    """
    主要動到達済
    """
    SecondaryReachedNoForecastinPLUM = "19"
    """
    主要動の到達予想なし（PLUM法による予想）
    """

class EEWArea:
    pref: str
    """
    府県予報区
    """
    name: str
    """
    地域名
    """
    scaleFrom: float
    """
        システムの都合で小数点が着くが、整数部のみ有効
    """
    scaleTo: Union[ float, 0, 99, None ]
    """
        システムの都合で小数点が着くが、整数部のみ有効
    """
    kindCode: KindCode
    """
    警報コード
    """
    arrivalTime: str
    """
        主要動到達予想時刻
    """

    def __init__( self, jsonObject: dict ) -> None:
        self.pref = jsonObject["pref"]
        self.name = jsonObject["name"]
        self.scaleFrom = jsonObject["scaleFrom"]
        self.scaleTo = convertMinusOne( jsonObject["scaleTo"] )
        self.kindCode = KindCode( jsonObject["kindCode"] )
        self.arrivalTime = jsonObject["arrivalTime"]

class EEW ( BasicData ):
    """
    緊急地震速報（警報）の内容です。ただし、以下の点に留意してください。

    内容や配信品質は無保証です。緊急地震速報（警報）としての利用・活用は非推奨です。
    - 多くの項目は[気象庁防災情報XMLフォーマット ｜ 技術資料の定義](https://xml.kishou.go.jp/tec_material.html)そのままです。
    - 地震の規模や予測震度なども提供しますが、緊急地震速報（警報）では発表されない内容です（参考：[気象庁｜緊急地震速報｜緊急地震速報（警報）及び（予報）について](https://www.data.jma.go.jp/svd/eew/data/nc/shikumi/shousai.html)）。
    - スキーマは今後拡張する可能性があります。

    遅延や欠落のリスクは以下の通りです。
    - 処理遅延: WebSocket API は約 70ms 、 JSON API は約 1000 ms （高負荷時はさらに遅延します）
    - サーバ所在地: 東京 (Linode Tokyo 2)
    - 欠落リスク: サーバや受信プログラムは冗長化しておらず、障害時は配信できず、復旧時の再配信もありません。

    また、このEEWクラスは一部拡張されています。詳細は以下の通りです。
    - 既存にはない`maxScale`プロパティを追加しています。
    """
    code: 556
    """
    コードはいつでも556です。
    """
    test: bool
    """
    テストであるか。
    """
    cancelled: bool
    """
    キャンセル報か。
    """
    earthquake: None | EEWDetail
    """
    EEWの詳細情報。

    取り消しの場合は`None`です。
    """
    issue: EEWIssue
    """
    このEEWについての情報
    """
    areas: list[EEWArea]
    """
    各地の予想される最大震度
    """
    maxScale: int | None
    """
    予想最大震度。各地の予想震度から最大のものを取得します。
    """

    def __init__( self, data: dict ) -> None:
        super().__init__( data )
        self.test = data["test"]
        self.cancelled = data["cancelled"]
        self.earthquake = EEWDetail( data["earthquake"] ) if data["earthquake"] else None
        self.issue = EEWIssue( data["issue"] )
        self.areas = [ EEWArea( area ) for area in data["areas"] ]
        self.maxScale = getMaxScale( self.areas )

def getMaxScale( data: list[ EEWArea ] ) -> int:
    """
    予想最大震度を取得します。
    """
    return max( [ area.scaleTo for area in data ] ) if data else None