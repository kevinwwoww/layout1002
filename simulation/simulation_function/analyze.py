import pandas as pd
import numpy as np
from pathlib import Path
import sys
import matplotlib.pyplot as plt

def analyze_result(
        *,
        points: int = 3,
        data_name: str,
        gdsfile_name: str,
):
    local = Path(sys.argv[0]).parent / "local" / f"{gdsfile_name}"
    for i in range(points):
        data = pd.read_csv(f"{local}\\{data_name}{i}.csv")
        data = np.array(data)
        plt.plot(data[:, 0], data[:, 1], label=f"{i}{data_name}")


    plt.xlabel("Wavelength")
    plt.ylabel("Transmission")
    plt.legend()
    plt.show()


