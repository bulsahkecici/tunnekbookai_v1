<!-- image -->

Logo

## FIXED FIRE FIGHTING AND EMERGENCY VENTILATION SYSTEMS FOR HIGHWAY TUNNELS - LABORATORY TESTING REPORT

<!-- image -->

Photograph

FHWA-HIF-23-022

## Technical Report Documentation Page

| 1. Report No. FHWA-HIF-23-022                                                                                                 | 2. Government Accession No. TBA                              | 3. Recipient's Catalog No. TBA                                                                                  |
|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| 4. Title and Subtitle Fixed Fire Fighting and Emergency Ventilation Systems for 7. Principal Investigator(s): William Connell | Matthew Bilson,                                              | Highway Tunnels - Research Report 5. Report Date May 2023 6. Performing Organization Code TBA WSP - Hasan Raza, |
| 8. Performing Organization Report TBA 9. Performing Organization WSP USA, Inc. One Penn Plaza                                 | and Address                                                  | Name 10. Work Unit No. (TRAIS) TBA Contract or Grant No.                                                        |
| 250 West 34 th Street New York, NY, 10119 11. DTFH6114D00048                                                                  | 250 West 34 th Street New York, NY, 10119 11. DTFH6114D00048 | 12. Sponsoring Agency Name and Address Federal Highway Administration U.S. Department of Transportation         |
|                                                                                                                               |                                                              | 13. Type of Report and Period Covered TBA                                                                       |
| 1200 New Jersey Avenue, SE Washington, DC 20590                                                                               | 1200 New Jersey Avenue, SE Washington, DC 20590              | 14. Sponsoring Agency Code                                                                                      |

## 15. Supplementary Notes

IFAB provided the testing services (Max Lakkonen, Babett Peters, Alexander Schmidt, Alexander Sasz)

## 16. Abstract

The Federal Highway Administration (FHWA) is currently researching the use of fixed fire fighting systems (FFFS) in  road  tunnels.  The  objective  of  this  research  project  is  to  identify  and  address  the  current industry's ability to consider the operational integration of highway tunnel emergency ventilation systems (EVS) with installed  fixed  fire  fighting  systems  (FFFS).  The  research  program  comprises  a  literature survey, an industry workshop, computer modeling, physical testing, and a summary report. This report documents  the  physical  testing.  Testing  was  conducted  in  a  model  tunnel  (approximately  1:4  scale relative to similar full-size) in February 2022. The tests considered the ability of an FFFS to improve smoke  management  in  a  longitudinal  ventilation  condition.  Measurements  of  velocity,  temperature, pressure, humidity, and surface temperature were recorded, and video footage was taken. Three different nozzles were used in the tests and measurements of the nozzle spray patterns are reported. Some tests were modeled using the computational fluid dynamics (CFD) software Fire Dynamics Simulator (FDS).

## 17. Key Words

Fixed  fire  fighting  system,  FFFS,  deluge,  water  mist,  tunnel,  tunnel

ventilation, CFD, FDS, testing, nozzle characterization

19. Security Classif. (of

this report)

UNCLASSIFIED

Form DOT F 1700.7(8-72)

21. No. of Pages

TBA

Reproduction of completed page authorized

20. Security Classif. (of

this page)

UNCLASSIFIED

18. Distribution Statement

No restrictions.

22. Price

## Notice

This document is disseminated under the sponsorship of the U.S. Department of Transportation in the interest of information exchange. The U.S. Government assumes no liability for the use of the information contained in this document.

The U.S. Government does not endorse products or manufacturers. Trademarks or manufacturers' names appear in this document only because they are considered essential to the objective of the document. They are  included  for  informational  purposes  only  and  are  not  intended  to  reflect  a  preference,  approval,  or endorsement of any one product or entity.

## Non-Binding Contents

Except for the statutes and regulations cited, the contents of this document do not have the force and effect of law and are not meant to bind the States or the public in any way. This document is intended only to provide information regarding existing requirements under the law or agency policies.

## Quality Assurance Statement

The  Federal  Highway  Administration  (FHWA)  provides  high-quality  information  to  serve  Government, industry, and the public in a manner that promotes public understanding. Standards and policies are used to ensure and maximize the quality, objectivity, utility, and integrity of its information. FHWA periodically reviews quality issues and adjusts its programs and processes to ensure continuous quality improvement.

## ACRONYMS

| ABBREVIATION   | DETAIL                                                                    |
|----------------|---------------------------------------------------------------------------|
| ASHRAE         | American Society of Heating, Refrigerating and Air-Conditioning Engineers |
| CFD            | Computational fluid dynamics                                              |
| EVS            | Emergency ventilation system                                              |
| FDS            | Fire Dynamics Simulator                                                   |
| FFFS           | Fixed fire fighting system                                                |
| FHRR           | Fire heat release rate                                                    |
| FHWA           | Federal Highway Administration                                            |
| NFPA           | National Fire Protection Association                                      |

## SUMMARY

The Federal Highway Administration (FHWA) has been conducting research into the use of fixed fire fighting systems (FFFS) in road tunnels. The objective of this research is to identify industry's current ability to consider the integration of highway tunnel emergency ventilation systems (EVS) with the installed fixed fire fighting system, and to then develop a set of suggested practices on the integration of FFFS and the EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (Fixed Fire Fighting and Emergency Ventilation Systems for  Highway  Tunnels  -  Literature  Survey  and  Synthesis,  Federal  Highway  Administration, FHWA-HIF-20-016).
2. Industry workshop and report (including workplans for computer modeling and testing) [2] (Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Workshop Report, Federal Highway Administration, FHWA-HIF-20-060).
3. Computer modeling research [3] (Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Computer Modeling Report, Federal Highway Administration, FHWA-HIF22-021).
4. Laboratory scale testing.
5. Research report and suggested practices.

This document is the laboratory scale testing report. Tests were conducted in a model tunnel (approximately 1:4 scale relative to similar full-size) with longitudinal ventilation. Measurements including velocity, temperature, pressure, humidity, and surface temperature were recorded, and video footage was taken. Three different FFFS nozzle types were tested, ranging from large drop systems  (approximate  droplet  diameter  1000 µm),  small  drop  systems  (approximate  droplet diameter 300 µm) and high-pressure water mist (approximate droplet diameter 100 µm). The fire was shielded in the tests to isolate the interaction of the FFFS and EVS from fire suppression. One of the main findings from the tests was an improvement in the smoke management when the FFFS was operated. Smaller water drops were found to provide increased cooling effect with temperatures downstream of the fire being reduced.

Nozzles used were tested to measure droplet sizes and spray patterns. These parameters were used in a Fire Dynamics Simulator (FDS) model that employed a genetic algorithm to estimate the spray model parameters for FDS models. The approach was found to work quite well for the purposes of water spray model development.

Computational fluid dynamics (CFD) models of the tests were conducted using Fire Dynamics Simulator (FDS). FDS is a free and open-source software tool provided by the National Institute of Standards and Technology (NIST) of the United States Department of Commerce. FDS was used because it is software purpose-built for fire modeling, it is widely and easily available, and it captures  the  major  physical  processes  regarding  FFFS  and  EVS  integration.  Results  were compared to test measurements. The FDS models showed good agreement with test data for temperatures downstream of the fire. In the region upstream of the fire the FDS models did not initially predict the backlayering that was observed in the tests. When uncertainty ranges in the test fire heat release rate (FHRR) and upstream velocity were accounted for, the backlayering was predicted with better agreement to the tests (FHRR was increased, and upstream velocity was decreased within the  test  uncertainty  ranges).  Sensitivity  analysis  was  conducted  and  a refined grid near to the walls was found to provide an improved prediction of backlayering.

## ACKNOWLEDGMENTS

The  FHWA  is  the  source  of  all  figures  and  photographs  within  this  document  unless  noted otherwise.

The  contribution  of  reviewers  from  industry  is  acknowledged:  David  Hahm  (ASHRAE  TC5.9 Technical  Committee),  Norris  Harvey  (NFPA  502  Technical  Committee),  Yoon  Ko  (ASHRAE TC5.9  Technical  Committee),  Igor  Maevski  (ASHRAE  TC5.9  Technical  Committee),  Sean Cassidy  (ASHRAE  TC5.9  Technical  Committee),  Petr  Pospisil  (ASHRAE  TC5.9  Technical Committee), Yinan Scott Shi (ASHRAE TC5.9 Technical Committee).

## UNIT CONVERSIONS

## TABLE OF CONTENTS

| ACRONYMS ................................................................................................................................................ III   | ACRONYMS ................................................................................................................................................ III   | ACRONYMS ................................................................................................................................................ III                                                                                       |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SUMMARY ................................................................................................................................................... IV  | SUMMARY ................................................................................................................................................... IV  | SUMMARY ................................................................................................................................................... IV                                                                                      |
| ACKNOWLEDGMENTS .............................................................................................................................. VI               | ACKNOWLEDGMENTS .............................................................................................................................. VI               | ACKNOWLEDGMENTS .............................................................................................................................. VI                                                                                                   |
| UNIT CONVERSIONS ................................................................................................................................ VII           | UNIT CONVERSIONS ................................................................................................................................ VII           | UNIT CONVERSIONS ................................................................................................................................ VII                                                                                               |
| 1                                                                                                                                                               | INTRODUCTION ................................................................................................................................... 1              | INTRODUCTION ................................................................................................................................... 1                                                                                                  |
| 2 TEST DESCRIPTION 2.1                                                                                                                                          | 2 TEST DESCRIPTION 2.1                                                                                                                                          | AND PROCEDURES ........................................................................................ 2 Test Tunnel Configuration ............................................................................................................. 3 |
| 2.2                                                                                                                                                             | 2.2                                                                                                                                                             | Measurements ............................................................................................................................... 9                                                                                                      |
| 2.3                                                                                                                                                             | 2.3                                                                                                                                                             | Test Detail ................................................................................................................................... 15                                                                                                  |
| 3 TEST SUMMARY AND RESULTS ..................................................................................................... 19                             | 3 TEST SUMMARY AND RESULTS ..................................................................................................... 19                             | 3 TEST SUMMARY AND RESULTS ..................................................................................................... 19                                                                                                                 |
| 3.1                                                                                                                                                             | 3.1                                                                                                                                                             | Inlet Velocity Profile ..................................................................................................................... 19                                                                                                     |
| 3.2                                                                                                                                                             | 3.2                                                                                                                                                             | Airflow Resistance of FFFS and Other Obstructions .................................................................. 21                                                                                                                             |
| 3.3                                                                                                                                                             | 3.3                                                                                                                                                             | Fire Heat Release Rate and Thermal Environment .................................................................... 28                                                                                                                              |
| 3.4                                                                                                                                                             | 3.4                                                                                                                                                             | Critical/Confinement Velocity ...................................................................................................... 43                                                                                                             |
| 3.5                                                                                                                                                             | 3.5                                                                                                                                                             | Adiabatic Surface Temperature .................................................................................................. 48                                                                                                                 |
| 3.6                                                                                                                                                             | 3.6                                                                                                                                                             | Static Pressure Measurements During Fire Conditions .............................................................. 51                                                                                                                               |
| 3.7                                                                                                                                                             | 3.7                                                                                                                                                             | Relative Humidity ........................................................................................................................ 54                                                                                                       |
| 3.8                                                                                                                                                             | 3.8                                                                                                                                                             | Water Spray Characteristics ....................................................................................................... 55                                                                                                              |
| 4 FDS MODELS ..................................................................................................................................... 58           | 4 FDS MODELS ..................................................................................................................................... 58           | 4 FDS MODELS ..................................................................................................................................... 58                                                                                               |
| 4.1                                                                                                                                                             | 4.1                                                                                                                                                             | FDS Model Setup ........................................................................................................................ 58                                                                                                         |
| 4.2                                                                                                                                                             | 4.2                                                                                                                                                             | FDS Results - Nozzle B .............................................................................................................. 62                                                                                                            |
| 4.3                                                                                                                                                             | 4.3                                                                                                                                                             | FDS Results - Nozzle A .............................................................................................................. 72                                                                                                            |
| 4.4                                                                                                                                                             | 4.4                                                                                                                                                             | Summary of Results .................................................................................................................... 81                                                                                                          |
| DISCUSSION AND CONCLUDING REMARKS ................................................................................ 83                                           | DISCUSSION AND CONCLUDING REMARKS ................................................................................ 83                                           | DISCUSSION AND CONCLUDING REMARKS ................................................................................ 83                                                                                                                               |
| 5 5.1                                                                                                                                                           | Research Hypotheses ................................................................................................................. 83                        | Research Hypotheses ................................................................................................................. 83                                                                                                            |
| 5.2                                                                                                                                                             | Discussion ................................................................................................................................... 86               | Discussion ................................................................................................................................... 86                                                                                                   |
| 5.3                                                                                                                                                             | Suggested Practices Based on Research Findings .................................................................... 86                                          | Suggested Practices Based on Research Findings .................................................................... 86                                                                                                                              |
| 5.4                                                                                                                                                             | Suggested Topics for Future Research ...................................................................................... 86                                  | Suggested Topics for Future Research ...................................................................................... 86                                                                                                                      |

## LIST OF FIGURES

| Figure 2-1:   | Sketch of the test tunnel (top view). ...........................................................................................                                                                                                                                                                       |   3 |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| Figure 2-2:   | Sketch of the test tunnel (side view). ..........................................................................................                                                                                                                                                                       |   4 |
| Figure 2-3:   | Constructed test tunnel. ..............................................................................................................                                                                                                                                                                 |   4 |
| Figure 2-4:   | Sketch of the ventilation system (side and isometric view). .......................................................                                                                                                                                                                                     |   5 |
| Figure 2-5:   | Flow conditioner with blockages. ................................................................................................                                                                                                                                                                       |   5 |
| Figure 2-6:   | Fire pool 1 (a) and fire pool 2 (b) setup. .....................................................................................                                                                                                                                                                        |   6 |
| Figure 2-7:   | Equation. Sprinkler K factor. .......................................................................................................                                                                                                                                                                   |   7 |
| Figure 2-8:   | Nozzle A layout. ..........................................................................................................................                                                                                                                                                             |   9 |
| Figure 2-9:   | Nozzle B layout. ..........................................................................................................................                                                                                                                                                             |   9 |
| Figure 2-10:  | Nozzle C layout.........................................................................................................................                                                                                                                                                                |   9 |
| Figure 2-11:  | Measurement set-up, point PXXX refers to distance along the tunnel in decimeter (e.g., P020 is 2 m along the duct). ...................................................................................................                                                                                 |  14 |
| Figure 2-12:  | Measurement set-up x-axis scale adjusted along the tunnel length for result plotting where fire location marks x = 0, upstream indicated using negative and downstream using positive x-coordinates. .................................................................................................. |  14 |
| Figure 3-1:   | Sketch of distributed grid points at the cross-section. ..............................................................                                                                                                                                                                                  |  19 |
| Figure 3-2:   | Equation. Calculation of total flow rate with the measured velocity at inlet probe C. ...............                                                                                                                                                                                                   |  20 |
| Figure 3-3:   | Test 1e/f, the average bulk velocity with and without FFFS using Nozzle A. ...........................                                                                                                                                                                                                  |  22 |
| Figure 3-4:   | Test 1e/f, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle A at 1.85 m/s inlet velocity. ................................................................                                                                                               |  22 |
| Figure 3-5:   | Test 1e/f, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle A at 4.15 m/s inlet velocity. ................................................................                                                                                               |  23 |
| Figure 3-6:   | Test 1g/h, average bulk velocity with and without FFFS using Nozzle B. ................................                                                                                                                                                                                                 |  24 |
| Figure 3-7:   | Test 1g/h, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle B at 1.85 m/s inlet velocity. ................................................................                                                                                               |  24 |
| Figure 3-8:   | Test 1g/h, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle B at 4.15 m/s inlet velocity. ................................................................                                                                                               |  24 |
| Figure 3-9:   | Equation. Pressure loss equation based on total loss factor. ..................................................                                                                                                                                                                                         |  25 |
| Figure 3-10:  | Equation. Pressure loss equation based on duct friction factor. ............................................                                                                                                                                                                                            |  25 |
| Figure 3-11:  | Equation. Hydraulic diameter. ................................................................................................                                                                                                                                                                          |  25 |
| Figure 3-12:  | Test 1c blockages. ..................................................................................................................                                                                                                                                                                   |  26 |
| Figure 3-13:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-08 (5a). ..................................                                                                                                                                                                                                       |  30 |
| Figure 3-14:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-09 (5a). ..................................                                                                                                                                                                                                       |  30 |
| Figure 3-15:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-10 (4a). ..................................                                                                                                                                                                                                       |  31 |
| Figure 3-16:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-11 (4a). ..................................                                                                                                                                                                                                       |  31 |
| Figure 3-17:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-12 (5a). ..................................                                                                                                                                                                                                       |  32 |
| Figure 3-18:  | FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-13 (5a). ..................................                                                                                                                                                                                                       |  32 |
| Figure 3-19:  | FHRR plot from O2 FHRR, test IFAB-14 (5b). .......................................................................                                                                                                                                                                                      |  33 |
| Figure 3-20:  | FHRR plot from O2 FHRR, test IFAB-15 (5b). .......................................................................                                                                                                                                                                                      |  33 |
| Figure 3-21:  | FHRR plot from O2 FHRR, test IFAB-19 (4b). .......................................................................                                                                                                                                                                                      |  34 |
| Figure 3-22:  | FHRR plot from O2 FHRR, test IFAB-20 (7b). .......................................................................                                                                                                                                                                                      |  34 |
| Figure 3-23:  | FHRR plot from O2 FHRR, test IFAB-21 (7a). .......................................................................                                                                                                                                                                                      |  35 |
| Figure 3-24:  | FHRR plot from O2 FHRR, test IFAB-22 (3a). .......................................................................                                                                                                                                                                                      |  35 |
| Figure 3-25:  | FHRR plot from O2 FHRR, test IFAB-24 (3b). .......................................................................                                                                                                                                                                                      |  36 |
| Figure 3-26:  | Test 4b, measured FHRR varying over time with FFFS using Nozzle A. ..............................                                                                                                                                                                                                       |  37 |
| Figure 3-27:  | Test 5b, measured FHRR varying over time with FFFS using Nozzle B. ..............................                                                                                                                                                                                                       |  37 |

| Figure 3-28:   | Test 7b, measured FHRR varying over time with FFFS using Nozzle C. ..............................                                                                                                                                 | 38                                                                               |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Figure 3-29:   | Test 4b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle A. ..........................................................................................                  | 39                                                                               |
| Figure 3-30:   | Test 4b, bulk velocity upstream of the fire. .............................................................................                                                                                                        | 39                                                                               |
| Figure 3-31:   | Test 5b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle B. ..........................................................................................                  | 40                                                                               |
| Figure 3-32:   | Test 5b, bulk velocity upstream of the fire. .............................................................................                                                                                                        | 40                                                                               |
| Figure 3-33:   | Test 7b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle C. ..........................................................................................                  | 41                                                                               |
| Figure 3-34:   | Test 7b, bulk velocity upstream of the fire.                                                                                                                                                                                      | ............................................................................. 41 |
| Figure 3-35:   | Test 4b, temperature at the ceiling with FFFS using Nozzle A larger drop. ...........................                                                                                                                             | 42                                                                               |
| Figure 3-36:   | Test 5b, temperature at the ceiling with FFFS using Nozzle B smaller drop. ........................                                                                                                                               | 42                                                                               |
| Figure 3-37:   | Test 7b, temperature at the ceiling with FFFS using Nozzle C. .............................................                                                                                                                       | 43                                                                               |
| Figure 3-38:   | Test 4b, a snapshot of tunnel cross-section showing smoke backlayering. ..........................                                                                                                                                | 44                                                                               |
| Figure 3-39:   | Test 4b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle A. ................................................................................................................................      | 44                                                                               |
| Figure 3-40:   | Test 5b, a snapshot of tunnel cross-section showing smoke backlayering. ..........................                                                                                                                                | 45                                                                               |
| Figure 3-41:   | Test 5b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle B. ................................................................................................................................      | 45                                                                               |
| Figure 3-42:   | Test 7b, a snapshot of tunnel cross-section showing smoke backlayering. ..........................                                                                                                                                | 46                                                                               |
| Figure 3-43:   | Test 7b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle C. ................................................................................................................................      | 46                                                                               |
| Figure 3-44:   | Critical velocity results compared with 2014 NFPA 502 equation. .........................................                                                                                                                         | 48                                                                               |
| Figure 3-45:   | Measured FHRR varying over time. .......................................................................................                                                                                                          | 49                                                                               |
| Figure 3-46:   | Adiabatic surface temperature at the ceiling, 1 m downstream of fire. ..................................                                                                                                                          | 50                                                                               |
| Figure 3-47:   | Adiabatic surface temperature at the sidewall, 1 m downstream of fire. ................................                                                                                                                           | 50                                                                               |
| Figure 3-48:   | Adiabatic surface temperature at the ceiling, 4.5 m downstream of fire. ...............................                                                                                                                           | 51                                                                               |
| Figure 3-49:   | Adiabatic surface temperature at the sidewall, 4.5 m downstream of fire. .............................                                                                                                                            | 51                                                                               |
| Figure 3-50:   | Test 4b (Nozzle A), static pressure before and after FFFS operation. ...................................                                                                                                                          | 53                                                                               |
| Figure 3-51:   | Test 5b (Nozzle B), static pressure before and after FFFS operation. ...................................                                                                                                                          | 53                                                                               |
| Figure 3-52:   | Test 7b (Nozzle C), static pressure before and after FFFS operation. ..................................                                                                                                                           | 54                                                                               |
| Figure 3-53:   | Test 4b, relative humidity results upstream and downstream of the fire with FFFS using Nozzle A. ................................................................................................................................ | 55                                                                               |
| Figure 3-54:   | Test 4b, measured FHRR varying over time with FFFS using Nozzle A. ..............................                                                                                                                                 | 55                                                                               |
| Figure 3-55:   | Spray pattern and FDS results for Nozzle A (EVS-10-52). ....................................................                                                                                                                      | 56                                                                               |
| Figure 3-56:   | Spray pattern and FDS results for Nozzle B (EVS-10-51). ....................................................                                                                                                                      | 57                                                                               |
| Figure 4-1:    | FDS model setup (dimensions in m). .......................................................................................                                                                                                        | 60                                                                               |
| Figure 4-2:    | FDS model setup showing Test 4b setup with Nozzle A. .........................................................                                                                                                                    | 60                                                                               |
| Figure 4-3:    | FDS model setup showing Test 5b setup with Nozzle B. .........................................................                                                                                                                    | 60                                                                               |
| Figure 4-4:    | Equation. Pearson correlation coefficient. ................................................................................                                                                                                       | 60                                                                               |
| Figure 4-5:    | FHRR profile for Test 5B FDS models. ....................................................................................                                                                                                         | 61                                                                               |
| Figure 4-6:    | FHRR profile for Test 4B FDS models. ....................................................................................                                                                                                         | 61                                                                               |
| Figure 4-7:    | Test 5b, FDS temperature results just upstream of the fire. ....................................................                                                                                                                  | 62                                                                               |
| Figure 4-8:    | Test 5b, FDS velocity results just upstream of the fire. ............................................................                                                                                                             | 62                                                                               |
| Figure 4-9:    | Test 5b, FDS temperature result just downstream of the fire. ..................................................                                                                                                                   | 63                                                                               |
| Figure 4-10:   | Test 5b, FDS velocity result just downstream of the fire. .......................................................                                                                                                                 | 63                                                                               |
| Figure 4-11:   | Test 5b, FDS results showing gas temperature near the ceiling averaged from 400 to                                                                                                                                                |                                                                                  |

410seconds. ...........................................................................................................................  64

| Figure 4-12:     | Test 5b, FDS results showing gas temperature near the ceiling averaged from 470 to 480 seconds. ..........................................................................................................................                                                                                         |   64 |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| Figure 4-13:     | Test 5b, FDS results showing isotherm of temperature (40 degrees Celsius) upstream of fire. ......................................................................................................................................                                                                                 |   65 |
| Figure 4-14:     | Test 5b, Case I (base case grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds). .................................................................................                      |   66 |
| Figure 4-15:Test | 5b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds). .................................................................................                               |   67 |
| Figure 4-16:     | Test 5b, Case III (uniform coarse grid) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds). ......................................................................................................................... |   67 |
| Figure 4-17:     | Test 5b, Case IV (uniform fine grid) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds). .........................................................................................................................    |   68 |
| Figure 4-18:     | Test 5b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.698. ..........................................................................                                                                                                   |   69 |
| Figure 4-19:     | Test 5b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.80. ............................................................................                                                                                                  |   69 |
| Figure 4-20:     | Test 5b, Case I (coarse grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds). ................................................................................................................................      |   70 |
| Figure 4-21:     | Test 5b, Case I (coarse grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds). ...........................................................................                          |   71 |
| Figure 4-22:     | Test 5b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds). ................................................................................................................................       |   71 |
| Figure 4-23:     | Test 5b, Case II (fine grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds). ...........................................................................                           |   72 |
| Figure 4-24:     | Test 4b, FDS temperature results just upstream of the fire. ..................................................                                                                                                                                                                                                     |   73 |
| Figure 4-25:     | Test 4b, FDS velocity results just upstream of the fire. ..........................................................                                                                                                                                                                                                |   73 |
| Figure 4-26:     | Test 4b, FDS temperature result just downstream of the fire. ................................................                                                                                                                                                                                                      |   74 |
| Figure 4-27:     | Test 4b, FDS velocity result just downstream of the fire. .......................................................                                                                                                                                                                                                  |   74 |
| Figure 4-28:     | Test 4b, FDS results showing gas temperature near the ceiling averaged from 340 to 350 seconds. ..........................................................................................................................                                                                                         |   75 |
| Figure 4-29:     | Test 4b, FDS results showing gas temperature near the ceiling averaged from 410 to 420 seconds. ..........................................................................................................................                                                                                         |   75 |
| Figure 4-30:     | Test 4b, FDS results showing isotherm of temperature (40 degrees Celsius) upstream of fire. ......................................................................................................................................                                                                                 |   76 |
| Figure 4-31:     | Test 4b, Case I (coarse grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). .................................................................................                         |   77 |
| Figure 4-32:     | Test 4b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). .................................................................................                          |   77 |
| Figure 4-33:     | Test 4b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.698. ..........................................................................                                                                                                   |   78 |
| Figure 4-34:     | Test 4b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.80. ............................................................................                                                                                                  |   78 |

| Figure 4-35:                                                                                                                                               | Test 4b, Case I (coarse grid with near-wall refinement) results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). .......................................................................................................   | 79             |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| Figure 4-36:                                                                                                                                               | Test 4b, Case I (coarse grid with near-wall refinement) results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). .............................................                            | 80             |
| Figure 4-37:                                                                                                                                               | Test 4b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). .................................................................................                      | 80             |
| Figure 4-38:                                                                                                                                               | Test 4b, Case II (fine grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds). ............................                                          | 81             |
| LIST OF TABLES                                                                                                                                             | LIST OF TABLES                                                                                                                                                                                                                                                                                                 | LIST OF TABLES |
| Table 2-1: Parameters of class B fire loads (EVS-01-30). ............................................................................                      | Table 2-1: Parameters of class B fire loads (EVS-01-30). ............................................................................                                                                                                                                                                          | 6              |
| Table 2-2: FFFS parameters. ........................................................................................................................       | Table 2-2: FFFS parameters. ........................................................................................................................                                                                                                                                                           | 8              |
| Table 2-3: Different measurement sensors used in the testing. .................................................................                            | Table 2-3: Different measurement sensors used in the testing. .................................................................                                                                                                                                                                                | 11             |
| Table 2-4: Measurements recorded. ...........................................................................................................              | Table 2-4: Measurements recorded. ...........................................................................................................                                                                                                                                                                  | 12             |
| Table 2-5: Cold flow tests. ...........................................................................................................................    | Table 2-5: Cold flow tests. ...........................................................................................................................                                                                                                                                                        | 16             |
| Table 2-6: Fire tests. ................................................................................................................................... | Table 2-6: Fire tests. ...................................................................................................................................                                                                                                                                                     | 17             |
| Table 2-7: Nozzle characterizations. ...........................................................................................................           | Table 2-7: Nozzle characterizations. ...........................................................................................................                                                                                                                                                               | 18             |
| Table 3-1: Summary of pressure changes from the cold flow tests (EVS-01-22). ......................................                                        | Table 3-1: Summary of pressure changes from the cold flow tests (EVS-01-22). ......................................                                                                                                                                                                                            | 27             |
| Table 3-2: FHRR notes. ..............................................................................................................................      | Table 3-2: FHRR notes. ..............................................................................................................................                                                                                                                                                          | 29             |
| Table 3-3: Parameters used for computation of critical velocity per NFPA 502 2014 equation. ................                                               | Table 3-3: Parameters used for computation of critical velocity per NFPA 502 2014 equation. ................                                                                                                                                                                                                   | 47             |
| Table 3-4: Adiabatic surface temperature (AST) selected results. .............................................................                             | Table 3-4: Adiabatic surface temperature (AST) selected results. .............................................................                                                                                                                                                                                 | 49             |
| Table 3-5: Nozzle parameter measurements. .............................................................................................                    | Table 3-5: Nozzle parameter measurements. .............................................................................................                                                                                                                                                                        | 56             |
| Table 3-6: Spray patterns and FDS parameters based on tests and analysis. ..........................................                                       | Table 3-6: Spray patterns and FDS parameters based on tests and analysis. ..........................................                                                                                                                                                                                           | 57             |
| Table 4-1: FDS parameters used in the computer modeling. .....................................................................                             | Table 4-1: FDS parameters used in the computer modeling. .....................................................................                                                                                                                                                                                 | 58             |
| Table 4-2: Sensitivity parameters tested in the FDS models. .....................................................................                          | Table 4-2: Sensitivity parameters tested in the FDS models. .....................................................................                                                                                                                                                                              | 65             |
| Table 4-3: Grid resolution sensitivity cases for Test 5b. .............................................................................                    | Table 4-3: Grid resolution sensitivity cases for Test 5b. .............................................................................                                                                                                                                                                        | 66             |
| Table 4-4: Grid sensitivity cases for Test 4b. ..............................................................................................              | Table 4-4: Grid sensitivity cases for Test 4b. ..............................................................................................                                                                                                                                                                  | 76             |
| Table 4-5: Summary of the FDS results. .....................................................................................................               | Table 4-5: Summary of the FDS results. .....................................................................................................                                                                                                                                                                   | 81             |

## 1 INTRODUCTION

The Federal Highway Administration (FHWA) has been conducting research into the use of fixed fire fighting systems (FFFS) in road tunnels. The objective of this research is to identify the current industry's  ability  to  consider  the  integration  of  highway  tunnel  emergency  ventilation  systems (EVS) with installed FFFS, and to then develop a set of suggested practices on the integration of FFFS and EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (Fixed Fire Fighting and Emergency Ventilation Systems for  Highway  Tunnels  -  Literature  Survey  and  Synthesis,  Federal  Highway  Administration, FHWA-HIF-20-016).
2. Industry workshop and report (including workplans for computer modeling and testing) [2] (Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Workshop Report, Federal Highway Administration, FHWA-HIF-20-060).
3. Computer modeling research [3] (Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Computer Modeling Report, Federal Highway Administration, FHWA-HIF22-021).
4. Laboratory scale testing.
5. Research report and suggested practices.

This  document  is  the  laboratory  scale  testing  report.  Section  2  of  this  document  provides  a summary of the test facility and procedures, Section 3 summarizes test results, Section 4 presents computational fluid dynamics models (CFD) of selected tests conducted using the Fire Dynamics Simulator (FDS) software, and Section 5 provides the conclusions.

## 2 TEST DESCRIPTION AND PROCEDURES

Principal hypotheses being investigated with this research and the anticipated contribution of the tests are discussed below.

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized because of the cooling effects of the FFFS water spray. This hypothesis can be verified via measurement of  the  critical  velocity  for  smoke  control,  pressure  loss  due  to  the  FFFS water  spray,  and  the impact of the EVS on water delivery. If the hypothesis is correct, then the critical velocity should decrease due to the cooling. Additional airflow resistance introduced by the FFFS spray should be negligible with respect to other airflow resistance in the tunnel from items such as vehicles, wall friction, buoyancy, fire, and external wind. Finally, the EVS should not cause excessive water droplet drift as to cause a negative effect on water droplet delivery to the fire zone. Testing was conducted to examine the effect of the water cooling on smoke control.

The second hypothesis (verified by computer modeling) is that CFD (specifically here, FDS as that  was  the  software  utilized)  can  be  used  to  predict  FFFS  and  EVS  interaction  for  design integration. The FDS software was used because it is software purpose-built for fire modeling, it is widely and easily available, and it captures the major physical processes regarding FFFS and EVS integration. Integration combinations of FFFS and EVS include:

- Small and large water droplet systems.
- Varying water application rates and FFFS zone configurations.
- Longitudinal ventilation.
- Transverse ventilation.
- Single point exhaust.
- Varying tunnel geometry (area, perimeter, height, grade).

Laboratory scale tests were performed via the Institute for Applied Fire Safety Research (IFAB) in Germany. IFAB has previously conducted laboratory and full-scale tunnel fire tests with and without FFFS. These tests are designed for the project and research questions being investigated. IFAB's experience conducting previous tests in tunnel situations is unique in the industry, with much of the modern testing experience concentrated in Europe. The research team is not aware of accreditation standards in the United States throughout the duration of this project. IFAB is an accredited test laboratory by Deutsche Akkreditierungsstelle (DAkkS), the national accreditation body  of  Germany,  per  DIN  EN  ISO/IEC  17025:2018-03.  Accreditation  is  for  the  proof  of  the effectiveness  of water-based  fire-fighting  systems  by  fire  tests for  tunnel  and  transport infrastructure systems, and for experimental determination of design fire scenarios by full-scale tests [4].

The tests were performed to better understand the interaction between longitudinal EVS and the FFFS.  The  tests  were  principally  structured  toward  the  goal  of  verifying  critical/confinement velocity with an FFFS operating and to provide data for FDS model validation. Per National Fire Protection Association (NFPA) Standard 502 (note that use of NFPA standards in highway tunnels is voluntary and not a Federal requirement), the following terms are used herein for backlayering and critical velocity [5]:

- Backlayering - Movement of smoke and hot gasses counter to the direction of ventilation airflow.
- Critical velocity - The minimum steady-state velocity of the ventilation airflow moving toward the fire, within a tunnel or passageway that is necessary to prevent backlayering at the fire site.

In this document the term confinement velocity is used to describe the steady-state velocity of the ventilation airflow moving toward the fire that is of a magnitude large enough to stop smoke movement upstream of the fire but not to prevent backlayering.

## 2.1 Test Tunnel Configuration

Tests were conducted by IFAB at its laboratory. Refer to the Workshop Report [2] (Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Workshop Report, Federal Highway Administration, FHWA-HIF-20-060) Section 5.1 for further information on the testing. For discussion about previous test programs refer to the Literature Survey and Synthesis [1] (Fixed Fire  Fighting  and  Emergency  Ventilation  Systems  for  Highway  Tunnels  -  Workshop  Report, Federal Highway Administration, FHWA-HIF-20-060) Chapter 3.

The test tunnel had dimensions of 2.5 m width, 1.25 m height, and 12.0 m length. The scale used was approximately 1 in 4, to give a full-scale equivalent of 10 m width and 5 m height, which is on the same order as a typical two-lane highway tunnel. Being limited somewhat by the test building site dimensions the tunnel total length was 16.5 m. To limit outside wind influence on the air flow within the tunnel a porous plate was added at the breakthrough to the outer wall of the building. The tunnel was set up using a temporary construction comprised of dry wall with non-combustible and water resistant aquapanel boards, which were replaceable in case of fire damage during the tests.  Figure  2-1  and  Figure  2-2  show  sketches  of  the  scale  test  tunnel.  Figure  2-3  shows  a photograph of the constructed scaled test tunnel.

Figure 2-1: Sketch of the test tunnel (top view).

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

Figure 2-2: Sketch of the test tunnel (side view).

<!-- image -->

Photograph

© IFAB 2022

Figure 2-3: Constructed test tunnel.

## 2.1.1 Ventilation System

The ventilation system was set up to supply an adjustable longitudinal air flow through the tunnel to investigate critical/confinement velocity and backlayering. Three fans were used to supply air (make and model type Ruck AL-560-D4-01) with a capacity of up to 34,000 m 3 /h (20,000 CFM). Fans were operated on a variable frequency drive to enable adjustment of the velocity. Air was directed into the tunnel via a duct with a 90-degree bend with turning vanes followed by a flow conditioner. Figure 2-4 shows the sketch of the ventilation system along with a photograph of the constructed system.

Figure 2-4: Sketch of the ventilation system (side and isometric view).

<!-- image -->

Engineering drawing

The flow conditioner was used to obtain an approximately even velocity profile through the tunnel. It was constructed using 200 mm diameter pipes of 250 mm length with some of them blocked to add some resistance for improved air distribution across the face (spaces between pipes were not blocked). Figure 2-5 shows the geometry of the flow conditioner used.

Figure 2-5: Flow conditioner with blockages.

<!-- image -->

Engineering drawing

## 2.1.2 Fire Loads

Fires  were  generated  as  class  B  fires  using  a  pan  of  heptane  or  diesel.  The  fire  loads  were designed  to  generate  an  approximate  fire  heat  release  rate  (FHRR)  of  0.63 MW  or  1.3 MW, depending on the size of the fire pan used.

Table 2-1: Parameters of class B fire loads (EVS-01-30).

| PARAMETER                  | DIESEL                                                                                    | HEPTANE                                         |
|----------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------|
| Burning rate (kg/m 2 /s)   | 0.045                                                                                     | 0.101                                           |
| Heat of combustion (MJ/kg) | 44.4                                                                                      | 44.6                                            |
| K β (m -1 )                | 2.1                                                                                       | 1.1                                             |
| D (m)                      | 0.61                                                                                      | 0.79                                            |
| Flash point (⁰C)           | 56                                                                                        | -7                                              |
| Pool 1                     | 0.49 m long, 0.59 m wide, and 0.10 m high, area of 0.29 m 2 for a nominal FHRR of 0.42 MW | As per diesel, but FHRR estimated to be 0.63 MW |
| Pool 2                     | 0.84 m long, 0.59 m wide, and 0.10 m high, area of 0.50 m 2 for a nominal FHRR of 0.80 MW | As per diesel, but FHRR estimated to be 1.3 MW  |

The fire load was shielded to prevent direct contact with water from the FFFS, with the goal of keeping the FHRR unaffected by the FFFS. The (small) height difference between pool 1 and 2 was compensated for by using plates placed underneath. Figure 2-6 shows the pool dimensions and setup from both the side and the top view. The shield had a cross sectional dimension facing into the airflow of 1100 mm wide and 680 mm tall. The shield was completely open at both sides, and closed at the front, top and rear.

Figure 2-6: Fire pool 1 (a) and fire pool 2 (b) setup.

<!-- image -->

Engineering drawing

## 2.1.3 Fixed Fire Fighting System

The potential impact of a water based FFFS on critical/confinement velocity is to reduce those velocities needed through the cooling action of the water spray, assuming no change in FHRR of the shielded fire pool.

A starting question is what water application rate to use. NFPA 502 does not establish water application rates for tunnel FFFS, but application rates used in U.S. highway tunnels have been partly informed by international approaches (Japan and Australia), results of full-scale tunnel test programs, and with consideration of NFPA 13. To date, U.S. highway tunnels that have been equipped with an FFFS use water application rates between 0.15 gpm/ft 2  and 0.30 gpm/ft 2  (6 mm/min to 12 mm/min) (refer to the Literature Survey and Synthesis [1], Section 2.6).

For the fire tests, nozzles were selected for characterization for laboratory testing based on the following factors:

- Application  in  U.S.  tunnels,  a  nozzle  that  is  approved  and  listed  for  the  application  per NFPA 13, if possible.
- Availability of sprinkler K-factor and spray pattern data (refer to Figure 2-7).
- Availability  of  droplet  size  distribution  or  similarity  of  the  nozzle  to  others  where  size distribution is available.
- Laboratory-scale versus full-scale availability noting that one key aspect of the testing is to compare laboratory-scale with full-scale nozzles.

Based on these factors, three different nozzles were used for the testing:

- Viking system (Nozzle A - large droplet size, typical nozzle listed for use in the United States).
- Lechler  system  (Nozzle  B  -  smaller  droplet  size  relative  to  Nozzle  A,  better  suited  to laboratory-scale).
- Fogtec system (Nozzle C - high pressure water mist).

The choice of nozzles was based on balancing the goals to use a nozzle listed for use in the United States and to use a nozzle that could work well at the laboratory scale. Nozzle A was used because it is a nozzle listed for use in the United States to NFPA 13 (i.e., a fire sprinkler), however, the flow rate from Nozzle A was large relative to the test scale, and the spray pattern was very wide. Therefore, Nozzle B was used because it had a smaller flow rate, spray pattern diameter and drop size relative to Nozzle A, thus making it better suited to the laboratory scale test. Table 2-2 summarizes the nozzle parameters that are used for the tests. Nozzle C was not originally planned to be used but an opportunity arose to run a fire test using water mist. The actual nozzle was selected based on similar reasoning to Nozzle B.

Sprinkler K factor is per the equation provided in Figure 2-7. In the equation Qs is the sprinkler flow rate (L/min), Ks is the sprinkler K factor (L/min/bar 0.5 ) and p is the water pressure (bar).

Figure 2-7: Equation. Sprinkler K factor.

<!-- image -->

Engineering drawing

Table 2-2: FFFS parameters.

| SYSTEM PARAMETER                                                                                                 | NOZZLE A                                               | NOZZLE B                                             | NOZZLE C                                                  |
|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|------------------------------------------------------|-----------------------------------------------------------|
| Nozzle type                                                                                                      | Viking VK329, pendent                                  | Lechler 490.648                                      | Fogtec                                                    |
| Number of nozzle rows                                                                                            | 1                                                      | 2                                                    | 1                                                         |
| Number of nozzles per row                                                                                        | 1                                                      | 4                                                    | 5                                                         |
| Total number of nozzles                                                                                          | 1                                                      | 8                                                    | 5                                                         |
| Nozzle pressure                                                                                                  | 1.5 bar                                                | 3.0 bar                                              | 90 bars                                                   |
| K-factor (L/min/bar 0.5 )                                                                                        | 40.83                                                  | 2.83                                                 | 0.48                                                      |
| Flow rate per nozzle                                                                                             | 49.9 L/min                                             | 4.9 L/min                                            | 4.6 L/min                                                 |
| Total system flow rate                                                                                           | 49.9 L/min                                             | 39.2 L/min                                           | 23 L/min                                                  |
| Water application rate (flow per area)                                                                           | 3.4 mm/min                                             | 2.0 mm/min                                           | 1.2 mm/min                                                |
| Water application area (length is estimated from nozzle spray diameter) used to calculate water application rate | 2.5 m (wide) by 5.8 m (long)                           | 2.5 m (wide) by 7.68 m (long)                        | 2.5 m (wide) by 7.74 m (long)                             |
| Spray radius at 1.25 m below nozzle (m) - approximate                                                            | 2.9 m                                                  | 1.5 m                                                | 1.5 m                                                     |
| Droplet diameter (Dv0.5)                                                                                         | 1.12 mm                                                | 0.28 mm                                              | 0.13 mm                                                   |
| Nozzle spacing within rows                                                                                       | N/A (single nozzle)                                    | 1.56 m                                               | 1.56 m                                                    |
| Spacing between rows                                                                                             | N/A (single nozzle)                                    | 1.25 m                                               | N/A (single row)                                          |
| Distance to the nearest side wall                                                                                | 1.25 m                                                 | 0.625 m                                              | 1.25 m                                                    |
| Orientation                                                                                                      | Single nozzle above fire pool at the tunnel centerline | Four nozzles alternating per row above the fire pool | Five nozzles above the fire pool at the tunnel centerline |

Figure 2-8, Figure 2-9 and Figure 2-10 show the approximate FFFS layout within the scale test tunnel. Water was supplied from a 1 m 3  tank to the FFFS with a submersible pump. The pump was connected to the nozzle systems via hoses and pressure adjustment valves. The tank was refilled manually in between tests. The scale test tunnel was developed to allow fires with and without FFFS operation under longitudinal ventilation.

Figure 2-8: Nozzle A layout.

<!-- image -->

Engineering drawing

Figure 2-9: Nozzle B layout.

<!-- image -->

Engineering drawing

Figure 2-10: Nozzle C layout.

<!-- image -->

Engineering drawing

## 2.2 Measurements

The following parameters were measured and recorded during all tests:

- The gas temperature at the ceiling on the tunnel centerline (very near to the ceiling, typically within 50 mm) and at varying longitudinal locations and vertical heights.
- Air velocity at selected locations upstream and downstream of the fire.
- Adiabatic surface temperature (measured via a plate thermometer).
- Fire heat release rate via mass loss rate of the fire load (fuel), and from combustion product gas  composition  measurements  (measurements of  oxygen,  carbon  monoxide  and  carbon dioxide concentration at P115, refer Figure 2-11, with further explanation provided below).
- Water pressure in the FFFS, which is used in conjunction with the manufacturer K factor to obtain the nozzle flow rate. The nozzle K factors are assumed to be reliable given they are per the nozzle specifications used for subsequent design development.
- Static pressure at selected locations along the tunnel. Pressure was recorded at one location (top  corner  of  the  tunnel)  and  as  such,  results  need  to  be  interpreted  carefully  as  these

measurements may not  be  representative  of  an  average  over  the  cross  section  (refer  to Section 3.6 for more discussion).

- Relative humidity upstream and downstream of the fire.
- Visual recording.

Table 2-3 summarizes the different measurement sensors used along with their accuracy and expected  uncertainty  (based  on  experience,  not  necessarily  explicit  calculation,  and  with consideration of the test conditions and influencing values). Table 2-4 provides an overview of the  measurement  positioning  in  the  test  tunnel.  Figure  2-11  provides  a  schematic  of  the measurement set-up. The first measurement position started on the upstream side of the fire at 1 m into the tunnel  and the  location  is  denoted  in  units  of  decimeters;  the  location  at  0.5 m  is donated as P005, 1.0 m is denoted as P010 and so on. Measurement probes use the same nomenclature, so V015x refers to a velocity measurement at 1.5 m into the tunnel and the x refers to the position of the sensor in the vertical dimension (usually A, B, C or D, located at distances from the ceiling of 156 mm, 485.5 mm, 781 mm, and 1093.5 mm, respectively).

The fire load was centered at 5.5 m location into the tunnel. The shield was positioned starting at 5.0  m,  which  served  as  the  dividing  point  between  upstream  (&lt;5.0  m  tunnel  length)  and downstream (&gt;5.0 m tunnel length) locations. The measurement sensors were installed in a way that protected from both the fire heat and FFFS moisture. The installed sensors did not obstruct any  airflow  within  the  tunnel  cross-section  and  therefore  did  not  interfere  with  the  quality  of measurement.

When plotting the test results that vary along the length of the duct, the x-axis scale was adjusted so that the start of the fire corresponded to 0 m (5.0 m in the unadjusted coordinate, the start of the  fire  shield),  and  locations  upstream  of  the  fire  had  negative  coordinates,  and  locations downstream positive coordinates. Figure 2-12 shows the updated scale.

For purposes of reporting results before and after FFFS operation, data are typically reported 10 seconds before the FFFS is operated, and from 50 seconds to 60 seconds after the FFFS is operated.  Data  were  chosen  at  these  times  for  a  consistent  basis  and  at  times  remote  from transient events such as fire ignition and FFFS operation. This was also done so that the data used were taken after velocity profile had sufficient time to fully develop after a change in the test conditions.

Table 2-3: Different measurement sensors used in the testing.

| MEASUREMENT                  | MAKE/MODEL                                                                     | ACCURACY                          | UNCERTAINTY                                                       | REMARKS                                                |
|------------------------------|--------------------------------------------------------------------------------|-----------------------------------|-------------------------------------------------------------------|--------------------------------------------------------|
| Gas temperature              | TMH GmbH/type K thermocouple                                                   | Class 1 as per EN60584            | Less than plus or minus 4 percent for greater than 5 °C           | 1-2 mm diameter with range up to 1250°C                |
| Adibatic surface temperature | Pentronic GmbH/plate thermocouple type K                                       | Class 1 as per EN60584 2          | Less than plus or minus 4 percent for greater than 5 °C           | 100 mm x 100 mm plate with range up to 1250°C          |
| Air velocity                 | SETRA Sensing Solutions/model 264 with McCaffrey probe                         | plus or minus 1 percent           | Plus or minus 50 percent                                          | Differential pressure sensor with range of 10 psi      |
| Static pressure              | SETRA Sensing Solutions/model 264 without McCaffrey probe                      | plus or minus 1 percent           | plus or minus 5 percent                                           | Differential pressure sensor with range of 10 psi      |
| Water pessure for Nozzle A   | SIKAR Gmbh/type DSW431H1H075 (A-10)                                            | plus or minus 0.5 percent         | plus or minus 2.5 percent                                         | Pressure sensor with range up to 10 bar                |
| Water pessure for Nozzle B   | SKV-TEC GmbH/type PT2-23- 13-2/4                                               | plus or minus 0.5 percent         | plus or minus 2.5 percent                                         | Pressure sensor with range up to 2 bar/4 bar           |
| Mass loss rate scale         | Dini Argeo/TQ150 type DFWXP                                                    | plus or minus 1.5 percent         | plus or minus 1.5 percent                                         | Industrial platform scale with range up to 150 kg      |
| Single gas sensors           | GfG GmbH/EC24                                                                  | plus or minus 0.5 percent for O 2 | plus or minus 0.5 percent for O 2                                 | Type MK-422-1 for O 2 ,                                |
| Multiple gas measurement     | Gasmet FTIR (Fourier transform infrared spectroscopy) gas analyzer/Type DX4000 | plus or minus 2 percent           | plus or minus10 percent for CO, plus or minus 10 percent for CO 2 | Used with PSP 4000 sampling system                     |
| Humidity                     | Hygerosens Instrument GmbH                                                     | plus or minus 2 percent           | 3.5 percent                                                       | Calibrated against atmosphere saturated salt solutions |

Table 2-4: Measurements recorded.

| POSITION IN TUNNEL (dm)   | GAS TEMPERATURE AT CEILING CENTERLINE (DISTANCE FROM CEILING IN mm)   | GAS TEMPERATURE AT CROSS SECTION AT CENTERLINE (DISTANCE FROM CEILING IN mm)   | AIR VELOCITY AT CROSS SECTION AT CENTERLINE (DISTANCE FROM CEILING IN mm)   | ADIABATIC SURFACE TEMPERATURE (DISTANCE FROM CEILING IN mm)   | STATIC PRESSURE    | RELATIVE HUMIDITY (DISTANCE FROM CEILING IN mm)   | GAS ANALYZER   |
|---------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------|--------------------|---------------------------------------------------|----------------|
| P010                      | T010 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | PS010 (top corner) | RH010 (sidewall, 937.5)                           | N/A            |
| P015                      | T015 (10)                                                             | N/A                                                                            | V015: a(156), b(468.5), c(781), d(1093.5)                                   | N/A                                                           | N/A                | N/A                                               | N/A            |
| P020                      | T020 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P025                      | T025 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P030                      | T030 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | PS030 (top corner) | N/A                                               | N/A            |
| P035                      | T035 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P040                      | T040 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P045                      | T045 (10)                                                             | TR045: a(156), b(468.5), c(781), d(1093.5)                                     | V045: a(156), b(468.5), c(781), d(1093.5)                                   | N/A                                                           | N/A                | N/A                                               | N/A            |
| P050                      | T050 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | PS050 (top corner) | N/A                                               | N/A            |
| P055                      | T055 (10)                                                             | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P060                      | N/A                                                                   | N/A                                                                            | N/A                                                                         | PT060: a(0) at ceiling, b(625) at sidewall                    | N/A                | N/A                                               | N/A            |
| P065                      | T065 (250)                                                            | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A            |
| P075                      | T075 (250)                                                            | N/A                                                                            | N/A                                                                         | N/A                                                           | PS075 (top corner) | N/A                                               | N/A            |
| P085                      | N/A                                                                   | TR085: a(156), b(468.5), c(781), d(1093.5)                                     | V085: a(312.5), b(937.5)                                                    | N/A                                                           | N/A                | N/A                                               | N/A            |

| POSITION IN TUNNEL (dm)   | GAS TEMPERATURE AT CEILING CENTERLINE (DISTANCE FROM CEILING IN mm)   | GAS TEMPERATURE AT CROSS SECTION AT CENTERLINE (DISTANCE FROM CEILING IN mm)   | AIR VELOCITY AT CROSS SECTION AT CENTERLINE (DISTANCE FROM CEILING IN mm)   | ADIABATIC SURFACE TEMPERATURE (DISTANCE FROM CEILING IN mm)   | STATIC PRESSURE    | RELATIVE HUMIDITY (DISTANCE FROM CEILING IN mm)   | GAS ANALYZER                                            |
|---------------------------|-----------------------------------------------------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------|--------------------|---------------------------------------------------|---------------------------------------------------------|
| P095                      | T095 (250)                                                            | N/A                                                                            | N/A                                                                         | PT095: a(0) at ceiling, b(625) at sidewall                    | N/A                | N/A                                               | N/A                                                     |
| P105                      | T105 (250)                                                            | N/A                                                                            | N/A                                                                         | N/A                                                           | N/A                | N/A                                               | N/A                                                     |
| P110                      | N/A                                                                   | N/A                                                                            | N/A                                                                         | N/A                                                           | PS110 (top corner) | N/A                                               | N/A                                                     |
| P115                      | T115 (250)                                                            | TR115: a (312.5), b (937.5)                                                    | V115: a (312.5), b (937.5)                                                  | N/A                                                           | N/A                | RH115 (sidewall, 937.5)                           | Suction point under the ceiling, near tunnel centerline |

Figure 2-11: Measurement set-up, point PXXX refers to distance along the tunnel in decimeter (e.g., P020 is 2 m along the duct).

<!-- image -->

Engineering drawing

Figure 2-12: Measurement set-up x-axis scale adjusted along the tunnel length for result plotting where fire location marks x = 0, upstream indicated using negative and downstream using positive x-coordinates.

<!-- image -->

Engineering drawing

## 2.3 Test Detail

Tests were performed under test series categories as follows (note that multiple tests under each series ID were sometimes performed and thus each test is given a unique numerical ID):

- Test 1: Cold flow tests to establish pressure loss in the tunnel due to wall friction and FFFS pipework.
- Test 2: Not Used.
- Test 3: Free burn tests with longitudinal ventilation; goal was to establish critical/confinement velocity with no FFFS operating.
- Test 4: As per test 3 but with FFFS  operating using Nozzle A; data point for critical/confinement velocity computation.
- Test 5: As per test 3, but with FFFS  operating using Nozzle B; data point for critical/confinement velocity computation.
- Test  6:  Laser  Doppler  analyses  to  determine  nozzle  spray  pattern  and  droplet  sizes  (for Nozzles A, B and C).
- Test 7: As per test 3, but with FFFS  operating using Nozzle C; data point for critical/confinement velocity computation.

Table 2-5, Table 2-6, and Table 2-7 provides a list of the tests performed. Results are included herein for the underlined cases (in test ID column) only. The cold flow tests shown in Table 2-5 were performed without any tunnel obstruction (i.e., no fire pool or shield was present inside the tunnel during these tests).

During the fire tests (test 3, 4, 5 and 7 series) the velocity was usually held at a constant level. When FFFS was not used (test 3 series) the velocity was set to a value approximately large enough to control backlayering (if backlayering was not controlled the velocity was increased or the FFFS was eventually operated). For tests with FFFS (test 4, 5 and 7 series) the velocity was generally held constant throughout the test. When backlayering was observed, the FFFS was operated after a period of a minute or so after backlayering onset.

During the tests the (unexpected) transient nature of the FHRR made it difficult determine critical or  confinement  velocity  without  the  FFFS  operating.  For  tests  where  no  backlayering  was recorded the velocity was quite a bit higher than the NFPA equation estimates. This is more likely a result of the test behavior rather than a true representation of critical or confinement velocity. The FHRR was changing with time and generally increasing. Thus, if the fan speed was turned down, by the time the impact of this could be seen, the FHRR had increased and backlayering was starting to occur. As a result, the velocity was usually kept higher than critical in the early stages of the test until backlayering started to occur. The FFFS usually had to be operated shortly after  this  time  because  the  FHRR  was  continuing  to  grow  and  there  was  a  concern  that  the increasing temperatures could damage the test rig.

Table 2-5: Cold flow tests.

| SERIES ID   | TEST ID (S)                                   | TEST INFORMATION (INLET V AND FHRR FOR FIRST TEST ID LISTED, OR TEST MARKED WITH A *, UNLESS NOTED)                                                                                                                                             | FHRR (MW)   | INLET V (m/s)           | NOZZLE AND WATER FLOW RATE (mm/min)   |
|-------------|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|-------------------------|---------------------------------------|
| 1i          | IFAB-18* (20220221-01), IFAB-23 (20220222-05) | Cold flow. Measure velocity at the duct inlet (with a rotating vane anemometer) over a grid of points to compute the total volume flow and correlate further measurements on the centerline (taken with probes).                                | N/A         | 1.5 m/s, 3 m/s, 4.5 m/s | N/A                                   |
| 1a,1b       | IFAB-02* (20220214-02), IFAB-01 (20220214-01) | Cold flow. Velocity ramped up and then down, 60 seconds between changes. Measure velocity and pressure changes. Determine wall friction effects, no tunnel obstructions. The '1a' and '1b' series ID correlates to different upstream velocity. | N/A         | 1 to 5 m/s              | N/A                                   |
| 1c          | IFAB-03* (20220214-03)                        | Cold flow (like test 1a/b). Internal obstructions in the tunnel (regular spaced blocks).                                                                                                                                                        | N/A         | 1 to 4 m/s              | N/A                                   |
| 1d          | IFAB-05* (20220215-01)                        | Cold flow (like test 1a/b). Internal obstructions in the tunnel (fire shield).                                                                                                                                                                  | N/A         | 1 to 4 m/s              | N/A                                   |
| 1e,1f       | IFAB-16* (20220218-01), IFAB-04 (20220214-04) | Cold flow (like test 1a/b). No obstruction in the duct, operate the FFFS. Velocity held at discrete levels. The '1e' and '1f' series ID correlates to different upstream velocity.                                                              | N/A         | 2 m/s, 4 m/s            | Nozzle A, 3.4 mm/min                  |
| 1g, 1h      | IFAB-17* (20220218-02), IFAB-06 (20220215-02) | Cold flow (like test 1a/b). No obstruction in the duct, operate the FFFS. Velocity held at discrete levels. The '1g' and '1h' series ID correlates to different upstream velocity.                                                              | N/A         | 2 m/s, 4 m/s            | Nozzle B, 2.0 mm/min                  |

Table 2-6: Fire tests.

| SERIES ID   | TEST ID (S)                                                                                 | TEST INFORMATION (INLET V AND FHRR FOR FIRST TEST ID LISTED, OR TEST MARKED WITH A *, UNLESS NOTED)          | FHRR (MW)   | INLET V (m/s)   | NOZZLE AND WATER FLOW RATE (mm/min)   |
|-------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-------------|-----------------|---------------------------------------|
| 3a          | IFAB-22* (20220222-04), IFAB-07 (20220215-03)                                               | Free burn test, diesel pool (heptane pool test for IFAB-07 - used for adiabatic surface temperature results) | 0.9 MW      | 1.2 m/s         | None                                  |
| 3b          | IFAB-24* (20220222-06)                                                                      | Free burn tests, diesel pool                                                                                 | 1.6 MW      | 1.3 m/s         | None                                  |
| 4a          | IFAB-11* (20220216-04), IFAB-10 (20220216-03)                                               | Tests with FFFS, diesel pool (heptane pool test for IFAB-10)                                                 | 0.5 MW      | 1.1 m/s         | Nozzle A, 3.4 mm/min                  |
| 4b          | IFAB-19* (20220222-01)                                                                      | Test with FFFS, diesel pool                                                                                  | 1.5 MW      | 1.2 m/s         | Nozzle A, 3.4 mm/min                  |
| 5a          | IFAB-13* (20220217-02), IFAB-08 (20220216-01), IFAB-09 (20220216-02), IFAB-12 (20220217-01) | Tests with FFFS, diesel pool (heptane pool used in IFAB-08/09 tests, hoses failed for the IFAB-12 test)      | 0.4 MW      | 1.0 m/s         | Nozzle B, 2.0 mm/min                  |
| 5b          | IFAB-15* (20220217-04), IFAB-14 (20220217-03)                                               | Tests with FFFS, diesel pool                                                                                 | 1.8 MW      | 1.3 m/s         | Nozzle B, 2.0 mm/min                  |
| 7a          | IFAB-21* (20220222-03)                                                                      | High pressure water mist, diesel pool fire                                                                   | 0.6 MW      | 1.1 m/s         | Nozzle C, 1.4 mm/min                  |
| 7b          | IFAB-20* (20220222-02)                                                                      | High pressure water mist, diesel pool fire                                                                   | 1.9 MW      | 1.3 m/s         | Nozzle C, 1.4 mm/min                  |

Table 2-7: Nozzle characterizations.

| ID   | TEST ID (S)   | TEST INFORMATION         | NOZZLE AND WATER FLOW RATE (mm/min)   |
|------|---------------|--------------------------|---------------------------------------|
| 6a   | IFAB-25       | Nozzle characterization. | Nozzle A                              |
| 6b   | IFAB-26       | Nozzle characterization. | Nozzle B                              |
| 6c   | IFAB-27       | Nozzle characterization. | Nozzle C                              |

## 3 TEST SUMMARY AND RESULTS

## 3.1 Inlet Velocity Profile

The inlet  velocity  profile  was  measured  manually  at  25  grid  points  distributed  over  the  cross section at 1.5 m into the tunnel using the handheld rotating vane anemometer (Testo 410i model, typical accuracy plus or minus 0.2 m/s (+2 percent of measured velocity) over a range 0.4 m/s to 20 m/s). The anemometer was held out in front of the person holding the device (i.e., upstream of the person) to minimize disturbance. The blockage of the person holding the anemometer may have added some additional pressure loss to the system, thus causing the fan to operate at a slightly shifted point. To check the effect of this on the measured profiles, fans were run at three speeds, 20 Hz (4.4 m 3 /s airflow), 35 Hz (8.2 m 3 /s airflow), and 50 Hz (12.5 m 3 /s airflow). Measured air speeds at the grid points were compared with the air velocities recorded using the velocity probes  at  the  V015  location  (refer  to  the  schematic  shown  in  Figure  2-11)  to  correlate  the centerline  readings  and  obtain  an  average  flow  rate  during  each  test.  Figure  3-1  shows  a schematic of the 25 grid points distributed over the cross-section of the scale test tunnel. The cross-section was divided into subareas numbered 1 through 6 horizontally, and A through E vertically. Velocity measurements using the anemometer at those 25 grid points were interpolated to the center of each subarea to determine volume flow rate values for the individual subareas. The summation of these subarea flow rates provided the measured anemometer volume flow rate.

Figure 3-1: Sketch of distributed grid points at the cross-section.

<!-- image -->

Scatter plot

Additionally, the air velocities were measured using the velocity probe located at the V015 location on the tunnel centerline (refer to the schematic in Figure 2-11), point C (point V015C, see Table 2-4 and Figure 2-11). This probe is 1.5 m into the tunnel on the centerline at a distance of 781 mm from the tunnel ceiling. The averaged reading was correlated to the measured anemometer flow rate using the equation in Figure 3-2. This was done to enable computation of volume flow during fire tests when it was not possible to use a handheld anemometer. A weight factor ( W ) was derived to match the V015C computed volume flow with the measured anemometer volume flow rate.

Since there exists an inherent uncertainty with all measurement techniques and equipment, a statistical analysis was also performed on this weight factor with a standard deviation of a 95 percent confidence interval. The following weight factors were calculated (calculation reference EVS-01-31):

- 20 Hz fan speed, 0.698 to 0.896, average 0.80.
- 35 Hz fan speed, 0.683 to 0.905, average 0.79.
- 50 Hz fan speed, 0.720 to 0.878, average 0.80.

The V015C computed flow rates were therefore adjusted for the tests with a varying weight factor within the determined range based on the observation of the FDS versus test results. The lowest fan speed data (20 Hz) were used for computation of the weight factor ranges because this was near to the speed that the fan was typically operated during the tests. The weight factor range is quite wide. Causes for this include velocity measurements taken using the velocity probes having more uncertainty  at  low  speeds,  and  exacerbation  of  any  velocity  fluctuations  due  to  relative proximity to the flow straightener.

Figure 3-2: Equation. Calculation of total flow rate with the measured velocity at inlet probe C.

In Figure 3-2, Q is the airflow rate (m 3 /s), W is the derived weight factor to correlate the calculated total flow rate with the measured flow rates per test (ranging from 0.698 to 0.895 with a 95 percent confidence interval), V015C is the average velocity at probe C at the V015 location (m/s) and At is the cross-sectional area of the test tunnel (m 2 ). This equation was used to compute the airflow and average velocity being delivered from upstream of the fire based on the velocity measured (at V015C).

The distribution of points Figure 3-1 is noted to be not uniform in the lateral direction, nor do the points follow a profile such as the Log-Tchebycheff as per ASHRAE Standard 41.2P [6] (note that ASHRAE standards are voluntary and not a Federal requirement). Research for fully developed turbulent flow using numerical flow analysis showed that using a measurement point distribution based on equal areas tends to over-predict the airflow rate by around 2 to 4 percent, while a point distribution based on a Log-Tchebycheff distribution predicts airflow to around plus or minus 1 percent [7]. Due to the test rig arrangement the flow profile was not fully developed and thus it is not  possible  to  compute  explicitly  an  uncertainty  introduced  due  to  the  measurement  point distribution. Numerical analysis was instead used to check the accuracy of the flow measurement approach.

To validate the equation and methodology used, models were run using Ansys Fluent, a general purpose CFD software. The geometry was created like the schematics shown in Figure 2-1 and Figure 2-2 without any fire pool. The turning vanes, flow conditioner and air flaps at 0-degree angle (fully open) were modeled, see Figure 2-4. Velocity data from the Ansys Fluent model were output at the 25 grid points as per Figure 3-1.

Velocity values were interpolated to the center of each subarea to determine volume flow rate values  for  the  individual  subareas.  The  summation  of  these  subarea  flow  rates  provided  the computed total CFD flow rate, which was found to be 3.23 m 3 /s. The actual flow rate that was assigned as the inlet boundary condition was 3.25 m 3 /s. This provided a percent error of 0.62 percent  using  the  methodology  described.  To  verify  the  equation  in  Figure  3-2,  velocity  was determined at V015C by interpolating results from Fluent at the centerline points C and D (i.e., centerline points in Figure 3-1). This velocity was found to be 1.317 m/s. Using the equation from Figure 3-2 with a cross-sectional area of 3.125 m 2  and average weight factor of 0.8, yields a computed airflow rate of 3.29 m 3 /s. This provides a percent error of 1.2 percent, thereby giving confidence in the equation derived and methodology adopted (calculation reference EVS-01-31).

In the FDS models, a weight factor of 0.698 was found to give results that had the best overall agreement with the tests for prediction of backlayering (refer to Section 4.2.2 and Section 4.3.2) and was therefore used unless otherwise noted. In the FDS models, backlayering was not usually observed unless the lower velocity range value (0.698 weight factor) was used. Tunnel centerline velocity  and  a  weight  factor  to  determine  the  total  flow  rate  have  been  used  in  other applications [8].

## 3.2 Airflow Resistance of FFFS and Other Obstructions

Average bulk velocity (based on measurements at probe V015C) results for the cold flow Test 1e/f without the fire shield obstruction in the duct and FFFS operating using Nozzle A are shown in Figure 3-3. The inlet velocity for the test varied over time, averaging 1.85 m/s for the duration of 300 to 540 seconds and 4.15 m/s for the duration of 630 to 900 seconds. The average inlet velocity  weight  factor  of  0.80  was  used  to  compute  the  bulk  velocities  for  reporting  airflow resistance (friction factors) herein. For airflow resistance computation, sensitivity to using a higher or lower weight factor (such as 0.698 to 0.896) is reported in Table 3-1.

The static pressure profiles are plotted relative to the pressure at the entry probe at 1.0 m along the duct (resultant entry pressure = 0 Pa). The static pressure probes were located in the top corner of the duct at 1.0 m (in Figure 2-11 location P010, which is -4.0 m on plot coordinates, just after the flow straightener), 3.0 m (before shield, -2.0 m on plot coordinates), 5.0 m (at the shield, 0.0 m on plot coordinates), 7.5 m (after shield, 2.5 m on plot coordinates), and 11.0 m (near the end of the test section, 6.0 m on plot coordinates). The static pressure increased from the entry probe to the probe before the shield (from -4.0 m to -2.0 m), likely because of the airflow being disturbed at the entry due to the bend. A similar change is seen downstream of the FFFS zone (2.5 m to 6.0 m) with the effect ever so slightly greater when FFFS is operated. The cause of this effect at this location was not able to be determined. The slight increase in the effect with FFFS operating is suggestive of a flow disturbance effect, but this is not the definite cause since cases without FFFS should not have had a disturbed flow. The pressure changes reported herein were computed from -2.0 m coordinate to 6.0 m coordinate. They were not computed from -4.0 m coordinate due to its proximity to the bend and flow conditioner, which likely influenced the flow and subsequent pressure. Also note, that pressure was measured at one point in the tunnel (top corner) and if the flow was disturbed or not developed, then a pressure reading at a different point in the cross section could give a different value. Therefore, a quantitative analysis is shown, but the unreliability of measurements should be kept in mind when using the data.

Figure 3-4 shows the static pressure along the test tunnel before and after FFFS was operated for  Test  1e/f  with  1.85  m/s  average  bulk  velocity  at  the  inlet.  Results  show  no  discernable difference due to the FFFS. That is, pressure change was found to be 1.6 Pa (approximately) with or without the FFFS operational. Figure 3-5 shows the static pressure along the scale test tunnel before and after FFFS was operated for Test 1e/f with 4.15 m/s average bulk velocity at the inlet. Results show no discernable difference due to the operation of the FFFS. Similarly, the pressure change is about 1.5 Pa. A reason for the pressure change being identical at the two different air speeds,  which  was  not  an  expected  result,  was  not  able  to  be  determined.  This  finding emphasizes  the  previous  paragraph's  points  about  measurement  unreliability  for  pressure.  It should be noted that the average bulk velocities reported herein are different than the values shown  in  Table  2-5.  This  is  because  values  shown  in  Table  2-5  were  approximates  of  the expected velocities (i.e., values planned to be used in the tests, not the actual values realized).

Figure 3-3: Test 1e/f, the average bulk velocity with and without FFFS using Nozzle A.

<!-- image -->

Line chart

Figure 3-4: Test 1e/f, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle A at 1.85 m/s inlet velocity.

<!-- image -->

Line chart

Figure 3-5: Test 1e/f, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle A at 4.15 m/s inlet velocity.

<!-- image -->

Line chart

Average bulk velocity results for the cold flow Test 1g/h with no obstruction in the duct and FFFS operating using Nozzle B are shown in Figure 3-6. The inlet velocity for the test was varied over time, averaging at 1.85 m/s for the duration of 200 to 460 seconds and 4.15 m/s for the duration of 520 to 800 seconds. An average inlet velocity weight factor of 0.80 was used to compute the bulk velocities shown on the plots (sensitivity to this is reported in Table 3-1). Nozzle B, with a smaller droplet size than Nozzle A, had a water application rate of 2.1 mm/min.

Figure 3-7 shows the static pressure along the tunnel before and after FFFS was operated for Test 1g/h with 1.85 m/s average bulk velocity at the inlet. Results show no discernable difference. Pressure change was approximately 1.7 Pa. Figure 3-8 shows the static pressure along the tunnel before and after FFFS was operated for Test 1g/h with 4.15 m/s average bulk velocity at the inlet. Pressure change before FFFS was found to be approximately 3.2 Pa and approximately 4.2 Pa after FFFS was operated. Results show increased pressure change with FFFS for this test. This was the only test which showed a different pressure change due to the FFFS. This might have been due to the larger number of nozzles used for the Nozzle B arrangement (causing increased pressure changes), and the larger air speed (larger pressure changes, thus possibly meaning that pressure changes due to FFFS were, for this test, more than the measurement error).

As noted above, pressure was measured at one point in the tunnel (top corner) and if the flow was disturbed or not developed, then a pressure reading at a different point in the cross section could give a different value. The unreliability of measurements should be kept in mind when using the data and caution is recommended in taking too much from the quantitative results herein.

Figure 3-6: Test 1g/h, average bulk velocity with and without FFFS using Nozzle B.

<!-- image -->

Line chart

Figure 3-7: Test 1g/h, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle B at 1.85 m/s inlet velocity.

<!-- image -->

Line chart

Figure 3-8: Test 1g/h, static pressure along the tunnel before (left) and after (right) FFFS was operated using Nozzle B at 4.15 m/s inlet velocity.

<!-- image -->

Line chart

A calculation was conducted to compute the loss factor (K) and the friction factor (f), per equations provided in Figure 3-9, Figure 3-10 and Figure 3-11.

Figure 3-9: Equation. Pressure loss equation based on total loss factor.

Figure 3-10: Equation. Pressure loss equation based on duct friction factor.

## Figure 3-11: Equation. Hydraulic diameter.

In Figure 3-9, Figure 3-10 and Figure 3-11, symbols are as follows: ∆ P is the pressure change along the duct (Pa), K is the loss factor, ρ is the density (kg/m 3 ), f is the friction factor, L is the tunnel length (m), Dh is the tunnel hydraulic diameter (m), A is the tunnel area (m 2 ), and P is the tunnel perimeter (m).

Table 3-1 summarizes the calculation results for K factor and friction factor based on pressure changes from the cold flow tests. The results in this table were taken from similar times to the results shown on plots in Figure 3-3 to Figure 3-8 but not at the exact same times, and they are based on averaged raw data rather than reading from plots, so there is some variation in the exact values for velocity and pressure quoted. The calculation includes the lower bound, average, and upper bound values for the K factor and friction factor computed based on the statistical analysis performed for the weight factors (per equation in Figure 3-2) in Section 3.1. In the calculations the following values were used unless noted: tunnel length was 8 m (static pressure from the probes at 3 m and 11 m; the probe at 1 m was not used because flow was disturbed in this region), the area  was  3.125 m 2 ,  hydraulic  diameter  was  1.67 m,  and  ambient  temperature  was  15 °C  for purposes of density calculation (assumed ideal gas, giving resultant density of 1.23 kg/m 3 ). Inlet velocity and other items that varied between tests are quoted in the table. The following points are noted regarding results in Table 3-1:

- K factors and friction factors were quite varied between the low inlet velocity cases and the higher inlet velocity cases (Tests 1e/f and 1g/h). Given that the velocity measurement from the velocity probes is more uncertain at lower air speeds (~1 m/s), the higher inlet velocity cases (~4 m/s) are suggested to be more reliable. The differences between low air speeds and  higher  air  speeds  suggest,  as  discussed  on  previous  pages  in  this  section,  that  the measurement reliability is low and the quantitative results herein for pressure changes are not very reliable.
- Test 1a/b had no internal duct obstruction, while Test 1d had the shield installed. Average K factor  increase  for  the  shield  inclusion  was  0.25  (0.81  average  K  factor  with  shield,  0.56 average  K  factor  with  no  shield).  The  loss  factor  with  no  shield  present  was  higher  than expected (typical duct friction factor with smooth walls is on the order of 0.02, or an equivalent

K factor around 0.1). The duct was mostly empty except for some instrumentation, a small sign, and a rough floor. Other similar tests to Test 1a/b included Test 1e/f (K factor 0.12) and Test g/h (K factor 0.3). These differences in results, which should have had an approximately equal K factor, provide further basis for low measurement reliability. Quantitative analysis of airflow resistance due to FFFS and other obstructions is provided below, but the unreliability of measurements should be kept in mind when using the data.

- For Nozzle A at around 4 m/s inlet velocity, the change in friction factor introduced by the FFFS is very small (increase in friction factor of 0.01, K factor increase of 0.05) (Test 1e/f).
- For Nozzle B at around 4 m/s inlet velocity, the change in friction factor introduced by the FFFS is more than Nozzle A (increase in friction factor of 0.03, K factor increase of 0.11) (Test 1g/h).
- Test 1c had a different internal obstruction designed to mimic a set of pipes at regular spacing in a duct. The obstruction was comprised of regularly and symmetrically spaced blockages, a long wooden prismatic object 2000 mm long, 100 mm high by 80 mm wide on the floor of the duct. The first blockage was placed at approximately 3 m along the duct, and there were a total of four blockages, equally spaced at around 1 m spacing. Refer to Figure 3-12. The loss factor for these blockages was 0.72 (average K factor with no internal obstruction was 0.56).
- The conclusions above provide a quantitative analysis but as mentioned before, caution is recommended nonetheless due to the possible unreliability of the measurements.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-12: Test 1c blockages.

Table 3-1: Summary of pressure changes from the cold flow tests (EVS-01-22).

| ID   | TEST ID   | K FACTOR (LOWER, AVERAGE, UPPER)   | FRICTION FACTOR (LOWER, AVERAGE, UPPER)   |   INLET V (m/s) |   PRESSURE CHANGE (Pa) | DESCRIPTION                                                                                |
|------|-----------|------------------------------------|-------------------------------------------|-----------------|------------------------|--------------------------------------------------------------------------------------------|
| 1e/f | IFAB-16   | 0.57, 0.72, 0.95                   | 0.12, 0.15, 0.2                           |            1.83 |                   1.48 | FFFS off, used test data from 300 s to 360 s                                               |
| 1e/f | IFAB-16   | 0.72, 0.91, 1.19                   | 0.15, 0.19, 0.25                          |            1.77 |                   1.75 | Nozzle A at 3.4 mm/min water application rate, used test data from 420 s to 480 s          |
| 1e/f | IFAB-16   | 0.10, 0.12, 0.16                   | 0.02, 0.03, 0.03                          |            4.14 |                   1.26 | FFFS off, used test data from 600 s to 720 s                                               |
| 1e/f | IFAB-16   | 0.14, 0.17, 0.23                   | 0.03, 0.04, 0.05                          |            4.18 |                   1.84 | FFFS on, Nozzle A at 3.4 mm/min water application rate, used test data from 810 s to 870 s |
| 1g/h | IFAB-17   | 0.70, 0.88, 1.16                   | 0.15, 0.18, 0.24                          |            1.91 |                   1.96 | FFFS off, used test data from 180 s to 270 s                                               |
| 1g/h | IFAB-17   | 0.62, 0.78, 1.02                   | 0.13, 0.16, 0.21                          |            1.88 |                   1.68 | FFFS on, Nozzle B at 2.0 mm/min water application rate, used test data from 360 s to 450 s |
| 1g/h | IFAB-17   | 0.24, 0.30, 0.39                   | 0.05, 0.06, 0.08                          |            4.19 |                   3.19 | FFFS off, used test data from 540 s to 630 s                                               |
| 1g/h | IFAB-17   | 0.33, 0.41, 0.54                   | 0.07, 0.09, 0.11                          |            4.09 |                   4.21 | FFFS on, Nozzle B at 2.0 mm/min water application rate, used test data from 720 s to 810 s |
| 1a/b | IFAB-02   | 0.56, 0.70, 0.92                   | 0.12, 0.15, 0.19                          |            3.09 |                   4.09 | No duct obstructions, used test data from 990 s to 1050 s                                  |
| 1a/b | IFAB-02   | 0.42, 0.53, 0.69                   | 0.09, 0.11, 0.14                          |            4.09 |                   5.40 | No duct obstructions, used test data from 1212 s to 1248 s                                 |
| 1a/b | IFAB-02   | 0.37, 0.46, 0.61                   | 0.08, 0.10, 0.13                          |            3.90 |                   4.32 | No duct obstructions, used test data from 1332 s to 1434 s                                 |
| 1d   | IFAB-05   | 0.63, 0.79, 1.04                   | 0.13, 0.16, 0.22                          |            3.83 |                   7.11 | Shield included, used test data from 666 s to 684 s                                        |
| 1d   | IFAB-05   | 0.61, 0.76, 1.0                    | 0.13, 0.16, 0.21                          |            4.15 |                   8.01 | Shield included, used test data from 726 s to 744 s                                        |
| 1d   | IFAB-05   | 0.71, 0.89, 1.17                   | 0.15, 0.18, 0.24                          |            3.35 |                   6.11 | Shield included, used test data from 816 s to 834 s                                        |
| 1c   | IFAB-03   | 0.54, 0.67, 0.88                   | 0.11, 0.14, 0.18                          |            3.52 |                   5.11 | No shield, internal obstacles included, used test data from 666 s to 684 s                 |
| 1c   | IFAB-03   | 0.56, 0.70, 0.92                   | 0.12, 0.15, 0.19                          |            3.79 |                   6.14 | No shield, internal obstacles included, used                                               |

| ID   | TEST ID   | K FACTOR (LOWER, AVERAGE, UPPER)   | FRICTION FACTOR (LOWER, AVERAGE, UPPER)   |   INLET V (m/s) |   PRESSURE CHANGE (Pa) | DESCRIPTION test data from 726 s to                                              |
|------|-----------|------------------------------------|-------------------------------------------|-----------------|------------------------|----------------------------------------------------------------------------------|
| 1c   | IFAB-03   | 0.64, 0.80, 1.06                   | 0.13, 0.17, 0.22                          |            3.07 |                   4.65 | 744 s No shield, internal obstacles included, used test data from 816 s to 834 s |

## 3.3 Fire Heat Release Rate and Thermal Environment

## 3.3.1  Heat Release Rate Measurements

The FHRR was measured by two methods:

1. A scale to record the mass consumption rate of fuel (HRR is fuel heat of combustion times mass consumption rate).
2. Oxygen consumption calorimetry [9].

The fire pan configuration included water in the pan added before the fuel was filled in. This was done to guard against the pan deforming during the test, thus influencing the FHRR. In some of the tests water evaporated due to boiling (observed via real-time video footage) and sometimes there was water dripping into the pan from the shield (despite best efforts of design to avoid this, in some cases water found a pathway into the pan).

The water level in the pan as well as the level of water with fuel was measured at the beginning of the test. Additionally, the level of the remaining fluid, which can be water or a mixture of water and fuel, was measured at the end of the test. The change of the levels during the fire test was compared to the mass loss in the pan. The assumption is that the mass loss and change of levels is only generated by combustion of the fuel. If the mass loss does not match to the change of levels, there could be some amount of water responsible for the deviation. An adjustment to the mass loss rate was made accounting for water evaporation or dripping into the pan. The correction was based on integrated mass conservation and observation of video footage to quantify times when water was most likely entering or leaving the pan.

Toward the end of some tests as the fuel had mostly burned off, water was observed to boil, and this  caused a secondary peak in the FHRR due to the boiling disturbing the fuel surface and increasing the fuel surface area as a result (like the fire flare up phenomenon observed when water is thrown onto a burning oil fire).

After completion of the test series the scale was found to be damaged as part of some future unrelated work. FHRR data from the tests were revisited as a result. The damage was determined to have occurred most likely during test IFAB-13. This determination was based on the correction for  water  level  change  failing  to  give  reasonable  results  after  this  test,  and  also  based  on observations during the test. In test IFAB-13 a lot of n-heptane burned and water evaporated in a short amount of time, and the area next to the scale was surrounded by burning fuel. It was possible  that  a  cable  might  have  been  damaged  during  this  event,  making  the  scale measurements after this time less reliable.

As a result of this situation with the scale, the oxygen consumption FHRR data were used as well. The  early  tests  where  the  scale  was  working,  show  reasonable  correlation  between  the  two methods. Calibration of the oxygen consumption method was conducted to account for factors such as the measured velocity and concentrations, since measurement points downstream of the fire  were  not  able  to  cover  the  whole  tunnel  cross  section.  Based  on  previous  experience, uncertainty in the oxygen consumption data with the method used to compute FHRR could be as high as plus or minus 30 percent, and the oxygen consumption data tends to lag in time due to sensors being downstream of the fire (minor effect here due to relatively short distane) and time for different gas sensors to reach equilibrium (could be on the order of 30 seconds depending on the rate of change in test conditions). Plots of FHRR with the oxygen consumption method are generated with a 20 percent range and this is considered in the FDS analysis (see Chapter 4). FHRR information from the tests is sumarized in Table 3-2 including reference to FHRR plots from each test. On FHRR plots a Bézier spline smoothing function is applied to allow overall trends to be seen, rather than instantaneous fluctuations.

The comparison between FHRR methods is better in some cases than others (see Figure 3-16, Figure 3-17 and Figure 3-18). The best comparisons were for cases with diesel fuel. The diesel fuel fires in the tests were generally slower to grow and it may have been that the slower changes in the FHRR with diesel were better able to be captured than the fires with n-heptane. The results herein demonstrate that there is a correlation between the two methods of computing FHRR but also  significant  uncertainty.  This  point  should  be  kept  in  mind  when  making  conclusions, developing models, etc. Note that in this report FHRR results reported herein are based on the oxygen consumption method unless noted otherwise.

Table 3-2: FHRR notes.

| DATE ID     | TEST ID, SERIES ID   | NOTES ON FHRR                                                                                                                                                                                                                                   |
|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 20220215-03 | IFAB-07, 3a          | O 2 results unreliable, sensor did not reach equilibrium, n-heptane                                                                                                                                                                             |
| 20220216-01 | IFAB-08, 5a          | Similar HRR from both methods, n-heptane, see Figure 3-13                                                                                                                                                                                       |
| 20220216-02 | IFAB-09, 5a          | Similar HRR from both methods, n-heptane, see Figure 3-14                                                                                                                                                                                       |
| 20220216-03 | IFAB-10, 4a          | HRR from O2 method larger than mass loss rate by factor of 2, n-heptane, see Figure 3-15                                                                                                                                                        |
| 20220216-04 | IFAB-11, 4a          | Similar HRR from both methods, diesel, see Figure 3-16                                                                                                                                                                                          |
| 20220217-01 | IFAB-12, 5a          | Similar HRR from both methods, test aborted due to hose failure, diesel, see Figure 3-17                                                                                                                                                        |
| 20220217-02 | IFAB-13, 5a          | Scale damaged during this test, similar HRR from both methods, diesel, see Figure 3-18                                                                                                                                                          |
| 20220217-03 | IFAB-14, 5b          | HRR from O 2 method only, diesel, see Figure 3-19                                                                                                                                                                                               |
| 20220217-04 | IFAB-15, 5b          | HRR from O 2 method only, diesel, see Figure 3-20                                                                                                                                                                                               |
| 20220222-01 | IFAB-19, 4b          | HRR from O 2 method only, diesel, see Figure 3-21 (test showed an increase in the FHRR after the FFFS was operated, scale results were checked too and although unreliable for this test suggested a similar behavior, as did temperature data) |
| 20220222-02 | IFAB-20, 7b          | HRR from O 2 method only, diesel, see Figure 3-22                                                                                                                                                                                               |
| 20220222-03 | IFAB-21, 7a          | HRR from O 2 method only, diesel, see Figure 3-23                                                                                                                                                                                               |
| 20220222-04 | IFAB-22, 3a          | HRR from O 2 method only, diesel, see Figure 3-24                                                                                                                                                                                               |
| 20220222-06 | IFAB-24, 3b          | HRR from O 2 method only, diesel, see Figure 3-25                                                                                                                                                                                               |

Figure 3-13: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-08 (5a).

<!-- image -->

Line chart

Figure 3-14: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-09 (5a).

<!-- image -->

Line chart

Figure 3-15: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-10 (4a).

<!-- image -->

Line chart

Figure 3-16: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-11 (4a).

<!-- image -->

Line chart

Figure 3-17: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-12 (5a).

<!-- image -->

Line chart

Figure 3-18: FHRR plot comparing scale FHRR and O2 FHRR, test IFAB-13 (5a).

<!-- image -->

Line chart

Figure 3-19: FHRR plot from O2 FHRR, test IFAB-14 (5b).

<!-- image -->

Line chart

Figure 3-20: FHRR plot from O2 FHRR, test IFAB-15 (5b).

<!-- image -->

Line chart

Figure 3-21: FHRR plot from O2 FHRR, test IFAB-19 (4b).

<!-- image -->

Line chart

Figure 3-22: FHRR plot from O2 FHRR, test IFAB-20 (7b).

<!-- image -->

Line chart

Figure 3-23: FHRR plot from O2 FHRR, test IFAB-21 (7a).

<!-- image -->

Line chart

Figure 3-24: FHRR plot from O2 FHRR, test IFAB-22 (3a).

<!-- image -->

Line chart

Figure 3-25: FHRR plot from O2 FHRR, test IFAB-24 (3b).

<!-- image -->

Line chart

## 3.3.2 Results

Fire tests with FFFS were performed using Nozzle A, Nozzle B, and Nozzle C respectively, with Figure 3-26, Figure 3-27, and Figure 3-28 showing the results comparing FHRR varying over time for the three different nozzles. 'FFFS start' indicates the approximate time at which the water pressure reached the target value, the actual pump start time was around 30 to 60 seconds before this. Ignition time indicates when the fuel was ignited.

Results show that Nozzle A FFFS with a large water droplet size (1.12 mm) had less impact on the FHRR than the Nozzle B FFFS with a small water droplet size (0.28 mm). Comparing results between Nozzle B and C FFFS (smaller drop sizes, 0.28 mm, and 0.13 mm respectively) shows that both test cases had FHRR profiles that were reduced after the FFFS was operated. The smaller drops (relative to Nozzle A) have a greater cooling potential due to increased surface area and  this  reduced  the  heat  feedback  to  the  fire  surface  and  hence  the  FHRR  more  than  the larger drops.  For  tests  with  smaller  fire  potential  (4a,  5a,  7a),  this  effect  was  not  observed. It is noted that Nozzle B had a FHRR profile that decreased with time, while Nozzle  C's  FHRR profile  remained  approximately  constant  after  an  initial  reduction  when  FFFS  was  operated. The reason for this was not able to be determined from the data, but it might have been due to the  Nozzle  B  droplets  achieving  an  optimal  balance  between  the  total  surface  area  (cooling potential) and momentum allowing them to penetrate the fire plume achieve an increased rate of fire suppression.

A secondary peak in the FHRR is observed for the Nozzle A tests in Figure 3-26. This peak was likely  due  to  the  water  in  the  fire  pan  boiling  and  causing  an  increase  in  the  FHRR.  This phenomenon was observed in late stages of several tests. The increasing FHRR in this test after the  water  was  operated  was  surprising.  The  temperature  profiles  at  the  tunnel  ceiling  were checked and showed a result that suggested FHRR was not decreasing.

Figure 3-26: Test 4b, measured FHRR varying over time with FFFS using Nozzle A.

<!-- image -->

Line chart

Figure 3-27: Test 5b, measured FHRR varying over time with FFFS using Nozzle B.

<!-- image -->

Line chart

Figure 3-28: Test 7b, measured FHRR varying over time with FFFS using Nozzle C.

<!-- image -->

Line chart

Figure 3-29, Figure 3-31, and Figure 3-33 show the contours for the temperature at the scale test tunnel ceiling, cropped to 120 degrees Celsius (purpose was smoke control visualization rather than temperature magnitude downstream) varying over time for the three different test nozzles. Upstream bulk velocity is shown for corresponding cases in Figure 3-30, Figure 3-32, and Figure 3-34  respectively.  The  fire  location  is  at  0  m,  indicated  by  the  vertical  line.  Smoke  control (measured by the gas temperature near to the tunnel ceiling) is seen to improve when FFFS was operated. FFFS with small water droplets was observed to provide a faster cooling effect, thereby resulting in a faster response for smoke control.

Figure 3-29: Test 4b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle A.

<!-- image -->

Line chart

Figure 3-30: Test 4b, bulk velocity upstream of the fire.

<!-- image -->

Line chart

Figure 3-31: Test 5b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle B.

<!-- image -->

Line chart

Figure 3-32: Test 5b, bulk velocity upstream of the fire.

<!-- image -->

Line chart

Figure 3-33: Test 7b, contour of tunnel gas temperature (degrees Celsius) at centerline near the ceiling with FFFS using Nozzle C.

<!-- image -->

Line chart

Figure 3-34: Test 7b, bulk velocity upstream of the fire.

<!-- image -->

Line chart

Figure 3-35, Figure 3-36, and Figure 3-37 show temperatures at the ceiling along the length of the scale test tunnel. Results are shown 10 seconds before the FFFS is operated and 60 seconds after the FFFS was operated. The fire location is at 0 m, indicated by the solid vertical line. Smoke control (measured by the temperature at the ceiling) was improved when FFFS was operated. The result in Figure 3-35 is suggestive of the FHRR not changing, or more likely increasing since downstream of the fire the temperature is the same after FFFS was operated (i.e., cooling effect of the FFFS water is offset by increasing FHRR). Results in Figure 3-2 6 show increasing FHRR.

Overall, the temperature downstream was found to be lower for FFFS with smaller water droplets. Figure 3-36 shows temperature with Nozzle B at 60 s after FFFS operation, with a downstream temperature of approximately 180 °C, FHRR approximately 1.1 MW per Figure 3-27). Figure 3-37 shows temperature with Nozzle C at 60 s after FFFS operation, with a downstream temperature of approximately 80 °C, FHRR approximately 1.1 MW per Figure 3-28.

Figure 3-35: Test 4b, temperature at the ceiling with FFFS using Nozzle A larger drop.

<!-- image -->

Line chart

Figure 3-36: Test 5b, temperature at the ceiling with FFFS using Nozzle B smaller drop.

<!-- image -->

Line chart

Figure 3-37: Test 7b, temperature at the ceiling with FFFS using Nozzle C.

<!-- image -->

Line chart

## 3.4 Critical/Confinement Velocity

Backlayering was judged based on monitoring the test videos as well as the FHRR, temperatures, and velocity data measured. It should be noted that the velocities here might not be considered 'critical velocity' to prevent backlayering, but instead might represent a 'confinement velocity' that is  sufficient  to  stop  smoke  movement  upstream  of  the  fire  but  not  to  absolutely  prevent backlayering. For visualization purposes figures include:

- Figure 3-38 and Figure 3-39 show snapshots in time of Test 4b before and after FFFS was activated.
- Figure 3-40 and Figure 3-41 show snapshots in time of Test 5b before and after FFFS was activated.
- Figure 3-42 and Figure 3-43 show snapshots in time of Test 7b before and after FFFS was activated.

Backlayering fluctuated in the tests but was controlled after FFFS was activated in all three cases. It is difficult to determine the distance of backlayering upstream when the FFFS was operated due  to  visual  obscuration  by  the  water  spray.  Prior  to  operation  of  the  FFFS  backlayering distances were on the order of 2.0 m to 2.5 m. After the FFFS was operated backlayering was only observed for Test 4b (Nozzle A) and it was limited to 0.5 m distance upstream (see Figure 3-26).

<!-- image -->

Photograph

© IFAB 2022

Figure 3-38: Test 4b, a snapshot of tunnel cross-section showing smoke backlayering.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-39: Test 4b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle A.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-40: Test 5b, a snapshot of tunnel cross-section showing smoke backlayering.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-41: Test 5b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle B.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-42: Test 7b, a snapshot of tunnel cross-section showing smoke backlayering.

<!-- image -->

Photograph

© IFAB 2022

Figure 3-43: Test 7b, a snapshot of tunnel cross-section 30 seconds after FFFS activated using Nozzle C.

Since the FHRR was a transient process throughout the duration of each test it was difficult to compare results with the critical velocity equations. Some judgment was needed to extract results for comparison and even then, the transient nature means the comparison to equations based on steady state analysis is tentative at best.

The data used to generate comparative results in Figure 3-44 are provided in Table 3-3. Note that the average velocities from the test quoted are based on the average weight factor of 0.8 (refer to Section 3.1). Figure 3-44 shows the experimental results compared with the 2014 NFPA 502

equation (calculation reference EVS-01-20) indicating a reduction in smoke control velocity with the FFFS operating. The height used for the computation was the tunnel height. The transient nature of the FHRR made it difficult determine critical or confinement velocity without the FFFS operating. For tests where no backlayering is recorded the velocity was quite a bit higher than the NFPA  equation  results.  This  is  more  likely  a  result  of  the  test  behavior  rather  than  a  true representation of critical or confinement velocity. The FHRR was changing with time and generally increasing. Thus, if the fan speed was turned down, by the time the impact of this could be seen, the FHRR had increased and backlayering was starting to occur. As a result, the velocity was usually kept higher than critical in the early stages of the test until backlayering started to occur. The FFFS usually had to be operated shortly after this time because the FHRR was continuing to grow and there was a concern the fire could get larger and damage the test rig.

Table 3-3: Parameters used for computation of critical velocity per NFPA 502 2014 equation.

| PARAMETER                        | VALUE                                                     | NOTES                                                                         |
|----------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------------------|
| Width of tunnel                  | 2.5 m                                                     | Test tunnel dimension                                                         |
| Height of tunnel                 | 1.25 m                                                    | Test tunnel dimension, value of height parameter used in calculation          |
| Area of tunnel (free area)       | 3.125 m 2                                                 | Test tunnel dimension                                                         |
| Blockage from fire shield        | 0.68 m tall, 1.1 m wide, giving a free area fraction 0.76 | Used annular (perpendicular to flow) area in computation of critical velocity |
| Radiative fraction               | 30 percent                                                | Assumed, typical value used                                                   |
| Ambient temperature              | 15 ⁰ C                                                    | Typical for most tests                                                        |
| Grade                            | 0 percent                                                 | Test tunnel parameter                                                         |
| Test data, backlayer, no FFFS    | 1.70 MW, 1.25 m/s                                         | Test IFAB-15, 5B at 410 s                                                     |
| Test data, backlayer, no FFFS    | 1.35 MW, 1.25 m/s                                         | Test IFAB-19, 4B at 350 s                                                     |
| Test data, backlayer, no FFFS    | 0.80 MW, 1.15 m/s                                         | Test IFAB-22, 3A at 340 s                                                     |
| Test data, backlayer, no FFFS    | 1.70 MW, 1.30 m/s                                         | Test IFAB-24, 3B at 420 s                                                     |
| Test data, backlayer, no FFFS    | 1.90 MW, 1.25 m/s                                         | Test IFAB-20, 7B at 350 s                                                     |
| Test data, no backlayer, FFFS    | 1.10 MW, 1.10 m/s                                         | Test IFAB-15, 5B at 480 s                                                     |
| Test data, no backlayer, FFFS    | 1.25 MW, 1.15 m/s                                         | Test IFAB-19, 4B at 420 s                                                     |
| Test data, no backlayer, FFFS    | 1.10 MW, 1.15 m/s                                         | Test IFAB-20, 7B at 420 s                                                     |
| Test data, no backlayer, no FFFS | 0.50 MW, 1.75 m/s                                         | Test IFAB-22, 3A at 515 s                                                     |
| Test data, no backlayer, no FFFS | 1.30 MW, 1.75 m/s                                         | Test IFAB-24, 3B at 515 s                                                     |

Figure 3-44: Critical velocity results compared with 2014 NFPA 502 equation.

<!-- image -->

Line chart

## 3.5 Adiabatic Surface Temperature

Figure 3-45 shows the FHRR for four selected tests. Lines are provided on this figure to mark times  of  interest.  Figure  3-46  (1  m  downstream  at  ceiling),  Figure  3-47  (1  m  downstream  at sidewalls), Figure 3-48 (4.5 m downstream at ceiling) and Figure 3-49 (4.5 m downstream at sidewalls) provide adiabatic surface temperatures for the tests.

The results are compared at times when FHRR is approximately the same, and prior to FFFS operation. Refer to Table 3-4. The results show the following:

- 1 m downstream at ceiling, inconsistency in results (e.g., test IFAB-08 versus IFAB-09).
- 1 m downstream at sidewall, inconsistency in results (e.g., test IFAB-03 versus IFAB-08).
- 4.5 m downstream at ceiling, results are getting closer to agreeing with one another (e.g., IFAB-03 versus IFAB-08 versus IFAB-09) although some results still are not quite as expected (e.g., IFAB-15).
- 4.5 m downstream at sidewall, results are consistent with one another.

Note the peak temperature for the diesel fuel downstream of the fire was substantially lower than the  heptane  fuel.  This  difference  could  be  related  to  the  radiation  being  shielded  through increased soot yield. However, analysis with FDS suggested that fuel chemistry sensitivity and soot yield effect on the adiabatic surface temperature was minor.

The  inconsistency  in  results  might  be  a  result  of  damage  to  the  instruments,  measurement accuracy limits or possibly even effects from the water spray. Given the inconsistency in results it is suggested that these data are interpreted with caution and used for qualitative considerations only.

Overall, operating the FFFS was seen to reduce the adiabatic surface temperatures both at the ceiling  and  the  wall,  but  the  degree  of  cooling  should  be  interpreted  with  caution  because  of difficulty in achieving consistent results as noted.

Table 3-4: Adiabatic surface temperature (AST) selected results.

| TEST         | FUEL      |   TIME (s) |   FHRR (kW) |   AST 1 m DS AT CEILING (°C) |   AST 1 m DS AT SIDE (°C) |   AST 4.5 m DS AT CEILING (°C) |   AST 4.5 m DS AT SIDE (°C) |
|--------------|-----------|------------|-------------|------------------------------|---------------------------|--------------------------------|-----------------------------|
| IFAB-03 (3a) | n-heptane |        435 |        1100 |                          120 |                       105 |                             85 |                          50 |
| IFAB-08 (5a) | n-heptane |        390 |        1100 |                          155 |                       290 |                             90 |                          60 |
| IFAB-09 (5a) | n-heptane |        390 |        1100 |                          240 |                       290 |                            100 |                          60 |
| IFAB-03 (3a) | n-heptane |        455 |        1500 |                          205 |                       120 |                            140 |                          70 |
| IFAB-15 (5b) | diesel    |        390 |        1500 |                           80 |                       160 |                             40 |                          60 |

Figure 3-45: Measured FHRR varying over time.

<!-- image -->

Line chart

Figure 3-46: Adiabatic surface temperature at the ceiling, 1 m downstream of fire.

<!-- image -->

Line chart

Figure 3-47: Adiabatic surface temperature at the sidewall, 1 m downstream of fire.

<!-- image -->

Line chart

Figure 3-48: Adiabatic surface temperature at the ceiling, 4.5 m downstream of fire.

<!-- image -->

Line chart

Figure 3-49: Adiabatic surface temperature at the sidewall, 4.5 m downstream of fire.

<!-- image -->

Line chart

## 3.6 Static Pressure Measurements During Fire Conditions

Static pressure measurements were recorded with for cases without fire (Section 3.2) and with fire. This section is concerned with fire scenarios and the aim was to record pressure changes due to fire and FFFS operation. Pressure was measured using differential pressure sensors with reported uncertainty of plus or minus 1 percent, however a likely measurement uncertainty of plus or minus 5 percent was noted (refer to Table 2-3). Results from Tests 4b, 5b and 7b are reported. Static  pressure  probes  were  located  in  the  top  corner  of  the  duct  at  1.0 m  (-4.0  m  on  plot coordinates,  just  after  flow  straightener),  3.0 m  (before  shield),  5.0 m  (at  shield),  7.5 m  (after shield), and 11.0 m (near end of test section). It should be noted that the results near -4.0 m coordinate  may  have  been  influenced  by  the  bend  and  flow  conditioner  due  to  the  sensor's proximity  at  this  location  and  the  subsequent  undeveloped  flow.  Furthermore,  sensors  were placed only in the upper corner of the tunnel and this factor also likely influenced readings where the flow was not fully developed and uniform over the cross section. Results herein should thus be interpreted carefully and not relied on too much for precise quantitative use.

Figure  3-50  shows  the  time-averaged  static  pressure  results  for  Test  4b  (Nozzle  A),  from  20 seconds to 10 seconds before the FFFS is operated, and from 50 seconds to 60 seconds after the FFFS is operated. During the selected times, velocity profile was mostly steady. Similar plots are provided for Test 5b (Nozzle B) and Test 7b (Nozzle C) in Figure 3-51 and Figure 3-52, respectively. While the static pressure measurements may have not been very reliable/accurate for making firm quantitative conclusions, but some relative comparisons may be possible:

- The pressure profiles for Test 4b (Figure 3-50) appears reasonable. There is an increase from the entry to the next pressure probe and then a decreasing pressure along the duct length. The pressure losses due to fire alone appear minor, and there is slightly more pressure loss when the FFFS is operated.
- Pressure profiles for Test 5b (Figure 3-51) are similar, except for a decrease in the region of the fire, and then pressure increase beyond the fire. This is suggestive of a disturbed airflow in this region; however, this result is not observed in the other two cases, which had the same fire  shield  configuration.  The  cause  may also have been related to fire dynamics differing between tests, or even a problem with one of the static pressure probes.
- Pressure profiles for Test 7b (Figure 3-52) are like Test 4b, except for some slight pressure recovery toward the exit of the tunnel. Like above, the precise reason for this is not able to be determined.
- In all cases, the pressure at the exit of the tunnel is lower when the FFFS is operating. The magnitude of the difference is approximately 0.5 Pa for Nozzle A and B, and slightly less for Nozzle C. This is suggestive of the FFFS introducing some additional pressure loss for airflow through the tunnel.
- Figure 3-30, Figure 3-32, and Figure 3-34 show the upstream bulk velocity for tests 4b, 5b and 7b, respectively. For each test, average velocity from 40 seconds prior to time of FFFS operation to time of operation, and 60 s to 100 s after FFFS operation was as follows: test 4b (1.4 m/s, 1.2 m/s, before and after FFFS operation respectively), test 5b (1.3 m/s, 1.0 m/s), and test 7b (1.2 m/s, 1.2 m/s). The velocity decreases slightly in each test (or remains the same in the case of Nozzle C), suggesting some additional pressure resistance due to the FFFS.

Figure 3-50: Test 4b (Nozzle A), static pressure before and after FFFS operation.

<!-- image -->

Line chart

Figure 3-51: Test 5b (Nozzle B), static pressure before and after FFFS operation.

<!-- image -->

Line chart

Figure 3-52: Test 7b (Nozzle C), static pressure before and after FFFS operation.

<!-- image -->

Line chart

## 3.7 Relative Humidity

Relative humidity was measured at the tunnel inlet and exit. It was expected that the relative humidity of the air should increase at the tunnel exit due to action of the FFFS. The FFFS water should evaporate due to fire, thereby increasing the concentration of water in the air (and relative humidity) at the tunnel exit. However, in some instances this was not observed. While this might have been due to a temperature increase (thus increasing the amount of water air could hold), in some instances the humidity was already 100 percent at the tunnel inlet. The data are reported herein, but it is suggested to view the results with caution because it is likely there was a problem with the instrumentation in many of these tests.

Relative humidity results for Test 4b with FFFS using Nozzle A are shown in Figure 3-53. The measured FHRR for the test is shown in Figure 3-54. An increase in relative humidity is observed downstream of the fire up to around 480 seconds. A decrease is seen in the relative humidity after 500 seconds. This is not a behavior that was expected given the FFFS was operating, even with the temperature increasing downstream and with time. The cause may have been a problem with instrumentation.

Figure 3-53: Test 4b, relative humidity results upstream and downstream of the fire with FFFS using Nozzle A.

<!-- image -->

Line chart

Figure 3-54: Test 4b, measured FHRR varying over time with FFFS using Nozzle A.

<!-- image -->

Line chart

## 3.8 Water Spray Characteristics

The nozzle spray pattern 1000 mm below the nozzle was surveyed. CFD models were developed using FDS for Nozzle A and Nozzle B, and a genetic algorithm was used to estimate the spray pattern  parameters  that  could  best  match  the  tests  (see  [3]  for  more  details  of  the  method). Results  of  the  analysis  are  provided  in  Figure  3-55  and  Figure  3-56  for  Nozzle  A  and  B respectively. The spray pattern parameters are provided in Table 3-6. Note that the diameter was allowed  to  vary  slightly  around  the  measured  test  value  of  Dv0.5  in  the  genetic  algorithm optimization. The range of variation allowed was chosen to be very small relative to the range of diameters measured in the tests.

For Nozzle C, a water mist nozzle, there was more than one water spray jet. This meant that the nozzle spray pattern was not really correlated to the conical patterns used in the genetic algorithm for Nozzles A and B. Thus, these spray parameters were not determined for Nozzle C.

Table 3-5: Nozzle parameter measurements.

| PARAMETER                  |   NOZZLE A |   NOZZLE B |   NOZZLE C |
|----------------------------|------------|------------|------------|
| Pressure (bar)             |        1.5 |          3 |         90 |
| Flow (L/min)               |       49.9 |        4.9 |        4.6 |
| K factor (L/(min bar 0.5 ) |      40.74 |       2.83 |       0.48 |
| Distance below nozzle (mm) |       1000 |       1000 |       1000 |
| Droplet count              |       2912 |      19370 |     282300 |
| D10 (µm)                   |      357.9 |      101.7 |       38.4 |
| D20 (µm)                   |      513.5 |      127.3 |       52.9 |
| D30 (µm)                   |      636.6 |      154.1 |       67.4 |
| D32 (µm)                   |      978.6 |      225.9 |      109.4 |
| Dv0.1 (µm)                 |      606.6 |      134.6 |       66.8 |
| Dv0.5 (µm)                 |     1117.4 |      279.5 |        131 |
| Dv0.9 (µm)                 |     1755.9 |      507.3 |      211.1 |
| Dv0.98 (µm)                |     2075.2 |      590.1 |      275.3 |
| Vz (m/s)                   |       1.65 |       2.32 |        2.4 |
| Vr (m/s)                   |       1.48 |          0 |        1.2 |

Figure 3-55: Spray pattern and FDS results for Nozzle A (EVS-10-52).

<!-- image -->

Line chart

Figure 3-56: Spray pattern and FDS results for Nozzle B (EVS-10-51).

<!-- image -->

Line chart

Table 3-6: Spray patterns and FDS parameters based on tests and analysis.

| PARAMETER                          | NOZZLE A RANGE FOR GENETIC ALGORITHM INPUT   | NOZZLE A RESULTS FROM GENETIC ALGORITHM   | NOZZLE B RANGE FOR GENETIC ALGORITHM INPUT   | NOZZLE B RESULTS FROM GENETIC ALGORITHM   |
|------------------------------------|----------------------------------------------|-------------------------------------------|----------------------------------------------|-------------------------------------------|
| Particle velocity (m/s)            | 1 to 45                                      | 27.0                                      | 1 to 45                                      | 13.8                                      |
| Spray angle (inner angle, degrees) | 0 to 45                                      | 45                                        | 0 to 45                                      | 2.3                                       |
| Spray angle (outer angle, degrees) | 46 to 90                                     | 90                                        | 46 to 90                                     | 75                                        |
| Particle diameter Dv,0.5 (μm)      | 1110 to 1130                                 | 1130                                      | 280 to 290                                   | 284.5                                     |
| Droplet offset (mm)                | N/A                                          | 0                                         | N/A                                          | 0                                         |
| Nozzle flow rate (LPM)             | N/A                                          | 49.9                                      | N/A                                          | 4.9                                       |
| Particles per second               | N/A                                          | 5000                                      | N/A                                          | 5000                                      |
| Age (s)                            | N/A                                          | 30                                        | N/A                                          | 30                                        |
| Reference                          | N/A                                          | EVS-10-52                                 | N/A                                          | EVS-10-51                                 |

## 4.1 FDS Model Setup

The FDS models were developed to replicate the environment of the scaled model test tunnel as closely as possible. The FDS version used for all the cases herein was 6.7.7 (nightly release FDS6.7.7-1095-g41174cbf6-nightly), unless stated otherwise.  The goal was to test the second research hypothesis that CFD (herein, FDS) can be used to predict FFFS and EVS interaction for design integration. Table 4-1 provides the main FDS parameters used in computer modeling.

Table 4-1: FDS parameters used in the computer modeling.

| ITEM                            | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Geometry                        | Tunnel 2.5 m by 1.25 m, length of 12.0 m. The grade of the models is 0 percent to match the test configuration.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Grid resolution - base case     | FDS models were developed with the same number of cells in each test case with grid refinement in Y and Z directions near the walls. Base case grid resolution was 0.1 m along the tunnel length and width, and 0.125 m along the tunnel height. Grid refinement was applied across the width (Y) direction as follows (0 m is the tunnel centerline): -1.25 m to -1.15 m, 4 cells, 0.025 m resolution -1.15 m to -1.05 m, 2 cells, 0.05 m resolution -1.05 m to +1.05 m, 21 cells, 0.1 m resolution +1.05 m to +1.15 m, 2 cells, 0.05 m resolution +1.15 m to +1.25 m, 4 cells, 0.025 m resolution Grid refinement was applied across the width (Z) direction as follows: 0 m to 0.125 m, 4 cells, 0.03125 m resolution 0.125 m to 0.25 m, 2 cells, 0.0625 m resolution 0.25 m to 1.00 m, 6 cells, 0.125 m resolution +1.00 m to +1.125 m, 2 cells, 0.0625 m resolution +1.125 m to +1.25 m, 4 cells, 0.03125 m resolution With the near-wall grid refinement, this results in 120 cells along the tunnel length, 33 cells along the tunnel width, and 18 cells along with the tunnel height. Models herein used this grid resolution unless otherwise stated. |
| Grid sensitivity - fine grid    | For the fine grid cases, FDS models were developed with the same number of cells in each test case with grid refinement in Y and Z directions near the walls. Grid resolution was 0.05 m along the tunnel length and width, and 0.0625 m in the vertical direction. With near-wall grid refinement, this results in 240 cells along the tunnel length, 66 cells along the tunnel width, and 36 cells along the tunnel height.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Grid sensitivity - uniform grid | Coarse grid resolution was 0.1 m along the tunnel and 0.125 m along the tunnel width and height. This resulted in 120 cells along the tunnel length, 25 cells along the tunnel width, and 10 cells along the tunnel height. Near-wall grid refinement was not applied. Fine grid resolution was halved relative to the coarse grid.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Fire heat release rate          | The models were based on a priori specified heat release rate per unit area for the fire with no fire suppression modeled, only cooling of combustion products. That is, the FHRR was a boundary condition to the model and not a result of the model computations.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Fire pool and shield            | Fire surface 0.25 m above the tunnel floor with default FDS heptane fire parameters. Shield height of 0.625 m above the tunnel floor. The shield was placed starting at the 5.0 m marker. The fuel was modeled in FDS as heptane to match the test conditions most closely. Diesel fuel did not have an easily applicable chemical formula, so the fuel was kept as heptane.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## 4 FDS MODELS

Figure 4-1 shows the FDS model geometry used for all the tests. Figure 4-2 and Figure 4-3 show the FFFS setup for Test 4b and Test 5b.

| ITEM                                   | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Inlet velocity                         | Inlet velocities vary per test case. Inlet vents (25 individual vents) were created at the tunnel inlet like the grid point setup. The total flow rate was correlated to match the measurement at the V015c probe for each test using the equation in Figure 3-2 and a weight factor of 0.698.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| FFFS parameters                        | FFFS was set up using nozzle parameters in Table 2-2. Following FDS inputs were used for the nozzles based on nozzle characterization, for Nozzle A: PARTICLE_VELOCITY = 27.0, SPRAY_ANGLE = 45.0,90.0, PARTICLES_PER_SECOND = 5000, SPRAY_PATTERN_SHAPE = 'UNIFORM', OFFSET = 0.00 For Nozzle B: PARTICLE_VELOCITY = 13.8, SPRAY_ANGLE = 2.3,75, PARTICLES_PER_SECOND = 5000, OFFSET = 0.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Wall boundary conditions               | The test tunnel had a wall boundary condition corresponding to the aquapanels used in the scaled tunnel, with a thickness of 1 cm and the backing exposed to ambient air. Material properties for the wall were as follows: Density = 750 kg/m 3 Heat capacity = 0.84 kJ/kg/K Conductivity = 0.16945 W/m/K Emissivity = 0.9                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| FDS model parameters                   | Settings for the pressure solver were adjusted to have a pressure tolerance of 100, maximum pressure iterations of 200, and the tunnel preconditioner setting was set to true. Other model parameters were as per FDS defaults.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Comparison based on linear correlation | Results are compared between test data and the FDS model using a Pearson correlation coefficient (r) (see Figure 4-4) to measure how well the data are agreeing based on a linear correlation. For purposes of using classifications in a consistent manner herein, the strength of association between test data and FDS is taken to be poor (r value between 0.0 and 0.25), fair (r value between 0.25 and 0.5), good (r value between 0.5 and 0.75), or very good (r value between 0.75 and 1.0). This terminology was used in the Computer Modeling Report. Negative r values represent a situation where the linear correlation between variables trends toward the straight-line interpretations having opposite slopes. Note that there is no standard that states how to assign interpretation to correlation coefficients [10]. The Pearson correlation cannot be used to say that the test and FDS agree within a certain percentage. Agreement between the test and FDS and test can also be judged qualitatively, based on whether the FDS is showing similar trends to the test (refer below). |

Figure 4-1: FDS model setup (dimensions in m).

<!-- image -->

Engineering drawing

Figure 4-2: FDS model setup showing Test 4b setup with Nozzle A.

<!-- image -->

Engineering drawing

Figure 4-3: FDS model setup showing Test 5b setup with Nozzle B.

<!-- image -->

Engineering drawing

Figure 4-4: Equation. Pearson correlation coefficient.

<!-- image -->

Engineering drawing

In Figure 4-4 symbols are as follows: r is the Pearson correlation coefficient, xi is the x values in a sample, x ̅ is the mean of the x values in a sample, yi is the y values in a sample, and y ̅ is the mean of the y values in a sample.

The FHRR profile used in the models (for Test 5b and Test 4b) is provided in Figure 4-5 and Figure 4-6. The plots are smoothed from raw data for presentation (raw data FHRR every 1 s was used in the models). Sensitivity to this was tested but found to not be significant.

Figure 4-5: FHRR profile for Test 5B FDS models.

<!-- image -->

Line chart

Figure 4-6: FHRR profile for Test 4B FDS models.

<!-- image -->

Line chart

## 4.2 FDS Results - Nozzle B

The temperature result for Test 5b is compared with the test result just upstream of the fire at the point near to the tunnel ceiling in Figure 4-7. Velocity result for Test 5b is compared with the test result  just  upstream  of  the  fire  in  Figure  4-8.  Agreement  between  results  is  very  good  for temperature and velocity (per the Pearson coefficient values).

Figure 4-7: Test 5b, FDS temperature results just upstream of the fire.

<!-- image -->

Line chart

Figure 4-8: Test 5b, FDS velocity results just upstream of the fire.

<!-- image -->

Line chart

The temperature result for Test 5b just downstream of the fire near the tunnel ceiling is compared with the test result in Figure 4-9. The velocity result for Test 5b is compared with the test result just downstream of the fire in Figure 4-10. Comparison between the test and FDS is very good for temperature (as per the Pearson coefficient) and good for velocity.

Figure 4-9: Test 5b, FDS temperature result just downstream of the fire.

<!-- image -->

Line chart

Figure 4-10: Test 5b, FDS velocity result just downstream of the fire.

<!-- image -->

Line chart

Gas temperature near the ceiling results for Test 5b at 400 and 480 seconds are compared with the test results in Figure 4-11 and Figure 4-12. Fire location is marked at 0 m, shown with a vertical line. Agreement between test and FDS is very good, per the Pearson coefficient, before FFFS was operated and good after FFFS was operated.

Figure 4-11: Test 5b, FDS results showing gas temperature near the ceiling averaged from 400 to 410seconds.

<!-- image -->

Line chart

Figure 4-12: Test 5b, FDS results showing gas temperature near the ceiling averaged from 470 to 480 seconds.

<!-- image -->

Line chart

Figure 4-13 provides a temperature isotherm near the tunnel ceiling as a measure of backlayering. The result shows that the FDS model does not give a similar trend to the test at the base grid resolution. This is evident from Figure 4-11 where temperatures upstream of the fire recorded using FDS are not high compared to the measured test data.

Figure 4-13: Test 5b, FDS results showing isotherm of temperature (40 degrees Celsius) upstream of fire.

<!-- image -->

Line chart

The  sensitivity  of  FDS  results  (backlayering  primarily)  was  tested  using  various  sensitivity parameters shown in Table 4-2. Sensitivity to different turbulence models in FDS, radiative heat fraction,  and  temperature measurement location was found to be relatively low. Results were shown to be more sensitive to the grid resolution of the FDS model, inlet velocity and FHRR. Sensitivity to these parameters is explored in more detail in the sections below.

Table 4-2: Sensitivity parameters tested in the FDS models.

| PARAMETER                        | DESCRIPTION                                                                                                               | SENSITIVITY   |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------|---------------|
| Turbulence model                 | Tested Deardorff (default) and other available turbulent viscosity models in FDS.                                         | Low           |
| Radiative heat fraction          | Varied from 0.1 to 0.33.                                                                                                  | Low           |
| Temperature measurement location | Varied the vertical location of the temperature sensors upstream of the fire from 1 to 5 cm away from the tunnel ceiling. | Low           |
| Grid resolution                  | Simulations run using both coarse and fine grid resolutions.                                                              | High          |
| Inlet velocity                   | Varied the weight factor that effects the inlet velocity magnitudes.                                                      | High          |
| Fire heat release rate           | Varied the fire heat release rate based on the possible uncertainty.                                                      | High          |

## 4.2.1 Grid Resolution Sensitivity

Grid resolution sensitivity considered included the cases outlined in Table 4-3. Cases I and II considered near-wall refinement whereas Cases III and IV had a uniform grid without near-wall refinement. Ceiling temperature results are compared since this tracks the critical/confinement velocity most closely and this was the key parameter of interest. Results for Test 5b at 400 and 480 seconds are compared (10 s time average from 400 to 410 s, and from 470 to 480 s). Refer to Figure 4-14 for Case I results, Figure 4-15 for Case II results, Figure 4-16 for Case III results, and Figure 4-17 for Case IV results. In these figures the fire location is marked at 0 m, shown with a vertical line and upstream of the fire is represented by coordinates less than 0 m.

Table 4-3: Grid resolution sensitivity cases for Test 5b.

| CASE   | NEAR-WALL REFINEMENT   | DESCRIPTION                                                                                                                                      | RUN ID   |
|--------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| I      | Yes                    | Base case with 0.1 m grid resolution in X, Y and Z directions with near-wall refinement, refer to Table 4-1.                                     | EVS-28-5 |
| II     | Yes                    | Fine grid with 0.05 m grid resolution in X, Y, and 0.0625 m in Z direction with near-wall refinement similar to Case I, but half the mesh sizes. | EVS-28-7 |
| III    | No                     | Uniform coarse grid with 0.1 m grid resolution in X, Y and 0.125 m in Z direction.                                                               | EVS-28-3 |
| IV     | No                     | Uniform fine grid with 0.05 m grid resolution in X, Y and 0.0625 m in Z direction.                                                               | EVS-28-4 |

Figure 4-14: Test 5b, Case I (base case grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds).

<!-- image -->

Line chart

Figure 4-15:Test 5b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds).

<!-- image -->

Line chart

Figure 4-16: Test 5b, Case III (uniform coarse grid) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds).

<!-- image -->

Line chart

Figure 4-17: Test 5b, Case IV (uniform fine grid) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 400 to 410 seconds and 470 to 480 seconds).

<!-- image -->

Line chart

The  results  reflect  that  using  a  refined  near-wall  grid  resolution  is  important  for  predicting backlayering. All cases of grid resolution do a reasonable job of predicting the temperature field trends on the downstream side of the fire (FDS results over predict temperature relative to tests), but the increase in temperature upstream of the fire is seen only when the grid is refined at the walls. This is evident from Figure 4-14 and Figure 4-17 where the coarser gird resolution with near-wall refinement (Case I) yielded better upstream temperature results than the uniform fine grid resolution (Case IV) due to having smaller mesh size near the walls. Thus, even though the fine grid is overall of higher resolution, it is the near-wall resolution that also needs to be refined here. Case II results in Figure 4-15 depicts this. The result shows that predicting backlayering is sensitive to the near-wall grid resolution with the coarse grid predicting less backlayering.

## 4.2.2 Inlet Velocity Sensitivity

The sensitivity to inlet bulk velocity was tested, within the range per the computations described in Section 3.1. Ceiling temperature results for Test 5b at 400 and 480 seconds using the inlet velocity weight factor of 0.698 are reprinted in Figure 4-18. Results can be compared with the inlet velocity weight factor of 0.80 in Figure 4-19.

Increasing the weight factor from 0.698 to 0.80 results in higher inlet velocities which in turn results in  less  backlayering  predicted.  This  is  evident  in  the  results  both  before  and  after  FFFS  was operated  at  420  seconds.  Temperature  downstream  were  less  sensitive  to  the  velocity  from upstream. The change in upstream velocity and sensitivity of backlayering (less backlayering with increased  upstream  velocity)  is  expected,  but  of  significance  is  how  a  small  change  in  the upstream  velocity  (within  the  range  of  test  data  uncertainty)  causes  the  result  to  change appreciably in the upstream region.

Figure 4-18: Test 5b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.698.

<!-- image -->

Line chart

Figure 4-19: Test 5b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.80.

<!-- image -->

Line chart

## 4.2.3 Heat Release Rate Sensitivity

The oxygen consumption method was used to obtain the FHRR for Test 5b. The mass loss rate of the fire load could not be used to derive the FHRR for this test as the scale underneath the fire pool  was  concluded to  be  damaged  during this  test  series  (refer  Section  3.3).  As  outlined  in Section  2.2,  the  combustion  product  gas  composition  measurements  were  taken  for  oxygen, carbon monoxide and carbon dioxide concentration at the P115 location. This method is known to give better results for larger FHRRs. For smaller FHRRs the result has larger uncertainty. These uncertainties  result  mostly  from  the  velocity  measurements  (relative  error  increases  for  lower velocities) and the oxygen measurements since measurements were taken at only one position. FHRR results  using  this  method  are  assumed  to  have  plus  or  minus  20  percent  uncertainty associated with them (based on previous experience).

Sensitivity cases were run with 20 percent increase and decrease in the FHRR values for Test 5b to see what the FDS could predict when the uncertainty is accounted for. Figure 4-20 shows the gas temperature near the ceiling results for Case I. Figure 4-21 shows the FDS results for the same Case I but with 20 percent increase in the FHRR. Figure 4-22 (base case) and Figure 4-23 (20 percent increases in FHRR) show the same results but for Case II.

The results indicate, for this test series, that backlayering predicted using FDS is not as sensitive to the FHRR profile as it is to the near-wall grid resolution, with backlayering prediction improving when the grid is finer and refined near the walls.

Figure 4-20: Test 5b, Case I (coarse grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds).

<!-- image -->

Line chart

Figure 4-21: Test 5b, Case I (coarse grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds).

<!-- image -->

Line chart

Figure 4-22: Test 5b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds).

<!-- image -->

Line chart

Figure 4-23: Test 5b, Case II (fine grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (400 seconds and 480 seconds).

<!-- image -->

Line chart

## 4.3 FDS Results - Nozzle A

The temperature result for Test 4b is compared with the test result just upstream of the fire at a point near the tunnel ceiling in Figure 4-24. The velocity result for Test 4b is compared with the test  result  just  upstream  of  the  fire  in  Figure  4-25.  Agreement  between  results  is  poor  for temperature and very good for velocity per the Pearson coefficient values. Velocity results start deviating from the test data after the FFFS start time. At the location upstream of the fire some backlayering was seen in the tests, and less so in the FDS, which is reflected in the results here. The temperature profile suggests better agreement between the FDS model and the test than the Pearson coefficient suggests.

Figure 4-24: Test 4b, FDS temperature results just upstream of the fire.

<!-- image -->

Line chart

Figure 4-25: Test 4b, FDS velocity results just upstream of the fire.

<!-- image -->

Line chart

The temperature result for Test 4b downstream of the fire near the tunnel ceiling is compared with the test result  in  Figure  4-26.  The  velocity  result  for  Test  4b  is  compared  with  the  test  result downstream of the fire in Figure 4-27. Comparison between the test and FDS is very good for temperature per the Pearson  coefficient, with FDS  predicting slightly higher velocities. Comparison between the test and FDS is fair for velocity as per the Pearson coefficient.

Figure 4-26: Test 4b, FDS temperature result just downstream of the fire.

<!-- image -->

Line chart

Figure 4-27: Test 4b, FDS velocity result just downstream of the fire.

<!-- image -->

Line chart

Gas  temperature  results  near  to  the  tunnel  ceiling  for  Test  4b  at  340  and  420  seconds  are compared with the test results in Figure 4-28 and Figure 4-29. The fire location is marked at 0 m, shown with a vertical line. Agreement between test and FDS is very good before and after the FFFS was operated per the Pearson coefficient. The results show that the FDS is not predicting backlayering before FFFS is operated.

Figure 4-28: Test 4b, FDS results showing gas temperature near the ceiling averaged from 340 to 350 seconds.

<!-- image -->

Line chart

Figure 4-29: Test 4b, FDS results showing gas temperature near the ceiling averaged from 410 to 420 seconds.

<!-- image -->

Line chart

Figure 4-30 provides a temperature isotherm near the tunnel ceiling as a measure of backlayering. The result shows that the FDS model does not give a similar trend to the test at the base grid resolution. This is evident from Figure 4-28 where temperatures upstream of the fire recorded using FDS are not high compared to the measured test data. Higher temperatures are observed later in the FDS model that are not present in the test data.

In summary, comparing the FDS results for Test 4b with the test results, the following conclusions are  made.  The  overall  agreement  (between  measurement  and  model)  for  temperature downstream of the fire is good. Velocity agreement downstream was poor, although prior to FFFS operation the agreement was better. The FDS model did not predict backlayering upstream of the fire very well before the FFFS was operated. Sensitivity of the results to the grid resolution of the FDS model, inlet velocity and FHRR is explored in the sections below.

Figure 4-30: Test 4b, FDS results showing isotherm of temperature (40 degrees Celsius) upstream of fire.

<!-- image -->

Line chart

## 4.3.1 Grid Resolution Sensitivity

Grid resolution sensitivity considered included the cases outlined in Table 4-2 but only the cases with near-wall refinement were considered (see Table 4-4). Figure 4-31 shows the results for Case I (base case) and Figure 4-32 shows the results for Case II.

Table 4-4: Grid sensitivity cases for Test 4b.

| CASE   | NEAR-WALL REFINEMENT   | DESCRIPTION                                                                                                                                 | RUN ID   |
|--------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------|
| I      | Yes                    | Coarse grid (base case). 0.1 m grid resolution in X, Y and Z directions with near-wall refinement, refer to Table 4-1.                      | EVS-28-1 |
| II     | Yes                    | Fine grid. 0.05 m grid resolution in X, Y and 0.0625 m in Z direction with near-wall refinement similar to Case I, but half the mesh sizes. | EVS-28-9 |

Figure 4-31: Test 4b, Case I (coarse grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

Figure 4-32: Test 4b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

The results on the finer grid show a very slight increase in the temperature upstream of the fire (refer to Figure 4-32) before FFFS is activated, which is a similar trend to observed in earlier analysis. FDS results after FFFS activation show almost no difference upstream of the fire. A slightly higher temperature is predicted downstream after FFFS activation.

## 4.3.2 Inlet Velocity Sensitivity

The sensitivity to the inlet velocity was investigated for Test 4b. Ceiling temperature results for Test 4b at 340 and 420 seconds using the inlet velocity weight factor of 0.698 are reprinted in Figure 4-33. Results can be compared with the inlet velocity weight factor of 0.80 in Figure 4-34.

Figure 4-33: Test 4b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.698.

<!-- image -->

Line chart

Figure 4-34: Test 4b, gas temperature near the ceiling, results before and after FFFS was operated with the inlet velocity weight factor of 0.80.

<!-- image -->

Line chart

Increasing the weight factor from 0.698 to 0.80 results in higher inlet velocities but sensitivity of the backlayering to the adjusted inlet velocity was almost negligible for these models. This is likely due to the model predicting almost no backlayering at the lowest inlet velocity. The downstream temperatures do not change appreciably with increased upstream velocity.

## 4.3.3 Heat Release Rate Sensitivity

The oxygen consumption method was used to obtain the FHRR for Test 4b. As mentioned in Section  4.2.3,  for  smaller  FHRRs  the  results  have  larger  uncertainty  associated  with  them. Therefore,  FHRR  results  using  this  method  are  concluded  to  have  plus  or  minus  20  percent uncertainty. For this purpose, sensitivity case were run with 20 percent increase in the FHRR values for Test 4b to see what the FDS could predict when the uncertainty is accounted for. Figure 4-35 shows the gas temperature near the ceiling results for Case I (base case, refer to Table 4-4). Figure 4-36 shows the FDS results for the same Case I but with 20 percent increase in the FHRR. Figure 4-38 shows the results for Case II (fine grid resolution with near-wall refinement) with 20 percent increase in the FHRR.

Figure 4-35: Test 4b, Case I (coarse grid with near-wall refinement) results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

Figure 4-36: Test 4b, Case I (coarse grid with near-wall refinement) results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

Figure 4-37: Test 4b, Case II (fine grid with near-wall refinement) FDS results showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

Figure 4-38: Test 4b, Case II (fine grid with near-wall refinement) FDS results with 20 percent increase in FHRR showing gas temperature near the ceiling before and after FFFS activation (averaged from 340 to 350 seconds and 410 to 420 seconds).

<!-- image -->

Line chart

The  results  show  that  backlayering  predicted  using  FDS  is  sensitive  to  the  FHRR  and  grid resolution. Accounting for the uncertainty in FHRR (larger FHRR by 20 percent) yielded upstream temperature results that match the test data better but generally only in a noticeable way if the finer grid was used.

## 4.4 Summary of Results

Refer to Table 4-5 for a summary of the analysis and results.

Table 4-5: Summary of the FDS results.

| TEST ID           | RUN ID    | GRID                                   | INLET VELOCITY   | FHRR      | REMARKS ON BACKLAYERING PREDICTION VIA TEMPERATURE NEAR THE TUNNEL CEILING                                                                      |
|-------------------|-----------|----------------------------------------|------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| IFAB-15 (Test 5b) | EVS- 28-5 | Coarse grid with near- wall refinement | No change        | No change | Base case for Test 5b, model did not predict backlayering to the same extent as observed in the tests. Downstream temperature was reasonable.   |
| IFAB-15 (Test 5b) | EVS- 28-7 | Fine grid with near- wall refinement   | No change        | No change | Increase in temperature upstream of the fire is observed both before and after FFFS activation, with improvement relative to the coarse grid.   |
| IFAB-15 (Test 5b) | EVS- 28-3 | Uniform coarse grid                    | No change        | No change | Lower temperature upstream of the fire before FFFS activation is observed from the FDS results, which indicates poorer backlayering prediction. |

| TEST ID           | RUN ID     | GRID                                   | INLET VELOCITY                                                | FHRR                | REMARKS ON BACKLAYERING PREDICTION VIA TEMPERATURE NEAR THE TUNNEL CEILING                                                                                                              |
|-------------------|------------|----------------------------------------|---------------------------------------------------------------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IFAB-15 (Test 5b) | EVS- 28-4  | Uniform fine grid                      | No change                                                     | No change           | Some minor improvement in the temperature results upstream of the fire before FFFS activation although still not as good as cases with refined near-wall grids.                         |
| IFAB-15 (Test 5b) | EVS- 28-6  | Coarse grid with near- wall refinement | Weight factor increased to 0.8 resulting in higher velocities | No change           | Results show reduction in temperature upstream and downstream of the fire before FFFS activation, indicating reduced backlayering is predicted when compared to the base case EVS-28-5. |
| IFAB-15 (Test 5b) | EVS- 28-13 | Coarse grid with near- wall refinement | No change                                                     | 20 percent increase | Results show increased temperature upstream of the fire both before and after FFFS activation.                                                                                          |
| IFAB-15 (Test 5b) | EVS- 28-17 | Fine grid with near- wall refinement   | No change                                                     | 20 percent increase | Similar results to previous coarse grid case with temperatures showing better agreement with test but extra FHRR causes higher temperature downstream.                                  |
| IFAB-19 (Test 4b) | EVS- 28-1  | Coarse grid with near- wall refinement | No change                                                     | No change           | Base case for Test 4b, results do not indicate that backlayering upstream of the fire is predicted.                                                                                     |
| IFAB-19 (Test 4b) | EVS- 28-9  | Fine grid with near- wall refinement   | No change                                                     | No change           | No appreciable improvement of backlayering prediction relative to the base case.                                                                                                        |
| IFAB-19 (Test 4b) | EVS- 28-2  | Coarse grid with near- wall refinement | Weight factor increased to 0.8 resulting in higher velocities | No Change           | No appreciable backlayering change, which was expected given that lower upstream velocity cases did not show any backlayering.                                                          |
| IFAB-19 (Test 4b) | EVS- 28-11 | Coarse grid with near- wall refinement | No change                                                     | 20 percent increase | Results show a small increase in the temperature result upstream of the fire before FFFS activation, indicating that potentially more backlayering is predicted.                        |
| IFAB-19 (Test 4b) | EVS- 28-16 | Fine grid with near- wall refinement   | No change                                                     | 20 percent increase | Results before FFFS activation matches very well with the test data, thus indicating a good backlayering prediction relative to test data.                                              |

## 5 DISCUSSION AND CONCLUDING REMARKS

## 5.1 Research Hypotheses

Laboratory tests were performed to better understand the interaction between longitudinal EVS and the FFFS. The tests were principally structured toward verifying the change in critical/confinement velocity with FFFS operating and providing data for FDS model validation. The following parameters were measured and recorded during all tests:

- The gas temperature near to the ceiling at varying longitudinal locations.
- Air velocity and temperature on the tunnel centerline at vertical stations placed upstream and downstream of the fire.
- Adiabatic surface temperature.
- Fire heat release rate (FHRR) via mass loss rate of the fire load.
- FHRR from combustion product gas composition measurements, with a cross-check of the FHRR calculation against mass loss rate measurements.
- Water pressure in the FFFS (and thus the water flow rate).
- Near-wall static pressure at selected locations along the tunnel.
- Relative air humidity upstream and downstream of the fire.
- Visual recording.

The hypotheses for this  work  were  looking  at  the  integration  of  the  FFFS  and  EVS,  and  the accuracy  of  modeling  the  system's  performance  using  FDS.  The  principal  hypotheses  being investigated are described below.

## 5.1.1  Hypothesis 1 - FFFS and EVS Integration

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized because of  the  cooling  effects  of  the  FFFS  water  spray.  This  hypothesis  is  partially  accepted.  Further discussion is provided below regarding this hypothesis. The statistical significance of acceptance of this hypothesis acceptance is not provided because many factors feed into FFFS and EVS integration, and the hypothesis and tests were not designed to come down to one quantifiable input or output.

Results from the tests demonstrate qualitatively that the EVS capacity can be reduced, as the confinement velocity decreases due to the cooling of the FFFS water spray. Refer to Section 3.3 and Section 3.4 for an investigation of cooling, confinement velocity and smoke control with and without FFFS operating. The results show that when the fan setting to control upstream velocity is  held  constant  and  backlayering  occurs,  that  the  backlayering  is  stopped  (or  backlayering distance reduced) once the FFFS is operated (even though the upstream velocity was observed to reduce slightly (for two of the three tests reported), see Section 3.6). This indicates a reduction in the longitudinal velocity needed to control the smoke spread upstream because of the cooling of  combustion  products.  Smoke  control  (measured  by  the  temperature  at  the  ceiling)  was improved when the FFFS was operated due to its cooling effect. Backlayering was controlled in all fire tests after FFFS was activated.

The following additional points are noted in relation to the first hypothesis:

- Effectiveness of the longitudinal velocity was improved when the FFFS was operated. Refer to Section 3.4.
- Optimization of the EVS because of cooling effects of the FFFS was not investigated in the tests.  The  focus  was  whether  EVS  capacity  can  be  reduced  due  to  FFFS  integration, something that the results show is feasible due to the improved smoke management with FFFS operating. Optimization of the EVS with FFFS use is a subject better applied to a specific design which can be investigated through computer modeling.
- Results from the tests are not able to be used to quantify the extent of critical/confinement velocity reduction when FFFS is operated. This is due to the transient FHRR and difficulty accurately controlling the upstream air speed at velocities encountered in the tests. Refer to Section 5.4 for discussion of suggested topics for further research.
- Temperatures were reduced with smaller water droplets. Figure 3-35 shows temperature with Nozzle  A  (1117 µm  droplet  diameter)  at  60  s  after  FFFS  operation,  with  a  downstream temperature of approximately 225 °C, FHRR approximately 1.25 MW per Figure 3-26. Figure 3-36  shows  temperature  with  Nozzle  B  (280 µm  droplet  diameter)  at  60  s  after  FFFS operation,  with  a  downstream  temperature  of  approximately  160 °C,  FHRR  approximately 1.1 MW per Figure 3-27). Figure 3-37 shows temperature with Nozzle C (131 µm droplet) at 60 s after FFFS operation, with a downstream temperature of approximately 80 °C, FHRR approximately 1.1 MW per Figure 3-28.
- The magnitude of pressure changes measured was too small to allow for a quantification of resistance effects due to FFFS. For design purposes, it is suggested that the FFFS resistance be  considered  in  the  EVS  design  since  this  effect  is  relatively  easy  to  estimate  (see  for instance reference [11]). Pressure measurements were also noted to be of low reliability since pressure was recorded at one point in the cross section and if the flow was varying over the cross section, then pressure could have also been expected to vary somewhat. The results reported for pressure show small/negligible pressure changes due to the operation of FFFS. Additionally,  the  static  pressure  did  not  vary  significantly  when  FFFS  was  operated  with different water droplet sizes. Refer to Section 3.2 and Section 3.6 for an investigation of the pressure changes with and without FFFS.
- The magnitude of some adiabatic surface temperature measurements is questionable and there may have been a problem with the instruments. Operation of FFFS was observed to reduce the adiabatic surface temperatures both at the tunnel ceiling and the wall. Refer to Section 3.5 for an investigation of the adiabatic surface temperatures measured during the different fire tests.
- Refer to Section 3.7 for an investigation of the measured relative humidity results. Relative humidity measurements in the tests were inconclusive. This may have been due to a fault with the sensor readings.

## 5.1.2 Hypothesis 2 - Use of FDS to Predict FFFS and EVS Interaction

The second hypothesis is that CFD (specifically here, FDS) can be used to predict FFFS and EVS interaction  for  design  integration.  This  hypothesis  is  partially  accepted.  Further  discussion  is provided  below  regarding  this  hypothesis.  The  statistical  significance  of  acceptance  of  this hypothesis acceptance is not provided because many factors feed into the FDS modeling, and the hypothesis and tests were not designed to come down to one quantifiable input or output.

- The FDS results and test data (gas temperatures at the tunnel ceiling) showed qualitatively similar  results  downstream  of  the  fire,  and  in  some  cases,  there  was  good  quantitative agreement as well. The cooling effect of the water spray (seen in temperatures downstream of the fire) was usually in good agreement (FDS model versus test).
- Backlayering proved difficult to predict with FDS, but in cases where the model did predict backlayering, a subsequent reduction in backlayering distance was seen when the FFFS was operated.
- Confidence  in  test  results  for  adiabatic  surface  temperature,  relative  humidity  and  static pressure was not high enough to make meaningful comparisons with the FDS results. These parameters were, however, not critical from the tests for the overall question of FFFS and EVS integration. Static pressure changes are addressed in literature [11], and the question of humidity is discussed in Section 5.3 of the Literature Survey and Synthesis.

There were several uncertainties in the test data that proved to be important for this hypothesis, especially around the upstream velocity magnitude and FHRR. Considering that data from the tests did have uncertainty, results from the FDS analysis showed that interaction between the FFFS and EVS can be predicted (FFFS caused backlayering distance to decrease), but that results for backlayering prediction can be very sensitive to grid resolution and model boundary conditions.  To  predict  backlayering  observed  in  the  tests  with  FDS,  the  uncertainty  in  the upstream velocity had to use the lower range of velocity (for Test 5b and 4b), and the FHRR input had to use the upper range value (for Test 4b). The following additional detailed points are noted from the FDS results in relation to the second hypothesis:

- For one test (5b, refer Section 4.2.1) the effect of the FFFS on smoke control was predicted. Backlayering was observed prior to FFFS operation and confinement/critical velocity reduction with FFFS operating was observed (with a fine near-wall grid and lower range of upstream velocity, refer Figure 4-15). Gas temperature profiles along the tunnel ceiling showed FDS predicted a higher temperature downstream of the fire prior to FFFS operation (by around 25 to 30 percent), and after FFFS operation the temperature results were in closer agreement. Sensitivity  to  near-wall  grid  resolution  was  noted,  with  the  finer  grid  needed  to  predict backlayering as seen in the test.
- For another test (4b, refer Section 4.3.1) the backlayering seen in the test prior to operation of the FFFS was not able to be predicted with FDS, except for tests where the grid was finer and the FHRR was increased by 20 percent, and where the lower range of upstream velocity was used (refer Figure 4-38). The FHRR increase was estimated based on prior experience with  uncertainty  in  the  measurements  used  to  compute  FHRR  via  oxygen  consumption calorimetry. Gas temperature profiles along the tunnel ceiling downstream of the fire were in good agreement with the finer grid performing best for backlayering (see Figure 4-36 and Figure 4-38 for coarse and fine grid respectively).

The  process  of  droplet  profile  development  (diameter,  spray  patterns)  and  subsequent  CFD model parameter determination (using FDS) was successfully demonstrated, refer to Section 3.8.

## 5.2 Discussion

The fire configuration in the tests utilized a shield to limit the impact of the water spray on the FHRR. The reason the shield was included was to avoid significant fire suppression/extinguishment  because  of  the  FFFS  operation,  and  thus  isolate  the  interaction between the ventilation and the FFFS. The shielded configuration affected the fire plume as it could not reach the tunnel ceiling unobstructed. Previous fire tests, such as the Memorial Tunnel fire  test,  did  not  utilize  a  shield  because  there  was  no  FFFS  present.  Thus,  the  fire  plume dynamics in the tests herein was different to the Memorial Tunnel tests (which also examined the longitudinal ventilation under fire and were used to test critical velocity equations). Equations for critical velocity typically have assumed a pool fire where the pool is placed on the floor of the tunnel. When comparing results herein with critical velocity equations, it is important to keep this physical difference in mind.

## 5.3 Suggested Practices Based on Research Findings

The following points are noted in relation to suggested practices based on the results herein:

- For the FDS models of the tests investigated herein, grid refinement near the tunnel walls was found to be important for predicting backlayering. Sensitivity to near-wall grid resolution is recommended to be considered when using FDS models to investigate longitudinal smoke control.  In  the  Computer  Modeling  Report  [3]  the  suggested  practices  section  noted  that coarse grids can give a reasonable prediction of the tunnel environment (remote from the immediate fire and backlayering regions) under longitudinal ventilation but a finer grid was needed to predict the backlayering distance (i.e., coarse grids showed less backlayering and finer grid results in FDS tended to show more backlayering, even relative to the test data, that is, FDS was tending to over predict backlayering). The results herein support that result; on a coarse grid the thermal environment downstream (and remote from the immediate fire) was predicted to a fair to good accuracy, but a finer grid was needed to predict the backlayering.
- Sensitivity  of  backlayering  to  FHRR  and  upstream  velocity  was  also  observed  with  an increased FHRR, and decreased velocity needed to see backlayering. This result, coupled with grid refinement sensitivity, suggests that backlayering prediction can be quite sensitive to the model boundary conditions.
- The test results  reaffirmed  that  smaller  water  drop  sizes  provide  increased  cooling  of  the tunnel environment for less overall water application rate. In terms of suggested practices, it is recommended to consider utilizing smaller water droplets if water supply is limited or optimal cooling efficiency is a key goal of the FFFS design.

## 5.4 Suggested Topics for Future Research

Suggested  further  research  based  on  findings  of  this  work  and  lessons  learned  from  testing includes the following:

- Revisit the design of the testing hypotheses and, where practicable, design quantitative tests for each hypothesis.
- Revisit  the  measurements  of  the  adiabatic  surface  temperature  and  relative  humidity. Determine if results seen herein have a physical explanation or were due to instrumentation faults  or  just  general  uncertainty  with  the  measurements  relative  to  the  magnitude  of measurements being made. For relative humidity, consider if the mass fraction of water vapor

can be measured instead of humidity. Mass fraction of water is less susceptible to temperature change than relative humidity.

- Revisit pressure measurements. Explore positioning probes over the tunnel cross section, or using multiple static pressure taps, to better account for developing flow, consider expected magnitude of pressure loss and whether the sensor can detect the changes expected, and explore  whether  a  longer  domain  can  be  developed  to  have  a  more  fully  developed  flow profile.
- Point  velocity  measurements  were  difficult  to  record  accurately  at  lower  air  speeds.  It  is suggested to explore whether an alternative measurement technique could be used. This might include, for instance, use of hot-wire probes. Laser Doppler techniques are probably not be feasible in this situation due to the need to seed the flow with particles.
- Additional tests are suggested to provide a quantification of the confinement/critical velocity. In the tests reported herein the FHRR was transient and there was uncertainty in the upstream air speed, and both these points meant it was not possible to determine quantitatively what the critical  velocity  was.  Future  testing  could  be  designed  to  address  these  points.  A  gas burner could be considered for the fire to achieve better FHRR control. The tunnel ventilation system could be designed in a manner that enables more accurate bulk velocity determination and  control  at  low  air  speeds  through  consideration  of  fan  selection  in  relation  to  fan performance characteristics. Real time measurement of FHRR and upstream (bulk) velocity, as well as back-up sensors for at least these two quantities, are suggested.
- Full-scale  testing  of  the  configurations  tested  herein  is  of  interest.  Specifically,  a  test conducted at a larger FHRR, more consistent with the magnitude likely to be encountered in practice. Planning for full-scale testing should carefully consider the findings as well as the suggested changes in previous points based on lessons learned from this work. Full-scale work may also be potentially more affected by certain factors such as wind conditions and planning should carefully consider this, and other possible influences.
- Development of equations following the physics of backlayering that approximate the known data.
- Further testing of CFD models, including FDS and other CFD software. Analysis with other CFD models is suggested as it could prove helpful to expand the range of physical models tested,  especially  in  relation  to  turbulence  models  (i.e.,  Reynolds-averaged  turbulence models), near-wall effects and geometry resolution (where curved surfaces are involved).

## REFERENCES

- [1] FHWA, 'Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Literature Survey and Synthesis.' Federal Highway Administration, FHWA-HIF-20-016, 2020.
- [2] FHWA, 'Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Workshop Report.' Federal Highway Administration, FHWA-HIF-20-060, 2020.
- [3] FHWA, 'Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Computer Modeling Report.' Federal Highway Administration, FHWA-HIF-22-021, 2022.
- [4] 'Institute for Applied Fire Safety Research (IFAB) - Accreditation,' IFAB . https://ifabfire.eu/institute/accreditation/ (accessed Sep. 04, 2022).
- [5] 'NFPA 502 Standard for Road Tunnels, Bridges and Other Limited Access Highways 2017.' NFPA, 2017.
- [6] 'ASHRAE Standard Methods for Velocity and Airflow Measurement, BSR/ASHRAE Standard 41.2P.' ASHRAE, 2022.
- [7] M. R. Ahemad, 'Estimation of Volumetric Flow Rate Through a Circular Duct: Equal Area Versus Log-Tchebycheff Method,' University of Windsor, Ottawa, 2006.
- [8] M. McPherson, Subsurface Ventilation Engineering . Springer-Science + Business Media, 1993.
- [9] M. L. Janssens, 'Measuring Rate of Heat Release by Oxygen Consumption,' Fire Technol , vol. 27, no. 3, pp. 234-249, Aug. 1991, doi: 10.1007/BF01038449.
- [10] H. Akoglu, 'User's guide to correlation coefficients,' Turkish Journal of Emergency Medicine , vol. 18, no. 3, pp. 91-93, Sep. 2018, doi: 10.1016/j.tjem.2018.08.001.
- [11] I. Riess, D. Weber, and M. Steck, 'On the Air-Flow Resistance of Tunnel Fires in Longitudinal Ventilation - The Throttling Effect,' 2020, p. 10.