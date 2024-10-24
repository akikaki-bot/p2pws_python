
from typing import Union, Literal
from src.types.p2pquakes.scale import Scale

shindoScales : dict[ int, str ] = {
    10: "1",
    20: "2",
    30: "3",
    40: "4",
    45: "5弱",
    50: "5強",
    55: "6弱",
    60: "6強",
    70: "7"
}

def convertJMAScale( scale: Union[ Scale, int, None ] ) -> Literal[ "1", "2", "3", "4", "5弱", "5弱以上", "5強", "6弱", "6強", "7", "不明" ]:
    """
    Convert the scale of JMA to the scale of P2PQuakes.
    """
    if scale is None: return "不明"
    if scale == -1: return "不明"
    if scale == 46: return "5弱以上"

    return shindoScales[ scale ] if scale in shindoScales else "不明"

    