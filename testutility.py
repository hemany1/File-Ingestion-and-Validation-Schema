import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re
import dask.dataframe as dd
import dask.array as da
import dask.bag as db


################
# File Reading #
################

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)


def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string) 
    return string




def col_header_val(df,table_config):
    '''
    replace whitespaces in the column
    and standardized column names
    '''
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('[^\w]','_',regex=True)
    df.columns = list(map(lambda x: x.strip('_'), list(df.columns)))
    df.columns = list(map(lambda x: replacer(x,'_'), list(df.columns)))
    expected_col = list(map(lambda x: x.lower(),  table_config['columns']))
    expected_col.sort()
    df.columns =list(map(lambda x: x.lower(), list(df.columns)))
    df = df.reindex(sorted(df.columns), axis=1)
    if len(df.columns) == len(expected_col) and list(expected_col)  == list(df.columns):
        print("column name and column length validation passed")
        return 1
    else:
        print("column name and column length validation failed")
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print("Following File columns are not in the YAML file",mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded",missing_YAML_file)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0

    
    
def pipe(df,name):
    '''
    create a pipe seperated text file 
    with the name passed in.
    '''
    # Write the DataFrame to a pipe-separated text file in gzip format
    df.to_csv('{}.txt.gz'.format(name), sep='|', index=False, compression='gzip')
    return None


def summary(df):
    print("Number of rows:",df.shape[0])
    print("Number of columns:",df.shape[1])
    print("DataFrame info",	df.info(memory_usage="deep"))
    return df.info(memory_usage="deep"))
