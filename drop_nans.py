import pandas as pd
def main(path,subset, *kwargs):
    df = pd.read_csv(path)
    df.dropna(inplace=True, subset=subset)
    return df
