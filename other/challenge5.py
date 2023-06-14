import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.stats import linregress

study=pd.read_csv('Study_results.csv')
mouse=pd.read_csv('Mouse_metadata.csv')

print('The total number of mouse : ',len(mouse['Mouse ID'].unique()))
print('---------------------------------------------------------------------------')
# Find the duplicate rows


study_dup = study[study.duplicated(['Mouse ID','Timepoint'])]
display(study_dup)
print('---------------------------------------------------------------------------')
# Drop the duplicate rows from the original DataFrame and store it in new DataFrame


study_new = study.drop_duplicates(['Mouse ID','Timepoint'])
display(study_new)
print('---------------------------------------------------------------------------')
# Merge the 2 files on Mouse ID column after removing the duplicate rows


df=pd.merge(mouse,study_new,on='Mouse ID')
display(df)
print('---------------------------------------------------------------------------')
# Calculate statistics data for each Drug Regimen

statistics_info=df.groupby('Drug Regimen')[['Tumor Volume (mm3)']].agg(['mean','median','var','std','sem'])
display(statistics_info)
print('---------------------------------------------------------------------------')
# Get the Timeoint count for each Drug Regimen

df_1=df.groupby(['Drug Regimen'])[['Timepoint']].count()
df_2=df_1.reset_index()
display(df_2)
print('---------------------------------------------------------------------------')
# Plot the above result using DataFrame bar method

ax = plt.bar(df_2['Drug Regimen'],df_2['Timepoint'])
plt.xticks(rotation=45)
plt.xlabel('Drug Regimen')
plt.ylabel('Timepoint')
plt.title('Bar using plt')
plt.ylim(0,300)
plt.show()
print('---------------------------------------------------------------------------')
# Plot the above result using plot

df_2.plot(x='Drug Regimen',kind='bar',rot=45)
plt.show()
print('---------------------------------------------------------------------------')
# Get the count for Mouse ID ( Male and Female )

mf=df.groupby('Sex')[['Mouse ID']].count()
mf=mf.reset_index()
display(mf)
print('---------------------------------------------------------------------------')
# Piechart using DataFrame

plt.pie(mf['Mouse ID'],labels=mf['Sex'],autopct='%1.1f%%',explode=(0,0.1))
plt.show()
print('---------------------------------------------------------------------------')
# Piechart using plot

mf.plot.pie(y='Mouse ID',autopct='%1.1f%%',explode=(0,0.1),shadow=True,labels=mf['Sex'])
plt.show()
print('---------------------------------------------------------------------------')
# Get the max Timepoint for each mouse

greatest_tumore_volume_1=df.groupby('Mouse ID')[['Timepoint']].max()
greatest_tumore_volume=greatest_tumore_volume_1.reset_index()
display(greatest_tumore_volume)
print('---------------------------------------------------------------------------')
# Merge the above data with the original table

pd.merge(greatest_tumore_volume,df,on=['Mouse ID','Timepoint'])
print('---------------------------------------------------------------------------')
# Reset index for the merged data

df_1=df.groupby('Mouse ID')[['Timepoint']].max().reset_index()
df_3=pd.merge(df,df_1,on=['Mouse ID','Timepoint'])
display(df_3)
print('---------------------------------------------------------------------------')
# Append the max tumor data treatment list in a list

max_tumor_volume=[]

treatment=['Capomulin','Ramicane','Infubinol','Ceftamin']
for drug in treatment:
    
    max_tumor_volume+=df_3[df_3['Drug Regimen']==drug]['Tumor Volume (mm3)'].to_list()
    
print(max_tumor_volume)
print('---------------------------------------------------------------------------')
# Get the upper bound for the above list


maximun=max_tumor_volume[0]
for k in range(len(max_tumor_volume)-1):
    if max_tumor_volume[k]>=max_tumor_volume[k+1]:
        maximum=max_tumor_volume[k]
print(maximum)
print('---------------------------------------------------------------------------')
# Get the lower bound for the above list


minimum=max_tumor_volume[0]
for m in range(len(max_tumor_volume)-1):
    if max_tumor_volume[m]>=max_tumor_volume[m+1]:
        maximum=max_tumor_volume[m]
print(minimum)
print('---------------------------------------------------------------------------')
# Calculate the quartiles

df_3['Tumor Volume (mm3)'].quantile([0.25,0.5,0.75])
print('---------------------------------------------------------------------------')
# Calculate the IQR at 0,25

q_1=np.quantile(max_tumor_volume,0.25)
print('First IQR : ',q_1)

# Calculate the IQR at 0,5

q_2=np.quantile(max_tumor_volume,0.5)
print('Second IQR : ',q_2)

# Calculate the IQR at 0,75

q_3=np.quantile(max_tumor_volume,0.75)
print('Third IQR : ',q_3)
print('---------------------------------------------------------------------------')
# Get the data for Capomulin , Ramicane, Infubinol , Ceftamin and put them in a new DataFrame

treatment=['Capomulin','Ramicane','Infubinol','Ceftamin']
df_Capomulin=df_3[df_3['Drug Regimen']=='Capomulin']
df_Ramicane=df_3[df_3['Drug Regimen']=='Ramicane']
df_Infubinol=df_3[df_3['Drug Regimen']=='Infubinol']
df_Ceftamin=df_3[df_3['Drug Regimen']=='Ceftamin']
final_df=pd.concat([df_Capomulin,df_Ramicane,df_Infubinol,df_Ceftamin])
display(final_df)
print('---------------------------------------------------------------------------')
# Plot the above data using boxplot

boxplot = final_df.boxplot(column=['Tumor Volume (mm3)'],by='Drug Regimen',rot=45)
plt.show()
print('---------------------------------------------------------------------------')
# Get data for a unique mouse for Capomulin

df_10=df.loc[(df['Drug Regimen']=='Capomulin') & (df['Mouse ID']=='x401'),:]
display(df_10)
print('---------------------------------------------------------------------------')
# Plot the data for Tumor Volume (mm3) and Timepoint in a line

plt.plot (df_10['Timepoint'],df_10['Tumor Volume (mm3)'])
plt.xlabel('Timepoint',fontsize=20)
plt.ylabel('Tumor Volume',fontsize=20)
plt.show()
print('---------------------------------------------------------------------------')
# Create a DataFrame for Capomulin drug using Weight (g) and Tumor Volume (mm3)

weight_tumor=df_Capomulin.groupby('Weight (g)')[['Tumor Volume (mm3)']].mean().reset_index()
weight_tumor
print('---------------------------------------------------------------------------')
# Use scatter to plot the above data

plt.scatter(weight_tumor['Weight (g)'],weight_tumor['Tumor Volume (mm3)'])
plt.xlabel('Weight')
plt.ylabel('Tumor Volume')
plt.show()
print('---------------------------------------------------------------------------')
# Find the regression eqt and plot it with the scatter graph

x_values=weight_tumor['Weight (g)']
y_values=weight_tumor['Tumor Volume (mm3)']

(slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
regress_values = x_values * slope + intercept
line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.annotate(line_eq,(5.8,0.8),fontsize=15,color="red")
plt.xlabel('Weight (g)',fontsize=20)
plt.ylabel('Tumor Volume (mm3)',fontsize=20)
plt.title(line_eq)
plt.show()
