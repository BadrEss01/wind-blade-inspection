# Wind Turbine Blade-Climbing Robot
### Undergraduate Research Assistant — From Research to Hardware Prototype

My undergraduate research focused on developing a robot that could attach to a wind turbine blade, climb along its surface, and change direction. The first challenge was to build the mobile platform that would eventually carry inspection or maintenance tools.

I designed the robot's 3D hardware from scratch in Fusion 360 and took the work through to a physical prototype. This involved researching climbing mechanisms, working through adhesion and mechanical design problems, producing 3D-printed parts, assembling the prototype, and programming its components.

The work was carried out at Jacobs University Bremen as part of a cooperative research project with Acquahmeyer Drone Tech and Prof. Francesco Maurelli.

**[Research report (PDF)](docs/research/wind-blade-inspection-report.pdf)** · [Hardware design](docs/robot-design.md) · [Report reading guide](docs/research/README.md)

## What I worked on

### Researching how the robot could climb

I studied existing wall-climbing robots and compared adhesion and locomotion approaches to establish a suitable design for a blade surface. The research covered suction cups, magnetic adhesion, and gripping mechanisms, alongside practical constraints such as weight, surface protection, energy consumption, and center of mass.

This informed the development of a platform using passive suction cups and belt-driven climbing modules. The central problem was maintaining attachment while allowing the robot to keep moving: each cup needed to meet the surface, be pressed into place, support the robot, and then release.

### Designing the hardware from scratch

I developed the mechanical design in Fusion 360, translating the climbing concept into individual components and an assembled robot model.

The design included:

- **Belt-and-pulley climbing modules** to carry the suction cups through their contact and release cycle.
- **A guide rail** to press the cups onto the blade, distribute load, and manage attachment and detachment.
- **A supporting tail** to help balance reaction forces and keep the front of the mechanism close to the surface.
- **A payload chassis and swivel connection** between the two modules to support the turning concept.

Turning was a particular design challenge. The report discusses differential movement of the two modules and a swivel connection to accommodate their relative motion while attached to the surface.

![Guide rail, payload chassis, and assembled climbing mechanism](assets/robot-design.jpg)

*CAD illustrations from our cooperative research report.*

### Working through the mechanics

The hardware development was supported by research into suction-cup materials, holding force, friction, belt-drive kinematics, motor torque, and weight distribution. The report documents these calculations and examines force equilibrium with and without an additional maintenance payload.

It also describes a proposed test rig for studying how the force used to press a suction cup onto a surface affects the force required to detach it.

### Building the prototype

I took the design into prototyping through 3D printing, component assembly, and programming. The report includes a photograph of the printed guide rail as well as drawings of the mechanism and assembled platform.

The assembly described in the report uses two 12 V DC motors with encoders, a dual H-bridge driver, an HX711-based force sensor, and PID mobility control with an ArduPilot board.

The main outcome of my work was the research, mechanical design, and prototype development toward a freely moving blade-climbing robot. Full operation on a wind turbine remains a validation goal.

## Wider team project

The climbing robot formed one part of a proposed system in which a UAV would carry it to a blade and deploy it onto the surface. The team's report also covers UAV positioning, obstacle avoidance, and deployment concepts.

My work centered on the climbing robot, from the initial research and 3D hardware design to the prototype.

## Research report

**[Wind Blade Inspection System with Unmanned Aerial Vehicle and Ground Robot](docs/research/wind-blade-inspection-report.pdf)**  
Project Report of Cooperative Work — Jacobs University Bremen

**Authors:** Badr Essefiany, Calin Constantin Clichici, Dongwook Lee, and Wail Bougida  
**Supervision:** Acquahmeyer Drone Tech and Prof. Francesco Maurelli

The sections most relevant to my work are:

| Section | Focus |
| --- | --- |
| 2.1 | Review of climbing robots and adhesion methods |
| 3.3 | Requirements, mechanical calculations, and climbing-robot design |
| 3.4 | Robot assembly and components |
| 4.2 | Force analysis and suction-cup experiment design |

The repository preserves the report and design illustrations. Original editable CAD, firmware, and raw test logs are not currently included.

## Later addition: visual defect screening

After the hardware research, I added an image-processing extension to explore a possible inspection function for the platform. It includes an OpenCV baseline and a trainable PyTorch segmentation pipeline.

This later addition processes still images and has been checked with synthetic examples. It has not been integrated with the climbing robot or validated on real turbine defects.

[Software setup, examples, and training instructions](docs/software-extension.md) · [Model card](docs/MODEL_CARD.md)

## Repository guide

| Location | Contents |
| --- | --- |
| `docs/research/` | Cooperative research report and reading guide |
| `docs/robot-design.md` | Climbing mechanism, design decisions, and prototype details |
| `assets/` | Robot design illustrations |
| `docs/software-extension.md` | Instructions for the later inspection software |
| `src/blade_inspection/` | Image-processing and segmentation code |
| `tests/` | Software tests |
| `examples/` | Synthetic inspection examples |

[My profile](https://github.com/BadrEss01) · [Authorship and sources](docs/provenance.md) · [Source and reuse notes](NOTICE.md)
