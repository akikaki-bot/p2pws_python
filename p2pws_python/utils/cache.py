from typing import Union
from aiohttp import ClientSession

from p2pws_python.types.p2pquakes.earthquakeReport import EarthquakeReports
from p2pws_python.types.p2pquakes.eew import EEW
from p2pws_python.types.base.map import Map





class DataCacheManager( 
    Map[ 
        Union[ 
            EarthquakeReports, 
            EEW 
        ]
    ] 
):

    httpSession: ClientSession

    def __init__( self ) -> None:
        super().__init__()
        self.httpSession = ClientSession(
            base_url='https://api.p2pquake.net/v2',
            headers={
                'User-Agent': 'Python, aiohttp and p2pquake websocket client'
            },
            timeout=10,
            raise_for_status=False
        )

    def getRecentEarthquakeData( self ) -> EarthquakeReports:
        for item in self.items:
            if isinstance( item, EarthquakeReports ):
                return item
        return None
    
    def getRecentEEWData( self ) -> EEW:
        for item in self.items:
            if isinstance( item, EEW ):
                return item
        return None
    
    async def fetchEarthquakeData( self, id : str ) -> Union[EarthquakeReports, None]:
        if id in self:
            return self[ id ]
        
        
        response = await self.httpSession.get(f'/jma/quake/{id}')
        data = await response.json()

        if data['code'] != "551":
            return None
        
        else:
            earthquakeData = EarthquakeReports( data )
            self.set( id, earthquakeData )
            return earthquakeData


    

