from urllib import request
import json
from datetime import datetime
from pathlib import Path

class Data:

    Dir: Path = ...
    Config = ...

    Location = 'Wroclaw'
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
        with open(Data.Dir.joinpath(now.strftime('%Y-%b'.lower()))) as f:
            return json.load(f)
