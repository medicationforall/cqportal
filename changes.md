# CQPortal changelog

## Main wip

## 4.2.0
* Updgraded cqterrain version 2.4.0
* Added FrameBlock
* Added FrameWindowBlock
* Added EnergyInsert
* Added portal CoffinTextured
* Added portal_cutaway example
* Added RampGreebledTwo
* Wrote documentation
* Added missing examples.
* removed unused parameter ramp_push
* Integrated EnergyInsert into portal
* Fix container code which I broke when I renamed protected method _make_frame to public make_frame.
* Fixed Portal bp_iris top length calculation.
* Rewrote truchet circle again, finally got unions to work correctly which fixes the generated stl file sizes.
* Updated README.md

## 4.1.0
* Fixed example syntax in shieldwall documentation
* Fixed syntax shieldwall straight example
* Added hexkey generation to hexmesh
* Conditionally build components is shieldwall set depending on if the count is zero
* Updgraded cqterrain version 2.1.0

## 4.0.0
* Updgraded cqterrain version 1.0.3
* Added example_runner.py
  * Moved examples around into sub packages 
* Added license blocks
* Updated README.md
* Modified PortalHinge tab_height and tab_z_translate
* Anotated shieldwall package
  * Added BaseGreeble,BaseMagnet, BaseMesh, BaseShape, BaseWall
  * These setup the interface for what attributes other components rely on when replacing these classes.
* Annotated Container package
* Annotated Portal package
* Added portal_hinge.py example
* Refactored ramp.py example
* Added container_ramp example
* Added container floor examples
* Added shieldwall arch_shape example
* Added shieldwall base_cut exmple
* Added shieldwall cap_greeble example
* Added shieldwall hex_straight example

## 3.4.0
* Added base_coffin.py example and stl
* Added frame_window example and stl
* Updated Frame example
* Documentation
  * BaseCoffin
  * Frame
  * FrameWindow
* Added shieldwall CurveBasic
  * Added example.

## 3.3.0
* Added shieldwall BaseCut and integrated into Straight. 
* Added assembly build for shieldwall components.
  * corner_connector
* Added shieldwall GothicMesh
* Updated Archset to use gothic mesh
* Updated Arch set example

## 3.2.0
* Added assembly build for shieldwall components.
  * Straight
  * EndCap
* Fix ShieldShape bug where the base height would break in a way that made the shape not actually symetrical.
* Shieldwall set added support for setting base_height to all parts.
* Shieldwall added Magnets
* Integrated Magnets into:
  * StraightBasic
  * Straight
  * EndCaps
  * CornerConnector
* Magnet spacing matches the jersey barrier set.

## 3.1.0
* Added shieldwall Set
* Added shieldwall HexSet
* Added shieldwall ArchSet
* Added shieldwall ArchShape
* Updated shieldwall STL example paths

## 3.0.1
* Clean up python imports for shieldwall files.

## 3.0.0
* Separated portal and container into their own sub-modules
* Updated example import paths
* Updated README.md
* Added HexMesh
* Added mesh, hexmesh, straight_hex examples
* Added Initial EndCap
* Added cap greeble
* Added HexStraight
* Added CornerConnector

## 2.1.0
* synced container tile example.
* Added initial shieldwall 
  * ShieldShape.
  * StraightBasic
  * Straight
  * Mesh 
* Added stubs for new Shield wall shapes

## 2.0.0
* Refactored Ramp to be an orchestrator
* Added BaseCoffin
* Added ContainerDoor
* Added ContainerRamp wich uses container door and RampGreebled
* Added Container Greeble Hack rough example container_greeble_hack.py

## 1.2.0
* Added FloorTile
* Added ContainerLadder

## 1.1.1
* Portal wired up hinges render flag
* Added Floor
* Modified Container to use floor
* Fixed a bug where the frame base_length cuts were being calculated at a different ratio then the top_length.
* Added Floor to container.

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