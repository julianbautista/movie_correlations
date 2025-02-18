import time
import numpy as np
from matplotlib import pyplot as plt
import camb
import hankl
import pickle 
import os
plt.ion()

def save(output, filename): 
    pickle.dump(output, open(filename, 'wb'))

def load(filename):
    output = pickle.load(open(filename, 'rb'))
    return output


os.makedirs('camb_outputs', exist_ok=True)
output_file = 'camb_outputs/camb_outputs_mnu0.10_v2.pkl'
accuracy = 3

pars = camb.CAMBparams(scalar_initial_condition='initial_adiabatic')
pars_cosmo = {'ombh2': 0.0224, 
              'omch2': 0.120, 
              'mnu': 0.00, 
              'tau': 0.054, 
              'cosmomc_theta':1.0411/100,
              'omk':0,
              'nnu': 3.046,
              'mnu':0.10, 
              }
pars_init = {'As': np.exp(3.043)*1e-10, 
             'ns': 0.9652}

pars.set_cosmology(H0=None, **pars_cosmo)
pars.InitPower.set_params(r=0, **pars_init)
pars.set_accuracy(AccuracyBoost=accuracy, lAccuracyBoost=accuracy)

pars.set_matter_power(redshifts=[0.], kmax=10.0)
results = camb.get_results(pars)
kh, _, pk0 = results.get_matter_power_spectrum(minkh=1e-3, maxkh=1, npoints = 512)

data = camb.get_transfer_functions(pars)


scale_factor  = 10**np.linspace(-7, 0, 1000)
redshifts = 1/scale_factor - 1 

nsteps = len(redshifts)

colors = plt.cm.jet(np.linspace(0, 1, nsteps))

nk = 1024
ks = 10**np.linspace(-4, 2, nk)

species = ['delta_baryon','delta_cdm', 'delta_photon', 'delta_neutrino',
           'delta_tot', 'Weyl']
names = ['Baryons', 'Cold Dark Matter', 'Photons', 'Neutrinos', 'Total Matter', 'Weyl Potential']
n_species = len(species)


time0 = time.time()
print('Computing evolution...')
evolution = data.get_redshift_evolution(ks, redshifts, species, lAccuracyBoost=accuracy)
time1 = time.time()
print(f'Done in {(time1-time0)/60:.3f} minutes.')

eta = data.conformal_time(redshifts)
sound_horizon = data.sound_horizon(redshifts)


#-- Corrected by Thibaut Louis 2023/03/20
pk_init = pars_init['As'] * (ks / (0.05)) ** (pars_init['ns'] - 1) * (2 * np.pi ** 2 / ks ** 3) #initial condition given in term of R
pk_final = pk_init[:, None, None] * evolution ** 2

#-- Adiabatic initial conditions  delta_i / (1+w_i) = delta_j / (1+w_j)

#-- photons
pk_final[:, :, 2] *= (3/4)**2
#-- neutrinos
pk_final[:, :, 3] *= (3/4)**2


time2 = time.time()
print('Computing Hankel transforms to obtain correlation functions...')
xi_final = np.zeros_like(evolution) 
for i in range(nsteps):   
    for j in range(n_species):        
        r, xi = hankl.P2xi(ks, pk_final[:, i, j], 0, n=0, lowring=False, ext=0, range=None, return_ext=False)
        xi_final[:, i, j] = xi.real*1
time3 = time.time()
print(f'Done in {(time3-time2)/60:.3f} minutes.')

output = {  'pars_cosmo': pars_cosmo,
            'pars_init': pars_init, 
            'scale_factor': scale_factor,
            'redshifts': redshifts,
            'species': species,
            'names': names,
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
print(f'Output written at: {output_file}')