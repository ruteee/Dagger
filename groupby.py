import pandas as pd
def main(previous_results, by, agg_func, *kwargs):
    dataset = previous_results['task_1']
    print(dataset)

    gp_df = pd.DataFrame()
    if agg_func == 'mean':
        gp_df = dataset.groupby(by=by).mean()
    elif agg_func == 'count':
        gp_df = dataset.groupby(by=by).count()
    elif agg_func == 'size':
        gp_df = dataset.groupby(by=by).size()
    elif agg_func == 'sum':
        gp_df = dataset.groupby(by=by).sum()
    else:
        gp_df =dataset.groupby(by=by).sum()
    return gp_df


        