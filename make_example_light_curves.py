import astropy.units as u
import batman
import numpy as np
import pandas as pd

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
b.u = [0.0, 0.0]
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
c.u = [0.0, 0.0]
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
d.u = [0.0, 0.0]
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
e.u = [0.0, 0.0]
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
f.u = [0.0, 0.0]
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
g.u = [0.0, 0.0]
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
h.u = [0.0, 0.0]
h.limb_dark = 'quadratic'

# Randomize order of planets
planets = [d, b, h, g, f, c, e]

# 20-day time array
# 2000 points over 20 days = 4 hr/s
t = np.linspace(0, 20, 2000)

# Save 20-day light curves
for i, planet in enumerate(planets):
    # Model light curve
    model = batman.TransitModel(planet, t)
    flux = model.light_curve(planet)

    # Include same minimum value so all midi files end up on the same scale
    flux[0] = 1.-0.007266

    # Save model
    df = pd.DataFrame({'t':t, 'flux':flux})
    df.to_csv(f'planet_{i+1}_20_day.csv', float_format='%0.5f', index=None)

# Single-transit time array
# 200 points overs 2 days = 4 hr/s
t = np.linspace(0, 2, 200)

# Save single-transit light curves
for i, planet in enumerate(planets):
    # Model light curve
    model = batman.TransitModel(planet, t)
    flux = model.light_curve(planet)

    # Include same minimum value so all midi files end up on the same scale
    flux[0] = 1.-0.007266

    # Save model
    df = pd.DataFrame({'t':t, 'flux':flux})
    df.to_csv(f'planet_{i+1}.csv', float_format='%0.5f', index=None)
