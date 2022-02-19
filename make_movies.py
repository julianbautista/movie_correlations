import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import pickle 

#plt.ion()


def load(filename):
    output = pickle.load(open(filename, 'rb'))
    return output


def simple_animation():
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True)
    plt.show()



def xi_animation(data, rmin=0, rmax=300, i_range=None, interval=30):

    r = data['r']
    xi_all = data['xi']
    w = (r>=rmin) & (r<rmax)
    r = r[w]
    xi = xi_all[w]

    conformal_time = data['conformal_time']
    sound_horizon = data['sound_horizon']
    redshifts = data['redshifts']
    names = ['Baryons', 'Cold Dark Matter', 'Photons', 'Neutrinos']
    linestyles = ['-', '-', '--', ':']
    colors = ['C0', 'k', 'C3', 'C1']

    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2)
    lines = []
    for j in range(4):
        line, = ax.plot([], [], color=colors[j], ls=linestyles[j], lw=2, label=names[j])
        lines.append(line)
    line = ax.axvline(0, color='k', ls='--', alpha=1, lw=1, label='Horizon')
    lines.append(line)
    line = ax.axvline(0, color='C0', ls='--', alpha=1, lw=1, label='Sound horizon')
    lines.append(line)

    def init():

        ax.set_xlim(0, 300)
        #ydata = xi[:, i_range[0], i_species] * r**2
        #ax.set_ylim(np.min(ydata), np.max(ydata))
        #line.set_data(r, ydata)
        #ax.figure.canvas.draw()
        ax.set_ylabel(r'$r^2 \xi(r)$', fontsize=12)
        ax.set_xlabel(r'$r$ [Mpc]', fontsize=12)
        return lines,

    def update(frame):

        ydatas = []
        for j in range(4):
            line = lines[j]
            ydata = xi[:, frame, j] * r**2
            line.set_data(r, ydata)
            ydatas.append(ydata)
        

        ymin = np.min(ydatas)
        ymax = np.max(ydatas)
        ymin_ = ymin - 0.05*(ymax-ymin)
        ymax_ = ymax + 0.05*(ymax-ymin)
        line = lines[4]
        line.set_xdata(conformal_time[frame])
        line = lines[5]
        rs = sound_horizon[frame]
        if rs <= data['rdrag']:
            line.set_xdata(rs)
        else:
            line.set_alpha(np.exp(-0.5*(rs-data['rdrag'])**2/40**2))

        ax.set_ylim(ymin_, ymax_)
        ax.set_title(f'z = {redshifts[frame]:.1f}', fontsize=12)
        ax.legend(loc='upper right')
        
        #lines[6].set_data(sound_horizon[frame])
        
        ax.figure.canvas.draw()
        return lines,

    ani = FuncAnimation(fig, update, frames=i_range,
                        interval=interval,
                        init_func=init, blit=False)
    return ani

def pk_animation(data, kmin=1e-4, kmax=10, scale_k=2, i_range=None, interval=30):


    k = data['k']
    pk_all = data['pk']
    w = (k>=kmin) & (k<kmax)
    k = k[w]
    pk = pk_all[w]

    conformal_time = data['conformal_time']
    sound_horizon = data['sound_horizon']
    redshifts = data['redshifts']
    names = ['Baryons', 'Cold Dark Matter', 'Photons', 'Neutrinos']
    linestyles = ['-', '-', '--', ':']
    colors = ['C0', 'k', 'C3', 'C1']


    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2)
    lines = []
    for j in range(4):
        line, = ax.plot([], [], color=colors[j], ls=linestyles[j], lw=2, label=names[j])
        lines.append(line)
    line = ax.axvline(1e-4, color='k', ls='--', alpha=1, lw=1, label='Horizon')
    lines.append(line)
    line = ax.axvline(1e-4, color='C0', ls='--', alpha=1, lw=1, label='Sound horizon')
    lines.append(line)
        

    def init():

        ax.set_xlim(kmin, kmax)

        if scale_k == 0 :
            ax.set_ylabel(r'$P(k)$ [Mpc$^3$]', fontsize=12)
        elif scale_k == 1:
            ax.set_ylabel(r'$k P(k) [Mpc$^2$]$', fontsize=12)
        else:
            ax.set_ylabel(rf'$k^{{{scale_k}}} P(k)$', fontsize=12)
        ax.set_xlabel(r'$k$ [Mpc$^{-1}$]', fontsize=12)
        ax.set_xscale('log')
        #ax.set_yscale('log')
        return lines,

    def update(frame):

        ydatas = []
        for j in range(4):
            line = lines[j]
            ydata = pk[:, frame, j] * k**scale_k
            line.set_data(k, ydata)
            ydatas.append(ydata)

        line = lines[4]
        line.set_xdata(1/conformal_time[frame])
        line = lines[5]
        rs = sound_horizon[frame]
        if rs <= data['rdrag']:
            line.set_xdata(1/rs)
        else:
            line.set_alpha(np.exp(-0.5*(rs-data['rdrag'])**2/40**2))

        ymin = np.min(ydatas)
        ymax = np.max(ydatas)
        ax.set_ylim(ymin - 0.05*(ymax-ymin), ymax + 0.05*(ymax-ymin))
        ax.set_title(f'z = {redshifts[frame]:.1f}', fontsize=12)
        ax.legend(loc='upper left')
        ax.figure.canvas.draw()
        return lines,

    ani = FuncAnimation(fig, update, frames=i_range,
                        interval=interval,
                        init_func=init, blit=False)
    return ani

def save_anim(anim, fname, fps=60, **kwargs):
    writermp4 = animation.FFMpegWriter(fps=fps)
    anim.save(fname, writer=writermp4, **kwargs)


data = load('camb_outputs.pkl')

print('Making pk video....')
anim = pk_animation(data, scale_k=0, i_range = np.arange(500, 1000), interval=100)
save_anim(anim, 'pk_movie_v2.mp4', fps=30, dpi=200)
#plt.show()

print('Making xi video....')
anim_xi = xi_animation(data, i_range = np.arange(500, 1000), interval=100)
save_anim(anim_xi, 'xi_movie_v2.mp4', fps=30, dpi=200)
#plt.show()
