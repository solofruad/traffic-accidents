#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 07:37:59 2021

@author: hat
"""

import pandas as pd


def split_dataframe(dataframe):
    init = 0
    end = 0
    dfs = []
    while end < len(dataframe):
        end += 1000
        if end > len(dataframe):
            end = len(dataframe)
        print(init, end)
        split = dataframe[init:end]
        dfs.append(split)
        init += 1000
    return dfs
    
def save_split_dataframes(dataframe, month):
    dfs = split_dataframe(dataframe)    
    for i, df in enumerate(dfs):
        _file = dir_+"split/accidents_format_"+month+"_"+str(i)+".csv"
        print("\nFile generated: ("+str(i)+")\n", _file)
        df.to_csv(_file,index=False)

def selected_month_dataset(dataframe, month, init, end):
    df = dataframe[(dataframe['created_at'] >= init) & (dataframe['created_at'] < end)]
    df = df.reset_index(drop=True)
    df.to_csv(dir_+"split/accidents_"+month+".tsv",sep='\t',index=False)
    
    df_format = df[['_id','id_tweet','address_normalization','iso2']]
    df_format.to_csv(dir_+"split/accidents_"+month+"_format.csv",index=False)
    return df, df_format


dir_ = '../../data/database/output_ml/M1/NER_extractor/'
file = 'accidents_tweets.tsv'


dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)
#dataset['address'] = dataset['address_normalization']
dataset['iso2'] = 'CO'

########33############################ OCTUBRE #########################################

month = "octubre"
init = '2018-10-01'
end = '2018-11-01'

octubre, octubre_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(octubre_format, month)

#result = pd.concat(dfs)
#result_d = result.drop_duplicates(subset=['_id'], keep='last')

#test = pd.read_csv(dir_+"split/accidents_format_octubre_0.csv")

########33############################ NOVIEMBRE #########################################

month = "noviembre"
init = '2018-11-01'
end = '2018-12-01'

noviembre, noviembre_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(noviembre_format, month)

########33############################ DICIEMBRE #########################################

month = "diciembre"
init = '2018-12-01'
end = '2019-01-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ ENERO #########################################

month = "enero"
init = '2019-01-01'
end = '2019-02-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ FEBRERO ####################################

month = "febrero"
init = '2019-02-01'
end = '2019-03-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ MARZO ####################################

month = "marzo"
init = '2019-03-01'
end = '2019-04-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)


########33############################ ABRIL ####################################

month = "abril"
init = '2019-04-01'
end = '2019-05-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ MNAYO ####################################

month = "mayo"
init = '2019-05-01'
end = '2019-06-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ JUNIO ####################################

month = "junio"
init = '2019-06-01'
end = '2019-07-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

########33############################ JUNIO ####################################

month = "julio"
init = '2019-07-01'
end = '2019-08-01'

df, df_format = selected_month_dataset(dataset, month, init, end)

save_split_dataframes(df_format, month)

