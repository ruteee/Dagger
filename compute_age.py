from termios import TIOCPKT_DATA
import pandas as pd
import numpy as np
from datetime import datetime
def main(previous_results, col):
    df = previous_results['task_0']
    df[col] = df[col].apply(pd.to_datetime)
    
    today = datetime.today()
    df['age'] = df[col].apply(func = lambda data:  int(np.floor((today - data).days/365)))

    return df

