import numpy as np
# from munch import Munch
from functions import *
from user_paths import *



"""
This file contain several classes to store parameters:
    *   physics_units   (c, mpc, AU, kb, etc)
    *   cosmo_params    (H0, ns, etc. )

    *   Powerspectrum  
        *   Pk_model.powerlaw
        *   Pk_model.lognormal
        *   Pk_model.gaussian
        *   Pk_model.broken_powerlaw

    *   PBH formation models
        *   standard formation model
        *   Musco20 model

    *   Mergin rates
        *   PBH binaries
        *   Clusters
"""


#######################################################################
# Units and cosmological parameters
#######################################################################

# units and constants
@froze_it
class p_PhysicsUnits:
    class addvars:
        pass 
    def __init__(self):
        self.c = 2.997924e8                     # (*Speed of light, [m/s] *)
        self.mpc = 3.085678e22                  # (* Megaparsec [m] *)
        self.pc = 3.086e16                      # (*parsec [m]*)
        self.G = 6.67428e-11                    # (* Gravitational constant [m^3/kg/s^2] *)
        self.m_sun = 1.989e30                   # (* Sun mass [kg]*)
        self.year = 365.25 * 24 * 3600          # (* year in seconds[s] *)
        self.hbar = 6.62607e-34 / (2. * np.pi)  # (* reduced planck constant in m^2 kg /s*)
        self.hp = 6.582e-16                     # (* Planck constant in eV s *)
        self.AU = 1.4960e11                     # (* Astronomical unit [m]*)
        self.kb = 8.617343e-5                   # (* Boltzmann constant [eV /K] *);
        self.eV_in_J = 1.60217e-19              # (*eV in Joule *)
        self.l_planck = 1.61e-35                # (*Planck length [m]*)
        self.rho_planck = 5.155e96              # (*Planck energy [kg/m^3]*)
        self.m_planck = 1.22e19                 # (*Planck mass [eV]*)
        self.additional_vars = self.addvars

# Standard cosmological parameters
@froze_it
class p_CosmologicalParameters:
    class addvars:
        pass 
    
    def __init__(self):
        physics_units = p_PhysicsUnits()
        self.ns = 0.961
        self.As = 2.1e-9
        self.Omb = 0.0456
        self.Omc = 0.245
        self.h = 0.7
        self.Nur = 3.046
        self.TCMB = 2.726
        self.kstar = 0.05 
        self.kp = 2.e6
        self.additional_vars = self.addvars

        # derived cosmological parameters
        self.H0 = self.h * 100000. / physics_units.mpc                          # (* Hubble rate today, [s^-1] *)
        self.rhocr = 3. * self.H0 ** 2 / (8. * np.pi * physics_units.G)         # (* Critical Density [kg/m^3] *)
        self.ar = 7.5657e-16                                                    # (* Stephan's constant in J m^-3 K^-4 *);
        self.Omr = self.ar * self.TCMB ** 4 / self.rhocr / physics_units.c ** 2 # (* Density of photons *)
        self.Omnu = self.Omr * 7. / 8 * self.Nur * (4. / 11.) ** (4. / 3.)      # (* Density of neutrinos *)
        self.OmLambda = 1. - (self.Omc + self.Omb + self.Omr + self.Omnu)       # (* Density of Dark Energy *)
        


#######################################################################
# Curvature power sperctrum Models:   Pk_models
#######################################################################

@froze_it
class p_PowerSpectrumGaussian:
    def __init__(self):
        self.name = "gaussian"
        self.kp = 2.e6           # Reference scale [mpc^-1] (2.e6 corresponds to mPBH = 1 Msun)
        self.AsPBH = 0.0205      # Power spectrum amplitude at the reference scale kp.
        self.sigma =  0.2        # Power spectrum variance.

@froze_it
class p_PowerSpectrumPowerlaw:
    def __init__(self):
        self.name = "powerlaw"
        self.ktrans = 1.e0      # Scale of the transition between CMB amplitude and PBH amplitude
        self.nsPBH = 0.97       # Spectral index
        self.kp = 2.e6          # Reference scale [mpc^-1] (2.e6 corresponds to mPBH = 1 Msun)
        self.AsPBH = 0.0205     # Power spectrum amplitude at the reference scale kp.

@froze_it
class p_PowerSpectrumLogNormal:
    def __init__(self):
        self.name = "lognormal"
        self.kp = 2.e6         # Reference scale [mpc^-1] (2.e6 corresponds to mPBH = 1 Msun)
        self.AsPBH = 0.0205    # Power spectrum amplitude at the reference scale kp.
        self.sigma = 1.        # Power spectrum amplitude at the reference scale kp.

@froze_it
class p_PowerSpectrumBrokenPowerlaw:
    def __init__(self):
        self.name = "broken_powerlaw"
        self.kp = 2.e6               # Reference scale [mpc^-1] (2.e6 corresponds to mPBH = 1 Msun)
        self.AsPBH = 0.0205          # Power spectrum amplitude at the reference scale kp.
        self.kc = 2.e6               # k critical: splits btw low/high
        self.kp_low = self.kp
        self.kp_high = self.kp
        self.AsPBH_low = self.AsPBH
        self.AsPBH_high = self.AsPBH
        self.ns_low = -0.1
        self.ns_high = -0.5

@froze_it
class p_PowerSpectrumMultifield:
    def __init__(self):
        self.name = "multifield"
        self.kf = 2e6          # scale H-crossing at sharp turn  [mpc^-1]
        self.P0 = 2e-9        # Amplitude Pk in absence of transient instability
        self.eta = 4.           # TODO: check value
        self.delta = 2.2          # TODO: check value
        self.kp = self.kf

@froze_it
class p_PowerSpectrumAxionGauge:
    def __init__(self):
        self.name = "axion_gauge"
        self.kp = 2.1e6           # Reference scale [mpc^-1] (2.e6 corresponds to mPBH = 1 Msun)
        self.As_vac = 0.0205      # TODO: k-dependent
        self.AsPBH = 0.0205       # TODO: k-dependent
        self.sigma = 1.           # TODO: k-dependent

@froze_it
class p_PowerSpectrumPreheating:
    def __init__(self):
        self.name = "preheating"
        self.kend = 2.e6             #
        self.Hstar = 1.0e14          # TODO: k-dependent
        self.e1 = 0.01               # TODO: k-dependent
        self.e2 = 0.0001             # TODO: k-dependent
        self.C = -0.7296          
        self.kp = self.kend

@froze_it
class p_PowerSpectrumUserImport:
    class addvars:
        pass 
    def __init__(self):
        self.name = "user_import"
        self.user_k = None
        self.user_PS = None 
        self.additional_vars = self.addvars

@froze_it
class p_PowerSpectrumUserFunction:
    class addvars:
        pass 
    def __init__(self):
        self.name = "user_function"
        self.user_function = None
        self.additional_vars = self.addvars

@froze_it
class p_PowerSpectrumVacuum:
    def __init__(self):
        self.name = "vacuum"

@froze_it
class p_PowerSpectrumModels:
    def __init__(self):
        # List of models: 
        self.gaussian = p_PowerSpectrumGaussian()
        self.powerlaw = p_PowerSpectrumPowerlaw()
        self.lognormal = p_PowerSpectrumLogNormal()
        self.broken_powerlaw = p_PowerSpectrumBrokenPowerlaw()
        self.axion_gauge = p_PowerSpectrumAxionGauge()
        self.preheating = p_PowerSpectrumPreheating()
        self.multifield = p_PowerSpectrumMultifield()
        self.user_import = p_PowerSpectrumUserImport()
        self.user_function = p_PowerSpectrumUserFunction()
        self.vacuum = p_PowerSpectrumVacuum()

@froze_it
class p_PowerSpectrum:
    p_models = p_PowerSpectrumModels

    def __init__(self):
        # default selection:
        self.model = 'powerlaw'
    
    



#######################################################################
#  PBH formation Model
#######################################################################

# standard formation model
@froze_it
class p_PBHFormationModelStandard:
    def __init__(self):  
        self.name = "standard"
        self.deltacr_rad = 0.41  #1.02

# Musco20 formation model
@froze_it
class p_PBHFormationModelMusco20:
    def __init__(self):
        self.name = "Musco20"
        self.eta = 0.1
        self.k_star =  2.1e6

# Collection of params for PBH formation models 
@froze_it
class p_PBHFormationModel:
    # standard = p_PBHFormationModelStandard()
    # Musco20 = p_PBHFormationModelMusco20()
    def __init__(self):
        self.standard = p_PBHFormationModelStandard()
        self.Musco20 = p_PBHFormationModelMusco20()

# General params for PBH formation
@froze_it
class p_PBHFormation:
    p_model=p_PBHFormationModel()

    def __init__(self):

        # generic params for PBH formation
        self.ratio_mPBH_over_mH = 0.8             # Ratio between PBH and Hubble masses at formation
        self.kmsun = 2.1e6
        self.Pkrescaling = True                   # option to rescale the power spectrum to get a fixed DM fraction
        self.forcedfPBH = 1.                      # Imposed DM fraction made of PBHs
        self.Pkscalingfactor = 1.
        self.use_thermal_history = True           # option to include the effect of the equation-of-state changes due to the known thermal history
        self.data_directory = datadir
        self.zetacr_thermal_file = zetacr_file    # File of the evolution of zeta_cr with thermal history
        self.zetacr_thermal_rad = 1.02            # Reference value of zeta_cr for this file
        self.Gaussian = True                      # Asssume Gaussian statistics (for now it must be True) #TODO
        
        # default model selection
        self.model = 'standard'

        # class containing specific model params 
        # self.p_model = p_PBHFormationModel()


#######################################################################
# Model merging rates
#######################################################################

# Primordial binaries
@froze_it
class p_MerginRatesPrimordial:
    def __init__(self):
        self.wanted = True
        self.norm = 1.6e6
        self.fsup = 0.0025  # Rate suppression factor from N-body simulations when f_PBH > 0.1

# Tidal capture in clusters
@froze_it
class p_MerginRatesClusters:
    def __init__(self):
        self.wanted = True
        self.Rclust = 400.

# General class containing parameters for merging rates
@froze_it
class p_MergingRates:
    def __init__(self):
        self.primordial = p_MerginRatesPrimordial()
        self.clusters = p_MerginRatesClusters()









if __name__ == "__main__":

    # This is a simple exemple, call and print params. 

    physics_units = p_PhysicsUnits()
    print("c = ", physics_units.c)
    
    physics_units.additional_vars.cc = 1
    print("cc = ", physics_units.additional_vars.cc)

    try:
        physics_units.cc = 1
        print("cc = ", physics_units.additional_vars.cc)
    except AttributeError as e: 
        print("\
              The class is frozen, \n\
              so it doesn't allow to create vars as attributes.\n\
              But you can use self.additional_vars.<new_var> . ")