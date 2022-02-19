import time
import numpy as np
from matplotlib import pyplot as plt
import camb
import hankl
import pickle 
plt.ion()

output_file = 'pk_xi_2022_02_17.pkl'

def save(output, filename): 
    pickle.dump(output, open(filename, 'wb'))

def load(filename):
    output = pickle.load(open(filename, 'rb'))
    return output

#Set up a new set of parameters for CAMB
pars = camb.CAMBparams(scalar_initial_condition='initial_adiabatic')

#This function sets up CosmoMC-like settings, with one massive neutrino and helium set using BBN consistency
pars_cosmo = {'ombh2': 0.0224, 
              'omch2': 0.120, 
              'mnu': 0.00, 
              'tau': 0.054, 
              'cosmomc_theta':1.0411/100,
              'omk':0,
              }

pars_init = {'As': np.exp(3.043)*1e-10, 
             'ns': 0.9652}

pars.set_cosmology(H0=None, **pars_cosmo)
pars.InitPower.set_params(r=0, **pars_init)
#pars.set_for_lmax(2500, lens_potential_accuracy=0)
pars.set_accuracy(AccuracyBoost=3, lAccuracyBoost=3)
#pars.set_matter_power(redshifts=[0., 0.8], kmax=10.0)

data = camb.get_transfer_functions(pars)

#pars.set_matter_power(redshifts=[0.], kmax=10.0)
#results = camb.get_results(pars)

#h, z, pk = results.get_matter_power_spectrum(minkh=1e-3, maxkh=1, npoints = 200)

scale_factor  = 10**np.linspace(-10, 0, 1000)
redshifts = 1/scale_factor - 1 

nsteps = len(redshifts)

colors = plt.cm.jet(np.linspace(0, 1, nsteps))

nk = 1024
ks = 10**np.linspace(-4, 2, nk)

species = ['delta_baryon','delta_cdm', 'delta_photon', 'delta_neutrino',
            'delta_tot', 'Weyl']

time0 = time.time()
print('Computing evolution...')
evolution = data.get_redshift_evolution(ks, redshifts, species, lAccuracyBoost=5)
time1 = time.time()
print(f'Done in {(time1-time0)/60:.3f} minutes.')

eta = data.conformal_time(redshifts)
sound_horizon = data.sound_horizon(redshifts)


pk_init = 4/9*pars_init['As']*(ks/0.05)**(pars_init['ns']-1) * (2*np.pi**2/ks**3)

pk_final = pk_init[:, None, None] * evolution**2

pk_final[:, :, 0] *= (2/3)**2 
pk_final[:, :, 1] *= (2/3)**2
pk_final[:, :, 2] *= 1/4
pk_final[:, :, 3] *= 1/4
pk_final[:, :, 4] *= 1/4


time2 = time.time()
print('Computing hankel transforms...')
xi_final = np.zeros_like(evolution) 
for i in range(nsteps):   
    for j in range(4):        
        r, xi = hankl.P2xi(ks, pk_final[:, i, j], 0, n=0, lowring=False, ext=0, range=None, return_ext=False)
        xi_final[:, i, j] = xi.real*1
time3 = time.time()
print(f'Done in {(time3-time2)/60:.3f} minutes.')

output = {'pars_cosmo': pars_cosmo,
            'pars_init': pars_init, 
            'scale_factor': scale_factor,
            'redshifts': redshifts,
            'species': species,
            'conformal_time': eta,
            'sound_horizon': sound_horizon,  
            'k': ks, 
            'pk': pk_final,
            'r': r,
            'xi': xi_final}

derived_params = data.get_derived_params()
for k in derived_params:
    output[k] = derived_params[k]


save(output, output_file)
