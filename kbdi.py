#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 18:52:08 2018

@author: root
"""

import pandas as pd
import matplotlib.pyplot as plt
file = "/home/andre/py-scripts/kbdi/canberra_airport.txt"
raw = pd.read_csv(file)
ref = raw.loc[:,"Year Month Day Hour Minutes in YYYY":"Air Temperature in degrees C"]
ref = ref.loc[ref["MI format in Local standard time"]!=0]
ref = ref.drop(columns=['Quality of precipitation since 9am local time','MI format in Local time','Year Month Day Hour Minutes in YYYY.1','MM.1', 'DD.1', 'HH24.1', 'MI format in Local standard time'])
ref.columns=["year","month","day","hour","rainfall","temperature"]
ref.index = pd.to_datetime(ref.loc[:,"year":"hour"])
ref = ref.drop(columns=["year","month","day","hour"])
ref['temperature'] = ref['temperature'].str.replace('     ', '')
ref["temperature"] = pd.to_numeric(ref["temperature"])
ref['rainfall'] = ref['rainfall'].str.replace("      ", '')
ref["rainfall"] = pd.to_numeric(ref["rainfall"])

kbdi = ref.loc[ref.index>"19960101"]
#m = kbdi.groupby(kbdi.index.year).sum().rainfall.mean()/25.4
k=800
fin = []
rr=[]
tt=[]
r_cons = False
kbdi_d = kbdi.resample("D").max()
m=kbdi_d.groupby(kbdi_d.index.year).sum().rainfall.mean()/25.4
for i in kbdi_d.iterrows():
    r = i[1][0]/25.4
    rr.append(r)
    t = i[1][1]*1.8+32
    tt.append(t)
    if r > 0.2:
        if r_cons == True:
            remove = 0
        else:
            remove = 0.2
        k -= (r - remove)*100
        r_cons = True
    else:
        r_cons = False
    k+=(800-k)*(0.968*np.exp(0.0486 * t))*(0.001/(1+(10.88*np.exp(-0.0441*m))))

    fin.append(k)
    
plt.plot(kbdi_d.index,fin) 
#    
#n=pd.Series(index=kbdi.index)
#n['index']=kbdi.index