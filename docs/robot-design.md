# Ground-robot design and evidence

## System context

The cooperative report proposes a UAV transporting a mobile robot to a wind blade, a deployment arm placing it on the surface, and a climbing platform supporting future contact inspection. This repository focuses on the ground robot and a new image-only screening module. It does not reproduce the UAV code or deployment arm.

## Mechanism

| Subsystem | Design described in the report | Evidence location |
| --- | --- | --- |
| Adhesion | Passive suction cups; attachment depends on pressing force, seal and surface conditions | Section 3.3.2, printed pp. 12-14 |
| Locomotion | Belt/pulley drive carrying suction cups through contact and release zones | Section 3.3.2, printed pp. 13-15 |
| Guide rail | Load distribution, cup pressing, transition and detachment; tail balances reaction forces | Printed pp. 15-17 |
| Turning | Two straight-moving modules, differential motion and a swivel between modules/payload | Printed p. 17 |
| Actuation | Two 12 V brushed DC motors, 146 RPM, encoders; dual H-bridge driver | Section 3.4, printed p. 18 |
| Sensing | Joy-IT SEN-HX711-20 / HX711 force measurement, nominal 20 kg module | Section 3.4, printed p. 18 |
| Control | PID mobility control using an ArduPilot control board is described | Section 3.4, printed p. 18 |

The stated 15 kg weight limit is a **design requirement**, not a measured robot mass or demonstrated payload. Component descriptions come from the report and are not a complete purchase list.

## Prototype and experiment status

The abstract states that a Fusion 360 design and passive-suction model were studied and built. The report includes CAD illustrations and a photograph labelled as a 3D-printed guide rail (Figure 23). Badr's account describes participating in design, printing, assembly and programming. The report does not allocate all contributions by author.

Section 4.2 discusses force equilibrium and proposes a test rig relating cup pressing force to detachment force. No recovered time series or numerical adhesion results support a rated operating load. Do not infer tested vertical climbing, reliable turning or outdoor blade operation from the CAD figures.

## Reproduction boundary

Available: report-based mechanism description, selected report illustrations, software extension and synthetic tests.

Unavailable: original Fusion 360 files/STLs, manufacturing dimensions, wiring diagrams, firmware, control gains, bill of materials, raw test logs and current prototype access. Recreating those from scratch would be a new engineering effort. No substitute CAD or firmware is labelled as historical work.

## Proposed future interface

An independently validated camera could provide still images to the inspection CLI. The current outputs are pixel-space candidate regions for human review. They are not position estimates on a blade and must not be used directly as motor commands. Camera calibration, image-to-surface registration, lighting, adhesion monitoring, emergency stop and fall protection require separate work before physical trials.
