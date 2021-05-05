# -*- coding: utf-8 -*-
import pandas as pd
import defunciones as df

defunciones = df.DefuncionesHandler(True, year=2014)

df_claves = pd.read_csv("./db/2018/catalogos/decatcausa.csv", header=0)
df_defunciones = df_claves.query("clave >= 'X600' and clave < 'X850'")
print(df_defunciones)