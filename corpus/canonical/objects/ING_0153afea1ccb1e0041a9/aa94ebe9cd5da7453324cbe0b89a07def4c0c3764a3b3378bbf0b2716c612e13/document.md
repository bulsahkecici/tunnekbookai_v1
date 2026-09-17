<!-- image -->

Logo

## FIXED FIRE FIGHTING AND EMERGENCY VENTILATION SYSTEMS FOR HIGHWAY TUNNELS - WORKSHOP REPORT

<!-- image -->

Photograph

FHWA-HIF-20-060

## Technical Report Documentation Page

| 1. Report No. FHWA-HIF-20-060                                                                                                        | 2. Government Accession No. TBA                              | 3. Recipient's Catalog No. TBA                                                                                         |
|--------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| 4. Title and Subtitle Fixed Fire Fighting and Emergency Ventilation Systems for 7. Principal Investigator(s): Bill Bergeson (FHWA),  | (Linh) Warren                                                | Highway Tunnels - Workshop Report 5. Report Date April 2020 6. Performing Organization Code TBA Tuonglinh (FHWA), Matt |
| Bilson (WSP), Bill McQuade-Jones (WSP) 8. Performing Organization Report TBA 9. Performing Organization WSP USA, Inc. One Penn Plaza | (WSP), Bobby Melvin and Address                              | Connell (WSP), Katie Name 10. Work Unit No. (TRAIS) TBA Contract or Grant No.                                          |
| 250 West 34 th Street New York, NY, 10119 11. DTFH6114D00048                                                                         | 250 West 34 th Street New York, NY, 10119 11. DTFH6114D00048 | 12. Sponsoring Agency Name and Address Federal Highway Administration U.S. Department of Transportation                |
|                                                                                                                                      |                                                              | 13. Type of Report and Period Covered TBA                                                                              |
| 1200 New Jersey Avenue, SE Washington, DC 20590                                                                                      | 1200 New Jersey Avenue, SE Washington, DC 20590              | 14. Sponsoring Agency Code                                                                                             |

## 15. Supplementary Notes

## 16. Abstract

There is a lot of global experience with fixed fire fighting systems in road tunnels, particularly in Australia and Japan, but also in several recently constructed tunnels in the United States and Europe. The U.S. first implemented FFFS in their tunnels in the 1950s, however, this approach did not become routine, partly  due  to  unsuccessful  tests  of  FFFS  in  the  Offneg  Tunnel  in  Europe.  Because  FFFS  were  not routinely applied in all tunnels, the present-day approach can vary between planned facilities and regions, especially in critical design areas such as operational integration with the emergency ventilation system (EVS). Further research and a design-focused approach to computational modeling and testing is needed to  develop  a  set  of  suggested  practices  for  the  operational  integration  of  FFFS  and  the  EVS.  This document describes the industry workshop, held in Washington, DC on January 15 and January 16, 2020. Workplans for computer modeling and testing (laboratory and full-scale) are also described.

| 17. Key Words Fixed fire fighting system, FFFS, deluge, tunnel, tunnel ventilation, CFD   | 17. Key Words Fixed fire fighting system, FFFS, deluge, tunnel, tunnel ventilation, CFD   | 17. Key Words Fixed fire fighting system, FFFS, deluge, tunnel, tunnel ventilation, CFD   | 18. Distribution Statement No restrictions.   |
|-------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------|
| 19. Security Classif. (of this report) UNCLASSIFIED                                       | 20. Security Classif. (of this page) UNCLASSIFIED                                         | 21. No. of Pages TBA                                                                      | 22. Price                                     |

Form DOT F 1700.7(8-72)

Reproduction of completed page authorized

## Notice

This document is disseminated under the sponsorship of the U.S. Department of Transportation in the interest of information exchange. The U.S. Government assumes no liability for the use of the information contained in this document.

The U.S. Government does not endorse products or manufacturers. Trademarks or manufacturers' names appear in this report only because they are considered essential to the objective of the document. They are included  for  informational  purposes  only  and  are  not  intended  to  reflect  a  preference,  approval  or endorsement of any one product or entity.

The contents of this document do not have the force and effect of law and are not meant to bind the public in  any  way.  This  document  is  intended  only  to  provide  clarity  to  the  public  regarding  the  existing requirements  under  the  law  or  agency  policies.  While  this  document  contains  non-binding  technical information, you must comply with the applicable statutes or regulations.

## Quality Assurance Statement

The  Federal  Highway  Administration  (FHWA)  provides  high-quality  information  to  serve  Government, industry, and the public in a manner that promotes public understanding. Standards and policies are used to ensure and maximize the quality, objectivity, utility, and integrity of its information. FHWA periodically reviews quality issues and adjusts its programs and processes to ensure continuous quality improvement.

## ACRONYMS

| ABBREVIATION   | DETAIL                                         |
|----------------|------------------------------------------------|
| CFD            | Computational Fluid Dynamics                   |
| DGV            | Dangerous Goods Vehicle                        |
| DOE            | Department of Energy                           |
| EVS            | Emergency Ventilation System                   |
| FDS            | Fire Dynamics Simulator                        |
| FFFS           | Fixed Fire Fighting System(s)                  |
| FHRR           | Fire Heat Release Rate                         |
| FHWA           | Federal Highway Administration                 |
| HGV            | Heavy Goods Vehicle                            |
| NFPA           | National Fire Protection Association           |
| NIST           | National Institute of Standards and Technology |
| PIARC          | World Road Association                         |
| RH             | Relative Humidity                              |
| SFPE           | Society of Fire Protection Engineers           |
| SOLIT          | Safety of Life in Tunnels                      |
| U.S.           | United States                                  |
| 1D             | One-Dimensional                                |

## SUMMARY

The Federal Highway Administration (FHWA) is researching the use of fixed firefighting systems (FFFS) in road tunnels. The objective of this project is to identify and address the current industry's ability to adequately consider the operational integration of highway tunnel emergency ventilation systems (EVS) with the installed fixed firefighting system (FFFS), and to then develop a set of suggested practices on the integration of FFFS and the EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (FWHA-HIF-20-016)
2. Workplans and workshops: Industry workshop and report (including computer modeling and testing workplans)
3. Computer modeling research
4. Physical testing
5. Research report and suggested practices

This document is the industry workshop report. The workshop was held on January 15/16, 2020 in Washington, DC. Section 2 of this document provides a summary of workshop attendees and logistics,  Section  3  provides  workshop  notes,  Section  4  summarizes  the  computer  modeling workplan,  Section  5  summarizes  the  physical  testing  (laboratory  and  full-scale  testing),  and Section 6 the next steps.

## ACKNOWLEDGMENTS

The FHWA wishes to acknowledge the workshop participants for their valued contributions to the research project.

The  FWHA  is  the  source  of  all  figures  and  photographs  within  this  document  unless  noted otherwise.

## UNIT CONVERSIONS

## TABLE OF CONTENTS

| INTRODUCTION ................................................................................................................................. 10   | INTRODUCTION ................................................................................................................................. 10                                                                                                                               | INTRODUCTION ................................................................................................................................. 10                                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Literature Survey and Synthesis ................................................................................................. 10                                                                                                                                            |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Terminology................................................................................................................................. 11                                                                                                                                 |
|                                                                                                                                                     | WORKSHOP LOGISTICS .................................................................................................................. 13                                                                                                                                        | WORKSHOP LOGISTICS .................................................................................................................. 13                                                                                                                                        |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | WORKSHOP FEEDBACK .................................................................................................................. 15 FFFS Combined with Other FLS Systems .................................................................................. 15              |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | New Energy Carriers - Alternative Fuel Vehicles ....................................................................... 16                                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Dangerous Goods ....................................................................................................................... 16                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Water Application Rate and FFFS Nozzle Parameters .............................................................. 16                                                                                                                                                             |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Owner Perspectives .................................................................................................................... 19                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Structural Fire Protection ............................................................................................................ 19                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Critical Velocity ............................................................................................................................ 20                                                                                                                               |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Ventilation Design ....................................................................................................................... 21                                                                                                                                   |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Transverse Ventilation ................................................................................................................ 23                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | CFD Models ................................................................................................................................ 24                                                                                                                                  |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Testing ......................................................................................................................................... 25                                                                                                                            |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Other System Considerations ..................................................................................................... 27                                                                                                                                            |
| COMPUTER MODELING WORKPLAN ............................................................................................. 29                         | COMPUTER MODELING WORKPLAN ............................................................................................. 29                                                                                                                                                     | COMPUTER MODELING WORKPLAN ............................................................................................. 29                                                                                                                                                     |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Critical Velocity ............................................................................................................................ 29                                                                                                                               |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Transverse Ventilation ................................................................................................................ 49                                                                                                                                      |
|                                                                                                                                                     |                                                                                                                                                                                                                                                                                 | Areas for Further (Future) Consideration .................................................................................... 55                                                                                                                                                |
| LABORATORY AND FULL-SCALE                                                                                                                           | LABORATORY AND FULL-SCALE                                                                                                                                                                                                                                                       | TESTING WORKPLANS ......................................................... 57                                                                                                                                                                                                  |
|                                                                                                                                                     | Laboratory-Scale Testing Workplan ............................................................................................ 57 Full-Scale Testing ....................................................................................................................... 64 | Laboratory-Scale Testing Workplan ............................................................................................ 57 Full-Scale Testing ....................................................................................................................... 64 |
|                                                                                                                                                     | Areas for Further (Future) Consideration .................................................................................... 71                                                                                                                                                | Areas for Further (Future) Consideration .................................................................................... 71                                                                                                                                                |
|                                                                                                                                                     | SUMMARY AND NEXT STEPS ......................................................................................................... 72                                                                                                                                             | SUMMARY AND NEXT STEPS ......................................................................................................... 72                                                                                                                                             |

## LIST OF FIGURES

| Figure 3-1: Example nozzle spray pattern. ................................................................................18                                                                                                                   |                                                                                            |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| Figure 3-2: Critical velocity concept. ..........................................................................................20                                                                                                            |                                                                                            |
| Figure 3-3: Equation. Pressure balance for a longitudinal EVS. ................................................21                                                                                                                              |                                                                                            |
| Figure 3-4: EVS design inputs and analysis. .............................................................................22                                                                                                                    |                                                                                            |
| Figure 3-5: Transverse ventilation system schematic.                                                                                                                                                                                           | ...............................................................23                          |
| Figure 3-6: Point exhaust schematic.                                                                                                                                                                                                           | ........................................................................................24 |
| Figure 4-1: Longitudinal ventilation. ...........................................................................................29                                                                                                            |                                                                                            |
| Figure 4-2: Memorial Tunnel test results, cross section averaged (bulk) flow rate along tunnel length [17]. .....................................................................................................................32            |                                                                                            |
| Figure 4-3: Memorial Tunnel test results, cross section averaged (bulk) temperature along tunnel length [17]. .....................................................................................................................32          |                                                                                            |
| Figure 4-4: Memorial Tunnel test results, temperature 203 ft. upstream of the fire [17].                                                                                                                                                       | ............33                                                                             |
| Figure 4-5: Memorial Tunnel test results, velocity 203 ft. upstream of the fire [17]. ...................33                                                                                                                                    |                                                                                            |
| Figure 4-6: Memorial Tunnel test results, temperature 217 ft. downstream of the fire [17].                                                                                                                                                     | ........34                                                                                 |
| Figure 4-7: Memorial Tunnel test results, velocity 217 ft. downstream of the fire [17].                                                                                                                                                        | ...............35                                                                          |
| Figure 4-8: Fire heat release rate profile with FFFS operating (LTA test 4) [8]. .........................36                                                                                                                                   |                                                                                            |
| Figure 4-9: Fire geometry for the LTA CFD model. ...................................................................37                                                                                                                         |                                                                                            |
| Figure 4-10: Test data, gas temperature downstream of the fire with FFFS (LTA test 4) [8]. .................................................................................................................................................37 |                                                                                            |
| Figure 4-11: Test data, heat flux downstream of the fire with FFFS (LTA test 4) [8].                                                                                                                                                           | .................38                                                                        |
| Figure 4-12: Example nozzle spray pattern. ..............................................................................39                                                                                                                    |                                                                                            |
| Figure 4-13: Equation. Critical velocity equation based on scale tunnel tests [19].                                                                                                                                                            | ....................41                                                                     |
| Figure 4-14: Equation. Backlayering length derived from scale tunnel tests [19].                                                                                                                                                               | ......................42                                                                   |
| Figure 4-15: Equation. Scaling relationships [19].                                                                                                                                                                                             | .....................................................................42                    |
| Figure 4-16: Equation. Critical velocity with an FFFS operating [11]. .........................................43                                                                                                                              |                                                                                            |
| Figure 4-17: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A). .........................45                                                                                                                                       |                                                                                            |
| Figure 4-18: Square cross section for CFD analysis (ID B).                                                                                                                                                                                     | ......................................................46                                   |
| Figure 4-19: Rectangular cross section for CFD analysis (ID C). ..............................................46                                                                                                                               |                                                                                            |
| Figure 4-20: Rectangular cross section for CFD analysis representing San Pedro de Anes tunnel at the fire site (ID D). ......................................................................................................46                |                                                                                            |
| Figure 4-21: Heavy goods vehicle fire geometry.                                                                                                                                                                                                | ......................................................................47                   |
| Figure 4-22: Tunnel with transverse ventilation showing ducts. .................................................50                                                                                                                             |                                                                                            |
| Figure 4-23: Photo of a tunnel with transverse ventilation.                                                                                                                                                                                    | ........................................................51                                 |
| Figure 4-24: Transverse ventilation system schematic. .............................................................51                                                                                                                          |                                                                                            |
| Figure 4-25: Transverse ventilation system in exhaust near to the bulkhead. ............................51                                                                                                                                     |                                                                                            |
| Figure 4-26: Interaction of water droplet and exhaust................................................................52                                                                                                                        |                                                                                            |
| Figure 5-1: Schematic of test setup. ..........................................................................................67                                                                                                              |                                                                                            |
| Figure 5-2: Example measurement locations. ...........................................................................67                                                                                                                       |                                                                                            |
| Figure 5-3: HGV mock up without shielding.                                                                                                                                                                                                     | .............................................................................68            |

## LIST OF TABLES

| Table 2-1: Workshop attendees. ...............................................................................................14                                                                                                             |             |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|
| Table 4-1: Memorial Tunnel proposed CFD model parameters. ................................................34                                                                                                                                 |             |
| Table 4-2: CFD parameters for critical velocity validation based on tests by Li et al. [13].                                                                                                                                                 | .........40 |
| Table 4-3: Model parameters for critical velocity and FFFS operating. ......................................43                                                                                                                               |             |
| Table 4-4: Critical velocity parameter study. ..............................................................................44                                                                                                               |             |
| Table 4-5: Critical velocity investigation - proposed analysis. ...................................................48                                                                                                                        |             |
| Table 4-6: Transverse ventilation - proposed analysis. .............................................................53                                                                                                                       |             |
| Table 5-1: Proposed laboratory-scale testing general information. ............................................58                                                                                                                             |             |
| Table 5-2: List of laboratory-scale tests specified and full-scale equivalents (calculated per Figure 4-15). .............................................................................................................................61 |             |
| Table 5-3: Model scale test procedures.....................................................................................63                                                                                                                |             |
| Table 5-4: Full-scale testing general information. ......................................................................65                                                                                                                  |             |
| Table 5-5: List of full-scale tests specified and laboratory-scale equivalents (calculated per Figure 4-15). .............................................................................................................................69 |             |
| Table 5-6: Full-scale test procedures. .......................................................................................70                                                                                                             |             |
| Table 5-7: Evaluation of full-scale test results. ..........................................................................71                                                                                                               |             |

## 1 INTRODUCTION

The Federal Highway Administration (FHWA) is currently researching the use of fixed firefighting systems (FFFS) in road tunnels. The objective of this project is to identify and address the current industry's ability to adequately consider the operational integration of highway tunnel emergency ventilation systems (EVS) with installed fixed firefighting systems (FFFS), and to then develop a set of suggested practices on the integration of FFFS and EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (FWHA-HIF-20-016)
2. Workplans and workshops: Industry workshop and report (including computer modeling and testing workplans)
3. Computer modeling research
4. Physical testing
5. Research report and suggested practices

This document is the industry workshop report. Section 2 of this document provides a summary of workshop attendees and logistics, Section 3 provides workshop notes, Section 4 summarizes the computer modeling workplan, Section 5 summarizes the laboratory and full-scale testing, and Section 6 the next steps.

## 1.1 Literature Survey and Synthesis

Relevant to the basic goal of this research, the following key areas are identified in the literature survey and synthesis [1] for further investigation as part of the computer modeling and testing (laboratory and full-scale) efforts:

- Critical velocity - Critical velocity is of interest because the ability to predict critical velocity when an FFFS is operated is the most fundamental input to an integrated EVS design. Existing equations have limited validity at high FHRRs. The goal for further investigation is to develop a  validated  and  verified  method  of  modeling  tunnel  fires  to  determine  critical  velocity  with FFFS, and to extend the range of validity of existing equations.
- Transverse ventilation - Transverse ventilation is of interest because many existing tunnels in the U.S. use a transverse ventilation system. Of concern is how smoke management in a transverse scheme is affected by the FFFS, as well as whether FFFS droplets (liquid water) can become entrained (drawn into) in the exhaust airflow and lower the effectiveness of the FFFS. The laboratory testing and full-scale testing, which follow the computer modeling, are developed to to provide specific test data for validation of models and equations.

Most new tunnels in the U.S. are using a longitudinal EVS via the action of jet fans. The literature survey and synthesis described a design approach where a one-dimensional calculation is used to compute the fan thrust. As part of that review several key parts of the calculation where the FFFS have an impact were identified and are listed below:

- Fire heat release rate (FHRR) - The impact of FFFS on the FHRR is well-established from full-scale tests. Measurements of FHRR (laboratory and full-scale testing) can provide useful additional data to further confirm the efficacy of the FFFS for a given water application rate and nozzle layout/type.
- FFFS cooling of the combustion products - The ability of the FFFS to cool combustion products is well-established. Critical velocity research, modeling and testing (measurement of temperatures), may provide additional data to further the knowledge in this area.
- Pressure  loss  (airflow  resistance)  due  to  fire  - Equations  have  been  developed  for pressure loss due to fire. Measurements of static pressure (laboratory and full-scale) upstream and downstream of the fire may provide useful additional data to further confirm validity of the equations and to understand the FFFS impacts.
- Pressure  loss  (airflow  resistance)  due  to  the  FFFS  (droplets  and  humidity)  - Measurements of pressure loss and humidity in the full-scale and laboratory scale tests may provide  useful  data  for  validation  of  analytical  calculations.  Cold  flow  measurements  may provide useful data related to droplet drag.
- Friction losses introduced by FFFS pipework - Measurements of pressure drop in the tunnel in the full-scale and laboratory scale tests with ventilation operating may provide useful data for validation of friction due to FFS pipework.
- Water droplet deflection due to the EVS - Cold flow measurements may provide useful data related to droplet drift (visualization) due to ventilation. Computer modeling for droplet drift may provide useful data for validation of a model to investigate transverse ventilation and droplet entrainment into a transverse ventilation system exhaust.
- Tenability for egress and fire fighting - The literature survey noted that the impact of FFFS on generation of carbon monoxide is such that the yield of CO is increased due to incomplete combustion. Measurement of CO is likely to provide useful data to help further verify this result. Measurement of irritant gas concentrations, although not a primary focus of this work, would provide useful additional data for future computer model development.

The workplans outline the approach and proposed modeling and testing to research the above topics.  The  content  of  the  workplans  was  presented  at  the  industry  workshop.  The  computer modeling  and  testing  workplans  have  been  developed  based  on  feedback  received  at  the workshop. This  document summarizes workshops and the main technical components of the workplans.

## 1.2 Terminology

In the industry, numerous terms are used to describe FFFS in tunnels. The following descriptions are used herein.

Although a water mist system is technically a deluge sprinkler system (per NFPA 13 - note that use of NFPA standards is voluntary and not a federal or statutory requirement), in the tunnel industry, the terms for deluge system and water mist system have a subtle difference between their meaning. Per the World Road Association (PIARC) publication on FFFS in highway tunnels [2], the following terms are used throughout this document:

- The term deluge system refers to lower pressure large water droplet deluge systems (typical water pressures in the order 1 bar to 1.5 bar, droplet diameter in the order 1000 μm or greater).
- The term water mist system is associated with a deluge system that employs a large water pressure and special nozzles to generate a very small droplet diameter (typical pressures 16 bar to 60 bar, droplet diameter in the order 400 μm to 200 μm).
- Systems that employ frangible bulbs in the nozzles are referred to as automatic sprinkler systems .

Regarding sprinkler systems that employ foam additives , where this document refers to an FFFS it  implicitly refers to a water only FFFS. If a foam additive is applicable or present, then this is explicitly stated in the discussion.

## 2 WORKSHOP LOGISTICS

The workshop was held over two days, from 9 am to 4 pm each day (January 15 to January 16, 2020) in Washington, DC.

The workshop agenda for day 1 (January 15, 2020) was as follows:

- Project intro and scope (9am-10am)
- Literature survey and synthesis - FFFS introduction (10am-12pm)
- Break/lunch (12pm-1pm)
- Literature survey and synthesis - FFFS and EVS (1pm-2:30pm)
- Literature survey and synthesis - FFFS and tunnel structure (2:30pm-3pm)
- Break/discussion (3pm-3:30pm)
- Summary - areas for further research, workplan overview (3:30pm-4pm)

The workshop agenda for day 2 (January 16, 2020) was as follows:

- Computer model workplan (9am-11:30am)
- Break/lunch (11:30am-12pm)
- Laboratory and full-scale testing workplan (12pm-2pm)
- Break/discussion (2pm-2:30pm)
- Summary, discussion and concluding remarks (2:30pm-4pm)

Table 2-1 provides a list of workshop attendees.

Table 2-1: Workshop attendees.

| NAME                         | ORGANIZATION                                                                                  |
|------------------------------|-----------------------------------------------------------------------------------------------|
| Ahmed Kashef (AK)            | National Research Council, Canada                                                             |
| Arnold Dix (AD)              | Consultant, ALARP                                                                             |
| Baron Ozden (call in) (BO)   | National Fire Protection Association                                                          |
| Bill Bergeson (BB)           | FHWA                                                                                          |
| Bill Connell (BC)            | Consultant, WSP                                                                               |
| Bobby Melvin (BM)            | Consultant, WSP                                                                               |
| Clay Naito (CN)              | Professor, Lehigh University                                                                  |
| Conrad Stacey (CS)           | Consultant, Stacey-Agnew                                                                      |
| Dirk Sprakel (DS)            | Director, Fogtec                                                                              |
| Gary English (GE)            | Fire chief (retired), Underground Command and Safety                                          |
| Igor Maevski (IM)            | Consultant, Jacobs / American Society of Heating Refrigeration and Air-Conditioning Engineers |
| Jarod Alston (JA)            | Consultant, ARUP                                                                              |
| Jia-Dzwan (Jerry) Shen (JS)  | FHWA                                                                                          |
| Katie McQuade-Jones (KMJ)    | Consultant, WSP                                                                               |
| Kees Both (KB)               | Promat Research and Technology Centre                                                         |
| Kevin McGrattan (KM)         | National Institute of Standards and Technology                                                |
| Lou Ruzzi                    | PennDOT                                                                                       |
| Maria Garlock (MG)           | Professor, Princeton University                                                               |
| Matt Bilson (MB)             | Consultant, WSP                                                                               |
| Max Lakkonen (ML)            | Director, IFAB                                                                                |
| Negar Elhami-Khorasani (NEK) | Professor, University at Buffalo                                                              |
| Norman Rhodes (NR)           | Consultant                                                                                    |
| Norris Harvey (NH)           | Consultant, Mott MacDonald                                                                    |
| Qi Guo (QG)                  | PhD student, Lehigh University                                                                |
| Spencer Quiel (SQ)           | Professor, Lehigh University                                                                  |
| Stephen Bartha (SB)          | FHWA                                                                                          |
| Tuonglinh (Linh) Warren (LW) | FHWA                                                                                          |
| Vince Chiarito (VC)          | FHWA                                                                                          |
| Yoon Ko (YK)                 | National Research Council, Canada                                                             |

## 3 WORKSHOP FEEDBACK

Day  1  of  the  workshop  was  focused  on  presenting  the  Literature  Survey  and  Synthesis  [3] (referred to herein as the literature survey) to the participants. Day 2 of the workshop focused on the scope of the proposed computer modeling and testing (laboratory and full-scale).

The workshop opened with a discussion about the project history, with participants noting that the project  is  in  part  based  on  research  needs  developed  between  members  of  NFPA  502  and ASHRAE working groups in 2015. The goal of the project was reiterated; to develop a set of suggested practices for the integration of highway tunnel emergency ventilation systems (EVS) and fixed  fire  fighting  systems  (FFFS).  The  overall  research  plan  was  discussed  in  terms  of planned deliverables associated with each phase of work, including a computer modeling report, a testing report, and a final research report describing the suggested practices. It was noted that the final research report is not planned to be a guideline or standard.

Key points from both days of the workshop are summarized in this section by discussion topic and actions. The actions are tied to one of the three report deliverables, computer modeling, testing or the final research report. The computer modeling and testing workplans, incorporating workshop feedback, are detailed in Section 4 and Section 5 herein.

## 3.1 FFFS Combined with Other FLS Systems

This discussion topic was inspired by presentation of an overview of U.S. tunnels as presented in Section 2-9 of the literature survey. The overview noted salient points about several U.S. tunnels including the length of the tunnel, ventilation system type and whether a FFFS was present.

It was noted that many of the older existing U.S. tunnels do not have an FFFS installed. The only U.S. tunnel presently operating with an FFFS retrofit is the Eisenhower-Johnson Memorial Tunnel in Colorado. The Brooklyn Battery (Hugh Carey Tunnel) in New York City is currently installing a mist system as a pilot project. Most all recently built U.S. tunnels have been equipped with an FFFS.

Consideration of the benefit to fire-life safety (FLS) that could be realized with installation of a FFFS were discussed. Examples include the design fire heat release rate (FHRR), spacing and placement  of  exit  doors  or  cross  passages,  and  level  of  structural  fire  protection  necessary. Development of a list of other possible FLS system combinations that could potentially be realized was suggested. The SOLIT (Safety of Life in Tunnels) [4] research report was noted to have discussed impacts of FFFS on other FLS systems.

Action: The final research report to consider including a list of potential FLS system combinations that become possible when an FFFS is installed; in addition to those developed directly from this research for the EVS.

## 3.2 New Energy Carriers - Alternative Fuel Vehicles

The discussion drew on material from Section 3.6 of the literature survey. This section presented information about new energy carriers, otherwise referred to as alternative fuel vehicles. It was noted that although many tunnels do not presently allow these vehicles that there is a significant amount of research taking place into the fire risks posed by these types of vehicles and their safety feature performance.

It  was noted that a key question is how fire departments respond to fires in these vehicles. In Germany there is testing taking place on electric vehicle type fires and publications are soon to be released. One key question relevant to this research is whether water-based suppression systems can be safely used on alternative fuel vehicle fires. Additionally, alternative fuel use was noted to be quite prolific for buses in several jurisdictions, and that research focused on bus fires could be a useful source of future information.

Action: Given the active research in this area, the final research report is to consider including an update on any new information of relevance to the use of water based FFFS on alternative fuel vehicles.

## 3.3 Dangerous Goods

The discussion drew on material of dangerous goods (cargo) fires, particularly bulk liquid fuel fires, as presented in Section 3.3.3 and Section 3.4.4 of the literature survey. Work conducted by the Research Institutes of Sweden (RISE) was presented. This work looked at tests involving running fuel spill tests and concluded that water-based systems alone were unlikely to reduce the FHRR, and that foam additives were needed [3]. The tests were noted to be small-scale.

The design fire suggested in NFPA 502 [5] for a gasoline tanker fire is in the range of 200 MW to 300 MW. One of the key characteristics for a gasoline tanker fire is the potentially fast fire growth rate. A previous incident has suggested that the fire can grow very fast [6], possibly limiting the ability  of  a  tunnel's  safety  systems  (FFFS  and/or  EVS)  to  respond  fast  enough  to  have  an impactful  affect.  An  issue  for  many  tunnel  operating  authorities  is  whether  dangerous  goods vehicles should be allowed passage through the tunnel or be forced to use an alternative route.

It was noted that there are no plans to study impacts of FFFS on hazardous/dangerous goods vehicle fires as part of this research, since the scope is focused solely on the interaction of the FFFS and EVS. This subject is considered a detailed topic for possible future research projects.

Action: This  topic  is  not  in  the  principal  scope  of  work,  but  it  is  relevant  to the  industry;  new developments are to be considered for a summary level inclusion in the final research report.

## 3.4 Water Application Rate and FFFS Nozzle Parameters

Water application rates for FFFS tunnel application were discussed; this parameter has a major impact on both system performance and design as it directly determines the overall water supply needed. It was noted that Section 4.4 of the literature survey details how international tunnel industry experience varies in regard to selected water application rates for FFFS, and that current design standards do not specify a water application rate for a tunnel application. Many factors were noted to come into consideration when choosing water application rate for a given tunnel application. One of the key considerations is to identify performance goals of the FFFS, and then look at how factors such as water application rate and droplet size influence that performance. The available water supply, both length and width of the FFFS zones, and number of operational FFFS zones were identified as key factors, especially when retrofitting an existing tunnel.

Mist systems versus deluge systems were discussed in relation to water application rate. Mist systems typically use less water with a smaller droplet size, while a deluge system uses larger droplets  and more water. The discussion noted that different mechanisms of cooling in a fire situation can dominate with one system or another; a small mist droplet has a larger surface area and evaporates faster to provide increased cooling, while a larger droplet tends to penetrate the fire plume and potentially reach the burning surface. Both systems were noted to have potential to provide FLS benefits. The choice of one system versus another can depend on the particulars of the application. For instance, drainage was noted to be a challenge when retrofitting an existing tunnel  and  thus  an  FFFS  using  less  water  may  be  beneficial.  Droplet  drift  due  to  ventilation conditions  is  another  consideration to  be  made when  choosing  an  FFFS  type, for  example  a system with larger droplets has potential to be less affected by ventilation.

Action: Water application rate is a key parameter for the FFFS design and performance. Consider this as a variable in the computer modeling and testing work, along with discussion of findings in the final research report.

Action: Include notes about NFPA 13 application rates and a goal to develop a tunnel water application rate chart like NFPA 13 in the workplan for testing. Refer to Section 5.3 herein, which identifies this as an area for further future research.

Nozzle parameters were also discussed. The nozzle directly influences the droplet size, water application rate, coverage area and hence the overall system performance. Nozzle manufacturers produce differing  nozzles  that  aim  sprinkler  sprays  in  different  directions  or  produce  different percentages of certain droplet diameters over a given area. These factors are considerations when designing an FFFS. Both mist and deluge type FFFSs were noted to produce a spectrum of  droplet  sizes.  For  instance,  a  low-pressure  deluge  system,  which  consists  mostly  of  large droplets  can  still  produce  a  lot  of  fine  droplets.  It  was  noted  by  participants  that  many manufacturers of nozzles do not typically provide droplet size data but that they do provide  water delivery data to a floor area or wall area for a given nozzle; refer to Figure 3-1. Participants noted that nozzle performance details need to be considered as part of an FFFS design. It was also noted that U.S. fire protection system codes specify nozzles to be 'listed' for their application. Note that "listed" herein means that a device has been tested and found suitable for a specified purpose and is included in a list published by an organization that is acceptable to the authority having jurisdiction. Many tunnel nozzles used in tunnel applications outside the U.S. may not be listed for use here. Consideration of the nozzles used in recent U.S. tunnel projects with an FFFS installed  was  suggested  (by  workshop  participant)  as  an  avenue  to  explore  to  further understanding of nozzle use in U.S. tunnels.

Figure 3-1: Example nozzle spray pattern.

<!-- image -->

Engineering drawing

The scope of the testing proposed is based on laboratory-scale tests (approximately 1:4 scale) and full-scale tests (refer to Section 3.11 and Section 5 herein). A concern was raised regarding how to scale from laboratory-scale up to full-scale for the nozzles. The scaling is based not just on dimensional considerations but also on matching dimensionless numbers such as the Froude number (refer to the literature survey Section 5.2.1.3). It was suggested that researchers in the fire sprinkler industry may offer insights on this matter.

For computer models, such as Fire Dynamics Simulator (FDS), the single droplet size specified is the median droplet size. An approach to computer modeling was outlined. It would involve using the  Rosslin-Ramler  distribution  of  droplet  diameters  (default  in  FDS,  established  via  previous research [7]), and investigating parameters such as the droplet speed and spray angles. The aim would be to correlate the model spray pattern with the test data for a given nozzle and flow rate (based on water pressure).

Action: Nozzles are a key parameter for the FFFS design. Increase the depth of the investigation to include consideration of nozzle parameters and how to link nozzle parameters from testing to computer  models.  Consider  reaching  out  to  industry  experts  on  nozzle  design  and  consult published data review the current knowledge. Explore how to include the parameters for a given nozzle  in  the  computer  model  such  that  the  computer  model  replicates  key  performance measures such as nozzle water spray distribution.

Action: Include  a  nozzle  parameter  study  in  the  Computer  Modeling  Workplan.  The  study involves adjusting FDS parameters including spray angle, velocity, droplet diameter, offset, and particles per second for a standard spray pendant nozzle in order to match the spray distribution of that nozzle. The nozzle type is planned to be informed by previous tunnel testing [8] where a standard pendant nozzle was used. For the nozzle, it might be necessary to assume an average droplet diameter for a typical pendant nozzle (for example, catalog data [9]). This would involve using droplet diameters per data provided in other test reports [7] since the specific nozzle type used  in  the  tunnel  test  [8]  was  not  disclosed.  Refer  to  the  workplan,  Section  4.1.2.2,  for  a discussion of the test data and modeling proposed. See also, Section 5.1.2 and 5.2.1 herein for discussion on testing.

## 3.5 Owner Perspectives

Some discussion of the owner's perspective with respect to FFFS took place. One issue owners face when looking at their existing tunnels is the decision to retrofit their facility with an FFFS. It was noted by one agency participant that a useful tool for tunnel owners would be a flowchart or decision tree to help them work through the process; or a checklist that outlines what they need to consider. Some factors to consider are that, in addition to life safety, a key area of concern is protection of assets i.e., the tunnel facility itself. Resiliency of the tunnel infrastructure is a likely benefit of the FFFS and there is a need to help inform policy makers of the overall role that an FFFS plays in this. A key goal of any tool developed would be to provide owners with an objective method to assess pros and cons of installing an FFFS; the goal would be to have a framework that could be used to help document the basis of a decision.

Action: This  topic  is  not  in  the  principal  scope  of  work,  but  it  is  relevant,  and  it  is  under consideration for some more detailed discussion in the final research report.

## 3.6 Structural Fire Protection

Structural fire protection and the impact of the FFFS is looked at in Section 6 of the literature survey. Data were quoted from research which showed that the FFFS can reduce temperatures in a tunnel fire, potentially reducing the design basis temperatures for structural fire durability. This reduction might enable a more integrated design for structural fire protection measures. This topic was discussed in the workshop and feedback was received from participants.

In looking at the benefits of the FFFS for structural fire durability it was noted that the impact of temperature on the structure is seen in two ways. One way is the impact of heat on the ability of the  structure  to  continue  to  withstand  the  load,  and  the  second  way  is  through  any  plastic deformation  of  the  structure.  Both  issues  were  noted  to  be  important  design  considerations although usually the focus is on the impact of heat on the structure's load bearing capacity. It was noted that deformation can cause cracks in the unexposed structure which can be hard to detect and repair.

It was noted that these aspects of structural design are an extension to the scope of the research and that detailed treatment is not planned. Data could be recorded in computer models and tests to help support future research in this area. It was also noted that when looking at the data that the time-temperature curve for structural fire protection design might be able to be adjusted based on  FFFS  inclusion.  The  adjustment  could  consider  the  peak  temperatures  reached  and  time duration.

A structural analysis model under development by Lehigh University was discussed [10]. The model considers the heat release rate and energy budget, and it can provide results in a short period of time. This can facilitate a parametric risk assessment. The model is validated against results from Fire Dynamics Simulator (FDS). The Lehigh model is not part of this work and it does not address FFFS or EVS impacts. The tool may have application for future research efforts.

Action: Include data collection in the computer modeling and testing to support future structural design  research  and  development  with  respect  to  inclusion  of  FFFS  influences.  Data  to  be recorded in CFD analysis and testing. Refer to the workplan, Section 4.1.4.1 and Section 4.2.3.1, for more detail on data to be recorded.

Action: Include discussion points on the Lehigh University model in the final research report as a potential area for further investigation.

## 3.7 Critical Velocity

Critical velocity is the air speed necessary, in a longitudinal ventilation system, to direct smoke downstream of a fire. Refer to Figure 3-2. Critical velocity varies with tunnel geometry and FHRR. Equations to predict critical velocity have been developed. Results of critical velocity prediction from  several  equations,  versus  Memorial  Tunnel  (full  scale  fire  and  ventilation  test  program conducted  in  the  U.S.  in  the  1990s)  test  data  (as  per  the  literature  survey  Section  5),  were presented. Equations derived as part of the PhD research of Ko [11], looking at the impact of the FFFS on critical velocity, were presented. Critical velocity is a useful parameter for measuring the potential efficiency in the EVS design when an FFFS is included; it is a single and relatively simple measurement of performance which can provide a consistent basis for comparison of the impact of certain FFFS parameters (droplet size, water application rate) on the EVS.

Figure 3-2: Critical velocity concept.

<!-- image -->

Engineering drawing

Discussions about critical velocity equations took place. In Ko's work it was noted that critical velocity was judged based on temperature and not visibility of smoke. The importance of having a consistent way to measure critical velocity was noted by participants. It was suggested that the work should  look  at  backlayering  (movement  of  smoke  back  upstream  against  the  prevailing airflow) as part of the parameter study since backlayering length can vary with airspeed. The importance of a hypothesis was discussed since it can help to narrow down the models and testing to address the key issues.

Action: Measure  critical  velocity  from  the  analysis  and  testing  considering  temperature  and visibility,  not  visibility  alone.  Seek  to  use  a  consistent  method  between  all  models  and  tests. Measure backlayering distance as well as critical velocity.

Action: Develop hypotheses as part of the workplan design. Refer to the workplan, Section 4.1 and Section 4.2 herein. Refer also to Section 5 herein.

Action: Note  need  to  vary  airspeed  and  measure  backlayering  length  in  computer  model workplan and testing workplan, as well as means to define critical velocity. Data to be recorded in CFD analysis and reported. Refer to the workplan, Section 4.1.4.1 herein for a summary of data to record, and mention of recording data such that backlayering length as a function of upstream velocity can be recorded. Refer to the workplan, Section 5.1.2 and 5.2.1 herein, which note the need to capture data from testing to record these aspects.

## 3.8 Ventilation Design

When designing a longitudinal ventilation system, a force balance is used, as per Figure 3-3. This is discussed in more detail in Section 5.3 of the literature survey [3].

## Figure 3-3: Equation. Pressure balance for a longitudinal EVS.

In Figure 3-3 symbols are defined as follows: Nf is the number of jet fans, ∆ Pj is the pressure rise due to a jet fan, ∆ PVEH is the pressure loss due to vehicles, ∆ Pf is the pressure loss due to wall friction,  lights,  FFFS  pipework,  entry  losses,  exit  losses, ∆ Pm is  the  pressure  loss  due  to meteorological effects, including wind, ∆ Pb is the pressure loss or rise due to buoyancy, ∆ Pfire is the pressure loss due to the fire, and ∆ PFFFS is the pressure loss due to the FFFS spray.

There are terms in the force balance that are potentially affected by the FFFS. The force balance equation in expanded form is non-linear; pressure loss due to vehicles can be significant, external wind can also be significant, but there is no one term that dominates. A combined FFFS-EVS design solution has a lot of inputs and interactions, as shown in Figure 3-4.

Figure 3-4: EVS design inputs and analysis.

<!-- image -->

Flow chart

In a tunnel environment, FFFS impacts to consider include the following:

- Fire heat release rate
- Critical velocity for smoke control
- FFFS cooling of the combustion products
- Pressure loss (airflow resistance) due to fire
- Pressure loss (airflow resistance) due to the FFFS (droplets and humidity)
- Friction losses introduced by FFFS pipework
- Water droplet deflection due to the EVS
- Tenability for egress and fire fighting

During the workshop, the input parameters for ventilation design that are both established and less well-established were identified. The presentation noted that some key areas for furthering knowledge  include  the  pressure  loss  due  to  both  the  fire  and  the  FFFS  (water  droplets  and humidity), and friction losses introduced by the FFFS pipework. Friction losses introduced by the water spray were discussed and noted to be generally small, but it was noted that for tunnels with very wide cross sections, or several zones operating, that this factor has potential to increase somewhat and a method of quantifying losses would be useful. Humidity of the air downstream of  the  fire  was  also  identified  as  a  possible  uncertainty;  it  was  noted  in  discussion  that  FDS accounts for the relative humidity, including limiting water evaporation per the saturation limit of the air, thus allowing the impact of this parameter to be quantified in the modeling. Testing was noted to include measurement of relative humidity.

Another parameter discussed was the uncertainty about whether water droplets would influence fan performance. Some participants noted this was an unlikely issue since water mist sprays are sometimes used to cool the airstream prior to the fan in a ventilation exhaust duct to prevent fan damage. This may be a secondary effect for a later study since practical experience has been that fan extract improves when the air stream is cooled. Further investigation was suggested, via a desktop survey, to see if any data are available. Specific testing to look at this was determined to be outside of the scope of the tests and the issue was not considered significant enough to add this testing.

Action: Consider if there are any published data on water and fan interaction. Water interaction testing with fan performance is not currently proposed as this has not proven an issue in practice. Has been noted for possible future work, refer to Section 5.3 herein. Include any findings in the final research report.

Action: Note the relative humidity in development of computer model workplans and fact that FDS does limit evaporation thus making it reliable for looking at this possible limit with FFFS-EVS integration. Data to be recorded in CFD analysis and reported. Refer to the workplan, Section 4.1.4.1 and Section 4.2.3.1 herein for a discussion of additional data to record.

## 3.9 Transverse Ventilation

Discussion of transverse ventilation, focused on a system with many distributed exhaust and supply ports, see Figure 3-5, took place. These types of transverse systems are most common in the U.S. It was proposed, for interaction of the FFFS and EVS, that once a water droplet is in the tunnel space, the physics (turbulence, heat transfer, multiphase flow) are similar for the transverse ventilation case as in the longitudinal ventilation case. The conclusion was made that the major unknown transverse ventilation parameter regarding FFFS is entrainment of water drops into the exhaust duct.

Figure 3-5: Transverse ventilation system schematic.

<!-- image -->

Engineering drawing

For single point exhaust, Figure 3-6, there is a question on how many dampers to open and that current publications do not consider FFFS when determining how large the single point zone should be. Also, for transverse ventilation with FFFS it is not certain by how much the FFFS might allow a reduction in exhaust flow rate, nor is it known whether this possible reduction is affected by having dampers located above the roadway or to the side of the roadway.

Figure 3-6: Point exhaust schematic.

<!-- image -->

Engineering drawing

Discussion  noted  that  there  are  many  permutations  of  EVS  and  FFFS  when  considering  a transverse ventilation system. The CFD model physics are similar for the various permutations of EVS (longitudinal, transverse, single point transverse), so testing all the possible permutations of tunnels as part of this project was not proposed. Adding some cases to the modeling scope is to be considered to shed some light, but a full study along the spectrum of all possible design cases was not considered practical nor necessary.

Stratification of smoke is more important in a transverse EVS compared to longitudinal systems. As part of the discussion questions were raised such as is there a stratification outcome to identify and can the FFFS affect this. It was noted that the Burnley Tunnel fire from 2007 was a practical example of a transverse system with FFFS. It was noted that some new studies are underway, or have been recently completed, in relation to water droplet and smoke layer interaction. This work is taking place at Ghent University in Belgium.

Action: Include extra CFD models in the workplan to allow for looking at the interaction of FFFS and EVS for some different transverse ventilation schemes, especially considering things like the location  of  exhaust  points  when  dealing  with  single  point  exhaust,  and  different  FFFS configurations (mist, deluge, varying water application rate). Include measurement or visualization of smoke stratification in the analysis, considering smoke spread as well. Refer to the workplan, Section 4.2, which discusses the workplan to address different (transverse) ventilation systems. One  outcome  of  the  research  conducted  per  this  section  is  a  planned  demonstration  of  the approach to addressing different FFS and EVS configurations.

Action: Investigate work at Ghent University on sprinklers and whether any relevant points arise to factor into modeling and testing work, and summarize in the final research report.

## 3.10  CFD Models

Computational  fluid  dynamics  (CFD)  model  approaches  were  presented  with  Fire  Dynamics Simulator (FDS) noted as the model of choice because of the number of fire dynamics phenomena already set up, as opposed to a customizable commercial CFD package. Some further justification for the use of FDS was requested by some participants. It was noted that FDS includes all the relevant physical models and input parameters specific to the problem of smoke management and sprinkler operation. Validation was emphasized in order to test the modeling approach and provide  assurance  that  the  user  has  set  the  problem  up  correctly.  The  approach  to  model validation was presented, focusing on existing test data for tunnel fires with and without FFFS operating.

A workplan for the critical velocity and transverse ventilation investigation was outlined. Several tests were outlined for use in validation, gradually adding factors, including a fire with no FFFS, an FFFS scenario, and critical velocity experiment cases. One key goal with the validation is to help  understand  the  model  uncertainty  with  respect  to  the  engineering  parameters  being investigated. This can include uncertainty in the test conditions (FHRR, upstream velocity) and the model results.

Action: Different CFD software options have been considered. At this time the FDS software is best suited because it includes all the necessary physics to address the scenarios proposed in the workplans, and the model is freely available, meaning that the findings of this research can be easily used and directly applied by other industry practitioners. Document some of the different CFD model software options and basis for choice of model in the computer modeling report..

Action: Test programs with useful data to be considered, especially as data relates to nozzles and scaling (see action 1). Major edits to the workplan for new test data are not proposed; after reviewing  the  workplans  and  data  available,  there  are  enough  data  in  the  existing  literature documented to sufficiently validate the CFD models. Refer to the workplan, Section 4.1.2.2 herein, for a discussion of the test data and modeling proposed.

Action: Communicate uncertainty clearly in the test data and model results where possible. Refer to the workplan, Section 4.1.2, Section 4.1.4.1 and Section 4.2.3.1 herein, which note the need to document uncertainty in model results. See also Section 5.1.2 and 5.2.1 herein, which note the need to document uncertainty for testing.

## 3.11  Testing

The testing scope originally called for in the project scope involved laboratory-scale and full-scale testing. An overview of both testing options was presented, including available facilities for fullscale testing.

For laboratory-scale testing, the idea is that results can be scaled up to full-scale equivalency through Froude scaling (refer to the literature survey Section 5.2.1.3). Droplet size scaling was noted  as  a  factor  to  include.  It  was  also  noted  that  scaling  becomes  less  reliable  with  FFFS involved due to cooling and a reduction in the buoyancy.

Laboratory-scale testing needs to consider whether the scaling rules are valid. In a wind tunnel, for instance, results can be scaled based on a single dimensionless parameter alone (e.g., the Reynolds number). However, in the multi physics fire situation there are many more parameters to consider (i.e. forced ventilation, upwelling current, buoyancy forces, combustion, heat transfer, radiation, etc.) which are described by more than one non-dimensional number, and can have dependencies  in  opposite  directions.  This  means  that  one  physical  phenomenon  can  be represented while other important physical phenomena  might  be  neglected or scaled inappropriately. Addressing all the uncertainty in scaling is a separate research project and any laboratory-scale work conducted needs to be carefully developed so that the data are useful with respect to research goals. The scope of this project is not to develop a new scaling regime. It is noted that one of the key goals of testing is to provide additional data for model validation and the detailed test protocol should consider this and the scaling uncertainties.

Action: Note  droplet  scaling  and  Froude  number  scale  weaken  when  the  FFFS  cools  the environment.  Scaling  is  an  area  of  uncertainty  and  the  need  to  factor  in  different  scales  in measurements is noted. The geometry from laboratory-scale to full-scale is geometrically scaled, thus allowing this to be investigated further when all data are available.

Action: New test programs with useful data to be considered, especially as data relates to nozzles and scaling. Refer to Section 5.1.2 herein, which identifies the possible need for nozzle parameter measurements via imaging.

Discussion  of  facilities  for  full-scale  testing  noted  that  the  Memorial  Tunnel,  located  in  West Virginia and previously used for full-scale fire tests in the 1990s, is now a Department of Defense training facility that is no longer a candidate for tunnel fire testing since it is built out. The San Pedro tunnel in Spain is the only facility ready to be used for full-scale tunnel fire tests with FFFS and EVS operations taking place. A suggestion was made that military facilities (Lakehurst Naval Air Base) might be worthwhile candidates for full-scale tunnel fire tests.

Testing  goals  were  discussed.  One  of  the  principal  goals  is  to  provide  data  to  compliment computer models and confirm the validity of the model. Additional goals were noted, including measurement of the pressure loss caused by FFFS components such as pipework and valves. The  pressure  loss  (airflow  resistance)  of  these  items  can  be  estimated  from  engineering textbooks, however, the correlations are not always a close match to the physical configuration of the FFFS components.

Uncertainty of FHRR measurement in testing was discussed. When an FFFS is operating, the FHRR is measured via oxygen consumption, and it was stated that the FFFS could introduce an error up to 15% in the reading. It was noted that whenever a test is run there are calibration exercises conducted to help limit the uncertainty.

Fan thrust was identified as a key measurement to take in order to provide data for calibration of FFFS effects in one-dimensional EVS models typically used in design (per Figure 3-3).

General discussion about full-scale testing took place. It was noted that thermocouples are in the walls of the tunnel at the San Pedro facility and these are in place to monitor conditions and trigger a stop to the test if potential for tunnel damage exists. Fire configuration was discussed, and it was agreed that a roof should be added to the fire configuration so that a worst-case condition can be tested. It was noted that the tests, especially at full-scale, are not seeking to develop a complete characterization of performance (such as the water application rate chart in NFPA 13) but rather the tests are planned to provide an additional data point specific to the purpose of looking at combined FFFS-EVS performance.

Action: Practical items, such as monitoring temperature, shielding, FFFS goals in the test, to be included in the testing workplan. Refer to the workplan, Section 5.1.2 and 5.2.1 herein, which note the need to capture data to test these aspects.

Action: Include notes on the possibility of developing a water application rate chart, like NFPA 13, in the final research report.

Action: Focus on laboratory-scale testing initially and revisit the full-scale testing scope once more information is available.

## 3.12  Other System Considerations

A lot of discussion took place around the other systems that the FFFS influences or relies on to operate. Some of the main items are included below along with actions.

## 3.12.1 FFFS Operation - When to Activate

There is a loss of visibility and direct impact on motorists when a FFFS is activated in a tunnel, so the tunnel operator's decision to activate the FFFS is far more critical than the immediate action to activate the EVS. There is generally some delay during the early stages of a vehicle fire where the emergency ventilation system can manage the flow of the smoke, before turning on the FFFS is  necessary  (depends  on  the  profile  of  the  fire  growth  curve).  In  response  plans  (recently developed for some tunnels with FFFS) operators are trained to activate the FFFS only when they see flame.

How the capabilities and performance of automatic fire detection systems affect system activation is a significant consideration. One concern is false activation. Participants noted that there have been multiple false activations of FFFS, likely resulting in areas of low visibility that catch motorists unaware.  This  fact  suggests  that  the  risk  associated  with  a  vehicular  accident  due  to  false activation  might  be  higher  than  having  a  non-automatic  FFFS.  It  was  noted  that  water  mist systems build up slowly due to the finer droplets and there would not be an instant "wall" of water as would be the case with a deluge type system. Meeting attendees could not confirm an instance where cars stopped driving through the FFFS water. In building applications, system engineers are noted to include interlocks to confirm fire to limit false activations. It was noted that turning on the EVS has no adverse effects on traffic. Discussion noted that deluge systems in tunnels that have 24/7 monitoring, typically have a delay time applied after the automatic fire detection initiates that allows the tunnel operator time to access and abort any automatic FFFS activation. It was noted that there are no known tunnels that have an FFFS without a 24/7 operator (there are tunnels with EVS and standpipe).

Action: The discussion points could be relevant to the final research report, consider inclusion.

## 3.12.2 Tunnel Washing

Washing operations could interfere with the FFFS, however, specific information was not known.

Action: Investigate and include findings in the final research report.

## 3.12.3 FFFS and EVS Combinations

Additional factors to consider when looked at combined FFFS and EVS operations include fire detection (automatic or manual), system reliability and impact on outcomes if a system fails to operate.

Action: Investigate and include findings in the final research report.

## 4 COMPUTER MODELING WORKPLAN

The computer modeling workplan is comprised of two components based on EVS operations. The first  component  looks  at  critical  velocity  and  the  impact  on  this  with  FFFS,  and  the  second component  looks  at  transverse  ventilation.  Principal  hypotheses  being  investigated  with  this workplan are described below.

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized as a result  of  the  cooling  effects  of  the  FFFS  water  spray.  This  hypothesis  can  be  verified  via measurement of the critical velocity for smoke control, pressure loss due to the FFFS water spray and impact of the EVS on water delivery. If the hypothesis is true, then the critical velocity should decrease due to the cooling. Additional airflow resistance introduced by the FFFS spray should be negligible with respect to other airflow resistance in the tunnel from items such as vehicles, wall friction, buoyancy, fire and external wind. Finally, the EVS should not cause excessive water droplet drift as to cause a negative effect on water droplet delivery to the fire zone.

The second hypothesis is that CFD can be used to predict FFFS and EVS interaction, such that a CFD approach can be defined for use to verify the FFFS and EVS design integration for the most commonly used combinations of FFFS (small and large water droplet systems, varying water application rates and zone configurations) and EVS (transverse ventilation, single point exhaust, longitudinal ventilation) within a varying tunnel geometry (area, perimeter, height). This hypothesis is to be verified via computer modeling proposed herein.

## 4.1 Critical Velocity

In a longitudinal ventilation system fans are used to generate air flow through the tunnel. Air is blown through the tunnel bore, therefore having one portal act as an inlet and the other an outlet; refer to Figure 4-1. Ventilation is typically achieved by jet fans installed in the tunnel ceiling space.

Figure 4-1: Longitudinal ventilation.

<!-- image -->

Engineering drawing

Critical velocity is a key design parameter for a longitudinal EVS. The methods used for predicting critical velocity in tunnels typically include semi-empirical equations [12] [13] and, in recent years, CFD modeling [14]. Critical  velocity  is  a  function  of  input  parameters  including  FHRR,  tunnel geometry and tunnel slope.

Per NFPA 502, the following definitions are used herein for backlayering and critical velocity [5]:

- Backlayering - Movement of smoke and hot gasses counter to the direction of ventilation airflow.
- Critical velocity - The minimum steady-state velocity of the ventilation airflow moving toward the fire, within a tunnel or passageway that is necessary to prevent backlayering at the fire site.

The potential FFFS impact on critical velocity is to reduce the velocity through the cooling action of the water spray, assuming no change in the FHRR. A detailed discussion of the interaction of FFFS and EVS can be found in the literature survey and synthesis [3].

## 4.1.1  Approach

Fire Dynamics Simulator (FDS) is proposed to be used for the modeling [15]. FDS encompasses all the essential physics for modeling fire in a tunnel and the cooling effects from the FFFS. The models are to be based on a priori specified heat release rate per unit area for the fire with no fire suppression modeled, only cooling of combustion products. Models are proposed to be developed to  validate the approach and, once the approach is validated, a series of scenarios are to be analyzed to determine the critical velocity with an FFFS operating.

The CFD models are to apply a fixed velocity from upstream of the fire which is to be varied in increments of 0.2 m/s to determine the nearest match to critical velocity. To determine the critical or  containment  velocity,  smoke  spread  upstream  is  to  be  measured  using  visibility  and temperature sensors placed at the tunnel ceiling. In line with previous tests, where there is doubt between visibility or temperature indicating backlayering, the temperature indicator is planned to be used. Backlayering length for a given velocity it to be recorded. The following terms are used herein when determining critical and containment velocity:

- Critical  velocity  -  The  minimum  upstream  ventilation  velocity  that  prevents  smoke  spread upstream of the fire.
- Containment velocity - The (average) upstream ventilation velocity that limits smoke spread upstream of the fire to no more than 30 meters (100 feet).

## 4.1.2 Validation

CFD models to be conducted for validation purposes as follows:

- Prediction of the tunnel environment during a fire:
- Memorial Tunnel (West Virginia) tests (no FFFS) [16] [17]

- San Pedro de Anes tunnel tests (with FFFS) [8]
- Prediction of the critical velocity:
- Li's scale tunnel tests (no FFFS) [18] [19]
- Ko's correlation (with FFFS) [11]

Models to be compared with test data available, primarily velocity and temperature profiles within the tunnels considered. For critical velocity comparisons the results are to be compared with the critical velocity equations provided in the literature. In all comparisons, the uncertainty and level of accuracy is planned to be quoted, and where possible, quantified. Uncertainty to include model and test data uncertainty where possible.

## 4.1.2.1  Memorial Tunnel Tests - Tunnel Temperature and Velocity

A series of physical fire tests were conducted in the Memorial Tunnel (located in West Virginia) with  a  longitudinal  ventilation  velocity  applied  [16]  [17].  For  this  validation  exercise,  Memorial Tunnel fire test 615B (longitudinal velocity) is proposed to be used. This test had an FHRR of 78 MW with an upstream velocity of 2.0 m/s (based on an unobstructed cross section, or 2.4 m/s accounting for blockages). Backlayering occurred in this test. Test data for validation includes temperature and velocity profiles upstream and downstream of the fire, and smoke spread extent. Tunnel set up details and test data are described below.

Tunnel cross section. Refer to Figure 4-17. Tunnel grade runs downward from north to south (smoke is always ventilated downgrade in the longitudinal ventilation tests), grade is a constant of 3.2%.

Fire geometry. The fire used a pan of fuel oil (number 2 fuel oil) to generate a heat release rate (HRR) ranging from 10 MW to 100 MW. A surface area of 48 ft 2  was estimated to produce a 10 MW HRR. Fire pans were set approximately 30 inches from the tunnel floor. Fire proofing was applied to the walls near the fire site [16]. The centerline of the fire was at loop 205, which was approximately 2019 ft. from the north portal. At the fire site the tunnel cross sectional area was approximately 650 ft 2 , and the instrumentation was estimated to take up an area of approximately 110 ft 2 ,  thus  giving  a  reduced  area  and  higher  velocity  in  the  region  of  the  fire.  Pans  were correlated to FHRR approximately as follows: 50 MW used a 20 ft. by 12 ft. pan, 20 MW used a 12 ft. by 5 ft. pan, 10 MW used a 4 ft. by 12 ft. pan, and 30 MW used a 12 ft. by 12 ft. pan [17].

Fire parameters. Heat of combustion 42.6 MJ/kg, radiation fraction 0.3, air to fuel ratio 14.5, soot yield  0.042  kg  soot/kg  fuel,  carbon  monoxide  yield  0.012  kg  CO/kg  fuel,  molecular  weight  of combustion products 28 kg/kmol.

Instrumentation, results and CFD models. Results for comparison with CFD models include total flow rate along the tunnel length (Figure 4-2) (note that the free area for conversion to a velocity is 540 ft 2 ), average temperature along tunnel length (Figure 4-3), temperature profile upstream of the  fire  (Figure  4-4),  velocity  profile  upstream  of  the  fire  (Figure  4-5),  temperature  profile downstream of the fire (Figure 4-6), velocity profile downstream of the fire (Figure 4-7), and smoke movement upstream of the fire (approximately 400 ft. in the tests). CFD model parameters are summarized in Table 4-1.

Figure 4-2: Memorial Tunnel test results, cross section averaged (bulk) flow rate along tunnel length [17].

<!-- image -->

Scatter plot

Figure 4-3: Memorial Tunnel test results, cross section averaged (bulk) temperature along tunnel length [17].

<!-- image -->

Scatter plot

Figure 4-4: Memorial Tunnel test results, temperature 203 ft. upstream of the fire [17].

<!-- image -->

Scatter plot

Figure 4-5: Memorial Tunnel test results, velocity 203 ft. upstream of the fire [17].

<!-- image -->

Scatter plot

<!-- image -->

Scatter plot

Figure 4-6: Memorial Tunnel test results, temperature 217 ft. downstream of the fire [17]. Table 4-1: Memorial Tunnel proposed CFD model parameters.

| ITEM                               | VALUE                                                                                                                                                                                                                                                                                                                                                                                                     |
|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Grid                               | Nominal grid resolution = 0.2 m, blockages are added upstream of the fire to catpure the 20% blockages due to measurement equipment, the grid is stepped to model the arched section, net CFD model area is 657 ft 2 , domain length is 300 m with sufficient upstream length modeled to capture the backlayering, grade is - 3.2%. Note that SI units are quoted as the FDS CFD software is in SI units. |
| Inlet boundary and outlet boundary | Inlet boundary condition = fixed velocity correpsonding to bulk velocity in the test, flow rate of 240 kcfm (113.4 m 3 /s), ambient temperature 53.5 deg F (12 deg C).                                                                                                                                                                                                                                    |
| FHRR                               | FHRR modeled is 78 MW, based on a surface area of 336 ft 2 (31 m 2 ) (adjusting for grid resolution, the net surface area is 30.96 m 2 ).                                                                                                                                                                                                                                                                 |
| FDS parameters                     | FDS defaults used except as noted - velocity tolerance for pressure solver = 0.075, settings for pressure solver (VN_MIN=0.3, VN_MAX=0.4, CFD_MIN=0.7, CFL_MAX=0.4).                                                                                                                                                                                                                                      |
| Fuel                               | The fuel is modeled in FDS to represent a typical polymer, with the chemical formula CH 1.8 N 0.05 O 0.3 and a soot yield of 0.131 and CO yield of 0.01. This is assumed to not have any major effect on backlayering or temperature and velocity prediction.                                                                                                                                             |
| Other                              | Sensitivity analysis to consider the impact of the grid resolution and turbulence model.                                                                                                                                                                                                                                                                                                                  |

Figure 4-7: Memorial Tunnel test results, velocity 217 ft. downstream of the fire [17].

<!-- image -->

Scatter plot

## 4.1.2.2  Tunnel Temperature with an FFFS Operating

The Singapore Land Transport Authority (LTA) conducted tests in the San Pedro de Anes Tunnel for large fires, representative of a HGV, with FFFS operating [8] (referred to herein as the "LTA" tests). The FFFS tests considered scenarios with a standard spray (pendant) sprinkler head, and a directional nozzle. A free burn (no FFFS) test was also conducted. Key parameters of the tunnel and tests include the following:

- The tunnel is 23.9 ft. (7.3 m) wide, 17.1 ft. (5.2 m) high, and 1968 ft. (600 m) long. The cross section is rectangular at the test section. A CFD model approximately 125 m long is proposed for this research. In the tests longitudinal ventilation was at 550 fpm to 590 fpm (2.8 m/s to 3 m/s).
- For this part of the validation, it is proposed to model Test 4. This scenario includes FFFS operating at 0.3 gpm/ft 2 (12 mm/min) using a standard (pendant) nozzle with activation at 400 seconds. The FHRR and temperature downstream of the fire were measured in the tests. Figure 4-8 shows the FHRR measured which is planned to be applied as a boundary condition in the models.
- For the FFFS configuration a total of 46 nozzles were used in the tests over a zone length of 164 ft. (50 m). Nozzles were arranged in three evenly spaced rows across the tunnel width and evenly spaced longitudinally within the zone of operation. The fire was (longitudinally) positioned in the center of the FFFS zone and on the tunnel centerline. Each nozzle covered an area of 96.8 ft 2 (9 m 2 ) with an operating pressure limited to 5 bar. At the water application rate  quoted,  this  equates  to  a  nozzle  flow  rate  of  28.5 gpm  (108 L/min)  and  a  K  factor  of 48 L/min/bar 1/2 . Nozzle parameters are discussed in further detail later in this section.
- For the CFD models a grid size is planned to be used as follows: 0.2 m in the longitudinal direction, 0.2 m in the width and vertical directions (SI units are quoted as this CFD software is in SI units). Rectangular tunnel geometry per the test geometry. Tunnel dimensions are to be rounded to the nearest 0.2 m to fit the grid resolution used.

- For the CFD models, FHRR set to vary with time based on the profile used in the original work. Figure 4-8 provides the FHRR profile. The fire load in the original test was comprised of wood pallets. The geometry of a pallet is such that features are smaller than can be resolved with  the  grid.  Given  that  detailed  combustion  processes  are  not  being  modeled  it  is  not necessary  to  model  the  pallet  geometry  in  detail.  Thus,  pallets  are  to  be  represented  as blocks, each having an area of 37.9 ft 2 (3.52 m 2 ), with a total of 30 pallets (three layers, two rows of five pallets per row). Pallets are assumed to all burn simultaneously in the model. A target (to assess fire spread) of wood pallets was included downstream of the main fire load for the testing and in the CFD model, but in the tests this target did not ignite and thus no FHRR was specified for this downstream target in the models. Figure 4-9 shows a typical fire geometry from a similar CFD model.
- Results to compare, based on published test data, include temperature data and heat flux downstream of the fire as per Figure 4-10 and Figure 4-11.
- Sensitivity  analysis  to  consider  the  impact  of  the  grid  resolution  and  turbulence  model parameters.
- Other  parameters  to  be  informed  from  the  outcome  of  analysis  are  discussed  in  Section 4.1.2.1.

Figure 4-8: Fire heat release rate profile with FFFS operating (LTA test 4) [8].

<!-- image -->

Line chart

Figure 4-9: Fire geometry for the LTA CFD model.

<!-- image -->

Icon

Figure 4-10: Test data, gas temperature downstream of the fire with FFFS (LTA test 4) [8].

<!-- image -->

Line chart

Figure 4-11: Test data, heat flux downstream of the fire with FFFS (LTA test 4) [8].

<!-- image -->

Line chart

Nozzle parameters (droplet size, spray pattern, model and manufacturer) were not published in the test data. The nozzle was a standard spray pendant with a flow rate of 108 L/min at a pressure up to 5 bar, giving a K factor of approximately 48 L/min/bar 1/2 . Manufacturer data and research publications are to be consulted to establish the approximate nozzle diameter and spray patterns as follows:

- Based on tests of similar nozzles (standard spray pendant) at similar pressures, a droplet diameter in the range of 0.5 mm to 1.2 mm is proposed [7].
- A typical  nozzle  spray  patterns  is  illustrated  in  Figure  4-12.  Based  on  the  nozzle  being  a standard spray pendant type, manufacturer data to be consulted to establish a spray pattern as informed by a nozzle with a similar K factor and flow rate (for example, a spray pattern is available for a standard coverage pendant nozzle with a K factor of 57 [20]).

Figure 4-12: Example nozzle spray pattern.

<!-- image -->

Engineering drawing

The FDS model for water droplets takes the following inputs in addition to nozzle flow rate and droplet  diameter:  PARTICLE  VELOCITY,  SPRAY  ANGLE,  PARTICLES\_PER\_SECOND, OFFSET and AGE [15]. An iterative process is planned, where the parameters listed here, as well as droplet diameter, are varied within credible ranges to match a typical nozzle spray pattern per manufacturer  data  for  a  selected  similar  nozzle.  Spray  pattern  is  planned  to  be  matched  by comparing the CFD model water delivery for a given location offset and distance below the nozzle with published test data.

Having matched the spray pattern as near as possible to test data, the CFD model with the fire are planned to be run and sensitivity to droplet diameter to be considered. Droplet diameter is the most important parameter to thermal environment prediction with the FFFS operating because it affects the rate of heat transfer from the hot gases to the water spray. Once an optimal droplet diameter  is  found,  the  spray  pattern  analysis  is  planned  to  be  checked  with  the  new  droplet diameter  to  determine  any  change  to  the  spray  pattern  relative  to  the  manufacturer  data.  If necessary, the other nozzle parameters (spray angles, velocity, etc.) are to be varied to better match the spray pattern, holding droplet diameter constant, and the CFD analysis for the fire scenario repeated. Once this process is complete, the calibrated nozzle parameters can be used going forward for other analyses.

## 4.1.2.3  Scale Model Tests - Prediction of Critical Velocity

Scale model tests were conducted by Li et al. to determine the critical velocity in a tunnel fire and an equation for the critical velocity was developed [19] [18] [13]. Figure 4-13 and Figure 4-14 provide the equations developed. This step of the validation exercise seeks to validate the ability of  the  CFD  model  to  predict  critical  velocity  (note  that  using  the  developed  equations  is  not mandatory)  and  it  is  proposed  to  compare  scale  results  versus  full-scale  results.  Table  4-2 provides the model parameters.

Table 4-2: CFD parameters for critical velocity validation based on tests by Li et al. [13].

| ITEM                         | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | SOURCE                                                   |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Cross section and length     | Square tunnel 0.25 m by 0.25 m, length of 12 m in small scale                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Corresponds to the scale tunnel type A in Li's work [13] |
| Fire and velocity scenario 1 | Propane burner on tunnel floor, 3.2 kW, critical velocity 0.57 m/s, ambient temperature 20 ° C. Using Froude number scaling (see Figure 4-15) and if the full-scale tunnel height is 8 m, the equivalent velocity and FHRR is 3.2 m/s and 18.5 MW respectively.                                                                                                                                                                                                                                                                                                                                                      | Corresponds to the scale tunnel type A in Li's work [13] |
| Fire and velocity scenario 2 | Propane burner on tunnel floor, 16.7 kW, critical velocity 0.67 m/s, ambient temperature 24.5 ° C Using Froude number scaling (see Figure 4-15) and if the full-scale tunnel height is 8 m, the equivalent velocity and FHRR is 3.8 m/s and 96.7 MW respectively.                                                                                                                                                                                                                                                                                                                                                    | Corresponds to the scale tunnel type A in Li's work [13] |
| Wall boundary conditions     | The test tunnel had a wall boundary condition corresponding to stainless steel with a thickness of 1 mm, with the backing exposed to ambient air. Material properties for the wall as follows: Density = 7,933 kg/m 3 Heat capacity = 0.46 kJ/kgK Conductivity = 19 W/mK Emissivity = 0.6 (type 301 stainless) Sensitivity to a concrete boundary condition to be tested for the full-scale models, with the wall having a thickness of 0.6 m (typical tunnel wall thickness). Materials properties proposed as follows: Density = 2,000 kg/m 3 Heat capacity = 0.88 kJ/kgK Conductivity = 1.4 W/mK Emissivity = 0.9 | [13] [21]                                                |
| Burner                       | A propane burner was used in the tests with a diameter of 100 mm; fire parameters are planned to be developed consistent with this                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | [13]                                                     |

April 2020

| CFD model parameters   | CFD models to be developed at small scale and at large scale. The same number of cells are to be used in each model, with 40 cells across the tunnel width and height (corresponds to 0.2 m grid size in full scale). Tunnel length to be modeled to be approximately 4 m long in small-scale, which corresponds to 128 m in full scale. Grid resolution is planned to be 0.2 m in the full-scale longitudinal direction and 0.00625 m in the small scale. The fire is planned to be placed at a location 2.5 m along the tunnel in small-scale and 80 m in full scale to enable backlayering to be observed. Grade of the models is 0% to match the test data. Inlet boundary condition = fixed velocity correpsonding to bulk velocity in the test, ambient correpsonding to test. In the tests the burner had a diameter of 100 mm, corresponding to an area of 0.00785 m 2 . A square burner is proposed to be modeled with dimensions 0.0875 m (area of 0.00765625 m 2 ). In full-scale the burner is to be kept the same, with dimensions factored by per the length scale (32 times larger). Sensitivity to the geometry of the burner (total area) to be considered (test a burner with twice the surface area). FDS defaults proposed except as noted - velocity tolerance for pressure solver = 0.075, settings for pressure solver (VN_MIN=0.3, VN_MAX=0.4, CFD_MIN=0.7, CFL_MAX=0.4). The fuel is modeled in FDS as propane to match the test   | Proposed parameters   |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| Critical velocity      | conditions. Computed per the test method where upstream temperature near the ceiling is used to indicate whether backlayering occurs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | [13]                  |
| Other                  | Sensitivity to grid resolution is planned to be tested on one case                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Proposed parameters   |

Figure 4-13: Equation. Critical velocity equation based on scale tunnel tests [19].

In Figure 4-13 symbols are as follows: Q * is the dimensionless heat release rate, Q is the fire heat release rate (kW), ρ o is  the  average density of the approach (upstream) air (kg/m 3 ), Cp is  the specific heat of air (kJ/kg/K), To is the ambient temperature (K), g is the acceleration due to gravity (m/s 2 ), H is the height of the tunnel (m), Vc * is the dimensionless critical velocity, and Vc is the critical velocity (m/s).

## Figure 4-14: Equation. Backlayering length derived from scale tunnel tests [19].

In Figure 4-14 symbols are as follows: H is the height of the tunnel (m), Lb is the backlayering length (m), L * b is the dimensionless backlayering length, Vcr is the critical velocity (m/s), and V is the air velocity in the tunnel (m/s).

## Figure 4-15: Equation. Scaling relationships [19].

In Figure 4-15 symbols are as follows: Fr is the Froude number, g is the acceleration due to gravity (m/s 2 ), l is length (m), Q is the heat release rate (kW), V is the ventilation velocity (m/s), and V ̇ is the  volumetric  flow  rate  in  (m 3 /s).  The  subscript F is  for  the  full-scale  facility  parameter;  the subscript M is for the model parameter.

## 4.1.2.4  Prediction of Critical Velocity with an FFFS Operating

The final part of the validation process involves checking the ability of the CFD model to predict backlayering  management  when  an  FFFS  is  operated.  The  equations  developed  by  Ko  and Hadjisophocleous [11] are proposed to be used for this purpose; refer to Figure 4-16. The model is planned to be based on the full-scale configuration described in Section 4.1.2.3 but now an FFFS is also modeled. A small-scale configuration is also to be considered in order to inform sensitivity to scaling. A shield is proposed to be placed over the fire geometry to prevent direct interaction  between  the  water  spray  and  the  fire.  Water  application  rates  of  6 mm/min  and 10 mm/min would be tested for an FHRR of 18.5 MW as this is within the range of validity of the equation (less than 40 MW), with smaller scale values computed per Figure 4-15.

Table 4-3: Model parameters for critical velocity and FFFS operating.

| ITEM                       | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | SOURCE                                                    |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| Cross section and length   | 8 m wide by 8 m high by 128 m long (SI units are typically quoted since the tunnel and testing, as well as CFD models, are in SI units)                                                                                                                                                                                                                                                                                                                                  | Full scale version of tunnel type A per Li's work [13]    |
| Fire and velocity scenario | FHRR of 3.2 m/s with no FFFS, and an FHRR of 18.5 MW, ambient temperature 20 ° C                                                                                                                                                                                                                                                                                                                                                                                         | Corresponds to the scale tunnel type A per Li's work [13] |
| Wall boundary conditions   | Concrete walls, refer to Section 4.1.2.3                                                                                                                                                                                                                                                                                                                                                                                                                                 | Proposed parameters                                       |
| FFFS arrangement           | Water application rate varies; 0.15 gpm/ft 2 (6 mm/min) and 0.25 gpm/ft 2 (10 mm/min), average droplet size 800 μ m, zone length 30 m, nozzles arranged on a grid with 4.4 m spacing in the longitudinal direction and 4.8 m in the tunnel width direction (two rows of nozzles symmetrically placed at 2 m from the tunnel centerline and 7 nozzles per row, with 4 m spacing). Nozzle water flow rate is varied to achieve desired water application rate to the zone. | Typical design values from projects                       |
| CFD model parameters       | In addition to parameters described here, refer to Section 4.1.2.3. Parameters for the nozzle DIAMETER, PARTICLE VELOCITY, SPRAY ANGLE, PARTICLES_PER_SECOND, OFFSET and AGE are to be informed by validation outcomes from Section 4.1.2.2, since the equation developed does not recognize droplet size as a significant parameter.                                                                                                                                    | Proposed parameters                                       |
| Critical velocity          | Computed per the test method where upstream temperature near the ceiling is used to indicate whether backlayering occurs                                                                                                                                                                                                                                                                                                                                                 | [13]                                                      |

Figure 4-16: Equation. Critical velocity with an FFFS operating [11].

In Figure 4-16 symbols are defined as follows: Cp is  the specific heat of air (kJ/kg/K), g is  the acceleration due to gravity (m/s 2 ), D is the hydraulic diameter of the tunnel (m), ρ o is the average density of the approach (upstream) air (kg/m 3 ), Q is the convective fire heat release rate (kW), Q' is the dimensionless heat release based on the tunnel hydraulic diameter, V'' is the dimensionless critical velocity without FFFS, To is the ambient temperature (K), V is the critical velocity without FFFS (m/s), VFFFS is  the  critical  velocity  accounting for  FFFS (m/s), and ω is  the  water  spray density (mm/min). The equation is valid up to a FHRR of 40 MW.

## 4.1.3 Prediction of Critical Velocity

The analysis should consider the impact of the FFFS on critical velocity over a range of different tunnel, fire and FFFS configurations as outlined in Table 4-4. Critical velocity to be determined iteratively  to  the  nearest  0.2 m/s  and  should  be  determined  by  temperature  and  visibility measurement near the tunnel ceiling. The basic model setup parameters (grid resolution, CFD software solver settings) to be determined by the outcomes of the validation study. Simulation iterations planned to be managed using an approach integrated with the DAKOTA software [22]. DAKOTA is a freely available package developed by Sandia National Labs. It is used to perform mathematical analysis tasks such as Monte Carlo analysis, genetic algorithm implementation and parameter studies.

Table 4-4: Critical velocity parameter study.

| PARAMETER                     | VALUE                                                                                                                                                                                                                                                                                           | NOTES / REFERENCE                                                                                                                                                                                                                                                                     |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tunnel geometry configuration | A = Memorial Tunnel B = 8 m by 8 m (scaled up version of critical velocity experiments referenced in Section 4.1.2.3 and referenced for completeness but not used in proposed parameter study) C = 30 m (wide) by 6 m high (like an overbuild of a highway, 5 or 6 lanes) D = San Pedro de Anes | Cross sections are selected to represent a spectrum of tunnels encountered in practice, refer to Figure 4-17, Figure 4-18, Figure 4-19 and Figure 4-20, with Figure 4-21 showing the typical fire geometry.                                                                           |
| FFFS - droplet size           | 200 μ m, 800 μ m, 1200 μ m (DV50)                                                                                                                                                                                                                                                               | Typical droplet diameters in FFFS applications ranging from water mist sizes to convention large drop sizes. The impact of these different parameters to be tested on tunnel type D only; tunnel types A and C to consider the 800 μ m result to verify that the behavior is similar. |
| FFFS - nozzle layout          | Zone length 30 m, nozzles arranged on a grid on the order of 4.4 m spacing in the longitudinal direction and 4.8 m in the tunnel width direction. Nozzle water flow rate is varied to achieve desired water application rate to the zone.                                                       | Typical design parameters                                                                                                                                                                                                                                                             |
| Water application rate        | 0, 2.5, 5, 10 mm/min                                                                                                                                                                                                                                                                            | Typical water application rates used in tunnel designs. The impact of these different parameters to be tested on tunnel type D only; tunnel types A and C to consider the 10 mm/min result to verify that the behavior is similar.                                                    |

| FHRR                              | 5 MW, 20 MW, 100 MW                                                                                             | Range of design FHRR values typically encountered in tunnel design. The impact of these different parameters to be tested on tunnel type D only; tunnel types A and C to consider the 20 MW result to verify that the behavior is similar.   |
|-----------------------------------|-----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fire geometry 1                   | Representative of a wood pallet pile with the top and ends shielded from the water spray                        | Refer Figure 4-21                                                                                                                                                                                                                            |
| Fire geometry 2 (no FFFS applied) | Fire at the tunnel floor with no blockage introduced                                                            | Used to check the influence of the wood pallet blockage representation (tunnel type D only)                                                                                                                                                  |
| Fire parameters                   | C = 1.0 H = 1.8 O = 0.3 N = 0.05 Soot yield = 0.131 g/g fuel CO yield = 0.010 g/g fuel Radiative fraction = 0.3 | The combined fire parameters represent a conservative soot yield combination for a vehicle, since they assume a predominantly polymer-based vehicle                                                                                          |

Figure 4-17: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A).

<!-- image -->

Engineering drawing

Figure 4-18: Square cross section for CFD analysis (ID B).

<!-- image -->

Engineering drawing

Figure 4-19: Rectangular cross section for CFD analysis (ID C).

<!-- image -->

Engineering drawing

Figure 4-20: Rectangular cross section for CFD analysis representing San Pedro de Anes tunnel at the fire site (ID D).

<!-- image -->

Engineering drawing

Figure 4-21: Heavy goods vehicle fire geometry.

<!-- image -->

Engineering drawing

Post-processing of results should seek to develop equations for critical velocity as a function of FHRR and water application rate. The method should use dimensionless velocity and FHRR like previous work [11] and seek to extend the applicability of the equation by Ko  and Hadjisophocleous to higher FHRRs (Figure 4-16). The reporting of the analysis should include a recommended  approach  to  CFD  modeling  to  determine  critical  velocity  when  an  FFFS  is operating.

## 4.1.4  List of Models and Outcomes

In summary, modeling for critical velocity is proposed to include the following:

## · Validation:

- Memorial  tunnel  tests:  Prediction  of  the  tunnel  environment  in  a  fire  with  longitudinal ventilation.
- LTA tunnel tests: Prediction of the tunnel environment in a fire with longitudinal ventilation and FFFS operating.
- Li's scale tunnel tests: Prediction of critical velocity.
- Ko and Hadjisophocleous tests: Prediction of critical velocity with an FFFS operating.

## · Investigation:

- Refer to Table 4-5 for a summary of the runs proposed.

Model  output  should  focus  on  the  smoke  control.  Additional  output  parameters  can  include adiabatic  surface  temperatures  (for  quantifying  the  degree  of  structural  protection  if  that information is desired in the future). Note that resistance to airflow (due to fire and FFFS) is not proposed to be processed from the models; that is planned to be measured as part of the testing program as modeling pressure loss in a tunnel due to fire has, in the author's experience, been problematic to predict with CFD.

The outcome of this modeling effort would include data for and development of an equation for the critical velocity as a function of FHRR and water application rate, and a validated and verified method to model tunnel fires using CFD to determine the critical velocity with FFFS.

Table 4-5: Critical velocity investigation - proposed analysis.

|   ID |   FHRR (MW) | TUNNEL GEOMETRY                     | FFFS DROP SIZE (MM)   |   WATER APPLICATION RATE (MM/MIN) | FIRE GEOMETRY                         | REMARKS                                                                                           |
|------|-------------|-------------------------------------|-----------------------|-----------------------------------|---------------------------------------|---------------------------------------------------------------------------------------------------|
|    1 |           5 | San Pedro de Anes cross section     | Not applicable        |                               0.0 | Wood pallet(s)                        | Cross section 7.3 m by 5.2 m                                                                      |
|    2 |           5 | As per model 1                      | 0.8                   |                               2.5 | Wood pallet(s)                        | As per model 1                                                                                    |
|    3 |           5 | As per model 1                      | 0.8                   |                               5.0 | Wood pallet(s)                        | As per model 1                                                                                    |
|    4 |           5 | As per model 1                      | 0.2                   |                               5.0 | Wood pallet(s)                        | As per model 1, test sensitivity to droplet size                                                  |
|    5 |           5 | As per model 1                      | 0.8                   |                              10.0 | Wood pallet(s)                        | As per model 1                                                                                    |
|    6 |          20 | As per model 1                      | Not applicable        |                               0.0 | Wood pallet(s)                        | As per model 1                                                                                    |
|    7 |          20 | As per model 1                      | 0.8                   |                               2.5 | Wood pallet(s)                        | As per model 1                                                                                    |
|    8 |          20 | As per model 1                      | 0.8                   |                               5.0 | Wood pallet(s)                        | As per model 1                                                                                    |
|    9 |          20 | As per model 1                      | 0.2                   |                              10.0 | Wood pallet(s)                        | As per model 1                                                                                    |
|   10 |          20 | As per model 1                      | 0.8                   |                               5.0 | Fire at the tunnel floor, no blockage | As per model 1, fire geometry sensitivity, consider two different fire areas to check sensitivity |
|   11 |          20 | Memorial Tunnel section, A          | 0.8                   |                               5.0 | Wood pallet(s)                        | Tunnel geometry sensitivity                                                                       |
|   12 |          20 | Cross section 30 m wide by 6 m high | 0.8                   |                               5.0 | Wood pallet(s)                        | Tunnel geometry sensitivity                                                                       |

|   13 |   100 | As per model 1   |   Not applicable |   0.0 | Wood pallet(s)   | As per model 1                                   |
|------|-------|------------------|------------------|-------|------------------|--------------------------------------------------|
|   14 |   100 | As per model 1   |              0.8 |   2.5 | Wood pallet(s)   | As per model 1                                   |
|   15 |   100 | As per model 1   |              0.2 |   2.5 | Wood pallet(s)   | As per model 1, test sensitivity to droplet size |
|   16 |   100 | As per model 1   |              0.8 |   5.0 | Wood pallet(s)   | As per model 1                                   |
|   17 |   100 | As per model 1   |              0.2 |   5.0 | Wood pallet(s)   | As per model 1, test sensitivity to droplet size |
|   18 |   100 | As per model 1   |              0.8 |  10.0 | Wood pallet(s)   | As per model 1                                   |
|   19 |   100 | As per model 1   |              0.2 |  10.0 | Wood pallet(s)   | As per model 1, test sensitivity to droplet size |
|   20 |   100 | As per model 1   |              1.2 |  10.0 | Wood pallet(s)   | As per model 1, test sensitivity to droplet size |

## 4.1.4.1  Data to Record in Models

The following data are to be recorded in the models:

- Fire heat release rate.
- Contour slices (temperature, velocity, gas concentrations, humidity).
- Wall temperature data (adiabatic surface temperature) to facilitate possible future investigations of the impact of FFFS on structural fire protection.
- Detailed data on water delivery including gas humidity and liquid water flux at solid surfaces.
- Point measurements (temperature and soot) are planned to be incorporated at the tunnel ceiling  to  facilitate  a  deterministic  computation  of  backlayering  length  as  a  function  of upstream velocity, and identification of critical velocity.

Uncertainty in the measurements to be quoted where possible based on test data or information provided for similar scenarios per the FDS Validation Guide [23].

## 4.2 Transverse Ventilation

Transverse ventilation systems utilize exhaust and supply ducts to control airflow in a tunnel. Many existing tunnels in the United States use a transverse ventilation system. Specific validation of CFD modeling for the transverse ventilation approach is not proposed because the validation for the critical velocity cases includes all the major physics: turbulent flow, heat transfer, FFFS modeling,  and  cooling  due  to  the  FFFS.  This  investigation  should  help  to  demonstrate  the approach to assessing different FFFS and EVS configurations. The principal hypotheses being investigated with this workplan are the same as those presented in 4.2.1:

- That FFFS and EVS can be integrated and EVS capacity optimized as a result of the cooling effects of the FFFS water spray.
- That CFD can be used to predict FFFS and EVS interaction, such that a CFD approach can be defined for use to verify the FFFS and EVS design integration for the most commonly used combinations of FFFS (small and large water droplet systems, varying water application rates and zone configurations) and EVS (transverse ventilation, single point exhaust, longitudinal ventilation) within a varying tunnel geometry (area, perimeter, height).

Relative to the above hypotheses, there are three aspects that arise for further investigation when a transverse ventilation system is used with FFFS:

1. Smoke management performance due to cooling of the combustion products.
2. Interaction between ventilation exhaust and the FFFS spray.
3. Pressure loss due to any pipework located in exhaust duct.

Pressure loss (item 3) is proposed to be determined as part of the testing program; this is a relatively easily measured quantity in a test. Smoke management and droplet entrainment can be considered further with CFD.

## 4.2.1 Transverse Ventilation Overview

A typical transverse ventilation system is shown in Figure 4-22, Figure 4-23, and Figure 4-24. The basic concept is to operate a combination of supply and exhaust fans to either: 1) Achieve a longitudinal velocity in  the  direction  of  vehicle  travel  when  in  unidirectional  traffic mode;  or  2) Minimize  longitudinal  velocity  and  exhaust  smoke  to  achieve  minimal  smoke  spread  when  in bidirectional traffic mode. The most challenging configuration for smoke management is operation to minimize smoke spread when the fire is placed near the exhaust duct bulkhead; in this mode of operation the longitudinal velocity is minimal and there exists the greatest potential for smoke spread. Figure 4-25 illustrates the concept.

Figure 4-22: Tunnel with transverse ventilation showing ducts.

<!-- image -->

Engineering drawing

<!-- image -->

Photograph

© WSP 2019

Figure 4-23: Photo of a tunnel with transverse ventilation.

<!-- image -->

Engineering drawing

Figure 4-24: Transverse ventilation system schematic.

<!-- image -->

Icon

Figure 4-25: Transverse ventilation system in exhaust near to the bulkhead.

## 4.2.2  Approach

Regarding  interaction  of  the  exhaust  and  FFFS  spray,  Figure  4-26  shows  the  concept.  This arrangement would occur when a retrofit operation uses the overhead duct to route FFFS branch pipes, and the nozzles are installed in the exhaust ports. Typical port dimensions and exhausts are as follows:

- 3 ft. wide and 0.33 ft. long.
- Exhaust rate on the order of 1.7 kcfm. per port (typical exhaust rate is 100 cfm/lane-ft. with 1 exhaust port every 20 ft. or 6 ports per lane per 100 ft.)

Figure 4-26: Interaction of water droplet and exhaust.

<!-- image -->

Photograph

## 4.2.3  List of Models and Outcomes

A  summary  of  models  proposed  for  the  transverse  system  is  provided  in  Table  4-6.  The parameters that are planned be investigated from the models include the amount of smoke spread (models 1 to 12) and the amount of water entrained into the duct (models 13 to 20). For models 21 to 36, variations of transverse ventilation schemes are tested; note that the final models may change slightly depending on outcomes of each individual model.

The outcome of this modeling effort aims to include data on the performance of a transverse ventilation system with an FFFS operating. Additional results would include a quantification of droplet entrainment into an exhaust flue for a typical configuration. The CFD methods used are to be based on the same techniques as those for critical velocity. Nozzle parameters would be per those derived from the validation exercise described in Section 4.1.2.2.

## 4.2.3.1  Data to Record in Models

The following data are to be recorded in the models:

- Fire heat release rate.
- Contour slices (temperature, velocity, gas concentrations, humidity).
- Contour slice of visibility obscuration due to soot in order to observe stratification.

- Wall temperature data (adiabatic surface temperature) to facilitate possible future investigations of the impact of FFFS on structural fire protection.
- Detailed data on water delivery including gas humidity and liquid water flux at solid surfaces.
- Point measurements (temperature and soot) are to be incorporated at the tunnel ceiling to facilitate  a  deterministic  computation  of  backlayering  length  and  identification  of  critical velocity.

Uncertainty  in  the  measurements  should  be  quoted  where  possible  based  on  test  data  or information provided for similar scenarios per the FDS Validation Guide [23].

Table 4-6: Transverse ventilation - proposed analysis.

|   ID |   FHRR (MW) | TUNNEL GEOMETRY TYPE               | FFFS DROP SIZE (MM)   | WATER APPLICATION RATE (MM/MIN)   | FIRE GEOMETRY   | REMARKS                                                                          |
|------|-------------|------------------------------------|-----------------------|-----------------------------------|-----------------|----------------------------------------------------------------------------------|
|    1 |           5 | San Pedro de Anes cross section, D | Not applicable        | Not applicable                    | Wood pallet(s)  | 100 cfm/lane foot exhaust rate, evenly distributed, cross section 7.3 m by 5.2 m |
|    2 |          20 | As per model 1                     | Not applicable        | Not applicable                    | Wood pallet(s)  | As per model 1                                                                   |
|    3 |         100 | As per model 1                     | Not applicable        | Not applicable                    | Wood pallet(s)  | As per model 1                                                                   |
|    4 |           5 | As per model 1                     | 0.8                   | 5.0                               | Wood pallet(s)  | As per model 1                                                                   |
|    5 |          20 | As per model 1                     | 0.8                   | 5.0                               | Wood pallet(s)  | As per model 1                                                                   |
|    6 |          20 | As per model 1                     | 0.2                   | 5.0                               | Wood pallet(s)  | As per model 1, test sensitivity to droplet size                                 |
|    7 |          20 | As per model 1                     | 0.8                   | 2.5                               | Wood pallet(s)  | As per model 1, water application rate sensitivity                               |
|    8 |          20 | As per model 1                     | 0.8                   | 10.0                              | Wood pallet(s)  | As per model 1                                                                   |
|    9 |          20 | As per model 1                     | 0.2                   | 2.5                               | Wood pallet(s)  | As per model 1, water application rate and droplet size                          |
|   10 |          20 | As per model 1                     | 0.8                   | 5.0                               | Wood pallet(s)  | As per model 1, reduce exhaust rate by 30%                                       |
|   11 |         100 | As per model 1                     | 0.8                   | 5.0                               | Wood pallet(s)  | As per model 1                                                                   |
|   12 |         100 | As per model 1                     | 0.8                   | 5.0                               | Wood pallet(s)  | As per model 1, reduce exhaust rate by 30%                                       |
|   13 |           0 | Single exhaust port                | 0.2                   | 2.5                               | Not applicable  | Cold flow case, 1700 cfm per port, port 3 ft. by 0.33 ft.                        |
|   14 |           0 | As per model 13                    | 0.8                   | 5.0                               | Not applicable  | As per model 13                                                                  |

|   15 |   0 | As per model 13     | 1.2            | 10.0           | Not applicable   | As per model 13                                                                                                                                            |
|------|-----|---------------------|----------------|----------------|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   16 |   0 | As per model 13     | 0.2            | 2.5            | Not applicable   | As per model 13                                                                                                                                            |
|   17 |   0 | As per model 13     | 0.8            | 5.0            | Not applicable   | As per model 13                                                                                                                                            |
|   18 |   0 | As per model 13     | 1.2            | 10.0           | Not applicable   | As per model 13                                                                                                                                            |
|   19 |   0 | As per model 13     | 0.8            | 5.0            | Not applicable   | Port dimension now 6 ft. by 0.33 ft. with same exhaust rate                                                                                                |
|   20 |   0 | Single exhaust port | 0.8            | 5.0            | Not applicable   | Port dimension now 1 ft. by 0.33 ft. with same exhaust rate                                                                                                |
|   21 | 100 | As per model 1      | Not applicable | Not applicable | Wood pallet(s)   | Point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent                                                     |
|   22 | 100 | As per model 1      | 0.8            | 6.0            | Wood pallet(s)   | As per model 21                                                                                                                                            |
|   23 | 100 | As per model 1      | Not applicable | Not applicable | Wood pallet(s)   | Exhaust configuration sensitivity, point exhaust system, 2 extract points downstream on side wall, exhaust rate 100 cfm/lf equivalent                      |
|   24 | 100 | As per model 1      | 0.8            | 6.0            | Wood pallet(s)   | As per model 23                                                                                                                                            |
|   25 | 100 | As per model 1      | Not applicable | Not applicable | Wood pallet(s)   | Exhaust flow rate sensitivity, point exhaust system, 2 extract points downstream at ceiling level, magnitude of exhaust to be informed by model 21 results |
|   26 | 100 | As per model 1      | 0.8            | 6.0            | Wood pallet(s)   | As per model 25                                                                                                                                            |
|   27 |  40 | As per model 1      | Not applicable | Not applicable | Wood pallet(s)   | FHRR sensitivity, point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent                                   |
|   28 |  40 | As per model 1      | 0.8            | 6.0            | Wood pallet(s)   | As per model 27                                                                                                                                            |

|   29 |   40 | As per model 1   | 0.8            | 12.0           | Wood pallet(s)   | Water application rate sensitivity, point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent   |
|------|------|------------------|----------------|----------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|   30 |   40 | As per model 1   | 0.8            | 3.0            | Wood pallet(s)   | Water application rate sensitivity, point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent   |
|   31 |   40 | As per model 1   | 0.5            | 6.0            | Wood pallet(s)   | Water droplet diameter sensitivity, point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent   |
|   32 |   40 | As per model 1   | 1.2            | 6.0            | Wood pallet(s)   | Water droplet diameter sensitivity, point exhaust system, 2 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent   |
|   33 |  100 | As per model 1   | Not applicable | Not applicable | Wood pallet(s)   | Multiple exhaust sensitivity, point exhaust system, 4 extract points downstream at ceiling level, exhaust rate 100 cfm/lf equivalent         |
|   34 |  100 | As per model 1   | 0.8            | 6.0            | Wood pallet(s)   | As per model 33                                                                                                                              |
|   35 |   40 | As per model 1   | Not applicable | Not applicable | Wood pallet(s)   | FHRR sensitivity, otherwise as per model 33                                                                                                  |
|   36 |   40 | As per model 1   | 0.8            | 6.0            | Wood pallet(s)   | FHRR sensitivity, otherwise as per model 33                                                                                                  |

## 4.3 Areas for Further (Future) Consideration

The following list of items are additional areas for discussion and possible investigation:

- Fire dynamics model of fire spread:
- The HRR for the primary fire would be based on a free burn tunnel test [24]. A target would be placed downstream of the primary fire and the target would represent a pile of wooden pallets. The primary fire would be unaffected by the FFFS but fire spread to the target

downstream would be impacted. These models would enable verification of the ability of a given FFFS to prevent fire spread, with the influence of ventilation rate included.

- Reduced water application rates could be modeled relative to the test, with no reduction in FHRR of the primary fire. The testing program would help to develop a more realistic FHRR at lower water application rates.
- Liquid fuels:
- This is an area of development and specific analyses are not proposed at present but could be considered further.
- Alternative energy carriers:
- This is an area of development and specific tests are not proposed at present but could be considered further.

## 5 LABORATORY AND FULL-SCALE TESTING WORKPLANS

The laboratory and full-scale testing workplans are comprised of tests to help verify data from the computer modeling tests. Principal hypotheses being investigated with this workplan remain as per the computer modeling hypotheses, repeated below.

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized as a result  of  the  cooling  effects  of  the  FFFS  water  spray.  This  hypothesis  can  be  verified  via measurement of the critical velocity for smoke control, pressure loss due to the FFFS water spray and impact of the EVS on water delivery. If the hypothesis is true, then the critical velocity should decrease due to the cooling. Additional airflow resistance introduced by the FFFS spray should be negligible with respect to other airflow resistance in the tunnel from items such as vehicles, wall friction, buoyancy, fire and external wind. Finally, the EVS should not cause excessive water droplet drift as to cause a negative effect on water droplet delivery to the fire zone.

The second hypothesis is that CFD can be used to predict FFFS and EVS interaction, such that a CFD approach can be defined for use to verify the FFFS and EVS design integration for the most commonly used combinations of FFFS (small and large water droplet systems, varying water application rates and zone configurations) and EVS (transverse ventilation, single point exhaust, longitudinal ventilation) within a varying tunnel geometry (area, perimeter, height). This hypothesis is to be verified via computer modeling proposed herein.

## 5.1 Laboratory-Scale Testing Workplan

Laboratory tests are proposed to better understand the interaction between longitudinal EVS and the FFFS. The tests are structured toward verifying critical velocity, providing a measure of the resistance that the FFFS creates to longitudinal flow, and providing data for CFD model validation.

## 5.1.1 General Information

Table 5-1 provides general information on the model scale tests including facility information, scheduling, and approximate costs.

Table 5-1: Proposed laboratory-scale testing general information.

| ITEM                                       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Testing location                           | IFAB's fire testing laboratory; Faßberg, Germany                                                                                                                                                                                                                                                                                                                                            |
| Testing facility and equipment suggestions | Previous experience testing water-based fixed firefighting systems, and their application to vehicle fires. Applicable standards and certifications: ISO/IEC 17025: General standards for the competence of testing and calibration laboratories, NFPA 502: Standard for Road Tunnels, Bridges, and Other Limited Access Highways, NFPA 750: Standard on Water Mist Fire Protection Systems |
| Staff                                      | Previous experience testing water-based fixed firefighting systems, and their application to vehicle fires                                                                                                                                                                                                                                                                                  |
| Cost estimate                              | Order of magnitude: $100,000 to $200,000 Cost is highly dependent on type and number of tests                                                                                                                                                                                                                                                                                               |
| Schedule                                   | 3-6 months before tests - agree on testing protocol 3-4 weeks before tests - test setup and calibration begin Testing occurs for 1 week                                                                                                                                                                                                                                                     |
| Model scale                                | Scale is 1:4 Translates to 2.5 m x 1.25 m x 12.0 m                                                                                                                                                                                                                                                                                                                                          |
| Test setup                                 | Scale tunnel with FFFS nozzles installed Fan installed at one end to provide longitudinal ventilation Fire source is a shielded wood pallet mock up                                                                                                                                                                                                                                         |
| Instrumentation                            | Needed to measure temperature, heat flux, FFFS water pressure, air velocity, static pressure along tunnel, relative humidity, gas concentrations (CO, CO 2 , O 2 ), visuals                                                                                                                                                                                                                 |

## 5.1.2  Test Procedures

The scale test tunnel is proposed to be developed to allow fires with and without FFFS operation under longitudinal ventilation. Table 5-2 and Table 5-3 outline the model scale tests to be run, including a brief description of the test setup as well as the objectives. Detailed procedures of these tests are planned to be produced by IFAB once the general testing outline is agreed upon. The final details of the tests are to be adjusted based on outcomes of the CFD modeling, which is  planned  to  take  place  before  the  tests.  Some  details  that  are  to  be  considered  include temperature monitoring (for structural safety), goals of the FFFS being tested (suppress, cool, etc.), and shielding of the fire from the water spray (depending on whether a specific FHRR is desired). Calibration pre-tests in addition to those listed below is expected and would occur during the test setup phase.

The following parameters are proposed to be measured and recorded during all tests:

- Temperature (including at varying longitudinal locations to help determine backlayering length as a function of upstream velocity)
- Adiabatic surface (plate) temperature to provide data for future structural considerations when FFFS are factored in
- Heat flux
- Water pressure in the FFFS

- Flow rate in the FFFS
- Air velocity
- Static pressure along tunnel
- Relative air humidity
- Material humidity (wooden pallets) (where possible to do so; a consistent drying procedure might be all that is possible on this aspect)
- Gas concentrations (O2, CO, CO2)
- Visual (video and thermal) recording

The heat release rate is planned to be calculated by measuring the oxygen consuption of the fire and correlating it to the energy released by the fire.

Uncertainty in test data is planned to be quantified where it is possible to do so via measurement accuracy information and calibration.

Five tests are proposed as follows:

- Test 1: Cold flow tests to establish pressure loss in the tunnel due to wall friction and FFFS pipework.
- Test 2: Cold flow tests with pipework arranged in the tunnel in a manner analogous to how pipework would be arranged in an exhaust duct for a transverse ventilation system; purpose is to confirm analytical sums for the airflow resistance due to the pipework.
- Test 3: Free burn test with longitudinal ventilation; establish critical velocity with no FFFS operating.
- Test  4:  As  per  test  3  but  with  FFFS  operating;  data  point  for  critical/confinement  velocity computation.
- Test 5: As per test 4, but with upstream velocity varied.

Nozzles for the tests are to be selected during the detailed design of the test procedures. Nozzles can be an important factor in the performance of an FFFS [25]. Full nozzle characterization, such as droplet size distributions and spray patterns are not always available. It is usually possible to obtain at least the nozzle K factor and spray pattern but not always the droplet size distribution [20] (see also Section 4.1.2.2). A nozzle is to be selected for characterization for laboratory and full-scale testing based on the following factors:

- Application  in  U.S.  tunnels,  a  nozzle  that  is  approved  and  listed  for  the  application  per NFPA 13, if possible.
- Availability of K-factor and spray pattern data.
- Availability  of  droplet  size  distribution  or  similarity  of  the  nozzle  to  others  where  size distribution is available.

- Laboratory-scale versus full-scale availability noting that one key aspect of the testing is to compare  laboratory-scale  with  full-scale  nozzles  (e.g.,  can  a  3D  model  of  the  nozzle  be obtained to enable 3D printing for laboratory-scale versions of the nozzle).

Nozzle  characterization  for  one  selected  nozzle  type  is  proposed  via  imaging  techniques described in literature [7]. Details of this test and nozzle are to be determined. The goals of the test  are  to  measure  the  nozzle's  droplet  size  distribution  and  the  nozzle's  spray  pattern.  The necessary data may already be available and if that is the case, then these tests would most likely not be needed.

Table 5-2: List of laboratory-scale tests specified and full-scale equivalents (calculated per Figure 4-15).

| ID   | NOTES                | PURPOSE                                       |   MODEL FHRR (MW) | MODEL INLET V (M/S)   |   MODEL WATER RATE Q W (MM / MIN) |   MODEL DROP SIZE D W (MM) |   MODEL FFFS ZONE (M) |   FULL- SCALE FHRR (MW) | FULL- SCALE V (M/S)   |   FULL- SCALE WATER RATE Q W (MM / MIN) |   FULL- SCALE DROP SIZE D W (MM) |   FULL- SCALE FFFS ZONE (M) |
|------|----------------------|-----------------------------------------------|-------------------|-----------------------|-----------------------------------|----------------------------|-----------------------|-------------------------|-----------------------|-----------------------------------------|----------------------------------|-----------------------------|
| 1a   | Cold flow            | Measure friction: walls, no pipework, no FFFS |                 0 | 1.5 and 2.5           |                                 0 |                          0 |                     5 |                     0.0 | 3.0 and 5.0           |                                     0.0 |                              0.0 |                        20.1 |
| 1b   | Cold flow            | Measure friction: walls, pipework, no FFFS    |                 0 | 1.5 and 2.5           |                                 0 |                          0 |                     5 |                     0.0 | 3.0 and 5.0           |                                     0.0 |                              0.0 |                        20.1 |
| 1c   | Cold flow            | Measure friction: walls, pipework, FFFS       |                 0 | 1.5 and 2.5           |                                 3 |                        0.4 |                     5 |                     0.0 | 3.0 and 5.0           |                                     6.0 |                              0.8 |                        20.1 |
| 2    | Cold flow            | Measure friction: distributed pipework        |                 0 | 1.5 and 2.5           |                                 0 |                          0 |                     5 |                     0.0 | 3.0 and 5.0           |                                     0.0 |                              0.0 |                        20.1 |
| 3    | Fire case, free burn | Free burn FHRR measurement                    |               3.5 | 1.5                   |                                 0 |                          0 |                     5 |                   113.2 | 3.0                   |                                     0.0 |                              0.0 |                        20.1 |
| 4    | Fire case, FFFS on   | FFFS impact on FHRR and critical v            |               3.5 | To be based on CFD    |                                 3 |                        0.4 |                     5 |                   113.2 | To be based on CFD    |                                     6.0 |                              0.8 |                        20.1 |
| 5    | Fire case, FFFS on   | FFFS impact on FHRR and critical v            |               3.5 | To be based on CFD    |                                 3 |                        0.4 |                     5 |                   113.2 | To be based on CFD    |                                     6.0 |                              0.8 |                        20.1 |

Table 5-3: Model scale test procedures.

| ID   | DESCRIPTION                               | OTHER SET-UP PARAMETERS                                                                                                           | KEY MEASUREMENTS                                                                                                                             | PROCEDURES, CALCULATIONS                                                                                                                                                                                                              |
|------|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1a   | Cold flow                                 | No obstructions, no pipes inside the tunnel                                                                                       | Static pressure at pressure taps distributed along test tunnel length (10 evenly spaced). Bulk velocity in the tunnel as a function of time. | Run fans to achieve steady state flow, record velocity and pressure measurements. Shut down the fans, record velocity decay as a function of time. Compute tunnel friction factor via Bernoulli equation and velocity decay equation. |
| 1b   | Cold flow                                 | Include pipes for the FFFS inside the tunnel                                                                                      | As above                                                                                                                                     | As above                                                                                                                                                                                                                              |
| 1c   | Cold flow                                 | Include pipes for the FFFS inside the tunnel, operate FFFS                                                                        | As above, plus measure humidity                                                                                                              | As above                                                                                                                                                                                                                              |
| 2    | Cold flow                                 | Include pipes for FFFS, evenly spaced at 5 m across width of tunnel (represents pipework in a duct - a transverse vent system)    | Static pressure at pressure taps distributed along test tunnel length (10 evenly spaced). Bulk velocity in the tunnel as a function of time. | As above                                                                                                                                                                                                                              |
| 3    | Fire case, free burn                      | Wood pallet mock- up, free burn test, shielded fire                                                                               | FHRR. All measurements as noted in the main report (velocity, temperature, pressure, etc.).                                                  | Blank                                                                                                                                                                                                                                 |
| 4    | Fire case, FFFS operating                 | Wood pallet mock- up, FFFS test, shielded fire                                                                                    | FHRR. All measurements as noted in the main report (velocity, temperature, pressure, etc.).                                                  | Blank                                                                                                                                                                                                                                 |
| 5    | Fire case, FFFS operating                 | Wood pallet mock- up, FFFS test, shielded fire                                                                                    | FHRR. All measurements as noted in the main report (velocity, temperature, pressure, etc.).                                                  | Blank                                                                                                                                                                                                                                 |
| 6    | Nozzle characterization (to be confirmed) | Imaging techniques similar to those reported in previous research [7] to be applied (if needed) to characterize nozzle parameters | Water droplet sizes, water spray distribution                                                                                                | Imaging techniques similar to those reported in previous research [7] to be applied (if needed) to characterize nozzle parameters                                                                                                     |

## 5.1.3 Evaluation of Results

A comprehensive report for the scale model testing is planned to be developed inclusive of video footage capturing the effect of the FFFS. The scale model test results should be compared with computer models from Task 3. The exact comparison is going to depend on testing outcomes and how they compare with the models.

Tests 1 and 2 are proposed to be used to evaluate the differences between ventilation only and ventilation with FFFS operating for cold flow scenarios (pressure losses). Tests 3 and 4 are also proposed to be used to evaluate the differences between ventilation only and ventilation with FFFS using the fire scenario.

## 5.2 Full-Scale Testing

The full-scale testing is proposed to be performed in the San Pedro de Anes Tunnel test facility located in Spain. The proposed fire fuel load is a heavy goods vehicle mockup using wood pallets. Table 5-4 provides general information on the model scale tests including facility information, scheduling, and approximate costs.

Note that the full-scale testing aspect of this research is the least certain area of investigation post-workshop. The plan may be revisited once computer modeling and laboratory-scale testing findings are available. This part of the workplan is therefore at a preliminary stage.

Table 5-4: Full-scale testing general information.

| ITEM                                       | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                                                 |
|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Testing location                           | San Pedro de Anes Tunnel; Asturias, Spain                                                                                                                                                                                                                                                                                                                                                   |
| Testing facility and equipment suggestions | Previous experience testing water-based fixed firefighting systems, and their application to vehicle fires. Applicable standards and certifications: ISO/IEC 17025: General standards for the competence of testing and calibration laboratories, NFPA 502: Standard for Road Tunnels, Bridges, and Other Limited Access Highways, NFPA 750: Standard on Water Mist Fire Protection Systems |
| Staff                                      | Previous experience testing water-based fixed firefighting systems, and their application to vehicle fires Staff should coordinate with local agencies for testing, including local fire department                                                                                                                                                                                         |
| Cost estimate                              | Order of magnitude: $500,000 - $1,000,000 Cost is highly dependent on type and number of tests                                                                                                                                                                                                                                                                                              |
| Schedule                                   | 5 months before tests - preparatory work begins 5 weeks before tests - test setup and calibration begin Testing occurs for 1 week                                                                                                                                                                                                                                                           |
| Tunnel dimensions                          | 7.3 m wide, 5.2 m high, 600 m long (at test section)                                                                                                                                                                                                                                                                                                                                        |
| Test setup                                 | Setup follows SOLIT Annex 7 test protocol [26] (following this protocol is voluntary) FFFS installed to provide 0.15 gpm/ft 2 Fire source is a heavy goods vehicle (HGV) with potential HRR of 150 MW Fans provide longitudinal ventilation                                                                                                                                                 |
| Instrumentation                            | Needed to measure temperature, heat flux, FFFS water pressure, air velocity, static pressure along tunnel, relative humidity, gas concentrations (CO, CO 2 , O 2 ), visuals.                                                                                                                                                                                                                |

## 5.2.1  Test Procedures

The test configuration is planned to be developed to simulate a heavy goods vehicle with a solid fuel load. A water application rate of 0.15 gpm/ft 2 is proposed since this is at the lower end of the range of water application rates used in the United States. The fuel load is proposed to have a potential peak heat release rate of 150 MW. Although, activation of the FFFS is proposed to limit the fire from reaching its peak HRR during the tests.

The planned full-scale fire test would follow an existing public test protocol for full-scale tunnel fire tests, SOLIT Annex 7: Fire Tests and Fire Scenarios for Evaluation of FFFS [26]. This protocol specifies the fire load and necessary measurement systems. The proposed tests are listed in Table 5-5 and Table 5-6. Detailed procedures for these tests would be produced once the general testing outline is agreed upon. Some details to be considered include temperature monitoring (for structural safety), goals of the FFFS being tested (suppress, cool, etc.), and shielding of the fire from the water spray (depending on whether a specific FHRR is desired or a physical process, such as water spray cooling, needs to be isolated).

The following parameters are planned to be measured and recorded during all tests:

- Temperature (including at varying longitudinal locations to help determine backlayering length as a function of upstream velocity)
- Adiabatic surface (plate) temperature to provide data for future structural considerations when FFFS are factored in
- Heat flux
- Water pressure in the FFFS
- Flow rate in the FFFS
- Air velocity (in tunnel)
- Static pressure along tunnel
- External wind speed
- Relative air humidity
- Material humidity (wooden pallets) (where possible to do so; a consistent drying procedure might be all that is possible on this aspect)
- Gas concentrations (O2, CO, CO2)
- Visual (video and thermal) recording
- Fan power consumption and fan thrust

The heat release rate is planned to be calculated by measuring the oxygen consuption of the fire and correlating it to the energy released by the fire. Figure 5-1 through Figure 5-3 show example full-scale test setups from the SOLIT2 tests.

Uncertainty  in  test  data  should  be  quantified  where  it  is  possible  to  do  so  via  measurement accuracy information and calibration.

<!-- image -->

Engineering drawing

© 2012 SOLIT2

Figure 5-1: Schematic of test setup.

<!-- image -->

Engineering drawing

Figure 5-2: Example measurement locations.

<!-- image -->

Photograph

© 2012 SOLIT2

Figure 5-3: HGV mock up without shielding.

Table 5-5: List of full-scale tests specified and laboratory-scale equivalents (calculated per Figure 4-15).

| SERIES   | DESCRIPTION               | PURPOSE                                       |   FULL- SCALE FHRR (MW) | FULL- SCALE V (M/S)   |   FULL- SCALE Q W (MM / MIN) |   FULL- SCALE D W (MM) |   FULL- SCALE FFFS ZONE LENGTH (M) |   MODEL FHRR (MW) | MODEL INLET V (M/S)   |   MODEL WATER RATE Q W (MM / MIN) |   MODEL DROP SIZE D W (MM) |   MODEL FFFS ZONE LENGTH (M) |
|----------|---------------------------|-----------------------------------------------|-------------------------|-----------------------|------------------------------|------------------------|------------------------------------|-------------------|-----------------------|-----------------------------------|----------------------------|------------------------------|
| 1a       | Cold flow                 | Measure friction: walls, no pipework, no FFFS |                     0.0 | 3.0 and 5.0           |                          0.0 |                    0.0 |                                0.0 |               0.0 | 1.5 and 2.5           |                               0.0 |                        0.0 |                          0.0 |
| 1b       | Cold flow                 | Measure friction: walls, pipework, no FFFS    |                     0.0 | 3.0 and 5.0           |                          0.0 |                    0.0 |                               30.0 |               0.0 | 1.5 and 2.5           |                               0.0 |                        0.0 |                          7.5 |
| 1c       | Cold flow                 | Measure friction: walls, pipework, FFFS       |                     0.0 | 3.0 and 5.0           |                          6.0 |                    0.8 |                               30.0 |               0.0 | 1.5 and 2.5           |                               3.0 |                        0.4 |                          7.5 |
| 2        | Fire case, FFFS operating | FFFS impact on FHRR and critical v            |                   113.2 | 3.0                   |                          6.0 |                    0.8 |                               30.0 |               3.5 | 1.5                   |                               3.0 |                        0.4 |                          7.5 |

Table 5-6: Full-scale test procedures.

| SERIES   | DESCRIPTION               | OTHER SET-UP PARAMETERS                                    | KEY MEASUREMENTS                                                                                                                                                      | PROCEDURES, CALCULATIONS                                                                                                                                                                                                              |
|----------|---------------------------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1a       | Cold flow                 | No obstructions, no pipes inside the tunnel                | Static pressure at pressure taps distributed along test tunnel length (10 evenly spaced). Bulk velocity in the tunnel as a function of time. Jet fan operation state. | Run fans to achieve steady state flow, record velocity and pressure measurements. Shut down the fans, record velocity decay as a function of time. Compute tunnel friction factor via Bernoulli equation and velocity decay equation. |
| 1b       | Cold flow                 | Include pipes for the FFFS inside the tunnel               | As above.                                                                                                                                                             | As above.                                                                                                                                                                                                                             |
| 1c       | Cold flow                 | Include pipes for the FFFS inside the tunnel, operate FFFS | As above, also measure humidity.                                                                                                                                      | As above. Reverse engineer 1D spreadsheet calculation to determine FFFS impact.                                                                                                                                                       |
| 2        | Fire case, FFFS operating | Wood pallet mock-up, FFFS test, shielded fire              | FHRR. All measurements as noted in the main report (velocity, temperature, pressure, etc.).                                                                           | Fire test case, operate at an upstream velocity expected to control smoke based on CFD. Reverse engineer 1D spreadsheet calculation to determine FFFS and fire impact.                                                                |

## 5.2.2 Evaluation of Results

A  report  for  the  full-scale  tests  is  planned  to  be  developed  following  completion  of  the  tests. Results should be compared with scale model tests. Full-scale test results should be compared with laboratory-scale results and computer model results per the models outlined for Task 3. The exact comparison is going to depend on testing outcomes and how they compare with the models.

Table 5-7 summarizes the model scale tests, the corresponding validation that is planned for using the results, and the knowledge gap each test addresses. Note that tests 1b and 1c should be used to evaluate the differences between ventilation only and ventilation with FFFS operating for cold flow scenarios.

Table 5-7: Evaluation of full-scale test results.

| TEST NO. AND DESCRIPTION                                  | VALIDATION                                                                                                                                              | KNOWLEDGE GAP                                                                                                                                                                                                                                                                |
|-----------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1a - cold flow, no obstructions                           | Calculate pressure loss through the tunnel - compare to hand calculations                                                                               | Test is to establish a base result.                                                                                                                                                                                                                                          |
| 1b - cold flow, pipework added (longitudinal ventilation) | Calculate pressure loss through the tunnel - compare to hand calculations                                                                               | What is the impact of FFFS pipework on the tunnel friction factor, determine how good hand calculations estimate this?                                                                                                                                                       |
| 1c - cold flow, FFFS activated                            | Calculate pressure loss through the tunnel - compare to hand calculations                                                                               | What is the impact of FFFS spray on the longitudinal velocity achieved, determine how good hand calculations estimate this?                                                                                                                                                  |
| 2 - fire case, FFFS activated                             | Results evaluated against: the equations by Ko and Hadjisophocleous [11], the Carlotti et al. fire pressure drop equations [27], and CFD model results. | How well is the critical velocity predicted by existing equations when an FFFS is used, especially at larger FHRRs. How is the fire pressure drop affected by the FFFS? Can CFD predict the pressure drop and critical velocity? Impact of increased water vapor on airflow? |

## 5.3 Areas for Further (Future) Consideration

In  addition  to  items  noted  in  Section  4.3,  the  following  list  of  items  are  additional  areas  for discussion and possible investigation regarding testing:

- Water and fan interactions to quantify the impact of FFFS water spray on fan performance.
- Impact  of  the  FFFS  on  FHRR  for  varying  water  application  rates.  This  information  could provide input to an application-based water application rate chart like that in NFPA 13.

## 6 SUMMARY AND NEXT STEPS

Workplans incorporating workshop feedback have been developed for computer modeling and testing.  As  different  elements  of  the  workplans  are  completed,  the  scope  of  the  follow-on workplans  may  need  to  change  slightly  based  on  findings.  The  computer  modeling  task  is recommended for initial investigation. There are numerous tests that can be used for validation, the computer modeling exercise is the least expensive overall, and it can yield a lot of useful insights. Following computer modeling, the laboratory-scale work may be recommended to move forward, as this has less investment attached than a full-scale test. The final element may be fullscale  testing  with  the  scope  adjusted  if  necessary,  per  CFD  modeling  and  laboratory-scale outcomes.

The  outcome  of  the  computer  modeling  and  testing  efforts  is  planned  to  include  data  for development of an equation for the critical velocity as a function of FHRR and water application rate, or a reverification of the equation in Figure 4-16. Another outcome could be a validated and verified  method  to  model  tunnel  fires  using  CFD  with  FFFS  under  transverse  or  longitudinal ventilation, thus providing a basis for a designer to quantify the impact of FFFS on the EVS for most tunnel configurations encountered in the U.S. Finally, the research is anticipated to provide data related to the FFFS impact on airflows produced by the FFFS, notably the resistance to airflow introduced by water sprays and FFFS pipework.

A key component to the success of the research going forward is going to be maintenance of industry participation. At certain key steps along the process of conducting the work, conference calls  and/or  webinar  style  updates  may  be  conducted.  The  follow-on  steps  may  include  the following:

- Distribute the Workshop Report to participants, hold a post-workshop call/webinar to discuss workplan updates arising from the workshop.
- Subject to approval, execute the computer modeling task and produce a draft report.
- Hold a call/webinar to discuss and get feedback on computer modeling.
- Subject to approval, execute the laboratory-scale testing task and produce a draft report.
- Hold a call/webinar to discuss and get feedback on the laboratory-scale testing.
- Revisit the full-scale testing scope of work.
- Subject to approval, execute the full-scale testing work and produce the draft report.
- On completion of modeling and testing, develop the summary report.

## REFERENCES

- [1] 'Fixed Firefighting and Emergency Ventilation Systems - Literature Survey and Synthesis.' Federal Highway Administration, FWHA-HIF-20-016, 2019, [Online]. Available: https://www.fhwa.dot.gov/bridge/tunnel/pubs/nhi09010/fixed\_firefighting.pdf.
- [2] PIARC, Fixed Fire Fighting Systems in Road Tunnels: Current Practices and Recommendations . Permanent International Association of Road Congresses, Technical Committee on Road Tunnel Operation, 3.3, 2016.
- [3] FHWA, 'Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Literature Survey and Synthesis.' 2020.
- [4] 'SOLIT2 Report, Engineering Guidance for Fixed Fire Fighting Systems in Tunnels,' 2012.
- [5] 'NFPA 502 Standard for Road Tunnels, Bridges and Other Limited Access Highways 2017.' NFPA, 2017.
- [6] M. H. Raddum and R. Mellum, 'Public Investigation of Fire in Tank Trailer in the Skatestraum Tunnel in Sogn og Fjordane County on 15th of July 2015,' in Eighth International Symposium on Tunnel Safety and Security , 2018, pp. 132-145.
- [7] D. T. Sheppard, 'Spray Characteristics of Fire Sprinklers,' PhD Thesis, Northwestern University, 2002.
- [8] M. K. Cheong, W. O. Cheong, K. W. Leong, A. D. Lemaire, and L. M. Noordijk, 'Heat Release Rate of Heavy Goods Vehicle Fire in Tunnels with Fixed Water Based FireFighting System,' Fire Technology , vol. 50, no. 2, pp. 249-266, 2014.
- [9] 'Sprinkler Spray Patterns (Tyco).' Tyco, 2018.
- [10] Q. Guo, K. J. Root, A. Carlton, S. E. Quiel, and C. J. Naito, 'Framework for Rapid Prediction of Fire-Induced Heat Flux on Concrete Tunnel Liners with Curved Ceilings,' Fire Safety Journal , vol. 109, p. 102866, Oct. 2019, doi: 10.1016/j.firesaf.2019.102866.
- [11] Y. J. Ko and G. V. Hadjisophocleous, 'Study of Smoke Backlayering During Suppression in Tunnels,' Fire Safety Journal , vol. 58, pp. 240-247, 2013.
- [12] Y. Wu and M. Z. A. Bakar, 'Control of Smoke Flow in Tunnel Fires Using Longitudinal Ventilation Systems - A Study of the Critical Velocity,' Fire Safety Journal , pp. 363-390, 2000.
- [13] Y. Z. Li, B. Lei, and H. Ingason, 'Study of Critical Velocity and Backlayering Length in Longitudinally Ventilated Tunnel Fires,' Fire Safety Journal , vol. 45, pp. 361-370, 2010.
- [14] W. D. Kennedy, 'Critical Velocity Past, Present and Future,' in Independent Technical Conferences - Smoke and Critical Velocity in Tunnels , 1997, pp. 58-67.
- [15] 'Fire Dynamics Simulator (Version 6) User's Guide.' National Institute of Standards and Technology, 2019, Accessed: Jan. 18, 2019. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1019.pdf.
- [16] Bechtel - Parsons Brinckerhoff, 'Memorial Tunnel Fire Ventilation Comprehensive Test Report Volume 1.' Massachusetts Highway Department, 1995.
- [17] Bechtel - Parsons Brinckerhoff, 'Memorial Tunnel Fire Ventilation Test Program Phase IV Report.' Massachusetts Highway Department, 1999.
- [18] Y. Z. Li and H. Ingason, 'Effect of Cross Section on Critical Velocity in Longitudinally Ventilated Tunnel Fires,' Fire Safety Journal , vol. 91, pp. 303-311, 2017.
- [19] Y. Z. Li, H. Ingason, and L. Jiang, 'Influence of Tunnel Slope on Smoke Control,' RISE Research Institutes of Sweden, RISE Report 2018:50, 2018.

- [20] 'Sprinkler Spray Patterns.' Tyco, 2018.
- [21] J. Holman, Heat Transfer , 7th ed. 1990.
- [22] M. S. Eldred et al. , 'Dakota: A Multilevel Parallel Object-Oriented Framework for Design Optimization, Parameter Estimation, Uncertainty Quantification, and Sensitivity Analysis. Version 5.0, User's Manual,' SAND2010-2183, 991842, 2018. doi: 10.2172/991842.
- [23] 'Fire Dynamics Simulator (Version 6) Technical Reference Guide Volume 3 Validation.' National Institute of Standards and Technology, 2019, Accessed: Jan. 18, 2019. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1018.pdf.
- [24] H. Ingason, 'Large Scale Fire Tests with Fixed Fire Fighting System in Runehamar Tunnel,' SP Technical Research Institute of Sweden, SP Report 2014:32, 2014.
- [25] G. Tanner and K. Knasiak, 'Spray Characterization of Typical Fire Suppression Nozzles,' Third International Water Mist Conference , p. 16, 2003.
- [26] SOLIT2 Research Consortium, 'SOLIT2 Report, Annex 7, Fire Tests and Fire Scenarios for Evaluation of FFFS.' 2012.
- [27] P. Carlotti and P. Salizzoni, 'Pressure Drop Caused by a Fire in a Tunnel,' in 17th International Symposium of Aerodynamics Ventilation and Fire in Tunnels , 2017, pp. 363-371.