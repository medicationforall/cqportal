# cqportal
Python library for making portal and container terrain.

![](./documentation/image/01.png)<br /><br />

### Example Portal Code

``` python
import cadquery as cq
from cqportal.portal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.render_base = False
bp_portal.render_ramps = True
bp_portal.ramp_push = 0
bp_portal.bp_ramp.width = 10

bp_portal.bp_hinge.rotate_deg = 0

bp_portal.make()


result_open = bp_portal.build()
#show_object(result_open)
cq.exporters.export(result_open, 'portal_open.stl')
```

## Container
![](./documentation/image/34.png)<br /><br />

### Example Container Code

``` python
import cadquery as cq
from cqportal.container import Container

bp_container = Container()
bp_container.bp_hinge.rotate_deg = -70

bp_container.make()

result = bp_container.build()
#show_object(result)
cq.exporters.export(result, 'container.stl')
```

---

## Project Documention
* [Portal](documentation/portal.md) 

## Changes
* [Changelog](./changes.md)

## Dependencies
* [CadQuery 2.x](https://github.com/CadQuery/cadquery)
* [cqterrain](https://github.com/medicationforall/cqterrain)

---


### Installation
To install cqportal directly from GitHub, run the following `pip` command:

	pip install git+https://github.com/medicationforall/cqportal

**OR**

### Local Installation
From the cloned cqportal directory run.

	pip install ./


---

## Running Example Scripts

* All of the examples live in the [example directory](./example)
* The examples generated output stl's are written to the [stl directory](./stl).

[example_runner.py](example_runner.py) runs all examples.

``` bash
C:\Users\<user>\home\3d\cqportal>python example_runner.py
```

**OR**

### Running individual examples
* From the root of the project run one of the example scripts:
  
``` bash
C:\Users\<user>\home\3d\cqportal>python ./example/rampGreebled.py
```
