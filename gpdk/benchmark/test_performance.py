#
from io import BytesIO, StringIO
from typing import Any, Callable

from fnpcell import all as fp
from gpdk.examples.example_demultiplexer2 import Demultiplexer2
from gpdk.examples.example_ringmod_transceiver import Transceiver
from gpdk.examples.example_sdl_circuit_03 import Circuit03_passive_demux


def layout():

    # spc_file = Path(__file__).parent / "local" / Path(__file__).with_suffix(".spc").name
    gds_file = BytesIO()
    spc_file = StringIO()

    library = fp.Library()

    # =============================================================
    # fmt: off

    library += Circuit03_passive_demux()
    library += Demultiplexer2()
    library += Transceiver()

    # fmt: on
    # =============================================================
    fp.export_gds(library, file=gds_file)
    fp.export_spc(library, file=spc_file)
    #  fp.plot(library)


def test_performance(benchmark: Callable[..., Any]):
    benchmark(layout)


if __name__ == "__main__":
    for _ in range(10):
        layout()
