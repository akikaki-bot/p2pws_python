
from typing import TypeVar, Generic, Union

T = TypeVar('T')

class Map( Generic[ T ] ):

    data : dict[ str, T ]

    def __init__( self ):
        self.data = {}

    def get( self, key: str ) -> Union[ Generic[ T ], None ] :
        """
        Get the property by `key`.
        """
        if key in self.data:
            return self.data[key]
        
        else:
            return None
        
    def set_safe( self, key: str, value: T ) -> bool:
        """
        Set the property if the `key` is not exists.
        """
        if key not in self.data:
            self.data[key] = value
            return True
        
        else:
            return False
    
    def set( self, key: str, value: T ) -> None:
        """
        Set the property with `key`.

        If the `key` is exists, the `value` will be overwritten.
        """
        self.data[key] = value

    def remove( self, key: str ) -> bool:
        """
        Remove the property by key.

        If remove success, return `True`.
        """
        if key in self.data:
            del self.data[key]
            return True
        
        return False
    
    def clear( self ) -> None:
        """
        Clear all properties.
        """
        self.data.clear()
        pass;

    def keys( self ) -> list[ str ]:
        """
        Get all keys.
        """
        return list( self.data.keys() )
    
    def values( self ) -> list[ T ]:
        """
        Get all values.
        """
        return list( self.data.values() )
    
    def items( self ) -> list[ tuple[ str, T ] ]:
        """
        Get all items.
        """
        return list( self.data.items() )
    
    def has( self, key: str ) -> bool:
        """
        Check if the property exists.
        """
        return key in self.data
    
    def __len__( self ) -> int:
        return len( self.data )
    
    def __str__( self ) -> str:
        return str( self.data )
    
    def __repr__( self ) -> str:
        return repr( self.data )
    
    def __iter__( self ):
        return iter( self.data )
    


    