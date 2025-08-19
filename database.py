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

    def get_axiality(self):
        """
        Return optical axiality ('isotropic', 'uniaxial', 'biaxial') based on self.system
        """
        system = self.system.lower()
        if system in {"cubic"}:
            return "isotropic"
        elif system in {"tetragonal", "hexagonal", "trigonal", "rhombohedral"}:
            return "uniaxial"
        elif system in {"orthorhombic", "monoclinic", "triclinic"}:
            return "biaxial"
        else:
            raise ValueError(f"Unknown crystal system: {system}")


    def get_n(self, wavelength_nm, polarization='unpolarized'):
        """
        parameters
        wavelength_nm
        polarization:
            "iso",
            "o", "e", degree (float), 
            "a", "b", "c", {axis: a or b or c, degree: (float)}
        """
        wvl = wavelength_nm / 1e3  # μm
        range_min = self.sellmeier["range"][0]
        range_max = self.sellmeier["range"][1]
        if wvl < range_min or wvl > range_max:
            raise ValueError(f"Wavelength out of approximation range: {range_min}-{range_max} um")
        # n_squared = 1 + self.constant
        # for A, B in self.coefficients:
        #     n_squared += A * λ**2 / (λ**2 - B)
        
        if self.axiality == "isotropic":
            coeff =  self.sellmeier["iso"]
            n_squared = self._sellmeier_eq(wvl, coeff)
            n = np.sqrt(n_squared)
            return n

        elif self.axiality =="uniaxial":
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

        elif self.axiality == "biaxial":
            coeff_a = self.sellmeier["a"]
            coeff_b = self.sellmeier["b"]
            coeff_c = self.sellmeier["c"]
            n_a_squared = self._sellmeier_eq(wvl, coeff_a)
            n_b_squared = self._sellmeier_eq(wvl, coeff_b)
            n_c_squared = self._sellmeier_eq(wvl, coeff_c)
            n_a = np.sqrt(n_a_squared)
            n_b = np.sqrt(n_b_squared)
            n_c = np.sqrt(n_c_squared)

            if polarization == "a":
                return n_a
            elif polarization == "b":
                return n_b
            elif polarization == "c":
                return n_c
            elif type(polarization) == dict:
                if polarization["axis"] == "a":
                    theta = np.radians(polarization["degree"])


# -----------------
class LiNbO3(CrystalData):
    def __init__(self):
        self.name = "LiNbO3"
        self.crystal_system = "triagonal"
        self.axiality = self.get_axiality()
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
        self.crystal_system = "orthorhombic"
        self.axiality = self.get_axiality()
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

        self.sellmeier = {"a" : [2.1479, 0.00726962, 0.00965209, 8.10153, 1394.25, 0.00320462],
                          "b" : [2.07977, 0.00650243, 0.0100106, 8.18289, 1451.04, 0.00321466], 
                          "c" : [2.1285, 0.00704687, 0.00999784, 8.56752, 1413.17, 0.00331969],
                          "range" : [0.15, 10.0]} # rough assumption from graphs on the papaer
        
        self.reference = {"crystal_system": "https://next-gen.materialsproject.org/materials/mp-14568?formula=BaMgF4",
                          "refractive_index": "https://doi.org/10.1364/OE.17.012362"
        }
        
    def _sellmeier_eq(wavelength_um, coefficient, polarization="independent"):
        wvl = wavelength_um
        coeff = coefficient
        n_squared = coeff[0] + \
            (coeff[1] /(wvl**2 - coeff[2])) + \
            (coeff[3] * wvl**2 /(wvl**2 - coeff[4])) + \
            (coeff[5] * wvl**2)
        return n_squared
