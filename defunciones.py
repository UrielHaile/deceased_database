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

        self.causa_auto = ['X600', 'X608', 'X609', 'X610', 'X618', 'X619', 'X620', 'X625', 'X630', 'X640',
                           'X644', 'X648', 'X649', 'X650', 'X654', 'X660', 'X669', 'X670', 'X677', 'X679',
                           'X680', 'X681', 'X683', 'X684', 'X685', 'X686', 'X687', 'X688', 'X689', 'X690',
                           'X691', 'X694', 'X695', 'X696', 'X697', 'X698', 'X699', 'X700', 'X701', 'X702',
                           'X703', 'X704', 'X705', 'X706', 'X707', 'X708', 'X709', 'X710', 'X711', 'X714',
                           'X715', 'X717', 'X718', 'X719', 'X720', 'X724', 'X725', 'X727', 'X728', 'X730',
                           'X737', 'X739', 'X740', 'X741', 'X742', 'X744', 'X745', 'X746', 'X747', 'X748',
                           'X749', 'X760', 'X764', 'X765', 'X768', 'X769', 'X780', 'X781', 'X784', 'X785',
                           'X787', 'X788', 'X789', 'X790', 'X800', 'X801', 'X802', 'X804', 'X805', 'X806',
                           'X807', 'X808', 'X809', 'X814', 'X815', 'X817', 'X818', 'X824', 'X828', 'X829',
                           'X830', 'X839', 'X840', 'X841', 'X842', 'X844', 'X845', 'X847', 'X848', 'X849']

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
        ent_regis_fil = state[state.causa_def.isin(self.causa_auto)]
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

