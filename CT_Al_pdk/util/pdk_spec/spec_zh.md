# 检查pdk所遵循的规则

## 简介
本文介绍检查用户pdk时所遵循的规则，帮助用户更好地规范pdk，并通过门禁系统检查，以此确保用户pdk能更好地适配到SDL。

## 使用说明
检查工具包含在CT_Al_pdk-x.x.x-py3-none-any.whl包中，用户通过pip安装CT_Al_pdk-x.x.x-py3-none-any.whl工具包后可参照以下示例，调用检查工具里check_pdk函数对用户pdk模块进行检查，检查完成后会显示检查结果及提示信息。

```
import user_pdk
from CT_Al_pdk.util.pdk_spec.check_all import check_pdk
check_pdk(pdk=user_pdk)
```

#### 检查提示说明
PASSED: 表示检查顺利通过，没有需要提示的信息
WARNING: 表示警告信息，有需要改进或引起用户注意的信息
FAILED: 表示导致检查失败的信息，需要用户修改后才能进行正常检查

## 规则说明
检查工具会对用户pdk的以下方面进行检查:

#### 1.必需的目录与文件
用户pdk下需要有components、technology两个目录，components目录下需要有all.py、func_all.py两个文件。如果未满足，检查工具会提示缺少的目录与文件。

#### 2.all.py包含所有自定义的器件，每个器件应该为其所有参数提供默认值，器件的所有参数定义满足规定
一般情况下，components目录下自定义的器件，都应该导出在components目录下的all.py中。如果未满足，检查工具会提示未导出的器件。另外，每个器件都应该为其所有参数提供默认值。如果未满足，检查工具会提示缺少默认值的器件。

检查所有器件的参数注解类型与参数默认类型是否匹配，如果不匹配，检查工具会提示不匹配的器件及其对应参数。
**器件的参数注解类型与参数默认类型匹配的规则**(from fnpcell import all as fp)：根据参数默认类型检查注解类型，参数默认类型应该为fp.Param或其子类的实例。fp.NameParam对应注解类型为str，fp.FloatParam、fp.DegreeParam、fp.NonNegFloatParam、fp.PositiveFloatParam对应注解类型为float，fp.IntParam、fp.PositiveIntParam、fp.NonNegIntParam对应注解类型为int，fp.BooleanParam对应注解类型为bool，fp.LayerParam对应注解类型为fp.ILayer，fp.AnchorParam对应注解类型为fp.Anchor，fp.PositionParam对应注解类型为fp.Point2D，fp.PortOptionsParam对应注解类型为fp.IPortOptions，fp.TransformParam对应注解类型为fp.Affine2D，fp.PointsParam对应注解类型为Sequence[fp.Point2D]，fp.WaveguideTypeParam对应注解类型为fpt.IWaveguideType的子类，fp.MappingParam对应注解类型为typing.Mapping。

检查所有器件的参数类型是否为SDL支持的参数类型，如果未满足，检查工具会提示不匹配的器件及其对应参数。
**SDL支持的参数类型**(from fnpcell import all as fp)：str、int、float、bool、typing.Dict、typing.FrozenSet、pathlib.Path、Sequence[Any]、Sequence[Tuple[float, float]]、Optional[str]、Optional[int]、Optional[float]、Callable、fp.StrPath、Optional[fp.StrPath]、Iterable[Union[fp.IRay, fp.Offset]]、fpt.Layer、fp.IPort、fp.ICellRef、fp.Affine2D、fp.Anchor、fp.ILayer、fpt.IWaveguideType的子类、fp.IBendWaveguideFactory、fp.ILinkingPolicy、fp.IDevice。

#### 3.func_all.py包含所有自定义的、可作为器件参数的可调用对象(此检查在扩展规则，默认规则中没有)
一般情况下，被用来作为components目录下自定义的器件参数的可调用对象，都应该导出在components目录下的func_all.py中。如果未满足，检查工具会提示缺少的可调用对象(因为可能无法准确区分用户自定义的、用作器件参数的可调用对象，所以可能会出现错误提示)。

#### 4.TECH类的完整性
pdk中需要包含定义了TECH类的pdk.technology.tech模块，TECH类应该有19个属性: GDSII、METRICS、PIN、PORT、LABEL、PROCESS、PURPOSE、LAYER、DEVICE、BAND、WG、METAL、VIAS、DISPLAY、AUTO_TRANSITION、AUTO_VIAS、LINKING_POLICY、FITTING_FUNCTION、LINK_BETWEEN。如果未满足，检查工具会提示缺少的属性。

#### 5.TECH类的BAND属性
检查pdk.technology.tech模块中TECH类的BAND属性，BAND属性类型为BAND类(继承自fnpcell.pdk.technology.all.BandEnum类)，BAND类有6个属性: O、E、S、C、L、U，这6个属性是fnpcell.pdk.technology.all.Band类的实例。如果其中未满足，检查工具会有对应提示。

#### 6.TECH类的DISPLAY属性
检查pdk.technology.tech模块中TECH类的DISPLAY属性，DISPLAY属性类型为DISPLAY类。DISPLAY类的LAYER_STYLE属性为fnpcell.pdk.technology.all.LayerStyleSet类的实例。如果其中未满足，检查工具会有对应提示。

#### 7.TECH类的PROCESS、PURPOSE、LAYER属性
检查pdk.technology.tech模块中TECH类的PROCESS、PURPOSE、LAYER属性，PROCESS属性类型为PROCESS类(继承自fnpcell.pdk.technology.all.ProcessEnum类)，PURPOSE属性类型为(继承自fnpcell.pdk.technology.all.PurposeEnum类)PURPOSE类，LAYER属性类型为LAYER类(继承自fnpcell.pdk.technology.all.LayerEnum类)。如果其中未满足，检查工具会有对应提示。

#### 8.TECH类的LINKER属性
检查pdk.technology.tech模块中TECH类的LINKER属性，LINKER属性类型为LINKER类，LINKER类中应该有自定义的类。如果其中未满足，检查工具会有对应提示。

#### 9.TECH类的AUTO_VIAS属性
检查pdk.technology.tech模块中TECH类的AUTO_VIAS属性，AUTO_VIAS属性类型为AUTO_VIAS类。AUTO_VIAS类的类方法DEFAULT的返回值为fnpcell.pdk.technology.all.AutoVias类的实例。检查pdk.technology.tech模块中TECH类的METAL属性，METAL属性类型为METAL类，METAL类中应该有metal_stack方法和from_single_layer方法。METAL类中至少定义一个类(该类继承自fnpcell.pdk.technology.all.ProfileMetalLineType类，并实现了profile方法)。如果其中未满足，检查工具会有对应提示。

检查所有两两不同类型METAL是否已经配置了vias，检查所有两两同种类型METAL是否已经配置了taper，如果存在没有配置的情况，检查工具会提示这些情况。

#### 10.TECH类的AUTO_TRANSITION属性
检查pdk.technology.tech模块中TECH类的AUTO_TRANSITION属性，AUTO_TRANSITION属性类型为AUTO_TRANSITION类。AUTO_TRANSITION类中的类方法DEFAULT的返回值为fnpcell.pdk.technology.all.AutoTransition类的实例。检查pdk.technology.tech模块中TECH类的WG属性，WG属性类型为WG类。WG类中至少定义一个类，WG类中定义的类中至少再定义一个类(该类继承自fnpcell.pdk.technology.all.ProfileWaveguideType类，并实现了profile方法)。如果其中未满足，检查工具会有对应提示。

检查所有两两不同类型WG是否已经配置了transition，检查所有两两同种类型WG是否已经配置了taper，如果存在没有配置的情况，检查工具会提示这些情况。

#### 11.TECH类的LINKING_POLICY属性
检查pdk.technology.tech模块中TECH类的LINKING_POLICY属性，LINKING_POLICY属性类型为LINKING_POLICY类(如果没继承其它类似CT_Al_pdk的pdk，LINKING_POLICY类的定义放在technology目录下的anto_link.py中)。LINKING_POLICY类中的类方法DEFAULT的返回值为fnpcell.pdk.technology.all.LinkingPolicy类的实例。检查pdk.technology.tech模块中TECH类的WG属性，WG属性类型为WG类。WG类中至少定义一个类，WG类中定义的类中至少再定义一个类(该类继承自fnpcell.pdk.technology.all.ProfileWaveguideType类，并实现了profile方法)。如果其中未满足，检查工具会有对应提示。

检查所有两两类型WG是否已经配置了link specs，如果存在没有配置的情况，检查工具会提示这些情况。

检查已配置了link specs的返回值(返回值为link_type和bend_factory)，link_type和bend_factory应该都可调用，link_type的调用返回值是fnpcell.pdk.technology.all.IWaveguideType类型，bend_factory的调用返回值是fnpcell.pdk.technology.all.IBendWaveguideFactory类型。如果其中未满足，检查工具会有对应提示。
