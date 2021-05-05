#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import defunciones as df

years = (2014, 2015, 2016, 2017, 2018, 2019)
year = 2018
defunciones_total = pd.DataFrame()
for year in years:
    defunciones = df.DefuncionesHandler(True, year=year)
    ent = defunciones.get_cve_ent('Guanajuato')
    guanajuato = defunciones.filter_by_ent_and_causa_def(ent)
    mun = defunciones.get_mun_ent_names(ent)
    d = mun.T.to_dict('index')
    mun_resid = guanajuato["mun_resid"].map(d['nom_loc'])
    mun_count = mun_resid.value_counts()

    for key in mun['nom_loc']:
        if not (key in mun_count):
            mun_count[key] = 0
    #print(mun_count)
    print("Año " + str(year) + " total: " + str(mun_count.sum()))
    mun_count.sort_index(inplace=True)

    if not defunciones_total.empty:
        defunciones_total = pd.concat([defunciones_total, mun_count], axis=1)
    else:
        defunciones_total = mun_count
    #mun_count.to_csv('suicidio_' + str(year) + '.csv')
#print(defunciones_total)