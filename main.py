
from src.client import Client

from src.types.p2pquakes.earthquakeReport import EarthquakeReports
from src.types.p2pquakes.eew import EEW

from utils.convertJMAScale import convertJMAScale

client = Client( isDebug=True, isSandbox=True )

@client.on
async def ready() -> None:
    print('ready client :)')

@client.on
async def earthquake( data: EarthquakeReports ):
    print( " <-- 良い感じの地震情報 --> " )
    print(f"震源地名 {data.earthquake.hypocenter.name} (最大震度 {convertJMAScale( data.earthquake.maxScale ) })")
    print(f"マグニチュード : {data.earthquake.hypocenter.magnitude} 深さ {data.earthquake.hypocenter.depth}km ")
    print(f"緯度 {data.earthquake.hypocenter.latitude} 経度 {data.earthquake.hypocenter.longitude}" )
    print(f"発生時間 {data.earthquake.time}")
    print(f"津波の心配：{data.earthquake.domesticTsunami} ")

@client.on
async def eew( data: EEW ):
    print( " <-- 緊急地震速報 --> " )
    print(f"発生時間 {data.issue.time} / イベントID {data.issue.eventId}")
    print(f"震源地名 {data.earthquake.hypocenter.name} (マグニチュード {data.earthquake.hypocenter.magnitude} / 深さ {data.earthquake.hypocenter.depth}km)")
    print(f"緯度 {data.earthquake.hypocenter.latitude} 経度 {data.earthquake.hypocenter.longitude}")
    print(f"予想最大震度：{ convertJMAScale( data.maxScale ) }")

client.start()



if __name__ == '__main__':
    pass;