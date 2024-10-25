
import websocket
import typing as type
import json

import p2pws_python.types.clientOptions as clientOptions
from p2pws_python.emitter import EventEmitter

from p2pws_python.types.p2pquakes.earthquakeReport import EarthquakeReports
from p2pws_python.types.p2pquakes.eew import EEW

from p2pws_python.utils.cache import DataCacheManager

class Client( EventEmitter ):
    """
    Represents the p2pquake websocket client.

    ## Examples
    - A simple example of using the Client class.

    ```
        from src.client import Client
        from src.types.p2pquakes.earthquakeReport import EarthquakeReports

        client = Client()

        @client.on
        async def ready() -> None:
            print('ready client :)')

        @client.on
        async def earthquake( data: EarthquakeReports ):
            print(f' hypocenterName: {data.earthquake.hypocenter.name} ')

        client.start()
    ```

    ## ClientOptions
    - `isDebug` : `bool`
        Whether to output debug messages.
    - `isSandbox` : `bool`
        Whether to use the sandbox server.

    ## Functions
    - `start() -> None`

        Start the websocket client.

        ⚠️ If you wanna use this function, you must call this function at the end of the script.

    ## Events
    - `ready() -> None` : Emitted when the websocket client is connected to the server.
    - `earthquake( data: EarthquakeReports ) -> None` : Emitted when the websocket client receives an earthquake report.
    - `eew( data: EEW ) -> None` : Emitted when the websocket client receives an EEW report.

    """
    option: clientOptions.ClientOptions
    ws: websocket.WebSocketApp
    isReady: bool = False
    cache : DataCacheManager

    def __init__( 
            self, 
            isDebug: type.Optional[bool] = False, 
            isSandbox: type.Optional[bool] = False 
    ) -> None:
        super().__init__()
        self.option = clientOptions.ClientOptions(
            isDebug,
            isSandbox
        )
        self.cache = DataCacheManager()


    def start( self ):
        self.ws = websocket.WebSocketApp( 
            self.__get_ws_url__(),
            on_open=self.__on_ready,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close
        )
        self.ws.run_forever()

    def __on_ready( 
            self, 
            ws: websocket.WebSocketApp 
    ) -> None:
        """
        @private
        on_open event handler. ( ready )

        This function is called when the websocket client is connected to the server.
        """
        self.isReady = True;
        self.__debug_message__(f"[client -> ws] connected to the websocket server. (url: {self.__get_ws_url__()})")
        self.emit('ready')
        pass;

    def __on_message( 
            self, 
            ws: websocket.WebSocketApp, 
            message: any 
    ) -> None:
        """
        @private
        on_message event handler.

        This function is called when the websocket client receives a message from the server.
        """
        self.emit('rawmessage', message)
        try:
            # 最初はdictにする
            data = json.loads( message )
            self.__debug_message__(f"[ws -> client] received data: {data['code']}")

            # 551 ・・・ 地震情報（震源・震度・各地の震度）
            if data['code'] == 551:
                dataClass = EarthquakeReports( data )
                self.emit('earthquake', dataClass )
                self.cache.set( dataClass._id, dataClass )

            # 556 ・・・ 緊急地震速報 配信データ
            if data['code'] == 556:
                dataClass = EEW( data )
                self.emit('eew', dataClass )
                self.cache.set( dataClass._id, dataClass )

        except Exception as e:
            self.__debug_message__(f"[client] json parsing error")
            self.__debug_message__( e )
        pass;
    
    def __on_error( 
            self, 
            ws: websocket.WebSocketApp, 
            error: any 
    ) -> None:
        self.__debug_message__(f"[client -> ws] error occurred. (url: {self.__get_ws_url__()})")
        self.__debug_message__( error )
        pass;
    
    def __on_close( 
            self, 
            ws: websocket.WebSocketApp, 
            *args 
    ) -> None:
        self.__debug_message__(f"[client -> ws] disconnected from the websocket server. (url: {self.__get_ws_url__()})")
        pass;

    
    def __debug_message__( 
            self, 
            message: str 
    ) -> None:
        if self.option.isDebug:
            print( message )

    def __get_ws_url__( self ):
        return "wss://api.p2pquake.net/v2/ws" if not self.option.isSandBox else "wss://api-realtime-sandbox.p2pquake.net/v2/ws"