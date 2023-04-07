import os
os.add_dll_directory("C:\\Program Files\\Lumerical\\V202\\api\\python")

def simulation(
        *,
        hide: bool = False,
):
    import importlib.util
    spec = importlib.util.spec_from_file_location('lumapi', 'C:\\Program Files\\Lumerical\\V202\\api\\python\\lumapi.py')
    lumapi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lumapi)
    function = lumapi.FDTD(hide=hide)
    return function

if __name__ == '__main__':
    fdtd = simulation()
