import os, time, datetime
from dask import dataframe as df1
from collections import defaultdict
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, send_from_directory




def process(filename, output_file):
    s_time_dask = time.time()
    dask_df = df1.read_csv(filename)
    dask_df = dask_df.rename(columns={"NumberofPlays": "Total Number of Plays for Date"})
    #time.sleep(60)
    dask_df = dask_df.groupby(['Song', 'Date'])['Total Number of Plays for Date'].sum() 
    dask_df.to_csv(f"output/{output_file}", single_file=True) 
    e_time_dask = time.time()
    print("Process Time ", (e_time_dask-s_time_dask), "seconds")
    
    return output_file

def results(requestedfile, files, under_processing):
    
    if requestedfile not in under_processing:         
            return render_template('request.html', result="check your file name and try again") 
            
    elif requestedfile not in files:
            
            return render_template('request.html', result="file is still under processing")
    else:
           return send_from_directory('output', requestedfile)   