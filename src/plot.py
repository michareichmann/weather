from plotting.draw import *
from src.data import Data
import numpy as np

draw = Draw()

KW = {'x_tit': 'Time [dd:hh]', 'xls': .03, 't_ax_off': 0, 'tform': '#splitline{%H}{%m-%d}'}


def temp(t0=None, t1=None, **dkw):
    x, y = Data.D['datetimeEpoch'], Data.D['temp']
    return draw.graph(x, y, 'Temp', **prep_kw(dkw, y_tit='Temperature [°C]', color=2, markersize=.5, draw_opt='apl', **KW))

def precip(daily=True, **dkw):
    x, y = Data.D['datetimeEpoch'], np.array(Data.D['precip']) * 25.4
    x, y = (x[::24], np.mean(y.reshape((-1, 24)), axis=1)) if daily else (x, y)
    kw = prep_kw({'tform': '%m-%d'}, **KW) if daily else KW
    gStyle.SetBarWidth(.7)
    return draw.graph(x, y, **prep_kw(dkw, y_tit='Precipation [l/m^2]', fill_color=4, **kw, draw_opt='ab'))