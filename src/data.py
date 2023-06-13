from urllib import request
import json
from datetime import datetime
from pathlib import Path
from plotting.utils import Config, BaseDir

class Data:

    Dir: Path = BaseDir.joinpath('data')
    Config = Config(BaseDir.joinpath('config', 'main.ini'), section='visual crossing')

    Location = Config.get_value('Location')
    Url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

    @staticmethod
    def load_from_url() -> dict:
        response = request.urlopen(f'{Data.Url}/{Data.Location}')
        data = response.read()
        data = json.loads(data.decode('utf-8'))
        if 'errorCode' in data:
            print(f'Error reading from errorCode {Data.Url}, error={data["errorCode"]}')
        return data

    @staticmethod
    def load(month: int = None, year: int = None) -> dict:
        now = datetime.now()
        now = now.replace(month=now.month if month is None else month, year=now.year if year is None else year)
        with open(Data.Dir.joinpath(now.strftime('%Y-%b.json').lower())) as f:
            return json.load(f)
