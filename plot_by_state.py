import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

file = 'db/mortalidad_total.xlsx'

xl = pd.ExcelFile(file)
df1 = xl.parse('Tabulado')

years = np.array([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019])

fig = plt.figure()
ax1 = fig.add_subplot(111)

for i in range(5,36):
    gto_row = df1.iloc[i] 
    if i == 15:
        ax1.plot(years, gto_row[1:40:4].to_numpy(),'ro-', label= str(gto_row[0]))
    else:
        #plt.plot(years, gto_row[1:40:4].to_numpy(), label= str(gto_row[0]))
        if i == 18 or i == 19:
            if i == 18 :
                ax1.plot(years, gto_row[1:40:4].to_numpy(), 'g+-', label= str(gto_row[0]))
            else:
                ax1.plot(years, gto_row[1:40:4].to_numpy(), 'bx-', label= str(gto_row[0]))
        else:
            if i == 20:
                ax1.plot(years, gto_row[1:40:4].to_numpy(), linewidth = 1, color='C4', label = 'otras entidades')
            else:
                ax1.plot(years, gto_row[1:40:4].to_numpy(), linewidth = 1, color='C4')
        
plt.legend(fontsize='small')
plt.grid(True)
#ax1.xticks(years)
ax1.set_xticks(years)
plt.xlim([2010, 2019])

plt.title('Defunciones por suicidio')
plt.xticks(fontsize='x-small') 
plt.yticks(fontsize='x-small') 
plt.xlabel('Año')
plt.ylabel('Suicidios')
plt.show()