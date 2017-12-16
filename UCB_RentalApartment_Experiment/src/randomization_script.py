# -*- coding: utf-8 -*-
import random
import numpy as np
import pandas as pd

df=pd.read_csv("/home/romulo/github/Rental-Apartment-Response-Rate-Experiment/src/data/craigslist_ny_listings_cleaned_20171110_openrefine.csv")
df=df[~pd.isnull(df.Neighborhood)]


df=df.groupby('Listed By Cleaned').apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
#need to disregard pilot study subjects
pilotStudySubjects = (pd.read_csv("/home/romulo/github/Rental-Apartment-Response-Rate-Experiment/src/data/pilotStudySubjects.csv"))['pilotStudyListedBy'].unique()
df = df[~df['Listed By Cleaned'].isin(pilotStudySubjects) ]

treatment1={}
treatment20={}
treatment21={}
neighborhood_list=[]

Neighborhood_group=df.groupby('Neighborhood')
for Neighborhood in df['Neighborhood'].unique():
    n=Neighborhood_group.Neighborhood.count()[Neighborhood]
    if n>=4:
        neighborhood_list.append(Neighborhood)
        if n%2==0:
            n1=n
            if n%4==0:
                n2=n
            else:
                n2=n+2
        else:
            n1=n+1
            if n1%4==0:
                n2=n1
            else:
                n2=n1+2
        
        treatment1[Neighborhood]=(int(n1/2)*[0])+(int(n1/2)*[1])
        treatment20[Neighborhood]=(int(n2/4)*[0])+(int(n2/4)*[1])
        treatment21[Neighborhood]=(int(n2/4)*[0])+(int(n2/4)*[1])
            
        np.random.shuffle(treatment1[Neighborhood])
        np.random.shuffle(treatment20[Neighborhood])
        np.random.shuffle(treatment21[Neighborhood])


treatment1_vector=[]
treatment2_vector=[]
df3=df[df['Neighborhood'].isin(neighborhood_list)]
df3=df3.reset_index(drop=True)
       
for i in range(len(df3)):
    treatment1_vector.append(treatment1[df3['Neighborhood'][i]].pop())
    if treatment1_vector[i]==0:
        treatment2_vector.append(treatment20[df3['Neighborhood'][i]].pop())
    else:
        treatment2_vector.append(treatment21[df3['Neighborhood'][i]].pop())
        
df3['treatment1']=treatment1_vector
df3['treatment2']=treatment2_vector

df3.to_csv("/home/romulo/github/Rental-Apartment-Response-Rate-Experiment/src/data/craigslist_post_treatment.csv")


dzz = df3[(df3['treatment1'] == 0) & (df3['treatment2']==0)]
dzz.to_csv("/home/romulo/github/Rental-Apartment-Response-Rate-Experiment/src/data/craigslist_post_treatment_0_0.csv")
