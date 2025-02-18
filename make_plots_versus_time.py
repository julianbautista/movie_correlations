import numpy as np
from matplotlib import pyplot as plt
import pickle 

plt.ion()

def load(filename):
    output = pickle.load(open(filename, 'rb'))
    return output

'''
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

species = ['delta_baryon','delta_cdm', 'delta_photon', 'delta_neutrino',
           'delta_tot', 'Weyl']

'''

suffix = 'mnu0.10_v2'
data = load(f'camb_outputs/camb_outputs_{suffix}.pkl')
#data = load(f'camb_outputs.pkl')

names = ['Baryons', 'Cold Dark Matter', 'Photons', 'Neutrinos', 'Total Matter', 'Weyl Potential']
c_ls = {'Baryons': ['C0','-'], 
                'Cold Dark Matter': ['purple', '-'],
                'Photons': ['C3', '--'],
                'Neutrinos': ['C1', ':'],
                'Total Matter': ['k', '-']}


a = data['scale_factor']
pk = data['pk']

k = data['k']
ks = [1e-3, 1e-2, 1e-1, 1]
k_index = [170, 341, 511, 682]

for i, ki in enumerate(k_index): 
    plt.figure(figsize=(5, 4)) 

    for j in [0, 1, 2, 3]:

        plt.plot(a, pk[ki, :, j]/a, color=c_ls[names[j]][0], ls=c_ls[names[j]][1], lw=2, label=names[j]) 
    
    plt.legend(ncol=2)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlim(1e-6, 1)
    plt.ylim(1e-8, 1e4)
    plt.xlabel('Scale factor $a(t)$')
    plt.ylabel('P(k, a)/a')
    plt.title(rf'$k = {ks[i]} \ h \mathrm{{Mpc}}^{{-1}}$')
    plt.tight_layout()
    plt.savefig(f'plots/pk_versus_time_{suffix}_k{ks[i]}.pdf')