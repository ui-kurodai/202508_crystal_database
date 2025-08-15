from abc import ABC, abstractmethod
import numpy as np
from sympy import symbols, Matrix


class CrystalData(ABC):
    @abstractmethod
    def _sellmeier_eq(wavelength_um, coefficient, polarization="independent"):
        """
        Inplement respectively in each material class.
        polarization needs to be specified only when sellmeier eq. looks different between o/e.
        """
        pass

    def get_n(self, wavelength_nm, polarization='unpolarized'):
        wvl = wavelength_nm / 1e3  # μm
        range_min = self.sellmeier["range"][0]
        range_max = self.sellmeier["range"][1]
        if wvl < range_min or wvl > range_max:
            raise ValueError(f"Wavelength out of approximation range: {range_min}-{range_max} um")
        # n_squared = 1 + self.constant
        # for A, B in self.coefficients:
        #     n_squared += A * λ**2 / (λ**2 - B)
        
        coeff_o = self.sellmeier["o"]
        coeff_e = self.sellmeier["e"]
        n_o_squared = self._sellmeier_eq(wvl, coeff_o)
        n_e_squared = self._sellmeier_eq(wvl, coeff_e)
        n_o = np.sqrt(n_o_squared)
        n_e = np.sqrt(n_e_squared)

        if polarization == "o":
            return n_o
        elif polarization == "e":
            return n_e
        elif type(polarization) == "float":
            theta = np.radians(polarization)
            n_eff = n_o*n_e / np.sqrt((n_o**2)*(np.sin(theta)**2) + (n_e**2)*(np.cos(theta)**2))
            return n_eff
        
        else:
            raise ValueError(f"Polarization has to be 'o/e' or degree from optic axis: {polarization}")


# -----------------
class LiNbO3(CrystalData):
    def __init__(self):
        self.name = "LiNbO3"
        self.crystal_system = "Triagonal"
        self.point_group = "3m"
        d_15, d_22, d_31, d_33 = symbols("d_15 d_22 d_31 d_33")
        self.d_matrix = lambda kleinmann=True: Matrix([
            [0, 0, 0, 0,  d_15, -d_22],
            [-d_22, d_22, 0, d_15, 0,  0],
            [d_31, d_31, d_33, 0, 0, 0]
        ]) if not kleinmann else Matrix([
            [0, 0, 0, 0,  d_31, -d_22],
            [-d_22, d_22, 0, d_31, 0,  0],
            [d_31, d_31, d_33, 0, 0, 0]
        ])

        self.sellmeier = {"o" : [1, 2.6734, 0.001764, 1.2290, 0.05914, 474.60],
                          "e" : [1, 2.9804, 0.02047, 0.5981, 0.0666, 8.9543, 416.08], 
                          "range" : [0.4, 5.0]}
        
        self.reference = {"crystal_system": "https://next-gen.materialsproject.org/materials/mp-552588?formula=LiNbO3",
                          "refractive_index": "https://refractiveindex.info/?shelf=main&book=LiNbO3&page=Zelmon-o"
        }
        
    def _sellmeier_eq(wavelength_um, coefficient, polarization="independent"):
        wvl = wavelength_um
        coeff = coefficient
        n_squared = coeff[0] + \
            (coeff[1] * wvl**2 /(wvl**2 - coeff[2])) + \
            (coeff[3] * wvl**2 /(wvl**2 - coeff[4])) + \
            (coeff[5] * wvl**2 /(wvl**2 - coeff[6]))
        return n_squared
    
# -----------------
class BaMgF4(CrystalData):
    def __init__(self):
        self.name = "BaMgF4"
        self.crystal_system = "Orthorhombic"
        self.point_group = "mm2"
        d_15, d_24, d_31, d_32, d_33 = symbols("d_15 d_24 d_31 d_32 d_33")
        self.d_matrix = lambda kleinmann=True: Matrix([
            [0, 0, 0, 0,  d_15, 0],
            [0, 0, 0, d_24, 0,  0],
            [d_31, d_32, d_33, 0, 0, 0]
        ]) if not kleinmann else Matrix([
            [0, 0, 0, 0,  d_31, 0],
            [0, 0, 0, d_32, 0,  0],
            [d_31, d_32, d_33, 0, 0, 0]
        ])

        self.sellmeier = {"o" : [],
                          "e" : [], 
                          "range" : [0.15, 10.0]} # rough assumption from graphs on the papaer
        
        self.reference = {"crystal_system": "https://next-gen.materialsproject.org/materials/mp-14568?formula=BaMgF4",
                          "refractive_index": "https://doi.org/10.1364/OE.17.012362"
        }
        
    def _sellmeier_eq(wavelength_um, coefficient, polarization="independent"):
        wvl = wavelength_um
        coeff = coefficient
        n_squared = coeff[0] + \
            (coeff[1] * wvl**2 /(wvl**2 - coeff[2])) + \
            (coeff[3] * wvl**2 /(wvl**2 - coeff[4])) + \
            (coeff[5] * wvl**2 /(wvl**2 - coeff[6]))
        return n_squared
