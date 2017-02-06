import pandas as pd
import numpy as np

def add_quantiles(df, metrics, weight='marsupwt'):
    if isinstance(metrics, str):
        metrics = [metrics]
    for metric in metrics:
        df = df.sort_values(metric)
        samp_prob = df[weight]/df[weight].sum()
        df['{}_quantile'.format(metric)] = np.cumsum(samp_prob) / samp_prob.sum()
    return df