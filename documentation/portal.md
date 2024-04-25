# cqportal - portal

Code for creating portal models with print in place hinges. 

![](image/09.png)

---

## BaseCoffin

![](image/portal/01.png)

![](image/portal/01_a.png)

#### Parameters
* length = 150
* width = 5
* height = 150
* top_length = 90 # Length at the top of the shape
* base_length = 100 # Length at the base of the shape
* base_offset = 35 # offset distance from the base of the shape



### Example

``` python
import cadquery as cq
from cqportal.portal import BaseCoffin

bp = BaseCoffin()
bp.length = 150
bp.width = 5
bp.height = 150
bp.top_length = 90
bp.base_length = 100
bp.base_offset = 35 # offset distance from the base of the ramp
bp.make()
ex = bp.build()

show_object(ex)
```

#### Links
* [source](../src/cqportal/portal/BaseCoffin.py)
* [example](../example/base_coffin.py)
* [stl](../stl/base_coffin.stl)