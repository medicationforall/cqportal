# CQPortal changelog

## Main wip
## 1.1.1
* Portal wired up hinges render flag
* Added Floor
* Modified Container to use floor
* Fixed a bug where the frame base_length cuts were being calculated at a different ratio then the top_length.

## 1.1.0
* Added Container class
* Added ContainerFrame
* Renamed container example to rotation_demo.py and added new container example file.

## 1.0.1
* RampGreebled fixed a bug with the fillet operation on the slots. Added error generation if the segment padding was too high.
* Added Portal and PortalHinge parameters to allow making better door alignments.

## 1.0.0
* Added FrameWindow which makes a cutout for the window piece
* Added PortalHinge which takes a ramp as a parent and aligns both the hinge and the ramp to a given rotation.
* Refactored Portal to use PortalHinge which support any rotation for the doors and correctly aligns
* Added container example
* Made the repo public
* Updated the README.md

## 0.1.2
* Refactored Ramp to have less convoluted parent if statements
* Added ramp_frame.py example
* Added RampGreebled
  * Added Portal Greebled Ramp Example
* Integrated hinges into the Portal

## 0.1.1
* As predicted fixed as issue with ramp inheriting width from frame in unexpected and exciting ways.

## 0.1.0
* Initial release