from urllib import request
import json
from datetime import datetime
from pathlib import Path
from plotting.utils import Config, BaseDir
import h5py
import numpy as np

class Data:

    Dir: Path = BaseDir.joinpath('data')
    Config = Config(BaseDir.joinpath('config', 'main.ini'), section='visual crossing')

    Location = Config.get_value('Location')
    Url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'

    FileName = Dir.joinpath('main.h5')
    D = h5py.File(FileName, 'r')

    @staticmethod
    def load_from_url() -> dict:
        response = request.urlopen(f'{Data.Url}/{Data.Location}')
        data = response.read()
        data = json.loads(data.decode('utf-8'))
        if 'errorCode' in data:
            print(f'Error reading from errorCode {Data.Url}, error={data["errorCode"]}')
        return data

    @staticmethod
    def load_json(month: int = None, year: int = None) -> dict:
        now = datetime.now()
        now = now.replace(month=now.month if month is None else month, year=now.year if year is None else year)
        with open(Data.Dir.joinpath(now.strftime('%Y-%b.json').lower())) as f:
            return json.load(f)

    @staticmethod
    def convert(d):
        with h5py.File(Data.FileName, 'a') as f:
            info = {'datetimeEpoch': 'u4', 'temp': 'f2', 'humidity': 'f2', 'precip': 'f2', 'windspeed': 'f2', 'winddir': 'f2', 'pressure': 'f4', 'solarradiation': 'f2', 'uvindex': 'u1'}
            data = {key: [] for key in info.keys()}
            for day in d['days']:
                for hour in day['hours']:
                    for key in info.keys():
                        data[key].append(hour[key])
            for key, dtype in info.items():
                x = np.array(data[key], dtype=dtype) if key != 'uvindex' else np.array(data[key], dtype=float).astype(dtype)
                f.create_dataset(key, data=x, maxshape=(None,))



