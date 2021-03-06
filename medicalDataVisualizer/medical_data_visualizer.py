import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('medical_examination.csv')


df['overweight'] = df['weight']/((df['height']/100)**2)
df.loc[df['overweight'] <= 25, 'overweight'] = 0
df.loc[df['overweight'] > 25, 'overweight'] = 1


df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1



def draw_cat_plot():
    
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'])['value'].count().to_frame()
    df_cat.rename(columns={'value': 'total'}, inplace=True)
    df_cat.reset_index(inplace=True)

  
    catplot = sns.catplot(x='variable', y='total', hue='value', col='cardio', kind='bar', data=df_cat)
    fig = catplot.fig

    
    fig.savefig('catplot.png')
    return fig



def draw_heat_map():
   
    height025 = df['height'].quantile(0.025)
    height975 = df['height'].quantile(0.975)
    weight025 = df['weight'].quantile(0.025)
    weight975 = df['weight'].quantile(0.975)
    df_heat = df[df['ap_lo'] <= df['ap_hi']]
    df_heat = df_heat[df_heat['height'] >= height025]
    df_heat = df_heat[df_heat['height'] <= height975]
    df_heat = df_heat[df_heat['weight'] >= weight025]
    df_heat = df_heat[df_heat['weight'] <= weight975]

    
    corr = df_heat.corr()
    corr = corr.round(1)

 
    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    
    fig, ax = plt.subplots(figsize=(12, 9))

    
    heat_map = sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", square=True)
    heat_map.set_yticklabels(heat_map.get_yticklabels(), rotation=0)
    heat_map.set_xticklabels(heat_map.get_xticklabels(), rotation=90)

   
    fig.savefig('heatmap.png')
    return fig
