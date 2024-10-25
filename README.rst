The Websocket client for p2p web api.

## Installation

```bash
pip install p2pws_python
```

## Usage

```python
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

# License
MIT License
