# cqportal
python Library for making portal terrain.

![](./documentation/image/01.png)<br /><br />

### Example Usage

``` python
import cadquery as cq
from cqportal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.render_base = False
bp_portal.render_ramps = True
bp_portal.ramp_push = 0
bp_portal.bp_ramp.width = 10
bp_portal.make()


result_open = bp_portal.build()
#show_object(result_open)
cq.exporters.export(result_open, 'stl/portal_open.stl')
```

## Dependencies
* [CadQuery](https://github.com/CadQuery/cadquery)
* [cqMore](https://github.com/JustinSDK/cqMore)
* [cadqueryhelper](https://github.com/medicationforall/cadqueryhelper)
* [cqterrain](https://github.com/medicationforall/cqterrain)


### Installation
To install cqdome directly from GitHub, run the following `pip` command:

	pip install git+https://github.com/medicationforall/cqportal

**OR**

### Local Installation
From the cloned cqdome directory run.

	pip install ./
