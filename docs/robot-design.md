# Blade-Climbing Robot — From Research to Prototype

## My role and objective

As an undergraduate research assistant, I worked on developing a prototype that could adhere to a wind turbine blade and move along its surface, including a mechanism for changing direction. My work ran from researching suitable climbing approaches to designing the hardware from scratch in Fusion 360, producing printed parts, assembling the prototype, and programming its components.

The immediate research objective was the climbing platform. Inspection and maintenance tools were future applications for that platform. The [coauthored report](research/wind-blade-inspection-report.pdf) explicitly places specific ground-robot inspection functions outside the original scope.

## From literature review to design

The study compared existing climbing robots and adhesion approaches, including suction, magnetic attachment, and gripping. The ground-robot requirements covered weight, center of mass, non-destructive surface contact, terrain adaptation, energy consumption, and reliability.

The resulting concept used passive suction cups carried by a belt-and-pulley system. Its design addressed both holding force and the sequence of pressing, attaching, and releasing each cup during movement.

## Mechanism

| Subsystem | Design | Report section |
| --- | --- | --- |
| Adhesion | Passive suction cups; attachment depends on pressing force, seal, and surface conditions | 3.3.2, printed pp. 12–14 |
| Locomotion | Belt-and-pulley drive carrying cups through attachment and release zones | 3.3.2, pp. 13–15 |
| Guide rail | Distributes load and controls cup pressing, transition, and release; a tail helps balance reaction forces | pp. 15–17 |
| Turning | Two climbing modules with differential movement and a swivel connecting them to the payload | p. 17 |
| Actuation | Two 12 V, 146 RPM brushed DC motors with encoders and a dual H-bridge driver | 3.4, p. 18 |
| Force sensing | HX711-based force-sensor module | 3.4, p. 18 |
| Control | PID mobility control using an ArduPilot board, as described in the report | 3.4, p. 18 |

The report's 15 kg limit is a design requirement. It is not a measured robot mass or demonstrated payload.

## Calculations and experiment design

The report discusses suction holding force, friction, belt-drive kinematics, motor torque, and static force equilibrium. It also considers the extra load introduced by a possible maintenance arm.

A proposed test rig uses a motor-driven plate and force sensor to investigate the relationship between suction-cup pressing force and detachment force. Varying the pressing force would help identify suitable attachment conditions. Numerical adhesion results and raw experiment logs are not available in this repository.

## From CAD to the physical prototype

I translated the mechanism into 3D part and assembly designs in Fusion 360, then worked on 3D printing, assembly, and programming. This was the practical continuation of the adhesion and locomotion research.

The guide rail was especially important: its geometry had to bring each cup into contact smoothly, apply pressing force, distribute load across attached cups, and allow release at the rear. A tail helped manage reaction forces, while the chassis and swivel connected the two climbing modules for the turning concept.

The report includes Fusion 360 illustrations and a photograph of a 3D-printed guide rail. These document the design and prototype development; reliable vertical climbing, turning, and outdoor blade operation still require experimental validation.

![Guide rail and climbing-platform design](../assets/robot-design.jpg)

*Illustrations from the report by Badr Essefiany, Calin Constantin Clichici, Dongwook Lee, and Wail Bougida.*

## Development status and next engineering steps

The repository contains the report, design overview, and a later image-inspection extension. Original CAD files, wiring, firmware, and raw test logs are not included.

Further development of the platform would focus on measuring adhesion under different loading and surface conditions, checking the attachment and release cycle, and validating climbing and turning. The proposed pressing-force test rig provides one starting point for that work.

The [later visual-inspection software](software-extension.md) is an additional function to explore once the physical platform and camera interface are ready.

[Research report and reading guide](research/README.md) · [Back to project](../README.md)
