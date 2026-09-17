## Multiscale Modelling of Tunnel Ventilation Flows and Fires

<!-- image -->

Logo

## FRANCESCO COLELLA

Thesis submitted for the degree of Doctor of Philosophy Politecnico di Torino, Dipartimento di Energetica. May 2010

© Francesco Colella, 2010

## DECLARATION

This thesis and the research described and reported herein have been completed solely by  Francesco  Colella  under  the  supervision  of  Professor  Romano  Borchiellini,  Dr Vittorio Verda, Dr Guillermo Rein and Professor Jose L. Torero. Where other sources are quoted, full references are given.

Francesco Colella

## TABLE OF CONTENTS

| 1 INTRODUCTION 1            | 1 INTRODUCTION 1                   | 1 INTRODUCTION 1                                              | 1 INTRODUCTION 1   |
|-----------------------------|------------------------------------|---------------------------------------------------------------|--------------------|
| 1.1.                        | Introduction                       | Introduction                                                  | 1                  |
| 1.2.                        | Fundamentals of tunnel fires       | Fundamentals of tunnel fires                                  | 2                  |
| 1.3.                        | The role of the ventilation system | The role of the ventilation system                            | 7                  |
| 1.3.1.                      | 1.3.1.                             | Natural ventilation systems                                   | 8                  |
| 1.3.2.                      | 1.3.2.                             | Mechanical ventilation systems                                | 9                  |
| 1.3.3.                      | 1.3.3.                             | Hybrid ventilation systems                                    | 13                 |
| 1.4.                        | 1.4.                               | Interaction between fire and ventilation system               | 14                 |
| 1.4.1.                      | 1.4.1.                             | Ventilation velocity and back-layering                        | 14                 |
| 1.5.                        | 1.5.                               | Analysis of tunnel ventilation systems and fires              | 22                 |
| 1.5.1.                      | 1.5.1.                             | Small and large scale experiments                             | 23                 |
| 1.5.2.                      | 1.5.2.                             | Numerical modelling                                           | 23                 |
| 1.6.                        | 1.6.                               | Test cases                                                    | 26                 |
| 1.6.1.                      | 1.6.1.                             | Case A: Frejus Tunnel, Bardonecchia (It)                      | 26                 |
| 1.6.2.                      | 1.6.2.                             | Case B: Norfolk road Tunnels, Sydney (Au)                     | 26                 |
| 1.6.3.                      | 1.6.3.                             | Case C: Wu-Bakar small scale tunnel                           | 27                 |
| 1.6.4.                      | 1.6.4.                             | Case D: Dartford Tunnels, London (UK)                         | 27                 |
| 1.6.5.                      | 1.6.5.                             | Case E: Test case tunnel                                      | 27                 |
| 2 ONE-DIMENSIONAL MODELLING | 2 ONE-DIMENSIONAL MODELLING        | 2 ONE-DIMENSIONAL MODELLING                                   | 29                 |
| 2.1.                        | 2.1.                               | Introduction                                                  | 29                 |
| 2.2.                        | 2.2.                               | Literature overview                                           | 30                 |
| 2.3.                        | 2.3.                               | Typical mathematical formulation for 1D models representation | 32                 |
| 2.3.1.                      | 2.3.1.                             | Topological                                                   | 32                 |
| 2.3.2.                      | 2.3.2.                             | Fluid dynamics model                                          | 33                 |
| 2.3.3.                      | 2.3.3.                             | Thermal model                                                 | 35                 |
| 2.3.4.                      | 2.3.4.                             | Steady state problem                                          | 36                 |
| 2.3.5. 2.3.6.               | 2.3.5. 2.3.6.                      | Time dependent problem Solving algorithm                      | 40 42              |

| 4.3.                                                         | Formulation of the multiscale problem                        | Formulation of the multiscale problem                        |   112 |
|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|-------|
| 4.4.                                                         | Coupling technique                                           | Coupling technique                                           |   114 |
| 4.4.1.                                                       | 4.4.1.                                                       | Direct coupling                                              |   114 |
| 4.4.2.                                                       | 4.4.2.                                                       | Indirect coupling                                            |   119 |
| 4.5.                                                         | Concluding remarks                                           | Concluding remarks                                           |   120 |
| 5                                                            | MULTISCALE MODELLING OF TUNNEL VENTILATION FLOWS             | MULTISCALE MODELLING OF TUNNEL VENTILATION FLOWS             |   121 |
| 5.1.                                                         | Introduction                                                 | Introduction                                                 |   121 |
| 5.2.                                                         | A case study: the Dartford tunnels                           | A case study: the Dartford tunnels                           |   122 |
| 5.3.                                                         | Overview on the experimental setups                          | Overview on the experimental setups                          |   125 |
| 5.4.                                                         | Characterization of the jet fan discharge cone               | Characterization of the jet fan discharge cone               |   126 |
| 5.4.1.                                                       | 5.4.1.                                                       | Assessment of the mesh requirements                          |   127 |
| 5.4.2.                                                       | 5.4.2.                                                       | Effect of the 1D-CFD interface location                      |   130 |
| 5.4.3.                                                       | 5.4.3.                                                       | Comparison to experimental data                              |   132 |
| 5.5. Characterization of the ventilation system              | 5.5. Characterization of the ventilation system              | 5.5. Characterization of the ventilation system              |   135 |
| 5.5.1.                                                       | 5.5.1.                                                       | Calculation of the jet fan characteristic curves             |   135 |
| 5.5.2.                                                       | 5.5.2.                                                       | Comparison to experimental data                              |   138 |
| 5.5.3.                                                       | 5.5.3.                                                       | Analysis of all the ventilation strategies                   |   139 |
| 5.5.4.                                                       | 5.5.4.                                                       | Assessment of the redundancy in the Dartford Tunnels         |   140 |
| 5.6.                                                         | Concluding remarks                                           | Concluding remarks                                           |   142 |
| 6                                                            | MULTISCALE MODELLING OF TUNNEL FIRES                         | MULTISCALE MODELLING OF TUNNEL FIRES                         |   145 |
| 6.1.                                                         | Introduction                                                 | Introduction                                                 |   145 |
| 6.2.                                                         | A case study: a modern tunnel 1.2 km in length               | A case study: a modern tunnel 1.2 km in length               |   146 |
| 6.3.                                                         | Characterization of the fire near field                      | Characterization of the fire near field                      |   147 |
| 6.3.1.                                                       | 6.3.1.                                                       | Assessment of the mesh requirements                          |   148 |
| 6.3.2.                                                       | 6.3.2.                                                       | Effect of the 1D-CFD interface location                      |   151 |
| 6.3.3.                                                       | 6.3.3.                                                       | Comparison to full CFD solutions                             |   155 |
| 6.4. Characterization of the ventilation system performance  | 6.4. Characterization of the ventilation system performance  | 6.4. Characterization of the ventilation system performance  |   161 |
| 6.4.1. Calculation of the fan and fire characteristic curves | 6.4.1. Calculation of the fan and fire characteristic curves | 6.4.1. Calculation of the fan and fire characteristic curves |   161 |

| 6.4.2.                                          | 6.4.2.                                          | Comparison to full CFD solutions 162            |
|-------------------------------------------------|-------------------------------------------------|-------------------------------------------------|
| 6.4.3. A note of the fire throttling effect     | 6.4.3. A note of the fire throttling effect     | 165                                             |
| 6.5.                                            | Concluding remarks                              | 166                                             |
| 7 MULTISCALE MODELLING OF TIME-DEPENDENT TUNNEL | 7 MULTISCALE MODELLING OF TIME-DEPENDENT TUNNEL | 7 MULTISCALE MODELLING OF TIME-DEPENDENT TUNNEL |
| VENTILATION FLOWS AND FIRES                     | VENTILATION FLOWS AND FIRES                     | 169                                             |
| 7.1.                                            | Introduction                                    | 169                                             |
| 7.2.                                            | A case study: a modern tunnel 1.2 km in length  | 170                                             |
| 7.3.                                            | Multiscale model results                        | 175                                             |
| 7.4.                                            | Concluding remarks                              | 182                                             |
| 8 CONCLUSIONS AND FUTURE WORKS                  | 8 CONCLUSIONS AND FUTURE WORKS                  | 185                                             |

## LIST OF FIGURES

| Figure 1: Typical traffic flow and induced ventilation in the 1.8 tunnel in Taipei City. Traffic density and                                                                                         | Figure 1: Typical traffic flow and induced ventilation in the 1.8 tunnel in Taipei City. Traffic density and                                                                                         |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| induced ventilation as presented in [23]                                                                                                                                                             | 8                                                                                                                                                                                                    |
| Figure 2: A schematic of a Saccardo longitudinal ventilation system [26]                                                                                                                             | 10                                                                                                                                                                                                   |
| Figure 3: A schematic of a jet fan longitudinal ventilation system [26]                                                                                                                              | 10                                                                                                                                                                                                   |
| Figure 4: A schematic of a fully transverse ventilation system                                                                                                                                       | 12                                                                                                                                                                                                   |
| Figure 5: A schematic of a supply semi-transverse ventilation system                                                                                                                                 | 13                                                                                                                                                                                                   |
| Figure 6: A schematic of a exhaust semi-transverse ventilation system                                                                                                                                | 13                                                                                                                                                                                                   |
| Figure 7: Photograph of a small scale tunnel fire during the occurrence of back-layering. The fire size in                                                                                           | Figure 7: Photograph of a small scale tunnel fire during the occurrence of back-layering. The fire size in                                                                                           |
| 15 kW. The tunnel has an arched cross section (width 274mm, height 244 mm). Adapted from                                                                                                             | [3].                                                                                                                                                                                                 |
|                                                                                                                                                                                                      | 15                                                                                                                                                                                                   |
| Figure 8: Variation of dimensionless critical velocity against dimensionless heat release rate. (O) measurements of critical velocity; (continuous line) equations (8) and (9): (dashed line) Thomas | Figure 8: Variation of dimensionless critical velocity against dimensionless heat release rate. (O) measurements of critical velocity; (continuous line) equations (8) and (9): (dashed line) Thomas |
| correlation (4). (from [29]).                                                                                                                                                                        | 17                                                                                                                                                                                                   |
| Figure 9: Two step approximation of fire growth rate phase for the Second Benelux tunnel fire Tests and                                                                                              | Figure 9: Two step approximation of fire growth rate phase for the Second Benelux tunnel fire Tests and                                                                                              |
| Runehamar Fire Test Program (from [18])                                                                                                                                                              | 22                                                                                                                                                                                                   |
| Figure 10: A schematic of a hybrid computational grid for multiscale calculation of tunnel ventilation                                                                                               | Figure 10: A schematic of a hybrid computational grid for multiscale calculation of tunnel ventilation                                                                                               |
| flows and fires                                                                                                                                                                                      | 25                                                                                                                                                                                                   |
| Figure 11: Example of the network representation of a tunnel showing branches between nodes                                                                                                          | 33                                                                                                                                                                                                   |
| Figure 12: Schematic of the control volumes adopted for the numerical solution                                                                                                                       | 37                                                                                                                                                                                                   |
| Figure 13: Meteorological pressure difference measured between the portals of Mont Blanc Tunnel                                                                                                      | [73]                                                                                                                                                                                                 |
|                                                                                                                                                                                                      | 45                                                                                                                                                                                                   |
| Figure 14: Frejus tunnel: top) cross section; down) Schematic of the ventilation system layout                                                                                                       | 48                                                                                                                                                                                                   |

| Figure 15: Schematic of the network used for the 1D calculation corresponding to the tunnel region                                                              | Figure 15: Schematic of the network used for the 1D calculation corresponding to the tunnel region                                                              |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| between section T 2 and T 3 of Figure 14.                                                                                                                       | 49                                                                                                                                                              |
| Figure 16: Velocity distribution computed with the developed 1D model and comparison to experimental                                                            | Figure 16: Velocity distribution computed with the developed 1D model and comparison to experimental                                                            |
| data recorded in the Frejus tunnel. Longitudinal velocity as function of the tunnel length                                                                      | 50                                                                                                                                                              |
| Figure 17: Velocity distribution computed with the developed 1D model and comparison to experimental                                                            | Figure 17: Velocity distribution computed with the developed 1D model and comparison to experimental                                                            |
| data recorded in the Frejus tunnel. Longitudinal velocity as function of the tunnel length at different times                                                   | 4 51                                                                                                                                                            |
| Figure 18: Schematic of the simplified fire representations used in this work.                                                                                  | 80                                                                                                                                                              |
| Figure 19: Schematic of mesh used the fan representations used in this work.                                                                                    | 83                                                                                                                                                              |
| Figure 20: Schematic of the CFD segregated solution algorithm.                                                                                                  | 84                                                                                                                                                              |
| Figure 21: Schematic of the Norfolk road tunnels cross section.                                                                                                 | 85                                                                                                                                                              |
| Figure 22: Schematic of the jet fan longitudinal position in the Westbound Norfolk road tunnel; jet fans                                                        | Figure 22: Schematic of the jet fan longitudinal position in the Westbound Norfolk road tunnel; jet fans                                                        |
| are numbered from 13 to 24.                                                                                                                                     | 86                                                                                                                                                              |
| Figure 23: Examples of the different meshes used for half of the tunnel cross section and number of cells                                                       | Figure 23: Examples of the different meshes used for half of the tunnel cross section and number of cells                                                       |
| per unit length of tunnel.                                                                                                                                      | 88                                                                                                                                                              |
| Figure 24: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the                                                            | Figure 24: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the                                                            |
| reference section 1. Velocity values are expressed in m/s.                                                                                                      | 88                                                                                                                                                              |
| Figure 25: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the                                                            | Figure 25: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the                                                            |
| reference section 2. Velocity values are expressed in m/s.                                                                                                      | 89                                                                                                                                                              |
| Figure 26: Computed velocity profile in the tunnel for scenarios 1.1, 1.2, 1.3, 2.1, 2.2, 4.2, 5.1, 5.2, 6.1                                                    | Figure 26: Computed velocity profile in the tunnel for scenarios 1.1, 1.2, 1.3, 2.1, 2.2, 4.2, 5.1, 5.2, 6.1                                                    |
| from Table 8. The plotted velocity fields are relative to plane 1 of Figure 21. Velocity values expressed in m/s.                                               | are 91                                                                                                                                                          |
| Figure 27: Comparison between predicted velocity and experimental measurements provided by the Sickflow 200 Units located at the centre of each tunnel tube. 92 | Figure 27: Comparison between predicted velocity and experimental measurements provided by the Sickflow 200 Units located at the centre of each tunnel tube. 92 |

- Figure 28: 3D visualisation of the computed velocity fields for ventilation scenario 3.4 involving all the 6 jet fan pairs. Velocity values are expressed in m/s. (not to scale). 93
- Figure 29: Schematic of the experimental rig accordingly to Wu and Bakar [3]. Section B has been used in this study. 94
- Figure 30: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel. 95
- Figure 31: Computed temperature and velocity fields for mesh #1 to #4 at reference sections 1 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 96
- Figure 32: Computed temperature and velocity fields for mesh #1 to #4 at reference sections 2 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 97
- Figure 33: Computed temperature and velocity fields in the vicinity of the fire source for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 98
- Figure 34: Computed temperature and velocity fields at reference sections 1 and 2 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 99
- Figure 35: Computed temperature and velocity fields in the vicinity of the fire source for a 3 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 100
- Figure 36: Computed temperature and velocity fields at reference sections 1 and 2 for a 3 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively. 101
- Figure 37: Effect o fire Froude number on the predicted critical for a 3 kW and a 30 kW fire 102
- Figure 38: up) Example computed velocity field for a pair of operating jet fans (jet fan discharge velocity ~34 m/s; down) Example computed temperature field for a 30MW fire subject to supercritical

| ventilation conditions. The velocity and temperature values are expressed in m/s and K,                                                                                                       | ventilation conditions. The velocity and temperature values are expressed in m/s and K,                                                                                                       |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| respectively.                                                                                                                                                                                 | 107                                                                                                                                                                                           |
| Figure 39: Example of domain decomposition with and without overlapping [65].                                                                                                                 | 108                                                                                                                                                                                           |
| Figure 40: Example of domain decomposition for solution of Navier-Stokes problem using a Dirichlet-                                                                                           | Figure 40: Example of domain decomposition for solution of Navier-Stokes problem using a Dirichlet-                                                                                           |
| Neumann iterative method.                                                                                                                                                                     | 110                                                                                                                                                                                           |
| Figure 41: Example of domain decomposition for solution of Navier-Stokes problem using a Schwartz                                                                                             | Figure 41: Example of domain decomposition for solution of Navier-Stokes problem using a Schwartz                                                                                             |
| (Dirichlet-Dirichlet) iterative method.                                                                                                                                                       | 111                                                                                                                                                                                           |
| Figure 42: Example of a domain decomposition in 1D and 3D sub-domains.                                                                                                                        | 113                                                                                                                                                                                           |
| Figure 43: Visualization of a three stage coupling procedure.                                                                                                                                 | 117                                                                                                                                                                                           |
| Figure 44: Visualization of the interaction procedure between 1D and 3D grids at the left CFD domain                                                                                          | Figure 44: Visualization of the interaction procedure between 1D and 3D grids at the left CFD domain                                                                                          |
| boundary (1D-CFD interfaces highlighted in green)                                                                                                                                             | 117                                                                                                                                                                                           |
| Figure 45: left) Evolution of total pressure and mass flow rate at a 1D-3D interface during a multiscale                                                                                      | Figure 45: left) Evolution of total pressure and mass flow rate at a 1D-3D interface during a multiscale                                                                                      |
| calculation. The maximum deviation allowed was 10 -6 . right). Deviation of the mass flow rate                                                                                                | and                                                                                                                                                                                           |
| total pressure at a 1D-CFD interface during a multiscale calculation                                                                                                                          | 118                                                                                                                                                                                           |
| Figure 46: Diagram of the East and West Dartford Tunnels showing the relative positions of jet fans and                                                                                       | Figure 46: Diagram of the East and West Dartford Tunnels showing the relative positions of jet fans and                                                                                       |
| extract shafts. (Drawn approximately to scale but with vertical distances five times larger)                                                                                                  | 122                                                                                                                                                                                           |
| Figure 47: East Dartford Tunnel; Picture taken approximately 1100 m from the Kent portal facing south                                                                                         | Figure 47: East Dartford Tunnel; Picture taken approximately 1100 m from the Kent portal facing south                                                                                         |
| (refer to Figure 46).                                                                                                                                                                         | 123                                                                                                                                                                                           |
| Figure 48: West Dartford Tunnel; Picture taken approximately 500 m from the Kent portal facing south                                                                                          | Figure 48: West Dartford Tunnel; Picture taken approximately 500 m from the Kent portal facing south                                                                                          |
| (refer to Figure 46).                                                                                                                                                                         | 123                                                                                                                                                                                           |
| Figure 49: Layout and general dimensions of the tunnel cross sections (west tunnel to the left; East tunnel                                                                                   | Figure 49: Layout and general dimensions of the tunnel cross sections (west tunnel to the left; East tunnel                                                                                   |
| to the right) including the points 1-9 where the air velocities where measured (dimensions are                                                                                                | to the right) including the points 1-9 where the air velocities where measured (dimensions are                                                                                                |
| expressed in mm).                                                                                                                                                                             | 125                                                                                                                                                                                           |
| Figure 50: Schematic of multiscale coupling between mono-dimensional and CFD models for the multiscale calculation of the jet fan discharge cone (1D-CFD interfaces highlighted in green) 127 | Figure 50: Schematic of multiscale coupling between mono-dimensional and CFD models for the multiscale calculation of the jet fan discharge cone (1D-CFD interfaces highlighted in green) 127 |

- Figure 51: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel. 128
- Figure 52: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 1. Velocity values are expressed in m/s. 129
- Figure 53: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 2. Velocity values are expressed in m/s. 130
- Figure 54: Convergence of the predicted mass flow rate as a function of the location of the interface  131
- Figure 55: Comparison of horizontal velocities between predictions (lines) and experimental measurements (symbols) in the West Tunnel. The two profiles and the numbers refer to locations in the tunnel section described in Figure 49. 132
- Figure 56: Comparison of horizontal velocities between predictions (lines) and experimental measurements (symbols) in the East Tunnel. The two profiles and the numbers refer to locations in the tunnel section described in Figure 4.b. 134
- Figure 57: Typical flow pattern produced by a series of seven jet fan pairs operating in the West Tunnel (not to scale). Velocity isocontours from 2 m/s to 20 m/s in steps of 2 m/s; Velocity expressed in m/s. 136
- Figure 58: Computational mesh for the CFD module around the jet fans in the West (right) and East (left) tunnels. (Note: the West tunnel's jet fans are installed in niches on the ceiling, in the East tunnel they are not.) 137
- Figure 59: CFD calculated jet fan thrust vs. tunnel average velocity for the Dartford tunnels. 137
- Figure 60: Comparison between experimental data and model predictions. 139
- Figure 61: Results for the West Tunnel, using the strategy for Zone C (Kent supply on, Essex extract on), varying the number of active jet fan pairs. (Note: Zone C extends from approximately 700 m into the tunnel to 1370 m). 141
- Figure 62: Results for the East Tunnel, using the strategy for Zone C (Kent supply on, Essex extract on), varying the number of active jet fans. (Note: Zone C extends from approximately 700 m into the tunnel to about 1300 m) 142

- Figure 63: Layout of the tunnel used as case study showing the relative positions of the fire, jet fans and portals (Not to scale). 146
- Figure 64: Schematic of the multiscale model of a 1.2 km tunnel including portals, jet fans, and the CFD domain of the fire region. Contours of the temperature field show the fire plume. (Not to scale). The 1D-CFD interfaces have been highlighted in green 148
- Figure 65: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel. 149
- Figure 66: Comparison of the longitudinal velocity (left) and temperature (right) contours for meshes #1 to #4 in the tunnel at Reference Section 1 for a 30 MW fire. The velocity and temperature values are expressed in m/s and K respectively. 150
- Figure 67: Comparison of the longitudinal velocity (left) and temperature (right) contours for meshes #1 to #4 in the tunnel Reference Section 2 for a 30 MW fire. Velocity and temperature values are expressed in m/s and K respectively 150
- Figure 68: Effect of the CFD domain length, LCFD, on the average longitudinal velocity and temperature at the outlet boundary of the CFD module. Units are in m/s and K respectively. Note that the shortest module length is 20 m. 152
- Figure 69: Effect of the CFD domain length LCFD on the error for the average longitudinal velocity and average temperature. Results for  top) Reference Section 1; bottom) Reference Section 2. Error calculated using Eq. (76). 153
- Figure 70: Effect of the CFD domain length LCFD on the horizontal velocity and temperature fields at Reference Section 1 for a 30MW fire. The velocity and temperature values are expressed in m/s and K respectively 154
- Figure 71: Effect of the CFD domain length LCFD on the horizontal velocity and temperature fields at Reference Section 2 for a 30MW fire. Velocity and temperature values are expressed in m/s and K respectively 154
- Figure 72: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 1. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. 157

- Figure 73: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 2. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. 158
- Figure 74: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 3. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. 159
- Figure 75: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 4. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. 160
- Figure 76: Characteristic curves of a tunnel region 50 m long where an activated jet fan pair (and a single jet fan) is located: Pressure drop between inlet and outlet vs. Mass flow rate across the inlet. (CFD calculated). 161
- Figure 77: Characteristic curves of the tunnel region 400 m long where the fire is located: Pressure drop between inlet and outlet vs. Mass flow rate across the inlet (CFD calculated) 162
- Figure 78: Longitudinal velocity iso-contours, calculated using full CFD for 10 operating jet fans pairs. (Not to scale) 163
- Figure 79: Predictions of average velocity for cold flow scenarios. Comparison and error between multiscale and full CFD results. 164
- Figure 80: Layout of the tunnel used as case study showing the relative positions of the fire, jet fans and portals (Not to scale). 171
- Figure 81: Fire growth curve, delay phase and detection times considered in the time dependent multiscale simulations. The fire growth curve is based on the work of Carvel (2008) [18]. 172
- Figure 82: Schematic of the multiscale model of a 1.2 km tunnel including portals, jet fans, and the CFD domain of the fire region. Contours of the temperature field show the fire plume. (Not to scale). The 1D-CFD interfaces have been highlighted in green 173

- Figure 83: Time dependent evolution of the mass flow rate through the tunnel for scenario 1, 2 and 3 (see Table 17). The time to detection is 2 min. Supercritical conditions (vair&gt; 3m/s) are reached after 244 s, 190 s and 160 s for scenario 2 and 3 respectively 175
- Figure 84: Multiscale results in the vicinity of the fire computed 2 min after the fire outbreak for scenario 1, 2 and  3 (see Table 17). The ventilation system is about to be started. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. (not to scale) 176
- Figure 85: Temperature profiles computed by the multiscale model 3 min after the fire outbreak for scenario 1, 2 and 3 (see Table 17). The ventilation system is operative since 1 min. Temperature values are expressed in K. (not to scale) 176
- Figure 86: Longitudinal velocity profiles computed by the multiscale model 3 min after the fire outbreak for scenario 1, 2 and 3 (see Table 17). The ventilation system is operative since 1 min. Velocity values are expressed in m/s. (not to scale) 177
- Figure 87: Temperature and velocity profiles 5 min (left column) and 10 min (right column) after the fire outbreak for scenario 1, 2 and 3 (see Table 17). Temperature and velocity values are expressed in K. and m/s, respectively (not to scale) 178
- Figure 88: Dependence between number of operating jet fan pairs, TD, and time required to remove backlayering computed from the moment of the ventilation system activation. 181
- Figure 89: Dependence between number of operating jet fan pairs, TD, and time required to remove backlayering computed from the fire outbreak 182

## LIST OF TABLES

| Table 1: Extension of tunnels in Europe                                                                                                                                                                  | 1                                                                                                                                                                                                        |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Table 2: Approximate energy contents of typical tunnel fire loads [11,12]                                                                                                                                | 4                                                                                                                                                                                                        |
| Table 3: Approximate max HRR for typical tunnel fires                                                                                                                                                    | 4                                                                                                                                                                                                        |
| Table 4: Approximate smoke production from tunnel fires [12]                                                                                                                                             | 6                                                                                                                                                                                                        |
| Table 5: Maximum peak temperature recorded on full scale experimental tunnel fires [1,2,14,19,20].                                                                                                       | 6                                                                                                                                                                                                        |
| Table 6: Summary of the observed correlation between ventilation rate, delay phase length and fire growth rate (from [18]).                                                                              | 22                                                                                                                                                                                                       |
| Table 7: Summary of the published CFD studies related to tunnel fires discussed in the literature review.                                                                                                | Table 7: Summary of the published CFD studies related to tunnel fires discussed in the literature review.                                                                                                |
|                                                                                                                                                                                                          | 66                                                                                                                                                                                                       |
| Table 8: Summary of ventilation scenarios explored during the experimental campaign conducted in the                                                                                                     | Table 8: Summary of ventilation scenarios explored during the experimental campaign conducted in the                                                                                                     |
| Westbound Norfolk road tunnel. Scenarios having the measurement unit located in the an operating jet fan have been highlighted in grey.                                                                  | vicinity of 86                                                                                                                                                                                           |
| Table 9: Grid Independence Study for a scenario involving an operating jet fan pair in the Norfolk tunnels                                                                                               | Table 9: Grid Independence Study for a scenario involving an operating jet fan pair in the Norfolk tunnels                                                                                               |
|                                                                                                                                                                                                          | 87                                                                                                                                                                                                       |
| Table 10: Grid Independence Study for a scenario involving a 30 kW fire scenario                                                                                                                         | 96                                                                                                                                                                                                       |
| Table 11: Grid Independence Study for a scenario involving an operating jet fan pair in the West tunnel                                                                                                  | Table 11: Grid Independence Study for a scenario involving an operating jet fan pair in the West tunnel                                                                                                  |
|                                                                                                                                                                                                          | 128                                                                                                                                                                                                      |
| Table 12: Summary of ventilation flows in the tunnels resulting from various ventilation strategies. The operating ventilation devices in each scenario are indicated by 'ON'. The predicted ventilation | Table 12: Summary of ventilation flows in the tunnels resulting from various ventilation strategies. The operating ventilation devices in each scenario are indicated by 'ON'. The predicted ventilation |
| velocities in the incident zones are highlighted in bold                                                                                                                                                 | 140                                                                                                                                                                                                      |
| Table 13: Summary of ventilation and fire scenarios analysed with the multiscale technique                                                                                                               | 147                                                                                                                                                                                                      |
| Table 14: Grid independence study of the full CFD domain for a 30 MW fire and 3 operating jet fan pairs.                                                                                                 | 149                                                                                                                                                                                                      |
| Table 15: Comparison between Full CFD and Multiscale predictions for the 7 scenarios investigated. The multiscale results are obtained with direct coupling. The table presents only bulk flow data. 155 | Table 15: Comparison between Full CFD and Multiscale predictions for the 7 scenarios investigated. The multiscale results are obtained with direct coupling. The table presents only bulk flow data. 155 |

| Table 16: Comparison between Full CFD, Multiscale, and 1D model predictions for the 7 scenarios investigated. The multiscale results are obtained with indirect coupling. The table presents only   |   Table 16: Comparison between Full CFD, Multiscale, and 1D model predictions for the 7 scenarios investigated. The multiscale results are obtained with indirect coupling. The table presents only |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| bulk flow data.                                                                                                                                                                                     |                                                                                                                                                                                                 164 |
| Table 17: Summary of the ventilation scenarios considered in the time dependent analysis                                                                                                            |                                                                                                                                                                                                 173 |
| Table 18: Summary of the ventilation scenarios considered and numerical findings                                                                                                                    |                                                                                                                                                                                                 180 |

180

## ACKNOLEDGEMENTS

I  would  like  to  thank  my  supervisors  Prof.  Vittorio  Verda  and  Prof.  Romano Borchiellini for their constant support, their precious advices and feedbacks. They are the original masterminds behind this work. A special 'Thank You' to Vittorio for the patience he had dealing with me during the last four years and above all and for being, besides an enthusiastic advisor, a good friend.

I  would  also  like  to  thanks  my  supervisors  Dr.  Guillermo  Rein  and  Prof.  Jose  Luis Torero for welcoming me at University of Edinburgh half the way through this project and for hosting me for more than 2 years. I thank them for tens of helpful discussions, for  their  invaluable  feedback  and  for  their  contagious  optimism.  I  have  been  very fortunate to learn about fire from them.

I  owe  my  gratitude  to  Dr.  Ricky  Carvel  for  his  expert  comments  and  for  providing insightful discussions. His help has been invaluable for the completion of this work.

I  would like to thank Le Crossing Company Ltd., Jacob (UK) Ltd. and the Highways Agency  for  allowing  access  to  the  Dartford  tunnels,  assistance  with  the  on-site measurements and permitting the completion of this work and the publication of several papers. Special thanks to Stuart Lowe of Jacobs (UK) Ltd. for all his help with the onsite measurements.

I am grateful to Transurban Ltd (AU) for supplying useful experimental measurements adding significant quality to this thesis. Special thanks to Cameron Torpy of Transurban Ltd (AU) for being a kind and expert interlocutor.

I  would  like  to  show  my  gratitude  to  all  my  colleagues  in  Torino,  Adriano,  Flavio, Chiara e Giorgia for many fruitful discussions but also for their friendship. The have been always around whenever I needed a break. A special thanks goes to Adriano for our  innumerable  conversations  on  CFD  and  music  related  topics  and  to  Giorgia  for being always so helpful while I was away.

I  am  also  thankful  to  all  the  people  I  have  meet  in  the  last  years  at  University  of Edinburgh. Thanks to Nicolas and Cristián for all t he interesting talks, the laughs and the culinary arguments we had since the beginning. They are among the best flatmates I have ever had. Thanks to Hubert and Wolfram for being always around for a talk, a joke or  a  serious  discussion.  I  am  thankful  to  Pedro  for  our  endless  conversations  and  for sharing  his  experiences.  I  cannot  forget  Thomas  and  his  family  for  several  enjoyable dinners and for introducing me to the pleasures of the 'Deutsche Sprache'. Thanks to Albert for all the interesting research related conversations and for our long discussions on  the  Italo-Corsican  culture.  Thanks  to  all  my  office  mates  Paolo,  Adam,  Cecilia, Rory, Angus, Joanne, Kate and Susan for never denying a smile or a chat.

I am thankful to all my old friends and flatmates in Torino, Sergio, Michele, Antonio, Pierluigi  and  Michele  for  making,  whenever  I  am  there,  my  life  pleasant  and  never boring. Thanks to them for all those late dinners, pool and poker games, sport activities and for always keeping the doors of their flats open for me to stay.

I also have to thank my father, my mother and my sister for encouraging and supporting me to follow my own choices and for insisting to invest in my education. I am grateful to  them for all the sacrifices and efforts they did and they still do for  me. To them I dedicate this thesis.

Finally,  I  would  like  to  express  my  deepest  thanks  to  Daniela.  Thanks  not  only  for coming into my life, but for the special person she is, for her enthusiastic support to my choices.  Without  her  care  and encouragements,  this  work  would  not  have  been successfully completed.

## THANK YOU ALL

## ABSTRACT

Tunnels represent a key part of world transportation system with a role both in people and  freight  transport.  Past  events  show  that  fire  poses  a  severe  threat  to  safety  in tunnels. Indeed in the past decades over four hundred people worldwide have died as a result  of  fires  in  road,  rail  and  metro  tunnels.  In  Europe  alone,  fires  in  tunnels  have brought  vital  parts  of  the  road  network  to  a  standstill  and  have  cost  the  European economy billions of euros. Disasters like Mont Blanc tunnel (Italy, 1999) and the more recent  three  Channel  Tunnel  fires  (2008,  2006  and  1996)  show  that  tunnel  fire emergencies  must  be  managed  by  a  global  safety  system  and  strategies  capable  of integrating detection, ventilation, evacuation and fire fighting response, keeping as low as  possible  damage  to  occupants,  rescue  teams  and  structures.  Within  this  safety strategy, the ventilation system  plays  a  crucial  role because  it  takes  charge  of maintaining tenable conditions to allow safe evacuation and rescue procedures as well as  fire  fighting.  The  response  of  the  ventilation  system  during  a  fire  is  a  complex problem. The resulting air flow within a tunnel is dependent on the combination of the fire-induced flows and the active ventilation devices (jet fans, axial fans), tunnel layout, atmospheric conditions at the portals and the presence of vehicles.

The  calculation  of  tunnel  ventilation  flows  and  fires  is  more  economical  and  time efficient when done using numerical models but physical accuracy is an issue. Different modelling approaches can be used depending on the accuracy required and the resources available. If details of the flow field are needed, 2D or 3D computational fluid dynamics (CFD) tools can be used providing details of the flow behaviour around walls, flames, ventilation devices and obstructions. The computational cost of CFD is very high, even for medium size tunnels (few hundreds meters). If the analysis requires only bulk flow velocities,  1D  models  can  be  adopted.  Their  low  computational  cost  favours  large number  of  parametric  studies  involving  broad  range  ventilation  scenarios,  portal conditions and fire sizes/locations.

Another  class  of  methods,  called  multiscale  methods,  adopts  different  levels  of complexity  in  the  numerical  representation  of  the  system.  Regions  of  interest  are described using more detailed models (i.e. CFD models), while the rest of the system can be represented using a simpler approach (i.e. 1D models). Multiscale methods are characterized  by  low  computational  complexity  compared  to  full  CFD  models  but provide the same accuracy. The much lower computational cost is of great engineering value,  especially  for  parametric  and  sensitivity  studies  required  in  the  design  or assessment of ventilation and fire safety systems. Multiscale techniques are used here for the first time to model tunnel ventilation flows and fires.

This thesis provides in Chapter 1 a general introduction on the fundamentals of tunnel ventilation flows and fires. Chapter 2 contains a description of 1D models, and a case study  on  the  Frejus  tunnel  (IT)  involving  some  comparisons  to  experimental  data. Chapter 3 discusses CFD techniques with an extensive review of the literature in the last 30 years. The chapter provides also two model validations for cold ventilation flows in the  Norfolk  Tunnels  (AU)  and  fire  induced  flows  in  a  small  scale  tunnel.  Chapter  4 introduces  multiscale  methods  and  addresses  the  typical  1D-CFD  coupling  strategies. Chapter  5  applies  multiscale  modelling  for  cold  flow  steady-state  scenarios  in  the Dartford Tunnels (UK) where a further validation against experimental data has been introduced. Chapter 6 present the calculations from coupling fire and ventilation flows in  realistic  modern  tunnel  layout  and  investigates  the  accuracy  of  the  multiscale predictions  as  compared  to  full  CFD.  Chapter  7  represents  application  of  multiscale computing  techniques  to  transient  problems  involving  the  dynamic  response  of  the ventilation system.

The multiscale model has been demonstrated to be a valid technique for the simulation of complex  tunnel ventilation systems both in steady-state and time-dependent problems.  It  is  as  accurate  as  full  CFD  models  and  it  can  be  successfully  adopted  to conduct parametric and sensitivity studies in long tunnels, to design ventilation systems, to  assess  system  redundancy  and  the  performance  under  different  hazards  conditions. Time-dependent simulations allow determining the evolution of hazardous zones in the tunnel domain or to determine the correct timing for the activation of fixed fire fighting systems. Another significant advantage is that it allows for full coupling of the fire and the whole tunnel domain including the ventilation devices. This allows for an accurate assessment  of  the  fire  throttling  effect  that  is  shown  here  to  be  significant  and  for  a prediction of the minimum number of jet fans needed to cope with a certain fire size. Furthermore, it is firmly believed that the multiscale methodology represents the only feasible  tool  to  conduct  accurate  simulations  in  tunnels  longer  than  few  kilometres, when the limitation of the computational cost becomes too restrictive.

## 1.1. Introduction

Tunnels represent a key part of world transportation system playing a fundamental role both  in  people  and  freight  transportation  system,  especially  in  developed  countries. Around  the  world  most  major  cities  and  metropolitan  areas  have  metro  systems accounting for hundreds of kilometres of underground tunnels and networked system. Similarly,  in  some  mountainous regions, tunnels represent a vital part of the network transportation  system.  At  present,  the  overall  length  for  operational  transportation tunnels throughout the whole of Europe is larger than 15000 km  [1]. An overview on the extension of the underground transportation systems in Europe is given in Table 1 including road and rail tunnels.

Table 1: Extension of tunnels in Europe

|          |   Italy |   Austria |   Switzerland |   Germany |   France |   UK |   Norway |   Spain |
|----------|---------|-----------|---------------|-----------|----------|------|----------|---------|
| Railways |    1200 |       105 |           360 |       380 |      650 |  220 |      260 |     750 |
| Roads    |    1160 |       210 |           140 |        70 |      180 |   30 |      370 |     100 |
| Total    |    2360 |       315 |           500 |       450 |      830 |  250 |      630 |     850 |

The issue of tunnel fire safety has become more important in the last decades due to the social  impact  of  disaster  like  King's  Cross  underground  station  in  1987  (31  deaths),

<!-- image -->

Icon

## Introduction

1

Baku  Underground  fire  in  1995  (289  deaths),  Gotthard  Tunnel  in  2001  (11  deaths), Tauern  Tunnel  in  1999  (12  deaths),  Mont  Blanc  Tunnel  in  1999  (39  deaths),  Frejus Tunnel in 2005 (2 deaths) and Channel tunnel fires in 1996, 2006 and 2008.

According to French statistics [2] it appears that there are only one or two car fires (per km of tunnel length) every hundred million cars passing through the tunnel. Same order of magnitude can be expected for fire involving heavy good vehicles (HGVs). In this case, 8 fires per hundred millions of HGVs are expected, but only one will be enough serious  to  produce  damage  to  the  structure  [3].  On  the  basis  of  such  values,  one  can expect that the chance of an accidental tunnel fire can be negligible. However given the high number of tunnels in Europe, their high traffic density (several millions of vehicles per year) and their length (sometimes up to several tens kilometres), the probability of accidental fires become significant. For instance statistics indicates that, on average, one fire incident occurred practically every month within the Elb tunnel in Germany, from 1990  to  1999.  And  this  is  not  an  isolate  case.  Indeed  in  the  past  decade  over  four hundred people worldwide have died as a result of fires in road, rail and metro tunnels. In Europe alone, fires in tunnels have destroyed over a hundred vehicles, brought vital parts of the road network to a standstill - in some instances for years - and have cost the European economy billions of euros [4]. This serious problem has the potential to get worse  it  the  future  due  to  the  drastic  increase  in  the  volume  of  dangerous  goods transported and in the number of new operative tunnels.

## 1.2. Fundamentals of tunnel fires

This section is  intended  to  provide  a  general  overview  of  the  fundamentals  of  tunnel fires. Fire behaviour in tunnel as well as in compartment is different from the behaviour in open space (free burning conditions). In particular, due to the confined enclosure, the heat feedback from the walls and hot gases enhances the fire burning rate. Furthermore, for very intense enclosure fires the oxygen supply can be reduced inducing a change in the  combustion regime from fuel-controlled (also over-ventilated fires) to ventilationcontrolled  (under-ventilated  fires).  In  the  last  case  the  combustion  process  generate  a large amount of incomplete combustion products and toxic effluents.

Ingason  identifies  three  main  differences  between  compartment  fires  and  tunnel  fires [5].  The  first  is  related  to  the  maximum  heat  release  rate  (HRR)  that  can  be  attained. Typically,  in  small  compartment  fires  the  maximum  HRR  is  controlled  by  the 'ventilation factor' that can be calculated as o o h A [m 5/2 ] where Ao and h0 are the area and the height of the opening, respectively. In the case of the tunnel fires, given the size of  the  tunnel  cross  section  and  the  air  flow  eventually  delivered  by  the  ventilation system, the oxygen supply to the fire zone is at least one order of magnitude larger than typical compartment fires. Therefore, in tunnel fire scenarios, the limiting factor to the maximum  HRR  is  not  represented  by  the  ventilation  conditions  but  by  the  fuel available. Under-ventilated conditions can be only achieved in severe tunnel fires with multiple vehicles involved in the burning process.

The second difference is  related  to  the  likelihood  of  attaining  flashover.  Flashover  is defined  as  a  transition  from  a  localized  fire  to  the  general  conflagration  within  the compartment  when  all  the  fuel  surfaces  are  burning  [6],  and  limited  by  ventilation flows.  External  flames  typically  appear  at  the  vents  of  the  compartment.  Indeed, flashover is unlikely to take place in a tunnel due to the large convective losses from the fire to the surroundings and lack of full containment of hot fire effluents. Nonetheless, it must be stressed that the ventilation system plays an important role in the development of a tunnel fire, especially during the under-ventilated regime [7].

The third difference is related to the smoke stratification. Early stage compartment fires are generally characterized by a buoyant layer of hot gases under the ceiling. The same smoke  pattern  can  be  observed  in  the  early  stages  of  tunnel  fires  but  in  absence  of longitudinal  ventilation.  In  this  condition,  the  smoke  front  will  spread  away  from  the fire  zone,  cooling  down  and partially mixing with the air layer underneath. However, after a certain distance and time the smoke layer will descend and touch the road deck. The distance from the fire at which such phenomenon takes place is mainly dependent on the tunnel geometry and fire characteristics. The activation of the ventilation system generally  produces  important  change  in  the  structure  of  the  smoke  layer.  Moderate ventilation  velocities  (&lt;  3  m/s)  generate  a  certain  degree  of  back-layering  in  the  fire upstream region while the stratification is lost in the fire downstream region. A more detailed discussion on the interaction between ventilation system and smoke movements will be presented in the next sections.

Tunnel  fires  usually  involve  material  from  vehicles  including  seats,  tyres,  plastic material from the finishing, fuel from the tanks and eventually the loading. The latter can  be  very  variable.    Evaluations  of  the  energy  content  for  typical  load  involved  in tunnel fires are presented in Table 2.

Table 2: Approximate energy contents of typical tunnel fire loads [8,9]

| Type of vehicle             | Approx. energy content [MJ]   |
|-----------------------------|-------------------------------|
| Private car                 | 3000-7000                     |
| Public bus                  | 41000                         |
| TIR fire load               | 65000                         |
| HGV                         | 88000 - 247000                |
| Tanker with 50 m3 of petrol | 1500000                       |

Besides the global energy content other characteristics are required to assess the hazard of  a  given  fire  scenario.  Typically  the  design  of  the  ventilation  system  and  structures requires an evaluation of the fire heat release rate (HRR), the smoke production and the temperature distribution and the maximum temperature at the tunnel walls.

Indeed  the  fire  HRR  represents  the  single  most  important  variable  to  evaluate  fire hazard [10] and its design value has  a  great influence on the tunnel construction and operating costs. Several guidelines have been formulated on the basis of large scale tests [8,11-13]. An overview is given in Table 3.

Table 3: Approximate max HRR for typical tunnel fires

| Type of vehicle            | Maximum HRR [MW]   |
|----------------------------|--------------------|
| 1 passenger car            | 2.5 - 5            |
| 2-3 passenger cars         | 8                  |
| 1 van                      | 15                 |
| 1 bus                      | 20                 |
| 1 lorry with burning goods | 20-30              |
| 1 HGV                      | 70-200             |
| Tanker                     | 200-300            |

The time evolution of the fire HRR (i.e. growth rate) is another important parameter to be evaluated when designing a ventilation system or an evacuation procedure. This task is much more complicated and only rough estimations can be provided with the current state-of-the-art. Fire growth is indeed linked to flame spread. Flame spread is directly dependent  on  material  properties  with  geometry  layout  and  ventilation  conditions playing a crucial role. Material properties controlling flame spread can be evaluated by using  small-scale  flammability  testing  within  an  acceptable  degree  of  accuracy  for material ranking purposes [14]. However, the extrapolation of small scale data to predict full scale behaviour is also a critical point still under active research, especially when attempting to span multiple orders of length scales. Typical tunnel fires involve a wide range of material, including thermo-plastics which show complex melting and dripping behaviour with burning surfaces highly convoluted. In typical full-scale fire scenarios every  burning  face  sees  a  variety  of  radiant  fluxes  coming  from  the  fire  plumes  and from other hot surface. The resulting heat release rate of a full-scale object is the sum of the heat release rate from a complex distribution of melting and burning surface, seeing a full spectrum of heat fluxes [15]. In general this distribution depends on the particular geometric configuration and it is not unique.

The geometry of the fire load also is critical issue when evaluating flame spread and the consequent  fire  growth  curve.  In  opposed  spread  the  flame  develops  against  the  air flow.  In  this  case  the  heated  region  of  the  material  produced  by  the  radiant  feedback from the flame is small and then the flame propagates slowly and steadily. In the case of concurrent flame spread, the air flow and the flame spread direction are the same. In this scenario  the  heated  region  of  the  material  produced  by  the  flame  has  the  same dimensions of the flame itself. Concurrent flame spread rate is in between one and two orders  of  magnitude  larger  than  opposite  spread  rates  [14]  and  it  is  self-accelerating. Tunnel  fires  experience  a  wide  range  of  geometry  and  consequently  different  spread regimes are present at different stages.

Further  complexity  is  added  when  introducing  the  effect  of  the  ventilation  system controlling  the  oxygen  supply  into  the  fuel  bed,  the  flame  shape  and  amount  of  heat which is re-irradiated back to the burning surfaces [16].

Given the large uncertainty incurring on flame spread from all the previous considerations,  a  meaningful  prediction  the  fire  growth  is  a  complex  task  and  only rough estimation  can  be  provided  with  the  current  state  of  the  art.  Most  of  them  are based on experimental evidences. For example observations of the above cited tunnel fire experiments have shown that the typical t 2 fire representation [6] does not explain the growth  of  any  of the experimental  data  available, while  a two-step  linear approximation provided a better estimation [17]. During the first growth stage, the fire would  grow  slowly  up  to  1÷2  MW,  while  during  the  second  stage,  the  growth  rate would be significantly higher (up to 15 MW/min). A more detailed explanation will be given in the following sections.

Same rough estimations can be provided for smoke production. Average values given by PIARC and confirmed by the EUREKA fire test program [12] are resumed in Table 4.

Table 4: Approximate smoke production from tunnel fires [9]

|                               | Smoke flow [m3/s]   | Smoke flow [m3/s]   |
|-------------------------------|---------------------|---------------------|
| Type of vehicle               | PIARC               | EUREKA TEST         |
| passenger car                 | 20                  | -                   |
| passenger van                 | -                   | 30                  |
| 2 -3 passenger cars           | -                   | -                   |
| 1 van                         | -                   | -                   |
| lorry without dangerous goods | 60                  | 50 -60              |
| HGV                           | -                   | -                   |
| Petrol tanker                 | 100 - 200           | -                   |

Temperature distributions and peak temperature attained during  a tunnel fire scenario represent important variable for design purposes. Also in this case the actual knowledge is based on experimental data. Table 5 gives an overview of the maximum temperatures recorded during full scale tunnel fires including MTFTVP, EUREKA, Second Benelux tunnel  test  and  Runehamar  tunnel  fire  tests  [11-13,18,19].  As  it  can  be  seen,  the temperature  ranges  are  quite  large  mainly  depending  on  the  specific  conditions including ventilation conditions, fire load and tunnel cross section geometry. A larger set of experimental measurements of tunnel fire peak temperature is available in [19].

Table 5: Maximum peak temperature recorded on full scale experimental tunnel fires [11-13,18,19].

| Type of vehicle   | Peak Temperature [˚C]   |
|-------------------|-------------------------|
| passenger car     | 200-400                 |
| bus               | 700                     |
| HGV               | 1000-1365               |
| petrol tanker     | 1000 -1400              |

The test involving HGVs fires showed that the temperatures measured downstream of the  fire  were  very  high  with  flaming  zone  expanding  up  70-100  m.  Such  high temperature  could  affect  the  entire  tunnel  ceiling  downstream  of  the  fire  causing considerable spalling of the unprotected tunnel ceiling and eventually flame spread to other vehicles. Same considerations can be given for the upstream region.

## 1.3. The role of the ventilation system

The  ventilation  system  plays  a  fundamental  role  in  tunnel  safety  both  in  normal operating conditions and in case of fire. In normal operating conditions, the ventilation has to dilute contaminants emitted from the travelling vehicles keeping the air quality within  safety  levels  for  the  tunnel  users.  The  dilution  of  smoke  will  have  a  direct improvement  on  the  tunnel  visibility.  The  first  attempts  of  installing  mechanical ventilation systems in tunnels have been made in the 1920s. This was mainly triggered by the concern on the increasing temperature which  was  taking place in the underground metro system in New York and London [20]. Previously, the ventilation of such environments was accomplished by utilizing the piston effect produced by moving trains  and  it  was  enhanced  by  the  presence  of  vertical  shafts  permitting  a  continuous exchange of air with the exterior. Analogously, the introduction of the first mechanical ventilation devices in road tunnels was triggered by the concern on air quality and the impact of exhaust gases emitted by internal combustion engines.

Due  to  the  growing  concern  on  tunnel  fire  safety,  the  ventilation  system  has  gained great  importance  also  in  the  management  of  emergency  fire  scenarios  in  tunnels.  In these cases it has the complex task of smoke management. Which ventilation system is to be selected depends mainly of the tunnel layout and the fire safety strategies chosen for  the  specific  tunnel.  However,  ventilation  systems  fall  in  two  broad  categories: natural and mechanical. In the first case, the air movement is induced by temperature or pressure  gradients  across  the  tunnel  portals  (i.e.  due  to  meteorological  effects)  which have importance for long tunnels, and by the piston effect induced by the traffic itself. Mechanical ventilation systems instead, use complex combinations of fans, ducts and dampers for the scope. Depending on the configuration, mechanical ventilation systems are  classified  in  longitudinal,  fully  transverse  ventilation  systems  and  semi-transverse ventilation systems. However  for specific reasons (i.e. enhance smoke control capabilities) hybrid configurations can be encountered.

## 1.3.1. Natural ventilation systems

Natural ventilation systems manly rely on meteorological conditions and piston effect from moving vehicles to guarantee acceptable environment conditions within a tunnel. Meteorological conditions, including temperature and static pressure difference across tunnel portals as well as the effect of the wind, can have a significant impact in long tunnels.  Eventually,  natural  ventilation  phenomena  can  be  promoted  by  including vertical shafts due to an enhanced chimney effect. Unfortunately none of the previous variables can be relied upon when designing tunnel ventilation strategies.

Same considerations can be drawn when considering the ventilation flows due to piston effects. Indeed, it depends on a large number of factors, vehicle speed, vehicle spacing, traffic direction, vehicle drag coefficient, and tunnel geometry, and as expected, many of them cannot be controlled. Small-scale experiments have demonstrated that the ratio between air bulk airflow velocity and vehicle velocity is mainly dependent on the traffic conditions  and  ranges  between  15%  and  26%  [21].  Full  scale  measurements  under various  realistic  traffic  situations  performed  in  a  1.8  km  long  tunnel  in  Taipei  City provided lower values: the ratio between vehicles and bulk flow speed ranged between 2% and 7% when the traffic density varied between 2 and 20 vehicles per km of tunnel length  and  the  average  traffic  velocity  is  90  km/h  [22].  Figure  1  depicts  the  typical correlation  between  traffic  density  and  induced  ventilation  flows  in  a  tunnel  in  the Taipei City tunnel.

Figure 1: Typical traffic flow and induced ventilation in the 1.8 tunnel in Taipei City. Traffic density and induced ventilation as presented in [22]

<!-- image -->

Line chart

Similar values have been encountered for railway tunnels during the passage of a train [23].    However,  the  same  authors  confirmed  that,  in  two-way  traffic  conditions,  the effectiveness  of  the  piston  effect  is  compromised  and  the  ratio  between  bulk  flow velocity and vehicle velocity is radically reduced.

For this reason, natural ventilation systems are applied to short tunnels. Depending on the  specific  national  guidelines,  the  boundary  between  short  and  long  tunnels  ranges between 350 m÷ 700 m in Germany or 400 m in UK [24].

In case of fire, smoke cannot be controlled due to the absence of mechanical ventilation devices,  and  naturally  stratifies  and  spreads  longitudinally  along  the  tunnel.  Due  to stratification, the lower portion of the tunnel cross section is free of smoke promoting a safe evacuation of the tunnel users. The depth of the smoke layer underneath the ceiling varies with fire size and fire growth rate, tunnel layout (i.e. dimensions, slope, and cross section),  distance  from  the  fire  source  and  eventually  with  the  natural  ventilation phenomena  (i.e.  environment  conditions  and  piston  effects).  Due  to  the  heat  losses through walls, mixing at the interface with the fresh air which is recirculated beneath the  smoke layer,  the  natural  smoke  stratification  breaks  down  after  a  certain  distance and the vitiated gases occupy the entire tunnel cross section. The smoke recirculation towards  the  fire  source  induces  also  a  serious  deterioration  of  the  environmental conditions in the vicinity of the fire. Experimental observations demonstrate that stable stratification can be maintained initially for a distance ranging between 400 m and 600 m from the fire [24]. Eventually, the presence of intermediate chimneys can improve the smoke  removal  from  the  tunnel  but  usually  this  is  not  a  reliable  approach.  For  this reason, it is easy to understand that natural ventilation becomes significantly risky for long  tunnels  and  it  represents  a  viable  approach  only  for  tunnels  shorter  than  few hundred meters.

## 1.3.2. Mechanical ventilation systems

## 1.3.2.1. Longitudinal ventilation systems

Longitudinal  ventilation  systems  are  designed  in  order  to  generate  a  longitudinal ventilation  flow  within  the  tunnel  with  air  introduced  or  extracted  from  a  limited number of  points.  The  longitudinal  movement  can  be  induced  by  the  presence  of  air injection  points  into  the  tunnel  or  by  using  fans  installed  on  the  ceiling  providing longitudinal thrust. The first design option uses Saccardo nozzles located in the vicinity of  the  tunnel  portals  which  inject  air  with  high  velocity  and  induce  longitudinal ventilation flow. A schematic of a Saccardo longitudinal ventilation system is depicted in Figure 2.

Figure 2: A schematic of a Saccardo longitudinal ventilation system [25]

<!-- image -->

Icon

Longitudinal ventilation systems based on jet fans use series of axial fans (known as jet fans or boosters) installed on the tunnel ceiling characterized by high thrust (hundreds of  N)  and  high  discharge  ventilation  velocities  (around  30  m/s).  The  jet  fans  can  be installed  individually,  in  pairs  or  even  more.  A  schematic  of  a  jet  fan  longitudinal ventilation system is depicted in Figure 3.

Figure 3: A schematic of a jet fan longitudinal ventilation system [25]

<!-- image -->

Geographical map

Both the previous ventilation systems are characterized by an almost uniform ventilation velocity through the whole tunnel domain with pollutant concentrations and air temperature increasing in direction of the ventilation flows. In comparison to other more  complex  ventilation  systems  (i.e.  transverse  and  semi-transverse  ventilation system), longitudinal ventilation systems require less space for ventilation building and ductworks, and a lower capital investment. On the contrary, the tunnel cross section has to  be  large  enough to accommodate their installation. The maintenance and operating cost break-even point associated with a large number of jet fans must be considered. If the  system  is  characterized  by  a  number  of  jet  fans  larger  than  20,  it  may  be economically convenient to move to other centralized ventilation layouts [26].

The typical ventilation strategies adopted in longitudinally ventilated tunnel require the ventilation  system  to  push  the  smoke  downstream  of  the  incident  region  in  the  same direction as the road traffic flow, avoiding the smoke spreading against the ventilation flow (back-layering effect). The vehicles downstream of the fire zone are assumed to leave the tunnel safely. All the studies on back layering show that the maximum critical velocity is in the range from 2.5 m/s to 3 m/s [27-30].  Thus, an adequate ventilation system  must  guarantee  air  velocities  higher  than  this  range  in  the  region  of  the  fire incident.  A  more  detailed  overview  on  the  critical  velocity  will  be  given  in  the following sections.  Longitudinal ventilation systems are very effective for tunnel with uni-directional traffic flows, providing enhanced smoke control for a wide range of fire sizes. The ventilation strategies to be adopted are also straightforward. Nowadays, their applicability is limited mainly by the tunnel length.

## 1.3.2.2. Transverse ventilation systems

Transverse ventilation systems are characterized by uniform air supply and extraction along the tunnel length realized by means of full-length ducts. Supply ducts are usually located either beneath the road deck or above a false ceiling and are connected to the tunnel  environment  through  grills  or  dampers  that  can  be  automatically  opened  in specific  location  to  promote  smoke  extraction.  The  ducts  lead  to  ventilation  stations equipped with axial fans. A schematic of a transverse ventilation system is presented in Figure  4.  In  long  tunnels  the  supply  ducts  are  usually  divided  in  sections  in  order  to limit the size of each ventilation station and the air velocities. Given the dimensions of the duct work and the size of the ventilation stations, the initial investment cost is high.

In  normal  operating  conditions  the  concentration  of  pollutants  is  uniform  along  the tunnel length (if there is no longitudinal air flow) making this systems well suited for long tunnels also for bi-directional traffic operation.

In  case  of  fire,  the  ventilation  system  is  operated  in  order  to  maintain  a  smoke  clear zone for evacuation purposes by creating a stable stratification of the smoke. The latter is  extracted  through  dampers  which  are  opened  in  the  vicinity  of  the  fire.  Eventually fresh air can be supplied. More complex ventilation strategies can be used depending on the specific tunnel layout or boundary conditions.

Globally,  transverse  ventilation  systems  are  operated  in  order  to  avoid  the  smoke spreading in the tunnel by promoting smoke confinement, stratification and extraction. An optimum strategy would provide limited air velocity (~ 1 m/s) in the fire vicinity. A velocity  profile  converging  towards  the  fire  zone  is  also  desired  in  order  to  promote faster smoke confinement. Transverse ventilation systems are proved to be effective for smoke  control  in  case  of  relatively  small  fires  (&lt;  20  MW).  In  these  scenarios,  the extraction efficiency appears to depend mainly on the air flow velocity while the shape of the dampers, for equal opening area, does not have any significant effect [31]. The same authors show that the efficiency of transverse ventilation systems mainly depends on the air flow velocity for small fire size. However, ineffective smoke and temperature managements have been observed for larger fire sizes [11].

It is worth to note that a viable longitudinal flow control is difficult to achieve, even if the system has a large capacity because there are not compensating forces acting in the longitudinal  direction.  Fire  detection  and  localization  are  also  critical  issues  for transverse ventilation system.

Figure 4: A schematic of a fully transverse ventilation system

<!-- image -->

Engineering drawing

## 1.3.2.3. Semi-transverse ventilation systems

Transverse  ventilation  systems  are  characterized  by  uniform  air  supply  or  extraction along the tunnel length realized by means of one full-length duct. Depending on the way the ventilation system is operated, semi-transverse ventilation systems can be classified as supply semi-transverse ventilation systems (see Figure 5) or exhaust semi-transverse ventilation systems (see Figure 6). The former are characterized by a uniform air supply while  the  latter  have  a  uniform  collection  of  air  along  the  tunnel  length.  In  normal operating conditions supply semi-transverse systems are activated in order to provide dilution to the traffic pollution. In emergency conditions the air supply could be used to dilute fire effluents; however, reversible fans should be preferably adopted and used to extract smoke during fire scenarios. In fire scenarios, exhaust semi-transverse systems are operated to extract smoke promoting smoke stratification and extraction.

The same limitations presented for fully transverse ventilation systems apply to semitransverse systems. They have limited capability in controlling longitudinal ventilation flows and they are likely to be unable in managing smoke and temperature in large fire scenarios.

Figure 5: A schematic of a supply semi-transverse ventilation system

<!-- image -->

Engineering drawing

Figure 6: A schematic of a exhaust semi-transverse ventilation system

<!-- image -->

Engineering drawing

## 1.3.3. Hybrid ventilation systems

Beside the previous classification, ventilation systems with intermediate characteristics are often encountered worldwide. In most of the cases they are hybrid combinations of longitudinal  and  transversal  layouts  resulting  from  refurbishments  or  updating  of  old un-effective ventilations systems. This is the case of the Mont Blanc tunnel (11.6 km), which  has  been  converted,  after  the  catastrophic  fire  in  1999,  from  fully  transverse ventilation system to hybrid transverse-longitudinal. Another example is represented by the Dartford Tunnels (UK) converted from semi-transverse ventilation system to hybrid semi-transverse-longitudinal. In both the previous cases the existing ventilation systems have been updated with the introduction of jet fans for enhancing longitudinal smoke control.

In  general  hybrid  ventilation  systems  are  designed  in  order  to  provide  high  smoke control capabilities both in bi-directional and uni-directional traffic operation. In some cases they are operated in order to generate smoke-clear zones on both sides of fire site. The ventilation strategies used in hybrid ventilation systems are generally very complex requiring a careful analysis of all the variables involved including fire location, tunnel layout, boundary conditions at the portals and ventilation system settings.

## 1.4. Interaction between fire and ventilation system

The management of indoor ambient quality in underground structures both in ordinary operating and emergency conditions involves the use of the ventilation system.

Here  it  is  stressed  that  a  tunnel  and  the  corresponding  ventilation  plant  constitutes  a single  system.  Its  thermo-fluid-dynamic  behaviour  is  affected  by  several  internal  and external factors, such as barometric pressure at the portals, tunnel slope, set-points of the ventilation system  and  traffic conditions [32].  Besides  these,  in  emergency scenarios,  fire  dynamics,  smoke  movements,  stratification  and  dilution,  heat  transfer with the tunnel linings are deeply coupled with the ventilation flows.

Mainly  two  aspects  must  be  taken  into  account  when  considering  the  interaction between  ventilation  flows  and  fires:  firstly,  it  controls  the  movements  of  smoke, stratification  and  dilution  and  secondly  it  supplies  the  fire  with  the  oxidizer.  A  good understanding of the interaction between ventilation and a fire is therefore vital when developing a fire safety strategy.

## 1.4.1. Ventilation velocity and back-layering

The  critical  velocity  is  by  definition  the  minimum  longitudinal  air  flow  required  to prevent  the  occurrence  of  back-layering  in  tunnel  fire  scenarios.  The  back-layering phenomenon is the reverse smoke flow that can spread against the tunnel longitudinal ventilation if it is too low. An example of back-layering occurrence is depicted in Figure 7.

Figure 7: Photograph of a small scale tunnel fire during the occurrence of back-layering. The fire size in 15 kW. The tunnel has an arched cross section (width 274mm, height 244 mm). Adapted from [33].

<!-- image -->

Photograph

The  exact  value  of  the  critical  velocity  depends  mainly  on  the  buoyant  plume characteristics including smoke temperature, smoke flow rate, fire source size as well as tunnel  height  and  width.  The  simplest  techniques  to  predict  the  critical  velocity  are based on semi-empirical equations obtained by Froude Number preservation combined with some experimental data.

The Froude Number is defined as

<!-- formula-not-decoded -->

where g is  the  gravity, D and U are  the  characteristics  length  and  velocity  scales respectively. Equation (1) can be rearranged by using the density ratio of the smoke in order  to  include  the  effects  of  stratification.  When  rearranged  in  this  for  it  is  usually called Richardson number or modified Froude number:

<!-- formula-not-decoded -->

where ρ represents the density.

The first empirical relation based on Froude theory is due to Thomas (1958) [27] who argued  that  the  characteristics  of  the  flow  are  dependent  on  the  ratio  of  buoyancy  to inertial forces on the tunnel cross section. Thomas concluded that, when the ventilation velocity  is  close  to  the  critical  value,  the  modified  Froude  number  is  close  to  1  and therefore  the  back-layering  does  not  occurs.  Under  this  assumption,  it  can  be  written that

<!-- formula-not-decoded -->

where, UC is  the  critical  velocity  value, H represents  the  tunnel  height  and ρ 0 is  the ambient temperature. After substituting an expression correlating the convective part of the  fire  heat  release  rate  (HRR)  and  fire  induced  smoke  characteristics  (temperature, density and flow rate), a final correlation can be obtained

<!-- formula-not-decoded -->

where k is a proportionality constant, Q is the total HRR, To is the ambient temperature, cp is the air specific heat, A is the tunnel cross section and λ is the radiative fraction of the HRR. On the basis of experiment conducted in short corridors, the proportionality constant was found to be equal to 0.8 [34].

A similar correlation has been developed by Kennedy and co-workers:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where K is  an dimensionless empirical constant equal to 0.61, α is  the tunnel gradient and Tf is  an  average  temperature  of  the  fire  effluents  [35].  This  correlation  has  been built on the basis of small scale experiments conducted by Lee and co-workers in 1979 [36].

Thomas correlation is valid within a limited range of heat release rates where the 1/3 law well fits the  experimental data.  For higher  heat release rates, the correlation fails because  it  is  not  able  to  represent  the  asymptotic  behaviour  of  the  critical  velocity. Indeed, on the basis of small scale experiments, Oka and Atkinson pointed out that for high HRR the critical velocity reaches an asymptotic value which is independent from the HRR [28]. This behaviour is clearly presented in Figure 8 showing the correlation between  dimensionless  critical  velocity  and  dimensionless  heat  release  rate.  Oka  and Atkinson proposed a modified correlation whish is presented hereafter (equations from (8) to (11)):

Figure 8: Variation of dimensionless critical velocity against dimensionless heat release rate. (O) measurements of critical velocity; (continuous line) equations (8) and (9): (dashed line) Thomas correlation (4). (from [28]).

<!-- image -->

Line chart

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where Q* and Uc* are  the  dimensionless  heat  release  rate  and  dimensionless  critical velocity that can be obtained by using equation (10) and equation (11).  The proportionality  constant Kv ranges  between  0.22  and  0.38  depending  on  the  burner geometry.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Such asymptotic behaviour has been also observed in full scale experimental campaigns such  as  Memorial  tunnel  fire  ventilation  test  program  (MTFVTP)  [11]  or  EUREKA [12]. A theoretical explanation has been given by Wu and Bakar [33] attributing such behaviour  to  the  positioning  of  the  intermittent  flames  in  the  tunnel  cross  section. Indeed, free fire plumes are characterized by three different regimes [6]

1. persistent flame region, located close to the fire source and characterized by an accelerating flow of combustion gases
2. Intermittent  flame  region,  characterized  by  intermittent  flaming  and  a  nearconstant flow velocity
3. The buoyant plume characterized by a decreasing velocity and temperature with the height.

For  relative  small  fires  having  flame  length  smaller  that  the  tunnel  height,  only  the buoyant smoke impinges the ceiling and in under-ventilated conditions, it will generate back-layering. Obviously the characteristics of the buoyant plume will be depending on the fire HRR. However, for large enough fires, the intermittent flames will impinge the ceiling occupying the upper portion of the tunnel cross section and in under-ventilated conditions they will be present in the back-layering. Intermittent flame are characterized by  constant  speed  regardless  the  fire  source  and  therefore,  they  build  up  a  buoyancy force with is not sensitive to the fire HRR. Consequently the critical velocity will tend to  its  asymptotic  values.  A  similar  explanation  has  been  given  also  by  Hwang  and Edwards [37].

However, it must be stressed  that  simplified  analysis  based  on  Froude  scaling  theory cannot take into account the effect of the tunnel geometry (i.e. tunnel width) and tunnel slope on the critical velocity. Based on the classical Thomas theory it is easy to obtain a linear  correlation  between  the  critical  velocity  and  the  quantity (1/W) 1/3 where W represents  the  tunnel  width.  Indeed,  small  scale  experiments  have  confirmed  that  for aspect ratios greater than 1 (width W to height H ) the critical velocity decreases with the tunnel width but following a trend different from the (1/W) 1/3 law proposed by Thomas. Furthermore,  it  appears  that  for  aspect  ratios  smaller  than  1  the  critical  velocity increases  with  the  tunnel  width  [30].  Analogous  deviations  from  the  classical  theory have been encountered when introducing blockages upstream the fire source or when varying  the  fire  source  geometry;  in  particular  the  critical  velocity  appears  reducing when wider fire sources are adopted [28].

The effect of the tunnel slope on the critical velocity has been investigated by Atkinson and Wu [38] and by Ko and co-workers [39] on the basis of small scale experiments involving a propane gas burner for the former and methanol, acetone and n-heptane pool fires for the latter. In both the cases the results showed that the critical velocity increases with the tunnel slope due to the enhanced stack effect following equation (12)

<!-- formula-not-decoded -->

where θ , C U and ,0 C U are the critical velocities in a inclined and horizontal tunnel, ϑ the tunnel slope, θ K an empirical constant ranging between 0.014 and 0.033 in accordance with [38] and [39], respectively.

On  the  basis  of  the  previous  theoretical  considerations  supported  by  experimental measurements,  it  can  be  claimed  that  the  maximum  critical  velocity  value  to  be expected  in  any  tunnel  fire  scenario  is  between  2.5  m/s  and  3  m/s.  If  the  ventilation velocity is in this range (or eventually larger) the back-layering is usually avoided and the  smoke  are  pushed  downstream  of  the  fire  region.  Smoke  stratification  is  usually compromised.

For ventilation velocities between 1 m/s and 2.5÷3  m/s, depending on the fire source size, back-layering can occur. The back-layering distance usually varies between zero and  17  times  the  tunnel  hydraulic  diameter  [5].  For  even  lower  ventilation  velocities (between 0 m/s and 1 m/s) the back-layering distance can be very large (several hundred meters) and it is almost uniform in both directions.

Ingason proposed an approximated correlation to predict back-layering distance based on small scale experiments [5] and Froude scaling theory.

<!-- formula-not-decoded -->

Equation  (13)  correlates  the  back-layering  distance Lb to  the  tunnel  geometry,  the ventilation velocity U and the fire HRR Q . The proportionality constant, deduced from small scale experiments, ranges between 0.6 and 2.2. Given the lack of large scale tests, great care must be adopted when predicting the back-layering distance on the basis of equation (13). Indeed, in a recent work, it appears that equation (13) seriously underpredicts the back-layering distance (up to 1 order of magnitude) [40]. This conclusion has been drawn on the basis of a recent large scale set of experiments in a 1 km long tunnel ( W ~ 10 m, H ~ 7 m, slope ~ 2%) involving fires between 1.8 MW and 3.2 MW.

## 1.4.1.1. Ventilation velocity and fire HRR

Ventilation  flows  have  a  direct  impact  on  the  tunnel  fire  dynamics.  By  using  a probabilistic  approach,  Carvel  and  co-workers  demonstrated  that  the  HRR  of  a  HGV could increase in size by a factor 4 when the ventilation velocity is around 3 m/s and by a factor 10 when the ventilation is up to 10 m/s [41]. The authors found that a similar behaviour could be expected for the fire growth rate asserting that it can increase by a factor of 5 at 3 m/s and by a factor of 10 at 10 m/s.

Such behaviour is mainly dependent on the enhanced heat transfer from tilted flames and on the improved transport of oxygen into the fuel bed. However, it can be expected that  for  ventilation  flows  higher  that  a  certain  limit,  the  cooling  effect  due  to  the ventilation  flows  counteracts  against  the  improved  radiative  heat  transfer  from  the flames; in this conditions peak HRR and fire growth rate can be reduced.

The enhancing effects of the ventilation flows on the fire peak HRR and growth rate have been observed experimentally both on large and small scale tests. In particular this behaviour  has  been  recorded  during  the  Second  Benelux  Tunnel  fire  tests  for  canvas covered trucks loaded with wooden cribs and tyres. The fire growth rate with ventilation velocity ranging between 4 m/s ÷ 6 m/s was almost 2 times higher when compared to the  fire  development  in  no-ventilation  scenarios.  The  peak  HRR  was  about  1.5  times higher  [13].  A  similar  behaviour  has  been  observed  on  small  scale  experiments  and described  by  Lonnemark  and  co-workers  [16].  The  increase  in  the  peak  HRR  ranged between 1.3÷1.7 and 1.8÷2 times for high and  low porosity  wood  cribs  respectively. They also found that the fire growth rate increased by a factor 5 to 10 depending on the tunnel cross section. Beyond a certain velocity limit the HRR and the fire growth rate did not seem to vary significantly.

A more recent literature review presented by Carvel addressed other significant aspect of the fire dynamics in tunnel [17]. The work reviewed a large number of tunnel fire experiments including the Second Benelux Tunnel fire tests [13], the Runehamar fire tests [8], and the EUREKA fire test program [12] and performed regular observations on the effect of the ventilation velocity on the fire growth phase.

The author observed that the typical t 2 fire representation [6] was not fitting any of the experimental data and proposed a two-step linear approximation. During the first step the fire would grow slowly up to 1÷2 MW, while during the second step, the growth rate  would  be  significantly  higher  (up  to  15  MW/min).  Figure  9  shows  a  two  steps approximation of the fire growth phase as observed in [8] and [13].

Figure 9: Two step approximation of fire growth rate phase for the Second Benelux tunnel fire Tests and Runehamar Fire Test Program (from [17])

<!-- image -->

Line chart

The changing in the fire regimes usually takes place after a delay phase usually as long as few minutes (from 2 to 6). The author observed also that the delay phase length and the fire growth rate are somehow correlated to the ventilation flows experienced by the fire  during  its  development.  A  table  resuming  the  observed  trends  is  introduced hereafter.

Table 6: Summary of the observed correlation between ventilation rate, delay phase length and fire growth rate (from [17]).

## 1.5. Analysis of tunnel ventilation systems and fires

On the  basis  of  the  previous  discussions  it  is  easy  to  understand  that  fire  behaviour, smoke dynamics and ventilation flows are deeply coupled and they cannot be studied separately.  In  other  words,  the  resulting  air  flow  within  a  tunnel  is  dependent  on  the combination  of  fire-induced  flows,  active  ventilation  devices  (jet  fans,  axial  fans), tunnel  layout,  atmospheric  conditions  at  the  portals  and  the  presence  of  vehicles. Although an overall analysis of tunnel ventilation flows and fires can be very complex, the  resulting  information  is  crucial  for  tunnel  fire  safety  purposes.  Studies  of  tunnel ventilation  flows  and  fires  are  indeed  fundamental  to  assess  the  capabilities  of  a ventilation system to manage smoke, to design ventilation and evacuation strategies, to predict loss of tenability in the environment and to minimize damages to the structure.

Depending  on  the  accuracy  required  and  the  resources  available,  a  solution  to  the problem can be reached using different ways.

## 1.5.1. Small and large scale experiments

Full scale tests, generally conducted within unused tunnels, require very large financial investments but provide large amounts of collected data. Some examples have already been cited. The Memorial Tunnel fire ventilation test program [11], the EUREKA fire test program [12] and the Second Benelux Tunnel fire test program [13] are only few examples.  A  wide  review  of  the  experimental  tunnel  fires  conducted  in  the  last  4 decades is available in [42]. Because of the huge costs associated, only a limited number of  tests  can  be  carried  out.  Furthermore  they  are  highly  specific  and  their  outcome  is strictly  related  to  the  specific  tunnel  layout,  fire  load  material  and  geometry.  Design procedures  sometimes  use  small  scale  tunnel  models  in  order  to  represent  ventilation and  fire  scenarios.  Interpretation  of  their  results  is  dependent  on  the  relevant  scaling laws and model scale results may not have a general validity in relation to the full scale case.  Nevertheless,  experimental  data  are  widely  used  to  extrapolate  proportionality constant  used  in  semi-empirical  correlation  to  predict  back-layering  occurrence  and distance, smoke production and smoke front velocity and temperature.

## 1.5.2. Numerical modelling

The  analysis  of  tunnel  ventilation  systems  can  be  also  conducted  using  numerical models  based  on  a  mathematical  representation  of  the  physical  phenomena  involved. Numerical  models  are  usually  highly  flexible,  significantly  more  economic  than experimental test, and allow for large parametrical studies and sensitivity analysis. The accuracy  of  numerical  models  must  be  always  addressed  on  the  basis  of  a  direct comparison  of  the  results  to  experimental  findings  in  order  to  assess  range  of applicability and limitations.

Several  numerical  approaches  have  been  adopted  by  the  international  community  to address tunnel fire safety issues.

The  overall  behaviour  of  the  ventilation  system  can  be  approximated  using  1D  fluid dynamics  models  under  the  assumptions  that  all  the  fluid-dynamic  quantities  are uniform in each tunnel cross section and gradients are only present in the longitudinal direction. 1D models have low computational requirements and are specially attractive for parametric studies where a large number of simulations have to be conducted. In the last  two  decades  several  contributions  on  the  application  of  1D  models  to  tunnel ventilation flows and fires flows have been published; a literature review as well as a wide description of their accuracy and range of applicability will be presented in chapter 2.

Zone models are based on the experimental evidence that, under certain conditions, fire effluents tend to stratify generating a cold air layer underneath and a hot smoke layer containing  the  fire  effluents  [43].  Zone  models  have  been  widely  used  to  simulate compartment fires but their applicability in tunnel fire scenarios is limited. Indeed, they are not able to simulate tunnel smoke dynamics due to the lack of a dedicated horizontal momentum equation needed to represent the longitudinal smoke transport in a tunnel environment. Furthermore, they are not able to take into account mixing between hot and  cold  layers  or  to  simulate  fire  scenarios  where  smoke  stratification  is  lost  (i.e. critical or supercritical ventilation scenarios).

Modified  version  of  zone  models  have  been  developed  trying  to  extend  their  use  to tunnel  fire  scenarios.  Charters  and  co-workers  developed  a  modified  version  of  zone models having a three layer domain: a hot smoke layer, a mixing layer and a cold air layer underneath [44]. As for any zone model, the accuracy of the new one mainly relies on calibration constants needed to predict the mixing between layers, hot layer velocity and plume entrainment. A similar approach has been followed by Kunst who developed a  zone model and used it to predict back-layering [29]. Kunst model is in qualitative agreement with former, widely used models and it has been validated by comparison with mostly large-scale experiments in instrumented galleries. A more recent application has been presented by Suzuki and co-workers [45]. The model uses several horizontal  layers  and  provides  reasonably  accurate  temperature  distributions  when compared to small scale fire scenarios. However also in this case, the accuracy of the model relies on calibration constants needed to predict plume entrainment and further validations test must be conducted.

CFD  techniques  are  usually  adopted  in  fire  safety  science  when  flow  field  data  are needed.  Such  techniques  are  able  to  provide  detailed  temperature  and  velocity  fields, smoke movement and stratification, toxic species evolution, heat fluxes mapping, time to untenability conditions and other important variables. The computational cost of this class of methods is high even for medium size tunnels and they are typically used for design verification. A literature review as well as a wide description of their accuracy and range of applicability will be presented in chapter 3.

Another  class of methods,  called multiscale methods,  adopt different levels of complexity in the numerical representation of the system. The multi-scale concept is an extension of the conventional 1D and CFD modelling techniques where the two models are coupled together with the latter providing the boundary condition to the former and vice-versa. The multi-scale model is solved on a hybrid computational grid, where 1dimensional elements are linked to 3-dimensional ones generating a continuous domain in the streamwise direction (see Figure 10). The 3D elements are modelled by means of a CFD tool while 1D elements by using a conventional 1D model. During the solution procedure  1D  and  CFD  models  dynamically  exchange  information  at  the  1D-3D interfaces  and  thus  run  in  parallel.  A  literature  review  as  well  as  a  wide  description multiscale modelling technique for tunnel ventilation flows and fires will be presented in chapters from 4 to 7.

Figure 10: A schematic of a hybrid computational grid for multiscale calculation of tunnel ventilation flows and fires

<!-- image -->

Icon

## 1.6. Test cases

This  thesis  contains  in  different  chapters  several  applications  of  1D  models,  CFD models and multiscale models. In most of the cases the developed models have been applied  to  predict  the  behaviour  of  real  operative  road  tunnels.  In  some  cases, experimental campaigns have been undertaken to characterize the behaviour of tunnel and  ventilation  system.  The  collected  data  have  been  used  to  validate  the  developed models and to assess their accuracy.

## 1.6.1. Case A: Frejus Tunnel, Bardonecchia (It)

In Chapter 2, the Frejus tunnel behaviour is simulated with a 1D model. This tunnel is a two-way  link  between  Italy  and  France  with  a  total  length  of  12870  m  and  an approximated hydraulic diameter of 6 m. The ventilation system is fully transverse and it  is  operated by means of full length supply and exhaust duct located over the tunnel ceiling.  Ordinary  ventilation  is  operated  by  introducing  fresh  air  along  the  tunnel through 3 U-shaped fresh air ducts which have 2 fans at each end. Fresh air openings are installed each 5 m. Emergency ventilation is operated using the fresh air ducts and 3 U-shaped extraction ducts. The extraction dumpers are installed each about 130 m. A more detailed description of the Frejus tunnel including typical emergency ventilation strategies  will  be  given  in  chapter  2.  Experimental  data  will  be  used  to  validate  the developed 1D model when simulating the tunnel ventilation system behaviour.

## 1.6.2. Case B: Norfolk road Tunnels, Sydney (Au)

In Chapter 3 the Norfolk road tunnels ventilation systems are simulated by using a CFD tool. These are two two-lanes unidirectional road tunnels located in Sydney (AU). The tunnels  are  460  m  long  with  a  virtually  flat  gradient.  Each  tunnel,  longitudinally ventilated, is equipped with 6 pairs of jet fans. A large set of air velocity measurements in the tunnel central section were made available by the tunnel operator and they have been used to validate the capability of CFD tools to model tunnel ventilation flows at ambient conditions.

## 1.6.3. Case C: Wu-Bakar small scale tunnel

In  Chapter  3  a  CFD  tool  has  been  also  used  to  simulate  small-scale  fire  scenarios. Experimental data have been provided by Wu and Bakar [33] that carried out a series of small scale experiments on five horizontal tunnels with different cross-sections. They assessed, on the basis of accurate measurements in a controlled environment, the effect on  the  critical  velocity  of  tunnel  cross  section  and  fire  heat  release  rate.  Among  the different cross sections, the data relative to the square cross-sectional tunnel (0.25×0.25 m 2 cross section) will be considered in this document. The small scale tunnel is around 15 m long and it is equipped with a circular porous bed propane burner (diameter equal to 0.106 m) located at a distance of 6.21 m from the tunnel inlet. The tunnel outlet is located  at  a  distance  of  8.7  m  from  the  burner  centre.  The  burner  heat  release  rate, controlled by the propane flow rate, was varied during the tests ranging between 1.5 kW and 30 kW. The measured values of critical velocities in two different fire scenarios (3 kW and 30 kW) will be used in the next sections to validate the fire CFD model.

## 1.6.4. Case D: Dartford Tunnels, London (UK)

In chapter 5 the multiscale model has been used to simulate the ventilation flows in the Dartford tunnels. They are two twin-lane, uni-directional road tunnels under the River Thames, crossing from Dartford at the south (Kent) side of the river to Thurrock at the north  (Essex)  side,  about  15  miles  east  of  London  in  the  UK.  Both  tunnels  have complex  ventilation  system  consisting  of  a  semi-transverse  system  together  with additional jet fans to control the longitudinal flow. Both the Dartford tunnels have two shafts  with  axial  extraction  fans  located  at  relatively  short  distance  from  each  of  the tunnel portals. They length is around 1.5 km while the approximate internal diameter is 8.6  m  and  9.5  for  the  West  and  the  East  tunnels,  respectively.  A  more  detailed description  of  the  Dartford  tunnel  including  typical  emergency  ventilation  strategies will  be  given  in  chapter  5.  A  large  set  of  experimental  data  measured  in  the  both  the tunnels will be used to corroborate the developed multiscale model.

## 1.6.5. Case E: Test case tunnel

A different test case has been used in chapters 6 and 7 to discuss the multiscale model formulation  when  dealing  with  tunnel  fire  scenarios  both  in  steady  state  and  timedependent  conditions.  The  tunnel  is  1.2  km  long  with  a  standard  horseshoe  cross section. The ventilation is longitudinal and uses 10 pairs of 50 m spaced jet fans. The jet fans are arranged in two groups, each group installed near each portal. A more detailed description of the geometry and typical emergency ventilation strategies will be given in chapters 6 and 7.

## 2.1. Introduction

The main advantage of using 1D models for the analysis of complex network systems, (i.e. the tunnel main gallery and ventilation ducts), is that it allows for a complete and compact description of the system. This characteristic has two major consequences: 1) it is  possible  to  define  with  adequate  precision  the  boundary  conditions,  such  as  the ambient  conditions  at  the  portals,  and  2)  it  is  suitable  for  applications  requiring  the computation  of  a  large  number  of  scenarios,  such  as  during  the  assessment  of  safety strategies for complex tunnels.

Its intrinsic limit is instead due to the fact that the flow in each cross section is assumed homogeneous; it is then identified by a unique value of the variables pressure, velocity, temperature,  smoke  concentration,  etc.  This  peculiar  assumption  makes  1D  models unsuitable to simulate the fluid behaviour in regions characterized by high temperature or velocity gradients. Regions characterized by high temperature gradients are typically

<!-- image -->

Icon

## One-dimensional modelling

## 2

encountered close  to  the  fire  where  well-defined  smoke  stratification  is  found.  In  the case of small fires, smoke stratification is important along large section of the tunnel and determines a peculiar propagation of the smoke front. In fact it proceeds with larger velocity  than  if  it  were  to  occupy  the  entire  cross  section.  Thus,  if  1D  models  are applied  to  fire  events  (particularly  in  the  case  of  small  fires  where  the  smoke  is stratified),  it  is  necessary  to  properly  introduce  corrections  to  account  for  nonhomogeneity caused by the stratification, otherwise the calculated propagation velocity of the smoke front would be significantly underpredicted  [46]. Once the smoke away from  the  fire  has  occupied  the  entire,  or  nearly  entire,  tunnel  cross  section,  the conditions  are  close  to  homogenous  and  the  prediction  of  the  propagation  velocity  is accurate.

Regions with high velocity gradients are also typically encountered close to ventilation devices (i.e. jet fans) where the fan thrust produces highly 3D (tri-dimensional) flows and the flow homogeneity assumption of 1D model fails. Usually, 1D models describe the  behaviour  of  such  regions  on  the  basis  of  empirical  correlations  that  must  be calibrated on the specific tunnel layout. Indeed, the jet fan thrust curve provided by the manufacturer only applies to the isolated jet fans and it does not describe its behaviour once installed in a particular tunnel gallery.

## 2.2. Literature overview

The first reported codes for digital calculation of a fluid networks were produced in the late  50s.  They  were  mainly  developed  to  design  mine  ventilation  systems  and,  in  the late 60s, they became a fundamental part of any ventilation planning [47]. In spite of the fact  that  an  increasing  number of attempts were made during the early  years to adapt such  network  calculation  codes  for  the  simulation  of  fire  scenarios,  none  of  them progressed enough. A first significant attempt of including the effect of fire in network system calculation has been made in the late 70s when Greuer and co-workers produced a tool able to perform  steady  state  calculation  of  networked  system  providing temperature  velocity  and  pollutant  distributions  [47].  The  resulting  code  was  able  to perform steady state simulations of complex networked system computing the solution by using a hardy-cross-like method [48]. The numerical method adopted was based on the  solution  of  longitudinal  momentum  equations  on  closed  airway  loops  whose definition  was  not  straightforward  as  erroneous  loop  definition  could  lead  to  slow convergence.

In  the  last  two  decades,  several  national  Institutions  proposed  contributions  to  the subject. Models such as MFIRE [49], ROADTUN [50,51], RABIT and SPRINT [52] and  [53],  Express'AIR  and  SES  [54]  and  [55]  are  now  commonly  used  to  perform complete studies of tunnel ventilation systems and fires.

MFIRE, developed by the US Bureau of Mines is able to perform steady state fluiddynamic  simulations  of  underground  network  system.  The  model  has  been  tested  by Cheng et al. [56] on experimental data from a small scale underground transportation network constituted of 27 branches about 0.1 m diameter and 1-2 m length, and then applied  to  simulate  a  hypothetical  fire  outbreak  in  the  Taipei  Mass  Rapid  Transit System. The simulations were designed to investigate the direction and rate of air flows, temperature  distribution  and  emergency  ventilation  responses.  The  same  theoretical approach has been used by Ferro et al. [57-58] and Jacques [59]. The former presented a 1D  computer  model  for  tunnel  ventilation.  The  model  was  designed  to  deal  with complex  tunnel  network  including  phenomena  like  the  piston  effect  from  moving vehicles and the distribution of pollutant concentration in the tunnel domain. The model was able to perform steady state calculations. Similar approach has been used in [59] where numerical simulations of urban tunnel 2.5 km in length have been presented.

The Subway Environmental Simulation code (SES), developed by Parson Brinckerhoff Inc.[61],  is  a  1D  simulation  tool  able  to  predict  steady  state  ventilations  scenarios  in tunnel networks. The tool includes a simplified model to predict the occurrence of backlayering  as  function  of  the  fire  size  and  ventilation  conditions  (see  equations  5  to  7). The  model,  based  on  Froude  scaling  analysis,  has  been  calibrated  on  small  scale experiments.  The  experiments  were  conducted  in  a  10  m  long  tunnel  with  a  0.09  m 2 cross  section  with  the  fire  source  represented  by  the  tunnel  wood  lining  [36].  No information on the fire HRR was made available.

A more recent application is represented by the code SPRINT [53]. It is able to perform time dependent analysis of fire scenarios in tunnel ad to handle gravity-driven smoke propagation due to thermal stratification. The latter effect is accounted by superposition of  the  mean  flow  velocity,  and  the  front  velocity  is  estimated  on  the  basis  of  semiempirical  correlation.  The  model  validated  against  experimental  data  recorded  during Memorial Tunnel Fire Ventilation Test Program [11] and in the Mont Blanc Tunnel, has been applied to simulate real tunnel fire scenarios.

In a recent application, a 1D model has been used in an optimization procedure used to determine the aerodynamic coefficient in a highway tunnels 1.8 km in length [62]. The optimization, performed on the basis of detailed experimental measurements, is able to provide the pressure rise coefficients of the jet fans, the wall friction coefficient and the averaged drag coefficients of small-sized and large-size vehicles.

## 2.3. Typical mathematical formulation for 1D models

The vast majority of the 1D models for tunnel applications found in the literature are based  on  a  generalized  Bernoulli  formulation  [63].  Most  of  them  are  designed  to account  for  buoyancy  effects,  transient  fluid-dynamic  and  thermal  phenomena,  piston effect and transport of pollutant species. They are usually developed to handle complex layouts  typical  of  modern  tunnel  ventilation  system  (especially  true  for  transverse ventilated tunnel) on the basis of a topological representation of the tunnel network.

## 2.3.1. Topological representation

The topological  structure  of  complex  flow  distribution  systems,  as  pipelines,  tunnels, mines,  etc,  is  easily  described  using  matrix  representation  and  graph  theory  (see  as example [64]). This representation lays on two concepts: node and branch. A node is a section where state properties as temperatures, pressures, mass or molar fractions, etc. are  defined.  A  unique  value  of  these  properties  is  defined  in  a  node.  A  branch  is  an element bounded by two nodes and characterized by geometrical properties as length and  cross  section,  together  with  flow  and  thermal  properties,  as  roughness,  wall temperature,  etc. Branches  are  associated  to mass  flow  rates and  velocities.  A conventional  flow  direction  is  also  selected  for  each  branch,  so  that  inlet  and  outlet nodes  are  defined.  Resulting  negative  flows  refer  to  flows  directed  from  the  outlet towards the inlet.

The  flow  network  is  described  through  the  interconnections  between  nodes  and branches (multiple branches can join in the same node), with the former playing the role of flow splitter and/or junction. In graph theory, incidence matrix A is used to express the interconnections. This matrix is characterized by a number of rows equal to the total number of nodes and a number of columns equal to the number of branches (in some analyses, the incidence matrix is defined as the transpose of that presented here). The general element Aij is 1 if the i-th node is the inlet node of j-th branch, it is -1 if the i-th node is the outlet node of the j-th branch and it is 0 in the other cases. A typical layout of a tunnel network system is presented in Figure 11.

Figure 11: Example of the network representation of a tunnel showing branches between nodes

<!-- image -->

Engineering drawing

The corresponding incidence matrix A is presented below:

<!-- formula-not-decoded -->

## 2.3.2.  Fluid dynamics model

Modelling  flow  system  requires  that  continuity  and  momentum  equations  are  written with spatial dependence on one single coordinate, which, in the case of tunnels, is the longitudinal  coordinate ,  x. The  starting  points  are  the  Navier-Stokes  equations,  as described in their classical form for a time dependent three dimensional fluid flow [66] and [65],

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where u is the velocity vector, t the temporal coordinate, p the static pressure, ρ the fluid density, τ is  the  stress  tensor, S a  vector  containing momentum source terms per unit volume  (including  the  gravity  term).  Equation  (15).a,  known  as  continuity  equation, states that the rate of flow into a volume must be equal to the rate of change of mass within the volume. Equation (15).b, known as momentum equation, states that the rate of change in the fluid momentum is equal to the sum of forces acting on it.

After eliminating the y and z spatial dependences, and neglecting the viscous stress term which loses its significance in a 1D formulation, the equations become

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where u is the longitudinal velocity and SMx is the longitudinal momentum source term. The momentum source term contains all the terms related to the chimney effect, wall friction,  losses  due  to  flow  separation  at  the  portals  or  after  obstacles.  Eventually, pressure  rise  due  to  fan  operation  and  piston  effect  are  also  accounted  for.  Equation 16.b,  after  integration  along  a  branch j (which  is  also  a  streamline)  from  node i-1 to node i, leads to the generalized Bernoulli formulation for transient flows (see equation (17)). The buoyancy term has been also included.

<!-- formula-not-decoded -->

where z represents the vertical elevation and g the  gravity acceleration. After defining the total pressure P as sum of the kinetic, pressure and gravity terms, and after making explicit all the sources of momentum, equation (17) can be expressed as

<!-- formula-not-decoded -->

where j ρ represents the average density in the branch j between nodes i and i-1 , uj the average  velocity  in  the  branch j ,  and j FAN P , ∆ j PIST P , ∆ and j FRICT P , ∆ the  source  of momentum due to the fan action, the piston effect and the friction.

Equations  (18)  can  be  solved  only  after  discretizing  the  computational  domain  in branches  interconnected  by  nodes.  Such  discretization  generates  control  volumes allowing  the  integration  of  the  momentum  and  continuity  equations.  In  this  model  a staggered arrangement is used where pressure and densities are defined in nodes while the velocities are defined in the branches. An overview on the numerical solution of the problem will be given in the next sections.

## 2.3.3. Thermal model

In this section the features of the thermal problem are described. In the case of thermal analysis,  the  problem  is  complicated  by  the  temperature  definition  in  the  nodes. Whereas pressures in nodes are univocally defined, temperatures are not. In the case of a flow junction, two flows at different temperature can converge in the same node and the total mass flow rate exits at the average temperature.

The  thermal  analysis  requires  the  solution  of  the  energy  equation.  The  general formulation, valid for constant pressure, constant heat capacity and low Mach number flows, is presented hereafter

<!-- formula-not-decoded -->

where T represents  the  fluid  temperature, c the  fluid  heat  capacity, k the  fluid conductivity, u the fluid velocity components, and SE the energy source terms/sink per unit volume. Equation (19) must be simplified eliminating the spatial dependencies with the exception of the x-coordinate. Furthermore, the summation of the source/sink terms is split in two terms: the first one accounting for the heat generation due to fire ( v q ) and the second one accounting for the heat losses through walls ( l q ).

<!-- formula-not-decoded -->

The definition of qv , which is particularly important in the case of fire, will be discussed in  the  next  sections.  In  general  the  term,  representing  the  heat  conduction  along  the longitudinal  coordinate  can  be  neglected  if  compared  to  the  other  terms  of  equation (20).

In  order  to  resolve  the  energy  equation,  a  finite  volume  formulation  has  been  used. More details on discretization techniques and numerical schemes will be given in the next section.

## 2.3.4. Steady state problem

The  solution  of  the  steady  state  problem  requires  the  integration  of  the  differential equations (18) and (20) over specific control volumes. Obviously, in this case the time derivatives  must  be  neglected.  The  tunnel  domain  is  first  discretized  in  branches  and nodes  indicated  as i and j in  Figure  12.  The  variables  are  allocated  in  a  staggered arrangement.  In  particular,  pressures,  temperatures  are  calculated  in  each  node  while velocities  in  each  branch.  Therefore,  continuity,  momentum  and  energy  equations  are applied on different control volumes. In particular, a control volume included between two nodes (red dashed volume in Figure 12) is used for the momentum equations. A node  centered  control  volume  (blue  dashed  volume  in  Figure  12)  is  used  for  the integration of continuity and energy equations.

Figure 12: Schematic of the control volumes adopted for the numerical solution

<!-- image -->

Engineering drawing

Once  defined  the  control  volumes,  the  integration  of  continuity  equations  leads  to equation 21.a. The momentum equation, which has been integrated along a streamline, is already in its final form.

<!-- formula-not-decoded -->

The control volume integrals are rewritten as integrals over the entire bounding surface by using Gauss's divergence theorem leading to equations (22).

<!-- formula-not-decoded -->

The above equations integrated over the control volume surface lead to the following general algebraic continuity and momentum equations for a generic node i and a branch j respectively.

<!-- formula-not-decoded -->

Equation (23).a states that  sum of the mass flow rates entering a generic node of the network must be equal to the sum of the mass flow rate exiting the node. In particular A j is the cross section of the generic interconnected branch j .  Equation (23).b states the total pressure difference across a generic branch j (delimited by the nodes i and i-1 ) is due to the sum of all the contributions due wall friction, losses due to flow separation at the  portals  and  after  obstacles,  pressure  rise  due  to  fan  operation  and  piston  effect. Making explicit all the terms, equation (23).b becomes

<!-- formula-not-decoded -->

where f the branch friction coefficient, β the minor loss coefficient, L the branch length, Dh the branch hydraulic diameter, while FAN P ∆ and PIST P ∆ represent the pressure gain inside the branch due to fans and piston effect respectively.

The  pressure  rise  due  to  fans  is  commonly  represented  as  generic  polynomial  of  the second order known as fan characteristic curve (see equations (25)). The characteristics curve coefficients are a , b , and c . They are usually obtained from empirical correlations and they are specific for each tunnel layout.

<!-- formula-not-decoded -->

Alternatively,  in  some  works,  the  pressure  rise  due  to  fans  can  be  represented  as described  in  equations  (25).b  and  (25).c.  In  the  last  two  cases, n,  AF,  uf and K respectively  represent  the  number  of  operating  fans,  the  fan  discharging  area,  the  fan discharging velocity and the pressure rise coefficient while, η , Pe are the fan efficiency and the fan electric power.

Commonly the piston effect term can be evaluated following the expression proposed by PIARC which includes the characteristics of the vehicles and the air velocity in the tunnel [67].

<!-- formula-not-decoded -->

where ε is the aerodynamic factor of the vehicles (multiple terms should be considered for  each  kind  of  vehicles), Av is  the  vehicle  cross  section, N1 and N2 the  number  of vehicles moving in the same direction and in the opposite direction of the branch j. The vehicle velocities are respectively u1 and u2 .

The  integration  over  the  control  volumes  of  the  energy  equation  (20)  leads  to  the expression  (27)  that  can  be  rearranged  to  generate  a  generic  algebraic  equation  for  a node i (see equation (28)) .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The diffusive term at the RHS of equation (28) is usually neglected for these systems as the advective term is by far dominating the heat transfer in tunnels. The terms QL and Q represent the total heat losses and the heat generated (i.e. due to the fire) in a generic node i.

The term QL in this work is represented as

<!-- formula-not-decoded -->

where Ω is the branch perimeter, L its length, U the global heat transfer coefficient and T ∞ is a fixed know temperature (i.e. the rock temperature in a tunnel bore). The global heat transfer coefficient can be computed by using well know heat transfer correlations [68]:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where h is the convective heat transfer coefficient and R is the global thermal resistance of rock and tunnel lining. Equation (31) is based on the applicability of the Reynolds analogy (valid for Prandlt number equal to 1) to air (Prandtl number around 0.7).

More  care  is  required  when  estimating  the  summation  on  the  LHS  of  equation  (28) since  temperature  values  are  not  defined  in  branches  but  in  nodes.  Therefore,  the estimation of the temperature at the boundary of the control volume has been performed by using a first order upwind scheme [66].

## 2.3.5. Time dependent problem

In  time  dependent  problems,  the  time  derivative  of  equations  (18)  and  (20)  must  be retained.  Furthermore  the  finite  volume  integration  over  the  control  volume  must  be augmented with a further integration over a finite time step ∆ t. This procedure leads to

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The terms at the LHS of equation (32), under the hypothesis that the variable under the time derivative (i.e. density, velocity and temperature) prevails over the whole control volumes, lead to

<!-- formula-not-decoded -->

where i V ∆ and j V ∆ are the volumes of integration and Lj is the length of the branch. The evaluation of the rest of the terms contained in (32) requires an assumption on the time evolution  of  the  quantities  contained  in  the  time  integrals.  In  this  work  an  implicit formulation has been adopted; this means that such quantities are the ones of the next time level. This approach is first order accurate but unconditionally stable for any time step size [70]. After performing the double integration and after some rearrangements, equations (33) can be rewritten in the final fashion

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Also for the time dependent formulation, a first order upwind scheme has been adopted to treat the convective fluxes in equations (34)

## 2.3.6. Solving algorithm

In both steady state and transient approaches, the continuity and momentum equations can be solved by using an iterative solution strategy known as the SIMPLE algorithm [71]. The method, based on a 'guess and correct' procedure has been rearranged in order to improve its applicability for complex mono-dimensional networks. The procedure is presented  hereafter  for  the  unsteady  formulation  of  the  problem  but  can  be  directly applied  for  steady  state  problems.  For  sake  of  simplicity  the  number  of  nodes  and branches in the network will be indicated as nn and nb respectively.

The whole set of continuity equations can be rearranged by using the incidence matrix A ( nn × nb ) as follow

<!-- formula-not-decoded -->

where M is a ( nb × nb ) matrix containing the product j j A ρ on the principal diagonal and b is vector containing the term at the LHS of equation (34).a which are treated explicitly during the iteration procedure.

Analogously, the complete set of momentum equations (34).b can be expressed as

<!-- formula-not-decoded -->

where Y is  a  ( nb × nb )  matrix  containing the term                 + + ∆ j j j j h j j t j j j u D L f t u L ρ β ρ , 2 1 on

the  principal  diagonal  and t is  a  vector  containing  the  rest  of  the  terms  contained  in equation (34).b. In particular the pressure gains due to the piston effect or fan action are treated explicitly by the model.

The  iterative  procedure  starts  by  guessing  a  pressure  field P* which  allows  for  the calculation of a guessed flow field u* by a rearranged version of equation (36)

<!-- formula-not-decoded -->

After defining pressure and velocity correction vectors u' and P' (see equation (38))

<!-- formula-not-decoded -->

and  after  some  rearrangements  a  correlation  between  velocity  vector  and  pressure correction can be obtained. As for the original SIMPLE algorithm formulation, the term [ ] { } t Y 1 - - is  dropped  to  keep  the  iteration  procedure  simpler  [66],  leading  to  equation (39)

<!-- formula-not-decoded -->

By substituting equation (39) into equation (35) a final set of equations for the pressure correction is obtained.

<!-- formula-not-decoded -->

At  each  iteration  step,  equation  (40)  is  used  to  calculate  the  pressure  correction  to update pressure and flow fields. Obviously, in the nodes where the values of pressure or velocities are known (i.e. domain boudaries), the pressure or velocity corrections are set to zero.

The developed numerical algorithm requires an under-relaxation step in order to reach convergence.  In  particular  the  new  update  values  for  pressure  and  velocities  are calculated  by  means  of  relaxation  factors  that  can  provide  more  stable  computations. The  status  of  the  convergence  is  checked  by  monitoring  the  scaled  values  of  the residuals.

The main steps of the solution procedure of the 1D model are resumed as follows:

1. Guess a pressure field P*
2. Solve the momentum equations to obtain u* (equations (37))
3. Solve the pressure correction equations to calculate P' (equation (40))
4. Update pressures and velocities
5. Solve energy equations (34).c and update temperatures and densities
6. Iterate from step 2 to step 5 until convergence is reached.

## 2.3.7. Typical input parameters and boundary conditions

Given the substantial simplifications introduced in the 1D models (i.e. onedimensionality  of  the  fluid  pattern),  their  accuracy  mainly  rely  on  the  calibration constants and semi-empirical parameters contained in previous equations. Furthermore, the boundary conditions to be input into the model are known only with low accuracy given all the uncertainties related to the estimation or static pressure at the portals or at the chimneys, wind conditions and variability, fire load and HRR.

The pressure difference at the portals usually plays a negligible role for short tunnels (few  hundred  meters)  while  is  a  dominant  parameter  for  long  tunnels  under  relevant meteorological  barriers  (such  as  mountains).  The  evaluation  of  this  effect  to  input reliable  boundary  conditions  is  subject  to  long  term  measurements.  A  first  rough approximation (based on measurements carried out  on the tunnels Frejus, Mont Blanc and Lioran) is given in [72] and is presented hereafter

<!-- formula-not-decoded -->

where ∆ p is  the  barometric  pressure  difference  at  the  portals  in Pa, and ∆ z it  the difference  in  the  portal  altitude.  Nevertheless,  this  value  represents  only  a  statistic average and significantly higher pressure difference can be achieved.

As example, the pressure differences measured over a long term experimental campaign for the Mont Blanc tunnel are reported in Figure 13. It shows that while average statistic pressure is larger at the French portal, the largest pressure differences (up to 1000 Pa) are in the opposite direction. Therefore the whole ventilation system has to be set up to cope with such critical environment conditions. In the case of the Mont Blanc Tunnel after the refurbishment, the ventilation system is designed to counteract against pressure differences of ±750 Pa with 76 jet fans.

Figure 13: Meteorological pressure difference measured between the portals of Mont Blanc Tunnel [73]

<!-- image -->

Bar chart

Similar  arguments  can  be  given  when  including  the  wind  pressure  as  boundary condition.  The portal load due to the effect of the wind is proportional to the stagnation pressure as presented in equation (42)

<!-- formula-not-decoded -->

where ζ is a pressure loss coefficient at the portals (~0.6) and uw,por is the wind velocity at  the  average  portal  height.  If  the  wind  velocity  at  the  average  portal  height  is  not known,  it  can  be  scaled  by  using  standard  power  laws  to  take  into  account  the atmospheric boundary layer.

Another  key  parameter  is  represented  by  the  effective  tunnel  friction  coefficient f. Indeed,  it  takes  into  account  not  only  the  wall  roughness  but  it  must  include  the 'apparent roughness' induced by all the appliances and auxiliary facilities installed on the  tunnel  lining.  Typical  values  can  differ  significantly  from  the  standard  values measured for pipes. The tunnel friction coefficients can range between 0.1 and 0.3. An average value of 0.026, calculated on the basis of a statistical analysis of experimental measurements  for  a  longitudinally  ventilated  tunnel  with  horse-shoe  cross  section,  is provided in [62].

The  modelling  of  jet  fans  and  ventilation  devices  require  the  adoption  of  a  fan characteristic curve. In most of the cases the fan characteristics curves are completely unknown  or  not  well  defined  because  their  behaviour  is  strongly  dependent  on  their surroundings and their installation; distance from the ceiling, eccentricity, presence of niches etc. The values provided by the manufacturer are in fact measured in laboratory whose  environment  is  different  from  a  real  tunnel.  Usually,  in  situ  measurements  or further CFD analysis are required to adequately define their behaviour. Typical values of jet fan thrust range between 500 N and 1400 N while the nominal jet fans pressure rise coefficients ranges between 0.8 and 0.9. However, the latter values can be highly variable, especially if the fans are installed in niches. Indeed Jang and co-workers [62], on  the  basis  of  experimental  measurements  conducted  in  a  real  operating  tunnel, proposed a value of 0.56 significantly lower that the nominal values.

The evaluation of the piston effect is a complex task since it depends on a large set of ill-defined parameters  including, vehicle drag coefficients and  speed  and  traffic conditions.  Experimental  studies  [62]  assert  that  the  average  drag  coefficients  of  the small-sized vehicles and the large-sized vehicles fall in the ranges 0.32-0.35 and 0.360.4, respectively, when  the averaged traffic density in the tunnel is below 8 vehicles/lane/km and the vehicular tailgating effect is weak. However, as the averaged traffic density in the tunnel increases to 8-23 vehicles/lane/km during the morning rush hours,  the  averaged  drag  coefficients  of  the  small-sized  vehicles  and  the  large-sized vehicles would be reduced to 0.20 and 0.24.

Besides, a large set of semi-empirical correlations to model the hydraulic resistance in complex  intersections  between  galleries,  shafts  or  large  obstructions  can  be  found  in [75]

The estimation of the heat generation due to fire is a complex process and 1D models cannot  provide  any  accurate  result.  Therefore,  data  on  the  fire  growth  curve  are required.  They  can  be  derived  from  available  experimental  data  or  from  design prescriptions.  Alternatively  the  same  approach  as  presented  by  Carvel  in  [4]  or  by Ingason and co-workers can be adopted [74]. The former has been vastly described in the  first  chapter  of  this  work.  The  latter  consist  of  a  parabolic  growth  followed  by  a constant heat flux over a period of time and an exponential decrease:

<!-- formula-not-decoded -->

This  expression  depends  on  parameters α and β ,  which  values  are  suggested  for  fast fires (buses: α =0.1 kW/s 2 ; β =0.0007 s -1 ) and medium fires (cars: α =0.01 kW/s 2 ; β =0.001 s -1 ). Time t 2 is calculated on the basis of the total energy released.

## 2.4. A case study: the Frejus Tunnel

The developed 1D model has been used to simulate the behaviour of the Frejus tunnel and the installed ventilation system. The analysis aims at defining ventilation strategies to be used in case of fire and illustrates the approach.

The  Frejus  tunnel  is  a  two-way  link  between  Italy  and  France  with  a  total  length  of 12870 m. A schematic of the typical Frejus tunnel cross section and ventilation system is  presented in Figure 14. The hydraulic diameter of the semicircular sections is 6 m. Ventilation is fully transversal. Figure 14 depicts 6 groups of fresh air fans (AF) and the six groups of extraction fans (AV). The French portal is located on the left side (x=0 m) while  the  Italian  on  the  right  side  (x=12870  m).  Ordinary  ventilation  is  operated  by introducing fresh air along the tunnel through 3 U-shaped fresh air ducts which have 2 fans at each end. Fresh air openings are installed each 5 m. Emergency ventilation is operated  using  the  fresh  air  ducts  and  the  3  U-shaped  extraction  ducts  connected  to extraction dumpers installed each about 130 m.

The Frejus tunnel ventilation system is operated in order to create a stagnation point as close  as  possible  to  the  fire  position  with  positive  velocity  upstream  the  fire  and negative  velocity  downstream  the  fire.  In  this  scenario  the  smoke  does  not  tend  to propagate along the tunnel but is extracted close to the section where it is generated.

Figure 14: Frejus tunnel: top) cross section; down) Schematic of the ventilation system layout

<!-- image -->

Engineering drawing

The most effective  strategy  to  be  applied  in  case  of  fire  depends  on  the  fire  location along the tunnel and the pressure difference between the two portals.

The pressure difference, assumed to be positive when inducing the air flowing from the French  towards  the  Italian  portal,  can  reach  values  of  several  hundreds  Pascals,  as typical for long tunnels across the Alps. Furthermore, given a certain positive pressure difference  across  the  portals,  the  ventilation  scenario  to  be  adopted  depends  on  the location of the fire.

If  the  fire  takes  place  in  the  first  tunnel  portion  (between  the  French  portal  and  the tunnel  central  section),  10  extraction  dumpers  over  the  fire  (5  upstream  and  5 downstream)  are  opened.  In  addition,  if  the  pressure  difference  is  large,  fresh  air  is supplied  downstream  of  the  fire  to  enhance  smoke  confinement (opposite  supply strategy) . Some fresh air is also supplied all along the tunnel mainly in order to prevent from smoke propagation in the fresh air ducts, which may be used as escape route.

If  the  fire  takes  place  in  the  last  portion  (between  the  tunnel  central  section  and  the Italian portal), a proper air extraction in the first portion of the tunnel is used to oppose the  effect  of  pressure  difference  between  the  portals (opposite  extraction  strategy). Similar strategies are also defined for negative pressure difference.

In order to implement these conceptual strategies it is necessary to provide the operators with proper guidelines in the form of tables or algorithms relating pressure difference and  fire  position  to  the  extraction  dumpers  to  be  opened  and  to  the  settings  of  each group  of  fans.  This  information  is  obtained  through  multiple  numerical  simulations, performed using the 1D approach. However, the model must be calibrated and validated against experimental data before being used as reliable simulation tool.

Figure 15: Schematic of the network used for the 1D calculation corresponding to the tunnel region between section T2 and T3 of Figure 14.

<!-- image -->

Engineering drawing

Two examples of validation for the developed code on specific ventilation scenarios are presented  hereafter.  The  global  network,  built  for  the  purpose,  is  composed  by  650 branches and 450 nodes. A schematic is presented in Figure 15.

The volumetric flow rates of the axial fans at full charge range between 222÷257 m 3 /s and  117÷124  m 3 /s  for  supply  and  extraction  units,  respectively.  The  tunnel  friction coefficient has been established on the basis of experimental measurements to be around 0.017.

A first comparison between numerical predictions and experimental data is relative to a steady  state  scenario  with  only  the  supply  fans  operating  at  30%  of  full  charge.  The pressure  difference  across  the  Frejus  tunnel  during  the  test  was  negligible.  This  is confirmed  by  the  computed  and  experimental  velocity  profiles  which  are  almost specular with respect to the tunnel central section (see Figure 16). An accurate match between numerical and experimental prediction has been achieved.

Figure 16: Velocity distribution computed with the developed 1D model and comparison to experimental data recorded in the Frejus tunnel. Longitudinal velocity as function of the tunnel length

<!-- image -->

Line chart

A  second  validation  has  been  performed  for  an  emergency  ventilation  scenario including  a  small  8MW  fire  source  located  in  the  tunnel  portion  indicated  as T3 (see Figure  14) . Given  the  high  pressure  difference  across  the  portals  (1000  Pa)  and  the location of the fire, an opposite supply ventilation strategy has been adopted. It consists of a localized extraction over the fire zone as well as an enhanced fresh air supply in the fire downstream region. The fans are supposed to be started at t=0 .

Computed horizontal velocity profiles established along the tunnel and measured data are  compared  in  Figure  17.  An  overall  good  agreement  is  obtained.  The  1D  model predicts well the overall flow behaviour of tunnel ventilation system.

Figure 17: Velocity distribution computed with the developed 1D model and comparison to experimental data recorded in the Frejus tunnel. Longitudinal velocity as function of the tunnel length at 4 different times

<!-- image -->

Line chart

## 2.5. Concluding remarks

The results obtained by 1D models can be used to assess whether the overall ventilation conditions  are  acceptable  for  the  fire  safety  strategies.  In  the  case  of  transversally ventilated  tunnels,  this  can  be  made  by  determining  the  presence  of  a  cross  section where  flow  is  stagnant,  as  close  as  possible  to  the  fire.  In  the  case  of  longitudinally ventilated tunnel 1D models can be used to assess whether or not the tunnel ventilation system  is  able  to  guarantee  super-critical  ventilation  velocity  in  the  fire  zone  and therefore avoid back-layering.

However, they are unsuitable to simulate the fluid behaviour in regions characterized by high temperature or velocity gradients typically encountered in the vicinity of the fire plume,  ventilation  devices  of  complex  interconnections  of  galleries.  In  order  to  deal with  such  complex  flow  conditions  they  mainly  rely  on  empirical  correlation  or calibration  constants  to  be  defined  on  the  basis  of  experimental  measurements  or detailed calculations.

Parts  of  this  work  have  been  published  in Building  and  Environment  [102] and Fire Technology  [105]. A  chapter  titled One  Dimensional  and  Multi-scale  Modelling  of Tunnel Ventilation and Fires is based on the work presented here and will be published in next edition of The Handbook of Tunnel Fire Safety [104] .

## 3.1. Introduction

In  the  last  two  decades  the  application  of  CFD  as  fire  safety  engineering  tool  has become  widespread.  This  tendency  has  reached  also  tunnel  applications  where  CFD calculations are now part of many designs, assessments and investigations.

CFD simulations require the solution of the complete set partial differential equations asserting  the  conservation  of  mass,  momentum  and  energy.  Such  set  of  equations  is solved  numerically  leading  to  detailed  predictions  of  velocity  and  temperature  fields, species concentration, heat fluxes mapping and so forth. The calculations are performed by enforcing the conservation laws on a high number of control volumes generated by a numerical discretization of the computational domain.

Severe limitations to the full numerical solution of the governing equations are induced by the impossibility of resolving the whole range of spatial and time scales involved in the  turbulent  flows  associated  with  any  ventilation  or  fire  scenarios  in  tunnels.  This problem has been tackled by modifying the governing equations in order to model the

## 3 CFD modelling

unresolvable turbulent transport phenomena. Typically, two main approaches have been used: the first one is based on a time-averaging of the Navier-Stokes equations (RANS) while the second one uses spatial averaging by means of specific filter functions. Such technique for turbulence modelling is known as Large Eddy Simulation (LES).

Besides to the uncertainty related to the modelling  of turbulence, considerable difficulties  are  also  introduced  by  the  description  of  turbulent  combustion  chemistry, buoyancy, radiation heat transfer and burning of condensed-phase fuels. Great uncertainty, especially when dealing with tunnel fire and ventilation scenarios, is also expected at the definition of the boundary conditions due to the unknown meteorological  conditions  at  the  portals,  actual  fire  load,  effective  lining  roughness, presence of vehicles and obstructions, etc.

Further  complexity  is  introduced  by  the  numerical  solution  of  the  final  set  of  partial differential  equations where the choice of the numerical schemes and the accuracy of the grid influence strongly the quality of the CFD solution.

Nowadays, computational fluid dynamics (CFD) can be considered as a mature tool to predict the overall flow behaviour due to ventilation devices, large obstructions or fire as well as to predict smoke spread in enclosure. However, more complex issues related to flame spread, soot formation, oxygen vitiation and combustion modelling are far by being solved, and they will not be satisfactorily addressed in the next decades.

Given all these complexities, any CFD  analysis requires two additional steps, verification and validation, in order to judge the appropriateness of its use and the level of confidence of its predictions [76]. Verification is a process to check the correctness of the solution of the governing equations. Validation is a process to check the appropriateness of the governing equations as model of the physical phenomena under investigation. Usually validation is made by comparing the model against experimental data. In this case, the differences that cannot be explained in terms of numerical issues, are attributed to uncorrected hypothesis and simplification introduced when building the governing equations.

There are a number of institutions dedicating a great effort in developing CFD tools for specific  fire  modelling  purposes.  A  recent  survey  identified  at  least  a  dozen  of  CFD model for fire modelling including JASMINE from the Fire Research Station (UK), Fire Dynamic  Simulator (FDS) from  NIST  (US),  SMARTFIRE  from  University  of Greenwich  (UK)  and  SOFIE  from  a  European  Consortium  [77].  Among  the  general purpose  CFD  codes  used  for  simulation  fire  scenarios,  the  authors  enumerate  CFX, Flow3D,  STAR-CD  and  Fluent.  This  work  uses  Fluent  as  CFD  tool  for  simulating tunnel ventilation flows and fires.

## 3.2. Literature overview

The  issue  of  CFD  modelling  of  fire  phenomena  is  too  wide  to  be  treated  is  a  single literature overview. Several books and literature review papers on the subject have been published in the last decades, and the interested reader is referred to them [78-80]. In this  section  only  the  archival  papers  direct  referring  to  the  CFD  modelling  of  tunnel ventilation flows and fires will be reviewed.

The  first  significant  contribution  on  the  subject  is  dated  1994  and  was  presented  by Fletcher and co-workers [81]. The paper presents a comparison between numerical and experimental data recorded in a 120 m long tunnel (cross section ~ 13 m 2 ). The authors used a kε turbulence  model  and  a  mixture  fraction  model  for  combustion.  Radiation heat transfer has been implemented by using a discrete transfer radiation model. A pool fire, whose size was estimated ranging between 2 MW and 2.4 MW was located in the middle of the tunnel. Three different ventilation velocity scenarios have been analysed (0.5 m/s, 0.85 m/s and 2 m/s). A qualitative good match between predicted and recorded temperature has been found with error ranging between 40÷100% in the vicinity of the flame  and  around  40%  in  the  far  field.  The  authors  recorded  that  the  addition  of  the turbulence production due to buoyancy was crucial to predict smoke stratification while soot production had a very little impact.

A comprehensive study has been presented by Woodburn and Britter in 1996 [82] and [83]. The study was performed by using a commercial CFD package Flow-3D and aims at predicting temperature and flow fields in a 360 m long tunnel under a 2.7 MW fire scenario.  A  kε turbulence  model  was  implemented  together  with  an  eddy  break-up model for combustion. Radiation heat transfer was not included. The authors assessed the  sensitivity  of  the  results  to  several  unknown  parameters  including  wall  friction coefficient, turbulence model,  tunnel slope and  so forth. They  highlighted that maximum  temperature,  velocity  profile  and  global  heat  transfer  were  significantly dependent on the input parameters; maximum temperatures showed variation within a 60%  range  of  base  case  scenario,  velocity  profile  up  to  30%  and  convective  heat transfer  up  to  45%.  Temperatures  were  generally  over-predicted  showing  deviation from  measured  values  ranging  between  260%  in  the  vicinity  of  fire  source  and 200÷400% in the downstream area.

Only a qualitative assessment of temperature and velocity fields has been developed by Chow by using the commercial CFD package Phoenix [84]. The CFD model has been applied to a 20 m long tunnel (25 m 2 cross section) under a 5 MW and a 40 MW fire source.  Fire  has  been  modelled  as  source  of  heat  and  smoke  without  a  dedicated combustion model.

A detailed analysis of CFD capabilities has been presented by Wu and Bakar (2000) [33]. The contribution presents a numerical analysis of two fire scenarios (1.4 kW and 28 kW) in 10.4 m long small scale tunnel. The corresponding full scale fires, using the canonical scaling laws presented in chapter 1, would range between 2.5 and 50 MW. The  numerical  model  has  been  developed  by  using  the  commercial  CFD  package FLUENT adopting a standard kε model  with  buoyancy  modifications  for  turbulence and  a  mixture  fraction  model  for  combustion.  Radiation  heat  transfer  has  not  been accounted  for.  The  comparison  to  experimental  data  shows  that  the  CFD  model underpredicts  the  critical  velocity  by  20%  as  maximum.  The  comparison  to  detailed velocity field data shows a qualitative agreement to the experimental data but typically, higher  deviations  are  recorded:  velocity  profiles  in  the  back-layering  region  close  to ceiling are slightly underpredicted (~12%), while deviations up to 100% are recorded in the  velocity  profiles  located  underneath  the  back-layering  nose.  Temperatures  are significantly over-predicted and do not show  any  qualitative agreement  to the experimental findings with deviation up to 500% recorded 30 cm downstream the fire source.  The  authors  asserted  that  temperature  overprediction  is  mainly  due  to  the hypothesis  of  fast  chemistry  embedded  in  the  mixture  fraction  model  adopted  for combustion which overestimates the reaction rate.

Similar level of accuracy has been reached in the contribution by Karki and Patankar (2000) [85]. The numerical model has been developed by using the commercial CFD package COMPACT-3D adopting a standard kε model including buoyancy modifications for turbulence. The fire has been modelled as source of heat and smoke without  any  dedicated  combustion  model.  Radiation  heat  transfer has not  been modelled.  This  contribution  has  the  merit  of  including  the  ventilation  devices  in  the computational domain performing the simulation of the whole system. In particular the jet fans have been modelled as combination of sources and sink with the volume within the  fan  region  treated  as  a  solid.  The  numerical  findings  have  been  validated  against experimental data recorded during the MTFVTP [11] test 606A (10MW pool fire) and 615B (100MW pool fire). After calibrating the CFD model on the basis of cold flow scenarios, good  bulk  flow  predictions could  be achieved  at  ambient  conditions (deviation within 7%). Predicted bulk flow data resulted in good agreement also for the simulated fire scenarios bur show larger deviations (within 30%). Predicted flow field data  show  an  overall  agreement  with  the  experimental  findings;  an  average  20% deviation  for  temperature  and  velocity  profiles  could  be  achieved  when  simulating scenario 606. The CFD simulation of test 615B showed higher deviations, up to 50% and 30% for temperature and velocity profiles, respectively.

Jojo and co-workers adopted the CFD open source package FDS to simulate a 100 m long tunnel (35 m 2 cross section) under two different fire hazards (0.5 MW and 50 MW) [26]. The CFD tool adopts a LES model for turbulence and mixture fraction model for combustion. Several configurations of the ventilation system (i.e. longitudinal, transversal, semi-transversal and hybrid) have been considered. Since experimental data were not available, the  CFD predictions have been compared to classical correlations for predicting critical velocity and average temperature which are generally overpredicted (deviations ranging between 30% and 100%).

Both the kε and LES turbulence models have been adopted in the contribution by Gao and  co-workers  (2004)  [86].  The  work  uses  the  same  experimental  set-up  and  data adopted by Fletcher and co-workers one decade before [81]. In general the authors find a  good  agreement  when  analysing  the  plume  inclination  angle  with  errors  ranging between  10%  and  30%.  Overall  flow  behaviour  could  be  accurately  predicted  (i.e. occurrence of back-layering) but local temperature fields were over-predicted by up to 250%.

A qualitative contribution has been presented by Bari and Naser (2005) [87]. The work addresses the spread of fire effluents within a longitudinally ventilated tunnel 1.6 km in length. The fire represented by a burning bus, was supposed to grow up to a HRR of around 44 MW in 10 s and to extinguish in 4 min. The fire was modelled as source of heat a smoke without dedicated combustion model. Besides the unrealistic design fire, the  results  were  not  corroborated  by  experimental  measurements  as  well  as  no information about the smoke production modelling was provided.

More  detailed  descriptions  of  the  CFD  modelling  procedure  has  been  provided  by Hwang and Edwards (2005) [37]. The authors adopted the open source CFD package FDS to simulate flow and temperature fields within two different tunnels. The first was a 4.9 m long (0.12 m 2 cross section) small scale tunnel including a 3.3 kW fire. The full scale  experimental  data  were  taken  from  the  MTFVTP  [11]  and  were  relative  to  a 50MW fire  under  longitudinal  ventilation  conditions.  The  authors  reported  a  general good  agreement  between  predicted  and  experimental  critical  velocity  for  both  the tunnels.  Detailed  flow  field  data  show  a  satisfactory  qualitative  and  quantitative agreement between experimental and numerical data for the small scale tunnel in the downstream region. In the upstream region velocities are overpredicted by up to 100%. The full scale simulations show a qualitative agreement to the experiments but higher deviations (up to 200%) are recorded.

Lee and Ryou (2006) used FDS to predict temperature and flow fields in a small scale tunnel having difference aspect ratio and fire sources ranging between 2 kW and 12 kW [88]. The  experimental  data  were  provided  in  [33]. An  overall qualitative  and quantitative  agreement  was  reached  when  computing  the  critical  velocity  and  backlayering  distance.  Temperature  distribution  under  the  ceiling  was  calculated  within  a 10% deviation from the experimental findings.

Same CFD tool was adopted by McGrattan and Hamins (2006) to perform a simulation of  the  Howard  Street  tunnel  fire  (2.65  km  long)  involving  a  60  cars  freight  train powered  by  three  locomotives  [89].  The  CFD  tool  was  used  to  simulate  natural ventilation  scenarios  involving  fires  ranging  between  20MW  and  50MW.  The  work provides only qualitative considerations on the peak temperatures and oxygen concentration  in  the  tunnel  without  any  corroboration  from  experimental  data  or canonical correlations.

The commercial CFD tool FLUENT was used by Ballesteros-Tajadura et al. to simulate velocity  and  temperature  fields  within  a  real  1.5  km  long  tunnel  under  a  30MW  fire scenario  [90].  Time  dependent  simulations  have  been  conducted  in  order  to  predict smoke spread in the domain but the final results were not validated against experimental data.  Furthermore,  the  adopted  mesh  density  (~162  cells/m)  was  largely  under  the minimum required to  achieve  accurate  field  predictions.  The  effect  of  the  ventilation system was taken into account by introducing a pressure difference across the tunnel domain which was previously computed on the basis of cold flow simulations.

The CFD package FLUENT was also used by Vauquelin and Wu (2006) to predict the effect of the tunnel width on the critical velocity [30]. The CFD data were corroborated against  small  scale  experimental  data  provided  in  [33].  Turbulence  was  addressed  by using  a  kε turbulence  model  with  buoyancy  modification  while  combustion  was implemented by using a mixture fraction model. The authors confirmed that the model was able to predict critical velocity with an uncertainty ranging between 5% and 14%. No conclusions on the accuracy of the predicted flow fields have been given.

Lin  and  Chuah  performed  a  qualitative  analysis  on  the  effectiveness  of  different extraction  strategies  in  a  semi-transverse  ventilated  tunnel  by  using  FDS.  The  tunnel considered for the case study  was 4 km long (~50 m 2 cross  section)  while  the  fire  is supposed to have a 100 MW peak HRR [91]. No comparisons to experimental data are provided.

The same numerical tool has been used by Jae Seong Roh et al. to simulate temperature and flow fields within a 10 m long small scale tunnel (~0.14 m 2 cross section)  [92]. The average fire size ranged between 2 kW and approximately 13 kW. The numerical model has been validated against temperature measurements recorded along the tunnel ceiling. The predicted temperature values deviated from the experimental findings as maximum as 20% for a 5 kW fire and 90% for a 13 kW fire.

A hypothetic fire outbreak in the Louis-Hippolyte-Lafontaine tunnel under a river in the Montreal area represented the test case for the work by Abanto and co-workers (2006) [93].  The  simulations  have  been  conducted  by  using  the  commercial  CFD  package FLUENT and an in-house CFD code. The fire has been modelled as a volumetric heat source while a un-specified combustion model has been used for the second run. In both the  cases  a  kε turbulence  model  has  been  adopted.  The  authors  provide  only qualitative results and most of them are questionable (e.g. temperature higher than 3000 K in certain domain regions). No comparison to experimental data has been provided.

A more comprehensive validation of FDS has been performed by Kim and co-workers (2007)  [94].  The  authors  performed  a  detailed  sensitivity  study  to  several  modelling parameters (i.e. Smagorisky constant, turbulent Prandlt number, Schmidt number, grid size)  and  included  a  systematic  comparison  to  experimental  findings  from  a  100MW fire test performed during the MTFVTP [11]. More detailed analyses were performed to refine the smoke layer predictions but without much success. The authors showed that FDS  produces  predictions  that  are  in  qualitative  agreement  with  the  actual  fire phenomena in the near-fire  and  downstream  region:  simulated  temperatures  and  flow velocities showing an error distribution of approximately +56% to +37%, and ±91%  to ±30%,  respectively.  For  the  upstream  region  of  the tunnel,  FDS  shows  serious limitations  in  predicting  the  smoke  layer  near  the  ceiling.  Some  inconsistencies  were also reported when trying to reproduce transient ventilation scenarios with FDS.

The MTFVTP was the source of experimental data also for Galdo-Vega and co-workers (2007) [95]. In particular 3 different ventilation scenarios involving 10MW and 50MW fires have been modelled. The whole computational domain was meshed including the ventilation devices (jet fans) modelled as source and sinks of mass. The mesh density adopted for the calculation (117 cells/m) is by far under the minimum requirements for accurate  predictions.  The  fire  has  been  modelled  as  source  of  heat  and  smoke  while turbulence  has  been  addressed  by  using  a  kε turbulence  model  with  buoyancy modifications. Nonetheless, the authors showed an overall agreement between numerical predictions and experimental data confirming that simplified fire modelling approaches  lead  to  accurate  predictions  of  the  global  ventilation  system  behaviour. However, higher deviations are expected in the vicinity of the fire.

A small scale experimental and numerical study has been presented by Rusch and coworkers (2008) [96]. The small scale experiments were performed in a 10 m long tunnel (0.64 m 2 cross section) including a buoyant hot jet released in cross flow. Velocity and temperature were recorded by using thermocouples and laser doppler anemometry. The numerical  predictions  were  performed  by  using  the  CFD  commercial  package  CFX. Turbulence was addressed by using several models including kε turbulence model with buoyancy modifications, kω ,  kω SST, and RSM. Steady simulations showed that all the previous models tend to overpredict temperature under the ceiling since unable to predict the entrainment of cold air from the cross-flow into the hot jet. The reason for the  failure  was  found  to  be  the  inability  of  the  models  to  solve  un-isotropic  vortical structures  in  steady  simulations.  Unsteady  simulations  showed  a  tiny  improvement  in the  temperature  predictions;  better  accuracy  could  be  achieved  when  adopting  a  DES (Detached Eddy Simulations) turbulence model. The authors asserted that an accurate wall treatment and well resolved large scale vortical structures are required to improve CFD predictions.

A comparison between LES and kε turbulence models for critical velocity prediction has been presented by Van Maele and Merci (2008) [97]. The kε turbulence model has been implemented in the commercial CFD package FLUENT. Radiation heat transfer was not considered while combustion was addressed by using a mixture fraction model. The LES calculations are performed by using the CFD tool FDS. Experimental data are provided by Wu and Bakar (2000) [33] for a 15 long tunnel (0.0625 m 2 cross section) under a 3 kW and a 30 kW fire scenario. The authors showed that both the modelling approaches are able to provide good predictions of the critical velocity with deviations ranging  between  20%  to  38%  and  31%  to  8%  for  kε and  LES  turbulence  model, respectively. Flow and temperature fields are no validated against experimental data.

Some  data  on  the  back-layering  occurrence  in  a  1.8  km  long  operative  tunnel  are presented  by  Kashef  and  Benichou  (2008)  [98].  The  tunnel  is  equipped  with  a  semitransverse ventilation system which is supposed to cope with a 20 MW fire scenario. The model, developed with FDS, is validated against data recorded during some tests involving  a  2  MW  fire.  Generally,  the  authors  find  a  good  agreement  between experimental and numerical findings but the extrapolation of the model up to fire sizes 10 times larger is questionable.

A qualitative analysis on the capabilities of CFD and zone models is presented by Jain and  co-workers  [99].  The  CFD  and  zone  model  calculations  are  performed  by  using CFX and CFAST respectively. A 150 m long tunnel (80 m 2 cross section) represents the test case. The numerical predictions are not compared to experimental data.

In a recent work FDS has been used to predict the fire growth, temperature and velocity fields established during the Runehamar fire test 1 characterized by a peak release rate around  200MW  [8,100].  The  authors  performed  several  attempts  to  reproduce  the measured fire growth by tuning the model parameters including fire load geometry, grid size  and  domain  size.  Following  this  approach,  which  is  fundamentally  questionable, the authors were able to reproduce the actual fire growth within an acceptable degree of accuracy. However, their conclusion are case dependent and cannot be generalized to any other tunnel, fire load, geometry of the fire source and ventilation velocities.

Nmira and co-workers (2009) performed a CFD analysis of a thermoplastic tunnel fire under a water mist mitigation agent (i.e. water mist) [101]. The CFD model uses a kε turbulence model, an Eddy-break-up-Arrhenius model for turbulent combustion and a multiphase  radiative  transfer  equation  including  the  contribution  of  soot,  combustion products  and  water  droplets.  A  dedicated  pyrolysis  model  for  PMMA  was  also introduced in order to calculate the time evolution of combustible gases released into the tunnel environment. The model was applied to simulate the behaviour of a PMMA fire in a 25 m long tunnel (3×5 m 2 cross section). A large set of CFD data have been presented but none of them has been corroborated by experimental measurements.

Table  7  summarizes  the  main  characteristics  of  the  tunnel  fire  related  CFD  studies discussed in the literature review.

CFD models of tunnel fires have been shown to predict critical ventilation velocity, and back layering distance  within an acceptable level of  accuracy (deviation smaller than 30%).  The  overall  flow  data  (i.e.  bulk  velocity  and  temperature)  are  also  accurately predicted with deviations from experimental values typically within 20%. The literature study, including the main reference paper of the last 25 years, shows that prediction of local flow field data (i.e. velocity and temperature fields), especially if calculated in the vicinity of the fire source, can be affected by error higher than 100% when compared to experimental measurements.

It has been shown that CFD analysis of fire phenomena within tunnels suffers from the limitations set by the size of the computational domains. The high aspect ratio between longitudinal  and  transversal  length  scales  leads  to  very  large  meshes.  The  number  of grid points escalates with  the  tunnel  length  and  often  becomes  impractical  for engineering purposes, even for short tunnels less than 500 m long. An assessment of the mesh  requirements  for  tunnel  flows  is  made  by  Colella  et  al.  [102,105]  for  active ventilation  devices  and  for  fire-induced  flows.  Grid  independent  solutions  could  be achieved only for mesh density larger that 4000 cells/m and 2500 cells/m for ventilation and fire induced flows, respectively.

The high computational cost leads to the practical problem that arises when the CFD model has to consider the boundary conditions or flow characteristics in locations far away from the region of interest. This is the case of tunnel portals, ventilation stations or jet fan series located long distances away from the fire. In these cases, even if only a limited region of the tunnel has to be investigated (i.e. to simulate the fire) an accurate solution of the flow movement requires that the numerical model includes all the active ventilation  devices  and  the  whole  tunnel  layout.  For  typical  tunnels,  this  could  mean that the computational domain is several kilometres long.

This limitation is the reason why only a limited number of CFD studies directly focus on the performance of tunnel ventilation systems.  In most of the  works  reviewed the computational domain is limited to a small region close to the fire and the ventilation velocity at the domain boundaries is considered to be known (i.e. estimated with crude correlations or determined by cold flow ventilation tests). Obviously, if the performances  of  a  ventilation  system  have  to  be  assessed,  this  kind  of  approach  is completely useless because it produces a de-coupling between ventilation system and fire.

| Reference                           | Domain size [m]   | fire size        | Small scale   | ventilation devices   | Code         | Turbulence   | Combustion             | Validation   | note                                                                                                                                                      |
|-------------------------------------|-------------------|------------------|---------------|-----------------------|--------------|--------------|------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fletcher et al. (1994)              | 90                | 2 and 2.4 MW     | -             | -                     | Furnace      | k- ε         | Mixture fraction       | √            | Octane pool fires were used in the experiments                                                                                                            |
| Woodburn et al. (1996)              | 366               | 2.3 MW           | -             | -                     | FLOW 3D      | k- ε         | Eddy break-Up          | √            | The combustion model is used when modelling the fire area (40 m).                                                                                         |
| Chow (1998)                         | 20                | 5 and 40 MW      | -             | -                     | PHOENIX      | N.A.         | N.A.                   | -            | Only qualitative observations are given                                                                                                                   |
| Wu et al. (2000)                    | 8.1               | 3 to 45 kW       | √             | -                     | Fluent       | k- ε         | Mixture fraction       | √            | Different tunnel cross section investigated                                                                                                               |
| Karki et al. (2000)                 | 850               | 10 MW and 100 MW | -             | √                     | COMPACT - 3D | k- ε         | Volumetric heat source | √            | Also cold flow scenarios are simulated                                                                                                                    |
| Jojo el al. (2003)                  | 100 m             | 0.5 to 50 MW     | -             | -                     | FDS          | LES          | Mixture fraction       | -            | Different ventilation systems are analysed                                                                                                                |
| Gao et al. (2004)                   | 90                | 2 and 2.4 MW     | √             | -                     | N.A.         | LES          | Volumetric heat source | √            | A comparison to k- ε turbulence model results is provided                                                                                                 |
| Bari et al. (2005)                  | 1600              | 44 MW            | -             | -                     | Fluent       | N.A.         | Volumetric heat source | -            | The fire behaviour is questionble and the smoke production parameters are unclear                                                                         |
| Hwang et al. (2005)                 | 4.9               | 1 to 100 kW      | √             | -                     | FDS          | LES          | Mixture fraction       | √            | Also large scale simulations are performed and validated against Memorial tunnel data. Large scale fire HRR up to 50 MW. Large scale tunnel length 853 m. |
| McGrattan et al. (2006)             | 2650              | 50 MW            | -             | -                     | FDS          | LES          | Mixture fraction       | -            | Only observation on the maximum temperature are given                                                                                                     |
| Ballestreros-Tajadura et al. (2006) | 1500              | 30 MW            | -             | -                     | Fluent       | k- ε         | Volumetric heat source | -            | The effect of the ventilation system is modelled as total pressure difference across the portals                                                          |
| Vauquelin et al. (2006)             | 8.1               | 15 kW            | √             | -                     | Fluent       | k- ε         | Mixture fraction       | √            | Different tunnel cross section investigated                                                                                                               |
| Lee et al. (2006)                   | 10.4              | 2.47 to 12.30kW  | √             | -                     | FDS          | LES          | Mixture fraction       | √            | Different tunnel cross section investigated                                                                                                               |
| Abanto et al. (2006)                | 1800              | N.A.             | -             | -                     | Fluent       | k- ε         | Volumetric heat source | -            | Fire model, fire sizes and are not clear. Qualitative description of the results are not given.                                                           |

Table 7: Summary of the published CFD studies related to tunnel fires discussed in the literature review.

| Reference                | Domain size [m]   | fire size      | Small scale   | ventilation devices   | Code       | Turbulence          | Combustion             | Validation   | note                                                                                                                                                      |
|--------------------------|-------------------|----------------|---------------|-----------------------|------------|---------------------|------------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Lin et al. (2007)        | 550               | 100MW          | -             | -                     | FDS        | LES                 | Mixture fraction       | -            | Only 550 m of tunnel have been simulated.The real tunnel length is 4000                                                                                   |
| Roh et al. (2007)        | 7                 | 2 to 13 kW     | √             | -                     | FDS        | LES                 | Mixture fraction       | √            | N-heptane pool fires are used in the experiments                                                                                                          |
| Galdo Vega et al. (2007) | 850               | 10 and 50 MW   | -             | √                     | Fluent     | k- ε                | Volumetric heat source | √            | Memorial tunnel fire tests are used as case studies                                                                                                       |
| Kim et al. (2007)        | 350               | 100 MW         | -             | -                     | FDS        | LES                 | Mixture fraction       | √            | Only 350 m of tunnel have been simulated.The real tunnel length is 850. Memorial tunnel data are used for the validation                                  |
| Jain et al. (2008)       | 150               | 9 MW           | -             | -                     | CFX/Cfast  | k- ε                | Volumetric heat source | -            | Only qualitative observations are given                                                                                                                   |
| Van Maele (2008)         | 8                 | 3 kW and 30 kW | √             | -                     | FDS/Fluent | LES and k- ε        | Mixture fraction       | √            | GGDH hypothesis used for k- ε modelling                                                                                                                   |
| Kashef et al. (2008)     | 1400              | 2 and 20 MW    | -             | -                     | FDS        | LES                 | Mixture fraction       | √            | The validation was conducted only for the 2 MW fire scenario                                                                                              |
| Rusch et al. (2008)      | 10                | N.A.           | √             | -                     | CFX        | k- ε /k- ω /RSM/DES | N.A.                   | √            | CFD simulations of a hot jet in cross flow conditions are presented                                                                                       |
| Cheong et al. (2009)     | 36 to 102         | up to 200 MW   | -             | -                     | FDS        | LES                 | Mixture fraction       | √            | The FDS model was calibrated agaist the Runehamar fire test experiments                                                                                   |
| Nmira et al. (2009)      | 25                | N.A.           | -             | -                     | N.A.       | k- ε                | Eddy break-Up          | -            | A pyrolysis model for PMMA was used to estimate the amount of combustible products generated. The interaction with a water mist agent is also considered. |

## 3.3. Governing equations

The  physics  of  fluid  flows  can  be  described  by  a  set  of  partial  differential  equations known  as  governing  equations  describing  the  conservation  of  mass,  momentum  and energy.  Each  of  these  can  be  derived  for  an  elemental  fluid  particle  having  volume dx·dy·dz .  An  interested  reader  can  refer  to  [66,70].  The  CFD  commercial  package FLUENT  [106],  used  in  this  work,  solves  the  mass  conservation  equation  in  the following form

<!-- formula-not-decoded -->

where ρ is  the  fluid  density  and u the  velocity  vector.  The  momentum  conservation equation states

<!-- formula-not-decoded -->

where p the  static  pressure, τ is  the  stress  tensor, g the  gravity  vector, and S a  vector containing the momentum source terms per unit volume. The stress tensor τ is given by

<!-- formula-not-decoded -->

where µ is the molecular viscosity, I the unit tensor while the second term on the RHS contains  the  effect  of  volume  dilation  which  is  typically  negligible  for  low  mach number flows.

FLUENT solves the energy equation in the following form

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where h is the  sensible  enthalpy, SE the  energy  source  term, keff the effective conductivity and τ eff is the global stress tensor including the Reynolds turbulent stresses. The  effective  conductivity keff can  be  obtained  by  summing  molecular  and  turbulent conductivity.

The equation of state for a fluid is used to relate the material properties to each other. By assuming thermodynamic equilibrium, pressure and internal energy are functions of density and temperature:

<!-- formula-not-decoded -->

For a perfect gas, for instance, the above equations are p= ρ RT and i=cvT+i0 where R is the specific gas constant, cv is the specific heat capacity at constant volume and i 0 is the reference internal energy.

In  the  solid  region  the  energy  transport  equation  solved  by  model  has  the  following form

<!-- formula-not-decoded -->

where h is the sensible enthalpy, k is the solid heat conductivity and SE is the volumetric heat source, and v is the velocity field eventually specified for the solid zone.

## 3.4. Turbulence modelling

Typical tunnel ventilation flows and fire induced flows are characterized by a turbulent regime in which the fluid velocities as well as other properties vary in a random and chaotic way.  The turbulent nature of the flow precludes any economical description of the motion of all the fluid parcels.

Typically,  the  description  of  turbulent  flows  can  be  addressed  by  decomposing  the instantaneous  fluid  velocity u(t) into  a  steady  mean  value U and  a  fluctuating component u'(t) . This approach, known as Reynolds decomposition, allows a turbulent flow  to  be  characterized  in  term  of  mean  value  properties (U,  V,  W,  P,  T) and  some statistical  properties  of  their  fluctuations (u',  v',  w',  p',  T') [66].  Visualization  of turbulent flows shows that, even if the mean velocity components or pressure vary in 1 or 2 dimensions, the turbulent fluctuations have always a three-dimensional character. In  practice,  turbulent  flows  are  characterised  by  trains  of  vortices,  also  called  eddies. Turbulent eddies take place over a continuous and wide spectrum of length scale; fluid parcel with are initially separated by a long distance can be brought closed by turbulent eddies motions.

Due to  the  convective  transport  of  eddies,  faster  moving  fluid  parcels  are  brought  in regions characterized by slower fluid motions and viceversa. This causes faster moving layer to be decelerated and slower moving layer to be accelerated inducing additional shear stresses in the fluid flow known as Reynolds stresses. Same conclusions could be drawn  when  analyzing  the  turbulent  transport  of  heat  or  species.  Due  to  turbulent transport,  heat,  mass  and  momentum  transfers  are  extremely  enhanced  in  turbulent flows. Effective mass, heat and momentum diffusion coefficients are therefore higher in turbulent flows than the correspondent laminar values.

Given the impact of turbulent transport phenomena in fluid dynamics and the fact that most of the industrial flows are turbulent, it is easy to understand the great effort done by  the  international  community  to  address  such  issues.  Indeed,  a  large  number  of different  turbulence  models  have  been  developed  but  there  is  no  universal  turbulence modelling approach which is suitable for all the CFD applications.

However, for most of the engineering purposes it is unnecessary to resolve the details of the  turbulent  fluctuations  since  the  information  provided  by  the  time  averaged  fluid properties  are  adequate.  Turbulence  models  for  Reynolds-averaged  Navier-Stokes equations (RANS) have been developed in this context.

The averaging of Navier-Stokes equations is performed under the assumption that the time averaged value of the fluctuating components of any fluid variable is zero. After substituting the decomposed variables into equations from (44) to (46), it can be easily shown  that  additional  terms  appear  in  the  RANS  equations  due  to  the  interactions between various turbulent fluctuations (see equations (50)).

<!-- formula-not-decoded -->

The  additional  terms,  containing  the  products  of  velocity  oscillating  components,  are commonly called Reynolds stresses and they have to be modelled to close the equations. Similar  transport  terms  will  arise  when  derivating  a  transport  equation  for  any  other scalar quantity; therefore a closure equation will be needed also for them.

A common closure method employs the Boussinesq hypothesis to model the Reynolds stresses which are related to the mean velocity gradients as shown in equation (51)

<!-- formula-not-decoded -->

where ( ) '2 '2 '2 2 1 w v u k + + = is defined as turbulent kinetic energy per unit mass and t µ is  the  turbulent  viscosity  .  The  Boussinesq  hypothesis  is  used  in  several  turbulence model  including,  kε ,  kω and  Spalart-Allmaras  models.  The  disadvantage  of  the Boussinesq hypothesis is that it assumes t µ to be an isotropic scalar quantity, which is not strictly true. Indeed, turbulence models based on such assumptions typically fail in situations where the anisotropy of turbulence has a dominant effect on the mean flow.

In  this  work  turbulence  modelling  has  been  addressed  by  using  the  standard kε turbulence  model  whose  first  version  was  developed  by  Lauder  and  Spalding  (1974) [107].  The  standard kε model  is  a  semi-empirical  model  based  on  the  transport equations for the turbulence kinetic energy (k) and its dissipation rate ( ε ). The transport equation for k is  derived from the exact equation, while the transport equation for ε is obtained  using  physical  reasoning  since  its  exact  transport  equation  contains  many unknowns and unmeasurable terms. Both of them are presented hereafter

<!-- formula-not-decoded -->

In the above equations, Gk represents the generation of turbulence kinetic energy due to the  mean  velocity  gradients, GB is  the  generation  of  turbulence  kinetic  energy  due  to buoyancy. C1 ε , C2 ε ,  and C3 ε are constants; σ k and σ ε are the turbulent Prandtl numbers for k and ε ,  respectively. Sk and S ε are  source  terms  for  turbulent  kinetic  energy  and dissipation rate.

The turbulent viscosity t µ is computed by combining k and ε as follows

<!-- formula-not-decoded -->

where µ C is a constant of the model.

The constants C1 ε , C2 ε , µ C , σ k and σ ε have the following default values determined from experiments with air and water for common flow conditions including shears flows and decaying isotropic grid turbulence:

<!-- formula-not-decoded -->

The constant C3 ε which determines how ε is affected by the buoyancy should be close to one for vertical buoyant shear layers and close to the zero for horizontal buoyant shear layers [108]. In order to make possible the use of a single expression for C3 ε Fluent uses the following relation

<!-- formula-not-decoded -->

where v is the component of the flow velocity parallel to the gravity vector and u is the perpendicular component [106].

The generation of turbulent kinetic energy due to the mean velocity gradients Gk can be computed as

<!-- formula-not-decoded -->

where S is the modulus of the mean rate-of-strain tensor, defined as

<!-- formula-not-decoded -->

The generation of turbulence due to buoyancy is computed by

<!-- formula-not-decoded -->

where β Is  the  coefficient  of  thermal  expansion. gi is  the  component  of  the  gravity vector in the i th direction, Prt is the turbulent Prandtl number by default assumed to be equal to 0.85. This approach is known as single gradient diffusion hypothesis (SGDH).

Once computed, turbulent kinetic  energy (k) and  turbulent  dissipation  rate ( ε ) can  be used to define velocity scale θ and length scale l which are representative of the large scale turbulence [66]

<!-- formula-not-decoded -->

The  Reynolds  stresses  can  be  computed  by  using  the  Boussinesq  approximation  (see equation (51).

As already pointed out in the previous literature review, the standard kε model  has been  used  and  largely  validated  by  the  scientific  community  to  simulate  fire  induced flows in tunnels. Several contributions assert that, if the model accounts for turbulence production  and  destruction  due  to  the  buoyancy  effects,  it  is  able  to  predict  with reasonable  accuracy  the  overall  behaviour  of  tunnel  fire  induced  flows    [30,33,8183,85,96,97]. Back-layering occurrence and back-layering distance are reasonably well predicted.

Some  limitations  of  the  kε turbulence  model  are  evident  when  modelling  highly anisotropic flow regions (i.e. the fire plume). Several works on the assessment of the kε model performance in this specific region are available in literature.

Nam and Bill (1993) noticed that the use of the standard kε model for simulating free plumes generates overpredictions in velocities and temperature at the central axis of the plume  underpredicting  the  vertical  spreading  rate  [109].  The  same  authors  tried  to correct  the  results  by  tuning  the  turbulent  viscosity  coefficient µ C and  the  effective Prandtl number reporting an agreement to experimental data within 2%.

Most of the uncertainties are related to the source term due to buoyancy in the transport equation  for ε which  is  poorly  understood.  Several  variants  for  determining  the coefficient C3 ε have been resumed in [108]. Some authors reported that the modification of such coefficient has only a marginal effect in the final solution when simulating free plumes. The latter could in fact achieve a 10% accuracy when comparing numerical and experimental  predictions  [110].  However  it  must  be  noted  that  the  grid  resolution adopted was significantly poor. Controversial aspects on the value to be adopted for C3 ε are also pointed out by [111].

Nevertheless,  it  is  well  known  that,  for  any  value  of C3 ε ,  the  kε model  tends  to underestimate vertical plume spread and to overestimate the spreading rate of horizontal ceiling layers [112]. Some improvements could be achieved by treating the buoyancy with  a  generalized  gradient  diffusion  hypothesis  (GGDH)  which  introduced  the transversal density gradients into the buoyancy production term [108].

Several  authors  have  tried  this  approach  and,  after  tuning  the  model  constants,  they could  improve  the  model  predictions.  However,  the  results  are  still  limited  given  the lack of general applicability of the tuned models. For instance, Merci and co-workers adopted a GGDH approach to predict the critical velocity in a small scale tunnel; the accuracy of the numerical predictions, when compared to experimental findings, ranged between 8% and 38% depending on the fire scenario which is comparable with standard kε turbulence modelling.

## 3.5. Boundary conditions

## 3.5.1. Pressure boundary conditions

Constant pressure boundary conditions are used in situations where the exact details of the  flow  field  are  unknown  but  the  boundary  value  of  the  pressure  is  known.  When performing  CFD  simulations  of  tunnel  ventilation  flows  and  fires,  pressure  boundary conditions are usually enforced at the tunnel portals or at the top open surface of vertical shafts or chimneys.

There  are  several  variations  on  how  to  apply  pressure  boundary  conditions;  the numerical  tool  adopted  for  the  simulations  (Fluent),  in  case  of  inflow  conditions, requires  the  definition  of  a  total  stagnation  pressure  just  outside  the  domain  which  is used  by  the  solver  to  compute  the  static  pressure  just  inside  the  domain.  In  case  of outflow conditions, static pressure can be directly fixed.

From a mathematical point of view, more natural boundary condition would require the prescription of force per unit area as a normal component of the stress tensor [65] as described hereafter

<!-- formula-not-decoded -->

where n is the unit vector normal to the specific boundary, τ is the stress tensor, p is the pressure and N ψ is the boundary value to be fixed. Clearly, being first derivatives of the velocity involved, equation (59) represents a Neumann type boundary condition . Under the assumption of negligible velocity gradients ( n τ ⋅ ~0), the force per unit area indeed corresponds to the value of the pressure. However, the positioning of pressure boundary condition boundaries is  a  critical  step  as  it  must  be  always  verified  that  the  flow  has reached a fully developed state having negligible gradients in the flow direction [66].

## 3.5.2. Velocity boundary conditions

Velocity inlet boundary conditions require all the flow variables to be specified at inlet boundaries. Typically, this approach is used to enforce a velocity profile or to model a solid  wall  moving  with  a  prescribed  velocity  under  no  slip  conditions.  From  a mathematical  point  of  view  this  corresponds  to  a Dirichlet  type  boundary  condition [65]. When performing CFD simulations of tunnel ventilation flows and fires, velocity boundary  conditions  are  usually  enforced  when  the  ventilation  conditions  are  known. This  requires  previous  experimental  test  to  be  carried  out  in  order  to  assess  the ventilation conditions within a certain degree of accuracy. However, such approach is questionable as induces a decoupling between fire and ventilation flows.

## 3.5.3. Wall boundary conditions

No-slip  conditions  have  been  applied  to  all  the  velocity  components  at  solid  walls. Typically,  a  zero  velocity  component  in  the  direction  normal  to  the  wall  is  the appropriate condition for the discretized continuity equation and discretized momentum equation in the direction normal to the wall. The estimation of the tangential and normal stresses at the wall (contained in the discretized momentum equations) requires extreme care given the typical turbulent nature of the flow. Indeed, a thin viscous sub-layer is located immediately adjacent to the wall followed by a buffer layer and a turbulent core. An extensive overview on the subject is given in [119] and is outside the scope of this document. However, the number of mesh points required to solve a turbulent boundary layer would be extremely large and commonly wall functions are used.

Wall functions are a collection of semi-empirical formulas and functions that interpolate the solution variables at the near-wall cells and the corresponding quantities at the wall. They  usually  comprise laws-of-the-wall for  mean  velocity  and  temperature  (or  other scalars) and correlations to prescribe near-wall turbulent quantities ( k and ε specifically).  In  this  work  standard  wall  functions,  based  on  the  work  of  Lauder  and Spalding [107], have been used. They are collected hereafter

<!-- formula-not-decoded -->

where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and κ is  the  Von  Karman  constant  (=0.4187), E wall  roughness  parameter  (=9.8  for smooth walls), U is  the mean fluid velocity ,  y the distance of the first grid point from the wall, τ u a velocity scale, µ the fluid molecular viscosity and ρ the fluid density.

The log-law (equation (60)) is valid as long as the first grid point is located in the fluid region  characterized  by 30  &lt;  y + &lt;  300. Fluent  by  default  uses  the  wall  functions  as described in (60) if y + &gt;11.63; if otherwise the code uses the laminar stress relationship known as linear law of the wall.

<!-- formula-not-decoded -->

However, intrusion of the first grid point in the viscous sub-layer should be avoided as the wall functions are based on the assumption that the rate of production of turbulent kinetic energy equals the rate of dissipation which is true in the log-layer but not strictly true  in  the  viscous  sub-layer.  This  hypothesis  is  on  the  basis  of  two  relationships between k , ε and the wall shear stress w τ .

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

For heat transfer, a wall function approach based on the universal near wall temperature distribution has been used [107]. For uncompressible flow calculation Fluent uses the following relationships

<!-- formula-not-decoded -->

where Tw is  the  wall  temperature, ρ the  fluid  density, cp the  fluid  specific  heat  at constant pressure, qw the wall heat flux, Prt the turbulent Prandtl number (=0.85 at the wall),  and P is  a  correction  function  Pee-function,  dependent  on  the  ratio  between laminar and turbulent Prandtl numbers [107]. Equation (63) is applied as long as y is larger than the non-dimensional sub-layer thickness defined as the intersection distance between  the  linear  and  the  log-law  of  the  wall.  For  smaller  values  of y a  linear relationship between T + and y + is used

<!-- formula-not-decoded -->

where Pr is the molecular Prandtl number of the fluid.

The  previous  relationships  are  valid  for  smooth  walls  where  the  changeover  from laminar to turbulent flows is assumed to take place at y + =11.63. For no smooth walls the constant E contained in (60) and indirectly in (63) is adjusted accordingly. Further details are given in [106,119].

By combining equations (60) and (64) it is easy for example to determine the wall shear stress to be input as boundary condition for a near wall cell in turbulent flow conditions

<!-- formula-not-decoded -->

where u + must be determined depending on the correspondent wall law. Equation (65) is  a  combination  of  the  wall  tangent  velocity  ( u )  and  its  derivative  contained  in w τ resulting in a non-linear Robin type boundary condition [120].

Similarly a heat flux boundary conditions can be introduced as

<!-- formula-not-decoded -->

Equation (66) is also a Robin type boundary condition . In case of adiabatic walls a zero normal  derivative  is  enforced.  If  not  specified,  all  the  following  simulations  are conducted  under  the  assumption  of  adiabatic  walls.  Other  heat  transfer  boundary conditions to the walls could be used, but the adiabatic condition represents the worst case in terms of buoyancy strength, threat to people and damage to the structure [121].

## 3.5.4. Boundary conditions for the transport equations of turbulent quantities

The  solution  of  two  additional  transport  equations  for  turbulent  kinetic  energy  and dissipation rate requires boundary conditions to be specified also for them.

Typically  a  profile  for k and ε must  be  specified  at  inlets  (i.e.  tunnel  portals  or chimneys).  Since  in  most  of  the  cases  no  information  is  available  in  the  literature,  a rough  estimation  for  inlets  distributions  for k and ε is  obtained  from  the  turbulent intensity and characteristic length (assumed for this case to be proportional to the tunnel hydraulic diameter h D ) can be conducted by means of the following simple forms [66].

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

l

h

D

0.07

=

where i is  the  turbulent  intensity, Uref the  reference  inlet  velocity, k the  turbulent kinetic energy, µ C the kε turbulence model constant, l a characteristic length scale and Dh the tunnel hydraulic diameter.

At outlets, commonly, a zero normal derivative is enforced for k and ε .

At walls, a zero normal derivative is fixed for the turbulent kinetic energy as prescribed in [107]. A Dirichlet boundary condition is instead enforced for ε which is assumed to be equal to

<!-- formula-not-decoded -->

where, µ C is the kε turbulence model constant, k is the turbulent kinetic energy, κ is the Von Karman constant and y is the distance from the wall of the first grid point.

## 3.5.5. Fire representation

The fire has been modelled as a volumetric source of energy without using a dedicated combustion model. It has been shown that this simplified approach, previously used to model tunnel fires [85,95], is the most practical given its low computational cost and its ability  to  reproduce  the  overall  behaviour  of  tunnel  fire  induced  flows.  It  avoids  the burden  and the complexity  of combustion  and  radiation models  and  the large uncertainty associated to the burning of condensed-phase fuels. Furthermore, it has been demonstrated that the same order of accuracy could be achieved when modelling a fire as volumetric source of heat or by adopting sophisticated combustion models [111]. In the  previous  reference,  the  accuracy  of  the  model  predictions  has  been  estimated  by comparing numerical data against experimental data from a number of enclosure fires including  large  atria  and  small  scale  tunnel.  Detailed  combustion  models  and  the volumetric source of heat approach produce reasonable results in most cases, but none of them are consistently accurate overall cases considered.

Figure 18: Schematic of the simplified fire representations used in this work.

<!-- image -->

Engineering drawing

In  this  work,  the  fire  heat  release  rate  (HRR), Q ,  has  been  introduced  in  the computational  domain  as  a  rectangular  slab  releasing  hot  gases  from  the  top  surface simulating  a  burning  vehicle  (see  Figure  18).  Mass  conservation  is  applied  by  the extraction of air at the obstruction four lateral surfaces simulating air entrainment. For sake of generality the mass extraction from the lateral faces is uniform and independent from the  ventilation  conditions.  This  may  not  be  completely  true  for  high  ventilation velocity  but  previous  sensitivity  studies  have  confirmed  a  minor  impact  of  this modelling detail. The amount of gases injected into the domain ( g m · ) is calculated using Equation  (69)  which  correlates  the  convective  part  of  the  HRR, Q(1λ ) ,    to  the temperature difference between air and hot gases:

<!-- formula-not-decoded -->

where λ is the flame radiative fraction, ) ( ∞ - T Tg is the temperature difference between ambient air and hot combustion products, Q the fire HRR and cp the air specific heat.

The flame radiative fraction λ can be up to 50 % [113] but most measured values are around 35% (value used in this work). The main limitation of this approach is that the maximum flame temperatures are not accurate very close to the fire source. However, as demonstrated  by  Vega  et  al.  [95]  and  by  Karki  and  Patankar  [85],  this  methodology produces  a  good  overall  agreement  with  experimental  temperature  measurements  of away from the flames.

There is little information in the literature on the gas phase temperature in a tunnel close to  the  fire  and  its  dependence  on  the  ventilation  conditions  and  fire  size.  Some experimental data are reported in the Runehamar tests in Norway, where the measured gas temperature above the centre of fire ranged between 1100 K and 1500 K [114]. The same  temperature  range  has  been  considered  in  this  paper  and  the  corresponding sensitivity of the solution investigated.

This modelling approach requires the definition of the top slab surface dimensions and its  dependence  on  the  fire  size.  A  surface  too  small  would  bring  unrealistic  air behaviour given the corresponding excessively high inlet velocity for the hot gases and the wrong balance between the momentum and buoyancy of the fire source. Thus, the fire  Froude  number  Q*  is  used  here  to  link  HRR  and  size  of  the  fire  source  [115], defined as

<!-- formula-not-decoded -->

where Df is  the  characteristic  dimension  of the fire source (hydraulic diameter of the slab top surface). Values of Q* above 2.5 are not realistic for diffusion flames [113]. Hence, the dimension of the fire source is calculated setting Equation (70) equal to 1, indicating a regime where the momentum and buoyancy strengths are of the same order of  magnitude.  This  choice  is  supported  by  the  fact  that  typical  tunnel  fires  can  be represented as a crib fires [116,117] that, following [118], have Froude number in the range of 1.

## 3.5.6. Jet Fan representation

CFD modelling of tunnel ventilation flows requires also a representation of the jet fans. Previous  CFD  analyses  of  tunnel  ventilation  [85,95]  simulated  the  jet  fans  as  a combination of discharge source and intake sinks of momentum and mass. This kind of approach  has  not  been  used  in  this  paper  avoiding  the  discrepancies  in  energy, momentum  and  species  conservations  that  are  generated  by  uncoupling  discharge sources and intake sinks. The methodology used here simulates the real construction of the jet fans as a cylindrical fluid region delimitated by walls and containing an internal cross surface where a constant positive pressure jump is enforced. Since no data on the specific jet  fan characteristic curve were available, the pressure rise across the jet fan internal  cross  section  has  been  supposed  to  be  independent  of  the  average  normal  air velocity. A schematic of the jet fan modelling approach is depicted in Figure 19; the internal  jet  fan  surfaces  used  to  fix  the  positive  pressure  difference  have  been highlighted in red.

However, in order to accurately predict the thrust with this approach or any other, it is highly recommended to use experimental data for calibration or validation of the results. This approach has been implemented successfully to model jet fan installed in a real tunnel where the comparison with experimental flow measurements is excellent (Colella et al. 2009 [102] and Colella et al. 2010 [103]).

Figure 19: Schematic of mesh used the fan representations used in this work.

<!-- image -->

Engineering drawing

## 3.6. Numerical features

The  complete  set  of  partial  differential  equations  including,  mass,  momentum,    and energy  conservation  equations  as  well  as  the  transport  equations  for  turbulent  kinetic energy  and  dissipation  rate,  cannot  be  solved  directly.  Numerical  methods  allow  the conversion of the governing equations into a set of algebraic equations whose derivation can be performed using different strategies.

The  first  step  involve  a  discretization  of  the  domain,  also  knows  as  meshing,  which allows the description of a continuous field variable θ into  a  set  of  discrete  values θ i defined at each mesh node.

The commercial CFD package Fluent adopts a finite volume approach to derive the set of  algebraic  equations.  Such  technique  uses  a  formal  volume  integration  of  the governing  equations  over  each  of  the  control  volumes  generated  by  the  meshing procedure. A simplified 1D control volume integration of the governing equations has been also  presented in chapter 2.    A  detailed  description  of  all  the  numerical  aspects involved  in  the  discretization  of  the  governing  equation  is  beyond  the  scope  of  this document but the interested reader can refer to [66]. However, some important aspects related to the settings of the CFD model are worth to be discussed.

The  integration  of  the  governing  equation  over  the  control  volumes  requires  the estimation of the variable at the boundary interface. In this work the convective fluxes and have been approximated by using a second-order upwind scheme [69].

Temporal discretization has been treated by using a first order implicit time integration as already described in chapter 2. The advantage of the fully implicit scheme is that it is unconditionally stable for any time step size [70].

The pressure-velocity linkage has been resolved by adopting the SIMPLE algorithm due to  Patankar  and  Spading  (1972)  [71].  An  adapted  version  of  the  algorithm  has  been developed for fluid network systems and presented in chapter 2. A segregated solution algorithm has been adopted for the calculation. The sequence of operations performed by the CFD solver is resumed in Figure 20.

Figure 20: Schematic of the CFD segregated  solution algorithm.

<!-- image -->

Flow chart

The degree of convergence of the solution has been estimated by using scaled residual and  by  monitoring  integral  values  of  relevant  quantities  (typically  mass  flow  rate through  tunnel  portals)  during  the  solution  procedure.  The  simulations  have  been considered  to  be  converged  when  the  scaled  residuals  were  lower  than  10 -5 with  the exception of the energy equation where the maximum allowed value was 10 -7 .

Given  the  complex  geometries  typically  encountered  in  tunnel  environments  (i.e. horseshoe cross sections, intersections with shafts, jet fan geometry) a quasi-structured meshing approach has been used. Once produced a base mesh case, the grid has been systematically refined in order to assess whether or not a grid-independent solution was reached. The refining has been iterated until no substantial variations both in the local field data and integral values were observed. A detailed grid independence analysis has been performed for any CFD or multiscale calculation presented hereafter.

## 3.7. Case Studies

## 3.7.1. Ventilation flows in the Norfolk road Tunnels

A  CFD  model  been  used  to  simulate  the  ventilation  flows  in  the  Norfolk  tunnels, Sydney (AU). The tunnels are 460 m long with a virtually flat gradient. Each tunnel, longitudinally ventilated, is equipped with 6 pairs of jet fans, rated by the manufacturer at  the  volumetric  flow  rate  of  34.2  m 3 /s  with  a  discharge  velocity  of  34.7  m/s.  A schematic of the tunnel  cross section including the jet fan installation  arrangement is presented in Figure 21.

Figure 21: Schematic of the Norfolk road tunnels cross section.

<!-- image -->

Engineering drawing

On the basis of the data provided by the tunnel operator, we were not able of accurately defining the longitudinal position of the jet fans within each tube; therefore, they have been considered approximately 80 m spaced as depicted in Figure 22.

Ventilation  flow  measurements  were  made  available  for  the  Westbound  tunnel;  they were taken by SickFlow 200 units located at the centre of each tunnel tube (~ 230 m from  the  inlet  portal).  Being  the  units  located  in  the  vicinity  of  jet  fans,  for  some ventilation scenarios the wind speed sensor readings are affected by adjacent jet fan. In these scenarios the accuracy of readings is compromised since they did not represent the real average velocity in the cross section.

Figure 22: Schematic of the jet fan longitudinal position in the Westbound Norfolk road tunnel; jet fans are numbered from 13 to 24.

<!-- image -->

Line chart

16  different  ventilation  scenarios  have  been  considered  during  the  experimental measurements.  The  main  characteristics  of  each  scenario  are  resumed  in  Table  8. Scenarios having the measurement unit located in the vicinity of an operating jet fan are highlighted  in  grey  and  they  have  been  discarded.  In  these  cases,  the  measured  air velocity is strongly dependent on the distance between fan and measurement unit and too little information of the effective fan and sensor locations was available.

Table 8: Summary of ventilation scenarios explored during the experimental campaign conducted in the Westbound Norfolk road tunnel. Scenarios having the measurement unit located in the vicinity of an operating jet fan have been highlighted in grey.

|          | sub scenarios   | Jet fan pairs   | Jet fan pairs   | Jet fan pairs   | Jet fan pairs   | Jet fan pairs   | Jet fan pairs   |                             |                          |                       |
|----------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------------------|--------------------------|-----------------------|
| scenario | sub scenarios   | 13-14           | 15,16           | 17,18           | 19,20           | 21,22           | 23,24           | experimental velocity [m/s] | predicted velocity [m/s] | mass flow rate [kg/s] |
|          | 1.1             | OFF             | OFF             | OFF             | OFF             | OFF             | ON              | 1.94                        | 1.14                     | 101.3                 |
| 1        | 1.2             | OFF             | OFF             | OFF             | OFF             | ON              | ON              | 4.16                        | 4.28                     | 379.3                 |
|          | 1.3             | OFF             | OFF             | OFF             | ON              | ON              | ON              | 5                           | 5.77                     | 510.8                 |
|          | 2.1             | ON              | OFF             | OFF             | OFF             | OFF             | OFF             | 2.7                         | 3.9                      | 339.2                 |
| 2        | 2.2             | ON              | ON              | OFF             | OFF             | OFF             | OFF             | 5.27                        | 5.66                     | 470.7                 |
|          | 2.3             | ON              | ON              | ON              | OFF             | OFF             | OFF             | 15.3                        | -                        |                       |
|          | 3.1             | ON              | ON              | ON              | OFF             | OFF             | OFF             | 15.3                        | -                        |                       |
| 3        | 3.2             | ON              | ON              | ON              | ON              | OFF             | OFF             | 15.8                        | -                        |                       |
|          | 3.3             | ON              | ON              | ON              | ON              | ON              | OFF             | 16.4                        | -                        |                       |
|          | 3.4             | ON              | ON              | ON              | ON              | ON              | ON              | 16.9                        | -                        |                       |
|          | 4.1             | OFF             | OFF             | ON              | OFF             | OFF             | OFF             | 14.4                        | -                        |                       |
| 4        | 4.2             | OFF             | OFF             | OFF             | ON              | OFF             | OFF             | 3.33                        | 3.83                     | 339.4                 |
|          | 4.3             | OFF             | OFF             | ON              | ON              | OFF             | OFF             | 15.3                        | -                        |                       |
| 5        | 5.1             | OFF             | ON              | OFF             | OFF             | OFF             | OFF             | 3.33                        | 4.06                     | 338.4                 |
|          | 5.2             | OFF             | ON              | OFF             | OFF             | ON              | OFF             | 5.83                        | 5.2                      | 470.5                 |
| 6        | 6.1             | OFF             | ON              | OFF             | ON              | OFF             | ON              | 6.1                         | 6.25                     | 512.8                 |

## 3.7.2. Assessment of the mesh requirements

The  computational  domain  has  been  discretized  by  using  a  quasi  structured  mesh arrangement. Various CFD  runs  have been also conducted to asses the  mesh requirements.  Four  different  meshes  have  been  generated  and  the  resulting  solutions compared. The mesh density per meter of tunnel length ranged from 260 cells/m up to 6200 cells/m. The symmetry of the domain across the longitudinal plane was considered since  the  explored  ventilation  scenarios  involved  activated  jet  fan  pairs  arranged symmetrically in respect to the tunnel longitudinal section. Four examples of the mesh cross  sections  are  presented  in  Figure  23.  The  test  case  used  for  the  grid  sensitivity analysis corresponds to scenario 2.1 and involves only 2 operating jet fans (#13 and #14 in Figure 22).

The solution is shown to converge as the mesh is made finer. A coarse mesh of 260 cells/m leads to a 16% underestimation of the average ventilation velocity. But a finer mesh  of  2500  cells/m  leads  to  results  within  0.36%  of  the  prediction  made  with  the finest mesh.

Table 9: Grid Independence Study for a scenario involving an operating jet fan pair in the Norfolk tunnels

|        |   mesh density [cells/m] |   predicted velocity [m/s] | deviation from mesh 4   |
|--------|--------------------------|----------------------------|-------------------------|
| mesh 1 |                      260 |                      3.125 | 16.41%                  |
| mesh 2 |                      700 |                      3.360 | 10.13%                  |
| mesh 3 |                     2800 |                      3.752 | 0.36%                   |
| mesh 4 |                     6200 |                      3.739 | -                       |

Besides  the  comparison  of  the  average  quantities,  detailed  field  solutions  have  been compared at Reference Sections 1 and 2, located 10 m and 100 m downstream of the jet fan  discharge  surface,  respectively.  The  comparison  of  the  longitudinal  velocity  is plotted  in  Figure  24  for  the  Reference  Section  1  and  in  Figure  25  for  the  Reference Section 2

Figure 23: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel.

<!-- image -->

Engineering drawing

Figure 24: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 1. Velocity values are expressed in m/s.

<!-- image -->

Engineering drawing

Figure 25: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 2. Velocity values are expressed in m/s.

<!-- image -->

Engineering drawing

As expected from the previous results, the computed solutions show larger deviations for the coarse meshes 1 and 2 while convergence is obtained for finer meshes 3 and 4. Based on the results, grid independence is considered reached in mesh 3 and therefore, the  following  simulations  have  been  conducted  using  this  grid.  The  total  number  of nodes for the 460 m long tunnel is around 1.3 million and the resulting computing time for  a  steady  state  scenario  ranged  between  3  and  5  hours  in  a  modern  quad-core workstation.

## 3.7.3.  Simulations  of  the  ventilation  scenarios  and  comparison to on-site measurements

The developed model has been used to simulate 9 ventilation scenarios from Table 8. The computed velocity profiles in the jet-fan longitudinal plane (plane 1 in Figure 21) are presented in Figure 26.

The available experimental data have been used to corroborate the model predictions. The  comparison  is  presented  in  Figure  40.  Generally,  accurate  velocity  predictions could  be  achieved  having  an  average  relative  deviation  from  experimental  findings around  17%.  The  maximum  deviation  (~40%)  has  been  found  for  the  ventilation scenario  2.1.  Given  the  lack  of  detailed  information  on  the  jet  fan  installation arrangement, geometry and longitudinal position, the accuracy achieved is considered satisfactory  and  no  other  attempts  to  improve  the  numerical  predictions  have  been performed. However it is believed that, if more detailed geometric details are provided, significantly better predictions can be achieved.

The model results confirm the very low efficiency of ventilation scenario 1.1 which was also observed experimentally. This is due to the unfavourable location of the jet fans 23 and 24 (see Figure 39). Indeed, they are too close to the tunnel outlet portal to allow their discharge velocity cones to develop and generate enough thrust.

<!-- image -->

Photograph

Figure 26: Computed velocity profile in the tunnel for scenarios 1.1, 1.2, 1.3, 2.1, 2.2, 4.2, 5.1, 5.2, 6.1 from Table 8. The plotted velocity fields are relative to plane 1 of Figure 21. Velocity values are expressed in m/s.

<!-- image -->

Bar chart

Figure 27: Comparison between predicted velocity and experimental measurements provided by the Sickflow 200 Units located at the centre of each tunnel tube.

<!-- image -->

Scatter plot

Table 8 contains also the predictions of the mass flow rates through the tunnel for each ventilation scenario. It can be seen that, scenarios 2.1, 4.2 and 5.1, involving only one operating jet fan pair, are equivalent since the same mass flow rate through the tunnel is generated (~338 kg/s). Same conclusion can be deduced when analysing scenarios 2.2 and  5.2  which  involve  2  operating  jet  fan  pairs.  In  the  last  two  cases  the  ventilation induced  flow  through  the  tunnel  is  around  ~470  kg/s.  In  the  ventilation  scenarios involving 3 jet fan pairs (1.3 and 6.1) an average ventilation induced flow of 510 kg/s could be attained.

A final CFD run has been performed to assess the ventilation system performance when all  the  6  jet  fan  pairs  are  operating  (ventilation  scenario  3.4  in  Table  8).  In  this ventilation scenario the predicted mass flow rate through the tunnel is around 764 kg/s corresponding to an average longitudinal velocity of around 8.5 m/s. A schematic of the CFD predictions is presented in Figure 28.

Figure 28: 3D visualisation of the computed velocity fields for ventilation scenario 3.4 involving all the 6 jet fan pairs. Velocity values are expressed in m/s. (not to scale).

<!-- image -->

Engineering drawing

## 3.7.4. Critical velocity calculation

Wu and Bakar [33] carried out a series of small scale experiments on five horizontal tunnels with different cross-sections. They assessed, on the basis of accurate measurements in a controlled environment, the effect on the critical velocity of tunnel cross  section  and  fire  heat  release  rate.  Among  the  different  cross  sections,  the  data relative  to  the  square  cross-sectional  tunnel  (0.25×0.25  m 2 cross  section)  will  be considered  in  this  document.  The  small  scale  tunnel  is  around  15  m  long  and  it  is equipped with a circular porous bed propane burner (diameter equal to 0.106 m) located at a distance of 6.21 m from the tunnel inlet. The tunnel outlet is located at a distance of 8.7 m from the burner centre. The tunnel upstream section was constructed of PMMA, while, the fire and the fire downstream regions were constructed of steel. A water spray device was constructed to cool the tunnel walls near the fire source and was used only when  the  tunnel  wall  temperature  was  excessive.  The  ventilation  flow  during  the experiments was driven by an air compressor. A schematic of the experimental rig is depicted in Figure 29.

The burner heat release rate, controlled by the propane flow rate, was varied during the tests  ranging  between  1.5  kW  and  30  kW.  These  fire  sizes  correspond  to  fires  of approximately 2.5÷50MW in a tunnel of diameter around 5 m and 300 m long when a scaling procedure is applied (see equations (10) and (11)).

The measured values of critical velocities in two different fire scenarios (3 kW and 30 kW) will be used in this section to validate the fire CFD model. The same scenarios have  been  used  by  Van  Maele  and  Merci  [97]  to  validate  two  different  turbulence modelling approaches (RANS and LES). They also adopted a mixture fraction model to simulate  the  combustion  process.  Their  results  will  be  taken  into  account  when evaluating  the  performance  of  the  simplified  fire  model  previously  presented  in  this chapter.

Figure 29: Schematic of the experimental rig accordingly to Wu and Bakar [33]. Section B has been used in this study.

<!-- image -->

Engineering drawing

## 3.7.5. Assessment of the mesh requirements

The computational domain has been discretized by using a structured mesh arrangement. The upstream edge of the fire source has been located 5 m downstream of the inlet section of the CFD domain. The length of the simulated CFD domain is 10 m. Various  CFD  runs  have  been  also  conducted  to  asses  the  mesh  requirements.  Four different meshes have been generated and the resulting solutions compared. The mesh size ranged from 37000 up to 1300000 nodes. The symmetry of the domain across the longitudinal  plane  was  considered.  Four  examples  of  the  mesh  cross  sections  are presented in Figure 30.

## Mesh characteristics

Figure 30: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel.

<!-- image -->

Engineering drawing

The simulations, conducted for a 30kW fire scenario at critical ventilation conditions, have been compared first in terms of the predicted critical velocity (see Table 10).

The solution is shown to converge as the mesh is made finer. The adoption of mesh #1 leads to an 11% underestimation of the critical ventilation velocity when compared to the finest mesh (#4) results. No appreciable variation in the critical velocity predictions could be observed when the computations have been performed using mesh #3.

Table 10: Grid Independence Study for a scenario involving a 30 kW fire scenario

|        |   mesh size [cells] |   predicted critical velocity [m/s] | deviation from mesh 4   |
|--------|---------------------|-------------------------------------|-------------------------|
| mesh 1 |               37000 |                                0.49 | 8.89%                   |
| mesh 2 |              120000 |                                0.46 | 2.22%                   |
| mesh 3 |              620000 |                                0.45 | 0.00%                   |
| mesh 4 |             1300000 |                                0.45 | -                       |

Besides,  detailed  field  solutions  have  been  compared  at  Reference  Sections  1  and  2, located  1  m  and  3  m  downstream  of  the  fire  source,  respectively.  The  predicted longitudinal  velocities  and  temperature  fields  are  plotted  in  Figure  31  for  Reference Section 1 and in Figure 32 for Reference Section 2.

Figure 31: Computed temperature and velocity fields for mesh #1 to #4 at reference sections 1 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Engineering drawing

Figure 32: Computed temperature and velocity fields for mesh #1 to #4 at reference sections 2 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Engineering drawing

As expected from the previous results, the computed solutions show larger deviations for the coarse meshes 1 and 2 while convergence is obtained for finer meshes 3 and 4. Based on the results, grid independence is considered reached in mesh 3 and therefore, all the following simulations have been conducted using this grid. The total number of nodes  for  the  10  m  long  small  scale  tunnel  is  around  1.3  million  and  the  resulting computing time for a steady state scenario ranged between 2 and 4 hours in a modern quad-core workstation.

## 3.7.6.  Critical velocity results

Two scenarios have been simulated first involving a 30 kW and a 3 kW fire. The size of the fire source has been calculated using the scaling relations as presented in equations (69)  and  (70)  under  the  assumption  of  fire  source  Froude  number  equal  to  1.  The corresponding sizes of the fire source are 0.042 m 2 and 0.007 m 2 for the 30 kW and 3 kW fire, respectively.

Following the same approach presented in [97], the simulated fire is considered to be at critical  ventilation  condition  when  the  velocity  component  parallel  to  the  tunnel  axis becomes around zero in the computational cell adjacent to the tunnel ceiling and above the  leading  edge  of  the  burner.  The  computed  critical  ventilation  velocities  are respectively 0.36 m/s  and  0.45  m/s  for 3  kW  and  the  30  kW  fire  scenarios, underestimating the experimental findings by around 25 % in both the cases. Indeed, the measured critical velocity values are 0.48 m/s and 0.6 m/s for the 3 kW and 30 kW fire, respectively.

Figure 33: Computed temperature and velocity fields in the vicinity of the fire source for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Engineering drawing

A schematic of the computed temperature and longitudinal velocity field in the vicinity of a 30 kW fire source at critical ventilation conditions is presented in Figure 33. An initial  stage  of  back-layering  occurrence  is  confirmed  by  the  presence  of  a  region characterized by sustained backward motions in the region located immediately above the  fire  source.  Same  conclusion  can  be  obtained  by  observing  the  high  temperature gases stratified in same regions. Temperature and longitudinal velocity fields have been also  plotted  for  reference  section  1  and  reference  section  2  located  1  and  3  m downstream of the fire source, respectively (see Figure 34).

Figure 34: Computed temperature and velocity fields at reference sections 1 and 2 for a 30 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Engineering drawing

The  velocity  and  temperature  isocontours  show  a  complex  flow  pattern  at  reference section 1. Instead, the temperature contours show that the flow has a stratified structure with  almost  horizontal  layers  at  reference  section  2.  It  has  been  verified  that  in  this region  the  maximum  transversal  velocity  components  are  almost  two  orders  of magnitude  smaller  than  the  maximum  longitudinal  velocity.  This  confirms  that,  at reference  section  2,  the  flow  has  evolved  to  fully  developed  channel  flow  which  is essentially  1D  with  small  recirculation  patterns.  As  a  consequence,  the  details  of  the flow  beyond  this  point  do  not  influence  the  flow  pattern  near  the  burner  surface  and hence the prediction of the critical velocity.

Same considerations can be obtained for the 3 kW fire. The computed temperature and longitudinal  velocity  fields  in  the  fire  near  field  are  presented  in  Figure  35  while temperature and longitudinal velocity fields at reference sections 1 and 2 are presented in Figure 36.

Figure 35: Computed temperature and velocity fields in the vicinity of the fire source for a 3 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Line chart

Figure 36: Computed temperature and velocity fields at reference sections 1 and 2 for a 3 kW fire at critical ventilation conditions. Temperature and velocity values are expressed in K and m/s respectively.

<!-- image -->

Engineering drawing

These two fire scenarios have been analysed by Van Maele and Merci [97] by using two different CFD tools: Fluent and FDS.

The first simulations have been conducted with Fluent by using a modified version of the kε turbulence model in which the turbulence production due to buoyancy has been treated by using the generalized gradient diffusion hypothesis briefly described in this chapter. Combustion has been addressed by adopting a mixture fraction approach. The critical velocity predictions underestimate the experimental values by around 8.5% and 31% for the 30 kW and 3 kW fire respectively.

Poorer predictions have been achieved when adopting the second CFD package (FDS) which  is  based  on  LES  turbulence  modelling.  The  LES  model  systematically  overpredicted the experimental critical velocity data by 21% and 40% for the 3 kW and 30 kW  fire  scenarios,  respectively.  The  simplified  fire  representation  developed  in  this work,  leads  to  a  critical  velocity  under-estimation  (25%  in  both  the  cases)  which  is comparable  with  the  accuracy  that  could  be  achieved  adopting  higher  sophisticated modelling approaches for turbulence and combustion. On the other hand, the resulting computing time is smaller since species transport equations and combustion phenomena are not solved. This is a point in favour of the simplified representation of the fire that will be used in the remaining part of this work.

## 3.7.7. Effect of the fire Froude number on the critical velocity

The  previous  simulations  have  been  conducted  under  the  assumption  that  the  fire Froude number is equal to 1 and the temperature of the hot combustion gases released by the horizontal slab is equal to around 1100 K. An initial study conducted by varying the temperature of the combustion products between 1100 K and 1500 K has shown that it  has  a  very  minor  impact  on  the  predicted  critical  velocity.  Therefore  it  has  been omitted. A much larger impact on the critical velocity predictions was observed when varying  the  fire  source  Froude  number  and  therefore  a  sensitivity  study  has  been undertaken. A wide range of Froude numbers (between 0.5 a 5) has been investigated in order to include the largest portion of possible fire scenarios involving different fuels [6]. Also in this case two different fire sizes (3 kW and 30 kW) have been considered for the sensitivity study and the results are resumed in Figure 37.

Figure 37: Effect o fire Froude number on the predicted critical for a 3 kW and a 30 kW fire

<!-- image -->

Line chart

The numerical  analysis  shows  that  there  is  a  linear  correlation  between  the  predicted critical velocity and the fire source Froude number at least within the range of Froude number  investigated.  As  expected,  the  slope  seems  to  be  correlated  to  the  fire  HRR being higher for larger fire sizes. A 100 % increase in the predicted critical velocity has been found for the 30 kW fire scenario when the Froude number was increased from 0.5 to 5. Around 10 % increase has been found for the 3 kW fire source. An analysis of this behaviour on the basis of Froude scaling theory has been undertaken but no conclusive results have been obtained and therefore the subject is currently under investigation.

## 3.8. Concluding Remarks

The chapter describes the application of CFD techniques to tunnel ventilation flows and fires. An overview of the literature studies since the first application in the late 90s has been  given.  The  review  process  showed  that  CFD  models  are  able  to  predict  critical ventilation velocity, and back layering distance within an acceptable level of accuracy (deviation  usually  smaller  than  30%).  The  overall  flow  data  (i.e.  bulk  velocity  and temperature)  are  also  accurately  predicted  with  deviations  from  experimental  values typically within 20%. On the other hand the literature study, showed that prediction on local  flow  field  data  (i.e.  velocity  and  temperatures),  especially  if  calculated  in  the vicinity of the  fire  source,  can  be  affected  by  error  significantly  higher  than  100%  in comparison to experimental measurements.

An  overview  of  CFD  model  characteristics including turbulence model,  typical boundary conditions for tunnel ventilation flows and fires and numerical features has also  been  provided.  A  simplified  approach  to  deal  with  the  fire  source  has  also  been developed. The fire has been modelled as a rectangular slab releasing hot combustion products without using a dedicated combustion model. This approach does not provide accurate  results  in  the  flame  region  but  allows  for  reasonable  accuracy  when  dealing with the overall tunnel flow behaviour (i.e. far field temperature and velocity, critical velocity and back layering distance). A comparison to the experimental findings from two small scale tunnel fire scenarios (3 kW and 30 kW) studied by Wu and Bakar [33] confirmed the ability of the simplified fire model to predict the critical velocity with a reasonable  level  of  accuracy  (~  25%).  A  similar  level  of  accuracy  for  the  same  fire scenarios  was  also  achieved  by  Van  Maele  and  Merci  [97]  that  adopted  a  dedicated combustion model and more sophisticated turbulence models.

Furthermore, the ability of the developed CFD tool to deal with cold flow ventilation scenarios has been assessed. The developed model  has been validated against experimental velocity data measured in 9 different ventilation scenarios in the Norfolk Tunnels  in  Sydney  (AU).  Also  in  this  case  a  significant  level  of  accuracy  (average relative deviation around 17%) has been achieved.

The CFD analyses have shown that significant computational resources (several hours of computing time in a modern 4-core workstation) were required to simulate a single steady state ventilation or fire scenario in relatively short tunnels. Indeed the small-scale tunnel was 15 m long (300 m on large scale if the diameter is scaled up to 5 m) while the  Norfolk  tunnels  are  460  m  in  length.  The  computational  time  would  become  a severe limitation when the full CFD approach is adopted to deal with fire or ventilation behaviour in tunnels several kilometres in length. For these scenarios, a way to avoid such  high  computational  complexity  is  the  adoption  of  multiscale  methods  based  on hybrid 1D-3D computational techniques. The application of multiscale methods in the framework of tunnel ventilation flows and fires is the subject of the following chapters.

Parts of this work have been published in Building and Environment [102] , Tunnelling and Underground Space Technology [103] and Fire Technology [105].

<!-- image -->

Icon

## Fundamentals of multiscale computing

## 4.1. Introduction

CFD models of tunnel fires have been shown to predict the overall behaviour of the ventilation system (i.e. critical ventilation velocity and back-layering distance) within an acceptable range of accuracy (namely, within 10÷30% deviation). Several studies on the subject  have  been  reviewed  and  discussed  in  the  previous  chapter.  However,  almost 90%  of  the  reviewed  papers  focused  only  on  the  back-layering  occurrence  without directly referring to the capabilities of the installed ventilation system (i.e. how many fans to be activated in order to prevent back-layering). Indeed, the ventilation velocity to be input as boundary condition into the model is supposed to be known on the basis of rough estimations or cold flow experimental tests conducted in the tunnel. This kind of approach does not allow a critical evaluation of the ventilation system performance under different fire hazards as ventilation velocities and fire behaviour are not coupled together.

4

The reason for this trend highlighted in the literature review process, is due to the very large  computational  demand  typical  for  comprehensive  CFD  studies  of  ventilation system  performance  during  fires.  The  high  computational  cost  leads  to  the  practical problem that arises when the CFD model has to consider boundary conditions or flow characteristics  in  locations  far  away  from  the  region  of  interest.  This  is  the  case  of tunnel portals, ventilation stations or jet fan series located long distances away from the fire.  In  these  cases,  even  if  only  a  limited  region  of  the  tunnel  has  to  be  investigated (e.g. for the fire), an accurate solution of the flow movement requires that the numerical model  includes  all  the  active  ventilation  devices  and  the  whole  tunnel  layout.  For typical  tunnels,  this  could  mean  that  the  computational  domain  is  several  kilometres long.

The study of ventilation and fire-induced flows in tunnels [30,33,85,95,97,102] provides the evidence that in the vicinity of operating jet fans or close to the fire source the flow field has a complex 3D behaviour with large transversal and longitudinal temperature and velocity gradients. The flow in these regions needs to be calculated using CFD tools since any other simpler approach would only lead to inaccurate results. These regions are hereafter named as the near field . However, it has been demonstrated for cold flow scenarios  and  for  fire  scenarios  that  some  distance  downstream  of  these  regions,  the temperature and velocity gradients in the transversal direction tend to disappear and the flow becomes essentially 1D. In this portion of the domain the transversal components of  the  velocity  can  be  up  to  two  orders  of  magnitude  smaller  than  the  longitudinal components. These regions are hereafter named as the far field . The use of CFD models to  simulate  the  fluid behaviour  in  the  far  field  leads  to  large  increases  in  the computational requirements but very small improvements in the accuracy of the results. A visual example of typical velocity and temperature fields established in the vicinity of an operating jet fan or fire is presented in Figure 38.

Figure 38: up) Example computed velocity field for a pair of operating jet fans (jet fan discharge velocity ~34 m/s; down) Example computed temperature field for a 30MW fire subject to supercritical ventilation conditions. The velocity and temperature values are expressed in m/s and K, respectively.

<!-- image -->

Bar chart

On  the  basis  of  these  observations  and  for  the  sake  of  an  efficient  allocation  of resources,  CFD  should  be  applied  only  to  model  the  near  field  regions  while  the  far field regions should be simulated using a 1D model. These types of hybrid model are commonly called multiscale models. Multiscale models allow a significant reduction in the  computational  time  as  the  more  time  consuming  tool  is  applied  only  to  a  limited portion of the domain.

In a multiscale approach, the CFD and the 1D models exchange flow information at the 1D-CFD interfaces. There are two general coupling options. The simplest one is the 1way  coupling (or  superposition).  For  example,  in  the  case  of  inclined  tunnels,  it  is possible  to  evaluate  the  global  chimney  effect  using  a  1D  model  of  the  entire  tunnel [122]. Then, a CFD analysis of specific tunnel portions can be run using as boundary conditions the 1D results. This approach does not represent true multiscale modelling since there is no coupling of the CFD results to the 1D flow. This would be equivalent to assume that the flow behaviour in the high gradient regions does not affect the bulk tunnel flow.

A 2-way coupling of  1D and CFD models, proper multiscale modelling, consists of a physical decomposition of the problem in two parts: a portion of the tunnel is simulated using a CFD model and the remaining portions through 1D model. The advantage of multiscale modelling resides on including in the flow calculations the effect of the fire on the entire ventilation system and vice versa. If the solver is able to receive the two sets  of  equations,  the  problem  can  be  solved  at  once.  In  most  of  the  cases  there  is  a different solver for each model, and therefore iterative calculations are necessary with the two solvers continuously exchanging information at boundary interfaces.

Few  examples  of  multiscale  modelling  fluid  flow  systems  have  been  found  in  the literature.  Examples  include  the  simulation  of  blood  flow  in  the  circulatory  system [123],  the  computation  of  gas  flows  in  exhaust  ducts  of  internal  combustion  engines [124],  the  characterization  of  the  flow  pattern  over  high  speed  trains  moving  through tunnels [125]. Recent applications of multiscale techniques address also the problem of naturally  fractured  oil  reservoirs  [127].  Multiscale  methods  have  been  only  cited  as possible  techniques  for  simulating  tunnel  ventilation  flows  and  fires  by  Rey  and  coworkers (2009) [126] without any significant results.

## 4.2. Fundamental of domain decomposition methods

Multiscale  techniques  are  based  on  domain  decomposition  methods  which  have  been developed for all the discretization techniques (i.e. finite difference, finite volume and finite elements) mainly in the framework of parallel computing. They allow the original single problem to be reformulated on several computational sub-domains. Eventually, this technique can be applied to solve heterogeneous problems which are described by different governing equation as in the present case.

Figure 39: Example of domain decomposition with and without overlapping [65].

<!-- image -->

Engineering drawing

The basic idea is to decompose the global domain in several sub-domains and to solve the  resulting  problems  characterized  by  smaller  domain  size  eventually  by  means  of parallel  computing.  Domain  decomposition  can  be  performed  adopting  two  different techniques  which  generate  overlapping  and  non-overlapping  sub-domains.  A  visual example  of  sub-domain  decomposition  with  and  without  overlapping  is  depicted  in Figure 39.

Three iterative methods based on domain decomposition are available in the literature and they are mainly differentiated by the boundary conditions applied at the interfaces and by the presence of overlapping regions [128]:

- Dirichlet-Dirichlet or Schwarz methods
- Dirichlet- Neumann methods
- Neumann - Neumann methods

Schwarz methods are applied for overlapping domain decomposition and use Dirichlet type  boundary  conditions  applied  on Γ 1 and Γ 2 for  the  sub-domains Ω 1 and Ω 2, respectively (see Figure 39).

Dirichlet-Neumann methods are applied for non-overlapping domain decomposition and use one Dirichlet-type boundary condition and one Neumann-type boundary condition.

Neumann-Neumann  methods are  applied  for  non-overlapping  domain  decomposition and use only Neumann-type boundary conditions applied on Γ for the sub-domains Ω 1 and Ω 2, respectively (see Figure 39).

A  description  of  the  mathematical  theory  behind  domain  decomposition  methods  is beyond the scope of this document. The interested reader should refer to [128].

The exact structure of the boundary conditions to be applied at the interfaces depends on the  differential  operator  defining  the  original  set  partial  differential  equations.  In  the case  of  Navier-Stokes  equations  only  Dirichlet-Neumann  and  Schwartz  methods  are used. Being S the  Navier-Stokes operator, a Dirichlet-Neumann iterative method must perform the following sequence of operating until convergence is achieved [65]

Figure 40: Example of domain decomposition for solution of Navier-Stokes problem using a DirichletNeumann iterative method.

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where

- 2 ϕ a 1 ϕ are vectorial functions describing the Dirichlet boundary conditions (e.g. prescribed velocities)  at  the  boundary D 2, Γ and D 1, Γ of  the  sub-domains Ω 1 and Ω 2 (refer to Figure 40)
- 2 ψ a 1 ψ are vectorial functions describing the Neumann boundary conditions (e.g. prescribed normal stresses) at the boundary N 2, Γ and N 1, Γ of the sub-domains Ω 1 and Ω 2 (refer to Figure 40)
- k is  the  multiscale iteration counter, α is  a  velocity  under-relaxation parameter required to improve convergence and n the normal coordinate.

It is here stressed that when a Dirichlet-Neumann method is adopted, the sub-domains Ω 1 and Ω 2 must not overlap.

Schwartz methods require overlapping sub-domains and Dirichlet boundary conditions prescribed on both the resulting interfaces 2 Γ and 1 Γ .

Figure 41: Example of domain decomposition for solution of Navier-Stokes problem using a Schwartz (Dirichlet-Dirichlet) iterative method.

<!-- image -->

Engineering drawing

Being S the  Navier-Stokes  operator  a  Schwartz  iterative  method  must  perform  the following sequence of operating until convergence is achieved [65]

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where

- 2 ϕ a 1 ϕ are vectorial functions describing the Dirichlet boundary conditions (e.g. prescribed velocities)  at  the  boundary D 2, Γ and D 1, Γ of  the  sub-domains Ω 1 and Ω 2 (refer to Figure 40)
- 2 ψ a 1 ψ are vectorial functions describing the Neumann boundary conditions (e.g. prescribed normal stresses) at the boundary N 2, Γ and N 1, Γ of the sub-domains Ω 1 and Ω 2 (refer to Figure 40)
- k is the multiscale iteration counter and n the normal coordinate.

The main advantage of Schwarz method is the easy way of dividing the sub-domains from a possibly complicated geometry. The main drawback is that the convergence of the iteration depends on the overlap [129].

## 4.3. Formulation of the multiscale problem

The  multiscale  model  developed  in  this  work  is  based  on  domain  decomposition techniques  which  have  been  proved  to  be  adequate  to  solve  also  heterogeneous problems  described  by  different  governing  equations  [128].  In  this  specific  case  the tunnel fluid-dynamic behaviour has been addressed by adopting two different numerical descriptions of the problem based on 1D and 3D-CFD tools.

For sake of simplicity and only in this section, it is supposed that the tunnel domain ( Ω ) is decomposed in two sub-domains Ω 1D and Ω 3D where the 1D model (see section 2) and the CFD model (see section 3) are respectively applied. Ω 1D and Ω 3D are built in order to be continuous in the streamwise direction. Figure 42 depicts a schematic of a 1D-3D domain decomposition. The 1D-3D interface Γ a is located in x=a in such way that there is no overlapping between the two sub-domains.

Figure 42: Example of a domain decomposition in 1D and 3D sub-domains.

<!-- image -->

Engineering drawing

On  the  right  hand  side  of Γ a the  1D  domain  provides  average  values  for  pressure, temperature, velocity and mass flow rate; they are indicated as ) ( + p a , ) ( + T a , ) ( + u a and consequently ) ( + · m a , respectively. Analogously, the same quantities can be defined for the left side of Γ a but, since the left hand side of Γ a belongs to the 3D domain, integral averaged values must be computed (see equation (73)).

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where u represents the velocity vector, p the pressure, ρ the density, T the temperature, n the unitary vector normal to the interface Γ a.

Following  the  same  approach  presented  in  [123],  it  is  reasonable  to  look  for  the continuity of the following quantities at the interface:

- a. Area ( ) ( ) + - = A a A a b. Mean pressure ( ) ( ) + - = p a p a c. Mean velocity ( ) ( ) + - = v a v a d. Mean temperature ( ) ( ) + - = T a T a (74)

The same authors underline that instead of the constraint (74).b, the continuity of the averaged normal stresses could also be prescribed; however, being the normal stresses partially neglected in the 1D model, and the 1D-3D interfaces located in regions where the  flow  is  fully  developed  ( 0 ≈ ∂ ∂ x u ),  the  previous  constraint  on  the  pressure  is adequate. However, the accuracy of such assumption will be checked in each multiscale computation by assessing how its location affects the global results. The solution of the coupled  multiscale  problem  cannot  be  reached  by  means  of  standard  computing algorithm but it is based on iterative computing procedures developed in the framework of domain decomposition methods. Obviously, being the sub-domains without overlapping regions, a Dirichlet-Neumann coupling strategy will be adopted.

## 4.4. Coupling technique

## 4.4.1. Direct coupling

The solution to the multiscale problem requires the coupling of the 1D and CFD models which  has  been  obtained  by  means  of  a  Dirichlet-Neumann  strategy.  In  particular Dirichlet boundary conditions (i.e. velocity boundary conditions) are prescribed at the interfaces  for  the  1D  model.  Neumann  boundary  conditions  (i.e.  pressure  boundary conditions) are instead prescribed at the interfaces for the CFD model.

The  iterative  solving  algorithm  will  be  presented  for  a  general  case  in  which  a  CFD model  of  the  near  field  domain  ( Ω 3D )  is  coupled  with  two  1D  models  of  far  field domains  ( Ω 1,1D and Ω 2,1D )  located  upstream  and  downstream,  respectively.  Two interfaces Γ i and Γ j are therefore generated (see Figure 43).

The algorithm requires a dynamic exchange of information between the models during the computation. A three stage coupling has been adopted for the scope (see Figure 43).

A full 1D model of the whole system is solved during the first stage.

A  CFD  model  of  the  near  field  domain Ω 3D is  solved  during  the  second  stage.  Its boundary conditions at Γ i and Γ j are provided by the full 1D model run at the first stage.

The global multiscale convergence is reached during the third stage when the 1D model of the far fields ( Ω 1,1D and Ω 2,1D )  and  the CFD model of the near field ( Ω 3D )  are run sequentially k-times exchanging periodically the boundary conditions at the interfaces Γ i and Γ j (see Figure 43).

In comparison to more traditional coupling approaches, a three stage coupling allows a significant reduction of the multiscale iterations needed to reach a global convergence.

The complete sequence of operations to be conducted during the solving procedure is described hereafter:

## STAGE 1

- a. Run the full 1D model of the whole system until convergence is reached
- b. Total  pressure  and  temperature  values  at  the  nodes  corresponding  to  the interfaces Γ i and Γ j are recorded (to be used as boundary conditions of the Ω 3D CFD model in the next stage)

## STAGE 2

- a. Run the CFD model of the near field Ω 3D until a certain degree of convergence is reached

- b. Calculate  average  velocity  values  at  the  interfaces Γ i and Γ j (to  be  used  as boundary conditions for the 1D model of the far fields in the next stage)
- c. Calculate average temperature values at the interfaces Γ i and Γ j (to be used as boundary conditions for the 1D model of the far field in the next stage)

## STAGE 3

- a. Run the 1D model of the far fields Ω 1,1D and Ω 2,1D until convergence is reached
- b. Pressure  and  temperature  values  at  the Γ i and Γ j are  recorded  as  used  as boundary conditions in step c.
- c. Run the CFD model of the near field until a certain degree of convergence is reached
- d. Calculate  average  velocity  values  at  the  interfaces Γ i and Γ j (to  be  used  as boundary conditions for the 1D model in the next multiscale iteration)
- e. Calculate average temperature values at the interfaces Γ i and Γ j (to be used as boundary conditions for the 1D model in the next multiscale iteration)
- f. Check global convergence
- I. If  global  convergence  is  not  reached  go  back  to point  a (eventually  a relaxation step can be added as prescribed in equation (72))
- II. If global convergence is reached quit the calculation or proceed to the next time step for time dependent calculation

## STAGE 1

## FULL 1D model

Figure 43: Visualization of a three stage coupling procedure.

<!-- image -->

Engineering drawing

It  must  be  noted  that,  the  coupling  between  grids  is  physically  realized  between  the pressure  nodes  of  the  1D  grid  ( i,j in Figure  43)  and  the  mesh  faces  lying  on  the interfaces Γ i and Γ j. . Therefore, the prescription of a velocity boundary condition for the 1D sub-domain is performed by using a ghost velocity node (indicated as t' in Figure 44 for the left interface) located beyond the last 1D pressure node (indicated as i in Figure 44). The implementation of this boundary condition causes the i pressure cell to act as a source/sink of mass. Instead, temperature and pressure values can be directly transferred from the 3D to the 1D grid (and vice-versa) since naturally defined in the i node.

Figure 44: Visualization of the interaction procedure between 1D and 3D grids at the left CFD domain boundary (1D-CFD interfaces highlighted in green)

<!-- image -->

Engineering drawing

Further considerations are required when dealing with the turbulent kinetic energy and the dissipation rate at the interfaces. Since these quantities are not calculated by the 1D model, they are introduced as a function of turbulence intensity, turbulent length scale and Reynolds number using well known relations for fully developed flow within pipes. They have been resumed in equations (67).

This coupling approach is called direct coupling . It allows for a significant reduction in the computational time in comparison to the full CFD calculation of the same scenario. However, the timescale of the direct coupling calculations is limited by the computational speed of the CFD portion of the model. This can take from some minutes to up to many hours depending on the complexity of the scenario.

Figure 45: left) Evolution of total pressure and mass flow rate at a 1D-3D interface during a multiscale calculation. The maximum deviation allowed was 10 -6 . right). Deviation of the mass flow rate and total pressure at a 1D-CFD interface during a multiscale calculation

<!-- image -->

Line chart

The global convergence check is performed by monitoring the evolution of any average fluid-dynamic  quantity  at  the 1D-CFD interfaces  during  the k-iterations performed during step 3. In particular, the model checks whether or not the deviation of a certain fluid-dynamic quantity during two sequential multiscale iterations is lower than a fixed tolerance. Figure 45 shows the evolution of total pressure and mass flow rate computed at a 1D-CFD interface during a multiscale calculation. The maximum deviation allowed was 10 -6 which  was  reached  after  around  20  multiscale  iterations.  It  is  worth  to  note that,  given  the  high  uncertainty  characterizing  tunnel  ventilation  flow  calculations, lower accuracy (i.e. 10 -3 ) can be used shortening significantly the computing time (~10 multiscale iterations).

The actual exchange of information between 1D and CFD tools has been performed by using User-defined-Functions (UDF)  that  can  be  dynamically  loaded  by  FLUENT  to enhance  the  standard  features  of  the  code  [130].  UDF  scripts  are  written  in  C++ programming  language  and  are  used  to  define  user-defined  source  terms,  boundary conditions and material properties. In the specific case compiled UDF have been used for mainly 3 purposes:

- Averaging fluid-dynamic quantities at the 1D-3D interfaces
- Launch the 1D model executable file
- Update and store the results before proceeding to the next time step calculation (for time-dependent simulations)

In particular the general-purpose ' DEFINE\_ON\_DEMAND' UDF have been chosen as they can be are called automatically by the solver during the solution procedure. A large effort  has  been  profused  in  order  to  produce 'parallelized' version  of  the  scripts  in order to be used both during serial and parallel computations. A detailed description of the UDF programming technique is beyond the scope of this document; the interested reader can refer to [130].

## 4.4.2. Indirect coupling

Most  of  the  ventilation  studies  require  bulk  flow  velocities  and  average  temperature values in steady state or quasi steady state conditions. In this case an indirect coupling method can be adopted allowing 1D and CFD simulations to be run separately. After identifying the near field, a series of CFD runs are conducted for a range of uniform boundary conditions at the interfaces. In this manner, the CFD results are arranged in terms of bulk flow velocities as a function of the total pressure differences across the near  field  allowing  the  definition  of  characteristic  curves.  These  curves  represent  the coupling of the active element of interest (shaft, jet fan, or fire) with the surrounding tunnel  gallery.  The  1D  model  is  designed  in  order  to  take  into  account  these  curves, accurately calculated by the CFD model and, hence, it couples them to the rest of the tunnel.  In  the  next  sections,  indirect  coupling  techniques  will  be  used  to  describe  the behaviour of jet-fan and fire near field in terms of fan and fire characteristic curves. The CFD  computed  curves  will  be  then  input  in  the  1D  model  improving  its  prediction capabilities.

Indirect coupling leads to higher set-up times, mainly dedicated to the calculation of the characteristic  curves,  but  then  provides  almost  instantaneous  results  for  steady  state calculation of tunnel flows and temperatures. The implementation of indirect coupling techniques for transient calculation is possible but complicated since the curves must be eventually updated each time step to follow the fire growth or the fan activation ramp.

## 4.5. Concluding remarks

In  this  section  the  fundamentals  of  multiscale  computing  have  been  presented.  The developed model is based on the decomposition of the tunnel layout in sub-domains:

- The near field regions, characterized by high velocity or temperature gradients, modelled by means of CFD techniques;
- The far field regions, characterized by milder gradients modelled by using a 1D model.

Some practical issues related to the coupling methods between the 1D and 3D solvers have been also addressed in the framework of domain decomposition techniques. The application of multiscale modelling techniques to simulate tunnel ventilation flows and fire will be the subject of the next sections.

Parts of this work have been published in Building and Environment [102] , Tunnelling and Underground Space Technology [103] and Fire Technology [105].

## 5 Multiscale modelling of tunnel ventilation flows

## 5.1. Introduction

In  this  section  a  multiscale  model  will  be  used  to  describe  the  behaviour  of  tunnel ventilation flows in normal operating conditions (i.e. cold flow). Computational analysis of tunnel ventilation flows are mainly interested in the characterization of the discharge cone  from  operating  jet  fans  and  in  assessing  the  global  performance  of  a  given ventilation  system.  The  first  analysis  is  required  for  optimization  purposes  or  to understand how the fan thrust depends on particular installation details (i.e. presence of niches, distance from the ceiling, eccentricity).  Comprehensive analysis of ventilation systems  are  instead  required  to  describe  the  ventilation  flows  in  the  overall  tunnel domain depending on the specific settings of the ventilation devices (i.e. set points of the fans, activation of specific extraction or supply stations). Such analyses are mainly required for ventilation strategy design.

The characterization of the jet fan discharge cones and a comprehensive analysis of the installed  ventilation  systems  have  been  performed  for  the  Dartford  tunnels  located  in London  (UK).  The  multiscale  model  results  have  been  corroborated  by  an  extensive experimental campaign we have conducted in the tunnels between 2007 and 2008.

## 5.2. A case study: the Dartford tunnels

The  Dartford  tunnels  are  two  twin-lane,  uni-directional  road  tunnels  under  the  River Thames, crossing from Dartford at the south (Kent) side of the river to Thurrock at the north  (Essex)  side,  about  15  miles  east  of  London  in  the  UK.  Both  tunnels  have complex  ventilation  systems  consisting  of  a  semi-transverse  system  together  with additional jet fans to control longitudinal flow.

Figure 46: Diagram of the East and West Dartford Tunnels showing the relative positions of jet fans and extract shafts. (Drawn approximately to scale but with vertical distances five times larger)

<!-- image -->

Engineering drawing

The tunnels are approximately 1.5 km long and each tunnel carries unidirectional traffic in two lanes. Generally, both tunnels carry northbound traffic only, while southbound traffic uses the four lane Queen Elizabeth II bridge, which lies slightly to the east of the tunnels.  In  instances  of  extreme  weather,  the  bridge  may  be  closed  and  the  traffic direction in the East Tunnel may be switched to southbound.

Figure  46  shows  the  general  layout  of  the  tunnels.  The  West  Tunnel  (approx.  8.6m internal  diameter)  was  opened  to  traffic  in  1963  and  the  East  Tunnel  (approx.  9.5m internal  diameter)  in  1980.  The  West  Tunnel  is  constructed  of  a  cast  iron  segmental lining, which has been infilled with concrete. The East Tunnel is constructed of three different types of primary lining material: the central 600m of the tunnel are constructed of pre-cast concrete segments with steel face plates, on either side of the central section there is a portion of the tunnel (170m long at the north end and 100m long at the south) constructed of cast iron segments, the remainder of the tunnel (200m at the north and 355m  at  the  south)  was  constructed  of  cast  in-situ  concrete  using  a  cut  and  cover technique. The real tunnel environment is represented in Figure 47 and Figure 48.

Figure 47: East Dartford Tunnel; Picture taken approximately 1100 m from the Kent portal facing south (refer to Figure 46).

<!-- image -->

Photograph

Figure 48: West Dartford Tunnel; Picture taken approximately 500 m from the Kent portal facing south (refer to Figure 46).

<!-- image -->

Photograph

In  both  tunnels  the  semi-transverse  ventilation  system  has  two  shafts  with  axial extraction  fans  located  at  relatively  short  distance  from  each  of  the  tunnel  portals.  In both tunnels the semi-transverse system supplies fresh air into the tunnel through grills along the side of the roadway between the extract shafts. The fresh air is pumped into the invert under the roadway by means of two axial fans, one at the Kent end and one at Essex. There are no transverse supply grills between the portals and the shafts. In the West tunnel, there are 14 pairs of unidirectional jet fans, located between the  extract shafts.  In  the  East  tunnel  there  are  five  individual  reversible  jet  fans  between  the southern  portal  and  the  southern  extract  shaft  and  three  pairs  of  reversible  jet  fans between the northern shaft and the northern portal. The jet fan spacing is around 50 m in both the tunnels. The layout of the tunnels and the position of the jet fans is shown in Figure 46.

In  the  event  of  a  fire,  the  emergency  strategy  currently  implemented  in  the  Dartford tunnels  assumes  that  all  vehicles  ahead  of  the  incident  will  be  able  to  safely  exit  the outgoing  portal,  while  a  queue  of  traffic  builds  up  behind  the  incident.  Thus,  the ventilation is configured in such a way as to blow any smoke away from the queuing traffic. To allow for a flexible emergency response, four different ventilation strategies are used, depending on the location within the tunnel where the fire occurs:

- If  the  incident  occurs  between  the  Kent  portal  and  the  southern  extract  shaft (hereafter referred to as 'Zone A'), the ventilation strategy utilises the activation of all jet fans (blowing south to north) and both extract fans, but sets both supply fans off.
- If the incident occurs between the southern extract shaft and the mid point of the tunnel ('Zone B'), the ventilation strategy utilises the activation of all jet fans (blowing south to north) and the northern extract fan, but sets both supply fans and the southern extract fan off.
- If  the  incident  occurs  between  the  mid  point  of  the  tunnel  and  the  northern extract shaft ('Zone C'), the ventilation strategy utilises the activation of all jet fans (blowing south to north), the southern supply fan and the northern extract fan, but sets the northern supply fan and the southern extract fan off.

- If  the  incident  occurs  between  the  northern  extract  shaft  and  the  Essex  portal ('Zone D'), the ventilation strategy utilises the activation of all jet fans (blowing south to north), both southern supply fans, but sets both extract fans off.

## 5.3. Overview on the experimental setups

In order to estimate the flow in the tunnels, the cross-section was divided into 9 equal areas, and the measurements of velocity were taken at the geometric centres of gravity of  each  section.  However,  in  order  to  simplify  the  measurement  process,  the  actual coordinates of the measurement points were slightly offset from the calculated values and are shown in Figure 49:

Figure 49: Layout and general dimensions of the tunnel cross sections (west tunnel to the left; East tunnel to the right) including the points 1-9 where the air velocities where measured (dimensions are expressed in mm).

<!-- image -->

Engineering drawing

The measurements of the jet fan discharge cones have been performed  at 6 different locations,  at  20  m  intervals,  starting  20  m  downstream  from  the  jet  fan  discharge surface. Furthermore, bulk flow velocities in the central section of the tunnels have been recorded for a wide range of fan combinations.

The measurements were carried out using 3 different types of instruments:

- hot wire anemometers
- rotating vane anemometers
- a Pitot tube

All these instruments were connected to Kimo portable data loggers. The instruments provide  measurements  in  the  range  0.3  to  35  m/s  with  an  accuracy  of  2%±0.1  m/s. They are also very robust in terms of their correct alignment with the flow: they present little error for angles of misalignment of up to 24° (in practice, anemometers positioned in the flow by hand, as in these tests, are unlikely to be misaligned by as much as 10°, so the results are well within the operating range of the equipment).

Error estimations were done for the rotating vane anemometer, the instrument used for most of the  measurements.  The  greatest  standard  error  was  of  ±14.5.  This  value  was measured 20 m downstream from a pair of jet fans, with all the other fans turned off. This  is  caused  by  the  unstable  nature  of  the  flow  close  to  the  jet  fans,  where  the  jet generated  is  probably  not  stable  in  space,  especially  when  there  are  no  other  fans operating.

In  order  to  avoid  redundancy,  the  experimental  measurements  will  be  presented  later together with the numerical predictions.

## 5.4. Characterization of the jet fan discharge cone

The characterization of the jet fan discharge cone for the East and West tunnel has been performed by adopting a multiscale model with direct-coupling. This approach allows for  the  computation  of  detailed  flow  field  data  in  the  3D-CFD  sub-domain  ( Ω 3D in Figure 50) while the rest of tunnel layout is represented by adopting a 1D modelling approach.  Indeed,  detailed  simulations  of  the  fluid  flow  behaviour  in  the  jet-fan surroundings may be not fully accomplished without taking into account the interaction with the rest of the tunnel layout and ventilation devices.

A schematic of the coupling between 1D model of the far field and CFD model of the near field has been depicted in Figure 50.

Figure 50: Schematic of multiscale coupling between mono-dimensional and CFD models for the multiscale calculation of the jet fan discharge cone (1D-CFD interfaces highlighted in green)

<!-- image -->

Engineering drawing

As  already  asserted  in the previous  sections, a critical point of the multiscale representation is the positioning on the 1D-3D interfaces Γ i and Γ j in Figure 50. Indeed, they  must  be  located  in  a  domain  region  where  the  flow  is  fully  developed  and  is characterized  by  mild  velocity  gradients.  Thus,  the  size  of  the  3D  sub-domain  ( L3D ) plays a crucial role in the accuracy of the global solution. This issue will be addressed in the next sections.

## 5.4.1. Assessment of the mesh requirements

Various CFD runs have been conducted to asses the mesh requirements. Four different meshes have been generated and the resulting solutions compared. The mesh density per meter of tunnel length ranged from 272 cells/m up to 7000 cells/m. The symmetry of the  domain  across  the  longitudinal  plane  was  considered  only  for  the  West  tunnel calculations  since  the  explored  ventilation  scenario  involved  a  jet  fan  pair  arranged symmetrically in respect to the tunnel longitudinal section. Four examples of the mesh cross section are presented in Figure 51.

Figure 51: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel.

<!-- image -->

Engineering drawing

The solutions have been compared in terms of bulk flow velocity and in terms of the flow  field  computed  in  two  reference  tunnel  cross  sections  located  10  m  and  100  m downstream of the jet fan discharge surface (see Figure 50).

Table 11: Grid Independence Study for a scenario involving an operating jet fan pair in the West tunnel

|        |   Mesh density [cell/m] |   Predicted air velocity [m/s] | Deviation from mesh 4   |
|--------|-------------------------|--------------------------------|-------------------------|
| Mesh 1 |                     272 |                          1.926 | 0.29%                   |
| Mesh 2 |                    1890 |                          1.927 | 0.34%                   |
| Mesh 3 |                    4000 |                          1.921 | 0.02%                   |
| Mesh 4 |                    7000 |                          1.920 | -                       |

The dependence of the computed average velocity as function of the mesh density is resumed in Table 11. It shows that the solution converges as the mesh is made finer. For instance, the computation performed with mesh 3 deviates by 0.02% from the prediction performed with the finest mesh.

<!-- image -->

Engineering drawing

0

Figure 52: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 1. Velocity values are expressed in m/s.

The  comparison  of  the  predicted  velocity  fields  at  the  Reference  Section  1  and Reference  Section  2  is  presented  in  Figure  52  and  Figure  53.  As  expected  from  the previous results, the computed solutions show larger deviations for the coarse meshes 1 and 2 while convergence is obtained for finer meshes 3 and 4. Based on the results, grid independence  is  considered  reached  in  mesh  3  and  therefore,  all  the  following simulations have been conducted using this grid.

Figure 53: Comparison of the longitudinal velocity contours for meshes #1 to #4 in the tunnel at the reference section 2. Velocity values are expressed in m/s.

<!-- image -->

Engineering drawing

## 5.4.2. Effect of the 1D-CFD interface location

A  sensitivity  analysis  has  been  conducted  in  order  to  asses  how  the  position  of  the interfaces between mono-dimensional and CFD domain affects the calculated solution. An operating jet fan produces a region where the fluid field has high velocity gradients and a proper modelling approach would require a CFD tool. The high gradient region does not extend for a long distance and after the flow behaves as fully developed and it could  be  successfully  represented  using  a  mono-dimensional  model.  The  interface between mono-dimensional and CFD domain must to be located in this region. In order to  identify  this  distance,  14  different  runs  were  performed.  In  each  run  the  interfaces were  placed  progressively  further  away  from  the  operating  fans,  increasing  the longitudinal extension of the CFD domain ( L3D Figure 50) and consequently reducing the  extension  of  the  mono-dimensional  domain.    For  each  run  the  predict  bulk  flow (Figure 51) has been recorded. The reference value is the bulk flow calculated using a full scale CFD simulation of the whole tunnel.

Figure 54: Convergence of the predicted mass flow rate as a function of the location of the interface

<!-- image -->

Line chart

Being L3D the  length  of  the  near  field  (see  Figure  50),  the  error  induced  by  an inappropriate location of the interfaces can be calculated as

<!-- formula-not-decoded -->

⋅

⋅

where mCFD is the mass flow rate calculated using the full CFD model, and mMS is the mass flow rate computed by the multiscale model for a given value of L3D .  Figure 54 shows the error calculated in each run and its dependence on the 3D domain length. It is clear that the multiscale approach can lead to accurate results when the dimensions of the  CFD  domain  are  only  a  fraction  of  the  whole  tunnel  length  (1.5km)  with  a significant reduction of the computational time. Results with less than 10% error can be obtained using a 3D domain longer than 80 m (5% of the tunnel length). The accuracy of the multiscale model is improved up to around 1% by using 300 m as length of the near  field  (20%  of  the  tunnel  length).  The  following  calculations  are  then  conducted with the length of the 3D model set to 300 m. The downstream 1D-CFD interface is then located at a distance from the jet fan discharge surface ( LD in Figure 50) larger than ~20 times the tunnel hydraulic diameter.

## 5.4.3. Comparison to experimental data

Figure 55: Comparison of horizontal velocities between predictions (lines) and experimental measurements (symbols) in the West Tunnel. The two profiles and the numbers refer to locations in the tunnel section described in Figure 49.

<!-- image -->

Line chart

The comparison between predicted and experimental velocities measured in the West tunnel  is  presented  in  Figure  55.  The  blue  continuous  line  represents  the  velocity profiles calculated in the middle of the tunnel cross sections ( profile 1 in Figure 49.a) while the red dashed ones represent the velocity profiles calculated along the vertical lines corresponding to the profiles 2 in Figure 49.a.

The  measured  velocity  values  represented  in  Figure  55  are  numbered  from  1  to  9 following the same pattern as presented in Figure 49.a. The measurements have been obtained with only the 5 th jet fan pair operating in the West tunnel. The comparison is quite encouraging as in almost all the measurement sections there is a good agreement between experimental and numerical data.

All the CFD tests done during the development of the model have demonstrated that the niches  where  the  jet  fans  are  located,  have  a  significant  effect  on  the  longitudinal development of the flow and their capability of producing thrust. The worst agreement between the model and the experimental data was found in the section 60m downstream of the fan; this peculiarity is most likely due to the presence of obstacles located on the tunnel ceiling (other fans and  lighting devices) which  are  not included in the computational domain but influence the discharge cone characteristics.

A  similar  degree  of  accuracy  is  obtained  when  comparing  predicted  and  measured velocity profiles in the East Tunnel (see Figure 56). In this case, only the 3 rd single jet fan was operating and therefore the velocity profile is not symmetrical across the tunnel longitudinal plane, unlike in the West Tunnel.

The blue continuous line represents the velocity profiles calculated in the middle of the tunnel  cross  sections  ( profile  2 in  Figure  49.b).  The  red  velocity  profile  with  finer dashing represents the velocity calculated on the vertical line indicated as profile 1 in Figure  49.b.  The  green  velocity  profile  with  coarser  dashing  represents  the  velocity calculated  on  the  vertical  line  indicated  as profile  3 in  Figure  49.b.  The  measured velocity values represented in Figure 56 are numbered from 1 to 9 following the same pattern as presented in Figure 49.b.

Also in this case the comparison is quite encouraging as in almost all the measurement sections there is a  good  agreement between experimental and numerical data. A poor agreement  between  experimental  and  numerical  data  has  been  encountered  in  the section 80 m downstream from the fan. This is most likely due to obstacles present in the specific region of the tunnel (luminaries or other jet fans) or to a sudden change in the  meteorological  conditions  given  the  strong  external  winds  recorded  during  the measurement campaign.

The analysis of the jet fan discharge cone confirmed that the flow is approximately one dimensional in nature beyond 80m downstream of the fan outlet in the case of the West tunnel. In the East tunnel the discharge cone is slightly longer at 100m. This is because the jet fans installed within the East tunnel are more powerful than in the West, and not installed in niches on the ceiling, as they are in the West Tunnel. When more than one jet  fan  pair  is  operating,  the  near  field  must  include  all  operating  devices  within  the module length.

Figure 56: Comparison of horizontal velocities between predictions (lines) and experimental measurements (symbols) in the East Tunnel. The two profiles and the numbers refer to locations in the tunnel section described in Figure 4.b.

<!-- image -->

Line chart

## 5.5. Characterization of the ventilation system

The assessment of the ventilation system performance required a comprehensive study of  the  ventilation  strategies  within  the  tunnels. In  particular,  the  study  aims  to understand  the  consequences  on  the  tunnel  flow  of  making  changes  to  the  fan configurations. This kind of analysis does not require detailed flow field data but only bulk flow velocities within the tunnel domain.

The  first  modelling  choice  to  address  this  problem  was  a  purely  1D  model.  For  this particular application, the main difficulty encountered when using the 1D approach was related to the assessment of the jet fan thrust and their losses induced by their peculiar installation locations (i.e. in niches in the West tunnel). In fact, it is well known that the pressure rise produced by the jet fans is strictly dependent on the specific surrounding environment [62]. Therefore, the prediction capability of a 1D model mainly relies on calibration constant  to be  defined  arbitrarily or on  the basis of literature data. Furthermore, some empirical correlations to estimate the thrust from jet fan pairs were adopted  (see  equations  (25))  but,  in  several  cases,  they  over-predicted  the  actual capabilities of the ventilation system.

In  order  to  overcome  this  problem,  a  multi-scale  modelling  approach  with  indirect coupling was used.

## 5.5.1. Calculation of the jet fan characteristic curves

When using a multiscale model with indirect coupling, the behaviour of high gradient regions  is  represented  in  terms  of  characteristics  curves.  Such  curves,  computed  by performing  several  CFD  runs  of  the  near-field  sub-domain,  are  built  in  order  to  be directly implemented in a 1D model.

The region of high velocity gradients, in this case, is represented by the fluid domain close to the operating jet fan pair.  In case of the activation of many jet fan pairs, the flow within the tunnel domain is characterized by many high gradients regions requiring to  be  modelled  using  a  CFD  approach.  Obviously,  depending  on  the  number  and location of the operating jet fans, different meshes for the near field must be built. To avoid  this  complexity,  some  preliminary  CFD  runs  have  been  performed  in  order  to understand how a series of operational jet fan pairs operates. All the results have shown that  a  series  of  equidistant  jet  fans  produces  a  flow  field  characterized  by  an  almost periodic  pattern.  Figure  58  is  a  clear  example.  It  shows  the  velocity  isocontours calculated  for  a  series  of  7  jet  fan  pairs  operating  in  the  West  tunnel  where  the periodicity of the flow field is evident.

Figure 57: Typical flow pattern produced by a series of seven jet fan pairs operating in the West Tunnel (not to scale). Velocity isocontours from 2 m/s to 20 m/s in steps of 2 m/s; Velocity expressed in m/s.

<!-- image -->

Bar chart

As the flow periodicity has been accessed, the computational domain of the near field has  been  limited  to  the  periodic  portion  of  the  tunnel  geometry  where  the  inlet  and outlet boundaries have been defined as periodic surfaces. Thus, a jet fan series can be modelled  by  including  a  single  representative  module  which  operates  in  a  periodic behaviour.  The  assumption  of  periodic  flows  implies  that  the  velocity  components repeat themselves in space while the pressure drop across the modules is periodic. This modelling approach is usually applied for periodic flows where a periodic pressure drop occurs across translationally repeated boundaries [69].

Figure 58: Computational mesh for the CFD module around the jet fans in the West (right) and East (left) tunnels. (Note: the West tunnel's jet fans are installed in niches on the ceiling, in the East tunnel they are not.)

<!-- image -->

Engineering drawing

Thus, once the near fields have been identified, the CFD mesh has been built following the available tunnel geometric data, in order to represent the jet fans installations and obtain a better estimation of the jet fans thrust. An example of the CFD meshes built for the East and West tunnels is presented in Figure 58.

Several runs of the near field CFD model have been performed, varying the pressure difference across the domain boundaries. The results can be presented in terms of bulk flow velocity and pressure difference across the domain (Figure 59). The curve obtained describes the capability of each pair of jet fans to produce thrust and its dependence on the bulk flow velocity.

Figure 59: CFD calculated jet fan thrust vs. tunnel average velocity for the Dartford tunnels.

<!-- image -->

Line chart

The results of this CFD study for the near fields are then coupled to the 1D model for the rest of the tunnel. Specifically, the computed curves are used as the characteristics of any  branch  of  the  1D  model  containing  jet  fans  avoiding  the  uncertainties  related  to calibration constants.

It is worth to highlight that the assumed flow periodicity lasts as long as the supply fans within the tunnel are off. The introduction of fresh air will slightly modify the velocity patterns  within  the  tunnel  and  the  mass  flow  rate  will  not  be  constant  along  the longitudinal  direction.  However,  these  effects  are  small  since  the  amount  of  fresh  air introduced is negligible compared to the large mass flow rate through the main gallery. Thus,  in  also  this  case,  the  computed  characteristic  curves  still  provide  a  good approximation.

The  same  approach  for  the  description  of  operating  jet  fan  series  has  been  used  by Colella and co-workers (2010) [105] and the results have been compared to full CFD representation of the same scenarios. The authors showed that the simplified representation  based  on  the  periodic  flow  assumption  leads  to  bulk  flow  velocities deviating as much as 1.5% from full CFD solutions.

## 5.5.2. Comparison to experimental data

The multiscale model with indirect coupling has been validated using bulk flow data recorded in the central section of the tunnels under a wide range of fan combinations. The comparison between predictions and recorded bulk velocities is presented in Figure 60  as  a  function  of  the  number  of  operating  jet  fans.  The  agreement  between  the experimental  data  and  the  predictions  is  excellent,  demonstrating  accurate  prediction capabilities.  Some  discrepancies  can  be  observed  for  the  East  tunnel  under  some ventilation scenarios. The differences are due to changes in the weather (i.e. strong wind at the portals) during the on-site measurements.

Figure 60: Comparison between experimental data and model predictions.

<!-- image -->

Line chart

The simplicity of the model and its robustness allows the simulation of many different ventilation  scenarios,  as  well  as  the  effect  of  different  fan  combinations  and  their interaction  with  the  extract  and  supply  fans.  The  effect  of  wind  or  other  external boundary conditions (e.g. difference between static pressures at the adits) can also be easily  taken  into  account,  as  can  the  influence  of  the  vertical  shafts,  stack  effect, dampers or any obstacles within the tunnel. The model can also be used to calculate the distribution of pollutants or the influence of traffic flow on the average air velocity, as well as to make real time predictions of ventilation flows for control purposes. In the next section some results of the assessment of the ventilation system performance are presented.

## 5.5.3. Analysis of all the ventilation strategies

The model was used to analyse the flows resulting from each of the existing ventilation configurations,  related  to  the  strategies  for  each  of  the  four  zones.  The  results  are summarised in Table 12.

Table 12: Summary of ventilation flows in the tunnels resulting from various ventilation strategies. The operating ventilation devices in each scenario are indicated by 'ON'. The predicted ventilation velocities in the incident zones are highlighted in bold

| Ventilation strategy   | Ventilation strategy   | All Jet Fans   | Kent Axial Extract Fan   | Essex Axial Extract Fan   | Kent Axial Supply Fan   | Essex Axial Supply Fan   | Between Kent portal and shaft (Zone A)   | Midpoint of tunnel (Between Zones B & C)   | Between Essex shaft and portal (Zone D)   |
|------------------------|------------------------|----------------|--------------------------|---------------------------|-------------------------|--------------------------|------------------------------------------|--------------------------------------------|-------------------------------------------|
|                        |                        |                |                          |                           |                         |                          | Ventilation velocities (m/s)             | Ventilation velocities (m/s)               | Ventilation velocities (m/s)              |
|                        | Zone A                 | ON             | ON                       | ON                        | OFF                     | OFF                      | 9                                        | 5.1                                        | 1.2                                       |
|                        | Zone B West            | ON             | OFF                      | ON                        | OFF                     | OFF                      | 4.5                                      | 5.9                                        | 2                                         |
|                        | Zone C                 | ON             | OFF                      | ON                        | ON                      | OFF                      | 3.5                                      | 5.9                                        | 3.3                                       |
|                        | Zone D Tunnel          | ON             | OFF                      | OFF                       | ON                      | ON                       | 2.2                                      | 5.4                                        | 5.1                                       |
|                        | JF only                | ON             | OFF                      | OFF                       | OFF                     | OFF                      | 4.2                                      | 5.6                                        | 3.6                                       |
|                        | Zone A                 | ON             | ON                       | ON                        | OFF                     | OFF                      | 5                                        | 2.2                                        | 5.2                                       |
|                        | Zone B East            | ON             | OFF                      | ON                        | OFF                     | OFF                      | 5                                        | 4.1                                        | 1.4                                       |
|                        | Zone C Tunnel          | ON             | OFF                      | ON                        | ON                      | OFF                      | 3.7                                      | 4.1                                        | 3                                         |
|                        | Zone D                 | ON             | OFF                      | OFF                       | ON                      | ON                       | 1.5                                      | 2.9                                        | 5.7                                       |
|                        | JF only                | ON             | OFF                      | OFF                       | OFF                     | OFF                      | 4.7                                      | 3.2                                        | 4.7                                       |

Studies  of  the  ventilation  required  to  control  smoke  from  fires  in  tunnels  [28,29,33] suggest that the critical velocity is generally of the order of 2.5 to 3 m/s. Thus, for the Dartford,  all  four  ventilation  strategies  for  both  tunnels  should  provide  more  than adequate smoke control in an emergency.

Further analysis of the simulations for the East Tunnel showed that some of the airflow generated by the jet fans between the Kent portal and the extract shaft is diverted up the extract shaft as this short shaft poses a smaller resistance to the airflow than the main portion of the tunnel does. For example, in the 'jet fans only' case, the flow in Zone A is 4.7  m/s,  while  the  flow  in  Zone  B  is  only  3.2  m/s,  some  of  the  air  is  lost.  Similar behaviour  has  been  found  in  the  East  tunnel  when  activating  the  Essex  jet  fan  pairs. Using the model it is possible to demonstrate, for example, that if dampers were fitted on the extract shafts, effectively blocking the losses, the resulting flow using all jet fans would be 3.7 m/s throughout the tunnel.

## 5.5.4. Assessment of the redundancy in the Dartford Tunnels

One of the advantages of using the multiscale model with indirect coupling is that it is comparatively easy and quick to assess the consequences of making small changes to the  fan  configuration,  thus  it  is  possible  to  assess  the  consequences  of  removing individual jet fans (or pairs) from a given scenario.

For example, Figure 61 shows the effects of varying the number of active jet fans in the Zone C ventilation strategy for the West Tunnel. If it is assumed that an airflow of at least 3 m/s is required throughout Zone C in this incident scenario, then it can be clearly seen that more than two pairs of jet fans are required to provide this magnitude of flow.

1800

Figure 61: Results for the West Tunnel, using the strategy for Zone C (Kent supply on, Essex extract on), varying the number of active jet fan pairs. (Note: Zone C extends from approximately 700 m into the tunnel to 1370 m).

<!-- image -->

Line chart

Similar calculations for the other zones reveal that, to generate a flow of at least 3 m/s in each of the incident zones, a minimum of three jet fan pairs are required in the Zone B scenario, only two pairs are required in the Zone D scenario and no jet fans are required in  the  Zone  A  scenario;  in  this  instance  sufficient  flow  can  be  generated  by  the  axial extract  fans  on  their  own.  Thus,  it  is  clear  that  several  pairs  of  jet  fans  in  the  West Tunnel may be safely taken out of use for maintenance or refurbishment, whilst still maintaining  sufficient  flow  control  capabilities  for  any  of  the  considered  incident scenarios.

In  the  East  Tunnel  the  situation  is  more  complex  due  to  the  positioning  of  the  fans between the portals and the shafts. An example of the results for the Zone C strategy is shown in Figure 62. Here, it is generally found that the majority of jet fans are required to produce the required level of flow in the central section of the tunnel.

- For Zone A ventilation strategy, only one pair of jet fans on the Essex incline is required to produce a longitudinal flow of 3 m/s.
- For Zone B ventilation strategy, all three pairs of jet fans on the Essex incline (or four Kent fans and one pair at Essex) are required to produce a longitudinal flow of 3 m/s.
- For Zone C ventilation strategy, at least four Kent jet fans plus one pair of Essex jet fans are required to produce a longitudinal flow of 3 m/s.
- For Zone D ventilation strategy, at least three jet fans on the Kent incline are required to produce a longitudinal flow of 3 m/s.

Thus, while there is some redundancy in the East Tunnel ventilation system, there is considerably less redundancy than in the West Tunnel. However, it appears that one or two fans may be safely taken out of service in the East Tunnel at any given time for maintenance purposes.

1800

Figure 62: Results for the East Tunnel, using the strategy for Zone C (Kent supply on, Essex extract on), varying the number of active jet fans. (Note: Zone C extends from approximately 700 m into the tunnel to about 1300 m)

<!-- image -->

Line chart

## 5.6. Concluding remarks

The  chapter  describes  the  application  of  multiscale  computing  techniques  to  model ventilation flows within road tunnels. The direct coupling approach has been adopted to simulate the velocity field generated by operating jet fans in the Dartford tunnels (UK). The  analysis  on  the  positioning  of  the  1D-CFD  interfaces  shows  that  high  accurate results (deviation from Full CFD calculation within 1%) can be achieved with CFD subdomains  whose  longitudinal  extension  is  around  300  m  representing  the  20%  of  the whole tunnel length. The corresponding multiscale model run-time is around 2 orders of magnitude  shorter  when  compared  to  the  requirements  of  full  CFD  calculations.  The results obtained have been also compared to on-site velocity measurements.

The multiscale model with indirect coupling has been used to characterize the Dartford tunnel ventilation systems and its redundancy. Also in this case the results have been corroborated  by  on-site  measurements.  The  analysis  of  the  jet  fan  near  field  has confirmed that the niches in the West tunnel play a considerable role in the development of the discharge cone affecting the fan capability in producing thrust.

The multiscale model has been demonstrated to be a valid tool for the simulation of the complex behaviour of the tunnel ventilation systems in cold flow scenarios. It can be successfully adopted to design ventilation systems and to assess their redundancy and their  performance  under  different  operative  conditions.    An  example  of  performance assessment  has  been  performed  in  the  case  of  the  Dartford  tunnels.  The  analysis demonstrates the capability of the actual ventilation systems to provide adequate levels protection for  all  the  incident  ventilation  strategies.  The  model  has  also  demonstrated that, for a given ventilation scenario, even if there are some jet fan failures, the tunnel ventilations system will still be able to provide adequate air flow levels.

Parts  of  this  work  have  been  published  in Building  and  Environment  [102] and Tunnelling and Underground Space Technology [103].

<!-- image -->

Icon

## Multiscale modelling of tunnel fires

## 6.1. Introduction

In the previous chapter, a multiscale modelling technique has been applied to address the  behaviour  of  tunnel  ventilation  systems  in  cold  flow  scenarios  (i.e.  ambient conditions).  The  aim  of  the  present  section  is  to  widen  the  range  of  applicability  by addressing tunnel fire scenarios.

In  this  case  further  complexity  is  added  by  the  presence  of  high  temperature  and velocity  gradients  in  the  plume  region.  However,  as  already  asserted  in  the  previous chapters, such high gradient regions do not extend too far downstream of the fire source since they evolve to fully developed flow regions.

The multiscale application discussed in this section is designed in order to include the fire near field region in the 3D-CFD sub-domain while the rest of the tunnel domain is modelled by means of a simple 1D modelling approach. It is in fact clear that detailed

6

simulations of the fire near field cannot be fully accomplished without accounting for the  interaction  with  the  remaining  part  of  the  tunnel  domain.  As  result,  detailed  flow field data in the fire near field are made available by the CFD solver including, backlayering  occurrence,  back-layering  distance,  smoke  stratification,  smoke  temperature, heat flux mapping, pollutant concentrations and so forth. At the same time, the overall interaction between fire near field and ventilation system, tunnel layout and eventually boundary conditions at the portals is maintained

## 6.2. A case study: a modern tunnel 1.2 km in length

The multiscale technique has been used to simulate a 1200 m long tunnel longitudinally ventilated. This layout is realistic and typical of a modern generic uni-directional road tunnel. A schematic of the tunnel layout is presented in Figure 63. The tunnel is 6.5 m high  with  standard  horseshoe  cross  section  of  around  53  m 2 and  hydraulic  diameter around 7.3 m. The same geometry of the East Dartford tunnel cross section has been used for the scope (see Figure 49). The tunnel is equipped with two groups of 5 jet fans pairs 50 m spaced, each group installed near a tunnel portal. The jet fans are rated by the manufacturer at the volumetric flow rate of 8.9 m 3 /s with a discharge flow velocity of 34 m/s.

Figure 63: Layout of the tunnel used as case study showing the relative positions of the fire, jet fans and portals (Not to scale).

<!-- image -->

Line chart

The fires are located in middle of the tunnel and 4 different sizes ranging from 10 MW to 100 MW are considered. The HRR is assumed to be constant and that steady state conditions  are  reached  within  the  tunnel.  The  multiscale  analysis  includes  7  different scenarios  involving  different  fire  sizes  and  active  ventilation  devices.  The  main characteristics of each scenario are resumed in Table 13.

Table 13: Summary of ventilation and fire scenarios analysed with the multiscale technique

|            | Fire Size   | Jet fan pairs #1- 2   | Jet fan pair #3   | Jet fan pair #4   | Jet fan pair #5   | Jet fan pairs #6 - 10   |
|------------|-------------|-----------------------|-------------------|-------------------|-------------------|-------------------------|
| Scenario 1 | 30 MW       | ON                    | ON                | OFF               | OFF               | OFF                     |
| Scenario 2 | 30 MW       | ON                    | ON                | ON                | ON                | OFF                     |
| Scenario 3 | 30 MW       | ON                    | ON                | ON                | ON                | ON                      |
| Scenario 4 | 30 MW       | OFF                   | OFF               | OFF               | OFF               | ON                      |
| Scenario 5 | 10 MW       | ON                    | OFF               | OFF               | OFF               | OFF                     |
| Scenario 6 | 50 MW       | ON                    | ON                | ON                | OFF               | OFF                     |
| Scenario 7 | 100 MW      | ON                    | ON                | ON                | ON                | OFF                     |

The  emergency  ventilation  strategy,  as  for  most  longitudinally  ventilated  tunnels, requires the ventilation system to push all the smoke downstream of the incident region in the same direction as the road traffic flow, thus avoiding the smoke spreading against the ventilation flow (back-layering effect). The vehicles downstream of the fire zone are assumed  to  leave  the  tunnel  safely.  All  the  studies  on  back  layering  show  that  the maximum critical  velocity  is  in  the  range  from  2.5  m/s  to  3  m/s.  Thus,  an  adequate ventilation system has to provide air velocities higher than this range in the region of the fire incident.

## 6.3. Characterization of the fire near field

The  characterization  of  the  fire  near  field  has  been  conducted  by  using  a  multiscale model  with  direct  coupling  approach.  This  approach  allows  for  the  computation  of detailed flow and temperature field data in the 3D-CFD sub-domain which includes the fire while the rest of tunnel layout is represented by adopting a 1D modelling.

A schematic of the coupling between 1D model of the far field and CFD model of the near field has been depicted in Figure 64.

Figure 64: Schematic of the multiscale model of a 1.2 km tunnel including portals, jet fans, and the CFD domain of the fire region. Contours of the temperature field show the fire plume. (Not to scale). The 1D-CFD interfaces have been highlighted in green

<!-- image -->

Engineering drawing

As  already  asserted  in the previous  sections, a critical point of the multiscale representation  is  the  positioning  on  the  1D-3D  interfaces  ( Γ i and Γ j in  Figure  64). Indeed, they must be located in a domain region where the flow is fully developed and is  characterized by mild velocity gradients. Thus, it is straightforward that the size of the 3D sub-domain ( L3D ) plays a crucial role in the accuracy of the global solution. This issue will be addressed in the next sections.

## 6.3.1. Assessment of the mesh requirements

The  computational  domain  has  been  discretized  using  quasi  structured  meshes  with refinements introduced close to each jet fan pairs and close to the fire source. Various full  CFD runs of the whole tunnel domain have been conducted to estimate the mesh requirements. Four different meshes  were  generated  and  the resulting solutions compared.  The  mesh  characteristics  are  resumed  in  Table  14.  The  symmetry  of  the solution across the longitudinal plane was also considered. Four examples of the mesh cross sections are presented in Figure 65. The data presented are relative to a 30 MW fire  scenario  and  ventilation  conditions  slightly  above  the  critical  velocity.  This condition could be achieved by activating 3 jet fan pairs upstream the fire.

Table 14: Grid independence study of the full CFD domain for a 30 MW fire and 3 operating jet fan pairs.

|       |   Mesh density [cells/m] |   predicted air velocity [m/s] | deviation from mesh 4   |
|-------|--------------------------|--------------------------------|-------------------------|
| mesh1 |                      105 |                           3.21 | -15.25%                 |
| mesh2 |                      695 |                           3.83 | 0.98%                   |
| mesh3 |                     2525 |                           3.80 | 0.32%                   |
| mesh4 |                     4125 |                           3.79 | -                       |

6

5

4

3

2

1

0

Figure 65: Examples of the different meshes used for half of the tunnel cross section and number of cells per unit length of tunnel.

<!-- image -->

Engineering drawing

The solution is shown to converge as the mesh is made finer. A coarse mesh of 100 cells/m leads to a 15% underestimation of the average ventilation velocity. But a finer mesh of 2500 cells/m leads to results within 0.3% of the prediction made with the finest mesh. Besides the comparison of the average quantities,  detailed  field  solutions  have been compared at Reference Sections 1 and 2, located 10 m and 100 m downstream of the fire source location, respectively. The location of these sections is shown in Figure 64.    The  comparison  of  the  longitudinal  velocity  and  temperature  fields  is  plotted  in Figure 66 for the Reference Section 1 and in Figure 67 for the Reference Section 2.

<!-- image -->

Engineering drawing

0

Figure 66: Comparison of the longitudinal velocity (left) and temperature (right) contours for meshes #1 to #4 in the tunnel at Reference Section 1 for a 30 MW fire. The velocity and temperature values are expressed in m/s and K respectively.

<!-- image -->

Engineering drawing

Figure 67: Comparison of the longitudinal velocity (left) and temperature (right) contours for meshes #1 to #4 in the tunnel Reference Section 2 for a 30 MW fire. Velocity and temperature values are expressed in m/s and K respectively

As expected from the previous results, the computed solutions show larger deviations for the courses meshes 1 and 2 while convergence of the temperature and velocity fields is  observed  for  finer  meshes  3  and  4.  Based  on  the  results,  grid  independence  is considered  reached  in  mesh  3  and  therefore,  all  the  following  simulations  have  been conducted using this mesh.

## 6.3.2. Effect of the 1D-CFD interface location

The  downstream  interface  boundary  between  1D  and  CFD  domain  must  be  located where the  flow  evolves  to  fully  developed.  Otherwise,  the  coupling  would  induce  an error  and  the  multiscale  results  would  depend  on  the  interface  location.  The  previous chapter  on  the  modelling  of  tunnel  flows  provides  the  sane  analysis  for  cold  flow scenarios. The boundary independence study conducted for the specific tunnel and jet fan  arrangement showed that notable accuracy in the computed mass flow rate (error smaller than 1%) could be achieved when the ratio between LD (distance from the fan to the downstream boundary interface) and Dh (tunnel hydraulic diameter ) is around 20.

In  order  to  identify  the  boundary  independence  limit  for  cases  including  fire-induced flows, several runs of the multiscale model were conducted for a range of fire sizes. In each  run  the  interface  was  placed  progressively  further  downstream  of  the  fire, increasing  the  longitudinal  extension  of  the  CFD  domain L3D (see  Figure  64)  and consequently  reducing  the  extension  of  the  1D  domain  by  the  same  amount.  The position of the upstream interface between 1D and CFD domain is not as critical as the downstream  one  where  the  focus  is  put  here,  but  fore  sake  of  generality  the  CFD domain is centered on the fire source. However, if the modeller is sure that during the simulated  scenarios  the  ventilation  velocity  does  not  change  direction  and  the  air velocity is super-critical (therefore no back-layering occurs), the upstream boundary can be  moved  significantly  closer  to  the  fire.  This  would  produce  a  further  reduction  of computing time.

In order to isolate the effect of the interface location on fire-induced flows, the jet fans at this stage are assumed to be located far away from the fire and thus simply modelled as a pressure difference between portals. This pressure difference is given by combining the characteristics curves of the operating fans.

A first analysis has been performed in order to clarify the dependence of the average bulk  flow  quantities  (temperature  and  velocity)  at  the  outlet  boundary  of  the  CFD domain. These values have an additional importance as they represent the input of the 1D model for the far field region located downstream of the fire. Figure 68 represents the average velocities and temperatures for longitudinal dimensions of the CFD domain increasing  from  20  m  to  600  m.  The  points  plotted  for LCFD equal  to  1200  m  are computed  by  using  the  full  CFD  model  and  represent  the  reference  values  in  each scenario. It can be easily seen that, for CFD domain lengths between 20 m and 200 m, the deviations in the average velocity from the reference values range between 6.5% and 40%; the variations  in  the  temperature  range  between  14%  and  21%.  No  appreciable variations can be observed when the CFD domain length is larger that 200 m.

Figure 68: Effect of the CFD domain length, LCFD, on the average longitudinal velocity and temperature at the outlet boundary of the CFD module. Units are in m/s and K respectively. Note that the shortest module length is 20 m.

<!-- image -->

Line chart

A second study has been performed in order to identify the dependence of the local flow field solutions on the dimension of the CFD domain. Also in this case, the full CFD data has  been  taken  as  reference  solution.  For  a  generic  flow  quantity θ ,  the  associated average error has been calculated with the following norm

<!-- formula-not-decoded -->

where CFD ϑ is the average predicted by the full CFD simulation, and j CFD , ϑ and j ms , ϑ are the values calculated in each grid point j belonging to the Reference Section of interest. The  subscript CFD and ms are  referred  to  the  full  CFD  and  multiscale  simulation results. Obviously, the summation over j is extended to all the grid points belonging to the specific Reference Section.

Figure 69: Effect of the CFD domain length LCFD on the error for the average longitudinal velocity and average temperature. Results for  top) Reference Section 1; bottom) Reference Section 2. Error calculated using Eq. (76).

<!-- image -->

Line chart

The effect of the interface location on average errors has been studied for four different fire  sizes  (10  MW,  30  MW,  50  MW  and  100  MW)  and  presented  in  Figure  69.  The results  show  that  the  error  does  not  depend  on  the  dimension  of  the  fire  within  that range.  Figure  70  and  Figure  71  present  the  field  results  at  Reference  Section  1  and Reference  Section  2,  respectively.  The  solution  obtained  with  a  20  m  long  domain provides  low  accuracy  (15%  error).  The  results  become  boundary  independent  and provide less than 1% error for domain lengths larger than 200 m (for Reference Section

1 at 10 m downstream of the fire source) and than 400 m (for Reference Section 2 at 100 m downstream of the fire source). Thus, highly accurate results  can be  achieved with domains whose downstream boundary is at a minimum distance of 100 m from the furthest location where a CFD accurate solution is required.

<!-- image -->

Engineering drawing

Figure 70: Effect of the CFD domain length LCFD on the horizontal velocity and temperature fields at Reference Section 1 for a 30MW fire. The velocity and temperature values are expressed in m/s and K respectively

<!-- image -->

Engineering drawing

0

0

0

Figure 71: Effect of the CFD domain length LCFD on the horizontal velocity and temperature fields at Reference Section 2 for a 30MW fire. Velocity and temperature values are expressed in m/s and K respectively

In  terms  of  the  distance  from  the  fire  to  the  downstream  boundary  interface LD (see Figure  64),  the  minimum  ratio  between LD and  the  tunnel  hydraulic  diameter DH is around 13. In a previous work Van Maele and Merci [97] simulated two different fire scenarios (3 kW and 30 kW) in a small scale tunnel (0.25×0.25 m 2 )  under ventilation conditions  close  to  the  critical  velocity.  The  CFD  solution  in  the  vicinity  of  the  fire plume became independent from the boundary location if the distance LD is at least 12 times the hydraulic diameter. The agreement between the present and previous result is excellent.

Combining  Figure  68  to  Figure  71  allows  identifying  a  range  of  CFD  sub-domain lengths between 20 and 200 m where the average quantities at the outlet boundary as well as temperature and velocity fields show high deviation from the reference full CFD solution.  In  particular,  average  and  flow  field  temperature  show  a  deviation  from  the CFD solution up to 25%; average and flow field velocities show a deviation up to 40%. However, if the CFD module is larger than 200 m, average and flow field deviations can be significantly reduced with error of few percents.

## 6.3.3. Comparison to full CFD solutions

The  solutions  obtained  with  the  multiscale  technique  and  direct  coupling  have  been compared  to  full  CFD  solutions  of  the  same  scenarios.  The  full  CFD  calculation included the full tunnel domain as well as the ventilation devices (i.e. jet fans). Based on the boundary independence study, the near field of the fire region was set to a length of  400  m.  A  description  of  the  ventilation  strategies  for  each  investigated  scenario  is given in Table 13.

Table 15: Comparison between Full CFD and Multiscale predictions for the 7 scenarios investigated. The multiscale results are obtained with direct coupling. The table presents only bulk flow data.

|            |           | Full Scale CFD mass flow   | Multiscale direct     | Multiscale direct   |
|------------|-----------|----------------------------|-----------------------|---------------------|
|            | Fire Size | rate [kg/s]                | mass flow rate [kg/s] | deviation           |
| Scenario 1 | 30 MW     | 216.10                     | 220.62                | 2.09%               |
| Scenario 2 | 30 MW     | 301.42                     | 301.44                | 0.01%               |
| Scenario 3 | 30 MW     | 435.19                     | 434.54                | 0.15%               |
| Scenario 4 | 30 MW     | 299.29                     | 296.05                | 1.08%               |
| Scenario 5 | 10 MW     | 204.52                     | 204.48                | 3.12%               |
| Scenario 6 | 50 MW     | 227.19                     | 234.28                | 0.02%               |
| Scenario 7 | 100 MW    | 194.28                     | 208.62                | 7.38%               |

The comparison has been performed both in terms of bulk flow and field data from the CFD sub-domain. The bulk flow solutions obtained with the multiscale model and the comparison to the full CFD data are given in Table 15.

The first scenario involves 3 jet fan pairs operating close to the north portal. This is the minimum number of fans required to guarantee velocities above the critical value for a 30 MW fire. The deviation between full CFD and multiscale predictions is very small, around 2%. Figure 72 shows the temperature and velocity fields computed with direct coupling for scenario 1. The multiscale model predictions compare very well to the full CFD  predictions. In particular no appreciable differences are observed in the temperature field. Very small differences are observed in the longitudinal velocity field. These small differences are due to the presence of the discharge cone generated by the operating  jet  fans  upstream  of  the  fire  source  which  are  included  in  the  full  CFD representation.

The same conclusions are reached when analyzing the results for scenarios 2 to 4. The differences in the predicted flow rate range between 0.01% and 1.4%. Field results for scenarios 2 to 4, presented in Figure 73 to Figure 75, confirm that high accuracy can be achieved.

For sake of simplicity, the comparison of the flow field data is not provided for scenario 5 to 7. However the deviations in the bulk flow predictions, resumed in Table 15, range between  0.02%  and  around  7%  for  the  100MW  fire  scenario.  However,  it  must  be stressed  that  the  simulations  of  tunnel  ventilation  flows  and  fires  suffers  of  high uncertainty on the real boundary conditions at the portals, effective wall roughness, fire load and its geometry, and throttling effects of vehicles. For these reasons, the largest error induced by using the multiscale model is by far within the uncertainty range of the enforced boundary conditions and it is acceptable.

The computational time required to run the full CFD model ranged between 48 and 72 hr.  The  multiscale  model  with  direct  coupling  runs  in  2  to  4  hours  depending  on particular scenario and initialization of the variables.

Figure 72: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 1. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain.

<!-- image -->

Engineering drawing

Figure 73: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 2. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain.

<!-- image -->

Engineering drawing

Figure 74: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 3. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain.

<!-- image -->

Engineering drawing

Figure 75: Comparison of results near the fire for the multiscale and the full CFD simulations for a fire of 30 MW and ventilation scenario 4. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain.

<!-- image -->

Engineering drawing

## 6.4. Characterization of the ventilation system performance

The  assessment  of  the  ventilation  system  performance  under  different  fire  hazards requires,  in  most  of  the  cases,  only  bulk  flow  data.  Such  issues  can  be  addressed  by using simple 1D models, but the final results can suffer of high uncertainty due to the simplistic representation of the fire source and the corresponding fire induced flows.

A significant improvement in the representation can be introduced by the adoption of a multiscale model with indirect coupling.

## 6.4.1. Calculation of the fan and fire characteristic curves

The adoption of indirect coupling strategies requires the calculation of the characteristic curves  of  the  near  field  regions.  Several  runs  of  the  near  field  CFD  model  are conducted,  varying  the  pressure  difference  across  the  domain  boundaries.  The  results are  presented  in  terms  of  bulk  flow  velocity  vs.  total  pressure  difference.    Figure  76 shows the characteristic curve of a single and a pair of operating jet fans. The curves describe the capability of jet fans to produce thrust and they are calculated adopting the methodology presented in the previous chapter.

Figure 76: Characteristic curves of a tunnel region 50 m long where an activated jet fan pair (and a single jet fan) is located: Pressure drop between inlet and outlet vs. Mass flow rate across the inlet. (CFD calculated).

<!-- image -->

Line chart

Figure 77: Characteristic curves of the tunnel region 400 m long where the fire is located: Pressure drop between inlet and outlet vs. Mass flow rate across the inlet (CFD calculated)

<!-- image -->

Line chart

The same approach has been followed to calculate the characteristic curves of the fire region. Different simulations have been conducted varying the total pressure difference across the domain and calculating the resulting bulk flow velocity. Figure 77 shows the resulting curves for different fire sizes in the range from 10 to 100 MW. The sensitivity of the results to the assumed temperature of the hot gases released by the fire source has been investigated in the experimentally measured range from 1100 to 1500 K. Despite the temperature difference of 400 K (almost 50% increment), the effect on the curve for the  10  MW  scenario  is  negligible  (~1%).  For  the  30  MW  and  50  MW  scenarios  the effect  is  smaller  than  5%,  and  for  the  100  MW  it  is  smaller  than  7%.  This  relatively small sensitivity is a point in favour of the simplified representation of the fire.

## 6.4.2. Comparison to full CFD solutions

The multiscale results obtained with indirect coupling have been compared to the full CFD solutions for cold flow and fire scenarios.

## 6.4.2.1. Cold flow scenarios

A previous analysis of cold flow scenarios has been performed to assess the capability of the ventilation system and whether or not the assumption of periodic behaviour for the jet fan train was acceptable. Also in this test case the analysis of the flow pattern established  for  10  operating  jet  fans  pairs  confirms  the  flow  periodic  behaviour  (see Figure 78).

Figure 78: Longitudinal velocity iso-contours, calculated using full CFD for 10 operating jet fans pairs. (Not to scale)

<!-- image -->

Engineering drawing

The multiscale calculations have been conducted with the jet fan characteristics curves implemented in the 1D model. The multiscale and full CFD predictions of the bulk flow in the tunnel as function of the number of operating jet fans are shown in Figure 79. It is seen that the adoption of the multiscale model, including the periodic flow hypothesis, induces a numerical error lower than 1.5% in all scenarios. In Figure 79, two different ventilation  scenarios  with  5  operating  jet  fans  pairs  have  been  considered.  The  first configurations uses all the north portal jet fans while the second uses all the south portal jet fans (see the configuration of the ventilation system as depicted in Figure 63).

The computational time required to run the full CFD model ranged between 48 and 72 hr.  The  multiscale  model  with  indirect  coupling  runs  almost  instantaneously  (few seconds).

Figure 79: Predictions of average velocity for cold flow scenarios. Comparison and error between multiscale and full CFD results.

<!-- image -->

Scatter plot

## 6.4.2.2. Fire scenarios

The  comparison  between  bulk  flows  computed  with  full  CFD  model  and    multiscale model is resumed in Table 16.

Table 16: Comparison between Full CFD, Multiscale, and 1D model predictions for the 7 scenarios investigated. The multiscale results are obtained with indirect coupling. The table presents only bulk flow data.

|            |           | Full Scale CFD mass flow   | Multiscale indirect   | Multiscale indirect   | 1D model              | 1D model   |
|------------|-----------|----------------------------|-----------------------|-----------------------|-----------------------|------------|
|            | Fire Size | rate [kg/s]                | mass flow rate [kg/s] | deviation             | mass flow rate [kg/s] | deviation  |
| Scenario 1 | 30 MW     | 216.10                     | 223.53                | 3.44%                 | 277.00                | 28.18%     |
| Scenario 2 | 30 MW     | 301.42                     | 305.58                | 1.38%                 | 356.00                | 18.11%     |
| Scenario 3 | 30 MW     | 435.19                     | 445.52                | 2.37%                 | 490.00                | 12.59%     |
| Scenario 4 | 30 MW     | 299.29                     | 300.25                | 0.32%                 | 351.00                | 17.28%     |
| Scenario 5 | 10 MW     | 204.52                     | 197.70                | 3.33%                 | 236.00                | 15.39%     |
| Scenario 6 | 50 MW     | 227.19                     | 242.74                | 6.85%                 | 310.00                | 36.45%     |
| Scenario 7 | 100 MW    | 194.28                     | 203.01                | 4.50%                 | 325.00                | 67.28%     |

Also in  this  case,  the  comparison  of  the  computed  bulk  flow  data  is  very  favourable with deviations ranging between 0.32% and 6.85%. It is worth to note that, the simple representation conducted  with  a  fully  1D  model  systematically  overpredicts  the capability of the ventilation system (up to 67% for a 100MW fire). This is due to the simplistic representation of the fire near field region and the inability in describing the high velocity gradients established in the vicinity of the fire.

The computational time required by full CFD simulations ranged between 48 h and 72 h while  multiscale  simulations  with  indirect  coupling  required  few  seconds  once  the characteristics curves are available. This is of great advantage  because  several ventilation  scenarios  can  be  explored  and  extensive  sensitive  analysis  and  parametric studies can be conducted.

## 6.4.3. A note of the fire throttling effect

The results contained in Table 15 and Table 16 show that the number of operating jet fans required to achieve critical ventilation velocity in the fire region varies with the fire size.  In  particular  2,  4  and  5  jet  fan  pairs  must  be  activated  to  provide  super-critical ventilation velocity for a 10 MW, 50 MW and 100 MW fire respectively. These results show that throttling effect of the fire is large.

Comparing the effect of the number of operating jet fans in cold flow scenarios (Figure 78) to the fire scenarios (Table 16), the fire throttling effect can be quantified at least for this specific tunnel layout. For a 100 MW fire, the mass flow when 5 jet fan pairs are activated  is  ~200  kg/s.  When  5  jet  fan  pairs  are  activated  in  cold  flow  scenarios,  the flow is ~290 kg/s. Thus, the effect of the 100 MW is to decrease the ventilation flow by more 30%. This is due to the additional fire induced pressure losses due to sudden air expansion, higher velocities in the tunnel generating higher frictional effects, buoyant effects  and  localized  losses  in  the  plume  region.  Obviously,  such  effects  will  be amplified for larger fires. Besides, it is worth to note that frictional and buoyant effects increase with the tunnel length, so the fire throttling effect can be severely magnified for longer tunnels.

The same conclusions were obtained experimentally on small scale tunnel fires by Lee and  Chaiken  [36]  and  very  recently  by  Harvey  and  Fuster  (2009)  [131].  The  latter provided a rough estimation of the fire induced pressure losses for a 70 MW and a 200 MW fire in a 2 km long tunnel. They concluded that a 200MW fire can induce 2 to 2.5 times higher pressure losses in comparison to the 70 MW one. However they could not give  any  conclusion  on the  actual  number  of  ventilation  devices  needed  to  cope  with specific fire hazards. In the present work such evaluation can be accurately performed in a  relatively  short  time  scale  since  the  main  features  of  fire  near  field  are  correctly reproduced  by  the  CFD  sub-domain  while  the  behaviour  of  the  remaining  tunnel (including  frictional  losses,  ventilation  device  behaviour,  portal  boundary  conditions etc.)  is  exactly  represented  by  the  1D  model  maintaining  the  coupling  between ventilation system and fire.

## 6.5. Concluding remarks

In  this  section  the  multiscale  modelling  approach has been  applied to simulate tunnel ventilation  flows  also  in  case  of  fire.  Both  direct  and  indirect  coupling  strategies  are used and compared to full CFD  predictions for steady state conditions. The methodology has been applied to a modern tunnel with 53 m 2 cross section and 1.2 km in  length.  Different  fire  scenarios  ranging  from  10  MW  to  100  MW  are  investigated varying the number of operating jet fans.

It is shown that the accuracy of the multiscale model is high when compared to the full CFD solution. In particular, the error for all the studied scenarios is below few percents. The  small  numerical  error  is  more  than  acceptable  when  compared  to  the  large uncertainty of the real meteorological conditions at the portals, actual fire load, effective lining roughness, presence of vehicles and obstructions, etc.

To the best knowledge of the author, this is the first time that a ventilation system has been  coupled  to  a  fire.  This  has  allowed,  among  other  things,  to  quantify  the  fire throttling effect, which is seen to be large and to reduce the flow up to 30% for a 100 MW fire.

The multiscale model has been demonstrated to be a valid technique for the simulation of complex  tunnel ventilation systems under different fire hazards. It can be successfully adopted to conduct parametric and sensitivity studies, to design ventilation systems,  to  assess  system  redundancy  and  to  assess  the  performance  under  different hazards  conditions.  Furthermore,  the  author  believes  that  the  multiscale  methodology represents the only feasible tool to conduct accurate simulations in tunnels longer than few kilometres, when the limitation of the computational cost becomes too restrictive.

In this section, the ventilation scenarios are set for super-critical velocities preventing the smoke back-layering. Thus, the assumption of 1D flow at the upstream boundary is guaranteed. In order to use the multiscale model to investigate sub-critical ventilation scenarios, the upstream boundary must be moved to ensure that all the back-layering is captured within the CFD domain. If otherwise, there will be a tunnel region close to the upstream boundary where the computed flow field will present deviation from the fullCFD solution as presented for the downstream boundary apply.

Parts of this work have been published in Fire Technology [105].

<!-- image -->

Icon

## Multiscale modelling of time-dependent tunnel ventilation flows and fires

## 7.1. Introduction

In  chapter  5  and  6  the  multiscale  modelling  approach  has  been  used  to  simulate  the behaviour  of tunnel ventilation flows  and  fires in steady state conditions.  The information  provided  by  this  type  of  simulations  is  fundamental  for  analysing  the effectiveness  of  the  ventilation  system  under  different  fire  hazards.  Typically  such analysis provides data related to the occurrence of back-layering, velocity and temperature  distributions  within  the  tunnel  domain,  velocity  profile  and  temperature fields in the vicinity of operating ventilation devices or close to the fire source.

However, a complete analysis of the ventilation system response and its interaction with the fire is a much more complex task. Indeed, when defining the optimum ventilation strategy for a given fire scenario, other significant issues arise. For instance, information

## 7

related  to  the  time  required  to  reach  the  critical  velocity  in  the  fire  region,  to  clear  a certain tunnel portion from smoke, or the temporal evolution of the smoke stratification, is fundamental to analyse the development of an emergency scenario. Furthermore, such data  are  fundamental  to  determine  the  evolution  of  hazardous  zones  in  the  tunnel domain,  to  design  evacuation  procedures  or  to  determine  the  correct  timing  for  the activation of fixed fire fighting systems (e.g. water mist, deluge or sprinkler systems).

Obviously, the amount variables that come into play when conducting time dependent analysis  increases  making  sensitivity  studies  or  parametric  analysis  more  complex. Indeed,  if  steady  state  analyses  require  mainly  peak  HRR  and  operating  ventilation devices,  time  dependent  analyses  require  inputs  data  related  to  the  detection  times, response  time  of  the  ventilation  system  and  fire  growth  curve.  Furthermore,  the characteristic  transient  time  ranges  from  5  min  for  the  detection  and  protection activation to 30 min for smoke moment. This last one increases with the tunnel length.

The application the multiscale model for time dependent analysis of tunnel ventilation flows and fires is the subject of this chapter. The great engineering value of multiscale techniques is boosted in this application since the number of input variables, the size of the computational domain and the temporal duration of the event to be simulated are so large that full-scale CFD would demand very large computational resources, most likely out of reach for applications to real systems.

Typically,  only  few  full  CDF  runs  are  conducted  and  sensitivity  studies  to  the  main variables  (e.g.  detection  time,  fire  growth  curve  and  operating  ventilation  devices) cannot be provided.

## 7.2. A case study: a modern tunnel 1.2 km in length

The multiscale technique has been used to simulate a 1200 m long tunnel longitudinally ventilated whose layout is the same as the one presented in the chapter 6. A schematic of the tunnel layout is presented in Figure 80. The tunnel is 6.5 m high with standard horseshoe  cross  section  of  around  53  m 2 and  hydraulic  diameter  around  7.3  m.  The same geometry of the East Dartford tunnel cross section has been used for the scope (see Figure 49).

The tunnel is  equipped  with  two  groups  of  5  jet  fans  pairs  50  m  spaced,  each  group installed  near  a  tunnel  portal.  The  jet  fans  are  rated  by  the  manufacturer  at  the volumetric flow rate of 8.9 m 3 /s with a discharge flow velocity of 34 m/s.

Figure 80: Layout of the tunnel used as case study showing the relative positions of the fire, jet fans and portals (Not to scale).

<!-- image -->

Line chart

The fire is located in middle of the tunnel and only a 30 MW fire is considered for this specific application.

The  fire  growth  curve  has  been  built  on  the  basis  of  the  prescriptions  proposed  by Carvel [17] that apply to tunnel fires involving typical material mixtures for European HGVs cargos [8]. The author observed that the typical t 2 fire representation [6] was not fitting  any  of  the  experimental  data  and  proposed  a  two-step  linear  approximation. During the first step the fire would grow slowly up to 1÷2 MW, while during the second step, the growth rate would be significantly higher (up to 15 MW/min). The changing of the fire regimes usually takes place after a delay phase usually as long as few minutes (from 2 to 6). The author observed also that the delay phase length and the fire growth rate are somehow correlated to the ventilation flows experienced by the fire during its development.  For  the  time  dependent  analysis  conducted  in  this  section  an  average temporal duration of the delay phase equal to 4 min has been chosen; during this phase the  fire  growth  rate  is  assumed  to  be  equal  to  0.5  MW/min.  The  following  phase  is characterized by a higher growth rate equal to 15 MW/min. The peak HRR (30 MW) is reached after around 350 s.

Figure 81: Fire growth curve, delay phase and detection times considered in the time dependent multiscale simulations. The fire growth curve is based on the work of Carvel (2008) [17].

<!-- image -->

Line chart

Three different ventilation strategies have been considered for the analysis: 1 st strategy involving operating jet fans pairs from #1 to #3; 2 nd strategy involving operating jet fans pairs from #1 to #5; 3 rd strategy involving operating jet fans pairs from #1 to #10. The fan characteristic curves are the ones computed in the previous chapter and depicted in Figure 76. The jet fans are supposed to reach full thrust after 10 s. However, it has been found that the impact of this variable on the results is negligible being the characteristic time scale of tunnel ventilation flows almost 2 orders of magnitude larger.

Three  initial  simulations  have  been  run  adopting  a  constant  value  of  detection  time (indicated  as  TD  hereafter)  equal  to  2  min  representing  an  average  value  for  slow growing fire detected by means of fibre optic linear detection cables [132]. Eventually, shorter  detection  times  could  be  expected  for  faster  growing  fires  (i.e.  pool  fires)  or more efficient detection techniques based on video analysis systems [133]. On the other hand,  longer  detection  times  can  be  expected  if  the  fire  is  shielded  by  obstacles  or located underneath the vehicle [134]. For these reasons, after running three base cases characterized by a 2 min detection time, it has been varied to 1.5 min and 2.5 min and the effects on the development of the emergency scenario have been assessed.

The temporal duration of the simulated fire emergency is equal to 10 min being this the time required to reach steady state conditions in the tunnel domain. An overview of the time-dependent ventilation scenarios analysed in this chapter is given in Table 17.

Table 17: Summary of the ventilation scenarios considered in the time dependent analysis

|            | Fire Size   | Jet fan pairs #1- 3   | Jet fan pair #4-5   | Jet fan pairs #6 - 10   |   Detection time [min] |
|------------|-------------|-----------------------|---------------------|-------------------------|------------------------|
| Scenario 1 | 30 MW       | ON                    | OFF                 | OFF                     |                      2 |
| Scenario 2 | 30 MW       | ON                    | ON                  | OFF                     |                      2 |
| Scenario 3 | 30 MW       | ON                    | ON                  | ON                      |                      2 |
| Scenario 4 | 30 MW       | ON                    | OFF                 | OFF                     |                    2.5 |
| Scenario 5 | 30 MW       | ON                    | ON                  | OFF                     |                    2.5 |
| Scenario 6 | 30 MW       | ON                    | ON                  | ON                      |                    2.5 |
| Scenario 7 | 30 MW       | ON                    | OFF                 | OFF                     |                    1.5 |
| Scenario 8 | 30 MW       | ON                    | ON                  | OFF                     |                    1.5 |
| Scenario 9 | 30 MW       | ON                    | ON                  | ON                      |                    1.5 |

The  multiscale  simulations  have  been  conducted  by  using  a  multiscale  model  with direct coupling approach. As already pointed out in the previous sections this approach allows the computation of detailed flow and temperature field data in the 3D-CFD subdomain which includes the fire while the rest of tunnel layout is represented by adopting a  1D  modelling  approach.  More  details  on  the  coupling  technique  can  be  found  in chapter 4

A schematic of the coupling between 1D model of the far field and CFD model of the near field has been depicted in Figure 82.

Figure 82: Schematic of the multiscale model of a 1.2 km tunnel including portals, jet fans, and the CFD domain of the fire region. Contours of the temperature field show the fire plume. (Not to scale). The 1D-CFD interfaces have been highlighted in green

<!-- image -->

Engineering drawing

As  already  asserted  in  the previous  chapters,  a  critical point of the  multiscale representation is the positioning of the 1D-3D interfaces ( Γ i and Γ j in Figure 82). Indeed, they  must  be  located  in  a  domain  region  where  the  flow  is  fully  developed  and  is characterized by mild velocity gradients. This issue was already addressed for the same tunnel  layout  ad  fire  sizes  in  the  previous  chapter.  The  analysis  confirmed  that,  if boundary is  located  at  a  distance  larger  that  13  times  the  tunnel  hydraulic  diameters, average  and  flow  field  deviations  can  be  significantly  reduced  with  error  of  few percents in comparison to full CFD solutions. On the basis of this estimation, the outlet boundary has been located at distance equal to 20 times the tunnel diameter (~ 150 m) and therefore, the length of the CFD sub-domain is equal to 300 m being the fire located in the middle.

The assumption of 1D flow at the upstream boundary must be maintained during the whole  calculation  and  also  during  the  initial  stages  of  the  fire  emergency  when  the ventilation  system  is  not  yet  operating  or  the  ventilation  flow  is  still  sub-critical.  In these  cases  it  must  be  ensured  that  all  the  initial  back-layering  is  captured  within  the CFD domain. If otherwise, there will be a tunnel region close to the upstream boundary where  the  computed  flow  field  will  present  deviation  from  the  full-CFD  solution  as presented  for  the  downstream  boundary.  For  time  dependent  calculations  a  rough estimation  of  the  smoke  front  velocity  and  the  consequent  travelled  distance  can  be based on the correlation presented in [135]

<!-- formula-not-decoded -->

where c is an empirical constant equal to 0.8, g is the gravity, T the smoke temperature, Q the fire HRR, λ the fire radiative losses, cp the air specific heat at constant pressure, W the  tunnel  width, ρ o the  ambient  density  and To the  ambient  temperature.  The  smoke temperature in the fire zone can be assumed to vary between 1100 K and 1500 K (lower values can be expected if the flame does not touch the ceiling). A rough approximation of the temperature evolution beneath the ceiling can be performed by using the energy equation for 1D tunnel bulk flows [5].

However, a posteriori post-processing of the CFD results must always be conducted to clarify this matter.

## 7.3. Multiscale model results

Figure  83  shows  the  temporal  evolution  of  the  mass  flow  rate  through  the  tunnel  as computed by the multiscale model for the first 3 base scenarios characterized by a TD of 2 min. Supercritical ventilation conditions, corresponding to bulk flow velocity larger than 3m/s, are reached after 244 s, 190 s and 156 s after the fire outbreak (124 s, 70 s and 36 s from the moment of the ventilation system activation) for scenario 1 2 and 3, respectively. At this moment in time the fire is still in its incipient phase and its HRR is lower than 2MW.

Figure 83: Time dependent evolution of the mass flow rate through the tunnel for scenario 1, 2 and 3 (see Table 17). The time to detection is 2 min. Supercritical conditions (vair&gt; 3m/s) are reached after 244 s, 190 s and 160 s for scenario 2 and 3 respectively

<!-- image -->

Line chart

Figure 84 shows the conditions within the tunnel 120 s after the fire outbreak. As it can be  seen  velocity  and  temperature  profiles  are  still  symmetric  since  the  ventilation system has not been yet activated. The smoke fronts are located around 110 m far away from the fire source (~40 m from the 1D-CFD interfaces). This first result shows that when  the  ventilation  system  is  activated  the  back-layering  nose  is  by  far  within  the upstream boundary of the computational domain.

Figure 84: Multiscale results in the vicinity of the fire computed 2 min after the fire outbreak for scenario 1, 2 and  3 (see Table 17). The ventilation system is about to be started. Velocity and temperature values are expressed in m/s and K respectively. The longitudinal coordinates start at the upstream boundary of the corresponding CFD domain. (not to scale)

<!-- image -->

Bar chart

Figure 85: Temperature profiles computed by the multiscale model 3 min after the fire outbreak for scenario 1, 2 and 3 (see Table 17). The ventilation system is operative since 1 min. Temperature values are expressed in K. (not to scale)

<!-- image -->

Bar chart

## Ventilation scenario 1 (3 JF pairs)

Figure 86: Longitudinal velocity profiles computed by the multiscale model 3 min after the fire outbreak for scenario 1, 2 and 3 (see Table 17). The ventilation system is operative since 1 min. Velocity values are expressed in m/s. (not to scale)

<!-- image -->

Engineering drawing

Figure  85  and  Figure  86  show  the  temperature  and  velocity  profiles  in  the  tunnel domain 3 min after the fire outbreak for ventilation scenarios from 1 to 3. The higher performance of ventilation strategy #3 involving 10 operating jet fan pairs is clear since the back-layering nose is completely removed from the tunnel region upstream of the fire. Differently, back-layering regions (100 m and 70 in length) can be still observed for ventilation  scenarios  #1  and  #2  involving  3  and  5  operating  jet  fan  pairs, respectively. The average ventilation velocity in the fire region is around 1.8 m/s, 2.8 m/s and 5 m/s for ventilation scenarios 1, 2 and 3, respectively. Furthermore it can be seen that, given the relatively low ventilation velocity and fire size (smaller that 2 MW), smoke stratification is maintained both in the upstream and downstream regions for all the scenarios. Therefore, both the regions upstream and downstream of the fire can be used for evacuation purposes within the first 3 min from the fire outbreak.

Figure 87: Temperature and velocity profiles 5 min (left column) and 10 min (right column) after the fire outbreak for scenario 1, 2 and 3 (see Table 17). Temperature and velocity values are expressed in K. and m/s, respectively (not to scale)

<!-- image -->

Bar chart

Figure 87 presents the computed temperature and flow fields 5 min and 10 min after the fire  outbreak  for  ventilation  scenarios  from  #1  to  #3.  The  temperature  contours computed 5 min (left column in Figure 87) after the fire outbreak show that the backlayering has been removed in the three ventilation scenarios while the smoke front is located at a distance downstream of the fire source of 350 m and 450 m for scenarios 1 and  2,  respectively.  Since  the  ventilation  velocities  achieved  during  the  emergency scenario 3 are considerably higher (see Figure 83), the smoke front has already reached the tunnel portal 5 min after the fire outbreak. The results show that smoke stratification downstream of the fire is lost at distances of 30, 60 and 100 m for scenarios 1,2 and 3, respectively.  Therefore,  only  the  tunnel  regions  upstream  of  the  fire  and  these  short distances  downstream  can  be  used  for  evacuation  purposes.  The  average  ventilation velocity in the fire region is around 3.5 m/s, 5 m/s and 7 m/s for ventilation scenarios 1, 2  and  3,  respectively.  Given  the  larger  ventilation  flows  attained  in  the  ventilation scenario 3, considerably lower temperatures (around 100 K lower than for ventilation scenario 1) are achieved within the tunnel domain.

Temperature  and  velocity  profiles  within  the  tunnel  domain  10  min  after  the  fire outbreak are resumed in Figure 87 right column. Both the fire and the ventilation flows have reached steady state conditions while the smoke front has reached the downstream portal  for  scenarios  1,  2  and  3.  The  average  ventilation  velocity  in  the  fire  region  is around 4 m/s, 5.5 m/s and 7.5 m/s for ventilation scenarios 1, 2 and 3, respectively.

Beside  the  time  required  to  reach  supercritical  ventilation  velocities  (indicated  as  TC hereafter) in the fire region, another important variable is the time required to remove the back-layering (indicated as TB hereafter) from the fire upstream region. In particular it has been computed that the fire upstream region can be cleared after 255 s, 220 s and 187 s after the fire outbreak (135 s, 100 s and 67 s from the moment of the ventilation system activation) for ventilation scenarios 1, 2 and 3, respectively.

The multiscale analysis conducted allows for an assessment of the impact of the number of  activated  jet  fan  pairs  on  TC  and  TB.  In  particular  it  can  be  calculated  that  the simultaneous activation of 10 jet fan pairs (ventilation scenario 3) instead of 3 jet fan pairs  (ventilation  scenario  1)  induces  a  reduction  on  TC  and  TB  by  36  %  and  30  %, respectively. However, it must be asserted that the TD (120 s) still represents a large portion of TC and TB and therefore its reduction is desirable as it impacts considerably their values. Table 18 gives an overall view on the numerical findings.

Table 18: Summary of the ventilation scenarios considered and numerical findings

|            | Fire Size   | Jet fan pairs #1- 3   | Jet fan pair #4-5   | Jet fan pairs #6 - 10   |   Detection time (TD) [min] |   Time to critical velocity (TC) [s] |   Time to remove back |
|------------|-------------|-----------------------|---------------------|-------------------------|-----------------------------|--------------------------------------|-----------------------|
| Scenario 1 | 30 MW       | ON                    | OFF                 | OFF                     |                           2 |                                  244 |                   255 |
| Scenario 2 | 30 MW       | ON                    | ON                  | OFF                     |                           2 |                                  190 |                   220 |
| Scenario 3 | 30 MW       | ON                    | ON                  | ON                      |                           2 |                                  156 |                   187 |
| Scenario 4 | 30 MW       | ON                    | OFF                 | OFF                     |                         2.5 |                                  290 |                   300 |
| Scenario 5 | 30 MW       | ON                    | ON                  | OFF                     |                         2.5 |                                  220 |                   260 |
| Scenario 6 | 30 MW       | ON                    | ON                  | ON                      |                         2.5 |                                  188 |                   222 |
| Scenario 7 | 30 MW       | ON                    | OFF                 | OFF                     |                         1.5 |                                  214 |                   212 |
| Scenario 8 | 30 MW       | ON                    | ON                  | OFF                     |                         1.5 |                                  160 |                   181 |
| Scenario 9 | 30 MW       | ON                    | ON                  | ON                      |                         1.5 |                                  126 |                   152 |

Among the remaining cases, scenarios 4 to 6 are characterized by a 2.5 min detection time  and  3,  5  and  10  operating  jet  fan  pairs,  respectively.  Scenarios  from  7  to  9  are characterized by a 1.5 min detection time and 3, 5 and 10 operating jet fans respectively.

A  careful  analysis  of  the  TC  values  shows  that  a  variation  in  the  time  to  detection produces a simple shift in the time required to attain critical velocity in the fire region. Indeed, for scenarios 1, 4 and 7 characterized by 3 operating jet fan pairs, the system required around 130 s (from the moment of activation) to generate critical ventilation velocities in the fire zone. Similarly, for scenarios 2, 5 and 8 characterized by 5 jet fan pairs, and for scenarios 3, 6, and 9 characterized by 10 jet fan pairs, it requires around 70 s and 40 s, respectively. The previous data show that TC can be reduced by 70% by increasing the number of operating jet fan pairs from 3 to 10.

These results confirm that the values of TC are mainly dependent on detection time and ventilation strategies (e.g. number  of  operating  jet  fans)  while  they  are  almost insensitive to the specific fire stage. Due to the presence of the initial low HRR stage, the ventilation system  is able in most  of the ventilation scenarios to generate supercritical  ventilation  velocity  before  the  fire  has  reached  a  considerable  size  and therefore  its  impact  on  the  ventilation  system  response  in  negligible.  Indeed  for  the fastest  response  case  (scenario  9)  the  fire  size  is  1.25  MW  while  for  the  slowest response case (scenario 4) the fire size is around 15 MW (half of the full size). It must be asserted that the fire growth could have a larger impact on the value of TC for faster developing fires (e.g. pool fires).

The analysis conducted provides also information related to the time required to remove the  back-layering  (TB)  defined  as  the  moment  when  ambient  conditions  are  reestablished  just  upstream  of  the  fire  source.  The  whole  set  of  computed  vales  is contained  in  Table  18  and  plotted  in  Figure  88  which  highlights  the  dependence between number of operating jet fans, time to detection and time  required to remove back-layering (computed from the moment of the ventilation system activation).

Figure 88: Dependence between number of operating jet fan pairs, TD, and time required to remove back-layering computed from the moment of the ventilation system activation.

<!-- image -->

Line chart

It  is  clearly  shown  how,  due  to  the  further  location  of  the  smoke  front  when  the ventilation system is activated, the larger is the time to detection the larger is the time required by a constant number of jet fans (once activated) to remove the back-layering. Figure 88 also clarify that impact of TD on TB becomes smaller when the number of jet fans simultaneously activated is larger; indeed, the curves tend to get closer when the number of operating fans is larger.

Although ventilation scenarios involving 3, 5 or 7 operating jet fan pairs are equivalent from  a  steady-state  point  of  view  since  able  of  removing  back-layering,  they  do  not have the same dynamic response. Figure 89 shows the correlations between the number of  active  jet  fan  pairs,  detection  time  and  the  time  required  for  remove  back-layering (computed, in this case, from the fire outbreak). TB values will be the sum of detection time and response time of the ventilation system. While the former depends mainly on the technology used for detection (linear detectors, video analysis or flame detectors), the latter will depends on the ventilation strategy adopted (i.e. number of available jet fan pairs) and on the tunnel geometry.

Figure  89:  Dependence  between  number  of  operating  jet  fan  pairs,  TD,  and  time  required  to  remove back-layering computed from the fire outbreak

<!-- image -->

Line chart

Figure  89  clarifies  also  the  great  impact  of  the  detection  time  on  the  time  to  remove back-layering. Indeed, a relative small variation on the detection time (30 s) has a huge impact  on  the  minimum  number  of  ventilation  devices  needed  to  fulfil  a  given requirement on TB.

## 7.4. Concluding remarks

In  this  section  the  multiscale  modelling  approach  has  been  applied  to  simulate  real tunnel fire emergency. The multiscale model, run in direct coupling fashion, has been used to solve time dependent problems.

The methodology has been applied to a 1.2 km long tunnel (53 m 2 cross section) under a 30  MW  fire  hazard.  The  fire  growth  curve  has  been  approximated  following  a  two linear step approximation. 3 different ventilation scenarios involving 3, 5 and 10 jet fan pairs have been simulated. The time to detection has been ranged between 1.5 and 2.5 min. The simulated time interval was equal to 10 min starting from the fire outbreak.

Being the model run in time dependent fashion, it allows for a complete analysis of the ventilation system response and its interaction with the fire. For instance, information on the time required to reach critical velocity conditions in the fire region, to remove back-layering or related  to  the  evolution  of  the  smoke  stratification  in  the  fire  region could be obtained. Such data are fundamental to determine the evolution of hazardous zones in the tunnel domain, to design evacuation procedures or to determine the correct timing  for  the  activation  of  fixed  fire  fighting  systems  (e.g.  water  mist,  deluge  or sprinkler systems). The computed data confirm the great impact of detection time and number of jet fans on the ventilation system response. A smaller impact is induced by the fire  growth curve but this is likely due to the design fire used for the simulations characterized by an initial low growth rate phase. Larger impact could be expected for faster growing design fires. Similar considerations can be done for longer tunnel, where the response of the ventilation system is intrinsically slower and therefore the fire has longer available time to evolve towards significantly larger size.

The  effectiveness  of  the  model  when  dealing  with  for  sub-critical  fire  scenarios  has been also confirmed. The crucial point is represented by the correct sizing of the CFD sub-domain in order to capture the back-layering occurrence. Some  empirical correlations related to this issue are provided.

A reduction of the required computing time of almost 2 orders of magnitude is expected also  for  time  dependent  calculations.  However,  a  direct  assessment  of  such  reduction could not be performed as done for steady state simulations since, based on estimations, each transient full CFD simulation could take up to 3 months. These results confirm that the  multiscale  methodology  represents  the  only  feasible  tool  to  conduct  accurate simulations in tunnels longer than few kilometres, when  the limitation of the computational cost becomes too restrictive.

Given  the  low  computational  complexity  of  the  multiscale  model  in  comparison  to traditional computing  techniques, the model  enables for  simultaneous  economic optimizations of the overall ventilation/detection system. For instance, we can think of a coupled ventilation/detection system which is designed to cope with a 30 MW fire and that, for evacuation purposes, requires to be able to fully control the smoke spread (i.e. remove  back-layering)  within  200  seconds  from  the  fire  outbreak.  Having  this  goal fixed,  the  following  combined  ventilation/detection  systems  would  be  equivalent  (see Figure 89):

1. 4 jet fan pairs + detection technique able to detect the fire within 1.5 min
2. 8 jet fan pairs + detection technique able to detect the fire within 2 min
3. 14 jet fan pairs (extrapolated value) + detection technique able to detect the fire within 2.5 min

Being the three different options equally performing, the final design must be chosen on the  basis  of  an  economic  analysis  of  the  initial  investment  (including  ventilation  and detection systems) and maintenance costs.

## 8 Conclusions and future works

The work presented is related to the numerical simulations of tunnel ventilation flows and  fires.  Different  numerical  techniques  have  been  developed  and  validated  against experimental data from real tunnels including 1D models, CFD models and multiscale models.

The developed 1D model has been validated against experimental data from the Frejus tunnel (IT) where it has been shown to be able to predict with reasonable accuracy the evolution  of  the  ventilation  conditions  within  the  tunnel  during  a  fire  emergency. Typically  1D  models  are  unsuitable  to  simulate  the  fluid  behaviour  in  regions characterized  by  high  temperature  or  velocity  gradients  typically  encountered  in  the vicinity of the fire plume, ventilation devices or complex interconnections of galleries. In  order  to  deal  with  such  complex  flow  conditions,  they  mainly  rely  on  empirical correlations  or  calibration  constants  to  be  defined  on  the  basis  of  experimental measurements or detailed CFD calculations.

The CFD models have been developed in FLUENT environment and used to simulate tunnel  ventilation  flows both  in  cold  (i.e.  ambient  conditions)  and  fire  scenarios.  The numerical sub-models have been chosen on the basis of an extensive literature review involving all the related papers published in the last 25 years on archival journals of the field.  Great  care  has  also  been  given  to  the  correct  choice  of  the  grid  size  which  has been systematically refined until no substantial variations both in the local field data and integral values were observed.

A  first  validation  work  has  been  undertaken  by  using  cold  flow  data  measured  in  9 different ventilation scenarios in the Norfolk Tunnels, Sydney (AU). A significant level of accuracy (average relative deviation around 17%) has been achieved. A comparison to the experimental findings from two small scale tunnel fire scenarios studied by Wu and  Bakar  [33]  confirmed  also  the  ability  of  the  CFD  model  to  predict  the  critical velocity with a reasonable level of accuracy (~ 25%).

The  CFD  analyses  have  also  shown  that  significant  computational  resources  were required to simulate a single steady state ventilation or fire scenario in relatively short tunnels.  The  computational  time  become  a  severe  limitation  when  the  full  CFD approach is adopted to deal with fire or ventilation in long tunnels or when analysing a broad range of ventilation strategies. Furthermore, the high computational cost leads to the  practical  problem  that  arises  when  the  CFD  model  has  to  consider  boundary conditions  in  locations  far  away  from  the  region  of  interest  (i.e.  tunnel  portals  or ventilation stations located long distances away from the fire). In these cases, even if only a limited region of the tunnel has to be investigated, an accurate solution of the flow  movement  requires  that  the  numerical  model  includes  all  the  active  ventilation devices  and  the  whole  tunnel  layout.  For  typical  tunnels,  this  could  mean  that  the computational domain is several kilometres long

Multiscale  methods,  based  on  hybrid  1D-CFD  computational  techniques,  represent  a way  to  avoid  such  high  computational  complexity.  They  have  never  been  applied  to simulate  tunnel  ventilation  flows  and  fires  and  this  work  represents  only  the  starting point  for  a  more  comprehensive  use  of  these  techniques  addressing  tunnel  related problems.

Multiscale models are based on the evidence that in the vicinity of operating jet fans or close to the fire source the flow field has a complex 3D behaviour with large transversal and longitudinal temperature and velocity gradients. The flow in these regions needs to be  calculated  using  CFD  tools  since  any  other  simpler  approach  would  only  lead  to inaccurate results. However, it has been demonstrated for cold flow scenarios and for fire  scenarios  that  some  distance  downstream  of  these  regions,  the  temperature  and velocity gradients become milder and the flow behaviour can be accurately represented by  1D  models.  The  work  presents  also  a  wide  description  on  the  1D-CFD  coupling techniques as well as gives emphasis to the control of the numerical error.

Multiscale  modelling  techniques  have  been  first  applied  to  simulate  steady  cold ventilation  flows  in  the  Dartford  Tunnels  (UK)  where  an  extensive  experimental campaign has been also undertaken. The comparison to experimental data shows that highly accurate results could be achieved both when modelling the local flow field in the vicinity of operating jet fans as well as bulk flows within the tunnel. The developed multiscale model has also been applied to include the effect of the fire. The comparison to full CFD solutions shows that the maximum flow field error can be reduced to less than few percents, but providing a significant reduction in computational time.

Time dependent analyses of tunnel ventilation flows and fires have also been conducted providing,  for  instance,  information  related  to  the  time  required  to  reach  the  critical velocity in the fire region, to clear a certain tunnel portion from smoke, or the temporal evolution  of  the  smoke  stratification  in  the  fire  region.  These  details  are  indeed fundamental  to  analyse  the  development  of  an  emergency  scenario  to  determine  the evolution of hazardous zones in the tunnel domain, to design evacuation procedures or to  determine  the  correct  timing  for  the  activation  of  fixed  fire  fighting  systems  (e.g. water mist, deluge or sprinkler systems).

The advantages of multiscale modelling techniques when dealing with tunnel ventilation  flows  and  fires  are  mainly  related  to  the  considerable  computational  time reduction in comparison to traditional full CFD approaches. Indeed, it has been shown that multiscale simulations of steady tunnel ventilation flows and fires in a 1.2 km long tunnel  are  almost  2  orders  of  magnitudes  faster  than  full  CFD  simulations.  A  direct assessment of  such  reduction  for  time  dependent  simulations  could  not  be  performed since each transient full CFD simulation could take up to 3 months. The reduction in the computing  time  is likely to be larger for longer tunnels where  the multiscale methodology represents the only feasible tool to conduct accurate simulations.

Given  the  low  computation  complexities,  multiscale  techniques  can  be  successfully adopted to conduct parametric and sensitivity studies, to design ventilation systems, to assess  their  redundancy  and  performance  under  different  fire  hazards.  The  great engineering  value  is  boosted  when  conducting  time  dependent  simulations  since  the number of input variables is larger and includes detection time and fire growth curve. Such  broad  spectrum  of  simulations  cannot  be  performed  adopting  traditional  CFD models due to the required computing time.

Another significant advantage is related to the simulation of the whole tunnel domain including  the  ventilation  devices.  This  allows  for  an  accurate  assessment  of  the  fire throttling effect and for a prediction of the minimum number of jet fans needed to cope with a certain fire size. For instance, it has been shown that a 100 MW fire in a 1.2 km long tunnel is likely to decrease the ventilation flow by more 30% due to the additional fire  induced  pressure  losses.  Obviously,  such  effects  will  be  severely  amplified  for larger  fires  and  longer  tunnels.  It  is  worth  to  note  that  1D  model  could  be  used  to address this issue but it  has been shown that they are likely to underestimate the fire induced losses.

One of the most important issues on the use of multiscale model for tunnel ventilation and fires is related to the location of the interfaces between 1D and CFD models. These boundaries must be located in regions of the domain where the temperature or velocity gradients are negligible and the flow behaves largely as 1D. These dictate the length of the CFD domain. This required length is case specific and in general depends on tunnel geometry, installation details of ventilation devices, presence of obstacle, etc. Based on the  test  cases  chosen  in  this  work,  which  represent  real  modern  tunnel  layouts,  a minimum length of the CFD domain for an accurate simulation of ventilation and fire induced flows could be provided.

Being  this  only  a  pioneering  work  on  the  subject,  there  are  several  other  issues  that deserve to be addressed in the next years or so. Some of them are directly related to the sub-models adopted for the simulations while others related to new possible applications and integration with different simulation tools.

A  first  improvement  could  be  represented  by  the  adoption  of  more  sophisticated combustion models (e.g. Eddy break up or mixture fraction models). The results could be compared to the simplified fire representation based on volumetric heat source as the one used in this work. On the basis of the literature review conducted, it is believed that only marginal improvements on the prediction capabilities can be obtained but this still represents  a  due  step.  Eventually,  comparisons  to  detailed  flow  field  and  temperature measurements can be introduced to address this issue.

Other  possible  applications  are  represented  by  longer  tunnels  equipped  with  different ventilation  system  types  (e.g.  transverse and  semi-transverse  systems).  The  first application  will  be  the  Frejus  tunnel  where  several  sets  of  experimental  data  are available.

An initial screening of other possible CFD solvers to be coupled to the developed 1D model has been undertaken. Other CFD packages are OpenFoam (general purpose opensource CFD code based on final volumes), FDS (open source CFD code based on finitedifferences)  and  CD-Adapco  (general  purpose  commercial  CFD  code  based  on  finite volume). The main requirement for the CFD code to be useful for multiscale computing is  the  accessibility.  Indeed,  the  boundary  conditions  of  the  CFD  model  must  be dynamically  updated  during  the  solution  procedure  in  order  to  achieve  a  global multiscale convergence.

Other interesting applications are represented by the coupling to risk analysis tools in order to perform enhanced studies of ventilation system performance and comprehensive  risk  analyses  involving  a  large  number  multiscale  runs.  The  current state-of-the-art,  due  to  the  huge  time  required  by  full  CFD  simulations,  uses  only  a limited number of CFD runs and then extrapolates their results to similar scenarios. The lower  cost  could  be  of  great  value  also  for  performing  cost  optimization  during  the design process of the tunnel ventilation and detection systems.

## REFERENCE LIST

- [1] Haack A., (2002), 'Current safety issues in traffic tunnels', Tunnelling and Underground space technology, 17: 117-127
- [2] Perard,  M.  (1996),  'Statistics  on  breakdowns,  accidents  and  fires  in  French  road  tunnels', Proceedings  of  the  1 st international  Conference  on  Tunnel  Incident  Management,  Korsor, Denmark, 13 -  15 May, 347-365
- [3] Carvel R.. Malair G. (2004), 'A history of fire incidents in tunnels', In The Handbook of Tunnel Fire Safety (R. O. Carvel and A. N. Beard, Eds.), Thomas Telford Publishing, 231-266, London, 2005.
- [4] Carvel R. (2007), 'Tunnel fire safety systems', EuroTransport, 5(6): 39-43
- [5] Ingason H., Fire Dynamics in tunnel (2005), chapter in, The handbook of tunnel fire safety, Ed A. Beard and R. Carvel, Thomas Telford, London, UK
- [6] Drysdale, D. (1998). An Introduction to Fire Dynamics. Wiley, England, 2 nd edition.
- [7] Carvel, R., (2010), 'Fire Dynamics During the Channel Tunnel Fires', Proceedings of the Fourth International Symposium on Tunnel Safety and Security, Frankfurt am Main, Germany, March 17-19, 463470
- [8] H.  Ingason  and  A.  Lönnermark,  Heat  release  rates  from  heavy  goods  vehicle  trailer  fires  in tunnels, Fire Safety Journal, Volume 40, Issue 7, October 2005, Pages 646-668.
- [9] World Road Association, PIARC technical committee on Road Tunnel Operation (C5), (2004), 'Fire and smoke control in Road Tunnels'
- [10] Babrauskas,  V.  and  Grayson  (1992.b)  Heat  Release  in  Fires.  S.J.  Editors,  Elsevier  Applied Science.
- [11] Massachusetts  Highway  Department  (1995)  Memorial  tunnel  fire  ventilation  test  program comprehensive test report
- [12] EUREKA 499 Report (1996), Fire in transport tunnels, report on full scale tests. Duesseldorf: Studiengesellschaft Stahlanwendung e.V.
- [13] Lemaire T., Kenyon Y., Large Scale Fire Tests in the Second Benelux Tunnel,Fire Technology, 42, 329-350, 2006
- [14] Lautenberger, C., Torero, J.L., Fernandez-Pello, C., (2006). Understanding materials flammability.  Chapter  in  Flammability  testing  of  materials  used  in  construction,  transport  and mining, Woodhead Publishin limited, Cambirdge UK
- [15] Bundy M., Ohlemiller, T., (2003). Bench-Scale Flammability Measures for Electronic Equipment, NIST Report 7031
- [16] Lonnemark  A,  Ingason  H.,  The  Effect  of  Air  Velocity  on  Heat  Release  Rate  and  Fire Development during Fires in Tunnels, Fire Safety Science-proceedings of the ninth international symposium, 701-712
- [17] Carvel,  R.,  'Design  fires  for  tunnel  water  mist  suppression  systems',  Proceedings  of  3rd International Symposium on Tunnel Safety and Security', Stockholm, 12-14 March, 2008
- [18] Lemaire  A,  van  de  Leur  PHE,  Kenyon  YM,  Safety  Proef:  TNO  Metingen  BeneluxtunnelMeetrapport, TNO, TNO-Rapport 2002-CVB-R05572, 2002.
- [19] Loennermark A., Ingason, H. (2005), Gas temperatures in heavy goods vehicle fires in tunnels, Fire Safety Journal 40: 506-527
- [20] Bendelius A., 'Tunnel ventilation - state of the art', In The Handbook of Tunnel Fire Safety (R. O. Carvel and A. N. Beard, Eds.), Thomas Telford Publishing, 231-266, London, 2005.

- [21] Chen T.Y., Lee T.T., Hsu C.C. (1998), 'Investigation of piston-effect and jet fan-effect in model vehicle tunnels', Journal of Wind Engineering and Industrial Aerodynamics, 73: 99-110
- [22] Jang  H.M.,  Chen  F.  (2000),  'A  novel  approach  to  the  transient  ventilation  of  road  tunnels', Journal of Wind Engineering and Industrial Aerodynamics', 28: 15-36.
- [23] Torbergsen, L.E., Paaske, P., Schieve, C. (2002), 'Numerical simulation of the fire and smoke propagation in long railway tunnels', Proceeding of the 4 th International conference on Tunnel Fires, Basel Switzerland, 2-4 December, ITC conferences Ltd, 330-346.
- [24] Jagger S., Grant G., 'Use of tunnel ventilation for fire safety', In The Handbook of Tunnel Fire Safety  (R.  O.  Carvel  and  A.  N.  Beard,  Eds.),  Thomas  Telford  Publishing,  231-266,  London, 2005
- [25] PIARC  (2008),  'Road  tunnels,  Operational  strategies  for  emergency  ventilation',  Technical committee C3.3 Tunnel operations, Working Group No. 6 Ventilation and fire Controll, World Road Association
- [26] Jojo  S.M.  Li,  W.K.  Chow  (2003),  Numerical  studies  on  performance  evaluation  of  tunnel ventilation safety systems Tunnelling and Underground Space Technology 18 435-452
- [27] Thomas PH (1958) The movement of buoyant fluid against a stream and venting of underground fires. Fire Research note:351.
- [28] Oka Y, Atkinson GT (1995) Control of smoke flow in tunnel fires. Fire Safety Journal 25(4): 305-22.
- [29] Kunsch  JP  (2002)  Simple  model  for  control  of  fire  gases  in  a  ventilated  tunnel.  Fire  Safety Journal 37(1): 67-81.
- [30] Vauquelin O, Wu Y (2006) Influence of tunnel width on longitudinal smoke control. Fire Safety Journal 41: 420-426
- [31] Oucherfi,  M.,  Gay,  B.,  Mos,  A.,  Carlotti,  P.,  (2009),  'Definition  and  optimisation  of  the efficiency of smoke extraction in a road tunnel', 13th international Symposium on Aerodynamics and ventilation of vehicle tunnels
- [32] Chasse P., Apvrille J-M. (1999). A new 1D computer model for fires in complex underground networks. Fire in Tunnels Conference, Lion. 201-222.
- [33] Wu Y, Bakar MZA (2000) Control of smoke flow in tunnel fires using longitudinal ventilation systems - a study of the critical velocity. Fire Safety Journal 35: 363-390
- [34] Hinkley PL. (1970), The flow of hot gases along an enclosed shopping mall. A tentative theory. Fire Research Note No. 807
- [35] William D. Kennedy (1997) Critical Velocity - Past, Present and Future (Revised 6 June 1997). American Public Transportation Association's Rail Trail Conference in Washington, DC.
- [36] Lee CK, Chaiken RF, J.M. Singer JM (1979) Interaction between duct fires and ventilation flow: an experimental study. Combustion Science &amp; Technology 20: 59-72
- [37] Hwang C.C, Edwards J.C. (2005), The critical ventilation velocity in tunnel fires-a computer simulation, Fire Safety Journal 40 (2005) 213-244
- [38] Atkinson,  G.T.  and  Wu,  Y.  (1996).  Smoke  Control  in  Sloping  Tunnels,  Fire  Safety  Journal, 27(4): 335-34
- [39] Ko G.H., Kim, G.R., Ryou H.S. (2010), 'An Experimental Study on the Effect of Slope on the Critical Velocity in Tunnel Fires', Journal of fire sciences, 28:27-47
- [40] Hu L.H., Huo R., Chow W.K. (2008), Studies on buoyancy-driven back-layering flow in tunnel fires, Experimental Thermal and Fluid Science 32: 1468-1483
- [41] Carvel R.O., Beard A.N., Jowitt P.W., Drysdale D., 'Variation of heat release rate with forced longitudinal ventilation for vehicle fires in tunnels', Fire Safety Journal 36 (2001) 569-596.

- [42] Carvel R., Marlair G. (2005), 'A history of experimental tunnel fires', chapter in, The handbook of tunnel fire safety, Ed A. Beard and R. Carvel, Thomas Telford, London, UK
- [43] Forney  G.P.,  Moss  W.F.,  'Analyzing  and  exploiting  numerical  characteristics  of  zone  fire models', NISTIT 4763, March 1992
- [44] Charters D.A., Gray, W.A., McIntosh, A. C., (1994) A computer model to assess fire hazards in tunnels (FASIT), Fire Technology 30,1.
- [45] Suzuki,  K.,  Tanaka  T.,  Harada  K.,  Tunnel  Fire  Simulation  Model  with  Multi-Layer  Zone Concept, Fire Safety Science-proceedings of the ninth international symposium, 713-724
- [46] Riess I.,  Bettelini  M.,  Brandt  R.  (2000).  'Sprint  -  a  design  tool  for  fire  ventilation',  10th  Int. Symp. on Aerodynamics and Ventilation of Vehicle Tunnels, Boston.
- [47] Greuer R. E.(1977), Study of mine fires and mine vemtilation, Part I, Computer simulations of mine ventilation systems under the influence of mine fires, Department of the interior bureau of mines, Washington D.C.
- [48] Tullis, J. P. (1989), Hydraulics of pipelines, John Wiley &amp; Sons, New York
- [49] U. S. Bureau of Mines, (1995), 'MFIRE users manual Version 2.20'.
- [50] Dai G., Vardy A.E. (1994). 'Tunnel temperature control by ventilation'. Proc 8th int symp on the Aerodynamics and Ventilation of Vehicle Tunnels, Liverpool, UK, 6/8 July, 175-198
- [51] West A., Vardy A.E., Middleton B., Lowndes J.F.L. (1994) 'Improving the efficacy and control of  the  Tyne  Tunnel  ventilation  system',  Proceedings   of  the  1st  International  Conference  on Tunnel Control and Communication, Basel, Switzerland, 28-30 Nov, 473-489
- [52] Riess I., Bettelini M. (1999). 'The Prediction of Smoke Propagation Due to Tunnel Fires'. 1st International Conference Tunnel Fires and Escape from Tunnels, Lyon, May 1999
- [53] Riess I.,  Bettelini  M.,  Brandt  R.  (2000).  'Sprint  -  a  design  tool  for  fire  ventilation'.  10th  Int. Symp. on Aerodynamics and Ventilation of Vehicle Tunnels, Boston, November 2000
- [54] NTIS. (1980) 'User's guide for the TUNVEN and DUCT programs'. Publication PB80141575. National Technical Information Service, Springfield, V A. 27.
- [55] Schabacker  J.,  Bettelini  M.,  Rudin  Ch.  (2002).  'CFD  study  of  temperature  and  smoke distribution in a railway tunnel'. Tunnel Management International, Volume 5, Number 3
- [56] L.H.  Cheng,  T.H.  Ueng,  C.W.  Liu.  Simulation  of  ventilation  and  fire  in  the  underground facilities. Fire Safety Journal 36 (2001) 597-619.
- [57] Ferro  V.,  Borchiellini  R.,  Giaretto  V.  (1991).    "Description  and  Application  of  a  Tunnel Simulation  Model"  "Aerodynamics  and  Ventilation  of  Vehicle  Tunnels"  Elsevier  Applied Science, London, pp. 487÷512.
- [58] Borchiellini  R.,  Ferro  V.,  Giaretto  V.  "Transient  Thermal  Analvsis  of  Main  Road  Tunnel"  In "Aerodynamics  and  Ventilation  of  Vehicle  Tunnels"  Mechanical  Engineering  Publications Limited London  1994,  pp. 17÷31  (8th  International  Symposium  on  Aerodynamics  and Ventilation of Vehicle Tunnels, Liverpool UK, 6-8 July 1994).
- [59] Jacques E, (1991) Numerical simulation of complex road tunnels. Proceedings of Aerodynamics and Ventilation of vehicle tunnels conference: 467-486
- [60] Parsons  Brinckerhoff  Quade  &amp;  Douglas,  Inc.,  'Subway  Environmental  Design  Handbook Volume II Subway Environment Simulation (SES) Computer Program Version 3 Part 1: User's Manual' , prepared in draft for the U.S. Department of Transportation, October 1980.
- [61] William D. Kennedy (1997) Critical Velocity - Past, Present and Future (Revised 6 June 1997). American Public Transportation Association's Rail Trail Conference in Washington, DC.
- [62] Jang  H,  Chen  F  (2002)  On  the  determination  of  the  aerodynamic  coefficients  of  highway tunnels. Journal of wind engineering and industrial aerodynamics 89 (8): 869 - 896.

- [63] Fox  RW,  McDonald  AT  (1995)  Introduction  to  fluid  mechanics  4th  edition.  John  Wiley  and Sons, Singapore.
- [64] Chandrashekar, M. &amp; Wong, F. C. (1982). Thermodynamic System Analysis - A graph-theoretic Approach. Energy, Vol.7 No.6, pp.539-566.
- [65] Quarteroni, A. (2008), 'Modellistica numerica di problemi differenziali', Springer, Italy, Milano
- [66] Versteeg  HK,  Malalasekera  W  (2007)  An  introduction  to  computational  fluid  dynamics,  the finite volume method. 2nd ed. Pearson Prentice Hall, Glasgow.
- [67] PIARC (1995), Tunnel routiers: emission, ventilation, environnement, Paris.
- [68] Incropera, F.P., DeWitt, D.P.(1996), 'Introduction to heat transfer, 3 rd edition',  John Wiley  &amp; Sons, New York
- [69] Fluent Inc. FLUENT 6.2 User's Guide. 2005.
- [70] Ferziger  J.H.,  Peric  M.  (2002),  'Computational  methods  for  fluid-dynamics,  3 rd edition', Springer Verlag, Berlin
- [71] Patankar, S.V., Spalding, D.B. (1972), 'A calculation procedure for Heat, Mass and momentum Tranfer in Three dimensional parabolic Flows', Int. J. Heat Mass Transfer, 15: 1787
- [72] Bettelini,  M.  (2009),  'Managing  the  longitudinal  air  velocity  in  long  road  tunnels',  13 th international Symposium on Aerodynamics and ventilation of vehicle tunnels
- [73] Bettelini, M., Glarey L., Koeofler A., Croci S., Di Noia L. (2001), 'The new Mont Blanc Tunnel - A milestone in Tunnel safety', International conference International tunnel forum', Basel, 4-6 December
- [74] Ingason, H., Bergqvist, A., Loennemark, A., Frantzich, H., Hasselrot, K. (2005), 'Räddningsinsatser i vägtunnlar', Räddningsverket, Karlstad, ISBN 91-7253-256-4 (in Swedish only).
- [75] Idelchik  I.  E.,  'Handbook  of  Hydraulic  Resistance  2 nd Edition',  Hemisphere  Publishing Corporation
- [76] McGrattan K., Miles S., (2008), 'Modeling  Enclosure fires using computational Fluid Dynamics' in 'The SFPE handbook of Fire Protection Engineering 4 th edition',  National  fire protection association, Quincy, Massachusetts, US
- [77] Olenick, S., Carpenter, D. (2003), 'An updated international survey of computer models for fire and smokes', journal of fire protection Engineering, 13:87-110.
- [78] Cox,  G.  (1995),  'Compartment  fire  modelling',  Combustion  fundamental  of  fire,  Academic press, London
- [79] Cox,  G.  (1998),  'Turbulent  closure  and  the  modelling  of  fire  using  CFD',  Philosophical transaction of  the royal society, A. 356, 2835
- [80] Novozhilov,  V.  (2001),  'Computational  fluid  dynamic  modelling  of  compartment  fires', Progress in energy and combustion science, 27: 611-666
- [81] Fletcher,  D.  F.,  Kent,  J.  H.  (1994),'Numerical  Simulations  of  Smoke  Movement  from  a  Pool Fire in a Ventilated Tunnel', Fire Safety Journal 23, 305-325
- [82] Woodburn PJ, Britter RE (1996) CFD simulation of tunnel fire - part I. Fire Safety Journal 26: 35-62
- [83] Woodburn PJ, Britter RE (1996) CFD simulation of tunnel fire - part II. Fire Safety Journal 26: 63-90
- [84] Chow, W.K. (1998),' On Smoke Control for Tunnels by Longitudinal Ventilation', Tunnelling and Underground Space Technology, Vol. 13, No. 3, pp. 271-275, 1998
- [85] Karki  KC,  Patankar  SV  (2000)  CFD  model  for  jet  fan  ventilation  systems.  Proceedings  of Aerodynamics and Ventilation of vehicle tunnels conference

- [86] Gao P.Z.,Liu S.L., Chow W.K., Fong N.K. (2004), 'Large eddy simulations for studying tunnel smoke ventilation', Tunnelling and Underground Space Technology 19: 577-586
- [87] Bari  S.,  Naser,  J.,  (2005),  'Simulation  of  smoke  from  a  burning  vehicle  and  pollution  levels caused  by  traffic  jam  in  a  road  tunnel',  Tunnelling  and  Underground  Space  Technology  20: 281-290
- [88] Lee,  S.R.,  Ryou,  H.S.  (2006),  'A  numerical  study  on  smoke  movement  in  longitudinal ventilation tunnel fires for different aspect ratio', Building and Environment 41:719-725
- [89] McGrattan, K., Hamins, A. (2006), 'Numerical Simulation of the Howard Street Tunnel Fire', Fire Technology, 42, 273-281
- [90] Ballesteros-Tajadura, R., Santolaria-Morros, C., Blanco-Marigorta E. (2006), 'Influence of the slope in the ventilation semi-transversal system of an urban tunnel', Tunnelling and Underground Space Technology 21: 21-28
- [91] Lin, C.j., Chuah, Y.K. (2007), 'A study on long tunnel smoke extraction strategies by numerical simulation', Tunnel. Underg. Space Technol., doi:10.1016/j.tust.2007.09.003
- [92] Jae Seong Roh, J.S., Ryou, H.S., Kim, D.H., Jung, W.S., Jang, Y.J. (2007),  'Critical velocity and  burning  rate  in  pool  fire  during  longitudinal  ventilation',  Tunnelling  and  Underground Space Technology 22: 262-271
- [93] Abanto, J., Reggio, M., Barrero, D., Petro, E., (2006), 'Prediction of fire and smoke propagation in an underwater tunnel', Tunnelling and Underground Space Technology 22: 90-95
- [94] Kim,  E.  Woycheese,  J.P.,  Dembsey,  N.A  (2007),  'Fire  Dynamics  Simulator  (Version  4.0) Simulation for Tunnel Fire Scenarios with Forced, Transient, Longitudinal Ventilation Flows',Fire Technology DOI: 10.1007/s10694-007-0028-2
- [95] Galdo  Vega,  M.,  Marıa  Arguelles  Dıaz,  K,  Fernandez  Oro,  J.M.,  Ballesteros  Tajadura,  R., Santolaria  Morros,  C.  (2007),  'Numerical  3D  simulation  of  a  longitudinal  ventilation  system: Memorial Tunnel case', Tunnelling and Underground Space Technology, doi:10.1016/j.tust.2007.10.001
- [96] Rusch,  D.,  Blum,  L.,Moser,  A.,  Roesgen,  T.  (2008),  'Turbulence  model  validation  for  fire simulation by CFD and experimental investigation of a hot jet in crossflow', Fire Safety Journal, doi:10.1016/j.firesaf.2007.11.005
- [97] Van Maele K., Merci B. (2008), Application of RANS and LES field simulations to predict the critical  ventilation velocity  in longitudinally  ventilated horizontal tunnels', Fire Safety Journal 43: 598-609
- [98] Kashef,  A.,  Benichou  N.  (2008),  'Investigation  of  the  Performance  of  Emergency  Ventilation Strategies  in  the  Event  of  Fires  in  a  Road  Tunnel  -  A  Case  Study',  Journal  of  FIRE PROTECTION ENGINEERING, Vol. 18: 165-198
- [99] Jain, S., Kumar, S., Kumar, S., Sharma, T.P. (2008), 'Numerical simulation of fire in a tunnel: Comparative  study  of  CFAST  and  CFX  predictions',  Tunnelling  and  Underground  Space Technology 23: 160-170
- [100] Cheong, M.K., Spearpoint, M.J., Fleischmann, C.M. (2009), 'Calibrating an FDS Simulation of Goods-vehicle  Fire  Growth  in  a  Tunnel  Using  the  Runehamar  Experiment',  Journal  of  FIRE PROTECTION ENGINEERING, Vol. 19
- [101] Nmira, F., Consalvi, J.L., Kaiss, A., Fernandez-Pello, A.C., Porterie, B., (2009), 'A numerical study of water mist mitigation of tunnel fires', Fire Safety Journal, 44: 198-211
- [102] Colella F, Rein G, Borchiellini R, Carvel R, Torero JL, V. Verda V, 'Calculation and Design of Tunnel Ventilation Systems using a Two-scale Modelling Approach', Building and Environment, 44, 2357-2367, 2009.
- [103] Colella,  F.,  Rein,  G.,  Carvel,  R.,  Reszka,  P.  Torero,  J.L.  (2010),  'Analysis  of  the  ventilation systems in the Dartford tunnels using a multi-scale modelling approach', Tunnel. Underg. Space Technol., doi:10.1016/j.tust.2010.02.007

- [104] The  Handbook of Tunnel  Fire  Safety  (R.  O.  Carvel  and  A.  N.  Beard,  Eds.),  Thomas  Telford Publishing, 231-266, London, 2005
- [105] Colella  F.,  Rein  G.,  Borchiellini  R.,  Torero  J.L.,  'A  Novel  Multiscale  Methodology  for Simulating Tunnel Ventilation Flows during Fires', Fire Technology, (in press).
- [106] Fluent Inc. FLUENT 6.2 User's Guide. 2005.
- [107] B.E. Launder, D.B. Spalding (1974) 'The numerical computation of turbulent flows', Comput. Methods Appl. Mech. Engrg; 3 (2): 269-289.
- [108] Van  Maele,  K.,  Merci,  B.,  (2006),  'Application  of  two  buoyancy-modified  kε turbulence models to different types of buoyant plumes', Fire Safety Journal, 41:122-134
- [109] Nam S., Bill Jr. RG. (1993), 'Numerical simulation of thermal plumes', Fire Safety journal, 21: 231-256
- [110] Hara,  T.,  Kato,  S.,  (2004),  'Numerical  simulations  of  thermal  plumes  in  free  space  using  the standard kε model', Fire Safety Journal 39. 105-129
- [111] Hue,  X.,  Ho,  J.C.,  Cheng,  Y.M.  (2001),  'Comparison  of  different  combustion  models  in enclosure fire simulation', Fire Safety Journal, 36:37-54
- [112] Yan, Z., Holmstedt G. (1999), 'A two-equation turbulence mode and its application to a buoyant diffusion flame', Int J. Heat and Mass Transfer, 42:1305-1315
- [113] Cox G, Kumar S (2002) Modelling enclosure fires using CFD. In: The SFPE handbook for fire safety engineering, 3rd edn. NFPA, Massachusetts International, Quincy
- [114] Lonnemark A, H. Ingason H (2005) Gas temperature in heavy goods vehicles fires in tunnels. Fire safety journal 40: 506-527
- [115] Heskestad G (2002) Fire plumes, Flame height and air entrainment. In: The SFPE handbook for fire safety engineering, 3rd edn. NFPA, Massachusetts International, Quincy
- [116] Loennermark A. &amp; Ingason H. (2008), The influence of tunnel cross-section on temperature and fire  development,  3rd  International  symposium  on  Tunnel  Safety  and  Security,  Stockholm, Sweden ,March 12-14
- [117] Ingason H. (2008), Model scale tunnel tests with water spray, Fire Safety Journal 43: 512-528
- [118] Drysdale  D.  (2000)  An  introduction  to  Fire  Dynamics  II  edition,  John  Wiley  &amp;  Sons  Inc. Hoboken, USA
- [119] Schlichting H (1979) Boundary layer theory 7th ed. McGraw-hill, New York
- [120] Lacasse,  D.,  Turgeon,  E.,  Pelletier,  D.  (2004),  'On  the  judicious  use  of  the  kε model,  wall functions and adaptivity', International Journal of Thermal Sciences, 43:925-938
- [121] Reszka  P,  Steinhaus  T,  Biteau  H,  Carvel  RO,  Rein  G,  Torero  JL  (2007)  A  Study  of  Fire Durability  for  a  Road  Tunnel  Comparing  CFD  and  Simple  Analytical  Models.  EUROTUN07 Computational Methods in Tunnelling, Wien. http://hdl.handle.net/1842/1892
- [122] Merci, B., (2008), 'One-dimensional analysis of the global chimney effect in the case of fire in an inclined tunnel', Fire Safety Journal 43: 376-389
- [123] Formaggia, L., Gerbeau, J.F., Nobile, F., Quarteroni, A., (2001), 'On the coupling of 1D and 3D Navier-Stokes equations for flow problems in compliant vessels' Comput. Methods Appl. Mech. Engrg 191: 561-582
- [124] Motenegro, G., (2002), 'Simulazione 1D-Multi D  di flussi instazionari e reagenti in sistemi di scarico ed aspirazione in motori a combustione interna', PhD thesis, Dipartimento di Energetica, Politecnico di Milano
- [125] Mossi.  M.  (1999),  'Simulation  of  benchmark  and  industrial  unsteady  compressible  turbulent fluid flows', PhD thesis, Mechanical Engineering Department, EPFL

- [126] Rey, B., Mossi, M., Molteni, P., Vos, J., Deville, M. (2009), 'Coupling of CFD software for the computation of unsteady flows in tunnel networks',  13 th international Symposium  on Aerodynamics and ventilation of vehicle tunnels
- [127] Geiger, S., Huangfu, Q., Reid, F., Mattha, S., Coumou, D., Belayneh, M., Fricke, C., Schimd, K. (2009),  'Massively  Parallel  Sector  Scale  Discrete  Fracture  and  Matrix  Simulations',  SPE Reservoir Simulation Symposium held in The Woodlands, Texas, USA, 2-4 February 2009
- [128] Quarteroni,  A.,  Valli,  A.  (1999),  'Domain  Decomposition  Methods  for  Partial  Differential Equations', Oxford Science Publications, Oxford.
- [129] Houzeaux,  G.,  Codina,  R.  (2004),  'A  Dirichlet/Neumann  domain  decomposition  method  for incompressible turbulent flows on overlapping subdomains', Computers &amp; Fluids: 33: 771-782
- [130] Fluent Inc. (2006), 'FLUENT 6.3 UDF manual'.
- [131] Harvey, N., Fuster T. (2009), 'Design fire heat release rate selection - impacts for road tunnels', 13 th international Symposium on Aerodynamics and ventilation of vehicle tunnels
- [132] Koffmane,  G.,  Hoff,  H.,  (2010),  'More  than  Just  Fire  Detection:  Fibre  Optic  Linear  Heat Detection  (DTS)  enables  Fire  Monitoring  in  Road-  and  Rail-Tunnels',  Fourth  International Symposium on Tunnel Safety and Security, Frankfurt am Main, Germany, March 17-19
- [133] Rogner, A., (2010), 'Safety and Reliability of Fire Detection Systems in Road Tunnels', Fourth International Symposium on Tunnel Safety and Security, Frankfurt am Main, Germany, March 17-19
- [134] Liu,  Z.G.,  Kashef  A.,  Lougheed,  G.D.,  Crampton,  G.,  Ko,  Y.,  Hadjisophocleous,  (2009), 'Parameters affecting the performance of detection systems in road tunnels', 13th international Symposium on Aerodynamics and ventilation of vehicle tunnels
- [135] Heselden,  A.J.M.,  'Studies  of  Fire  and  Smoke  Behavior  Relevant  to  Tunnels',  Current  Paper CP66/78, Building Research Establishment, 1978.