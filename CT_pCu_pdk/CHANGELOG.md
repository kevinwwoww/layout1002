Version 1.2.24 (2022-11-27)
============================
- remove `PCell` base class in CT_pCu_pdk
- some other updates

Version 1.2.23 (2022-11-24)
============================
- Components: `BendCircular90_Hard_Mask_WG_C_WIRE`, `BendCircular90_Hard_Mask_WG_C_EXPANDED`, `BendEuler90_Hard_Mask_WG_C_WIRE`, `BendEuler90_Hard_Mask_WG_C_EXPANDED`
- `waveguide_factory.py` is updated to use new (90 degrees) bends

Version 1.2.22 (2022-11-23)
============================
- basic support for simulation
- `TECH.RESOURCE.ROOT_FOLDER` as fallback resource search root

Version 1.2.21 (2022-11-10)
============================
- updated for fnpcell 1.4.16

Version 1.2.20 (2022-11-07)
============================
- `example_query_technology_value.py`

Version 1.2.19 (2022-10-29)
============================
- `generate_layers_and_display_from_csv.py` in `technology` folder

Version 1.2.18 (2022-10-25)
============================
- minor fixes

Version 1.2.17 (2022-10-22)
============================
- remove @fp.pcell_class decorators, band is now assigned during class declaration
- minor updates

Version 1.2.16rc4 (2022-9-2)
============================
- CompScan minor update
- minor bugfixes

Version 1.2.15 (2022-8-17)
============================
- CompScan minor update

Version 1.2.14 (2022-7-11)
============================
- vias for MT and M1

Version 1.2.13 (2022-7-11)
============================
- minior updates

Version 1.2.12 (2022-7-11)
============================
- Components: Mmi1x2, BondPad75, BondPad100

Version 1.2.11 (2022-7-6)
============================
- TW_mzm layer updates

Version 1.2.10 (2022-7-5)
============================
- Pins(electrical port) now have default orientations now

Version 1.2.9 (2022-6-24)
============================
- util.pdk_spec.check_all function to check if user's custom pdk supports SDL
- examples/example_mzi_perf.py as a performance test demo
- linker.py/TECH.LINKER, link_between/LINK_BETWEEN is deprecated and will be removed in a future version

Version 1.2.8.post3 (2022-4-13)
============================
- make `link_type` and `bend_factory` frozen parameters in LINK_BETWEEN

Version 1.2.8.post2 (2022-4-13)
============================
- remove band annotations from CT_pCu_pdk/technology/link_between.py

Version 1.2.8.post1 (2022-3-24)
============================
- example_array_mzi.py

Version 1.2.7 (2022-3-22)
============================
- AUTO_TRANISITON and AUTO_VIAS updates

Version 1.2.6.post1 (2022-3-10)
============================
- linking_policy updates

Version 1.2.6 (2022-3-7)
============================
- Custom LinkBetween in technology, see CT_pCu_pdk/technology/link_between.py

Version 1.2.5.post2 (2022-2-25)
============================
- components: spiral ports fix

Version 1.2.5.post1 (2022-2-24)
============================
- minor updates

Version 1.2.4 (2022-2-16)
============================
- example_sdl_circuit_01.py update

Version 1.2.3 (2022-2-7)
============================
- updates to align fnpcell's update
- examples: example_linked_elec_layers.py

Version 1.2.2.post3 (2022-1-14)
============================
- components: all parameters have default values now. So every component can be called without any argument.
- examples: example_waveguide_offset.py, example_phase_shifter.py
- add some `fp.export_pls` output
- minor updates

Version 1.2.1.post1 (2021-12-30)
============================
- Remove most `flatten` calls due to `fp.export_gds(auto_flatten=True)`
- port/pin names update


Version 1.2.0 (2021-12-24)
============================
- technology: `CircularBendFactory` and `EulerBendFactory` in bend_factory.py, components now use `IBendWaveguideFactory` instead of `AUTO_BEND`
- technology: `auto_link.py` defines `LINKING_POLICY` for auto link
- technology: `display.py` use `LayerStyle` and `LayerStyleSet` now. **Breaking Change**
- bends implements `IWaveguideLike` now
- examples: `example_elliptical_rings.py` demos rings with different outer initial/final angle and inner initial/final angle
- fonts: font_bombardier, font_college_tm, font_fragile_bombers, font_graduate, font_karisma, font_karnivore, font_pop_warner, font_staubach, font_traceroute, font_your_complex_brk
- components: pn_phase_shifter_sample.py demos `PeriodicSampler` and `with_patches` to build complex waveguide-like cell
- components: pn_phase_shifter_sample2.py demos `CurvePaint` to build complex waveguide-like cell
- routing: `CompScan` and `CompScanBuilder` added `fiber_coupler_factory`, and `Title` supports `font_size`
- font: `font_std_vented.py`
- bugfixes

Version 1.1.2 (2021-11-10)
============================
- `name` in `Process`, `Purpose` and `Layer` shows first in `__repr__` now
- `core_bias` and `cladding_bias` moved behind in `__repr__`, now `core_layout_width` and `cladding_layout_width` shows first
- `JsonCell` supports full layer and waveguide_type path now.
- minor updates and bugfixes

Version 1.1.1 (2021-11-10)
============================
- examples: example_merge.py to demo polygon and layer boolean operations.
- examples: example_link_between_flyline.py to demo flyline and how to turn `FlylineWarning` to an error
- util: `JsonCell` as a base class to define a pcell by import from json, see components/fixed_mh_te_1550/fixed_mh_te_1550.py and Fixed_MH_TE_1550.json
- util: `expect_same_content` in test_util.py provide a decorator for testing whether test function returns same result as before(in gds format)
- util/gds_util.py removed
- technology: `CoreCladdingWaveguideType` and `SlotWaveguideType` use `__post_init__` to eager calculate layout width now
- technology: `SlotWaveguideType` has a new `slot_bias` parameter

Version 1.1.0 (2021-10-29)
============================
- examples: example_pcell_dataclass_oversimplified.py to demo how to define a pcell class in an oversimplified way.

Version 1.0.0 (2021-10-27)
============================
- fonts: font_line_pixel_7 has different appearance for `0` and `O` now
- examples: example_pcell_dataclass_with_final.py demo `final` on class / field
- examples: example_demultiplexer2.py, example_ringMod_transceiver.py and example_linked_elec2.py are updated to demo `fp.Timing`() and `fp.statistics`()
