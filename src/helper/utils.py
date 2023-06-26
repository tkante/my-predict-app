import pandas as pd
import geopandas as gpd
import numpy as np
import datetime
from datetime import date
import pickle
from typing import List 
import json
import random 


def characterReplacement(ch:str)->str:
    ch = str(ch)
    if ch:
        res = ch.replace("é", "e")
        res = ch.replace("é", "e")
        res = ch.replace("ë", "e")
        res = res.replace("ê", "e")
        res = res.replace("ô", "o")
        res = res.replace("à", "a")
        res = res.replace("â", "a")
        res = res.replace("è", "e")
        res = res.replace("î", "i")
        res = res.replace("û", "u")
        res = res.replace("é","e")
        return res
    return ch

def load_classifier(path:str, city:str, targets:List[str]):
    models = dict()
    print('Load Model Using Pickle !')
    for target in targets:
        filename= path.joinpath(f"{city}/{characterReplacement(target)}.sav")
        model= pickle.load(open(filename, 'rb'))
        models[target] = model
    return models


def one_hot_encoder(df:pd.DataFrame, features:List[str]) -> pd.DataFrame:
  one_hot_df= pd.get_dummies(df[features], prefix="", prefix_sep="")
  df= pd.concat([df, one_hot_df], axis=1)
  return df

def loadJSON(path:str, sub_dir:str, filename:str) -> dict:
        filename=  path.joinpath(f'{sub_dir}/{filename}')
        with open(filename, encoding="utf-8") as fh:
            data = json.load(fh)
        return data


def set_target_variables(db:pd.DataFrame, sub_category_col, targets:dict):
  for target in targets:
    db[target] = 0
    db.loc[db[sub_category_col].isin(targets[target]), target] = 1
    print(target)
    print(db[target].value_counts())
  return db

def select_clusters(df, cluster_col, month_col, dayofweek_col, window_col, month, dayofweek, window, proba):
    df_filter = df[(df[month_col] == month) & (df[dayofweek_col] == dayofweek)]
    if isinstance(window, str):
        window = [window]
    df_filter = df_filter[df_filter[window_col].isin(window)]
    if df_filter.shape[0] > 0:
        clusters = dict(df_filter[cluster_col].value_counts(normalize = True))
        occurences = dict(df_filter[cluster_col].value_counts())
        clusters = {k:v+proba for k,v in clusters.items()}
        sum_values = sum(clusters.values())
        clusters = {k:v/sum_values for k, v in clusters.items()}
    else:
       clusters   = {}
       occurences = {}
    return clusters, occurences

def A1fit(db,  target:str):
  df = db.copy()
  df[target] = np.where(df[target] > 0, 1, 0)
  return df

def series_to_supervised(db, target:str, n_in=1, dropnan=True):
  # input sequence (t-n, ... t-1)
  for i in range(n_in, 0, -1):
     db[f"{target}(t-{i})"] = db[[target]].shift(i)
  # drop rows with NaN values
  if dropnan:
    db.dropna(inplace=True)
  return db

def predict_proba(X, model) -> None:
    try:
        predProb= model.predict_proba(X)[:, 1]
        predProb= predProb[-1] 
    except:
        predProb= 0.09999
    return round(predProb, 5)

def feeaturesX(data, date_col, month_col, dayofweek_col, window_col, monthname, dayofweek, window, holiday_name, target, features, variables, n_in=6):
  df_filter = data.copy()
  df_filter[date_col] = pd.to_datetime(df_filter[date_col].dt.date)
  df_filter = df_filter[
        (df_filter[month_col] == monthname) & (df_filter[dayofweek_col].isin(dayofweek)) & (df_filter[window_col].isin(window))
      ]
  df_filter = df_filter[df_filter[date_col] >= df_filter[date_col].max() - datetime.timedelta(days=6)]
  df_filter = df_filter.groupby([date_col, holiday_name, month_col, dayofweek_col])[target].sum().reset_index()
  df_filter.index = df_filter[date_col]
  ix= pd.date_range(df_filter[date_col].max() - datetime.timedelta(days=6), df_filter[date_col].max(), freq='D')
  df_filter = df_filter.reindex(ix, fill_value=0)
  df_filter = A1fit(df_filter, target)
  df_filter = one_hot_encoder(df_filter, features)
  df_filter = series_to_supervised(df_filter, target, n_in)
  cols = df_filter.columns
  for variable in variables:
    if variable not in cols:
      df_filter[variable] = 0
  return df_filter[variables]

