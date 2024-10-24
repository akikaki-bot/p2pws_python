
# P2PWS_Client.py

Represents [P2P Earthquake API](https://www.p2pquake.net/develop/json_api_v2/) Websockets client.

## Install

```
# ↓ pip is working in progress..
pip install p2pws_python 
# or
pip install https://github.com/akikaki-bot/p2pws_python
```

## Usage

```py
from p2pws_python.client import Client
from p2pws_python.types.p2pquakes.earthquakeReport import EarthquakeReports

client = Client(
    # if you wanna enabled debug mode, add the arguments on client option, like this:
    # isDebug = True
    # Other, if you wanna connect to sandbox server, add the arguments on client option, like this:
    # isSandbox = True
)

@client.on
async def earthquake( data : EarthquakeReports ):
    print( data.earthquake.hypocenter.name )

client.start()
```