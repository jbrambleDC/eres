#import matplotlib
import pandas as pd
import sys
import vincent as v
from pandasql import sqldf
from vincent import AxisProperties, PropertySet, ValueRef

def get_data():
    #some annoying data munging
    csvfile = open('test_data.out.csv','rU')
    test_data = pd.read_csv(csvfile,delimiter=',')
    framework_results = pd.read_csv('test_results.csv', delimiter=',')
    test_data_name = test_data.sort('actual_name')['actual_name'].drop_duplicates().dropna()
    grouped_conf = test_data.groupby('actual_name').mean()
    grouped_conf = grouped_conf['confidence']
    framework_results['actual_name'] = framework_results['company name']
    conf = [grouped_conf[i] for i in framework_results['actual_name'].dropna()]
    framework_results = framework_results.dropna()
    framework_results['confidence'] = conf
    return framework_results


def generate_scat(df,column):
    data = df[[column,'similarity']]
    scatter = v.Scatter(data, key_on=column)
    scatter.axis_titles(x=column, y='similarity')
    return scatter

def main():
    df = get_data()
    vis = generate_scat(df,sys.argv[1])
    vis.to_json('palman_vega.json')

main()
