from urllib import request
import json
from datetime import datetime, timedelta
from pathlib import Path
from plotting.utils import Config, BaseDir
import h5py
import numpy as np

def load_file(fname):
    return h5py.File(fname, 'r') if fname.exists() else None

class Data:

    Dir: Path = BaseDir.joinpath('data')
    Config = Config(BaseDir.joinpath('config', 'main.ini'), section='visual crossing')

    Location = Config.get_value('Location')
    Url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'


    FileName = Dir.joinpath('main.h5')
    D = load_file(FileName)

    @staticmethod
    def time():
        return np.array(Data.D['datetimeEpoch'])

    @staticmethod
    def query_from_url(month: int, save_json=True) -> None:  # TODO: set to False if it works
        t = datetime.now().replace(month=month, day=1)
        first_day, last_day = [dt.strftime('%Y-%m-%d') for dt in [t, t.replace(month=month + 1) - timedelta(days=1)]]
        url = f'{Data.Url}/{Data.Location}/{first_day}/{last_day}?unitGroup=metric&key={Data.Config.get_value("key")}&contentType=json'
        data = request.urlopen(url).read()
        data = json.loads(data.decode('utf-8'))
        if 'errorCode' in data:
            print(f'Error reading from errorCode {Data.Url}, error={data["errorCode"]}')
        if save_json:
            with open(Data.Dir.joinpath(t.strftime('%Y-%b.json').lower()), 'w') as f:
                json.dump(data, f)
        Data.save2h5(data)

    @staticmethod
    def load_json(month: int = None, year: int = None) -> dict:
        now = datetime.now()
        now = now.replace(month=now.month if month is None else month, year=now.year if year is None else year)
        with open(Data.Dir.joinpath(now.strftime('%Y-%b.json').lower())) as f:
            return json.load(f)

    @staticmethod
    def save2h5(d):
        if Data.D is not None:
            Data.D.close()
        with h5py.File(Data.FileName, 'a') as f:
            info = {'datetimeEpoch': 'u4', 'temp': 'f2', 'humidity': 'f2', 'precip': 'f2', 'windspeed': 'f2', 'winddir': 'f2', 'pressure': 'f4', 'solarradiation': 'f2', 'uvindex': 'u1'}
            data = {key: [] for key in info.keys()}
            for day in d['days']:
                for hour in day['hours']:
                    for key in info.keys():
                        data[key].append(hour[key])
            if 'datetimeEpoch' in f:
                t_data = np.concatenate([f['datetimeEpoch'], data['datetimeEpoch']])
                unique = np.unique(t_data, return_index=True)[1]  # check if the data already exists
                i_sorted = t_data[unique].argsort() if 'datetimeEpoch' in f else []  # sort timestamps
            for key, dtype in info.items():
                x = np.array(data[key], dtype=dtype) if key != 'uvindex' else np.array(data[key], dtype=float).astype(dtype)
                if key in f:
                    x = np.concatenate([f[key], x])[unique][i_sorted]
                    del f[key]
                f.create_dataset(key, data=x)
        Data.D = load_file(Data.FileName)



