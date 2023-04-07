import os
fdtd_path = "C:\\Program Files\\Lumerical\\v202\\bin\\fdtd-solutions.exe"
def fdtd_run(
        *,
        lsf_path: str,
        hide=False,
        exit=False,
):
    if hide is True:
        HIDE = "-hide"
    else:
        HIDE = ""
    if exit is True:
        EXIT = "-exit"
    else:
        EXIT = ""
    os.system(f'"{fdtd_path}" -trust-script {HIDE} -run {lsf_path} -logall {EXIT}')




