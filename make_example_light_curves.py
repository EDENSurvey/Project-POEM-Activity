import astropy.units as u
import batman
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Functions
def find_nearest_idx(array, value):
    array = np.asarray(array)
    return (np.abs(array-value)).argmin().astype('int')

# Planetary properties
# b
b = batman.TransitParams()
b.t0 = 1.
b.per = 1.51087081
b.rp = np.sqrt(0.007266)
b.a = 20.50
b.inc = 89.65
b.ecc = 0.
b.w = 0.
b.u = [0.04, 0.50]
b.limb_dark = 'quadratic'

# c
c = batman.TransitParams()
c.t0 = 1.
c.per = 2.4218233
c.rp = np.sqrt(0.00687)
c.a = 28.08
c.inc = 89.67
c.ecc = 0.
c.w = 0.
c.u = [0.04, 0.50]
c.limb_dark = 'quadratic'

# d
d = batman.TransitParams()
d.t0 = 1.
d.per = 4.049610
d.rp = np.sqrt(0.00367)
d.a = 39.55
d.inc = 89.75
d.ecc = 0.
d.w = 0.
d.u = [0.04, 0.50]
d.limb_dark = 'quadratic'

# e
e = batman.TransitParams()
e.t0 = 1.
e.per = 6.099615
e.rp = np.sqrt(0.00519)
e.a = 51.97
e.inc = 89.86
e.ecc = 0.
e.w = 0.
e.u = [0.04, 0.50]
e.limb_dark = 'quadratic'

# f
f = batman.TransitParams()
f.t0 = 1.
f.per = 9.206690
f.rp = np.sqrt(0.00673)
f.a = 68.4
f.inc = 89.680
f.ecc = 0.
f.w = 0.
f.u = [0.04, 0.50]
f.limb_dark = 'quadratic'

# g
g = batman.TransitParams()
g.t0 = 1.
g.per = 12.35294
g.rp = np.sqrt(0.00421)
g.a = 83.2
g.inc = 89.710
g.ecc = 0.
g.w = 0.
g.u = [0.04, 0.50]
g.limb_dark = 'quadratic'

# h
h = batman.TransitParams()
h.t0 = 1.
h.per = 18.767
h.rp = np.sqrt(0.00346)
h.a = 109.
h.inc = 89.76
h.ecc = 0.
h.w = 0.
h.u = [0.04, 0.50]
h.limb_dark = 'quadratic'

# Randomize order of planets
planets = [d, b, h, g, f, c, e]

# Single-transit time array
# 40 points over 4 hours @ 600 bpm = 1 hr/s
t = np.linspace(1.-2./24., 1.+2./24., 40)
t_hr = (t-t.min())*24. # hours

# Higher time-resolution for the plot
t_plot = np.linspace(1.-2./24., 1.+2./24., 400)
t_plot_hr = (t_plot-t_plot.min())*24. # hours

# Save single-transit light curves
for i, planet in enumerate(planets):
    n = i+1
    color = f'C{i}'

    # Model light curve
    model = batman.TransitModel(planet, t)
    flux = model.light_curve(planet)*100. # percent

    model_plot = batman.TransitModel(planet, t_plot)
    flux_plot = model_plot.light_curve(planet)*100. # percent

    fig, ax = plt.subplots()
    ax.set_title(f'Transit Light Curve of Planet {n}')
    ax.set_xlabel('Time (hrs)')
    ax.set_ylabel('Star Brightness (%)')
    ax.set_ylim(99.05, 100.2)
    ax.plot(t_plot_hr, flux_plot, color=color)
    plt.savefig(f'pdfs/planet_{n}_single_transit_light_curve.pdf', bbox_to_inches='tight')

    # Include same minimum value so all midi files end up on the same scale
    flux[0] = 99.

    # Save model
    df = pd.DataFrame({'t':t_hr, 'flux':flux})
    df.to_csv(f'csvs/planet_{i+1}.csv', float_format='%0.5f', index=None)

# 20-day time array
# 333 points over 20 days @ 1000 bpm = 1 day/s
# The maximum bpm is set by the sonification software (Aria Maestosa)
# But it doesn't give great time-resolution for a 20-s light curve
# So we have to jerry-rig a light curve in this case
t = np.linspace(0, 20, 333)

# Save 20-day light curves
for i, planet in enumerate(planets):
    n = i+1
    color = f'C{i}'

    # Jerry-rig a light curve
    flux = np.ones(t.shape)
    t_now = 1.
    while t_now <= t.max():
        idx = find_nearest_idx(t, t_now)
        flux[idx] = 1.-planet.rp**2
        t_now += planet.per
    flux *= 100. # percent
    # model = batman.TransitModel(planet, t)
    # flux = model.light_curve(planet)*100. # percent

    fig, ax = plt.subplots()
    ax.set_title(f'20-day Light Curve of Planet {n}')
    ax.set_xlabel('Time (days)')
    ax.set_ylabel('Star Brightness (%)')
    ax.set_ylim(99.05, 100.2)
    ax.plot(t, flux, color=color)
    plt.savefig(f'pdfs/planet_{n}_20-day_light_curve.pdf', bbox_to_inches='tight')

    # Include same minimum value so all midi files end up on the same scale
    flux[0] = 99.

    # Save model
    df = pd.DataFrame({'t':t, 'flux':flux})
    df.to_csv(f'csvs/planet_{n}_20-day.csv', float_format='%0.5f', index=None)
