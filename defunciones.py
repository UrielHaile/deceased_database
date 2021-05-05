# -*- coding: utf-8 -*-
import pandas
import pandas as pd
import numpy as np
from array import *

"""
@author: Uriel Haile Hernández Belmonte
"""

class DefuncionesHandler:
    def __init__(self, cached: bool = True, year: int = 2018):
        self.path_catalogos = 'db/2019/catalogos/'
        self.path_entidad_municipio_localidad = self.path_catalogos + 'entidad_municipio_localidad.csv'
        self.entidad_municipio_localidad = pd.read_csv(self.path_entidad_municipio_localidad, header=0)

        self.df_decatcausa = pd.read_csv("./db/2018/catalogos/decatcausa.csv", header=0)
        self.df_autoinflingidas = self.df_decatcausa.query("clave >= 'X600' and clave < 'X850'")
        if cached:
            #            self.path_defunciones = 'db/defunciones_2019/DEFUN_2019/Defunciones_2019.csv'
            self.path_defunciones = 'db/' + str(year) + '/defunciones/defunciones.csv'
            self.defunciones = pd.read_csv(self.path_defunciones, header=0)

    def filter_by_ent(self, ent_regis):
        df_ent_regis = self.defunciones['ent_resid'] == ent_regis
        pos = np.flatnonzero(df_ent_regis)
        ent_regis = self.defunciones.iloc[pos]
        return ent_regis

    def filter_by_ent_and_causa_def(self, ent_regis):
        state = self.filter_by_ent(ent_regis)
        ent_regis_fil = state[state.causa_def.isin(self.df_autoinflingidas.clave)]
        return ent_regis_fil

    def filter_ent(self) -> pandas.DataFrame:
        df_ent = self.entidad_municipio_localidad['cve_mun'] == 0
        pos = np.flatnonzero(df_ent)
        ent = self.entidad_municipio_localidad.iloc[pos]
        # The data contains some unnecessary rows
        to_remove = array('i', range(ent.shape[0] - 5, ent.shape[0]))
        df_ent_filtered = ent.drop(ent.index[to_remove])
        return df_ent_filtered

    def get_cve_ent(self, name: str) -> np.int64:
        df_ent = self.filter_ent()
        index = df_ent['nom_loc'].str.match(name)
        dt_row = df_ent[index]
        if dt_row.shape[0] == 1 and dt_row.shape[1] == 4:
            return dt_row.iloc[0, 0]
        return np.int64(-1)

    def get_mun_ent(self, df_ent: pandas.DataFrame):
        pos = np.flatnonzero(df_ent)
        ent = self.defunciones.iloc[pos]
        return ent

    def get_mun_ent_regis(self, ent_id):
        df_ent_regis = self.defunciones['ent_regis'] == ent_id
        return self.get_mun_ent(df_ent_regis)

    def get_mun_ent_resid(self, ent_id):
        df_ent_resid = self.defunciones['ent_resid'] == ent_id
        return self.get_mun_ent(df_ent_resid)

    def get_mun_ent_names(self, ent_id: int):
        """
        :type ent_id: Identification number of the state
        """
        df = self.entidad_municipio_localidad
        df_ent = df.loc[(df['cve_ent'] == ent_id) & (df['cve_loc'] == 0)]
        filter_ent = df_ent.loc[:, ['cve_mun', 'nom_loc']]
        filter_ent.set_index('cve_mun', drop=True, inplace=True)
        return filter_ent

