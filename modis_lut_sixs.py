import os
import time
import numpy as np


class MODIS_LUT_SixS:
    def __init__(self, results_directory, sixs_cmd):
        self.results_directory = results_directory
        self.sixs_cmd = sixs_cmd
        self.in_name = self.results_directory + 'input.txt'
        self.out_name = self.results_directory + 'output.txt'
        self.lut_name = self.results_directory + 'modis_lut_blue_marine.txt'
        self.igeom = 0
        self.sz = np.arange(0.0, 80.1, 4, dtype=np.float64)  # Solar Zenith
        self.sa = np.arange(0.0, 180.1, 6, dtype=np.float64)  # Solar Azimuth
        self.vz = np.arange(0.0, 80.1, 4, dtype=np.float64)  # View Zenith/Sensor Zenith
        self.va = 0.0  # View Azimuth/Sensor Azimuth
        self.month = 9  # Month of Date
        self.day = 1  # Day of Date
        self.idatm = 2
        self.iaer = 2
        self.v = 0
        self.aod = [0.01, 0.25, 0.50, 1.00, 1.25, 1.50, 2.00, 3.00, 5.00]  # Set Value of AOD  0.01, 0.25, 0.50, 1.00, 1.25, 1.50, 2.00, 3.00,
        self.xps = 0
        self.xpp = -1000  # Sensor On the Satellite
        self.iwave = 44  # Red/Blue Band of MODIS
        self.inhomo = 0
        self.idirec = 0
        self.igroun = 1
        self.rapp = -2

    def _lut_create_(self):
        modis_lut_txt = open(self.lut_name, 'w')
        for i_aod in self.aod:
            for i_sz in self.sz:
                for i_vz in self.vz:
                    for i_sa in self.sa:
                        in_txt = open(self.in_name, 'w')
                        in_txt.write(str(self.igeom) + '\n')
                        in_txt.write(str(i_sz) + '\n')
                        in_txt.write(str(i_sa) + '\n')
                        in_txt.write(str(i_vz) + '\n')
                        in_txt.write(str(self.va) + '\n')
                        in_txt.write(str(self.month) + '\n')
                        in_txt.write(str(self.day) + '\n')
                        in_txt.write(str(self.idatm) + '\n')
                        in_txt.write(str(self.iaer) + '\n')
                        in_txt.write(str(self.v) + '\n')
                        in_txt.write(str(i_aod) + '\n')
                        in_txt.write(str(self.xps) + '\n')
                        in_txt.write(str(self.xpp) + '\n')
                        in_txt.write(str(self.iwave) + '\n')
                        in_txt.write(str(self.inhomo) + '\n')
                        in_txt.write(str(self.idirec) + '\n')
                        in_txt.write(str(self.igroun) + '\n')
                        in_txt.write(str(self.rapp) + '\n')
                        in_txt.close()
                        os.system(sixs_cmd)
                        out_txt = open(self.out_name, 'r')
                        lines_txt = out_txt.readlines()
                        out_T = lines_txt[123].split(' ')[-10]
                        out_S = lines_txt[129].split(' ')[-10]
                        out_rou = lines_txt[132].split(' ')[-10]
                        print(out_rou)
                        out_txt.close()
                        modis_lut_txt.write(
                            out_rou + ' ' + out_T + ' ' + out_S + ' '
                            + str(i_sz) + ' ' + str(i_vz) + ' ' + str(i_sa) + ' ' + str(i_aod) + '\n')
        modis_lut_txt.close()


if __name__ == '__main__':
    start_time = time.time()
    results_directory = '/mnt/d/Experiments/AOD_Retrieval/Models/6SV-1.1_Linux/Results/'
    sixs_cmd = './sixsV1.1</mnt/d/Experiments/AOD_Retrieval/Models/6SV-1.1_Linux/Results/input.txt>/mnt/d/Experiments/AOD_Retrieval/Models/6SV-1.1_Linux/Results/output.txt'
    modis_lut_sixs = MODIS_LUT_SixS(results_directory, sixs_cmd)
    modis_lut_sixs._lut_create_()
    end_time = time.time()
    run_time = round(end_time - start_time, 3)
    print('The LUT of Sixs is saved! Time consuming is ' + str(run_time) + ' s.')
