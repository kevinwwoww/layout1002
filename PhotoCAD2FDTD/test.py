from collections import OrderedDict
from api_load import simulation


fdtd = simulation(name="FDTD")
fdtd.addfdtd(dimension="2D", x=0.0e-9, y=0.0e-9, x_span=3.0e-6, y_span=1.0e-6)
fdtd.addgaussian(name='source', x=0., y=-0.4e-6, injection_axis="y", waist_radius_w0=0.2e-6, wavelength_start=0.5e-6,
                 wavelength_stop=0.6e-6)
fdtd.addring(x=0.0e-9, y=0.0e-9, z=0.0e-9, inner_radius=0.1e-6, outer_radius=0.2e-6, index=2.0)
fdtd.addmesh(dx=10.0e-9, dy=10.0e-9, x=0., y=0., x_span=0.4e-6, y_span=0.4e-6)
fdtd.addtime(name="time", x=0.0e-9, y=0.0e-9)
fdtd.addprofile(name="profile", x=0., x_span=3.0e-6, y=0.)

# Dict ordering is not guaranteed, so if there properties dependant on other properties an ordered dict is necessary
# In this case 'override global monitor settings' must be true before 'frequency points' can be set
props = OrderedDict([("name", "power"),
                     ("override global monitor settings", True),
                     ("x", 0.), ("y", 0.4e-6), ("monitor type", "linear x"),
                     ("frequency points", 10.0)])

fdtd.addpower(properties=props)
fdtd.save(f"local\\fdtd_test.fsp")
fdtd.run()

# Return raw E field data
Ex = fdtd.getdata("profile", "Ex")
f = fdtd.getdata("profile", "f")
x = fdtd.getdata("profile", "x")
y = fdtd.getdata("profile", "y")

print('Frequency field profile data Ex is type', type(Ex), ' with shape', str(Ex.shape))
print('Frequency field profile data f is type', type(f), 'with shape', str(f.shape))
print('Frequency field profile data x is type', type(x), 'with shape', str(x.shape))
print('Frequency field profile data y is type', type(y), 'with shape', str(y.shape))


