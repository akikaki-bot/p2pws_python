from typing import Union, TypeVar

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def convertMinusOne( value: int ) -> Union[ int, None ]:
    """
    もしも与えられた`value`が`-1`であった場合に、Noneを返します。

    それ以外は`value`をそのまま返します。
    """
    return value if value != -1 else None

def convertValue( 
        value: T, 
        condition: Union[ T, U ],
        convert: V 
) -> Union[ T, V ]:
    """
    型`T`の`value`が型`T | U`である`condition`と等しい場合に、型`V`の`convert`を返却します。

    それ以外の場合は`value`をそのまま返却します。
    """
    if condition is None:
        if value is None: 
            return convert
        
    if value == condition: return convert
    return value