<!-- image -->

Logo

FIXED FIREFIGHTING AND EMERGENCY VENTILATION SYSTEMS FOR HIGHWAY TUNNELS - COMPUTER MODELING REPORT

<!-- image -->

Photograph

## Technical Report Documentation Page

| 1. Report No. FHWA-HIF-22-021                                                                                                                                                                                                                                                                                                                                 | 2. Government Accession No.                                                                                                | 3. Recipient's Catalog No. 5. Report Date January 2022                                        |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| 4. Title and Subtitle Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Computer Modeling Report                                                                                                                                                                                                                                    | 4. Title and Subtitle Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Computer Modeling Report |                                                                                               |
|                                                                                                                                                                                                                                                                                                                                                               |                                                                                                                            | 6. Performing Organization                                                                    |
| 7. Principal Investigator(s): Tuonglinh (Linh) Warren Bilson (WSP), Bill Connell 8. Performing Organization Report 9. Performing Organization WSP U.S.A, Inc. One Penn Plaza 250 West 34 th Street New York, NY, 10119 12. Sponsoring Agency Federal Highway Administration U.S. Department of 1200 New Jersey Avenue, Washington, DC 20590 15. Supplementary | Stephen Bartha (FHWA), Matt Emil Persson (WSP) Name and Address Address                                                    | 10. Work Unit No. (TRAIS) 11. Contract or Grant No. DTFH6114D00048 14. Sponsoring Agency Code |
| 13. Type of Report and Period Covered                                                                                                                                                                                                                                                                                                                         | 13. Type of Report and Period Covered                                                                                      |                                                                                               |

17. Key Words

9. Performing Organization Name and Address WSP U.S.A, Inc. One Penn Plaza 250 West 34 th  Street New York, NY, 10119 10. Work Unit No. (TRAIS) 11. Contract or Grant No. DTFH6114D00048 12. Sponsoring Agency Name and Address Federal Highway Administration U.S. Department of Transportation 1200 New Jersey Avenue, SE Washington, DC 20590 13. Type  of Report and Period Covered 14. Sponsoring Agency Code 15. Supplementary Notes 16. Abstract Because fixed fire fighting systems (FFFS) were not routinely applied in all U.S. tunnels, the present-day approach can vary between planned facilities and regions, especially in critical design areas such as operational  integration  with  the  emergency  ventilation  system  (EVS).  Further  research  and  a  designfocused  approach  to  computational  modeling  and  testing  is  needed  to  develop  a  set  of  suggested practices  for  the  operational  integration  of  FFFS  and  the  EVS.  This  document  describes  computer modeling of the FFFS and EVS. Included are validation studies based on full-scale tests (Memorial Tunnel and San Pedro de Anes Tunnel tests) and parameter studies for longitudinal and transverse ventilation. The impact of FFFS and cooling of combustion products on EVS performance is considered. ARCHIVED

Fixed fire fighting system, FFFS, deluge, tunnel, tunnel ventilation, CFD

19. Security Classif. (of this report)

UNCLASSIFIED

20. Security Classif. (of this page)

UNCLASSIFIED

21. No. of Pages

196

18. Distribution Statement

No restrictions.

22. Price

Form DOT F 1700.7(8-72)

Reproduction of completed page authorized

## Notice

This document is disseminated under the sponsorship of the U.S. Department of Transportation in the interest of information exchange. The U.S. Government assumes no liability for the use of the information contained in this document.

The U.S. Government does not endorse products or manufacturers. Trademarks or manufacturers' names appear in this report only because they are considered essential to the objective of the document. They are included  for  informational  purposes  only  and  are  not  intended  to  reflect  a  preference,  approval,  or endorsement of any one product or entity.

## Non-Binding Contents

The contents of this document do not have the force and effect of law and are not meant to bind the public in  any  way.  This  document  is  intended  only  to  provide  clarity  to  the  public  regarding  the  existing requirements  under  the  law  or  agency  policies.  While  this  document  contains  non-binding  technical information, you must comply with the applicable statutes or regulations.

The  Federal  Highway  Administration  (FHWA)  provides  high-quality  information  to  serve  Government, industry, and the public in a manner that promotes public understanding. Standards and policies are used to ensure and maximize the quality, objectivity, utility, and integrity of its information. FHWA periodically reviews quality issues and adjusts its programs and processes to ensure continuous quality improvement.

<!-- image -->

Stamp

## Quality Assurance Statement ARCHIVED

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

## World Road Association Relative Humidity Safety of Life in Tunnels United States One-Dimensional ARCHIVED

## SUMMARY

The Federal Highway Administration (FHWA) is researching the use of fixed fire fighting systems (FFFS) in road tunnels. The objective of this project is to identify and address the current industry's ability to adequately consider the operational integration of highway tunnel emergency ventilation systems (EVS) with the installed fixed fire fighting system (FFFS), and to then develop a set of suggested practices on the integration of FFFS and the EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (FWHA-HIF-20-016)
2. Workplans and workshops: Industry workshop and report (including computer modeling and testing workplans) [2] (FHWA-HIF-20-060)
- Chapter 4 looks at longitudinal smoke management including the velocity needed to control smoke (critical or confinement velocity) without and with an FFFS. Results using CFD are compared with published equations and similar order of magnitude results arrived at. The impact of the FFFS is also investigated and it is found that the FFFS reduces the longitudinal velocity needed. The result is compared with published equations for the impact of the FFFS.
3. Computer modeling research 4. Physical testing 5. Research report and suggested practices This report summarizes the computer modeling research. · Chapter 2 provides a validation study using the Memorial Tunnel test data. The computational fluid  dynamics  (CFD)  software  Fire  Dynamics  Simulator  (FDS)  is  used,  and  results  are compared with test data. The purpose of this study was to validate the ability of FDS to predict the tunnel environment during a fire with longitudinal ventilation active. Comparison with test data was made with similar results achieved, although a sensitivity of backlayering length to model  grid  resolution  is  noted,  which  is  likely  due  to  the  tunnel  friction  varying  with  grid resolution. These tests and models did not include an FFFS. · Chapter 3 provides a validation study based on 2011 tests in the San Pedro de Anes Tunnel. with an FFFS operational. The CFD models were compared with test data with similar results for  temperature  prediction  downstream  of  the  fire  when  the  FFFS  is  operated.  Some discrepancy between model and test for the radiation heat flux downstream of the fire was identified, with the CFD model tending to predict a larger peak heat flux. ARCHIVED
- Chapter 5 provides an investigation of the interaction between longitudinal ventilation and FFFS for a range of parameters, including tunnel cross section, water application rate and FFFS drop diameter. Results confirmed that a smaller droplet diameter and increased water application rate lead to less smoke backlayering and a reduced confinement velocity.

- Chapter  6  and  Chapter  7  provide  parameter  studies  related  to  transverse  ventilation. Interaction of water spray and transverse exhaust systems was investigated, and it was found that  a distributed  transverse exhaust system (many small ventilation slots) did not entrain much water into the exhaust air stream, but a single point exhaust did tend to draw water into the exhaust, thus reducing the amount of water reaching the roadway. Chapter 7 looks at the interactions between a transverse ventilation system with FFFS operating to provide insight into the influences of the EVS. The results show that the FFFS improves the efficiency of the transverse system, with overall smoke spread extent being reduced when using FFFS. The FFFS did cause some reduction in tenability in the zone of FFFS operation due to the water spray mixing smoke downward. However, this was confined to an area near to the fire when the FFFS was operating, and additional exhaust is not suggested as a remedy.
- Chapter 8 summarizes the results and discusses next steps. The first research hypothesis was that FFFS and EVS can be integrated, and EVS capacity optimized due to FFFS cooling. The second research hypothesis was that CFD can be used to help integrate the FFFS and EVS for varying system designs. Both hypotheses are supported by the results presented in the report.

## ARCHIVED

## ACKNOWLEDGMENTS

The  FWHA  is  the  source  of  all  figures  and  photographs  within  this  document  unless  noted otherwise.

The contribution of reviewers from industry is gratefully acknowledged: Andre Calado (ASHRAE TC5.9, Jacobs), Arnold Dix (ITA), David Hahm (ASHRAE TC5.9, Jacobs), Norris Harvey (NFPA 502,  Mott-MacDonald),  Yoon  Ko  (ASHRAE  TC5.9,  Jacobs),  Igor  Maevski  (ASHRAE  TC5.9, Jacobs).

<!-- image -->

Stamp

## UNIT CONVERSIONS

| ARCHIVED   |
|------------|

## TABLE OF CONTENTS

| INTRODUCTION .............................................................................................................................   | INTRODUCTION .............................................................................................................................   | INTRODUCTION .............................................................................................................................   |
|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| 1 1.1                                                                                                                                        | Terminology .............................................................................................................................    | 1 1                                                                                                                                          |
| 1.2                                                                                                                                          | Literature Survey and Synthesis ...............................................................................................              | 2                                                                                                                                            |
| 1.3                                                                                                                                          | Workshop Report - Research Hypotheses ...............................................................................                        | 3                                                                                                                                            |
| 1.4                                                                                                                                          | Outline of Report                                                                                                                            | ...................................................................................................................... 4                     |
| 2                                                                                                                                            | CFD MODEL VALIDATION - MEMORIAL TUNNEL TESTS ........................................................... 6                                   |                                                                                                                                              |
| 2.1                                                                                                                                          | Overview                                                                                                                                     | .................................................................................................................................. 6         |
| 2.2                                                                                                                                          | Memorial Tunnel Test 606A (10 MW) .....................................................................................                      | 10                                                                                                                                           |
| 2.3                                                                                                                                          | Memorial Tunnel Test 611/612B (50 MW) ...............................................................................                        | 23                                                                                                                                           |
| 2.4                                                                                                                                          | Research Findings and Suggested Practices Based on Findings ............................................                                     | 79                                                                                                                                           |
| 2.5                                                                                                                                          | Suggested Areas for Further Research ...................................................................................                     | 81                                                                                                                                           |
| 3                                                                                                                                            | CFD MODEL VALIDATION - FIXED FIRE FIGHTING SYSTEM ...................................................                                        | 82                                                                                                                                           |
| 3.1                                                                                                                                          | Overview                                                                                                                                     | ................................................................................................................................ 82          |
| 3.2                                                                                                                                          | Representation of FFFS Nozzles ............................................................................................                  | 86                                                                                                                                           |
| 3.3                                                                                                                                          | Base Case CFD Models and FHRR Profile .............................................................................                          | 91                                                                                                                                           |
| 3.4                                                                                                                                          | Droplet Diameter Sensitivity ...................................................................................................             | 95                                                                                                                                           |
| 3.5                                                                                                                                          | Grid Resolution ......................................................................................................................       | 97                                                                                                                                           |
| 3.6                                                                                                                                          | Volumetric Heat Source ..........................................................................................................            | 99                                                                                                                                           |
| 3.7                                                                                                                                          | Research Findings and Suggested Practices Based on Findings ..........................................                                       | 103                                                                                                                                          |
| 3.8                                                                                                                                          | Suggested Areas for Further Research .................................................................................                       | 103                                                                                                                                          |
|                                                                                                                                              | CRITICAL AND CONFINEMENT VELOCITY ..............................................................................                             | 104                                                                                                                                          |
| 4.1                                                                                                                                          | Overview ..............................................................................................................................      | 104                                                                                                                                          |
| 4 4.2                                                                                                                                        | Mixing Controlled Combustion Models .................................................................................. ARCHIVED              | 107                                                                                                                                          |
| 4.3                                                                                                                                          | Volumetric Heat Source Models ...........................................................................................                    | 110                                                                                                                                          |
| 4.4                                                                                                                                          | Scaled Tunnel Critical Velocity .............................................................................................                | 115                                                                                                                                          |
| 4.5                                                                                                                                          | Critical Velocity with FFFS ....................................................................................................             | 118                                                                                                                                          |
| 4.6                                                                                                                                          | Research Findings and Suggested Practices Based on Findings ..........................................                                       | 121                                                                                                                                          |
| 4.7                                                                                                                                          | Suggested Areas for Further Research .................................................................................                       | 124                                                                                                                                          |
|                                                                                                                                              | LONGITUDINAL VENTILATION..................................................................................................                   | 125                                                                                                                                          |
| 5 5.1                                                                                                                                        | Overview ..............................................................................................................................      | 125                                                                                                                                          |
| 5.2                                                                                                                                          | Results for San Pedro de Anes Tunnel - Cross Section D ....................................................                                  | 129                                                                                                                                          |
| 5.3                                                                                                                                          | Results for Extra Wide Cross Section - Cross Section C ......................................................                                | 136                                                                                                                                          |
| 5.4                                                                                                                                          | Results for Memorial Tunnel - Cross Section A ....................................................................                           | 136                                                                                                                                          |
| 5.5                                                                                                                                          | Additional Results (Tenability) ..............................................................................................               | 137                                                                                                                                          |
| 5.6                                                                                                                                          | Structural Temperatures                                                                                                                      | ....................................................................................................... 143                                  |

| 5.7                                                                                                                                           | Research Findings ............................................................................................................... 146         |
|-----------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 5.8                                                                                                                                           | Suggested Areas for Further Research ................................................................................. 147                    |
| 6 TRANSVERSE VENTILATION AND WATER SPRAY INTERACTIONS ...................................... 148                                              | 6 TRANSVERSE VENTILATION AND WATER SPRAY INTERACTIONS ...................................... 148                                              |
| 6.1                                                                                                                                           | Overview .............................................................................................................................. 148   |
| 6.2                                                                                                                                           | Transverse Exhaust Slots ..................................................................................................... 149            |
| 6.3                                                                                                                                           | Single Point Exhaust ............................................................................................................ 152         |
| 6.4                                                                                                                                           | Research Findings ............................................................................................................... 156         |
| 6.5                                                                                                                                           | Suggested Areas for Further Research ................................................................................. 156                    |
| 7                                                                                                                                             | TRANSVERSE VENTILATION .................................................................................................... 157               |
| 7.1                                                                                                                                           | Overview .............................................................................................................................. 157   |
| 7.2                                                                                                                                           | Transverse Ventilation - Distributed Exhaust ........................................................................ 157                     |
| 7.3                                                                                                                                           | Transverse Ventilation - Point Exhaust ................................................................................ 171                   |
| 7.4                                                                                                                                           | Research Findings ............................................................................................................... 182         |
| 7.5                                                                                                                                           | Suggested Areas for Further Research ................................................................................. 182                    |
| 8 CONCLUSION............................................................................................................................. 183 | 8 CONCLUSION............................................................................................................................. 183 |
| 8.1                                                                                                                                           | Research Hypotheses and Discussion .................................................................................. 183                     |
| 8.2                                                                                                                                           | Suggested Practices Based on Research Findings ............................................................... 184                            |
| 8.3                                                                                                                                           | Suggested Topics for Future Research ................................................................................. 185                    |
| APPENDIX A: TABLE OF CFD RUNS REPORTED ........................................................................ 190                           | APPENDIX A: TABLE OF CFD RUNS REPORTED ........................................................................ 190                           |

<!-- image -->

Stamp

ARCHIVED

## LIST OF FIGURES

| Figure 1-1:                                                                                                                                                                                                                                                                                                                                                                          | Longitudinal ventilation.                                                                                                                                                                                        |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Figure 2-1: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A). Figure 2-2: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 307 (EVS-02-27). Figure 2-3: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 305 (EVS-02-27). Figure 2-4: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 304 (EVS-02-27). Figure 2-5: Memorial Tunnel (606A, 10 MW) | .............................................................................................2 .............................6 .......11 .......12 .......12 versus CFD, velocity loop 302 (EVS-02-27). .......13 |
| Figure 2-6: Memorial Tunnel (606A, 10 MW) (EVS-02-27). Figure 2-7: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop (EVS-02-27). .............................................................................................................................14                                                                                                           | versus CFD, temperature loop 307 .............................................................................................................................13 305                                             |
| Figure 2-8: Memorial Tunnel (606A, 10 MW) versus CFD, temperature                                                                                                                                                                                                                                                                                                                    | loop 304                                                                                                                                                                                                         |
| (EVS-02-27). .............................................................................................................................14                                                                                                                                                                                                                                         |                                                                                                                                                                                                                  |
| Figure 2-9: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop (EVS-02-27). .............................................................................................................................15                                                                                                                                                                  | 302                                                                                                                                                                                                              |
| Figure 2-10: Equation. Haaland equation for friction factor. .......................................................16 Figure 2-11: Equation. Pressure loss equation. .........................................................................16 Figure 2-12: CFD model configuration and blockages near to the fire. ARCHIVED                                                      | ......................................16 sensitivity,                                                                                                                                                            |
| Figure 2-13: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions velocity loop 307 (r value for EVS-02-43). .................................................................................18 Figure 2-14: Memorial Tunnel (606A, 10 MW)                                                                                                                                     | versus CFD, wall conditions sensitivity,                                                                                                                                                                         |
| velocity loop 305 (r value for EVS-02-43). .................................................................................19 Figure 2-15: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions velocity loop 304 (r value for EVS-02-43).                                                                                                                                     | sensitivity,                                                                                                                                                                                                     |
| .................................................................................19 Figure 2-16: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity,                                                                                                                                                                                                              | sensitivity,                                                                                                                                                                                                     |
| velocity loop 302 (r value for EVS-02-43). .................................................................................20 Figure 2-17: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions                                                                                                                                                                                |                                                                                                                                                                                                                  |
| temperature loop 307 (r value for EVS-02-43). Figure 2-18: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions temperature loop 305 (r value for EVS-02-43). ..........................................................................21                                                                                                                                      | ..........................................................................20 sensitivity,                                                                                                                        |
| Figure 2-19: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity,                                                                                                                                                                                                                                                                                                  |                                                                                                                                                                                                                  |
| temperature loop 304 (r value for EVS-02-43). ..........................................................................21 Figure 2-20: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity,                                                                                                                                                                       |                                                                                                                                                                                                                  |
| temperature loop 302 (r value for EVS-02-43). ..........................................................................22 Figure 2-21: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 307 (EVS-02-51).                                                                                                                                                                     | .................................................................................................................................................25                                                              |
| .................................................................................................................................................25 Figure 2-23: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 304                                                                                                                                                         |                                                                                                                                                                                                                  |
| Figure 2-24: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 302                                                                                                                                                                                                                                                                                                             |                                                                                                                                                                                                                  |
| (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                  |
| .................................................................................................................................................26                                                                                                                                                                                                                                  |                                                                                                                                                                                                                  |
| Figure 2-22: Memorial Tunnel (612B, 50 MW)                                                                                                                                                                                                                                                                                                                                           | versus CFD, velocity loop 305 (EVS-02-51).                                                                                                                                                                       |
| (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                         |                                                                                                                                                                                                                  |

.................................................................................................................................................26

| Figure 2-25: (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                                                 | Memorial .............................................................................................................................27                                                                                                                                                                                                                                                                                  | Tunnel                                                                                                                                                                                                                                                                                                                                                                                                                    | (612B,                                                                                                                                                                                                                                                                                                                                                                                                                    | 50 MW)                                                                                                                                                                                                                                                                                                                                                                                                                    | versus CFD,                                                                                                                                                                                                                                                                                                                                                                                                               | temperature                                                                                                                                                                                                                                                                                                                                                                                                               | loop                                                                                                                                                                                                                                                                                                                                                                                                                      | 307                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| Figure 2-26: (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                                                 | Memorial                                                                                                                                                                                                                                                                                                                                                                                                                  | Tunnel                                                                                                                                                                                                                                                                                                                                                                                                                    | (612B,                                                                                                                                                                                                                                                                                                                                                                                                                    | 50 MW)                                                                                                                                                                                                                                                                                                                                                                                                                    | versus CFD,                                                                                                                                                                                                                                                                                                                                                                                                               | temperature .............................................................................................................................27                                                                                                                                                                                                                                                                               | loop                                                                                                                                                                                                                                                                                                                                                                                                                      | 305                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                     |
| Figure 2-27: (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                                                 | Memorial                                                                                                                                                                                                                                                                                                                                                                                                                  | Tunnel                                                                                                                                                                                                                                                                                                                                                                                                                    | (612B,                                                                                                                                                                                                                                                                                                                                                                                                                    | 50 MW)                                                                                                                                                                                                                                                                                                                                                                                                                    | versus                                                                                                                                                                                                                                                                                                                                                                                                                    | CFD, temperature .............................................................................................................................28                                                                                                                                                                                                                                                                          | loop                                                                                                                                                                                                                                                                                                                                                                                                                      | 304                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                     |
| Figure 2-28: (EVS-02-51).                                                                                                                                                                                                                                                                                                                                                                                                 | Memorial                                                                                                                                                                                                                                                                                                                                                                                                                  | Tunnel                                                                                                                                                                                                                                                                                                                                                                                                                    | (612B,                                                                                                                                                                                                                                                                                                                                                                                                                    | 50 MW)                                                                                                                                                                                                                                                                                                                                                                                                                    | versus                                                                                                                                                                                                                                                                                                                                                                                                                    | CFD, temperature .............................................................................................................................28                                                                                                                                                                                                                                                                          | loop                                                                                                                                                                                                                                                                                                                                                                                                                      | 302                                                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                     |
| Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         | Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48). ..........................................................................29                                                                                                                                                                                                         |                                                                                     |
| Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         |                                                                                     |
| Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         | Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48). ..........................................................................30                                                                                                                                                                                                         |                                                                                     |
| Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         | Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48). ..........................................................................31                                                                                                                                                                                                         |                                                                                     |
| Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             | Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48). ...................................................................31                                                                                                                                                                                                             |                                                                                     |
| Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             |                                                                                     |
| Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             | Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48). ...................................................................32                                                                                                                                                                                                             |                                                                                     |
| Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             | Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). ...................................................................33                                                                                                                                                                                                             |                                                                                     |
| Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          |                                                                                     |
| Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          | Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53). .................................................................................34                                                                                                                                                                                                          |                                                                                     |
| Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          | Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53). .................................................................................35                                                                                                                                                                                                          |                                                                                     |
| Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         | Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model,                                                                                                                                                                                                                                                                                                                                         |                                                                                     |
| velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 | velocity loop 302 (r value for EVS-02-53). .................................................................................35 Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, ARCHIVED                                                                                                                                                                                                 |                                                                                     |
| temperature loop 307 (r value for EVS-02-53). ..........................................................................36 Figure 2-42:                                                                                                                                                                                                                                                                                   | Memorial                                                                                                                                                                                                                                                                                                                                                                                                                  | Tunnel                                                                                                                                                                                                                                                                                                                                                                                                                    | (612B, 50                                                                                                                                                                                                                                                                                                                                                                                                                 | MW)                                                                                                                                                                                                                                                                                                                                                                                                                       | versus CFD, dynamic                                                                                                                                                                                                                                                                                                                                                                                                       | Smagorinsky                                                                                                                                                                                                                                                                                                                                                                                                               | temperature loop 307 (r value for EVS-02-53). ..........................................................................36 Figure 2-42:                                                                                                                                                                                                                                                                                   | model,                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                     |
| temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, | temperature loop 305 (r value for EVS-02-53). ..........................................................................36 Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53). ..........................................................................37 Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, |                                                                                     |
| temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                | temperature loop 302 (r value for EVS-02-53). ..........................................................................37                                                                                                                                                                                                                                                                                                |                                                                                     |
| Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | 307 (r value                                                                                                                                                                                                                                                                                                                                                                                                              | for                                                                                                                                                                                                                                                                                                                                                                                                                       | EVS-02-54).                                                                                                                                                                                                                                                                                                                                                                                                               | Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop                                                                                                                                                                                                                                                                                                                      | .................................................................................38 |
| Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     | Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54). .................................................................................38                                                                                                                                                                                                     |                                                                                     |
| Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     | Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54). .................................................................................39                                                                                                                                                                                                     |                                                                                     |

| Figure 2-48: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 302 (r value for EVS-02-54). .................................................................................39     |      |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|
| Figure 2-49: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 307 (r value for EVS-02-54). ..........................................................................40         |      |
| Figure 2-50: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 305 (r value for EVS-02-54). ..........................................................................40         |      |
| Figure 2-51: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 304 (r value for EVS-02-54). ..........................................................................41         |      |
| Figure 2-52: Memorial Tunnel (612B, 10 MW) versus CFD, closure coefficient set to 0.2, temperature loop 302 (r value for EVS-02-54). ..........................................................................41         |      |
| Figure 2-53: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test velocity loop 307 (r value for EVS-02-47 compared to test 611). ...............................................42                               | 611, |
| Figure 2-54: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test velocity loop 305 (r value for EVS-02-47 compared to test 611). ...............................................43                               | 611, |
| Figure 2-55: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test velocity loop 304 (r value for EVS-02-47 compared to test 611). ...............................................43                               | 611, |
| Figure 2-56: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test velocity loop 302 (r value for EVS-02-47 compared to test 611). ...............................................44                               | 611, |
| Figure 2-57: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test temperature loop 307 (r value for EVS-02-47 compared to test 611). ........................................44                                   | 611, |
| Figure 2-58: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test temperature loop 305 (r value for EVS-02-47 compared to test 611). ........................................45                                   | 611, |
| Figure 2-59: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test temperature loop 304 (r value for EVS-02-47 compared to test 611). ........................................45                                   | 611, |
| Figure 2-60: Memorial Tunnel (612B, 10 MW) versus CFD, comparison to test 611, temperature loop 302 (r value for EVS-02-47 compared to test 611). ........................................46 ARCHIVED                     |      |
| Figure 2-61: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 307 (r value for EVS-02-63). .....................................................................................................47 |      |
| Figure 2-62: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 305 (r value for EVS-02-63). .....................................................................................................47 |      |
| Figure 2-63: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 304 (r value for EVS-02-63). .....................................................................................................48 |      |
| Figure 2-64: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 302 (r value for EVS-02-63). .....................................................................................................48 |      |
| Figure 2-65: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 307 (r value for EVS-02-63). ..............................................................................................49     |      |
| Figure 2-66: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 305 (r value for EVS-02-63). ..............................................................................................49     |      |
| Figure 2-67: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 304 (r value for EVS-02-63). ..............................................................................................50     |      |
| Figure 2-68: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 302 (r value for EVS-02-63). ..............................................................................................50     |      |
| Figure 2-69: Memorial Tunnel (612B, 50 MW) versus CFD, smooth walls, velocity loop 307 (r value for EVS-02-50). .....................................................................................................51   |      |
| Figure 2-70: Memorial Tunnel (612B, 50 MW) versus CFD, smooth walls, velocity loop 305 (r value for EVS-02-50). .....................................................................................................52   |      |

| Figure 2-71: Memorial Tunnel (612B, 50 MW) CFD, backlayering versus time with smooth walls and obstructions (both cases). .........................................................................................52               |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Figure 2-72: Memorial Tunnel (612B, 50 MW) CFD, backlayering versus time with rough walls (roughness height 0.9 m) and no obstructions (EVS-02-62). ............................................53                                  |
| Figure 2-73: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 307 (r value for EVS-02-71). ..............................................................................................55            |
| Figure 2-74: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 305 (r value for EVS-02-71). ..............................................................................................55            |
| Figure 2-75: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 304 (r value for EVS-02-71). ..............................................................................................56            |
| Figure 2-76: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 302 (r value for EVS-02-71). ..............................................................................................56            |
| Figure 2-77: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 307 (r value for EVS-02-71). ..........................................................................57                             |
| Figure 2-78: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 305 (r value for EVS-02-71). ..........................................................................57                             |
| Figure 2-79: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 304 (r value for EVS-02-71). ..........................................................................58                             |
| Figure 2-80: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 302 (r value for EVS-02-71). ..........................................................................58                             |
| Figure 2-81: Memorial Tunnel (612B, 50 MW) backlayer distance versus time for varying grid resolution. ..........................................................................................................................59 |
| Figure 2-82: Visualization of backlayering differences for 0.2 m and 0.1 m grids. ......................59                                                                                                                          |
| Figure 2-83: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 307 (r value for EVS-02-66). ..........................................61 ARCHIVED                      |
| Figure 2-84: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 305 (r value for EVS-02-66). ..........................................61                               |
| Figure 2-85: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 304 (r value for EVS-02-66). ..........................................62                               |
| Figure 2-86: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 302 (r value for EVS-02-66). ..........................................62                               |
| Figure 2-87: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 307 (r value for EVS-02-66)....................................63                                    |
| Figure 2-88: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 305 (r value for EVS-02-66)....................................63                                    |
| Figure 2-89: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 304 (r value for EVS-02-66)....................................64                                    |
| Figure 2-90: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 302 (r value for EVS-02-66)....................................64                                    |
| Figure 2-91: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 306 (r value for EVS-02-66)....................................65                                    |
| Figure 2-92: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 303 (r value for EVS-02-66)....................................65                                    |
| Figure 2-93: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 307 (r value for EVS-02-67)...................................................................66                         |

| Figure 2-94: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 305 (r value for EVS-02-67)...................................................................67   |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Figure 2-95: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 304 (r value for EVS-02-67)...................................................................67   |
| Figure 2-96: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 302 (r value for EVS-02-67)...................................................................68   |
| Figure 2-97: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 307 (r value for EVS-02-67). ..........................................................68       |
| Figure 2-98: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 305 (r value for EVS-02-67). ..........................................................69       |
| Figure 2-99: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 304 (r value for EVS-02-67). ..........................................................69       |
| Figure 2-100: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 302 (r value for EVS-02-67). ..........................................................70      |
| Figure 2-101: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-68). ..................................71                 |
| Figure 2-102: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-68). ..................................71                 |
| Figure 2-103: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-68). ..................................72                 |
| Figure 2-104: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 302 (r value for EVS-02-68). ..................................72                 |
| Figure 2-105: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 307 (r value for EVS-02-68). ...........................73 ARCHIVED            |
| Figure 2-106: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 305 (r value for EVS-02-68). ...........................73                     |
| Figure 2-107: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-68). ...........................74                     |
| Figure 2-108: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 302 (r value for EVS-02-68). ...........................74                     |
| Figure 2-109: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 307 (r value for EVS-02-73). .............................................................75   |
| Figure 2-110: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 305 (r value for EVS-02-73). .............................................................76   |
| Figure 2-111: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 304 (r value for EVS-02-73). .............................................................76   |
| Figure 2-112: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 302 (r value for EVS-02-73). .............................................................77   |
| Figure 2-113: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 307 (r value for EVS-02-73). ......................................................77       |
| Figure 2-114: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 305 (r value for EVS-02-73). ......................................................78       |
| Figure 2-115: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 304 (r value for EVS-02-73). ......................................................78       |
| Figure 2-116: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 302 (r value for EVS-02-73) .......................................................79       |

| Figure 3-1: Fire heat release rate profile with FFFS operating (LTA test 4) [11]. .......................83                                                                                                                                 |                     |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|
| Figure 3-2: Test data, gas temperature 5 m to 10 m downstream of the fire with FFFS (LTA test 4) [11]. ................................................................................................................................83   |                     |
| Figure 3-3: Test data, heat flux downstream of the fire with FFFS (LTA test 4) [11].                                                                                                                                                        | .................84 |
| Figure 3-4: Fire geometry for the LTA CFD model. ...................................................................86                                                                                                                      |                     |
| Figure 3-5: Example nozzle spray pattern. ................................................................................87                                                                                                                |                     |
| Figure 3-6: Genetic algorithm concept.......................................................................................88                                                                                                              |                     |
| Figure 3-7: Results from genetic algorithm trial A (EVS-10-18). ................................................89                                                                                                                          |                     |
| Figure 3-8: Results from genetic algorithm trial B (EVS-10-20). ................................................89                                                                                                                          |                     |
| Figure 3-9: Spray results for 82 LPM flow rate, based on results from a genetic algorithm fit at 40 LPM, trial A1 (EVS-10-19). ...........................................................................................90                |                     |
| Figure 3-10: Spray results for 82 LPM flow rate, based on results from a genetic algorithm fit at 58 LPM, trial A2 (EVS-10-19). ...........................................................................................91               |                     |
| Figure 3-11: Base case result for LTA tests, 5 m downstream of the fire, no change to the input FHRR profile (EVS-09-31). ...............................................................................................92                 |                     |
| Figure 3-12: Base case result for LTA tests, 10 m downstream of the fire, no change to the input FHRR profile (EVS-09-31). .........................................................................................92                      |                     |
| Figure 3-13: LTA test HRR shift. ...............................................................................................93                                                                                                          |                     |
| Figure 3-14: Temperature results 5 meters downstream of the fire with FFFS operating (EVS-09-34). .............................................................................................................................94           |                     |
| Figure 3-15: Temperature results 10 meters downstream of the fire with FFFS operating (EVS-09-34). .............................................................................................................................94 ARCHIVED |                     |
| Figure 3-16: Incident heat flux data downstream of the fire (EVS-09-34). ..................................95                                                                                                                               |                     |
| Figure 3-17: Temperature downstream of the fire using larger droplet diameter (EVS-09-35). .............................................................................................................................96                  |                     |
| Figure 3-18: Temperature downstream of the fire using smaller droplet diameter (EVS-09-36). .............................................................................................................................97                 |                     |
| Figure 3-19: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m sensitivity (r value for case EVS-09-44). .......................................................98                                 |                     |
| Figure 3-20: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m sensitivity (r value for case EVS-09-44). .......................................................98                                |                     |
| Figure 3-21: Incident heat flux data downstream of the fire, coarse grid 0.4 m sensitivity (r value for case EVS-09-44). .......................................................................................................99          |                     |
| Figure 3-22: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m, volumetric heat source (r value for case EVS-09-39). ................................                                              | 100                 |
| Figure 3-23: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m, volumetric heat source (r value for case EVS-09-39). ................................                                             | 100                 |
| Figure 3-24: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m and radiation on, volumetric heat source (r value for case EVS-09-41). ......                                                       | 101                 |
| Figure 3-25: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m and radiation on, volumetric heat source (r value for case EVS-09-41). ......                                                      | 101                 |
| Figure 3-26: Temperature results 5 meters downstream of the fire with FFFS operating, finer grid 0.2 m, volumetric heat source (r value for case EVS-09-40). ....................................                                           | 102                 |
| Figure 3-27: Temperature results 10 meters downstream of the fire with FFFS operating, finer grid 0.2 m, volumetric heat source (r value for case EVS-09-40). ....................................                                          | 102                 |

| Figure 4-1: Equation. Critical velocity, NFPA 502 2014 [12] and 2017 edition [7]. ...................                                                                                                                                    | 105                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Figure 4-2: Equation. Critical velocity, NFPA 502 2020 edition [13]. ........................................                                                                                                                            | 106                                                                                                                                                 |
| Figure 4-3: Static pressure profile along the tunnel for mixing-controlled models. ...................                                                                                                                                   | 109                                                                                                                                                 |
| Figure 4-4: Static pressure profile for mixing-controlled and volumetric heat source combustion with small openings distributed along the tunnel. .................................................                                      | 113                                                                                                                                                 |
| Figure 4-5: Static pressure profile for a volumetric heat source comparing cases with and without small openings distributed along the tunnel.................................................................                           | 113                                                                                                                                                 |
| Figure 4-6: Static pressure profile for a volumetric heat source with refined grid. ....................                                                                                                                                 | 114                                                                                                                                                 |
| Figure 4-7: Equation. SVS pressure drop equation due to fire. ................................................                                                                                                                           | 114                                                                                                                                                 |
| Figure 4-8: Equation. Pressure drop equation recommended for EVS design [28]. .................                                                                                                                                          | 115                                                                                                                                                 |
| Figure 4-9: Equation. Scaling relationships [30] [31]................................................................                                                                                                                    | 115                                                                                                                                                 |
| Figure 4-10: Static pressure profile results for models with and without a passive scalar. .......                                                                                                                                       | 117                                                                                                                                                 |
| Figure 4-11: Static pressure profile results for full-scale and one quarter scaled models, with results plotted as full-scale equivalent. .............................................................................                  | 117                                                                                                                                                 |
| Figure 4-12: Equation. Critical velocity with an FFFS operating [14]. .......................................                                                                                                                            | 118                                                                                                                                                 |
| Figure 4-13: Static pressure profiles for cases with an FFFS. .................................................                                                                                                                          | 121                                                                                                                                                 |
| Figure 4-14: Summary plot of CFD results versus NFPA 502 equations, no FFFS. .................                                                                                                                                           | 122                                                                                                                                                 |
| Figure 4-15: Summary plot of CFD results versus equations by Ko and Hadjisophocleous [14], FFFS operating. ..............................................................................................................                | 123                                                                                                                                                 |
| Figure 5-1: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A). .........................                                                                                                                                    | 127                                                                                                                                                 |
| Figure 5-2: Square cross section for CFD analysis (ID B).                                                                                                                                                                                | ...................................................... 127                                                                                          |
| Figure 5-3: Rectangular cross section for CFD analysis (ID C)................................................                                                                                                                            | 128                                                                                                                                                 |
| Figure 5-4: Rectangular cross section for CFD analysis representing San Pedro de Anes tunnel at the fire site (7.2 m width used in models) (ID D). ...................................................... ARCHIVED                       | 128                                                                                                                                                 |
| Figure 5-5: Backlayering and upstream velocity for 5 MW fires.                                                                                                                                                                           | .............................................. 133                                                                                                  |
| Figure 5-6: Backlayering and upstream velocity for 20 MW fires.                                                                                                                                                                          | ............................................ 133                                                                                                    |
| Figure 5-7: Backlayering and upstream velocity for 100 MW fires. ..........................................                                                                                                                              | 134                                                                                                                                                 |
| Figure 5-8: Equation. Critical velocity with an FFFS operating [14]. .........................................                                                                                                                           | 135                                                                                                                                                 |
| Figure 5-9: CO concentration along tunnel for 5 MW fires with and without FFFS. ..................                                                                                                                                       | 138                                                                                                                                                 |
| Figure 5-10: Relative humidity downstream of fire for 5 MW fires with and without FFFS.                                                                                                                                                  | ....... 138                                                                                                                                         |
| Figure 5-11: Temperature along tunnel for 5 MW fires with and without FFFS. .......................                                                                                                                                      | 139                                                                                                                                                 |
| Figure 5-12: Visibility along tunnel for 5 MW fires with and without FFFS. ...............................                                                                                                                               | 139                                                                                                                                                 |
| Figure 5-13: CO concentration along tunnel for 20 MW fires with and without FFFS. ..............                                                                                                                                         | 140                                                                                                                                                 |
| Figure 5-14: Relative humidity downstream of fire for 20 MW fires with and without FFFS. ............................................................................................................................................... | 140                                                                                                                                                 |
| Figure 5-15: Temperature along tunnel for 20 MW fires with and without FFFS. .....................                                                                                                                                       | 141                                                                                                                                                 |
| Figure 5-16: Visibility along tunnel for 20 MW fires with and without FFFS. .............................                                                                                                                                | 141                                                                                                                                                 |
| Figure 5-17: CO concentration along tunnel for 100 MW fires with and without FFFS.                                                                                                                                                       | ............ 142                                                                                                                                    |
| Figure 5-18: Relative humidity downstream of fire for 100 MW fires with and without FFFS.                                                                                                                                                | ............................................................................................................................................... 142 |
| Figure 5-19: Temperature along tunnel for 100 MW fires with and without FFFS. ...................                                                                                                                                        | 143                                                                                                                                                 |
| Figure 5-20: Visibility along tunnel for 100 MW fires with and without FFFS.                                                                                                                                                             | ........................... 143                                                                                                                     |

| Figure 5-21: Ceiling surface temperature for 20 MW fires with and without FFFS. .................. FFFS.                                                                                                                              | 144                                                                               |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Figure 5-22: Ceiling adiabatic surface temperature for 20 MW fires with and without ...............................................................................................................................................   | 145                                                                               |
| Figure 5-23: Ceiling surface temperature for 100 MW fires with and without FFFS. ................                                                                                                                                     | 145                                                                               |
| Figure 5-24: Ceiling adiabatic surface temperature for 100 MW fires with and without FFFS. ......................................................................................................................................     | 146                                                                               |
| Figure 6-1: Interaction of water droplet and exhaust................................................................                                                                                                                  | 148                                                                               |
| Figure 6-2: Transverse ventilation set up. ...............................................................................                                                                                                            | 150                                                                               |
| Figure 6-3: Sensitivity scenario schematic showing full duct model. ........................................                                                                                                                          | 150                                                                               |
| Figure 6-4: Contour view of tunnel roadway and water accumulation for 5 mm/min water application rate and 650 µm drop size. ....................................................................................                      | 152                                                                               |
| Figure 6-5: Contour view of tunnel roadway and water accumulation for 2.5 mm/min water application rate and 155 µm drop size. ....................................................................................                    | 152                                                                               |
| Figure 6-6: Overhead exhaust configuration.                                                                                                                                                                                           | .......................................................................... 154    |
| Figure 6-7: Sidewall exhaust configuration.                                                                                                                                                                                           | ............................................................................. 154 |
| Figure 7-1: Tunnel with transverse ventilation showing ducts. .................................................                                                                                                                       | 158                                                                               |
| Figure 7-2: Photo of a tunnel with transverse ventilation. ........................................................                                                                                                                   | 158                                                                               |
| Figure 7-3: Transverse ventilation system schematic. .............................................................                                                                                                                    | 158                                                                               |
| Figure 7-4: Transverse ventilation system in exhaust near to the bulkhead. ............................                                                                                                                               | 159                                                                               |
| Figure 7-5: Visibility along ceiling for 5 MW fires (EVS-15-4 and EVS-15-7)............................                                                                                                                               | 161                                                                               |
| Figure 7-6: Visibility 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7)........                                                                                                                                         | 162                                                                               |
| Figure 7-7: Temperature 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7). ..............................................................................................................................                | 162                                                                               |
| Figure 7-8: Carbon monoxide 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7). .............................................................................................................................. ARCHIVED   | 163                                                                               |
| Figure 7-9: Visibility along ceiling for 20 MW fires (EVS-15-5, EVS-15-8 and EVS-15-13). .....                                                                                                                                        | 164                                                                               |
| Figure 7-10: Visibility 2.4 m above the roadway for 20 MW fires (EVS-15-5, EVS-15-8 and EVS-15-13). ............................................................................................................................      | 164                                                                               |
| Figure 7-11: Visualization of smoke spread (cropped at 10 m or less visibility), no FFFS.                                                                                                                                             | ....... 165                                                                       |
| Figure 7-12: Visualization of smoke spread (cropped at 10 m or less visibility), FFFS. ............                                                                                                                                   | 165                                                                               |
| Figure 7-13: Visualization of smoke spread (cropped at 10 m or less visibility), FFFS, reduced exhaust rate. .............................................................................................................            | 165                                                                               |
| Figure 7-14: Temperature 2.4 m above the roadway for 20 MW fires (EVS-15-5 and EVS-15-8 and EVS-15-13). .....................................................................................................                         | 166                                                                               |
| Figure 7-15: Carbon monoxide 2.4 m above the roadway for 20 MW fires (EVS-15-5 and EVS-15-8 and EVS-15-13). .....................................................................................................                     | 166                                                                               |
| Figure 7-16: Visualization of temperature (cropped below 60 ⁰C), no FFFS. ...........................                                                                                                                                 | 167                                                                               |
| Figure 7-17: Visualization of temperature (cropped below 60 ⁰C), FFFS. ................................                                                                                                                               | 167                                                                               |
| Figure 7-18: Visualization of temperature (cropped below 60 ⁰C), FFFS, reduced exhaust rate. ........................................................................................................................................ | 167                                                                               |
| Figure 7-19: Visualization of temperature (black is 28 ⁰C and higher), no FFFS. .....................                                                                                                                                 | 168                                                                               |
| Figure 7-20: Visualization of temperature (black is 28 ⁰C and higher), FFFS.                                                                                                                                                          | .......................... 168                                                    |

| Figure 7-21: Visibility along ceiling for 20 MW fires (EVS-15-9, EVS-15-10, EVS-15-11 and EVS-15-12). Droplet size and water application impact. ..........................................................                 | 169                                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Figure 7-22: Visibility 2.4 m above the roadway for 20 MW fires (EVS-15-9, EVS-15-10, EVS-15-11 and EVS-15-12). Droplet size and water application impact. .................................                                | 169                                                                                                                                                 |
| Figure 7-23: Visibility along ceiling for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15). ............................................................................................................................    | 170                                                                                                                                                 |
| Figure 7-24: Visibility 2.4 m above the roadway for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15). ..................................................................................................................... | 170                                                                                                                                                 |
| Figure 7-25: Carbon monoxide 2.4 m above the roadway for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15). ...................................................................................................              | 171                                                                                                                                                 |
| Figure 7-26: Ventilation configuration for case EVS-16.                                                                                                                                                                     | .......................................................... 171                                                                                      |
| Figure 7-27: Visibility along ceiling EVS-16-1 and EVS-16-2 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s). .......................................................................          | 174                                                                                                                                                 |
| Figure 7-28: Visibility 2.4 m above roadway, EVS-16-1 and EVS-16-2 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s). ...................................................                       | 175                                                                                                                                                 |
| Figure 7-29: Visibility along ceiling EVS-16-19 and EVS-16-20 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s, decreased upstream velocity). ..................                                | 175                                                                                                                                                 |
| Figure 7-30: Visibility 2.4 m above roadway, EVS-16-19 and EVS-16-20 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s, decreased upstream velocity). ARCHIVED                                   | ............................................................................................................................................... 176 |
| Figure 7-31: Visibility along ceiling EVS-16-3 and EVS-16-4 (20 MW, extract points C and E at sidewall, total exhaust rate 150 m3/s). .............................................................................         | 176                                                                                                                                                 |
| Figure 7-32: Visibility along ceiling EVS-16-21 and EVS-16-22 (20 MW, extract points C and E at sidewall, total exhaust rate 150 m3/s, decreased upstream velocity). .......................                                | 177                                                                                                                                                 |
| Figure 7-33: Visibility along ceiling EVS-16-5 and EVS-16-6 (100 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s). ................................................................                | 177                                                                                                                                                 |
| Figure 7-34: Visibility along ceiling EVS-16-7 and EVS-16-8 (100 MW, extract points C and E at sidewall, total exhaust rate 150 m3/s). ......................................................................               | 178                                                                                                                                                 |
| Figure 7-35: Visibility along ceiling EVS-16-9 and EVS-16-10 (100 MW, extract points C and E at ceiling level, total exhaust rate 150 m3/s), FFFS parameters sensitivity. ...................                               | 178                                                                                                                                                 |
| Figure 7-36: Visibility along ceiling EVS-16-11 and EVS-16-12 (20 MW, extract points A and C at ceiling level, total exhaust rate 150 m3/s). ................................................................               | 179                                                                                                                                                 |
| Figure 7-37: Visibility 2.4 m above roadway, EVS-16-11 and EVS-16-12 (20 MW, extract points A and C at ceiling level, total exhaust rate 150 m3/s). ...................................................                     | 179                                                                                                                                                 |
| Figure 7-38: Visibility along ceiling EVS-16-13 and EVS-16-14 (20 MW, extract points A and C at sidewall, total exhaust rate 150 m3/s). ......................................................................              | 180                                                                                                                                                 |
| Figure 7-39: Visibility 2.4 m above roadway EVS-16-13 and EVS-16-14 (20 MW, extract points A and C at sidewall, total exhaust rate 150 m3/s). ........................................................                      | 180                                                                                                                                                 |
| Figure 7-40: Visibility along ceiling EVS-16-15 and EVS-16-16 (20 MW, extract points A and C at ceiling level, total exhaust rate 100 m3/s). ................................................................               | 181                                                                                                                                                 |
| Figure 7-41: Visibility along ceiling EVS-16-17 and EVS-16-18 (all extract points A, B, C, D, and E at ceiling level, total exhaust rate 100 m3/s). ............................................................            | 181                                                                                                                                                 |

## LIST OF TABLES

| Table 2-1: Memorial Tunnel CFD model parameters. ..................................................................9                                                                                                                  |                                                                                                 |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Table 2-2: Memorial Tunnel test 606A measured FHRR and bulk velocity [9]. ..........................10                                                                                                                                |                                                                                                 |
| Table 2-3: Cold flow results for tunnel friction calculation. .........................................................17                                                                                                             |                                                                                                 |
| Table 2-4: Memorial Tunnel test 611 measured FHRR and bulk velocity [9]..............................23                                                                                                                               |                                                                                                 |
| Table 2-5: Memorial Tunnel test 612B measured FHRR and bulk velocity [9]. ..........................23                                                                                                                                |                                                                                                 |
| Table 3-1: LTA test CFD model parameters. .............................................................................85                                                                                                             |                                                                                                 |
| Table 3-2: Nozzle parameter development, genetic algorithm input ranges and optimal values, trial A and trial B. ..........................................................................................................88         |                                                                                                 |
| Table 3-3: Summary of sensitivity results for varying nozzle flow rates. ....................................90                                                                                                                       |                                                                                                 |
| Table 3-4: Nozzle parameter development, genetic algorithm input ranges and optimal values, trial A and trial C. ..........................................................................................................96         |                                                                                                 |
| Table 4-1: CFD parameters for critical velocity validation. .......................................................                                                                                                                   | 107                                                                                             |
| Table 4-2: Longitudinal smoke control results - mixing-controlled combustion models (FDS default)........................................................................................................................... ARCHIVED | 109                                                                                             |
| Table 4-3: Longitudinal smoke control results - volumetric heat source results. ......................                                                                                                                                | 112                                                                                             |
| Table 4-4: Critical velocity results - volumetric heat source results for scaled geometry.                                                                                                                                            | ........ 116                                                                                    |
| Table 4-5: Model parameters for critical velocity and FFFS operating. ....................................                                                                                                                            | 118                                                                                             |
| Table 4-6: Critical velocity results - volumetric heat source results with FFFS. .......................                                                                                                                              | 120                                                                                             |
| Table 5-1: Confinement velocity parameter study. ..................................................................                                                                                                                   | 125                                                                                             |
| Table 5-2: Longitudinal ventilation - 5 MW fires. .....................................................................                                                                                                               | 130                                                                                             |
| Table 5-3: Longitudinal ventilation - 20 MW. ...........................................................................                                                                                                              | 131                                                                                             |
| Table 5-4: Longitudinal ventilation - 100 MW. .........................................................................                                                                                                               | 132                                                                                             |
| Table 5-5: Confinement velocity and backlayering with FFFS.                                                                                                                                                                           | ................................................ 136                                            |
| Table 5-6: Longitudinal ventilation, extra wide cross section - 20 MW. ...................................                                                                                                                            | 136                                                                                             |
| Table 5-7: Longitudinal ventilation, Memorial tunnel - 20 MW. ................................................                                                                                                                        | 137                                                                                             |
| Table 6-1: Droplet parameters tested. .....................................................................................                                                                                                           | 148                                                                                             |
| Table 6-2: Transverse ventilation and water spray interactions. ..............................................                                                                                                                        | 150                                                                                             |
| Table 6-3: Transverse ventilation, single point exhaust and water spray interactions. .............                                                                                                                                   | 155                                                                                             |
| Table 7-1: Transverse ventilation.                                                                                                                                                                                                    | ........................................................................................... 160 |
| Table 7-2: Transverse ventilation - point exhaust.                                                                                                                                                                                    | .................................................................. 172                          |

## 1 INTRODUCTION

The Federal Highway Administration (FHWA) is currently researching the use of fixed fire fighting systems (FFFS) in road tunnels. The objective of this project is to identify and address the current industry's ability to adequately consider the operational integration of highway tunnel emergency ventilation systems (EVS) with installed FFFS, and to then develop a set of suggested practices on the integration of FFFS and EVS. The technical approach to this research project is divided into the following five distinct tasks:

1. Literature survey and synthesis [1] (FWHA-HIF-20-016).
2. Workplans and workshops: Industry workshop and report (including computer modeling and testing workplans) [2] (FHWA-HIF-20-060).
- The term water mist system is associated with a deluge system that employs a high water pressure and special nozzles to generate a very small droplet diameter (typical pressures 16 bar to 60 bar, droplet diameter in the order 400 μm to 200 μm).

3. Computer modeling research. 4. Physical testing. 5. Research report and suggested practices. This document is the report summarizing the computer modeling research. 1.1 Terminology In the industry, numerous terms are used to describe EVS and FFFS in tunnels. The following descriptions are used herein. Although a water mist system is technically a deluge sprinkler system (per NFPA 13 - note that use of NFPA standards in highway tunnels is voluntary and not a Federal requirement), in the tunnel  industry,  the  terms  for  deluge  system  and  water  mist  system  have  a  subtle  difference between their meaning. Per the World Road Association (PIARC) publication on FFFS in highway tunnels [3], the following terms are used throughout this document: · The term deluge system refers to lower pressure large water droplet deluge systems (typical water pressures in the order 1 bar to 1.5 bar, droplet diameter in the order 1000 μm or greater). ARCHIVED

- Systems that employ frangible bulbs in the nozzles are referred to as automatic sprinkler systems .

Regarding sprinkler systems that employ foam additives , where this document refers to FFFS it implicitly refers to a water-only FFFS.

In a longitudinal ventilation system fans are used to generate air flow through the tunnel. Air is blown through the tunnel bore, therefore having one portal act as an inlet and the other an outlet; refer to Figure 1-1. Ventilation is typically achieved by jet fans installed in the tunnel ceiling space.

Figure 1-1: Longitudinal ventilation.

<!-- image -->

Flow chart

Critical velocity is a key design parameter for a longitudinal EVS. The methods used for predicting critical velocity in tunnels typically include semi-empirical equations [4] [5] and, in recent years, computational fluid dynamics (CFD) modeling [6]. Critical velocity is a function of input parameters including fire heat release rate (FHRR), tunnel geometry and tunnel slope.

Per NFPA 502, the following terms are used herein for backlayering and critical velocity [7]:

- Backlayering - Movement of smoke and hot gasses counter to the direction of ventilation airflow.
- Critical velocity - The minimum steady-state velocity of the ventilation airflow moving toward the fire, within a tunnel or passageway that is necessary to prevent backlayering at the fire site.

In this document the term confinement velocity is used to describe the steady-state velocity of the ventilation airflow moving toward the fire that is of a magnitude large enough to stop smoke movement upstream of the fire but not to prevent backlayering.

## 1.2 Literature Survey and Synthesis

Relevant to the basic goal of this research, the following key areas are identified in the literature survey and synthesis [1] for further investigation as part of the computer modeling and testing (laboratory and full-scale) efforts:

- Critical velocity - Critical velocity is of interest because the ability to predict critical velocity when  FFFS  are  operated  is  a  fundamental  input  to  an  integrated  EVS  design.  Existing equations have limited validity at high FHRRs. The goal for further investigation is to develop a validated and verified method of modeling tunnel fires to determine critical velocity with FFFS, and to extend the range of validity of existing equations.

ARCHIVED

- Transverse ventilation - Transverse ventilation is of interest because many existing tunnels in the U.S. use a transverse ventilation system. Of concern is how smoke management in a transverse scheme is affected by the FFFS, as well as whether liquid water droplets can become entrained (drawn into) in the exhaust airflow and lower the effectiveness of the FFFS.

Most new tunnels in the U.S. are using a longitudinal EVS via the action of jet fans. The literature survey and synthesis described a design approach where a one-dimensional calculation is used to compute the fan thrust. As part of that review several key parts of the calculation where the FFFS have an impact were identified and are listed below:

- Fire heat release rate (FHRR) - The impact of FFFS on the FHRR is well-established from full-scale tests. Measurements of FHRR (laboratory and full-scale testing) can provide useful additional data to further confirm the efficacy of the FFFS for a given water application rate and nozzle layout/type.
- FFFS cooling of the combustion products - The ability of the FFFS to cool combustion products is well-established. Critical velocity research, modeling, and testing (measurement of temperatures) may provide additional data to further the knowledge in this area.
- Pressure  loss  (airflow  resistance)  due  to  fire  - Equations  have  been  developed  for pressure loss due to fire. Measurements of static pressure (laboratory and full-scale) upstream and downstream of the fire may provide useful additional data to further confirm validity of the equations and to understand the FFFS impacts.
- Pressure  loss  (airflow  resistance)  due  to  the  FFFS  (droplets  and  humidity)  - Measurements of pressure loss and humidity in the full-scale and laboratory scale tests may provide  useful  data  for  validation  of  analytical  calculations.  Cold  flow  measurements  may provide useful data related to droplet drag.
- Friction losses introduced by FFFS pipework - Measurements of pressure drop in the tunnel in the full-scale and laboratory scale tests with ventilation operating may provide useful data for validation of friction due to FFS pipework.
- Water droplet deflection due to the EVS - Cold flow (no fire) measurements may provide useful data related to droplet drift (visualization) due to ventilation. Computer modeling for droplet  drift  may  provide  useful  data  for  validation  of  a  model  to  investigate  transverse ventilation and droplet entrainment into a transverse ventilation system exhaust.
- Tenability for egress and fire fighting - The literature survey noted that the impact of FFFS on generation of carbon monoxide is such that the yield of CO is increased due to incomplete combustion. Measurement of CO is likely to provide useful data to help further verify this result. Measurement of irritant gas concentrations, although not a primary focus of this work, might provide useful additional data for future computer model development.

ARCHIVED

The workplans arising from the workshop report [2] outline the principal research hypotheses, approach and suggested modeling and testing to research the above topics.

## 1.3 Workshop Report - Research Hypotheses

The computer modeling workplan [2] is comprised of two components based on EVS operations. The first component looks at critical velocity and the impact on this with FFFS, and the second component  looks  at  transverse  ventilation.  Principal  hypotheses  being  investigated  with  this workplan are described below.

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized as a result  of  the  cooling  effects  of  the  FFFS  water  spray.  This  hypothesis  can  be  verified  via measurement of the critical velocity for smoke control, pressure loss due to the FFFS water spray and impact of the EVS on water delivery. If the hypothesis is true, then the critical velocity should decrease due to the cooling. Additional airflow resistance introduced by the FFFS spray should be negligible with respect to other airflow resistance in the tunnel from items such as vehicles, wall friction, buoyancy, fire, and external wind. Finally, the EVS should not cause excessive water droplet drift as to cause a negative effect on water droplet delivery to the fire zone.

The second hypothesis (to be verified by computer modeling) is that CFD can be used to predict FFFS and EVS interaction for design  integration.  Integration  combinations of  FFFS  and EVS include:

<!-- image -->

Logo

· Small and large water droplet systems. · Varying water application rates and FFFS zone configurations. · Longitudinal ventilation. · Transverse ventilation. · Single point exhaust. · Varying tunnel geometry (area, perimeter, height, grade). 1.4 Outline of Report The computational fluid dynamics (CFD) software, Fire Dynamics Simulator (FDS) was selected for the modeling [8]. FDS encompasses all the essential physics for modeling fire in a tunnel and the cooling effects from the FFFS. The models are to be based on a priori specified heat release rate with no fire suppression modeled, only cooling of combustion products. CFD models were planned to be conducted for validation purposes as follows: · Prediction of the tunnel environment during a fire: - Memorial Tunnel (West Virginia) tests (no FFFS) [9] [10]. - San Pedro de Anes tunnel (Spain) tests (with FFFS) [11]. ARCHIVED

- Prediction of the critical velocity:
- NFPA 502 equations from the editions published in 2014 [12], 2017 [7] and 2020 [13]. The 2020  edition  equations  have  recently  been  retracted  and  are  under  revision,  but comparison is still informative for this research.
- Ko's correlation (with FFFS) [14].

Once  the  approach  is  validated,  a  series  of  scenarios  are  to  be  analyzed  to  investigate  the interaction between the EVS and FFFS. Chapter 2 provides a validation study using the Memorial Tunnel test data, Chapter 3 provides a validation study with FFFS operational, Chapter 4 looks into the velocity to control smoke and the impact of the FFFS, Chapter 5 provides an investigation of the interaction between longitudinal ventilation and FFFS for a range of parameters, Chapter 6 provides an investigation of the interactions between ventilation and FFFS droplets, Chapter 7 looks at transverse ventilation, and Chapter 8 summarizes the results and discusses next steps.

<!-- image -->

Stamp

## 2 CFD MODEL VALIDATION - MEMORIAL TUNNEL TESTS

A series of 95 physical fire tests were conducted in the Memorial Tunnel (located in West Virginia) in the 1990s [9] [10]. This project was a joint effort between FHWA, Massachusetts Department of  Transportation  and  industry  partners.  The  tests  conducted  with  a  longitudinal  ventilation velocity applied are considered herein. Previous validation of CFD has occurred as part of the Memorial  Tunnel  work  in  the  phase  IV  report  [10].  The  CFD  model  developed  for  that  work (SOLVENT) did not include the ability to model the FFFS, and as such, a different CFD model is used for this work. The goal in this chapter is to validate the CFD approach for predicting the environment in a tunnel during a fire, without an FFFS operating. Model results are compared with test data available, primarily velocity and temperature profiles within the tunnel. The intent of this validation step is to have a basis on which to build for models that include the FFFS.

<!-- image -->

Engineering drawing

2.1 Overview 2.1.1 Memorial Tunnel Experiments In  the  Memorial Tunnel fire tests, a series of 95 full-scale fire tests were performed covering multiple  ventilation  regimes  including  longitudinal,  transverse,  and  natural  ventilation.  For  this validation  exercise,  Memorial  Tunnel  fire  tests  606A  (nominal  FHRR  of  10  MW)  and  tests 611/612B (nominal FHRR of 50 MW), associated with longitudinal ventilation, are considered. Measurement data included temperature and velocity profiles upstream and downstream of the fire, and smoke spread extent. Full details of the tunnel and tests are provided in the reports [9] [10]. Tunnel geometry includes the cross section, length, and grade. Refer to Figure 2-1 for the tunnel cross  section.  Tunnel  grade  runs  downward  from  north  to  south  (smoke  is  always  ventilated downgrade in the longitudinal ventilation tests), grade is a constant of 3.2 percent. The tunnel was approximately 854 m (2801 ft.) long. ARCHIVED

Figure 2-1: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A).

The fire used a pan of fuel oil (number 2 fuel oil) to generate a heat release rate (HRR) ranging from 10 MW to 100 MW. A surface area of 4.46 m 2  (48 ft 2 ) was estimated to produce a 10 MW HRR. Fire pans were set approximately 0.46 m (30 inches) from the tunnel floor. Fire proofing was applied to the walls near the fire site [9]. The centerline of the fire was approximately 615.5 m (2019 ft.) from the north portal. At the fire site the unobstructed tunnel cross sectional tunnel area was approximately 60.4 m 2  (650 ft 2 ), and the instrumentation was estimated to take up an area of approximately 10.2 m 2  (110 ft 2 ),  thus  giving  a  reduced area and higher velocity in the region of the fire [9]. Pans were correlated to FHRR approximately as follows: 50 MW used a 6.1 m by 3.7 m (20 ft. by 12 ft.) pan, 20 MW used a 3.7 m by 2.4 m (12 ft. by 8 ft.) pan, 10 MW used a 3.7 m by 1.2 m (4 ft. by 12 ft.) pan, and 30 MW used a 3.7 m by 3.7 m (12 ft. by 12 ft.) pan [10].

Results are compared herein on a pseudo-steady basis, where models were run with a constant FHRR and upstream velocity. It was necessary to time-average test data based on a period of time when the FHRR and velocity were approximately constant. For test 606A, data were timeaveraged from the comprehensive test report data (obtained from the temperature and velocity profiles provided as spreadsheet data with the test report CD-ROM [9] [15]) between 989 seconds and  1110  seconds.  For  test  612B  the  test  data  were  time  averaged  between  839  and  959 seconds.  For  test  611  data  were  time  averaged  between  887  seconds  and  1007  seconds. Comparisons with test data are made in U.S. units since the data were reported in these units; however, note that the CFD software uses SI units and thus some switching between units occurs when reporting inputs or outputs. Generally, SI units are used herein with conversions provided in the report or per the table provided at the start of this report. 2.1.2 CFD Models CFD models were developed for a (nominal) 10 MW fire (test 606A) and a (nominal) 50 MW fire (test  611/612B).  The  goal  of  the  models  was  to  validate  the  CFD  approach  for  modeling longitudinal ventilation and to test sensitivity to certain model parameters. Base case models were initially developed and then model set up parameters varied to test influence on results. Model parameters considered included the following: ARCHIVED

- Upstream velocity  magnitude  and  FHRR -  These are  the  key parameters  for  longitudinal smoke control and there was some uncertainty in the precise values that were applied in a given test. Sensitivity to these parameters was considered.
- Wall heat transfer - There was an insulated region around the fire and the wall heat transfer in this region might have had an impact on the outcomes.
- Wall friction - The tunnel was a concrete lined tunnel and there were numerous obstructions present,  such  as  measurement  instruments.  The  impact  on  these  obstructions  to  flow resistance was investigated.
- Tunnel obstructions - The obstructions in the tunnel for measurement stations created a large blockage, equivalent to about 17 percent of the cross section [9]. Sensitivity of the smoke control to these blockages was looked at.

- Turbulence model - Turbulence models in the CFD software used, Fire Dynamics Simulator (FDS), are generally based on large eddy simulation [8] and there are some different options available to test, such as a dynamic sub-grid scale model.
- Fire representation - Models with a mixing-controlled approach and a volumetric heat source were considered. The mixing-controlled approach is the default in FDS. A volumetric heat source was used in previous CFD models of the Memorial Tunnel tests [10].
- Grid resolution - Dependence of the solution on grid resolution was considered.

The FHRR modeled varies between cases and it is set to match the test data as closely as possible. The goal was to run a CFD model that was representative of portion of the test where the FHRR and upstream velocity were approximately constant with respect to time, a pseduosteady state. For the 10 MW (nominal) cases Table 2-2 provides data for test 606A; the FHRR modeled for this test is 10.2 MW with an upstream velocity of1.7 m/s. The FHRR was chosen for the 10 MW tests based on the maximum measured value. This was not initially considered to have any major affect on results due to the small (less than 1 MW) changes in FHRR observed for this test. For the 50 MW (nominal) cases Table 2-4 and Table 2-5 provide data for tests 611 and 612B; the FHRR modeled for this test is 47.2 MW (approximate mid value between minimium and maximum FHRR reported) and the upstream velocity is 2.5 m/s (approximate mid value between minimium and maximum FHRR reported). FHRR variation was larger for the 50 MW tests and sensitivity cases are considered for this case. For fire parameters, heat of combustion 42.6 MJ/kg, radiation fraction 0.3, air to fuel ratio 14.5, soot yield 0.042 kg soot/kg fuel, carbon monoxide yield 0.012 kg CO/kg fuel, molecular weight of combustion products 28 kg/kmol [10]. Fire Dynamics Simulator (FDS) is used for the CFD modeling [8]. FDS encompasses the main physics associated with modeling fire in a tunnel and the cooling effects from the FFFS. The CFD models use a fixed velocity from upstream of the fire. CFD model parameters are summarized in Table 2-1. ARCHIVED

Table 2-1: Memorial Tunnel CFD model parameters.

| ITEM                                                       | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Grid                                                       | Nominal grid resolution = 0.2 m. Blockages are added upstream of the fire to capture the 17 percent blockages due to measurement equipment. The grid is stepped to model the arched section and the net CFD model area is 61.04 m 2 . The domain length is approximately 160 m long with enough upstream length modeled to capture the backlayering, grade is -3.2 percent. Note that SI units are quoted as the FDS CFD software is in SI units. Some results are compared in U.S. units since that was the principal unit used in the test data.                                                                                                                                                                                                                                                                                                                   |
| Inlet boundary and outlet boundary                         | Inlet boundary condition = fixed velocity correpsonding to bulk velocity in the test (1.8 m/s for test 606A, 2.5 m/s for test 611/612B). Computed based on the quoted volume flow rate divided by the tunnel cross sectional area. Ambient temperature 12 ⁰C (53.5 ⁰F). Outlet boundary = open boundary per FDS User Guide [8].                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| FHRR                                                       | Varies between tests. For test 606A the FHRR is 10.2 MW and for tests 611/612B the FHRR is 47.2 MW.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| FDS parameters                                             | Simulation of long tunnels sometimes results in numerical instability in the FDS models. Remedies are noted in the FDS User Guide [8] and include setting the specific heat to be constant and adjusting pressure solver parameters. Adding micro vents along the tunnel length is also sometimes used to help with stability problems although this was not necessary in this case. The FDS version used was FDS6.7.5-578-gc15229f4f-nightly. The nominal version number was 6.7.5 and the nightly release from 30 November 2020 was used since the version addressed some issues with FFFS discovered during validation. Note that in the months after the models for this work were conducted, that updates to the FDS software were made to address stability issues with tunnel models. The impact of these updates was not considered in this report. ARCHIVED |
| Fuel                                                       | The fuel is modeled in FDS to represent a typical polymer, with the chemical formula CH 1.8 N 0.05 O 0.3 and a soot yield of 0.131 and CO yield of 0.01. Heat of combustion for these fuel parameters in the CFD model is 23,468 kJ/kg. This is assumed to not have any major effect on backlayering or temperature and velocity prediction. A volumetric heat source is used in some models and discussion relevant to the model set up is provided in the specific section presenting those results.                                                                                                                                                                                                                                                                                                                                                               |
| Measurement loop locations relative to the fire centerline | Loop 307 at 61.9 m (203 ft.) upstream of the fire centerline, loop 305 at 11.2 m (37 ft.) upstream of the fire centerline, loop 302 at 66.2 m (217 ft.) downstream of the fire centerline, loop 304 at 12.2 m (40 ft.) downstream of the fire centerline. Other loops of interest included: loop 214 at 595.7 m (1954 ft.) upstream of the fire centerline, loop 209 at 294.5 m (966 ft.) upstream, loop 208 at 189.0 m (620 ft.) upstream, and loop 207 at 110.1 m (361 ft.) upstream.                                                                                                                                                                                                                                                                                                                                                                              |
| Comparison based on linear correlation                     | Results are compared between test data and the CFD model using a Pearson correlation coefficient (r) to measure how well the data are agreeing based on a linear correlation. Strength of association between test data and CFD is taken to be poor (r value between 0.0 and 0.25), fair (r value between 0.25 and 0.5), good (r value between 0.5 and 0.75) or very good (r value between 0.75 and 1.0). Negative r values represent a situation where the linear correlation between variables trends toward the straight-line interpretations having opposite slopes.                                                                                                                                                                                                                                                                                             |

## 2.2 Memorial Tunnel Test 606A (10 MW)

## 2.2.1 Base Case Models

Bulk velocity and FHRR are key input parameters for the CFD model. For test 606A a sample of the FHRR and velocity was considered since both parameters vary slightly with time. The velocity was based on measurements at loops upstream of the fire and a free area of 60.4 m 2  (650 ft 2 ). Table 2-2  provides  the  data  from  test  measurements.  In  the  table  data  are  reported  at measurement loops upstream of the fire, refer to Table 2-1 for measurement loop locations. The average FHRR was 9.9 MW, and the average upstream velocity was 1.8 m/s. As explained in Section 2.1 the models used an FHRR of 10.2 MW and upstream velocity of 1.7 m/s.

Velocity profiles at  the  tunnel  centerline,  upstream  of  the  fire,  are  provided  in  Figure 2-2  and Figure 2-3, for distances 61.9 m (203 ft.) upstream and 11.2 m (37 ft.) upstream, respectively. Agreement between the test data and CFD is very good by the Pearson coefficient measure (r) (refer to Table 2-1 for further detail on the r value) at a distance 61.9 m (203 ft.) upstream of the fire, although some disagreement is observed near the ceiling due to the CFD model predicting additional backlayering. At a distance 11.2 m (37 ft.) upstream of the fire the Pearson coefficient measure is very good. Velocity profiles downstream of the fire, at the tunnel centerline, are provided in Figure 2-4 and Figure 2-5,  for  distances  12.2 m  (40  ft.)  and  66.2 m  (217  ft.)  downstream,  respectively.  The Pearson coefficient comparison between test data and CFD is very good 40 ft. downstream of the fire and fair at a distance 217 ft downstream. At the 217 ft. location the agreement appears very good from a qualitative perspective and the lower Pearson coefficient is not of concern. Table 2-2: Memorial Tunnel test 606A measured FHRR and bulk velocity [9]. TIME (s) FHRR (MW) LOOP 214 (m/s) LOOP 209 (m/s) LOOP 208 (m/s) LOOP 207 (m/s) 990 9.3 2.14 1.65 1.70 1.70 1019 10.1 2.09 1.70 1.69 1.71 1050 9.8 1.73 1.71 1.71 1.70 1081 10.2 2.16 1.73 1.72 1.73 1111 10.2 2.19 1.74 1.70 1.72 ARCHIVED

|   TIME (s) |   FHRR (MW) | LOOP 214 (m/s) LOOP 209 (m/s)   |   LOOP 208 (m/s) |   LOOP 207 (m/s) |   LOOP 307 (m/s) |   AVG (m/s) |   MAX (m/s) |   MIN (m/s) |
|------------|-------------|---------------------------------|------------------|------------------|------------------|-------------|-------------|-------------|
|        990 |         9.3 | 2.14 1.65                       |             1.70 |             1.70 |             1.71 |        1.78 |        2.14 |        1.65 |
|       1019 |        10.1 | 2.09 1.70                       |             1.69 |             1.71 |             1.71 |        1.78 |        2.09 |        1.69 |
|       1050 |         9.8 | 1.73 1.71                       |             1.71 |             1.70 |             1.70 |        1.80 |        2.14 |        1.70 |
|       1081 |        10.2 | 2.16 1.73                       |             1.72 |             1.73 |             1.73 |        1.81 |        2.16 |        1.72 |
|       1111 |        10.2 | 2.19 1.74                       |             1.70 |             1.72 |             1.73 |        1.82 |        2.19 |        1.70 |

Temperature  profiles  at  the  tunnel  centerline  are  provided  in  Figure 2-6  and  Figure 2-7,  for distances  61.9 m  (203  ft.)  upstream  and  11.2 m  (37  ft.)  upstream,  respectively.  Pearson coefficient  (r)  agreement between the test data and CFD is fair at a distance 61.9 m (203 ft.) upstream of the fire due to the CFD model predicting additional backlayering. At a distance 11.2 m (37 ft.) upstream of the fire the r-value agreement is very good.

Temperature profiles downstream of the fire, at the tunnel centerline, are provided in Figure 2-8 and Figure 2-9, for distances 12.2 m (40 ft.) and 66.2 m (217 ft.) downstream, respectively. Test data and CFD show good agreement (per the Pearson coefficient) at the first location, 12.2 m (40

ft.) downstream, although some differences between test data and CFD are apparent nearer to the tunnel ceiling. The reason for this is difficult to be certain of but it could be related to the close distance to the fire and some flame dynamics. The CFD model under-predicts temperature at this location; in the Memorial Tunnel work the CFD model developed as part of that work also showed an  under-prediction  of  temperature  at  this  location  (see  [10],  Figure 7.6.3-2K).  At  a  distance 66.2 m (217 ft.) downstream, the agreement per the Pearson coefficient is very good.

The results suggest that the CFD model can reliably predict the tunnel environment during a fire. The backlayering was overpredicted in the CFD model and while this is a conservative result for ventilation design, given the desire to integrate FFFS and EVS, and explore possible trade-offs, further investigation into the backlayering prediction was conducted. Reasons for differences in the backlayering could be due to the turbulence model, near-wall conditions, thermal conditions (wall heat transfer), wall friction, or uncertainty in the test data. The following sections explore the possible causes.

Figure 2-2: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 307 (EVS-02-27).

<!-- image -->

Line chart

Figure 2-3: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 305 (EVS-02-27).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-4: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 304 (EVS-02-27).

Figure 2-5: Memorial Tunnel (606A, 10 MW) versus CFD, velocity loop 302 (EVS-02-27).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-6: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop 307 (EVS-02-27).

Figure 2-7: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop 305 (EVS-02-27).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-8: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop 304 (EVS-02-27).

<!-- image -->

Line chart

Information was also stated in the test report that an insulating material was incorporated on the tunnel walls in the region of the fire. Both the insulation and friction losses could have influenced the extent of smoke movement upstream and thus sensitivity analyses were conducted.

Figure 2-9: Memorial Tunnel (606A, 10 MW) versus CFD, temperature loop 302 (EVS-02-27). 2.2.2 Wall Heat Transfer and Wall Roughness Influences The test report noted that the tunnel had wall friction that was attributable to the wall roughness and obstructions in the tunnel. Blockages were present in the tunnel for the measuring stations and reported to cover about 17 percent of the tunnel area. The wall roughness height was noted to be 0.01 ft, equating to a friction factor (calculation per Figure 2-10) on the order of 0.015 to 0.020 (friction factor per Figure 2-11). The overall friction losses through the tunnel the Memorial Tunnel accounting for inlet, exit, wall friction and obstructions amounted to a loss factor of 13.1 [10]. This was converted to an effective friction factor, per Figure 2-11, in the tunnel region around the fire. An effective friction factor (due to walls and obstructions) of 0.083 was determined. ARCHIVED

Some blockages were included in the tunnel CFD model (applied to all models herein unless noted)  to  represent  the  measuring  stations  (for  all  cases  unless  noted  otherwise),  refer  to Figure 2-12, and cold flow models (no fire present) were run to record pressure losses and enable computation of the effective friction factor in the CFD model. The wall roughness height in the FDS models was adjusted and results were compared with the Haaland equation for wall friction [16], see Figure 2-10.

Figure 2-10: Equation. Haaland equation for friction factor.

In Figure 2-10 symbols are as follows. The symbol f is the dimensionless Darcy friction factor, epsilon  is  the  roughness  height  in  meters,  D  is  the  tunnel  diameter  in  meters,  and  Re  is  the dimensionless  Reynolds  number.  The  Reynolds  number  is  computed  as  the  product  of  fluid density  in  kilograms  per  meter  cubed  times  velocity  in  meters  per  second  times  diameter  in meters, divided by the fluid viscosity in Newton seconds per meter squared. The Darcy friction factor  is  used  to  compute  the  pressure  loss  along  a  length  of  tunnel  or  duct  according  to Figure 2-11.

<!-- image -->

Logo

<!-- image -->

Bar chart

Figure 2-11: Equation. Pressure loss equation. In Figure 2-11, delta P is pressure change in Pascals, L is the length of duct or tunnel in meters, rho is the fluid density in kilograms per meter cubed, and u is the average velocity in meters per second. Table 2-3 provides results of a series of cold flow models run on different grids, with differing roughness heights with and without obstructions present. Note that the roughness heights given here  are  not  physical  values  but  were  varied  to  determine  the  effect  on  the  overall  pressure change along the length of the model. This pressure change was then used per a calculation using the equation in Figure 2-11 to compute the friction factor. POINT MONITORS ARCHIVED

Figure 2-12: CFD model configuration and blockages near to the fire.

Table 2-3: Cold flow results for tunnel friction calculation.

| CASE ID                |   ROUGHNESS HEIGHT (m) | OBSTRUCTIONS   |   INLET VELOCITY (m/s) |   HAALAND EQUATION FRICTION FACTOR |   FDS FRICTION FACTOR |
|------------------------|------------------------|----------------|------------------------|------------------------------------|-----------------------|
| EVS-02-37              |                   0.10 | No             |                    2.5 |                              0.042 |                 0.039 |
| EVS-02-38              |                   0.45 | No             |                    2.5 |                              0.079 |                 0.059 |
| EVS-02-39              |                   0.90 | No             |                    2.5 |                              0.115 |                 0.069 |
| EVS-02-75 (0.4 m grid) |                   0.90 | No             |                    2.5 |                              0.115 |                 0.085 |
| EVS-02-74 (0.1 m grid) |                   0.90 | No             |                    2.5 |                              0.115 |                 0.049 |
| EVS-02-76              |                   0.10 | Yes            |                    2.5 |                              0.042 |                 0.102 |
| EVS-02-77              |                   0.45 | Yes            |                    2.5 |                              0.079 |                 0.148 |
| EVS-02-78              |                   0.90 | Yes            |                    2.5 |                              0.115 |                 0.179 |
| EVS-02-79 (0.4 m grid) |                   0.90 | Yes            |                    2.5 |                              0.115 |                 0.181 |
| EVS-02-80 (0.1 m grid) |                   0.90 | Yes            |                    2.5 |                              0.115 |                 0.148 |

EVS-02-77 0.45 Yes 2.5 EVS-02-78 0.90 Yes 2.5 EVS-02-79 (0.4 m grid) 0.90 Yes 2.5 EVS-02-80 (0.1 m grid) 0.90 Yes 2.5 The base case models had a roughness height of 0.1 m (model EVS-02-37) and this model was observed to show more backlayering than the Memorial Tunnel tests (refer to Section 2.2.1). Sensitivity  to  (approximately  10  percent  variations  in)  upstream  velocity  and  FHRR  were considered in development stages, but neither parameter had a major impact on the backlayering extent and thus models with differing effective friction factors were explored. Models were run with a roughness height up to 0.9 m (model EVS-02-78 case), which gave an effective friction factor of 0.183, and as discussed below, these models gave better agreement for backlayering length. Note that the friction factor here is much greater (more than double) than measured in the Memorial Tunnel tests. Further study on near-wall models of turbulent flow is needed to refine this and make a better prediction; however, for this research the roughness height was used as a calibration factor. Grid resolution is also important here and this is discussed further in Section 2.3.9 and Section 2.3.13). ARCHIVED

Thermal conditions around the fire zone were also considered and an insulated boundary was included for a distance 60 m (200 ft.) upstream and downstream of the fire. The insulation material properties were as follows: specific heat capacity (Cp) = 1100 J/kg-K, conductivity (k) = 0.21 W/m/K, density (ρ) = 900 kg/m 3 , emissivity(ε) = 0.5, thickness = 0.15 m [17].

Velocity profile results for the 10 MW fire are provided in Figure 2-13, Figure 2-14, Figure 2-15 and Figure 2-16 for cases with a 0.9 m roughness height and insulated region around the fire. There is an improvement in the result upstream of the fire. The increased wall friction has reduced the backlayering length and thus the velocity prediction is improved (later results in Section 2.3.3

demonstrate that the outcomes are less sensitive to wall thermal properties). A similar result is seen for temperature upstream of the fire.

Downstream of the fire at loop 302, the velocity agreement is not as favorable (Figure 2-16). Figure 2-15 also  shows  comparison  with  test  data as  quoted  in the phase  IV  report  from  the Memorial Tunnel project [10] (Fig 7.6.3-2M). In the phase IV report, CFD modeling was compared with  test  data.  In  some  circumstances  test  data  in  the  phase  IV  report  were  observed  to  be different to the data provided in the comprehensive test report [15]. Agreement between data from the  phase  IV  report  and  CFD  is  improved  relative  to  the  comprehensive  test  report  data.  No reason for this could be determined after looking through the reports, however, the results herein suggest some sort of issue with the test data.

Temperature results are provided in Figure 2-17, Figure 2-18, Figure 2-19 and Figure 2-20. An improved result is seen at loop 307 upstream of the fire, Figure 2-17. Temperature downstream of the fire is mostly unchanged relative to the base case. Overall, the adjustments to wall friction improve conditions in a key area upstream of the fire. Section 2.3.7 and Section 2.3.8 provide some additional sensitivity analyses considering impact of wall friction and tunnel obstructions; the analyses show a sensitivity to both factors. When the wall  friction  or  tunnel  blockages  are  removed,  much  more  backlayering  occurs.  Given  the improvement in prediction of upstream conditions and minor change in predictions downstream, it  was decided to run models with a roughness height of 0.9 m and insulating material thermal properties in the region near the fire. Further research is suggested to improve the correlation between test data and model for the effective friction factor. ARCHIVED

Figure 2-13: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, velocity loop 307 (r value for EVS-02-43).

<!-- image -->

Line chart

Figure 2-14: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, velocity loop 305 (r value for EVS-02-43).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-15: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, velocity loop 304 (r value for EVS-02-43).

Figure 2-16: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, velocity loop 302 (r value for EVS-02-43).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-17: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, temperature loop 307 (r value for EVS-02-43).

Figure 2-18: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, temperature loop 305 (r value for EVS-02-43).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-19: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, temperature loop 304 (r value for EVS-02-43).

<!-- image -->

Line chart

Figure 2-20: Memorial Tunnel (606A, 10 MW) versus CFD, wall conditions sensitivity, temperature loop 302 (r value for EVS-02-43).

<!-- image -->

Stamp

## ARCHIVED

## 2.3 Memorial Tunnel Test 611/612B (50 MW)

## 2.3.1 Bulk Velocity and Fire Heat Release Rate

Bulk velocity and FHRR are the principal parameters for a longitudinal ventilation model for critical or confinement velocity. Consideration of the Memorial Tunnel test data measurements indicates that the upstream velocity and FHRR varied with time and thus when it comes to running a steady state analysis there is some uncertainty in exactly what boundary condition should be applied. Table 2-4 and Table 2-5 provide a sample of some data (measured) from tests 611 and 612B (nominal  50  MW  FHRR)  to  show  the  typical  variation.  In  the  tables  data  are  reported  at measurement loops upstream of the fire, refer to Table 2-1 for measurement loop locations.

The tables show that there is variation in the measured data, with FHRR varying from 44.5 MW to 50.1 MW, and bulk velocity from 1.99 m/s to 3.18 m/s. Some of this variation can be attributed to the changing rate of fuel consumption in the tests. For purposes of comparison, data from each test were time averaged over the period shown here and upstream velocity and FHRR were varied to understand sensitivity of results. For test 611 the average upstream velocity was 2.18 m/s and the FHRR was 45.7 MW. For test 612B the average upstream velocity was 2.76 m/s and the FHRR was 47.9 MW. In developing a CFD model, the variations in FHRR and upstream velocity were not modeled; a model with steady state boundary conditions was developed. The FHRR modeled for this test was 47.2 MW (approximate mid value between minimium and maximum FHRR reported in test data) and the upstream velocity was 2.5 m/s (approximate mid value between minimium and maximum FHRR reported in the test data). Table 2-4: Memorial Tunnel test 611 measured FHRR and bulk velocity [9]. TIME (s) FHRR (MW) LOOP 214 (m/s) LOOP 209 (m/s) LOOP 208 (m/s) LOOP 207 (m/s) 887 45.7 2.11 2.34 2.14 2.38 917 46.0 1.99 2.30 2.06 2.38 947 46.2 2.07 2.24 2.04 2.51 977 46.1 2.02 2.24 2.02 2.26 1007 44.5 2.04 2.47 2.05 2.19 ARCHIVED

|   TIME (s) |   FHRR (MW) | LOOP 214 (m/s) LOOP 209 (m/s)   |           |   LOOP 208 (m/s) |   LOOP 207 (m/s) LOOP 307 (m/s) |   AVG (m/s) |   MAX (m/s) |   MIN (m/s) |
|------------|-------------|---------------------------------|-----------|------------------|---------------------------------|-------------|-------------|-------------|
|        887 |        45.7 | 2.11 2.34                       | 2.14      |             2.38 |                            2.15 |        2.22 |        2.38 |        2.11 |
|        917 |        46.0 | 1.99 2.30                       | 2.06      |             2.38 |                            2.12 |        2.17 |        2.37 |        1.99 |
|        947 |        46.2 | 2.07 2.24                       | 2.04      |             2.51 |                            2.11 |        2.19 |        2.51 |        2.04 |
|        977 |        46.1 | 2.02 2.24                       | 2.02      |             2.26 |                            2.13 |        2.13 |        2.26 |        2.02 |
|       1007 |        44.5 | 2.04                            | 2.47 2.05 |             2.19 |                            2.12 |        2.18 |        2.47 |        2.04 |

Table 2-5: Memorial Tunnel test 612B measured FHRR and bulk velocity [9].

|   TIME (s) |   FHRR (MW) |   LOOP 214 (m/s) |   LOOP 209 (m/s) |   LOOP 208 (m/s) |   LOOP 207 (m/s) |   LOOP 307 (m/s) |   AVG (m/s) |   MAX (m/s) |   MIN (m/s) |
|------------|-------------|------------------|------------------|------------------|------------------|------------------|-------------|-------------|-------------|
|        887 |        49.0 |             2.33 |             2.93 |             2.73 |             2.90 |             3.05 |        2.79 |        3.05 |        2.33 |
|        917 |        48.0 |             2.34 |             2.51 |             3.03 |             3.06 |             2.85 |        2.76 |        3.06 |        2.34 |
|        947 |        46.9 |             2.32 |             3.18 |             2.75 |             3.06 |             2.81 |        2.82 |        3.18 |        2.32 |
|        977 |        50.1 |             2.24 |             2.83 |             2.65 |             2.68 |             2.86 |        2.65 |        2.86 |        2.24 |
|       1007 |        45.6 |             2.41 |             3.14 |             2.69 |             2.75 |             2.81 |        2.76 |        3.14 |        2.41 |

## 2.3.2 Base Case Results

The base  case  analysis  used  an  upstream  velocity  of  2.5  m/s  with  a  FHRR  47.2  MW.  Wall roughness (0.9 m) and an insulated region were used (refer Section 2.2.2). The centerline velocity profile is provided in Figure 2-21 and Figure 2-22 for locations upstream of the fire. Agreement is poor by the Pearson coefficient measure (r) (refer to Table 2-1) at loop 307 (203 ft. upstream), however,  visual  observation  indicates  that  the  situation  is  not  too  bad  with  generally  good qualitative agreement. At loop 305 the velocity profile agreement is very good per the r value, but some of this is attributable to the interpolation routine used to compute the data. There is a point near the ceiling where test and CFD model vary, and this is not picked up in the r value due to the interpolation needed to compute correlations at the same coordinate. The result indicates that the CFD is predicting more backlayer than observed in the test data.

Figure 2-23 and Figure 2-24 provide velocity profiles downstream of the fire and the agreement is fair (per the Pearson coefficient) immediately downstream and poor further away from the fire (loop 302) with the CFD model giving a higher velocity than the test data. Like the results for the 10 MW fire, there is some discrepancy with test data as quoted in the phase IV report from the Memorial Tunnel project [10] (Fig 7.6.5-2B). In the phase IV report, CFD modeling was compared with  test  data.  In  some  circumstances  test  data  in  the  phase  IV  report  were  observed  to  be different to the data provided in the comprehensive test report [15]. Agreement between data from the  phase  IV  report  and  CFD  is  improved  relative  to  the  comprehensive  test  report  data.  No reason for this could be determined after looking through the reports, but the results do suggest an irregularity in the test data. Temperature results upstream of the fire are provided in Figure 2-25 and Figure 2-26. Like the velocity profiles, at loop 307 the agreement per the Pearson coefficient is good, but again, the results are qualitatively better than the r value suggests. Closer to the fire at loop 305 there is some more deviation, which is indicative of the CFD predicting more backlayer, and at this location the r value indicates a poor correlation. ARCHIVED

Figure 2-27 and Figure 2-28 show temperature profiles downstream and trends in the profiles are similar, with very good (per Pearson r value measure) agreement between model and test data. The CFD model under-predicts the temperature field at a location 12.2 m (40 ft.) downstream of the fire. The reason for this is difficult to be certain of but it could be related to the close distance to the fire and some flame dynamics. The CFD model under-predicts temperature at this location; in the Memorial Tunnel work it was noted that the thermocouples at loop 304 may have been reading an increased temperature due to absorption of radiation direct from the fire flames (see [10],  Section  7.6.4-c).  At  a  distance  66.2 m  (217  ft.)  downstream,  the  Pearson  measure agreement is very good. Overall, the 50 MW CFD model is able to provide a prediction of the tunnel environment that is seen to have close comparison with test data. The main notable issues observed were uncertainty in some test data and the CFD model predicting more backlayering.

Figure 2-21: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 307 (EVS-02-51).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-22: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 305 (EVS-02-51).

Figure 2-23: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 304 (EVS-02-51).

<!-- image -->

Line chart

<!-- image -->

Scatter plot

ARCHIVED

Figure 2-24: Memorial Tunnel (612B, 50 MW) versus CFD, velocity loop 302 (EVS-02-51).

Figure 2-25: Memorial Tunnel (612B, 50 MW) versus CFD, temperature loop 307 (EVS-02-51).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-26: Memorial Tunnel (612B, 50 MW) versus CFD, temperature loop 305 (EVS-02-51).

Figure 2-27: Memorial Tunnel (612B, 50 MW) versus CFD, temperature loop 304 (EVS-02-51).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-28: Memorial Tunnel (612B, 50 MW) versus CFD, temperature loop 302 (EVS-02-51).

## 2.3.3 Thermal Boundary Conditions

As noted earlier, the region near the fire is insulated. An insulating material was modeled in the base case model. To test the sensitivity of the CFD result to this condition the runs were repeated with  the  insulated  zone  having  an  adiabatic  boundary  condition.  Results  are  provided  in Figure 2-29,  Figure 2-30,  Figure 2-31,  Figure 2-32,  Figure 2-33,  Figure 2-34,  Figure 2-35  and Figure 2-36. In general, the results do not appear much different to the base case results. There is a slight increase in the temperature downstream of the fire, refer to Figure 2-35 and Figure 2-36. The increase is small, and differences in other results negligible, that it is concluded that the thermal boundary conditions have a minor impact in this case. Backlayer length was 146 ft. for this case versus 111 ft. for the base case.

Figure 2-29: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 307 (r value for EVS-02-48).

<!-- image -->

Line chart

Figure 2-30: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 305 (r value for EVS-02-48).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-31: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 304 (r value for EVS-02-48).

Figure 2-32: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, velocity loop 302 (r value for EVS-02-48).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-33: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 307 (r value for EVS-02-48).

Figure 2-34: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 305 (r value for EVS-02-48).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-35: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 304 (r value for EVS-02-48).

<!-- image -->

Line chart

Figure 2-36: Memorial Tunnel (612B, 50 MW) versus CFD, adiabatic region near to the fire, temperature loop 302 (r value for EVS-02-48). 2.3.4 Turbulence Model Parameters Sensitivity  to  the  turbulence  model  was  tested  for  two  conditions.  In  one  case,  the  dynamic Smagorinsky turbulence model  was used, and  in  the  other  themodel  closure  coefficient  was changed from the default value of 0.1 to 0.2. Further information on the turbulence models can be found in the FDS User's Guide [8]. For cases using the dynamic Smagorinsky model, results for the velocity profile on the centerline are provided  in  Figure 2-37,  Figure 2-38,  Figure 2-39  and  Figure 2-40.  The  changes  from  the base case model are negligible. Temperature results are provided in Figure 2-41, Figure 2-42, Figure 2-43 and Figure 2-44. Improvement in the temperature prediction downstream of the fire at loop 304 is noted, although the overall differences are minor once away from this near-fire region. Backlayering length was only slightly affected. ARCHIVED

For cases with a different closure coefficient (0.2 instead of 0.1), results for velocity are provided in  Figure 2-45,  Figure 2-46,  Figure 2-47  and  Figure 2-48.  Sensitivity  of  the  model  results  is negligible.  Temperature  results  are  provided  in  Figure 2-49,  Figure 2-50,  Figure 2-51  and Figure 2-52. Improvement in the temperature prediction downstream of the fire at loop 304 is noted, although the overall differences are minor. Backlayer length was 146 ft. for this case versus 111 ft. for the base case.

Figure 2-37: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-53).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-38: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-53).

Figure 2-39: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-53).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-40: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, velocity loop 302 (r value for EVS-02-53).

Figure 2-41: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 307 (r value for EVS-02-53).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-42: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 305 (r value for EVS-02-53).

Figure 2-43: Memorial Tunnel (612B, 50 MW) versus CFD, dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-53).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-44: Memorial Tunnel (612B, 10 MW) versus CFD, dynamic Smagorinsky model, temperature loop 302 (r value for EVS-02-53).

Figure 2-45: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 307 (r value for EVS-02-54).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-46: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 305 (r value for EVS-02-54).

Figure 2-47: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 304 (r value for EVS-02-54).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-48: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, velocity loop 302 (r value for EVS-02-54).

Figure 2-49: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 307 (r value for EVS-02-54).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-50: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 305 (r value for EVS-02-54).

Figure 2-51: Memorial Tunnel (612B, 50 MW) versus CFD, closure coefficient set to 0.2, temperature loop 304 (r value for EVS-02-54).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-52: Memorial Tunnel (612B, 10 MW) versus CFD, closure coefficient set to 0.2, temperature loop 302 (r value for EVS-02-54).

## 2.3.5 Upstream Velocity

Base case results had an upstream velocity of 2.5 m/s (492 fpm). As noted in Section 2.3.1 there is some variation in the upstream velocity between the different cases in the tests. For test 612B, the average velocity ranged from 2.7 m/s to 2.8 m/s (531 fpm to 551 fpm), with a minimum of 2.2 m/s (433 fpm) and maximum of 3.2 m/s (457 fpm). For test 611, the average velocity ranged from 2.1 m/s to 2.2 m/s (413 fpm to 433 fpm), with a minimum of 2.0 m/s (394 fpm) and maximum of 2.5 m/s (492 fpm). Consideration of velocity profiles in Figure 2-21 and Figure 2-22, suggest that the upstream velocity in the CFD models was slightly higher than tests. Comparison of base case results with test 611 data is made to provide further insight, where the upstream velocity in the test was less than the CFD by a greater magnitude. The model is otherwise the same as the base case (EVS-02-51).

Velocity  profile  results  are  provided  in  Figure 2-53,  Figure 2-54,  Figure 2-55  and  Figure 2-56. There is a slight improvement between CFD and test data just upstream of the fire, at loop 305, but otherwise, the changes between the cases are negligible. Temperature profile results are provided in Figure 2-57, Figure 2-58, Figure 2-59 and Figure 2-60. Changes between the test and CFD are minor. ARCHIVED

Figure 2-53: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, velocity loop 307 (r value for EVS-02-47 compared to test 611).

<!-- image -->

Line chart

Figure 2-54: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, velocity loop 305 (r value for EVS-02-47 compared to test 611).

<!-- image -->

Line chart

<!-- image -->

Scatter plot

ARCHIVED

Figure 2-55: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, velocity loop 304 (r value for EVS-02-47 compared to test 611).

Figure 2-56: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, velocity loop 302 (r value for EVS-02-47 compared to test 611).

<!-- image -->

Scatter plot

<!-- image -->

Line chart

ARCHIVED

Figure 2-57: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, temperature loop 307 (r value for EVS-02-47 compared to test 611).

Figure 2-58: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, temperature loop 305 (r value for EVS-02-47 compared to test 611).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-59: Memorial Tunnel (612B, 50 MW) versus CFD, comparison to test 611, temperature loop 304 (r value for EVS-02-47 compared to test 611).

<!-- image -->

Line chart

<!-- image -->

Logo

Figure 2-60: Memorial Tunnel (612B, 10 MW) versus CFD, comparison to test 611, temperature loop 302 (r value for EVS-02-47 compared to test 611). 2.3.6 Fire Heat Release Rate The FHRR was uncertain in the tests, by around 10 percent. A case was run with the FHRR reduced from 47.2 MW to 42.2 MW. The upstream velocity was 2.5 m/s, consistent with the base case scenarios. Results are provided in Figure 2-61, Figure 2-62, Figure 2-63 and Figure 2-64 for velocity, and Figure 2-65, Figure 2-66, Figure 2-67 and Figure 2-68 for temperature. Results vary to a very minor extent, principally, the temperature downstream of the fire is slightly lower with the reduced FHRR. Backlayering length predicted in the models was the same for both cases, at a distance of approximately 111 ft. ARCHIVED

Figure 2-61: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 307 (r value for EVS-02-63).

<!-- image -->

Scatter plot

<!-- image -->

Line chart

ARCHIVED

Figure 2-62: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 305 (r value for EVS-02-63).

Figure 2-63: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 304 (r value for EVS-02-63).

<!-- image -->

Line chart

<!-- image -->

Scatter plot

ARCHIVED

Figure 2-64: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, velocity loop 302 (r value for EVS-02-63).

Figure 2-65: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 307 (r value for EVS-02-63).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-66: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 305 (r value for EVS-02-63).

Figure 2-67: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 304 (r value for EVS-02-63).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-68: Memorial Tunnel (612B, 50 MW) versus CFD, FHRR variation, temperature loop 302 (r value for EVS-02-63).

## 2.3.7 Wall Roughness

Wall roughness in base case models was set to 0.9 m. The sensitivity to this was tested by running a  case  with  wall  roughness  set  to  0  m  (smooth  walls).  Consideration  of  the  velocity  profile upstream of the fire, refer Figure 2-69 and Figure 2-70, indicates a difference in the results. The CFD model is now showing a large degree of backlayering with smooth walls.

Backlayering versus time for the base case and the smooth wall case is shown in Figure 2-71. Backlayering  was  measured  based  on  temperature  at  the  tunnel  ceiling.  The  degree  of backlayering is greatly increased when smooth walls are used.

Figure 2-69: Memorial Tunnel (612B, 50 MW) versus CFD, smooth walls, velocity loop 307 (r value for EVS-02-50).

<!-- image -->

Line chart

ARCHIVED

Figure 2-70: Memorial Tunnel (612B, 50 MW) versus CFD, smooth walls, velocity loop 305 (r value for EVS-02-50).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-71: Memorial Tunnel (612B, 50 MW) CFD, backlayering versus time with smooth walls and obstructions (both cases).

## 2.3.8 Tunnel Obstructions

The base case CFD models had tunnel obstructions modeled to represent the measurement trees, refer to Figure 2-12. The previous section highlighted a sensitivity to wall roughness, but the possibility that blockages were responsible for backlayering control was also explored.

A case was run with the blockages removed. That case showed substantially more backlayering than the base case. Refer to Figure 2-72. This indicated that the blockages also play a significant role in the degree of backlayering.

Figure 2-72: Memorial Tunnel (612B, 50 MW) CFD, backlayering versus time with rough walls (roughness height 0.9 m) and no obstructions (EVS-02-62).

<!-- image -->

Line chart

## 2.3.9 Grid Resolution

The base case models had a grid resolution of 0.2 m. Sensitivity to the grid was tested by running with a 0.1 m grid and a 0.4 m grid.

ARCHIVED

Comparison  of  velocity  profiles  is  provided  in  Figure 2-73,  Figure 2-74,  Figure 2-75  and Figure 2-76. The variation between the 0.1 m grid and 0.2 m grid is minor except at the loop 203 feet  upstream,  Figure 2-73.  At  this  location  results  are  indicative  of  the  finer  grid  case predicting more backlayering. The grid resolution of 0.4 m gives reasonable results relative to the 0.2 m grid, with only some small differences except as mentioned 203 feet upstream.

For temperature profiles, comparison is provided in Figure 2-77, Figure 2-78, Figure 2-79 and Figure 2-80. The results show almost identical solutions between the 0.1 m and 0.2 m grid, except at the upstream location where there is evidence of more backlayering, Figure 2-77. The coarse grid results (0.4 m) show greater temperature variation downstream of the fire, with a tendency to show lower magnitudes of temperature. While the coarse grid case (EVS-02-64) still exhibits the same trends as the finer grids, the improved resolution of temperature downstream of the fire suggests  the  finer  grid  case  should  be  utilized;  at  least  for  models  using  a  mixing-controlled approach. It is noted that a coarse grid could give acceptable results for initial runs to help narrow down  the  key  aspects  of  an  investigation,  provided  sensitivity  to  engineering  conclusions  is checked.

Figure 2-81 shows the backlayering distance versus time for the three grid resolutions. The finer grid cases show the greatest amount of backlayering. Figure 2-82 shows a visualization of the backlayering  distance  for  the  0.2  m  and  0.1  m  grids.  The  result  shows  a  difference  of  18 m (59 feet) in the backlayering distance. From the point of view of the CFD modeling method, it would be of interest to run a finer grid, at 0.05 m, to see if the backlayering distance converges. However, this would take a model with around 90 million cells and the run time would take months, thus making this a topic for future research.

<!-- image -->

Logo

In all cases the backlayering is not progressing more with time, the smoke layer remains in the ceiling  region,  and  the  fire  is  at  the  peak  FHRR.  From  the  smoke  control  point  of  view,  for engineering design impact, these results do not show a difference that is likely to have an impact on life safety outcomes. Either grid resolution gives reasonable results. Care should be taken when interpreting backlayering distance as this parameter can be sensitive to the grid resolution; trends can be inferred on grids that are coarse (0.4 m) but sensitivity to a finer grid (0.2 m) should be considered, and if the backlayering distance needs to be determined with greater confidence, then a 0.1 m grid might be in order. Cold flow results to determine tunnel friction factor, reported in Table 2-3, note an overall friction factor on the 0.2 m grid of 0.179, on the 0.4 m grid it is 0.181 and on the 0.1 m grid it is 0.148. The backlayering distance appears to correlate fairly well with the effective friction factor in the tunnel, with the finest grid giving the lowest effective friction factor and most backlayering. ARCHIVED

Figure 2-73: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 307 (r value for EVS-02-71).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-74: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 305 (r value for EVS-02-71).

Figure 2-75: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 304 (r value for EVS-02-71).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-76: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, velocity loop 302 (r value for EVS-02-71).

Figure 2-77: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 307 (r value for EVS-02-71).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-78: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 305 (r value for EVS-02-71).

Figure 2-79: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 304 (r value for EVS-02-71).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-80: Memorial Tunnel (612B, 50 MW) versus CFD, grid resolution test, temperature loop 302 (r value for EVS-02-71).

Figure 2-81: Memorial Tunnel (612B, 50 MW) backlayer distance versus time for varying grid resolution.

<!-- image -->

Line chart

<!-- image -->

Engineering drawing

ARCHIVED

Figure 2-82: Visualization of backlayering differences for 0.2 m and 0.1 m grids.

## 2.3.10 Volumetric Heat Source

Volumetric heat source models were developed to examine whether this method of modeling the fire  would produce reasonable results. Models used a relatively coarse grid for base cases at 0.4 m, and the base case models did not include the radiative heat (30 percent radiative heat fraction was used). The approach with radiative heat is consistent with other modeling methods using a volumetric heat source, including the Memorial Tunnel work [10]. The size of the fire volume was chosen using the Memorial Tunnel work as a guide, with a FHRR per unit volume, with  radiation  heat  excluded,  on  the  order  of  500 kW/m 3 .  The  numerical  grid  caused  slight variations from this and in the models a volume size of 6 m (L) by 4 m (W) by 2.8 m (H) was used with a FHRR per unit volume of 520.833 kW/m 3 . This equates to a convective FHRR of 35 MW, which is a nominal 50 MW when the radiation component is considered.

Results  comparing  velocity  profiles  are  provided  in  Figure 2-83,  Figure 2-84,  Figure 2-85  and Figure 2-86. General agreement between the mixing-controlled models and the volumetric heat source models is observed. Data from the Memorial Tunnel work Phase IV report (CFD models) were available at loop 302 and Figure 2-86 shows the results. The Memorial Tunnel Phase IV models gave similar results except for the dip in velocity magnitude, which is likely attributable to the jet fans modeled. Results at other loops as modeled herein were not published in the report.

Temperature profiles are compared in Figure 2-87, Figure 2-88, Figure 2-89, and Figure 2-90. Upstream  of  the  fire  the  agreement  (per  the  Pearson  r-value  measure  in  Table 2-1)  for temperature profiles is very good, and downstream the only exception is the result 12.2 m (40 ft.) downstream of the fire. The volumetric heat source models do not predict the flaming region of the fire, and the poor agreement here is consistent with observations made in the Memorial Tunnel tests that the thermocouple measurements in the region near to the fire were affected by radiation direct  from  the  fire  (see  [10],  Section  7.6.4-c).  Results  in  Figure 2-90  provide  comparison  of temperatures with the Memorial Tunnel phase IV report CFD models at loop 302; the previous CFD predicts a slightly higher temperature near the ceiling and slightly lower at the roadway, however, the overall behavior (shape and magnitude) of the profile is in agreement. Additional  results  are  included  in  Figure 2-91  and  Figure 2-92  for  locations  29.6 m  (97 ft.) upstream and downstream of the fire,  respectively.  Through  the  r-value  (Pearson  coefficient) measure the results at the location upstream are in very good agreement with the test, suggesting the volumetric heat source approach predicts slightly less backlayering than the mixing-controlled method. Downstream of the fire results between the CFD models are in closer agreement with each other and the tests, supporting the hypothesis that the region 12.2 m (40 ft.) downstream of the fire is affected by proximity to the flaming region and the CFD model not always predicting the environment as accurately in this area. ARCHIVED

As  noted,  the  volumetric  heat  source  used  was  on  the  order  500 kW/m 3 .  Sensitivity  to  this parameter  has  not  been  conducted  in  this  research  since  the  boundary  conditions  were comparable  to  previous  CFD  conducted  for  the  Memorial  Tunnel  [10].  Further  research  is suggested to check the impact of this parameter, and also when conducting a CFD study using this  approach  the  temperature  predictions  should  be  checked  against  typical  fire  plume temperatures. If the volume is too small excessive fire temperatures could result, but if too large the temperatures might be too small.

Figure 2-83: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 307 (r value for EVS-02-66).

<!-- image -->

Scatter plot

<!-- image -->

Line chart

ARCHIVED

Figure 2-84: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 305 (r value for EVS-02-66).

Figure 2-85: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 304 (r value for EVS-02-66).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-86: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, velocity loop 302 (r value for EVS-02-66).

Figure 2-87: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 307 (r value for EVS-02-66).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-88: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 305 (r value for EVS-02-66).

Figure 2-89: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 304 (r value for EVS-02-66).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-90: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 302 (r value for EVS-02-66).

Figure 2-91: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 306 (r value for EVS-02-66).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-92: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source versus mixing-controlled model, temperature loop 303 (r value for EVS-02-66).

## 2.3.11 Volumetric Heat Source Radiation Included

Models were conducted using the volumetric heat source with radiation included. The radiation model used in FDS is based on a finite volume method using angular discretization, where the volumes are associated with the solid angle for radiation transmission [18]. Aspects surrounding radiation model validation are discussed at length in the FDS validation guide [19]. Note that the Memorial Tunnel phase IV CFD models used a six flux radiation model [10].

Refer to Figure 2-93, Figure 2-94, Figure 2-95 and Figure 2-96 for velocity profile results. Some minor differences are observed downstream of the fire, with the models including radiation giving slightly higher velocity, which is attributable to some of the radiant heat increasing the overall temperature. Figure 2-97, Figure 2-98, Figure 2-99 and Figure 2-100 show temperature profiles. As expected, temperatures with radiation included are slightly higher relative to the base case. At the location 12.2 m (40 ft.) downstream of the fire, Figure 2-99, there is very little change in results with the CFD model still under estimating temperature relative to the test at this location. Although radiation is included in the model it doesn't necessarily capture the physics of the flame near to the fire which means that peak temperatures, attributable to radiation from flame impingement in the  tests,  would  not  necessarily  be  accurately  captured  in  this  case  where  no  flame  front  is resolved. ARCHIVED

Figure 2-93: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 307 (r value for EVS-02-67).

<!-- image -->

Line chart

Figure 2-94: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 305 (r value for EVS-02-67).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-95: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 304 (r value for EVS-02-67).

Figure 2-96: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, velocity loop 302 (r value for EVS-02-67).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-97: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 307 (r value for EVS-02-67).

Figure 2-98: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 305 (r value for EVS-02-67).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-99: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 304 (r value for EVS-02-67).

<!-- image -->

Line chart

<!-- image -->

Logo

Figure 2-100: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and radiation, temperature loop 302 (r value for EVS-02-67). 2.3.12 Volumetric Heat Source with Dynamic Smagorinsky Model Models were conducted using the volumetric heat source with the dynamic Smagorinsky model for turbulence. Refer to Figure 2-101, Figure 2-102, Figure 2-103 and Figure 2-104 for velocity profile results. No appreciable differences in the results are observed. Figure 2-105, Figure 2-106, Figure 2-107  and  Figure 2-108  show  temperature  profiles.  No  appreciable  differences  in  the results are observed. ARCHIVED

Figure 2-101: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 307 (r value for EVS-02-68).

<!-- image -->

Scatter plot

<!-- image -->

Line chart

ARCHIVED

Figure 2-102: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 305 (r value for EVS-02-68).

Figure 2-103: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 304 (r value for EVS-02-68).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-104: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, velocity loop 302 (r value for EVS-02-68).

Figure 2-105: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 307 (r value for EVS-02-68).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-106: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 305 (r value for EVS-02-68).

Figure 2-107: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 304 (r value for EVS-02-68).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-108: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and dynamic Smagorinsky model, temperature loop 302 (r value for EVS-02-68).

## 2.3.13 Volumetric Heat Source with Refined Grid

The base case volumetric heat source models were conducted on cases with a nominal grid resolution of 0.4 m. The base case was rerun with a grid resolution of 0.2 m and 0.1 m to test the sensitivity of results. Velocity profiles are provided in Figure 2-109, Figure 2-110, Figure 2-111 and Figure 2-112. Overall agreement shows similar results between the different grids, but the finest grid (0.1 m) is showing results indicative of the finer grid predicting more backlayering, which is similar to observations made previously on the mixing-controlled models (refer Section 2.3.9).

Temperature results show are compared in Figure 2-113, Figure 2-114 for locations upstream of the  fire.  The  results  here  are  indicative  of  the  finest  grid  predicting  more  backlayering. Figure 2-115 and Figure 2-116 provide results 40 ft. and 217 ft. downstream of the fire. At the 40 ft. location the finest grid gives an increased magnitude of temperature and a closer match to the test data (though still an under-prediction like observed in other models herein). At the 217 ft. location the difference is less pronounced although the trend is similar with the finest grid giving an increased magnitude.

<!-- image -->

Line chart

The three grid resolutions give results that exhibit the general trends seen in the test data and seen previously on mixing-controlled models of the same case (refer Section 2.3.9). As noted in Section 2.3.9 care should be taken when interpreting backlayering distance as this parameter can be sensitive to the grid resolution; trends can be inferred on grids that are coarse (0.4 m) but sensitivity to 0.2 m should be considered, and if the backlayering distance needs to be determined with greater confidence, then a 0.1 m grid might be in order. ARCHIVED

Figure 2-109: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 307 (r value for EVS-02-73).

Figure 2-110: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 305 (r value for EVS-02-73).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-111: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 304 (r value for EVS-02-73).

Figure 2-112: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, velocity loop 302 (r value for EVS-02-73).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-113: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 307 (r value for EVS-02-73).

Figure 2-114: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 305 (r value for EVS-02-73).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 2-115: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 304 (r value for EVS-02-73).

<!-- image -->

Line chart

Figure 2-116: Memorial Tunnel (612B, 50 MW) versus CFD, volumetric heat source and refined grid, temperature loop 302 (r value for EVS-02-73) 2.4 Research Findings and Suggested Practices Based on Findings In this chapter FDS has been used to model the Memorial Tunnel tests with longitudinal ventilation for fires with nominal FHRRs of 10 MW and 50 MW. Larger fires (100 MW) have been considered in other studies also [20]. The main findings and suggested practices are summarized below. 2.4.1 Upstream Velocity Magnitude and FHRR Upstream velocity and FHRR are important parameters for longitudinal smoke control since they are boundary conditions for determining the smoke control effectiveness via backlayering control. The FHRR is a difficult parameter to measure precisely during a fire test as it can vary with time due to the inherent unsteady nature of fire. The upstream velocity can also vary in a full-scale tunnel fire test as a result of the varying FHRR. Variations of 10 percent were noted in the test data and sensitivity to changes on the order of 10 percent was tested (refer to Section 2.3.5 and Section 2.3.6). The overall impact on results when compared with test data was minor. ARCHIVED

The suggested practice for CFD models of longitudinal velocity is to consider the sensitivity of results to changes in upstream velocity and FHRR by a magnitude of around 10 percent.

## 2.4.2 Wall Heat Transfer

There was an insulated region around the fire and the wall heat transfer in this region might have had an impact on the outcomes. Sensitivity was tested and changes were minor (refer to Section 2.3.3). Since the wall heat transfer parameters are relatively simple to determine and model, the suggested practice for CFD modeling is to implement wall heat transfer material properties that match the physical implementation as closely as practical.

## 2.4.3 Wall Friction and Tunnel Obstructions

Wall friction and tunnel blockages were shown to have a significant effect on backlayering (refer to Section 2.2.2, Section 2.3.7 and Section 2.3.8). If a tunnel is likely to have vehicles upstream of the fire, or there are significant near-wall obstructions (e.g., lighting and FFFS piping), then the backlayering  might  be  reduced  in  a  situation  that  includes  the  effect  of  these  features.  It  is important to note, however, that while an increased wall friction factor and tunnel blockage might decrease the extent of backlayering, that a greater demand is placed on the ventilation system. For instance, if using jet fans for longitudinal ventilation, this increase could amount to more fans needed to overcome the friction and achieve the target velocity.

Caution is suggested when relying on blockages to achieve a certain degree of smoke control. More blockages tend to improve smoke control and reduce the free stream velocity needed to contain  smoke,  however, assumptions on  the  degree  of blockage  likely  and  sensitivity  to not achieving the assumptions should be tested. Wall friction can have a significant impact on smoke control, and it is suggested to keep the modeled wall friction factor low, on the order of 0.02 to 0.03 (roughness heights 0.1 m or less). This is typical for a concrete lined tunnel and it generates a conservative outcome for smoke management (a higher velocity magnitude) with respect to cases modeled with much higher friction factors. 2.4.4 Turbulence Model The  dynamic  Smagorinsky  model  performs  slightly  better  on  cases  using  mixing-controlled combustion. However, the improvements overall are minor and there's little net advantage to using a model different to the default turbulence models in FDS. When running with a volumetric heat source, the differences due to turbulence model are negligible. The suggested practice is to run models using default settings in FDS. 2.4.5 Fire Representation ARCHIVED

Mixing-controlled models and volumetric heat source models both gave a reasonable prediction of the tunnel environment during a fire with longitudinal ventilation. The mixing-controlled model is based on a more detailed representation of fire as it models a combustion process [1]. However, both models could produce a similar prediction of the tunnel environment with respect to test data, except that the volumetric heat source model did not perform as well in the region just downstream of the fire for temperature prediction on both coarse and fine grids (refer to Section 2.3.10 and Section 2.3.13).

Volumetric heat source models gave results in qualitative agreement to the test data on cases with  a  coarse  grid  (0.4  m)  and  no  radiation  included,  which  is  consistent  with  previous  CFD modeling conclusions [10]. This has an advantage for engineering work at early stages of a project as these models can run much faster. Sensitivity needs to be checked, but for the purposes of screening initial concepts and identifying trends, it is advantageous to have a model that can run in a less than a day, versus a week or more. Caution should be exercised if using volumetric heat source models since this method does not predict temperature of the flame (peak temperature output is a function of FHRR, volume size and upstream velocity).

In terms of suggested practices, a volumetric heat source or mixing-controlled approach can be used.  Coarse  grid  (0.4 m)  volumetric  heat  source  models  can  be  used  to  quickly  test  initial concepts but sensitivity to grid resolution and mixing-controlled approaches should be checked for key cases used to develop a design basis. A FHRR per unit volume on the order of 500 kW/m 3 was used for cases herein, which is consistent with previous studies [10]. Volumetric heat source models are not suggested for use when models need to resolve the flame temperature, such as models to predict structure temperatures due to fire.

## 2.4.6 Grid Resolution

Dependence of the solution on grid resolution was considered and cases with 0.4 m, 0.2 m and 0.1 m grids were tested. For the mixing-controlled models there was a sensitivity to grid resolution in going from 0.4 m to 0.2 m (refer to Section 2.3.9) although this was only observed at the location just  downstream of  the  fire  (40 ft.  downstream,  refer  to  Figure 2-79).  For  the  volumetric  heat source models, a similar result was observed; changes to results based on grid resolution were observed at a location 40 ft. downstream between grids 0.2 m and 0.1, refer to Figure 2-115).

Backlayering was sensitive to grid resolution and this is attributable to the changes in wall friction, with finer grids giving less wall friction (refer to Section 2.2.2 and Section 2.3.9). For  initial  screening  models  a  grid  resolution  of  0.4 m  is  suggested.  Sensitivity  to  this  grid resolution  should  be  checked,  with  a  resolution  down  to  at  least  0.2 m  (for  either  fire  model approach). A grid resolution of 0.1 m is generally not suggested unless a more precise prediction of backlayering distance is needed. It is also suggested that models be run with effective wall friction factor on the order of 0.02 and that this be checked with a cold flow model to verify the friction factor for the grid under consideration (refer to Section 2.2.2). Although models herein were run with much larger friction factors (on the order 0.1), this was done because of calibration with respect to available test data, which is not typically available when approaching a new design. In terms of a conservative result for smoke control (higher upstream velocity), a case with lower wall friction is thus suggested. 2.5 Suggested Areas for Further Research Based on the findings herein and items that could not be fully resolved within the scope of this research project, potential areas for further research include the following: ARCHIVED

- Grid resolution - A sensitivity of backlayering length to grid resolution was identified, with finer grids tending to predict more backlayering. Wall models in FDS are discussed in the technical reference  guide  and  user  guide  [18]  [19].  Near-wall  turbulent  flow  and  heat  transfer  are complex  issues  in  CFD  modeling  and  are  a  possible  cause  of  the  backlayering  distance changes, since results in Section 2.2.2 showed a sensitivity of model friction factor to grid resolution.
- Memorial Tunnel test data - In some instances discrepancies were identified between the Memorial  Tunnel  Report  test  data  [9]  and  the  data  reported  in  the  phase  IV  CFD  model validation  [10].  While  the differences  were  mostly  minor,  future  research efforts  to  resolve these items could be beneficial.

## 3 CFD MODEL VALIDATION - FIXED FIRE FIGHTING SYSTEM

The Singapore Land Transport Authority (LTA) conducted fire tests in 2012 in the San Pedro de Anes Tunnel with a fire load representative of a heavy goods vehicle with FFFS operating [11] (referred to herein as the "LTA" tests). These tests were used as part of the CFD model validation process.  The  purpose  was  to  validate  the  ability  of  the  CFD  model  to  predict  the  thermal environment in the tunnel with the FFFS operating.

## 3.1 Overview

## 3.1.1 LTA Tests

Tests were conducted with fire loads that were mock-ups of a heavy goods vehicle. The fire load consisted  of  wood  pallets  and  a  total  of  seven  fire  tests  were  run.  Six  of  the  tests  included operation  of  the  FFFS  and  one  of  the  tests  was  a  free  burn.  The  tunnel  was  ventilated longitudinally. Test 4 was considered for the validation exercise herein. This test included FFFS operating at 12 mm/min (0.3 gpm/ft 2 ) using a standard (pendant) nozzle with activation at 400 seconds  after  the  start  of  the  fire.  The  FHRR  and  temperature  downstream  of  the  fire  were measured in the tests. Figure 3-1 shows the FHRR measured. The tunnel was 23.9 ft. (7.3 m) wide, 17.1 ft. (5.2 m) high, and 1968 ft. (600 m) long. The cross section was rectangular at the test section. In the tests, longitudinal ventilation was at 2.8 m/s to 3 m/s (550 fpm to 590 fpm). The full-scale FFFS tests considered scenarios with a standard spray (pendant) sprinkler head, and a directional nozzle. For the FFFS configuration a total of 46 nozzles were used in the tests over a zone length of 50 m (164 ft.). Nozzles were arranged in three evenly spaced rows across the tunnel width and evenly spaced longitudinally within the zone of operation. The fire was (longitudinally) positioned in the center of the FFFS zone and on the tunnel centerline. Each nozzle covered an area of 9 m 2 (96.8 ft 2 ) with an operating pressure limited to 5 bar. At the water application rate quoted, this equates to a nozzle flow rate of 108 L/min (28.5 gpm) and a K factor of 48 L/min/bar 1/2 . Key measurements from the tests that were reported in the literature and are used for comparison here  included  the  temperature  downstream  of  the  fire and heat flux.  Refer  to  Figure 3-2 and Figure 3-3. ARCHIVED

Figure 3-1: Fire heat release rate profile with FFFS operating (LTA test 4) [11].

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-2: Test data, gas temperature 5 m to 10 m downstream of the fire with FFFS (LTA test 4) [11].

Figure 3-3: Test data, heat flux downstream of the fire with FFFS (LTA test 4) [11].

<!-- image -->

Line chart

## 3.1.2 CFD Models

A CFD model was developed to represent test 4 from the LTA tests. Details of the models are summarized in Table 3-1. Key CFD model parameters considered included the following:

- Model boundary conditions - Variation of the FHRR with time was considered as this was found to be a potential source of variation between CFD model and test data.
- Nozzle parameters - Models were developed determine parameters such as spray angles and droplet velocity for the FDS representation. Sensitivity to droplet size was considered.
- Fire representation - Models with a mixing-controlled approach and a volumetric heat source were considered. The mixing-controlled approach is the default in FDS. A volumetric heat source was used in the previous section and cases using were considered herein with FFFS included.
- Grid resolution - Dependence of the solution on grid resolution was considered.

ARCHIVED

Table 3-1: LTA test CFD model parameters.

| ITEM                               | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Grid                               | For the CFD models a grid resolution was used as follows: 0.2 m in the longitudinal direction, 0.2 m in the width and vertical directions. Rectangular tunnel geometry per the test geometry. Tunnel dimensions were rounded to the nearest 0.2 m to fit the grid resolution used (the model was made 7.2 m wide). A CFD model approximately 125 m long was used for analysis herein. This is shorter than the domain used for the Memorial Tunnel models because backlayering was not reported in the tests and thus was not expected to be observed in models. The fire was placed approximately 70 m from the inlet of the CFD domain.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Fire and FHRR                      | For the CFD models, the FHRR was set to vary with time based on the profile used in the original work. Figure 3-1 provides the FHRR profile. The fire load in the original test was comprised of wood pallets. The geometry of a pallet is such that it has features which are smaller than can be resolved with the grid. Given that detailed combustion processes are not being modeled it was not considered necessary to model the pallet geometry in detail. Thus, pallets were represented as blocks, each having an area of 3.52 m 2 (37.9 ft 2 ), with a total of 30 pallets (three layers, two rows of five pallets per row). The pallets were assumed to all burn simultaneously in the model and the peak FHRR per unit area was 276.47 kW/m 2 . A target (used in the tests to assess fire spread) of wood pallets was included downstream of the main fire load for the testing and in the CFD model, but in the tests with FFFS this target did not ignite and thus no FHRR was specified for this downstream target in the models. Figure 3-4 shows a typical fire geometry from the CFD model. ARCHIVED |
| Inlet boundary and outlet boundary | Inlet boundary condition was a fixed upstream velocity of 3 m/s (590 fpm) which is consistent with the tests. Outlet boundary was an open boundary per FDS User Guide [8].                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Wall boundary condition            | The walls were modeled as smooth walls (roughness height of 0 m). The thermal properties of the walls were based on concrete with a specific heat of 880 J/kg/K, density of 2000 kg/m 3 , conductivity of 1.3 W/m/K and emissivity of 0.9 [21]. The walls had an insulated back with a thickness of 1.0 m.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| FDS parameters                     | Simulation of long tunnels sometimes results in numerical instability in the FDS models. Remedies are noted in the FDS User Guide [8] and include setting the specific heat to be constant and adjusting pressure solver parameters. Adding micro vents along the tunnel length is also sometimes used to help with stability problems although this was not necessary in this case. The FDS version used was FDS6.7.5-578-gc15229f4f-nightly. The nominal version number was 6.7.5 and the nightly release from 30 November 2020 was used since the version addressed some issues with FFFS discovered during validation. Note that in the time after the models for this work were conducted, that updates to the FDS software have been made to address stability issues with tunnel models [22]. The impact of these updates was not considered in this report.                                                                                                                                                                                                                                                     |

| ITEM                                                       | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fuel                                                       | The fuel is modeled in FDS to represent a typical polymer, with the chemical formula CH 1.8 N 0.05 O 0.3 and a soot yield of 0.131 and CO yield of 0.01. Heat of combustion for these fuel parameters in the CFD model is 23,468 kJ/kg. This is assumed to not have any major effect on backlayering or temperature and velocity prediction. A volumetric heat source is used in some models and discussion relevant to the model set up is provided in the specific section presenting those results.                                                                   |
| Measurement loop locations relative to the fire centerline | Measurement locations were situated on the tunnel centerline 5 m or 10 m downstream of the fire. There was some uncertainty as to the exact location of the measurements so data were recorded 5 m and 10 m downstream.                                                                                                                                                                                                                                                                                                                                                  |
| Comparison based on linear correlation                     | Results are compared between test data and the CFD model using a Pearson correlation coefficient (r) to measure how well the data are agreeing based on a linear correlation. Strength of association between test data and CFD is taken to be poor (r value between 0.0 and 0.25), fair (r value between 0.25 and 0.5), good (r value between 0.5 and 0.75) or very good (r value between 0.75 and 1.0). Negative r values represent a situation where the linear correlation between variables trends toward the straight-line interpretations having opposite slopes. |

<!-- image -->

Icon

## 3.2 Representation of FFFS Nozzles

Figure 3-4: Fire geometry for the LTA CFD model. ARCHIVED

Nozzle parameters (droplet size, spray pattern, model, and manufacturer) were not published in the LTA test publication. The nozzle was known to be a standard spray pendant type with a flow rate of 108 L/min at a pressure up to 5 bar, giving a K factor of approximately 48 L/min/bar 1/2 . Manufacturer data and research publications were consulted to establish the approximate nozzle droplet diameter and spray patterns as follows:

- Based on tests of similar nozzles (standard spray pendant) at similar pressures, a droplet diameter (median volumetric diameter, Dv,0.5) in the range of 0.5 mm to 1.2 mm was assumed [23]. Sensitivity to the median droplet diameter was tested.

- A typical nozzle spray pattern is illustrated in Figure 3-5. Based on the nozzle being a standard spray  pendant  type,  manufacturer  data  were  consulted  to  establish  a  spray  pattern  as informed by a nozzle with a similar K factor and flow rate. A spray pattern was available for a standard  coverage  pendant  nozzle  with  a  K  factor  of  57  L/min/bar 1/2   [24]  and  this  was considered as a basis.

The FDS model for water droplets takes the following inputs in addition to nozzle flow rate and droplet  diameter:  PARTICLE  VELOCITY,  SPRAY  ANGLE,  PARTICLES\_PER\_SECOND, OFFSET and AGE [8]. An iterative process was developed using a genetic algorithm, where the parameters listed here, as well as droplet diameter, were varied within credible ranges to match a typical nozzle spray pattern per manufacturer data for a selected similar nozzle. The algorithm varied the input parameters with a goal of matching the manufacturer spray pattern based on water delivery at a given distance from the nozzle. Refer to Figure 3-6. The spray pattern was matched by comparing the CFD model water delivery for a given location offset and distance below the nozzle with published data. The models were run with a grid resolution of 0.4 m in the horizontal directions and 0.2 m in the vertical (sensitivity to 0.2 m throughout was checked found to have minimal impact on results). ARCHIVED

Figure 3-5: Example nozzle spray pattern.

<!-- image -->

Engineering drawing

Figure 3-6: Genetic algorithm concept. ARCHIVED

January 2022

<!-- image -->

Flow chart

Two iterations of the genetic algorithm were run, with slight differences in the range of parameters used to check the sensitivity to inputs. Table 3-2 displays the range of values used and optimal values arrived at per the genetic algorithm results. Spray pattern results are provided in Figure 3-7 and Figure 3-8.

Table 3-2: Nozzle parameter development, genetic algorithm input ranges and optimal values, trial A and trial B.

| PARAMETER                          | TRIAL A RANGE   | TRIAL A RESULTS   | TRIAL B RANGE   | TRIAL B RESULTS   |
|------------------------------------|-----------------|-------------------|-----------------|-------------------|
| Particle velocity (m/s)            | 1 to 25         | 18.5              | 1 to 25         | 8.1               |
| Spray angle (inner angle, degrees) | 0 to 30         | 30.0              | 0 to 30         | 19.6              |
| Spray angle (outer angle, degrees) | 31 to 90        | 74.5              | 31 to 90        | 81.5              |
| Particle diameter Dv,0.5 (μm)      | 650 to 1050     | 650.0             | 900 to 1300     | 1080.7            |
| Droplet offset (mm)                | 30              | 30                | 30              | 30                |
| Nozzle flow rate (LPM)             | 82              | 82                | 82              | 82                |
| Particles per second               | 5000            | 5000              | 5000            | 5000              |
| Age (s)                            | 30              | 30                | 30              | 30                |
| Reference                          | EVS-10-18       | EVS-10-18         | EVS-10-20       | EVS-10-20         |

<!-- image -->

Line chart

<!-- image -->

Line chart

Figure 3-7: Results from genetic algorithm trial A (EVS-10-18). ARCHIVED

Figure 3-8: Results from genetic algorithm trial B (EVS-10-20).

Sensitivity analysis included considering the number of particles injected per second (value of 10,000 tested) and the nozzle offset (value of 50 mm tested). Neither setting had any appreciable impact on the results. Different nozzle flow rates were tested. Results of the genetic algorithm at these different flow rates are provided in Table 3-3. Results from trial A1 and A2 (40 LPM and

50 LPM,  respectively)  were  used  to  run  a  case  with  a  nozzle  flow  rate  of  82  LPM.  Spray visualization  of  the  results  is  provided  in  Figure 3-9  and  Figure 3-10,  for  comparison  with Figure 3-7. There is no discernable difference in the results, suggesting that the outcomes in terms of delivered spray density are not sensitive to flow rate. That is, a data fit at one flow rate could be extrapolated to different flow rates. Going forward, nozzle parameters from Table 3-2 were used in the analysis.

Table 3-3: Summary of sensitivity results for varying nozzle flow rates.

| PARAMETER                          | TRAIL A RANGES   | TRIAL A RESULTS   | TRIAL A1 RESULTS   | TRIAL A2 RESULTS   |
|------------------------------------|------------------|-------------------|--------------------|--------------------|
| Particle velocity (m/s)            | 1 to 25          | 18.5              | 13.0               | 15.6               |
| Spray angle (inner angle, degrees) | 0 to 30          | 30.0              | 24.2               | 21.7               |
| Spray angle (outer angle, degrees) | 31 to 90         | 74.5              | 78.2               | 78.7               |
| Particle diameter D v,0.5 (μm)     | 650 to 1050      | 650.0             | 781.5              | 721.5              |
| Droplet offset (mm)                | 30               | 30                | 30                 | 30                 |
| Nozzle flow rate (LPM)             | Varies           | 82                | 40                 | 58                 |
| Particles per second               | 5000             | 5000              | 5000               | 5000               |
| Age (s)                            | 30               | 30                | 30                 | 30                 |
| Reference                          | Varies           | EVS-10-18         | EVS-10-16          | EVS-10-17          |

<!-- image -->

Line chart

ARCHIVED

Figure 3-9: Spray results for 82 LPM flow rate, based on results from a genetic algorithm fit at 40 LPM, trial A1 (EVS-10-19).

<!-- image -->

Line chart

Consideration of the data showed that the peak FHRR was occurring at around 480 seconds, yet the reference literature noted that the FFFS was activated at 400 seconds. Further, consideration of  fire  temperatures  showed  that the  peak temperature  near the  fire occurred  at  around 400 seconds. In the tests, the FHRR was measured by oxygen consumption techniques based on a measuring station 170 m (558 ft.) downstream of the fire [11]. At a nominal longitudinal velocity of 3 m/s, the air from upstream would take on the order of 60 seconds to reach the downstream measuring station. Furthermore, the activation time of the FFFS was noted to be 400 seconds, but it is plausible that some delay may have occurred after the FFFS valve was opened and water was discharged from nozzles at full flow rate. Experience suggests this could have been 20 to 30 seconds.

Figure 3-10: Spray results for 82 LPM flow rate, based on results from a genetic algorithm fit at 58 LPM, trial A2 (EVS-10-19). 3.3 Base Case CFD Models and FHRR Profile Base case analysis was conducted and temperature downstream of the fire was monitored. Initial test cases showed that the temperature prediction was not achieving the peak observed from tests at around 400 seconds, refer to Figure 3-11 and Figure 3-12. The r values indicated good agreement between test data and CFD model, but the offset in peak temperature times was a concern. Consideration was made for a free burn test, to check the model performance, and this showed agreement between the measured and simulated temperature profiles. This result led to focusing on the FFFS as the source of the variation. ARCHIVED

Figure 3-11: Base case result for LTA tests, 5 m downstream of the fire, no change to the input FHRR profile (EVS-09-31).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-12: Base case result for LTA tests, 10 m downstream of the fire, no change to the input FHRR profile (EVS-09-31).

Based on the above considerations a case was tested where the FHRR profile was shifted back in time by 80 seconds (first 80 seconds was neglected), so that the peak FHRR occurred at 400 s (to correspond to the peak from temperature data); refer Figure 3-13. The results were considered at locations 5 m and 10 m downstream of the fire since there was some uncertainty as to exactly where the measurement location applied. Refer to Figure 3-14 and Figure 3-15. The CFD results show  slightly  better  agreement  10  m  downstream.  Overall,  the  agreement  (per  the  r-value) between the test and the CFD can be classed as very good when the HRR profile is shifted.

Heat flux data are provided in Figure 3-16. Agreement with CFD data is classified as good based on  the  r  value,  however,  the  CFD  model  is  showing an  over-prediction of  the peak heat  flux magnitudes. Several attempts were made to determine the cause of the higher heat flux prediction with the CFD model, including consideration of whether the FDS output parameter (incident heat flux in these cases) was the appropriate representation. A definite cause for the difference was not able to be ascertained but it was most likely some sort of discrepancy between the model output parameters and what the instrument used in the test was actually measuring. Given the very good r-value correlation for temperature profiles, and improved prediction of heat flux at times except for when the peak occurred), it was decided that the model was performing well enough and that improvement of the heat flux correlation could be investigated as part of future research.

<!-- image -->

Line chart

Figure 3-13: LTA test HRR shift. ARCHIVED

Figure 3-14: Temperature results 5 meters downstream of the fire with FFFS operating (EVS-09-34).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-15: Temperature results 10 meters downstream of the fire with FFFS operating (EVS-09-34).

<!-- image -->

Line chart

An additional genetic algorithm trial was run where the droplet size was constrained to a smaller range. trial C in Table 3-4 provides the parameters and results. Figure 3-18 provides the results with the trial C droplets; agreement between test and CFD is similar to the trial A result. Additional cooling is observed, via the lower temperatures after 400 seconds, which is expected given the smaller droplet size.

Figure 3-16: Incident heat flux data downstream of the fire (EVS-09-34). 3.4 Droplet Diameter Sensitivity Additional runs were conducted with varying droplet sizes. Per the trials described in Section 3.2 a larger droplet size was tested. Results using the trial B results from Table 3-2 are provided in Figure 3-17. The result shows slightly less cooling downstream of the fire, which is attributable to the larger drop size. A larger water drop has less surface area relative to the volume of water flow.  The  rate  of  cooling by  a  water  spray  depends on  the  rate of  evaporation,  which  in  turn depends on the rate of heat transfer to the water. A larger water drop surface area increases the efficiency (cooling rate per unit volume). With larger water drops there is less total surface area of water, thus meaning that larger water drops provide less cooling. ARCHIVED

Figure 3-17: Temperature downstream of the fire using larger droplet diameter (EVS-09-35).

<!-- image -->

Line chart

Table 3-4: Nozzle parameter development, genetic algorithm input ranges and optimal values, trial A and trial C.

| PARAMETER                          | TRIAL A RANGE   | TRIAL A RESULTS   | TRIAL C RANGE   | TRIAL C RESULTS   |
|------------------------------------|-----------------|-------------------|-----------------|-------------------|
| Particle velocity (m/s)            | 1 to 25         | 18.5              | 1 to 25         | 16.5              |
| Spray angle (inner angle, degrees) | 0 to 30         | 30.0              | 0 to 44         | 30.0              |
| Spray angle (outer angle, degrees) | 31 to 90        | 74.5              | 45 to 90        | 79.9              |
| Particle diameter D v,0.5 (μm)     | 650 to 1050     | 650.0             | 200 to 650      | 550.0             |
| Droplet offset (mm)                | 30              | 30                | 30              | 30                |
| Nozzle flow rate (LPM)             | 82              | 82                | 82              | 82                |
| Particles per second               | 5000            | 5000              | 5000            | 5000              |
| Age (s)                            | 30              | 30                | 30              | 30                |
| Reference                          | EVS-10-18       | EVS-10-18         | EVS-10-24       | EVS-10-24         |

ARCHIVED

<!-- image -->

Line chart

<!-- image -->

Logo

Figure 3-18: Temperature downstream of the fire using smaller droplet diameter (EVS-09-36). 3.5 Grid Resolution Models reported in Section 3.3 were revisited using a grid resolution of 0.4 m (coarser grid, case EVS-09-34 was rerun) to test sensitivity to the grid resolution. Temperature downstream of the fire is shown in Figure 3-19 and Figure 3-20 for distances 5 m and 10 m downstream. The two results from the different grid resolution cases closely match. Figure 3-21 shows the incident heat flux downstream and results between the two grids closely match. The results here support a 0.4 m grid resolution, at least for initial investigations, which is a conclusion similar to that reached in the previous chapter for the Memorial Tunnel CFD models. ARCHIVED

Figure 3-19: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m sensitivity (r value for case EVS-09-44).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-20: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m sensitivity (r value for case EVS-09-44).

<!-- image -->

Line chart

A sensitivity was tested where the radiation was modeled; results are given in Figure 3-24 and Figure 3-25 and changes in the results are minor. This suggests that when the FHRR is prescribed (not determined by the model) that it might not be critical to include radiation when considering interaction between the FFFS and the EVS. An additional sensitivity test using a finer grid of 0.2 m was conducted, refer to Figure 3-26 and Figure 3-27. The agreement in these cases is still very good (per the Pearson coefficient) and slightly more consistent with the previously conducted mixing-controlled models where agreement is better 10 m downstream of the fire.

Figure 3-21: Incident heat flux data downstream of the fire, coarse grid 0.4 m sensitivity (r value for case EVS-09-44). 3.6 Volumetric Heat Source Given the agreement for the Memorial Tunnel tests using a CFD model with a volumetric heat source, the models for the FFFS herein were revisited to also consider the volumetric heat source. Cases were conducted on a coarse grid (0.4 m) and results for temperature downstream are provided in Figure 3-22 and Figure 3-23. Correlation between the model and the test data is very good  per  the  Pearson  coefficient  measure,  and  comparable  to  the  results  observed  with  the mixing-controlled models. ARCHIVED

Figure 3-22: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m, volumetric heat source (r value for case EVS-09-39).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-23: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m, volumetric heat source (r value for case EVS-09-39).

Figure 3-24: Temperature results 5 meters downstream of the fire with FFFS operating, coarse grid 0.4 m and radiation on, volumetric heat source (r value for case EVS-09-41).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-25: Temperature results 10 meters downstream of the fire with FFFS operating, coarse grid 0.4 m and radiation on, volumetric heat source (r value for case EVS-09-41).

Figure 3-26: Temperature results 5 meters downstream of the fire with FFFS operating, finer grid 0.2 m, volumetric heat source (r value for case EVS-09-40).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 3-27: Temperature results 10 meters downstream of the fire with FFFS operating, finer grid 0.2 m, volumetric heat source (r value for case EVS-09-40).

## 3.7 Research Findings and Suggested Practices Based on Findings

The results in this chapter demonstrate that FDS can predict the temperature field downstream of the fire when the FHRR is set as a boundary condition and the FFFS is included. Results show correlation to test data with either the mixing-controlled approach or the volumetric heat source approach. Reasonable results were achieved on a coarse grid (0.4 m) resolution for a volumetric heat source approach.

Sensitivity to the nozzle parameters was tested and some differences were observed dependent on the droplet size. The input HRR profile was also noted to be important. Exact details of the nozzles  were  not  available  (drop  size,  manufacturer, and  spray pattern),  but  using  what  was thought to be a similar nozzle the results were in reasonable agreement if the HRR profile was adjusted per observations noted for timing. The possibility that the nozzle parameters in the test might have been different and the HRR profile not being the source of different temperatures downstream cannot be completely ruled out, however, the evidence presented herein gives a reasonable degree of confidence in the ability of FDS to predict the environment in the tunnel when an FFFS is operated. This conclusion agrees with other studies [25].

The model did not predict heat flux very well with respect to test data. Exact reasons for this are not certain, but it could be a function of the devices used in the test to measure heat flux and differences relative to what was measured in the FDS model. The only way to address these two uncertainties is via future testing where more certainty in conditions is attained. Going forward, the  results  are  considered  acceptable,  given  agreement  here  and  in  previous  studies,  for developing analysis of the interaction of the FFFS and EVS, with the caveat that the methodology would be checked with future stages of research looking at new test data compared with CFD. The suggested practices based on results herein are to consider using a volumetric heat source model on a coarse grid (0.4 m), with no radiation modeled, for initial runs. Results in this section suggest that this approach can give a reasonable prediction of the temperature field. Sensitivity to  a finer grid  (0.2 m)  should  be  considered once initial  runs  have  been  completed. It is  also suggested  that  nozzle  parameters  be  matched  where  possible  by  comparing  spray  patterns between the computational model and available test data. 3.8 Suggested Areas for Further Research ARCHIVED

An area for further potential research could be the radiative heat flux correlation; models herein were predicting a larger magnitude of heat flux downstream of the fire. The differences could be due to the model, but they could also be due to the measurement technique since radiative heat flux is very sensitive to temperature.

## 4 CRITICAL AND CONFINEMENT VELOCITY

Models were developed to examine the ability of the FDS model to predict longitudinal smoke control. Results from the models were compared with equations for longitudinal smoke control as published in NFPA 502 in the 2014, 2017 and 2020 editions. The impact of the FFFS on smoke management is computed as well and results are compared with the equations developed by Ko and Hadjisophocleous [14]. The goal of this chapter is to test the ability of the CFD models to predict the longitudinal velocity needed to control smoke, and to determine the impact of the FFFS on the smoke control.

When this document was being drafted, the NFPA 502 2020 edition equation had been retracted from the standard as part of a tentative interim amendment [26]. Comparison with results from the equation is still made herein since the equation is based on scale testing and Froude scaling, and similar equations have been reported in the literature [4] [5]. The NFPA 502 2020 edition equation is used as it has provision to account for tunnel aspect ratio and backlayering length. For these reasons, even though the equation was retracted, comparison of results to the NFPA 502 2020 edition equation was considered to be beneficial for furthering the current research.

4.1 Overview 4.1.1 Critical Versus Confinement Velocity Critical velocity is the steady state velocity needed, in a longitudinal ventilation system, to direct smoke downstream of a fire and prevent backlayering. In this document the term confinement velocity is used to describe the steady-state velocity of the ventilation airflow moving toward the fire that is of a magnitude large enough to stop smoke movement upstream of the fire but not to prevent backlayering. The  term  confinement  velocity  is  introduced  here  because  many  of  the  models  achieved confinement velocity, but the models reported in this section and Section 5 did not strictly achieve critical velocity. The variability of models with slightly different inputs was typically on the order of 10 to 15 percent (backlayering length and velocity needed to achieve a given backlayer length), and given this point, as well as uncertainty in what the magnitude of critical velocity actually is (that  is,  different  equations  predict  different  values  of  critical  velocity),  it  was  decided  that  no additional insight could be gained principal to the goal of looking at FFFS-EVS interaction by pushing models to achieve zero backlayering if a result had shown achievement of a confinement velocity. ARCHIVED

## 4.1.2 Critical Velocity Equations

The NFPA 502 critical velocity equations from the 2014 edition and 2017 edition are provided in Figure 4-1, and from the 2020 edition in Figure 4-2.

The critical velocity equation from NFPA 502 2014 edition was initially validated as part of the Memorial Tunnel test work [9] [10]. In that work, it was noted that a smoke-controlled situation was deemed to have occurred generally when the backlayering was 40 feet or less. Thus, per the terminology noted for critical and confinement velocity, it is possible that this equation for critical velocity (no backlayering) was validated using a result that was technically confinement velocity (some backlayering but no ongoing upstream smoke spread). Since the equation in NFPA 502 2014 edition represents the critical velocity, any velocity computed using this equation is referred to  as  such.  The  same  is  done  for  the  2017  edition  equation.  Distinction  between  critical  and confinement velocity is made for the 2020 edition equation since that allows input of backlayering length into the computation.

Figure 4-1: Equation. Critical velocity, NFPA 502 2014 [12] and 2017 edition [7].

<!-- image -->

Page thumbnail

In Figure 4-1 symbols are as follows: A is the area perpendicular to the flow (m 2 ), Cp is the specific heat of air (kJ/kg/K), g is the acceleration due to gravity (m/s 2 ), G is the absolute value of tunnel grade as a percent, H is the height of duct or tunnel at the fire site (m) (measured from base of fire of the fire site to tunnel ceiling herein), K1 is 0.606 (for the 2014 equation), which is the Froude number factor raised to the negative one third power, Kg is the grade factor which is 1 for 0 percent or uphill grade, and calculated per the provided equation for downhill grade (equation for Kg is based on Figure D.1 in NFPA 502 2014), ρ is the average density of the approach (upstream) air (kg/m 3 ), Q is the heat the fire adds directly to air at the fire site (kW), T is the temperature of the approach air (K), Tf is  the average temperature of the fire site gases (K), and Vc is the critical velocity (m/s). For the 2017 equation, K1 varies with FHRR and if Q is greater than 100 MW, K1 is 0.606, for Q of 90 MW, K1 is 0.620; for 70 MW is 0.640; for 50 MW is 0.680; for 30 MW is 0.740; and for Q less than 10 MW, K1 is 0.870.

<!-- formula-not-decoded -->

January 2022

Figure 4-2: Equation. Critical velocity, NFPA 502 2020 edition [13].

In Figure 4-2 symbols are as follows: Cp is the specific heat of air (kJ/kg/K), g is the acceleration due to gravity (m/s 2 ), H is the height of duct or tunnel measured from base of fire at the fire site (m), W is  the  tunnel  width  (m), Lb is  the  backlayering  length  (m), ρa is  the  average  density  of the approach (upstream) air (kg/m 3 ), Q is the total fire heat release rate at the fire site (kW), Ta is the temperature of the approach air (K), and u is the critical velocity (m/s), if Lb is 0 and if Lb is not 0 then u is the confinement velocity. The tunnel grade is accounted for by multiplying by the grade factor, which is the same as used in Figure 4-1.

Critical velocity and confinement velocity were computed for comparison with CFD with a FHRR of 46.7 MW, based on an ambient temperature of 20 ⁰C, 0 percent gradient, tunnel width of 7.2 m, tunnel height of 5.2 m, heat capacity of 1005 J/kg/K, and a radiative heat fraction of 30 percent. This gave  values of  critical  velocity  of  2.40  m/s  (2014),  2.97 m/s  (2017)  and  3.07 m/s  (2020) (calculation reference EVS-01-18). For a backlayering length of 6 m, the confinement velocity was 2.88 m/s (2020 edition). 4.1.3 CFD Models Analysis  was  conducted  for  a  tunnel  with  a  cross  section  7.2 m  wide  and  5.2 m  high, corresponding to the LTA tunnel analyzed in Section 3. CFD analysis was conducted using similar methods as presented in Section 2 but with some minor changes as summarized in Table 4-1. Models were conducted using a mixing-controlled approach for fire, a volumetric heat source, with and  without  radiation  heat  transfer,  various  turbulence  models,  and  grid  resolution.  For comparison, the velocity needed for longitudinal smoke control was computed using the NFPA 502 equations from the 2014, 2017 editions and 2020 editions. The FHRR was 46.7 MW unless noted otherwise. ARCHIVED

Table 4-1: CFD parameters for critical velocity validation.

| ITEM                     | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                   | SOURCE                                                                                                           |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| Cross section and length | Tunnel cross section 7.2 m wide by 5.2 m high, 0 percent grade, model was 150 m long.                                                                                                                                                                                                                                                                                                                                                                   | Corresponds to the LTA tunnel cross section                                                                      |
| Fire parameters          | FHRR = 46.7 MW, fire geometry is positioned on the tunnel floor and is 6 m long and 4 m wide, and where a volumetric heat source is used it is 2.8 m high and the radiative fraction is set to 30 percent (in these cases radiation was not modeled unless stated).                                                                                                                                                                                     | Based on Memorial Tunnel tests (pan sizes) and previous CFD analysis where a volumetric heat source is used [10] |
| Wall boundary conditions | Concrete boundary condition with a smooth (0 roughness height) wall having a thickness of 1.0 m (typical tunnel wall thickness) and an insulted backing. Materials properties as follows: Density = 2,000 kg/m3 Heat capacity = 0.88 kJ/kg/K Conductivity = 1.3 W/m/K Emissivity = 0.9                                                                                                                                                                  | [21]                                                                                                             |
| CFD model parameters     | CFD models had a nominal grid resolution of 0.4 m and FDS defaults were used as per those applied in models discussed in Section 2. The inlet velocity was set as a constant value. Models had small openings (open boundary condition) 0.4 m by 0.4 m placed along the tunnel to help with numerical stability [8]. The openings were spaced at 12 m and were on alternating sides of the tunnel. Variations from these parameters are noted. ARCHIVED | -                                                                                                                |
| Critical velocity        | Critical velocity was computed by temperature to identify the extent of any backlayering. Sensors were placed at the tunnel ceiling on the centerline and a temperature of 25 ⁰C was used to demarcate the backlayering region. This temperature was 5 ⁰C above ambient and, given the large temperatures likely in a fire, assumed to be enough to detect the onset of backlayering.                                                                   | -                                                                                                                |
| Other                    | Sensitivity to grid resolution, turbulence models, wall models, radiation heat transfer, and boundary conditions (inlet velocity and heat transfer conditions) are tested.                                                                                                                                                                                                                                                                              | -                                                                                                                |

## 4.2 Mixing Controlled Combustion Models

Key results for mixing-controlled combustion models are summarized in Table 4-2. As noted in Section 4.1.2 the critical velocity calculated using equations per NFPA 502 was 2.40 m/s (2014 edition), 2.97 m/s (2017 edition) and 3.07 m/s (2020 edition). For a backlayering length of 6 m, the confinement velocity was 2.88 m/s (2020 edition).

Results show that FDS does a reasonable job of predicting velocity for smoke control with the base case showing results that over-predict relative to the equation in the NFPA 502 2014 edition, and under-predict relative to the equations provided in the 2017 and 2020 editions.

Note  that  the  velocity  calculated  with  the  CFD  model  does  not  result  in  the  absence  of backlayering (0 m). Results from models conducted show that the backlayering length tends to be an unsteady quantity and it typically fluctuates back and forth in the model. No attempt was made to produce 0 m of backlayering (critical velocity). The aim was to demonstrate, using CFD, a controlled smoke condition (confinement velocity), and the order of magnitude upstream velocity used. Based on accuracy of the CFD models, a velocity increment range of 0.25 m/s (about 10 percent) was used, and for backlayering length, increments on the order of 10 m were used. Based on results seen in earlier sections, attempting to control smoke to any more precise degree would be  working  in  a  range  where  modeling  errors  could  easily  affect  the  results  and  thus confidence in trends would be lower.

- Sensitivity to near-wall grid resolution (EVS-19-3 versus EVS-19-20): The case with a finer grid near the wall predicted more backlayering relative to the base case (14 to 16 m versus 28 m). The result with a finer near-wall grid took such a very long time to run (several weeks). In both cases the smoke movement upstream was controlled, so the engineering outcomes would be unchanged due to this sensitivity. Finer grid cases were observed to give more backlayering, refer also to Section 2.3.9.
- Key results include: · Sensitivity to upstream velocity (EVS-19-1 versus EVS-19-10): A change of upstream velocity (decrease) of 0.25 m/s resulted in an increase in backlayer length on the order of 10 m. · Sensitivity to  openings along the tunnel length (EVS-19-24 versus EVS-19-10, EVS-19-11 versus EVS-19-18): Closing the openings caused the backlayering length to decrease. · Sensitivity  to  wall  turbulence  model  (EVS-19-24  versus  EVS-19-19):  No  change  in backlayering length. · Sensitivity to grid resolution (EVS-19-10 versus EVS-19-3): Sensitivity to grid resolution was tested by running cases with an upstream velocity less than critical. This was done because cases with some backlayering are more likely to be sensitive to grid changes. The results show  that  grid  resolution  had  a  minor  impact  with  the  finer  grid  predicting  slightly  more backlayering. ARCHIVED

Static pressure profiles were measured along the tunnel using points placed on the centerline at a height of 2.4 m above the roadway (roughly halfway between roadway and tunnel ceiling), refer to  Figure 4-3  for  a profile  plot.  One of  the profiles  is  provided for a  case  with small  openings distributed along the tunnel, and the other for the same scenario with the openings closed off. The  pressure  profile  appears  to  be  affected  by  the  backlayering.  Further  discussion  on  the magnitude of the pressure change is provided in later subsections.

Table 4-2: Longitudinal smoke control results - mixing-controlled combustion models (FDS default).

| ID        |   V (M/S) | BL (M)   | REMARKS                                                                                                                                                                                                                                                                              |
|-----------|-----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EVS-19-1  |      2.73 | 6        | Base case model (model halt 380 s). Variation from NFPA 502: critical velocity 2014 (+13 percent), 2017 (-8 percent), 2020 (-12 percent) and confinement velocity 2020 (-6 percent). Upstream velocity based on a temperature sensor placed 2 m upstream of the fire reaching 25 ⁰C. |
| EVS-19-10 |      2.50 | 20       | Reduced upstream velocity (model halt 1200 s).                                                                                                                                                                                                                                       |
| EVS-19-24 |      2.50 | 8        | Closed the small openings that are distributed along the tunnel sidewalls (model halt 1200 s).                                                                                                                                                                                       |
| EVS-19-3  |      2.50 | 14 to 16 | Refined the grid, 0.2 m resolution, and closed the small openings that are distributed along the tunnel sidewalls (model halt 1200 s).                                                                                                                                               |
| EVS-19-19 |      2.50 | 9        | Wall adapting large eddy simulation (WALE) turbulence model near the walls (model halt 1200 s). Closed the small openings that are distributed along the tunnel sidewalls.                                                                                                           |
| EVS-19-20 |      2.50 | 28 to 30 | Closed the small openings that are distributed along the tunnel sidewalls, refined grid, 0.1 m near the walls, 0.2 m otherwise (model halt 900 s - model took several weeks of computer time to reach this point).                                                                   |
| EVS-19-11 |      2.25 | 42       | Reduced upstream velocity (model halt 1200 s).                                                                                                                                                                                                                                       |
| EVS-19-18 |      2.25 | 32       | Closed the small openings that are distributed along the tunnel sidewalls (model halt 1200 s).                                                                                                                                                                                       |

<!-- image -->

Line chart

ARCHIVED

Figure 4-3: Static pressure profile along the tunnel for mixing-controlled models.

## 4.3 Volumetric Heat Source Models

Results are summarized in Table 4-3 for models using a volumetric heat source. The volumetric heat source results show a trend toward slightly lower confinement velocity relative to the models from the previous section, however, results are still within about 10 percent of each other. Some observations are as follows:

- Base case model (EVS-19-21) gave slightly less backlayering relative to a similar mixingcontrolled model from the previous section (see EVS-19-10 in Table 4-2). Refined grid case (EVS-19-22 at 0.2 m) give similar results.
- Including  a  passive  scalar  to  represent  soot  had  no  impact  on  results  (EVS-19-23)  and including radiation in the model had no impact on results (EVS-19-32).
- A  reduced  upstream  velocity  (2.25  m/s,  EVS-19-13)  gave  only  a  small  increase  in backlayering relative to the initial velocity used (2.50 m/s). Relative to the mixing-controlled models the backlayering was less (see case see EVS-19-11 in Table 4-2). · Turbulence  model  closure  coefficient  (EVS-19-13  versus  EVS-19-15):  Minor  change  in results, slightly better control of smoke when the closure coefficient is increased though this is well within the margin of accuracy. · Closing  off  the  small  openings  along  the  tunnel  (EVS-19-13  versus  EVS-19-17):  Slightly reduced backlayering length, however, the difference is within model accuracy levels. · Reynolds-averaged Navier-Stokes (RANS) k-epsilon turbulence model approach in FLUENT versus using large eddy simulation (EVS-19-12 versus EVS-19-17): Differences in the results are minor in terms of backlayering length (within range of model accuracy). The RANS model predicts slightly less backlayering, but to fully conclude this a dedicated parameter study to compare models would be needed. · Refined grid (EVS-19-17 versus EVS-19-16): Backlayering increases with the grid refined, which is consistent with what was seen in mixing-controlled models. The reason for this could be related to the increased peak temperatures near the walls because of the finer grid. The difference is not enough to impact conclusions. ARCHIVED
- Adiabatic boundary conditions on the walls mean no heat can transfer into the walls, and all heat  therefore  is  controlled  with  ventilation.  The  result  of  this  is  a  substantial  increase  in backlayering distance (EVS-19-36). This issue is not significant in most fire scenarios, since a perfectly adiabatic wall does not exist, and even a protective fire board can absorb some heat. However, this result does show that critical velocity depends on energy balance between the air stream and the tunnel walls and other heat absorbing elements (such as an FFFS).

In summary, the results show that closing small openings along the tunnel length improved smoke management slightly. A refined grid case (EVS-19-16) suggested the finer grid would predict an increased  critical  velocity.  When  the  openings  were  closed  off  and  the  upstream  velocity increased to 2.5 m/s, there was minimal difference in the smoke control behavior between 0.2 m grid or 0.4 m grid in this case.

The backlayering length can fluctuate, and small changes in backlayering length can be observed, especially when backlayering is less than 10 m. In general, once backlayering is at around 10 m with a coarse grid (0.4 m), these results show that the range for critical velocity is usually within about 10 percent of the velocity used. For example, case EVS-19-17 gave a backlayering length 6 m to 8 m at 2.25 m/s (0.4 m grid); sensitivity with a refined grid showed more backlayering, but an  increase  of  the  velocity  by  0.25  m/s  showed  a  convergence  of  the  backlayering  control outcome, for all sensitivities.

A suggested method follows:

- Avoid using small openings along the tunnel unless necessary for numerical stability. It is noted that some tests on a transverse ventilated tunnel were unstable for a mixing-controlled combustion model unless openings were included but were stable with a volumetric heat source model.

· A  grid  resolution  of  0.4  m  can  give  reasonable  results.  The  magnitude  of  smoke  control velocity  might  be  10  percent  more  than  arrived  at  with  this  result,  but  if  backlayering  is contained to 10 m to 20 m, no material differences in smoke management outcomes are likely. · The coarse grid can be used for initial runs with sensitivity on a finer grid (0.2 m) once a smoke control velocity is determined on a coarse grid. The final smoke control velocity is not expected to be more than 10 percent of the value initially arrived at on the coarse grid. Static  pressure profiles  for  cases  with  openings  included  are  shown  in  Figure 4-4  for  mixingcontrolled combustion versus a volumetric heat source. There is an appreciable difference in the pressure  profile  in  the  region  just  upstream  of  the  fire,  which  is  attributable  to  the  different backlayering degree between the two models. A result looking at the impact of the openings using a volumetric heat source is provided in Figure 4-5. The result shows no major difference in results when the difference in backlayering is considered. Results  for  the  coarse  and  refined  grid  at  an  increased  upstream  velocity  can  be  seen  in Figure 4-6. There is virtually no difference in the results, with the net pressure drop magnitude (difference between upstream entry and downstream exit) being around 9.5 Pa. ARCHIVED

Table 4-3: Longitudinal smoke control results - volumetric heat source results.

| ID        |   V (m/s) | BL (m)   | REMARKS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|-----------|-----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EVS-19-21 |      2.50 | 2 to 4   | Closed the small openings that are distributed along the tunnel sidewalls (model halt 1200 s). Variation from NFPA 502: critical velocity 2014 (+4 percent), 2017 (-17 percent), 2020 (-20 percent) and confinement velocity 2020 (-16 percent).                                                                                                                                                                                                                                                                   |
| EVS-19-22 |      2.50 | 0 to 5   | Closed off small openings spread along the tunnel, refined grid to 0.2 m (model halt 1200 s).                                                                                                                                                                                                                                                                                                                                                                                                                      |
| EVS-19-23 |      2.50 | 2 to 4   | Added a passive scalar to represent soot, otherwise as per EVS-19-21 (model halt 1200 s). No change in results.                                                                                                                                                                                                                                                                                                                                                                                                    |
| EVS-19-32 |      2.50 | 3        | Added a passive scalar to represent soot, otherwise as per EVS-19-21 (model halt 1200 s) and included radiation. No change in results.                                                                                                                                                                                                                                                                                                                                                                             |
| EVS-19-13 |      2.25 | 8 to 12  | Nominal grid resolution 0.4 m (model halt 1200 s).                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| EVS-19-15 |      2.25 | 10 to 12 | Turbulence model closure coefficient from 0.1 to 0.2, unsteady backlayering (pulsing) (model halt 1200 s).                                                                                                                                                                                                                                                                                                                                                                                                         |
| EVS-19-17 |      2.25 | 6 to 8   | Closed the small openings that are distributed along the tunnel sidewalls, unsteady backlayering (model halt 1200 s).                                                                                                                                                                                                                                                                                                                                                                                              |
| EVS-19-12 |      2.25 | 4        | Ran with a steady state Reynolds Averaged Navier- Stokes turbulence model (RNG k-epsilon) (ANSYS Fluent used since FDS cannot model turbulence this way) with a grid resolution nominally 0.3 m. Volumetric heat source 6 m long, 4 m wide and 3 m high, and 30 percent of the heat was radiation (removed from the computation, not directly modeled). Variation from NFPA 502: critical velocity 2014 (-6 percent), 2017 (-28 percent), 2020 (-31 percent) and confinement velocity 2020 (-27 percent). ARCHIVED |
| EVS-19-9  |      2.15 | 18       | Similar model to EVS-19-12, but with a reduced upstream velocity.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| EVS-19-16 |      2.25 | 16 to 18 | Closed the small openings that are distributed along the tunnel sidewalls, refined grid to 0.2 m. Backlayering observed to increase toward the end of the simulation (model result reported at 1200 s, backlayering slowly increases up to 1500 s to around 26 m).                                                                                                                                                                                                                                                 |
| EVS-19-36 |      2.25 | 66       | Closed the small openings that are distributed along the tunnel sidewalls, refined grid to 0.2 m (model halt 1200 s). Walls are adiabatic.                                                                                                                                                                                                                                                                                                                                                                         |
| EVS-19-37 |      2.00 | 20 to 28 | Closed the small openings that are distributed along the tunnel sidewalls, unsteady backlayering (model halt 1200 s).                                                                                                                                                                                                                                                                                                                                                                                              |

Figure 4-4: Static pressure profile for mixing-controlled and volumetric heat source combustion with small openings distributed along the tunnel.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 4-5: Static pressure profile for a volumetric heat source comparing cases with and without small openings distributed along the tunnel.

<!-- image -->

Line chart

<!-- image -->

Photograph

Figure 4-6: Static pressure profile for a volumetric heat source with refined grid. Equations are presented in the literature for the purposes of computation of a pressure loss due to fire. The first equation considered is taken from the governing equations of the SVS (Subway Ventilation Simulation, previously known as SES for Subway Environment Simulation) software [27]. SVS is a one-dimensional flow solver, aimed for use in rail tunnels, but is applicable to road tunnels as well. Its calculation of the fire pressure loss is based on Figure 4-7. Note that the pressure change given by Figure 4-7 represents only one loss term and in a tunnel ventilation design, several other terms (wall friction, vehicle friction, buoyancy, wind) are important for the overall pressure losses and need to be factored into a ventilation design calculation (see [1], Section 5.3). ARCHIVED

Figure 4-7: Equation. SVS pressure drop equation due to fire.

In Figure 4-7 ∆Pfire is the pressure loss due to the fire (Pa), ρ0 is the density of air (kg/m 3 ), vin is the magnitude of the upstream velocity (m/s), Tfire is  the  temperature at  the fire  (K), T0 is  the ambient temperature (K), Qconv is the convective portion of the fire heat release rate (W), Cp is the specific heat of air (J/kg/K), and ṁ is the mass flow rate of air (kg/s).

Additionally, a recent paper by Carlotti and Salizzoni [28] uses dimensional analysis of multiple empirical formulae and compares the results with small-scale experimental data to derive a new equation for the pressure drop, shown below in Figure 4-8.

Figure 4-8: Equation. Pressure drop equation recommended for EVS design [28].

In Figure 4-8 ∆Pfire is the pressure loss due to the fire (Pa), Qconv is the convective portion of the fire heat release rate (W), v is the magnitude of the upstream velocity (m/s), Cp is the specific heat of air (J/kg/K), T0 is the ambient temperature (K), and Dh is the hydraulic diameter of the tunnel (m).

Using Figure 4-7 for the parameters of this tunnel geometry, a value of 6.3 Pa is arrived at (velocity of 2.25 m/s). Using Figure 4-8 to compute the pressure loss for this geometry, a value of 10.3 Pa is arrived at (calculation reference EVS-01-16). Both values are comparable to the CFD result of 9.5 Pa (±1Pa). From experience, the equation in Figure 4-7 tends to predict a lower pressure loss due to fire.

Pressure loss due to fire is noted to be an area of active research with FDS, and some authors have reported difficulty in being able to generate a reliable computation of the pressure field near to a fire in a long computational domain [29]. A detailed investigation of this aspect has not been developed in this report.

## 4.4 Scaled Tunnel Critical Velocity

For testing purposes, it is desirable to use a scaled tunnel model since tests can be run faster and for less cost compared with a full-scale tunnel. A scaled tunnel can be derived using the Froude scaling equations in Figure 4-9.

ARCHIVED

Figure 4-9: Equation. Scaling relationships [30] [31].

In Figure 4-9 symbols are as follows: Fr is the Froude number, g is the acceleration due to gravity (m/s 2 ), l is length (m), Q is the heat release rate (kW), V is the ventilation velocity (m/s), and V ̇ is the  volumetric  flow  rate  in  (m 3 /s).  The  subscript F is  for  the  full-scale  facility  parameter;  the subscript M is for the model parameter.

A scaled CFD model was conducted to examine whether the principal characteristics (critical velocity,  backlayering  length)  would  follow  the  scaling  equations.  Results  are  provided  in Table 4-4. The geometry is scaled by a factor of 4, and per the equations, the velocity should scale down by a factor of 2. The results show that the backlayering length in the scaled model decreases by a factor of 4, which is consistent with the scaling. Note that scaling the geometry is a very complex issue and not every physical characteristic (such as radiation heat transfer) can be scaled easily. The results here show a trend toward similar behavior for smoke control, but much more in-depth work would be needed, beyond the scope of this research, to fully quantify the efficacy of this scaling technique.

Figure 4-10 shows the pressure profile results (pressure scales according to the length scale [30]) with and without a scalar representing soot being introduced. There are differences in the absolute value of the pressure but the magnitude of relative change along the length is minimal. Figure 4-11 shows results for the small-scale (scaled up by a factor of four to achieve full-scale equivalency) and full-scale models. The profiles are quite similar when considering there is a factor of four difference in the geometry.

Table 4-4: Critical velocity results - volumetric heat source results for scaled geometry.

| ID        |   V (m/s) | BL (m)   | REMARKS                                                                                                                                                                                                                                          |
|-----------|-----------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EVS-19-21 |      2.50 | 2 to 4   | Closed the small openings that are distributed along the tunnel sidewalls (model halt 1200 s). Variation from NFPA 502: critical velocity 2014 (+4 percent), 2017 (-17 percent), 2020 (-20 percent) and confinement velocity 2020 (-16 percent). |
| EVS-19-32 |      2.50 | 3        | Added a passive scalar to represent soot, otherwise as per EVS-19-21 (model halt 1200 s) and included radiation. No change in results.                                                                                                           |
| EVS-19-33 |      1.25 | 1        | Scaled version of EVS-19-32 (1:4 for length, 1:2 for velocity).                                                                                                                                                                                  |

<!-- image -->

Icon

ARCHIVED

Figure 4-10: Static pressure profile results for models with and without a passive scalar.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 4-11: Static pressure profile results for full-scale and one quarter scaled models, with results plotted as full-scale equivalent.

## 4.5 Critical Velocity with FFFS

The final part of the analysis in this chapter involves checking the ability of the CFD model to predict backlayering management when an FFFS is operated. The equations developed by Ko and Hadjisophocleous [14] are used for comparison with CFD; refer to Figure 4-12. Note that the nozzles used in the experiments [14] generated large droplets, with a K factor of 161.3 L/min/bar 1/2 and water application rates ranged from 3 to 9 mm/min. The CFD model herein is based on the full-scale  configuration  described  in  Section  4.1.3  but  now  an  FFFS  is  also  modeled.  Model parameters are provided in Table 4-5.

Table 4-5: Model parameters for critical velocity and FFFS operating.

| ITEM                       | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | SOURCE                |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|
| Fire and velocity scenario | FHRR of 18.7 MW, upstream velocity is varied, ambient temperature 20°C                                                                                                                                                                                                                                                                                                                                                                                                 | -                     |
| FFFS arrangement           | Water application rate is 0.12 gpm/ft 2 (5 mm/min), droplet parameters are as per trial A in Table 3-4. The geometry of the nozzles comprises two rows of nozzles running along the tunnel length from 33 m upstream of the fire to 27 m downstream of the fire with 4 m between nozzles. Each row of nozzles is placed 2.4 m from the tunnel side walls. Total zone length is 64 m, width of 7.2 m, with 32 nozzles at a flow rate of 72.0 L/min/nozzle (5.0 mm/min). | Typical design values |
| CFD model parameters       | Refer to Table 4-1. A volumetric heat source model is used. The FFFS had no impact on the FHRR in the models; it only acted to cool the tunnel environment and products of combustion.                                                                                                                                                                                                                                                                                 | -                     |
| Critical velocity          | Typically, computed by using upstream temperature near the ceiling is used to indicate whether backlayering occurs                                                                                                                                                                                                                                                                                                                                                     | [5]                   |

<!-- image -->

Engineering drawing

ARCHIVED

Figure 4-12: Equation. Critical velocity with an FFFS operating [14].

In Figure 4-12 Cp is the specific heat of air (kJ/kg/K), g is the acceleration due to gravity (m/s 2 ), D is the hydraulic diameter of the tunnel (m), ρo is the average density of the approach (upstream) air (kg/m 3 ), Q is the total fire heat release rate (kW), Q' is the dimensionless heat release based on the tunnel hydraulic diameter, V'' is the dimensionless critical velocity without FFFS, To is the ambient temperature (K), V is the critical velocity without FFFS (m/s), VFFFS is the critical velocity accounting for FFFS (m/s), and ω is the water spray density (mm/min). The equation is valid up to a FHRR of approximately 40 MW.

Model results are provided in Table 4-6. The method of controlling or setting the upstream velocity varies between models and it is noted in the table which method is used. Key conclusions as follows:

- The model makes a reasonable prediction of velocity for longitudinal smoke control at the FHRR used with no FFFS operational (EVS-19-25).
- The effect of the FFFS can be seen in models run with a very low upstream velocity (EVS-1926  and  EVS-19-34).  In  these  models  there  is  substantial  backlayering  until  the  FFFS  is operated and after that the smoke control improves. Radiation heat transfer, when included, slightly reduces the efficacy of the water spray cooling. Critical velocity primarily depends on convective heat management and if radiation is included then some of the water spray cooling capacity goes into radiation absorption meaning less convective fire energy can be absorbed by the water. Radiation heat transfer has less effect when the temperature sensor is located less than one tunnel height upstream of the fire (EVS-19-35 versus EVS-19-30). · Location of the temperature sensor used to trigger critical velocity determination: Models show a  clear  decrease  in  the  upstream  velocity  when  the  FFFS  is  used  (temperature  sensor approximately  two  tunnel  height  distances  upstream,  EVS-19-27  versus  EVS-19-28,  and temperature sensor located approximately one tunnel height distance upstream EVS-19-29 versus EVS-19-30). Note that when the FFFS is not used and the temperature sensor is placed  further  upstream  of  the  fire  (two  tunnel  heights),  the  smoke  control  with  no  FFFS operating  is  significantly  worse,  as  evidenced  by  the  much  great  backlayering  distance (compare EVS-19-28 and EVS-19-29). ARCHIVED
- Per  [14]  the  critical  velocity  with  5 mm/min  water  application  should  be  3.02 m/s  for  the 18.7 MW FHRR with no FFFS, and 2.66 m/s with the FFFS operating at 5 mm/min (NFPA 502 2014 edition equation gives 1.95 m/s, 2017 edition gives 2.79 m/s and 2020 edition gives 3.07 m/s). If the equation per [14] is used just to predict longitudinal velocity change from a CFD case with no FFFS operating the following result is found: 1) Based on case with no FFFS  operating  a  velocity  of  2.23  m/s  is  found  to  achieve  the  smoke  control  objective (EVS-19-29, 2 to 4 m of backlayering); 2) Starting then with a velocity of 2.23 m/s, and using the equation in Figure 4-12 with a 5 mm/min water application rate and a convective heat fraction  of  70%  of  18.7  MW,  the  velocity  for  smoke  control  with  FFFS  is  predicted  to  be 1.80 m/s; 3) The CFD model (like EVS-19-29 but with FFFS at 5 mm/min, case EVS-19-30) has a smoke control velocity of 1.77 m/s (with 2 m to 4 m of backlayering). The result suggests that the equation in Figure 4-12 can be used to make an estimate the change in velocity that might arise when an FFFS is applied. The result is interesting for further work, but it is noted that this was not the intended use of the equation and further investigation is needed since the agreement between equation and CFD may have been affected by the coarse grid

Table 4-6: Critical velocity results - volumetric heat source results with FFFS.

| ID        |   V (m/s) | BL (m)     | FFFS   | REMARKS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|-----------|-----------|------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EVS-19-25 |      2.30 | 2 to 6     | N      | Upstream velocity set to 2.30 m/s. Variation from NFPA 502: critical velocity 2014 (+16 percent), 2017 (-19 percent), 2020 (-29 percent), per [14] (-27 percent) and confinement velocity 2020 (-23 percent).                                                                                                                                                                                                                                                                                          |
| EVS-19-26 |      1.00 | 33         | Y      | Upstream velocity 1.0 m/s. Prior to FFFS operation the backlayering length is greater, back to the inlet of the computation domain (70 m), and the extent would likely be more if the domain were longer. When the FFFS is operated the backlayering length decreases.                                                                                                                                                                                                                                 |
| EVS-19-34 |      1.00 | 40m (+/-5) | Y      | Upstream velocity 1.0 m/s. Included radiation heat transfer and 30 percent radiative fraction. This model is the same as EVS-19-26 except for inclusion of radiation heat transfer. The results show backlayering is not reduced as much when radiation is included, meaning that the balance between radiative energy and convective energy absorbed by the FFFS is important. If radiation is not modeled, then the model might predict a slightly greater benefit of the FFFS than likely. ARCHIVED |
| EVS-19-27 |      1.43 | 13         | Y      | Velocity is decreased until a temperature sensor at the tunnel ceiling 12 m upstream of the fire registers 25 ⁰C.                                                                                                                                                                                                                                                                                                                                                                                      |
| EVS-19-28 |      1.80 | >50        | N      | Velocity is decreased until a temperature sensor at the tunnel ceiling 12 m upstream of the fire registers 25 ⁰C.                                                                                                                                                                                                                                                                                                                                                                                      |
| EVS-19-29 |      2.23 | 2 to 4     | N      | Velocity is decreased until a temperature sensor at the tunnel ceiling 4 m upstream of the fire registers 25 ⁰C.                                                                                                                                                                                                                                                                                                                                                                                       |
| EVS-19-30 |      1.77 | 2 to 4     | Y      | Velocity is decreased until a temperature sensor at the tunnel ceiling 4 m upstream of the fire registers 25 ⁰C.                                                                                                                                                                                                                                                                                                                                                                                       |
| EVS-19-35 |      1.84 | 4          | Y      | Same model as EVS-19-30 but included the radiation heat transfer component. Per [14] the critical velocity is predicted to be 2.16 m/s.                                                                                                                                                                                                                                                                                                                                                                |
| EVS-19-38 |      2.30 | 0          | Y      | Same model as EVS-19-25 but includes FFFS. Per [14] the critical velocity is predicted to be 2.66 m/s.                                                                                                                                                                                                                                                                                                                                                                                                 |

Pressure profiles are provided in Figure 4-13 for cases with the FFFS operating and without. In this case it is noted there is very little difference in the overall relative pressure change (note the case EVS-19-25 was shifted down by 1.5 Pa to have the same entry pressure), thus suggesting that the water droplets have a small impact (relative to other losses such as pressure loss due to the fire) in terms of introducing additional pressure losses that the ventilation system would need to overcome. The pressure loss due to the FFFS, comparing cases EVS-19-25 and EVS-19-38 is on the order of 1 Pa; which is small relative to the much greater pressure loss due to fire, and potentially negligible depending on the design being progressed. Another study has reported that the  injection  of  water  spray  causes  additional  pressure  losses  along  the  tunnel,  due  to acceleration of the droplets, and that this pressure drop is large enough (on the order 5 to 10 Pa) to warrant inclusion in the ventilation design [32]. As noted earlier in this section, FDS is noted to not always reliably predict pressure profiles in long tunnels [29]; further research on this subject is suggested, including computational research and testing.

<!-- image -->

Line chart

## 4.6 Research Findings and Suggested Practices Based on Findings

The results herein have demonstrated the ability of FDS to make a reasonable prediction of the velocity needed for longitudinal smoke control. This conclusion is based on observations of the results relative to the published critical velocity equations in NFPA 502. Figure 4-14 provides a graph showing some selected results for longitudinal velocity for smoke control compared to the equations.  The  FHRR  and  velocity  have  been  made  non-dimensional  per  methods  given  in Figure 4-2. Note that the NFPA 502 2020 edition equation was undergoing revision [26], [33]. No single equation gives a perfect prediction of the velocity needed to control smoke, but the results here do show the ability of the CFD model to make a reasonable prediction of the velocity needed for smoke control.

Note that in conducting this analysis a result with 0 m backlayering was not sought out. The goal was instead to control the smoke to a distance one or two tunnel heights upstream of the fire. Given the accuracy with which FHRR can be measured in a test, and the accuracy with which upstream velocity can be controlled, both in a test and in a model (for instance, grid resolution sensitivity as demonstrated in Section 2.3.9), it was decided this was an approach that would yield more meaningful trends in results with respect to engineering levels of accuracy. Technically, the velocity arrived at in many simulations was the confinement velocity. Comparison is made with the NFPA 502 2020 edition equation with 0 m backlayer (critical velocity) and 15 m backlayer (confinement  velocity).  The  2020  edition  equation  results  are  noted  to  be  closer  to  the  other editions of NFPA 502 when backlayering is included.

Figure 4-14: Summary plot of CFD results versus NFPA 502 equations, no FFFS.

<!-- image -->

Line chart

Results with the FFFS operating are compared to equation of Ko and Hadjisophocleous [14] in Figure 4-15. Dimensionless terms are as shown in Figure 4-12. Note that the FHRR used in the computation of dimensionless FHRR for the CFD models is important. If the convective term is used to compute dimensionless FHRR the agreement with equations is improved relative to a computation if the total FHRR is used. Note that the CFD models only included convective FHRR. This difference between the results and predictions is noted to also be exacerbated by the large variation  in  dimensionless  critical  velocity  with  dimensionless  FHRR;  a  small  change  in dimensionless  FHRR  shows  quite  a  large  change  in  the  dimensionless  critical  velocity  in Figure 4-15. However, further research is suggested to attempt to achieve a better correlation between CFD results and the equation of Ko and Hadjisophocleous [14] given in Figure 4-12. The CFD  results  have  a  lower  velocity  for  smoke  control,  but  this  might  have  been  due  to  grid resolution too.

Results in Table 4-6 suggested radiation heat transfer has a minor impact on results, with cases including radiation showing slightly more backlayer when considering the impacts of the FFFS. The reason for this is that when radiation is included some of the energy absorbing capability of the water goes into radiation absorption. If radiation is included then some of the water spray cooling ability goes into radiation absorption, meaning less convective fire energy is absorbed by the water. Comparison of results with equations of Ko and Hadjisophocleous [14] also suggest consideration  of  whether  the  FHRR  is  radiative  or  convective  is  important.  More  research  is suggested to better quantify the impact of radiative heat transfer.

Figure 4-15: Summary plot of CFD results versus equations by Ko and Hadjisophocleous [14], FFFS operating.

<!-- image -->

Line chart

In  terms  of  suggested  practices,  the  volumetric  heat  source  approach  with  no  radiation  heat transfer active, and on a coarse grid (0.4 m) has been found to give reasonable results, at least to understand trends in the interaction between FFFS and EVS. The mixing-controlled model also gives reasonable predictions of longitudinal velocity for smoke control.

The volumetric heat source approach was found to be more stable numerically. While this method has potential shortcomings as it may not predict flame temperatures accurately, it has been found to give reasonable predictions of the temperature and velocity field remote from the immediate fire. In the mixing-controlled approach one practice used sometimes with FDS is to include small openings  along  the  tunnel  length  to  help  with  stability;  this  approach  gave  slightly  more backlayering.  Given  this  point,  and  apart  from  the  questionable  physics  of  including  small openings, it is desirable to not use small openings unless necessary. Going forward, a volumetric heat source approach is used for this research in most cases.

## 4.7 Suggested Areas for Further Research

Areas for further potential research include work to better understand the reasons for mixingcontrolled models giving unstable results. This is an active area of research and improvement with FDS [34], [22]. The instability potentially ties into problems that have been reported in the past in using FDS to compute the pressure profile (and pressure losses due to fire) in long tunnels [29] and further investigation of this is a worthwhile topic for future research. This research could also look at the losses caused by the FFFS, and it is noted that empirical data (planned to be measured as part of the laboratory scale testing) could be of value.

Further research on model scale versus full-scale fire tests and the influence on critical velocity could be of value.

Finally, further research is suggested to develop a better understanding of the role of radiation heat transfer in the FFFS-EVS interactions. Results herein suggested the effect is probably minor, perhaps influencing backlayering length. However, earlier sections herein (Section 2) have shown that  grid  resolution  also  affects  backlayering  length,  and  a  more  in-depth  study  could  help determine the reasons for the differences in results.

<!-- image -->

Stamp

## ARCHIVED

## 5 LONGITUDINAL VENTILATION

The previous section demonstrated the prediction of longitudinal smoke control and the influence of the FFFS. A reduction in the upstream velocity necessary to control the smoke was seen and results  arrived  at  that  were  of  comparable  magnitude  to  that  predicted  with  the  NFPA  502 equations from the 2014 and 2017 editions. The NFPA 502 2020 edition equation includes an expression for backlayering distance, and this was tested in cases where backlayering occurred. The CFD model tended to predict a lower confinement velocity that the NFPA 502 2020 edition equation.

In this chapter the influence of FFFS and EVS parameters on the confinement velocity, including FHRR, water application rate, droplet size and tunnel geometry, is investigated.

| PARAMETER                     | VALUE                                                                                                                                                                      | NOTES / REFERENCE                                                                                                                                                                                                                                                                    |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Tunnel geometry configuration | A = Memorial Tunnel B = 8 m by 8 m (not used) C = 30 m (wide) by 6 m high (like an overbuild of a highway, 5 or 6 lanes) D = San Pedro de Anes (7.2 m wide and 5.2 m high) | Cross sections were selected to represent a spectrum of tunnels encountered in practice, refer to Figure 5-1, Figure 5-2, Figure 5-3 and Figure 5-4.                                                                                                                                 |
| FFFS - median droplet size    | 155 μm, 650 μm, 1200 μm                                                                                                                                                    | Typical droplet diameters in FFFS applications ranging from water mist sizes to conventional large drop sizes. The droplet parameters for the 650 μm and 1200 μm droplets were set per the trial A parameters in Table 3-2, and the 155 μm per the 'mist 1' parameters in Table 6-1. |

5.1 Overview 5.1.1 Parameter Study and CFD Model Setup The analysis considers the impact of the FFFS on confinement velocity over a range of different tunnel, fire and FFFS configurations as outlined in Table 5-1. The purpose is to demonstrate the potential for integrated FFFS and EVS design through a parameter study. Confinement velocity was determined by the temperature near the tunnel ceiling at a position located upstream of the fire.  Reasons  for  investigating  confinement  velocity  versus  critical  velocity  are  discussed  in Chapter 4. Table 5-1: Confinement velocity parameter study. PARAMETER Tunnel geometry configuration FFFS - median droplet size ARCHIVED

| PARAMETER                                                           | VALUE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | NOTES / REFERENCE                                                                                                                                                                                                                                |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FFFS - nozzle layout                                                | Total length 40 m, representing one zone around the fire and one upstream of the fire location. Nozzles arranged on a grid on the order of 4.0 m spacing in the longitudinal direction and between 2.4 m to 3.2 m in the tunnel width direction depending on tunnel geometry. Nozzle water flow rate is adjusted for specific cases to achieve desired water application rate to the zone.                                                                                                                                      | Typical design parameters                                                                                                                                                                                                                        |
| Water application rate                                              | 0, 2.5, 5, 10 mm/min                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Typical water application rates used in tunnel designs. The impact of these different parameters was tested on the tunnel type D only.                                                                                                           |
| FHRR                                                                | 5 MW, 20 MW, 100 MW                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Range of design FHRR values typically encountered in tunnel design. The impact of these different parameters was tested on tunnel type D only. Tunnel types A and C to consider the 20 MW result to verify that the behavior is similar.         |
| Temperature sensor location for backlayering indication and control | Base models used a sensor upstream a distance 2H (two tunnel height distance from the fire) on the tunnel centerline. Sensitivity analysis used sensors at a distance 1H upstream. ARCHIVED                                                                                                                                                                                                                                                                                                                                     | Temperature sensors were used to trigger confinement velocity determination. The velocity was started at a large magnitude and ramped down until the temperature sensor upstream of the fire registered a temperature 5 ⁰C greater than ambient. |
| Fire geometry                                                       | The volumetric heat source approach, as outlined in Section 4.3, was used with no radiation heat transfer active. The heat source was placed on the floor of the tunnel. For the 5 MW fire with no radiation modeled, the heat release rate per unit volume was 390.625 kW/m 3 , for 20 MW it was 446.429 kW/m 3 , and for 100 MW it was 446.429 kW/m 3 . When radiation was included the heat release rate per unit volume was increased based on the no radiation models including 70 percent of the FHRR as convective heat. | -                                                                                                                                                                                                                                                |

| PARAMETER       | VALUE                                                                                                     | NOTES / REFERENCE               |
|-----------------|-----------------------------------------------------------------------------------------------------------|---------------------------------|
| Fire parameters | Heat of combustion = 20 MJ/kg Soot yield = 0.1 g/g fuel CO yield = 0.05 g/g fuel Radiative fraction = 0.3 | Typical values seen in practice |
| Walls           | Smooth walls were modeled.                                                                                | -                               |
| CFD set up      | Volumetric heat source, grid resolution 0.4 m.                                                            | See also Chapter 4.             |

<!-- image -->

Engineering drawing

Figure 5-1: Tunnel cross section for CFD analysis (Memorial Tunnel) (ID A).

<!-- image -->

Engineering drawing

ARCHIVED

Figure 5-2: Square cross section for CFD analysis (ID B).

Figure 5-3: Rectangular cross section for CFD analysis (ID C).

<!-- image -->

Engineering drawing

Figure 5-4: Rectangular cross section for CFD analysis representing San Pedro de Anes tunnel at the fire site (7.2 m width used in models) (ID D).

<!-- image -->

Engineering drawing

## 5.1.2 List of Models and Results

Three different  tunnel  cross  sections  were  studied  (A,  C  and  D  as  described  in  the  previous section). In summary, modeling for longitudinal ventilation included the following:

- San Pedro de Anes tunnel (cross section D): Prediction of the tunnel environment during a fire  with longitudinal ventilation and FFFS operating. This corresponds to Case 21 models herein (denoted as EVS-21) and is the main geometry studied. Other variations of geometry were made as sensitivity analysis without the same comprehensive variation of parameters.

ARCHIVED

- Tests for prediction of critical velocity with an FFFS operating: Results found in the CFD study were compared to values shown by the equation developed by Ko and Hadjisophocleous [14].
- Extra wide cross section (cross section C): Prediction of the tunnel environment in a fire with longitudinal ventilation and FFFS operating. This corresponds to Case 13 (denoted as EVS13), which is mainly used to verify that impact of FFFS is like results shown for cross section D.
- Memorial  tunnel  (cross  section  A):  Prediction  of  the  tunnel  environment  in  a  fire  with longitudinal ventilation and FFFS operating. This corresponds to Case 14 (denoted EVS-14), which is mainly used to verify that the impact of FFFS is like results shown in cross section D.

Model output focuses on smoke control and confinement velocity. Additional output parameters are presented for some selected cases to illustrate the general trends in results with or without the FFFS.

## 5.2 Results for San Pedro de Anes Tunnel - Cross Section D

Model results for  the San  Pedro  de  Anes  tunnel  configuration  are  provided  in  Table 5-2  and Figure 5-5 (5 MW fires), Table 5-3 and Figure 5-6 (20 MW fires), and Table 5-4 and Figure 5-7 (100 MW fires). Pressure change results are quoted in the tables as well; as noted in the previous chapter, these should be interpreted with caution as determination of pressure change in tunnels with  FDS  is  an  area  of  active  development.  The  pressure  change  was  computed  based  on pressure at the inlet minus pressure at the exit.

<!-- image -->

Stamp

Table 5-2: Longitudinal ventilation - 5 MW fires.

| ID        | REMARKS                                                               |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APP'N RATE (mm/min) |   VEL (m/s) |   BACK- LAYER LENGTH (m) | TOTAL P DELTA (Pa)               |
|-----------|-----------------------------------------------------------------------|-------------|-----------------------|-----------------------------|-------------|--------------------------|----------------------------------|
| EVS-21-1  | Backlayer length was constrained by CFD model extents (70 m upstream) |           5 | N/A                   |                           0 |        1.29 |                       69 | N/A - due to back layer to inlet |
| EVS-21-2  | -                                                                     |           5 | 0.65                  |                         2.5 |        1.03 |                       34 | 2.2                              |
| EVS-21-3  | -                                                                     |           5 | 0.65                  |                           5 |        0.77 |                       17 | 1.7                              |
| EVS-21-4  | Water mist droplet size                                               |           5 | 0.155                 |                           5 |        0.72 |                       11 | 1.6                              |
| EVS-21-5  | -                                                                     |           5 | 0.65                  |                          10 |        0.60 |                       13 | 2.1                              |
| EVS-21-19 | Temp sensor moved closer to fire (1H instead of 2H)                   |           5 | N/A                   |                           0 |        1.39 |                       53 | 1.8                              |
| EVS-21-21 | Constant velocity upstream                                            |           5 | 0.65                  |                         2.5 |        1.29 |                        8 | 1.8                              |
| EVS-21-30 | Constant velocity upstream                                            |           5 | N/A                   |                           0 |        1.60 |                        2 | 2.0                              |

ARCHIVED

Table 5-3: Longitudinal ventilation - 20 MW.

| ID        | REMARKS                                                               |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APP'N RATE (mm/min) |   VEL (m/s) |   BACK- LAYER LENGTH (m) | TOTAL P DELTA (Pa)               |
|-----------|-----------------------------------------------------------------------|-------------|-----------------------|-----------------------------|-------------|--------------------------|----------------------------------|
| EVS-21-6  | Backlayer length was constrained by CFD model extents (70 m upstream) |          20 | N/A                   |                           0 |        1.72 |                       64 | N/A - due to back layer to inlet |
| EVS-21-7  | -                                                                     |          20 | 0.65                  |                         2.5 |        1.56 |                       25 | 4.6                              |
| EVS-21-8  | -                                                                     |          20 | 0.65                  |                           5 |        1.42 |                       14 | 4.5                              |
| EVS-21-9  | Water mist droplet size                                               |          20 | 0.155                 |                          10 |        1.01 |                       10 | 3.6                              |
| EVS-21-20 | Temp sensor moved closer to fire (1H instead of 2H)                   |          20 | N/A                   |                           0 |        1.87 |                       28 | 4.9                              |
| EVS-21-22 | Constant velocity upstream                                            |          20 | 0.65                  |                         2.5 |        1.72 |                       13 | 4.7                              |
| EVS-21-31 | Constant upstream velocity                                            |          20 | N/A                   |                           0 |        2.00 |                        4 | 5.4                              |

ARCHIVED

Table 5-4: Longitudinal ventilation - 100 MW.

| ID        | REMARKS                                                               |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APP'N RATE (mm/min) |   VEL (m/s) |   BACK- LAYER LENGTH (m) | TOTAL P DELTA (Pa)               |
|-----------|-----------------------------------------------------------------------|-------------|-----------------------|-----------------------------|-------------|--------------------------|----------------------------------|
| EVS-21-11 | Backlayer length was constrained by CFD model extents (70 m upstream) |         100 | N/A                   |                           0 |        1.76 |                       65 | N/A - due to back layer to inlet |
| EVS-21-12 | -                                                                     |         100 | 0.65                  |                         2.5 |        1.57 |                       28 | 12.4                             |
| EVS-21-13 | Water mist droplet size                                               |         100 | 0.155                 |                         2.5 |        1.31 |                       16 | 19.4                             |
| EVS-21-14 | -                                                                     |         100 | 0.65                  |                           5 |        1.46 |                       16 | 11.9                             |
| EVS-21-15 | Water mist droplet size                                               |         100 | 0.155                 |                           5 |        1.17 |                       13 | 15.9                             |
| EVS-21-16 | -                                                                     |         100 | 0.65                  |                          10 |        1.20 |                       14 | 18.0                             |
| EVS-21-17 | Water mist droplet size                                               |         100 | 0.155                 |                          10 |        1.00 |                       16 | 12.8                             |
| EVS-21-18 | -                                                                     |         100 | 1.20                  |                          10 |        1.50 |                       17 | 13.4                             |
| EVS-21-23 | Constant velocity upstream                                            |         100 | 0.65                  |                         2.5 |        1.76 |                       13 | 13.7                             |
| EVS-21-32 | Constant upstream velocity                                            |         100 | N/A                   |                           0 |        2.25 |                        1 | 18.1                             |

ARCHIVED

<!-- image -->

Line chart

<!-- image -->

Line chart

Figure 5-5: Backlayering and upstream velocity for 5 MW fires. ARCHIVED

Figure 5-6: Backlayering and upstream velocity for 20 MW fires.

<!-- image -->

Line chart

- Droplet  size:  Smaller  droplet  size  leads  to  less  backlayering  and  lower  upstream  velocity (EVS-21-3 versus EVS-21-4 (5 MW), and EVS-21-14 versus EVS-21-15 (100 MW)). Smaller droplets have a larger overall surface area, meaning they are more efficient at absorbing heat.
- Figure 5-7: Backlayering and upstream velocity for 100 MW fires. Key conclusions are as follows: · Backlayering is not controlled when the FFFS is not operating since case EVS-21-1 (5 MW), EVS-21-6 (20 MW) and EVS-21-11 (100 MW) are all showing backlayering length greater than 60 m, meaning that backlayering had extended to the inlet of the computation domain and may have increased even more if a greater upstream distance had been included. · Backlayering and upstream velocity is reduced for all models with FFFS compared to models without FFFS. The impact of FFFS on backlayering length is most obvious when comparing cases with the same upstream velocity: EVS-21-1 versus EVS-21-21 (5 MW), and EVS-21-6 versus EVS-21-22 (20 MW). For both comparisons, backlayering is reduced to a distance less than 50 m when FFFS is operating. · Temperature sensor used to trigger critical velocity: Sensor located closer to fire source (one tunnel height) reduces the backlayering length when FFFS is not used (EVS-21-1 versus EVS21-19 (5 MW), and EVS-21-6 versus EVS-21-20 (20 MW)). ARCHIVED
- Water application: Increased water application leads to less backlayering and lower upstream velocity  (EVS-21-2  versus  EVS-21-3  (5 MW),  EVS-21-7  versus  EVS-21-8  (20 MW),  and EVS-21-12 versus EVS-21-14 (100 MW)).
- At the 100 MW FHRR, cases EVS-21-32 notes a velocity of 2.25 m/s being enough to control the smoke. This result should be treated with caution as it might be a low velocity due to the relatively coarse grid used. Given the same grid is used throughout, the results herein should still be sufficient for examining trends with different model parameters. The FFFS is seen to reduce the confinement velocity.

The  equations  per  [14]  and  presented  in  Figure 4-12  are  used  to  estimate  the  change  in confinement velocity for scenarios with the FFFS operating. That is, the confinement velocity for a scenario with no FFFS is computed, and the equation is then used to predict the change in confinement velocity when FFFS is used. Figure 5-8 presents the equation used. In this figure Q' is the dimensionless heat release (see Figure 4-12), V is the critical/confinement velocity without FFFS (m/s) (e.g., this could be the velocity derived from a CFD model), VFFFS is the critical velocity accounting for FFFS (m/s), and ω is the water spray density (mm/min).

Figure 5-8: Equation. Critical velocity with an FFFS operating [14].

<!-- image -->

Engineering drawing

From the 20 MW CFD model (EVS-21-31), a velocity of 2.0 m/s (V in Figure 5-8) can control the smoke with no FFFS operating. Based on the velocity without FFFS being 2.0 m/s, the velocity with  5  mm/min  water  application  is  predicted  (using  equations  in  Figure 5-8)  to  be  1.64 m/s (assuming 30% radiation). The value is comparable to the CFD result including FFFS (1.42 m/s, EVS-21-8). It is especially comparable since case EVS-21-8 is showing a backlayering length of 14 m and if the case was run with a slightly higher velocity the backlayer length would decrease. Table 5-5 shows confinement velocities given by Ko and Hadjisophocleous [14] compared to the CFD results for 5 MW and 20 MW fires. In the use of the equation, radiation was removed from the FHRR since the CFD models being compared to have no radiation modeled. The CFD results represent confinement velocity, and the equation represents critical velocity, so caution is needed in  making  comparisons.  The  CFD,  in  these examples, thus  tends  to  predict  a  lower  value of confinement velocity. The difference between results with and without FFFS is of interest: · At 5 MW FHRR, the equation per [14] predicts a change in critical velocity of 0.72 m/s (1.721.00), and the CFD model reflects a change of 0.83 m/s. · At 20 MW FHRR, the equation per [14] predicts a change in critical velocity of 0.49 m/s (2.732.25), and the CFD model reflects a change of 0.58 m/s. It appears from these results that the equation for FFFS impact might serve well to estimate the likely change in velocity needed for longitudinal smoke control. Caution is needed as there may be a FHRR limit on this as the equation was originally only valid to 40 MW. ARCHIVED

Table 5-5: Confinement velocity and backlayering with FFFS.

| CASE ID   |   FHRR (MW) | FFFS                                              |   V IN CFD (m/s) | BACKLAYER IN CFD (m)   | VC (m/s) PER [14] AND FIGURE 4-12, 30 PERCENT RADIATION REMOVED (AND PERCENT DIFFERENCE TO CFD)   |
|-----------|-------------|---------------------------------------------------|------------------|------------------------|---------------------------------------------------------------------------------------------------|
| EVS-21-30 |           5 | N/A                                               |             1.60 | 2 to 4                 | 1.72 (+7.5 percent)                                                                               |
| EVS-21-3  |           5 | Drop size - 0.65 mm, water application - 5 mm/min |             0.77 | 16                     | 1.00 (+26 percent)                                                                                |
| EVS-21-31 |          20 | N/A                                               |             2.00 | 4                      | 2.74 (+31 percent)                                                                                |
| EVS-21-8  |          20 | Drop size - 0.65 mm, water application - 5 mm/min |             1.42 | 14                     | 2.25 (+45 percent)                                                                                |

| ID        | REMARKS         |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APPLICATION RATE (mm/min) |   UPSTREAM VELOCITY (m/s) |   BACKLAYER LENGTH (m) - INCREMENTS OF 1 M |
|-----------|-----------------|-------------|-----------------------|-----------------------------------|---------------------------|--------------------------------------------|
| EVS-13-1  | Cross section C |          20 | N/A                   |                                 0 |                      2.14 |                                         16 |
| EVS-13-2  | Cross section C |          20 | 0.65                  |                                 5 |                      1.84 |                                          4 |
| EVS-21-31 | Cross section C |          20 | N/A                   |                                 0 |                      2.00 |                                          4 |
| EVS-21-8  | Cross section C |          20 | 0.65                  |                                 5 |                      1.42 |                                         14 |

EVS-21-8 20 Drop size - 0.65 mm, water application - 5 mm/min 1.42 5.3 Results for Extra Wide Cross Section - Cross Section C The models conducted with the extra wide cross section (tunnel type C), aimed to clarify if smoke control is in line with results shown in San Pedro de Anes tunnel geometry (tunnel type D). Two scenarios were studied. Model results for the wide cross section tunnel configuration are provided in Table 5-6. The effect of the FFFS on smoke control is clear. Backlayering and upstream velocity is reduced with FFFS compared to models without FFFS. Hence, results are in line with results shown in Section 5.2. Table 5-6: Longitudinal ventilation, extra wide cross section - 20 MW. ID REMARKS FHRR (MW) FFFS DROP SIZE (mm) EVS-13-1 Cross section C 20 N/A EVS-13-2 Cross section C 20 0.65 EVS-21-31 Cross section C 20 N/A EVS-21-8 Cross section C 20 0.65 5.4 Results for Memorial Tunnel - Cross Section A ARCHIVED

The models conducted with the Memorial Tunnel geometry (A), aimed to clarify if smoke control is in line with results shown in San Pedro de Anes tunnel geometry (D). Two models were studied. Results for the Memorial tunnel configuration are provided in Table 5-7. The effect of the FFFS on smoke control is clear. Backlayering and upstream velocity is reduced with FFFS compared to models without FFFS. Hence, results are in line with results shown in Section 5.2 in terms of trends in the change for smoke management when FFFS is included.

Table 5-7: Longitudinal ventilation, Memorial tunnel - 20 MW.

| ID        | REMARKS                       |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APPLICATION RATE (mm/min) |   UPSTREAM VELOCITY (m/s) |   BACKLAYER LENGTH (m) - INCREMENTS OF 1 M |
|-----------|-------------------------------|-------------|-----------------------|-----------------------------------|---------------------------|--------------------------------------------|
| EVS-14-1  | Memorial Tunnel cross section |          20 | N/A                   |                                 0 |                      2.65 |                                         19 |
| EVS-14-2  | Memorial Tunnel cross section |          20 | 0.65                  |                                 5 |                      1.99 |                                          8 |
| EVS-21-31 | 7.4 m by 5.2 m cross section  |          20 | N/A                   |                                 0 |                      2.00 |                                          4 |
| EVS-21-8  | 7.4 m by 5.2 m cross section  |          20 | 0.65                  |                                 5 |                      1.42 |                                         14 |

EVS-21-8 7.4 m by 5.2 m cross section 20 0.65 5.5 Additional Results (Tenability) In the following section more results are shown for specific cases. The figures aim to highlight the differences for tenability between cases with and without FFFS operating. Tenability limits were sourced from NFPA 502 2020 edition, annex B [13]. For the 5 MW fires, case EVS-21-21 (drop size 0.65 mm, water application 2.5 mm/min) is compared to case EVS-21-1 (no FFFS). Upstream velocity in both cases is 1.29 m/s. For the 20 MW fires, case EVS-21-22 (drop size 0.65 mm, water application 2.5 mm/min) is compared to case EVS-21-6 (no FFFS). Upstream velocity in both  cases  is  1.72  m/s.  For  the  100  MW  fires,  case  EVS-21-23  (drop  size  0.65  mm,  water application 2.5 mm/min) is compared to case EVS-21-11 (no FFFS). Upstream velocity in both cases is 1.76 m/s. The plots are showing the following: · CO concentration along the tunnel 2.4 m above roadway level. Carbon monoxide results are provided in Figure 5-9, Figure 5-13 and Figure 5-17 (5 MW, 20 MW and 100 MW). The FFFS lowers  the  CO  concentration  slightly  for  the  20 MW  and  100  MW  cases  and  increases  it slightly for the 5 MW. However, in relation to tenability the impact is negligible. Note that the models do not include the impact of incomplete combustion on CO levels, which has been seen in testing to cause increased levels of CO downstream of the fire in FFFS testing [11]. ARCHIVED

- Relative humidity  downstream  of  fire  at different  heights  above  the  roadway.  Results  are provided  in  Figure 5-10,  Figure 5-14  and  Figure 5-18  (5  MW,  20  MW  and  100  MW).  An increase in the relative humidity is seen downstream of the fire when the FFFS is operated, although in all cases conditions are below the saturation limit.
- Temperature along the tunnel 2.4 m above roadway level. Results are provided in Figure 5-11, Figure 5-15 and Figure 5-19 (5 MW, 20 MW and 100 MW). Temperature is reduced due to the FFFS, however, not to a degree that has a major impact on tenability outcomes.
- Visibility along the tunnel 2.4 m above roadway level. Results are provided in Figure 5-12, Figure 5-16 and Figure 5-20 (5 MW, 20 MW and 100 MW). Visibility is improved upstream of the fire due to the improved degree of smoke control. At the fire, and downstream, there is

little  change  with  or  without  FFFS.  This  is  most  likely  because  visibility  downstream  is dominated by the mixing effect from longitudinal ventilation and there is no stratification for the FFFS to interfere with.

<!-- image -->

Line chart

Figure 5-9: CO concentration along tunnel for 5 MW fires with and without FFFS.

<!-- image -->

Line chart

ARCHIVED

Figure 5-10: Relative humidity downstream of fire for 5 MW fires with and without FFFS.

Figure 5-11: Temperature along tunnel for 5 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-12: Visibility along tunnel for 5 MW fires with and without FFFS.

Figure 5-13: CO concentration along tunnel for 20 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-14: Relative humidity downstream of fire for 20 MW fires with and without FFFS.

Figure 5-15: Temperature along tunnel for 20 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-16: Visibility along tunnel for 20 MW fires with and without FFFS.

Figure 5-17: CO concentration along tunnel for 100 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-18: Relative humidity downstream of fire for 100 MW fires with and without FFFS.

Figure 5-19: Temperature along tunnel for 100 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-20: Visibility along tunnel for 100 MW fires with and without FFFS.

## 5.6 Structural Temperatures

Structural temperatures have been studied for cases with a mixing-controlled combustion fire model.  The  mixing-controlled  approach  can  provide  a  more  accurate  prediction  of  flame temperatures nearer to the fire. The literature survey gives more discussion about CFD methods for modeling fires [1]. The following figures show the wall temperature at the ceiling along with adiabatic surface temperature at the ceiling. The adiabatic surface temperature is a measure of the heat flux incident to the structure. The FFFS lowers the temperature both in the proximity of the fire and downstream of fire. However, taking a nominal concrete temperature limit of 380 ⁰C to 400 ⁰C [13] (applied to wall temperature), it is apparent that the FFFS does not completely mitigate the structural vulnerability, although the extent of damage is potentially reduced based on consideration of temperatures alone. Note that in Section 3 CFD models were found to overpredict heat flux relative to test data and this might also be reflected in the peak adiabatic surface temperature reported here (larger values predicted). Further research would be needed to fully resolve this.

Refer to Figure 5-21 and Figure 5-22 for 20 MW, and Figure 5-23 and Figure 5-24 for 100 MW. For the 20 MW fires, case EVS-12-7 (drop size 0.65 mm, water application 2.5 mm/min) and case EVS-12-8 (drop size 0.65, water application 5.0 mm/min) are compared to case EVS-12-6 (no FFFS). For the 100 MW fires, case EVS-12-13 (drop size 0.65 mm, water application 2.5 mm/min) and EVS-12-15 (drop size 0.155, water application rate 2.5 mm/min) and case EVS-12-15 (drop size 0.155, water application rate 5.0 mm/min) are compared to case EVS-12-11 (no FFFS). The 20 MW case shows temperatures that are in the range of being acceptable, while at 100 MW the concrete temperature limits are exceeded near to the fire. The temperatures tend to be reduced with increased water application rate. Note that per Figure 5-23 and Figure 5-24; there is not a noteworthy sensitivity to water droplet size for the structural temperatures. ARCHIVED

Figure 5-21: Ceiling surface temperature for 20 MW fires with and without FFFS.

<!-- image -->

Line chart

Figure 5-22: Ceiling adiabatic surface temperature for 20 MW fires with and without FFFS.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 5-23: Ceiling surface temperature for 100 MW fires with and without FFFS.

Figure 5-24: Ceiling adiabatic surface temperature for 100 MW fires with and without FFFS.

<!-- image -->

Line chart

## 5.7 Research Findings

In this chapter a parameter investigation of the impact on FFFS on longitudinal smoke control has been conducted. The aim was to test the impact of FFFS on EVS over a range of different settings. The results showed the following:

- The results show that use of FFFS can reduce backlayering and confinement velocity over a range of different EVS and FFFS conditions.
- The results also confirm that a smaller droplet size and an increased water application rate leads to less backlayering and lower confinement velocity.
- The equation shown in Ko and Hadjisophocleous [14] may predict the likely change in critical or confinement velocity for cases with FFFS operating, relative to a case without FFFS. CFD models tend to predict a lower critical or confinement velocity, which might be caused by grid resolution (per findings summarized in Chapter 2).

ARCHIVED

- Impact on tenability due to FFFS was relatively minor, however, it is noted that the models herein did not compute the impact of FFFS on the FHRR. Thus, temperature reductions when FFFS reduces FHRR could be greater, and per published test findings [11], the CO levels might be higher downstream.
- Models were run using mixing-controlled combustion to look at the impact of FFFS on wall temperatures. The FFFS tended to reduce temperatures, although for large FHRRs (100 MW) the  temperatures  were  still  in  the  range  (local  to  the  fire)  where  the  concrete  could  be

vulnerable  to  spalling.  Increased  water  application  rate  caused  a  small  reduction  in temperature, while water drop size had a minor impact.

## 5.8 Suggested Areas for Further Research

Areas for further potential research include:

- Development of  an  equation  for  quantitative  prediction  of  FFFS  impact  on  the  EVS.  The equation shown in Ko and Hadjisophocleous [14] is suggested as a starting point and more CFD analysis on finer grids may show better agreement with this equation than achieved herein.
- Further studies on refined grids. Results herein were developed on relatively coarse grids, and  all  cases  used  the  same  settings  to  allow  comparison  between  impact  of  different parameters.  To  improve  the  accuracy  of  future  equation  development,  a  refined  grid  is recommended (0.2 m or finer per findings summarized in Chapter 2).
- Investigation of the ability of the FFFS to mitigate concrete spalling during a fire.

## ARCHIVED

## 6 TRANSVERSE VENTILATION AND WATER SPRAY INTERACTIONS

## 6.1 Overview

CFD models were conducted to investigate the interaction of the ventilation system and water droplets. Of interest was the question of whether the droplets would be entrained into an overhead exhaust duct, as illustrated in Figure 6-1. Water spray parameters tested are provided in Table 6-1 and these parameters are consistent with those used in Section 3 (Table 3-2).

<!-- image -->

Photograph

| PARAMETER                          | TRIAL A   | TRIAL B   | MIST 1                 | MIST 2                 |
|------------------------------------|-----------|-----------|------------------------|------------------------|
| Particle velocity (m/s)            | 18.5      | 8.1       | 12.0                   | 12.0                   |
| Spray angle (inner angle, degrees) | 30.0      | 19.6      | 1.0                    | 1.0                    |
| Spray angle (outer angle, degrees) | 74.5      | 81.5      | 60.0                   | 60.0                   |
| Particle diameter D v,0.5 (μm)     | 650.0     | 1080.7    | 155                    | 390                    |
| Droplet offset (mm)                | 30        | 30        | 100                    | 100                    |
| Nozzle flow rate (LPM)             | 82        | 80        | Varies, typically 39.6 | Varies, typically 39.6 |
| Particles per second               | 5000      | 5000      | 5000                   | 5000                   |
| Age (s)                            | 30        | 30        | 30                     | 30                     |
| Reference                          | EVS-10-18 | EVS-10-20 | [35]                   | [35]                   |

© WSP 2019 Figure 6-1: Interaction of water droplet and exhaust. Table 6-1: Droplet parameters tested. ARCHIVED

Models had a nominal grid resolution of 0.2 m. The ventilation rates used were comparable to a typical transverse ventilation system. The general model set up is shown in Figure 6-2. Note that the exhaust duct was not directly modeled in most cases, rather, a ventilation boundary condition was applied. Particles had to have a velocity of 0.01 m/s or greater to be extracted, otherwise they would not be entrained and would fall back to the roadway. This was specified in the FDS input files via the PARTICLE\_EXTRACTION\_VELOCITY parameter [8]. Results are presented as a percentage of the overall inflow of water into the domain. Based on mass balance sums, the result was typically accurate to within 1 percent or 2 percent of the overall water flow. The reason for some imbalance could be due to the particle extraction velocity, droplets falling back to the roadway, and effectively being counted twice, or numerical errors.

## 6.2 Transverse Exhaust Slots

- The key question being investigated here was whether the water spray was entrained into the exhaust duct in a transverse ventilation system. Several models were conducted to investigate the interaction between the transverse ventilation and droplet parameters. Key cases and model set up are summarized in detail in Table 6-2, and detailed observations are as follows: · Base case - case EVS-11-16 shows that droplets (type trial A in Table 6-1) are not entrained into the exhaust duct. Some of the water hits the tunnel sidewalls rather than the roadway. · Droplet size sensitivity - case EVS-11-17 looks at smaller drops and less water reaches the tunnel roadway, with significantly more water drift downstream. · Droplet size sensitivity - case EVS-11-22 looks at a larger drop size (per trial B in Table 6-1) and results show most water reaching the roadway, some water on tunnel sidewalls and some entrainment into the duct, although at 1.3 percent of the overall water application rate it is negligible and inside the typical amount of imbalance error observed in models. The larger droplets had a lower injection speed (8.1 m/s for trial B versus 18.5 m/s for trial A) and this could explain why some water was entrained into the duct. There is some imbalance for the larger droplet  size, but  it  is  within  1  percent  to  2  percent  of  the  overall water injected.  A  sensitivity case was conducted (EVS-11-40) where the duct was modeled (see Figure 6-3) rather than just a ventilation boundary condition to represent the slot; no appreciable change in  water delivery was observed although the amount of water entrained into the duct was decreased (suggesting that not modeling the duct at least gives a conservative result with respect to amount of water delivered to the tunnel space). ARCHIVED
- Water application rate sensitivity, less water but keeping with trial A droplet parameters - case EVS-11-18  looks  at  a  reduced  water  application  rate.  Results  do  not  change  by any  appreciable amount from the base case (EVS-11-16) in terms of the water distribution.
- Droplet size and water application rate sensitivity - case EVS-11-19 looks at a larger drop size (per trial B  in  Table 6-1) and increased water application rate. A similar distribution of water to the roadway and sidewalls is observed.
- Upstream velocity - case EVS-11-20 tested a scenario with no upstream velocity applied. The results did not change in terms of water distribution relative to the base case, and still there was only a negligible amount of water entrained into the duct.

<!-- image -->

Flow chart

Figure 6-2: Transverse ventilation set up.

<!-- image -->

Engineering drawing

| CASE ID                                   | GEOMETRY AND VENTILATION                                                                                                                                                  | FFFS PARAMETERS                                                                                                                                                                                    | FINDINGS                                                                                                                                                                                         |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 650 μm water drop, 5 mm/min (EVS-11-16)   | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s. | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1.  | 87.4 percent water on roadway, 12.7 percent water on sidewall, 0.1 percent water out of downstream portal. Water did not get entrained into the exhaust slot.                                    |
| 155 μm water drop, 2.5 mm/min (EVS-11-17) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s. | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 39.6 L/min, all other parameters otherwise as per Mist 1, Table 6-1. | 47.1 percent water on roadway, 0 percent water on sidewall, 53.9 percent water out of downstream portal. Droplets were blown downstream of the target zone but were not entrained into the duct. |

Figure 6-3: Sensitivity scenario schematic showing full duct model. Table 6-2: Transverse ventilation and water spray interactions. ARCHIVED

| CASE ID                                   | GEOMETRY AND VENTILATION                                                                                                                                                                              | FFFS PARAMETERS                                                                                                                                                                                            | FINDINGS                                                                                                                                                                                                    |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1081 μm water drop, 5 mm/min (EVS-11-22)  | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s.                             | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial B, Table 6-1.          | 89.3 percent water on roadway, 11.4 percent water on sidewall, 0.1 percent water out of downstream portal, 1.3 percent water through exhaust ports.                                                         |
| 1081 μm water drop, 5 mm/min (EVS-11-40)  | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s. Duct modeled above roadway. | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial B, Table 6-1.          | 88.4 percent water on roadway, 13.2 percent water on sidewall, 0.1 percent water out of downstream portal, negligible water through exhaust ports.                                                          |
| 650 μm water drop, 2.5 mm/min (EVS-11-18) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s.                             | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 41 L/min, all other parameters otherwise as per trial A, Table 6-1. ARCHIVED | 88.6 percent water on roadway, 11.5 percent water on sidewall, 0.6 percent water out of downstream portal, <0.1 percent water through exhaust ports. Droplets did not get entrained into the exhaust slot.  |
| 1081 μm water drop, 10 mm/min (EVS-11-19) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Upstream ventilation velocity 2.5 m/s.                             | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 164 L/min, all other parameters otherwise as per trial B, Table 6-1.         | 88.4 percent water on roadway, 12.1 percent water on sidewall, <0.1 percent water out of downstream portal, 1.7 percent water through exhaust ports. Droplets did not get entrained into the exhaust slot.  |
| 650 μm water drop, 5 mm/min (EVS-11-20)   | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 0.2 m by 1.0 m each, exhaust rate of 0.8 m 3 /s per port. Open boundaries at ends (no longitudinal ventilation).             | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1.          | 86.6 percent water on roadway, 13.9 percent water on sidewall, <0.1 percent water out of downstream portal, <0.1 percent water through exhaust ports. Droplets did not get entrained into the exhaust slot. |

The longitudinal drift of the water drops is visualized via a contour plot of water accumulation at the tunnel roadway. Figure 6-4 provides a contour for 650 µm water drops at 5 mm/min water application  (case  EVS-11-16),  and  Figure 6-5  for  155 µm  water  drops  at  2.5 mm/min  water application (case EVS-11-17). The water spray profile on the roadway is very different between the two cases. The smaller water drop diameter with less water flow, shows much more droplet drift  downstream, as would be expected. The smaller water drops also do not show as much lateral distribution of the water spray. The result demonstrates how the CFD model can be used to examine the water spray interaction with ventilation for delivery of water to the intended target. The result also shows that lower water application rates and smaller drop sizes are potentially more susceptible to ventilation conditions.

Figure 6-4: Contour view of tunnel roadway and water accumulation for 5 mm/min water application rate and 650 µm drop size.

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

ARCHIVED

Figure 6-5: Contour view of tunnel roadway and water accumulation for 2.5 mm/min water application rate and 155 µm drop size.

## 6.3 Single Point Exhaust

Additional cases were conducted to look at the effect of single point exhaust ventilation systems. Cases  with  an  overhead  exhaust  and  a  sidewall  point  exhaust  were  considered,  refer  to Figure 6-6 and Figure 6-7 respectively. Results are presented in Table 6-3 and summarized as follows:

- Single point exhaust (tunnel ceiling) - case EVS-11-31 shows that more than half of the water (58  percent)  from  the  nozzles  is  entrained  into  the  exhaust  duct.  The  result  is  based  on nozzles positioned at the center of each exhaust point, which is arguably not a very practical approach, but it is representative of the worst-case scenario in terms of minimal water going to where it is desired (tunnel roadway). A sensitivity scenario was conducted (EVS-11-35) where the duct above was modeled. In this case slightly less water was entrained into the duct (46 percent), although the qualitative behavior is the same. It is hypothesized that less water is entrained into the duct in the model where the duct is resolved because some droplets fall back through the opening, and when the duct is resolved, the airflow across the exhaust port is less uniform compared with a case where a velocity boundary condition is used to represent the exhaust. The result does support an approach where the duct is not resolved as being conservative since less water gets to the tunnel roadway.

· Single point exhaust with upstream tunnel air velocity - case EVS-11-23 considers a scenario where a single point exhaust system is modeled but with the tunnel air moving at 2.5 m/s. In this case a large percentage of water is still entrained into the duct (55.3 percent as opposed to  58  percent).  The  differences  between  the  two  scenarios  are  minor  since  the  droplets represent a typical nozzle (trial A) and not a fine drop nozzle like a mist system. · Sidewall exhaust - case EVS-11-21 represents a case where the exhaust point is in the tunnel wall. In this case water is still entrained into the duct though a lesser amount since the nozzles are  not  positioned  right  at  the  exhaust  point  (24.4  percent  entrained  as  opposed  to  58 percent). The results with single point exhaust show that more water is entrained into the duct compared with a typical transverse system. This result is expected since the single point arrangement has a larger concentrated exhaust whereas the transverse system has a much lower, distributed rate of exhaust. Even accounting for additional exhaust slots in a transverse system, the magnitude of  exhaust  through  a  single  point  system  is  still  many  orders  of  magnitude  more  than  in  a transverse system. There is a more urgent need to consider the potential for water entrainment with  single  point  exhaust  systems,  and the  possible  reduction  in  water  delivery  to  the  tunnel roadway, compared with transverse systems. ARCHIVED

<!-- image -->

Engineering drawing

<!-- image -->

Logo

Figure 6-6: Overhead exhaust configuration. Figure 6-7: Sidewall exhaust configuration. ARCHIVED

Table 6-3: Transverse ventilation, single point exhaust and water spray interactions.

| CASE ID                                 | GEOMETRY AND VENTILATION                                                                                                                                                                                                          | FFFS PARAMETERS                                                                                                                                                                                                       | FINDINGS                                                                                                                                      |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 650 μm water drop, 5 mm/min (EVS-11-31) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 2 m by 2 m each, exhaust rate of 40 m 3 /s per port. Upstream ventilation velocity 0 m/s. Duct not modeled, extract velocity 0.01 m/s.                   | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1.                     | 38 percent water on roadway, 5 percent water on sidewall, 58 percent through the exhausts.                                                    |
| 650 μm water drop, 5 mm/min (EVS-11-35) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 2 m by 2 m each, exhaust rate of 40 m 3 /s per port. Upstream ventilation velocity 0 m/s. Duct above modeled, exhaust point sealed shut once FFFS stops. | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1. ARCHIVED            | 47 percent water on roadway, 7 percent water on sidewall, 46 percent through the exhausts.                                                    |
| 650 μm water drop, 5 mm/min (EVS-11-23) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the ceiling, 2 m by 2 m each, exhaust rate of 40 m 3 /s per port. Upstream ventilation velocity 2.5 m/s. Duct not modeled, extract velocity 0.01 m/s.                 | One nozzle positioned at the geometric center of each exhaust port, offset 0.1 m below each exhaust port, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1.                     | 40.3 percent water on roadway, 5.4 percent water on sidewall, <0.1 percent water out of downstream portal, 55.3 percent through exhaust port. |
| 650 μm water drop, 5 mm/min (EVS-11-21) | Tunnel section 8.8 m wide, 4.4 m high. Two exhaust ports in the sidewall, 4 m long by 2 m high, exhaust rate of 80 m 3 /s. Upstream ventilation velocity 2.5 m/s. Duct not modeled, extract velocity 0.01 m/s.                    | Two nozzles positioned at the tunnel ceiling, symmetric with respect to the tunnel sidewalls, offset 0.1 m below the ceiling, nozzle flow rate of 82 L/min, all other parameters otherwise as per trial A, Table 6-1. | 64 percent water on roadway, 11 percent water on sidewall, <0.1 percent water out of downstream portal, 24.4 percent through exhaust port.    |

## 6.4 Research Findings

CFD analysis has been conducted to look at some cases where water droplets are potentially entrained into the exhaust duct in a transversely ventilated tunnel. A small subset of scenarios has been considered herein to demonstrate a few concepts:

- For a transverse system with many distributed slots, there is relatively little water entrainment into the duct. This does not mean no water would be observed being entrained into a duct in practice  since  the  water  could  be  entrained  at  several  exhaust  points  along  the  tunnel. However, in that scenario there would be additional nozzles too, which would cancel out much of the effect of causing deficiency of water delivery to the roadway.
- For a single point exhaust system, most if not all the exhaust rate is concentrated at one location. The volume of air at the exhaust point is orders of magnitude more than a transverse system based on distributed slots. Thus, in the analysis herein, a significant amount of water was entrained into the duct. This shows that the potential for water entrainment into the duct is likely to be more significant with a single point system. The degree of entrainment would likely be a function of exhaust rate, droplet parameters such as speed and diameter, spray angles and droplet residence time. · Different droplet parameters were considered and for relatively large droplets (650 µm and greater) the impact of the ventilation in the tunnel (upstream air speed) is minor. For smaller droplets  (155  µm)  the  tunnel  air  speed  has  a  significant  effect  on  droplet  drift.  When considering a fully transverse system the smaller droplet size cases did not show any more tendency for water to be entrained into the duct. · For  longitudinal  ventilation,  droplet  drift  downstream  increases  when  the  droplet  size decreases. The zoning of the FFFS can help to mitigate this and direct water to where it is needed. When droplet drift is a concern, a suggested practice is to activate multiple FFFS zones  including  one  over  the  fire  and  one  zone  upstream.  CFD  analysis  similar  to  that presented  herein  could  be  considered  to  check  the  FFFS  zone  arrangement,  ventilation configuration and droplet drift. ARCHIVED

In summary, the integration between the FFFS and EVS should consider the droplet parameters based on the nozzles provided, the ventilation conditions, and placement of the nozzles. CFD models have shown that there is potential  for  water  application  to be  affected and,  in  lieu  of running a full-scale test, CFD models could give an indication of optimal combinations and nozzle layouts in a design development exercise.

## 6.5 Suggested Areas for Further Research

Additional  parameter  studies  on  water  droplet  size,  spray  patterns,  longitudinal  ventilation configuration,  and  extent  of  droplet  drift  could  be  of  interest  for  further  potential  research. Development of an empirical correlation could be useful as well.

## 7.1 Overview

Transverse ventilation systems utilize exhaust and supply ducts to control airflow in a tunnel. Many existing tunnels in the United States use a transverse ventilation system. Specific validation of CFD modeling for the transverse ventilation approach has not been conducted because the validation for the critical velocity cases includes all the major physics: turbulent flow, heat transfer, FFFS modeling, and cooling due to the FFFS. This investigation is intended to demonstrate the approach  to  assessing  different  FFFS  and  EVS  configurations.  The  principal  hypotheses investigated are the same as those presented in previous sections:

· That FFFS and EVS can be integrated and EVS capacity optimized as a result of the cooling effects of the FFFS water spray. · That CFD can be used to predict FFFS and EVS interaction for design integration. Integration combinations of FFFS and EVS include water drop size, water application rate, ventilation type and rate, and tunnel geometry. Relative to the above hypotheses, there are three aspects that arise for further investigation when a transverse ventilation system is used with FFFS: 1. Smoke management performance due to cooling of the combustion products. 2. Interaction between ventilation exhaust and the FFFS spray. 3. Pressure loss due to any pipework located in exhaust duct. Pressure loss (item 3) is to be determined as part of the testing program; and this is a relatively easily measured quantity in a test and CFD methods are also well established for this purpose. Interaction  between  the  water  spray  and  exhaust  is  investigated  in  Chapter  6.  Smoke management (item 1) is considered herein using CFD. Note that the CFD models do not include fire suppression; only cooling of the products of combustion is included. 7.2 Transverse Ventilation - Distributed Exhaust ARCHIVED

A typical transverse ventilation system is shown in Figure 7-1, Figure 7-2, and Figure 7-3. The basic concept is to operate a combination of supply and exhaust fans to either: 1) Achieve a longitudinal velocity in the direction of vehicle travel when in unidirectional traffic mode; or 2) Minimize  longitudinal  velocity  and  exhaust smoke  to  achieve minimal  smoke  spread  when  in bidirectional traffic mode. The most challenging configuration for smoke management is operation to minimize smoke spread when the fire is placed near the exhaust duct bulkhead; in this mode of operation the longitudinal velocity is minimal and there exists the greatest potential for smoke spread. Figure 7-4 illustrates the concept. CFD models were developed for this ventilation regime.

## 7 TRANSVERSE VENTILATION

<!-- image -->

Icon

<!-- image -->

Photograph

<!-- image -->

Engineering drawing

Figure 7-1: Tunnel with transverse ventilation showing ducts. © WSP 2019 Figure 7-2: Photo of a tunnel with transverse ventilation. ARCHIVED

Figure 7-3: Transverse ventilation system schematic.

<!-- image -->

Icon

Figure 7-4: Transverse ventilation system in exhaust near to the bulkhead. One of the aims of the CFD models was to investigate the performance of a transverse ventilation system  with  an  FFFS  operating.  In  addition,  the  impact  of  different  droplet  sizes  and  water application rates were investigated. The main parameters investigated from the models were the smoke spread along the tunnel ceiling and visibility 2.4 m above the roadway. The tunnel cross section configuration (tunnel type D) was used in the analysis. Case 15 (EVS-15-XX) models follow  the  ventilation  system  schematic  shown  in  Figure 7-3  with  small,  evenly  distributed, exhaust/supply  openings  along  the  tunnel  and  supply  flues  located  at  roadway  level.  These models only include active exhaust from ceiling, where all exhaust ports are exhausting air/smoke. The tunnel studied with this ventilation configuration is 1020 m long with the fire located in the middle of tunnel (510 m) at the same location as the bulkhead in the exhaust duct. A summary of the models is provided in Table 7-1. ARCHIVED

Due to the large model size (1020 m long), the CFD models were developed on a coarse grid at 0.4 m. As noted in Section 2.3.9, results can be sensitive at coarse grids, but the general trends can be seen, which meets the aims herein. The fire was modeled via a volumetric heat source. Radiation was not directly modeled, and a 30 percent radiation fraction was used (i.e., it was deducted from the modeled FHRR). Results were tested with a mixing-controlled approach as well, but these were unstable. Models were run to 900 s, which gave a steady result in terms of smoke spread extent. Averaging was performed between 800 s and 900 s.

The results in terms of smoke spread along the ceiling, throughout the tunnel. Key conclusions are as follows, with detailed plots and discussion following:

- FFFS: The effect of the FFFS on smoke control is clear for 20 MW and 100 MW cases. When FFFS is operating  the smoke  spread  along  the ceiling  is  reduced.  However,  the  reduced smoke spread due to FFFS operating does not cover for a reduced ventilation exhaust rate (at 30 percent reduction).

- Droplet size: Finer droplets leads to better smoke control (case EVS-15-10 versus EVS-1512).
- Water application: Increased  water application  from 2.5 mm/min  to 10.0 mm/min  leads  to better  smoke  control  (EVS-15-10  versus  EVS-15-11).  However,  when only  increasing the water application from 2.5 mm/min to 5.0 mm/min for models with 0.155 mm droplet size (EVS-15-12 versus EVS-15-9), the increase in smoke control effectiveness is limited.
- Tenability: The momentum of the FFFS droplets causes smoke to mix downwards toward the tunnel roadway. Thus, in several cases, at a height 2.4 m above the roadway the low visibility region near the fire covers a longer distance compared with the case with no FFFS. However, at large FHRR (100 MW), the cooling effect of the FFFS improves exhaust efficiency enough to  also  reduce  the  length  of  the  untenable  zone.  Tenability  in  the  active  FFFS  zone  is discussed further below.

| ID        | VENTILATION CONFIGURATION                                   |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APPLICATION RATE (mm/min) |
|-----------|-------------------------------------------------------------|-------------|-----------------------|-----------------------------------|
| EVS-15-4  | 100 cfm/lane foot exhaust rate, evenly distributed          |           5 | N/A                   |                                 0 |
| EVS-15-5  | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | N/A                   |                                 0 |
| EVS-15-6  | 100 cfm/lane foot exhaust rate, evenly distributed ARCHIVED |         100 | N/A                   |                                 0 |
| EVS-15-7  | 100 cfm/lane foot exhaust rate, evenly distributed          |           5 | 0.65                  |                               5.0 |
| EVS-15-8  | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | 0.65                  |                               5.0 |
| EVS-15-9  | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | 0.155                 |                               5.0 |
| EVS-15-10 | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | 0.65                  |                               2.5 |
| EVS-15-11 | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | 0.65                  |                              10.0 |
| EVS-15-12 | 100 cfm/lane foot exhaust rate, evenly distributed          |          20 | 0.155                 |                               2.5 |
| EVS-15-13 | 70 cfm/lane foot exhaust rate, evenly distributed           |          20 | 0.65                  |                               5.0 |
| EVS-15-14 | 100 cfm/lane foot exhaust rate, evenly distributed          |         100 | 0.65                  |                               5.0 |
| EVS-15-15 | 70 cfm/lane foot exhaust rate, evenly distributed           |         100 | 0.65                  |                                 0 |

Figure 7-5 shows visibility along tunnel ceiling for the two 5 MW models and impact of FFFS on smoke spread along the tunnel is low. At roadway level, as seen in Figure 7-6, the FFFS scenario shows lower visibility due to the FFFS mixing smoke downward for a region approximately 30 m on each side of the fire. Temperature and carbon monoxide at 2.4 m above the roadway is also affected, with the FFFS mixing heat and gas down from ceiling level, as shown in Figure 7-7 and Figure 7-8. Quantities  were  spatially averaged  across  the  tunnel  width  from 2.1 m  above  the roadway to 2.4 m. Thus, some peak values of temperature or CO might be less than expected.

<!-- image -->

Line chart

<!-- image -->

Logo

Figure 7-5: Visibility along ceiling for 5 MW fires (EVS-15-4 and EVS-15-7). ARCHIVED

Figure 7-6: Visibility 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-7: Temperature 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7).

<!-- image -->

Line chart

Visual representation of the smoke spread for the different scenarios is provided in Figure 7-11, Figure 7-12  and  Figure 7-13.  The  contours  show  the  extent  of  smoke  spread  and  mixing downward. The results help to understand that the down-mixing of smoke is not too severe relative to a case with no FFFS. The smoke is not cooled to such an extent that it mixes down to road level beyond the FFFS zone. There is actually some recovery of smoke stratification, which is likely part due to exhaust and part due to the FFFS not removing all the heat from combustion products. Similar behavior (smoke stratifying beyond the active FFFS zone) has been observed in tests [36].

Figure 7-8: Carbon monoxide 2.4 m above the roadway for 5 MW fires (EVS-15-4 and EVS-15-7). Figure 7-9 shows visibility along ceiling for three of the 20 MW cases. The base case model without  FFFS  (EVS-15-5)  is  compared  to  FFFS model  (EVS-15-8, drop  size  0.65  mm,  water application  rate  5.0  mm/min)  and  FFFS  in  conjunction  with 30 percent  reduced  exhaust  rate (EVS-15-13). The FFFS reduces the smoke spread along the ceiling approximately 20 m to 30 m both upstream and downstream of the fire location. However, the reduced smoke spread due to the FFFS does not compensate the 30 percent reduction in exhaust rate since smoke spread along the tunnel is greater (model EVS-15-13 compared to EVS-15-5). Like the 5 MW cases, decreased visibility is seen at a height 2.4 m above the roadway, refer to Figure 7-10. Some visibility is recovered beyond the active FFFS zones (zones exist about 20 m each side of the fire). ARCHIVED

Figure 7-9: Visibility along ceiling for 20 MW fires (EVS-15-5, EVS-15-8 and EVS-15-13).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-10: Visibility 2.4 m above the roadway for 20 MW fires (EVS-15-5, EVS-15-8 and EVS-15-13).

Figure 7-11: Visualization of smoke spread (cropped at 10 m or less visibility), no FFFS.

<!-- image -->

Line chart

<!-- image -->

Engineering drawing

<!-- image -->

Line chart

Figure 7-12: Visualization of smoke spread (cropped at 10 m or less visibility), FFFS. Figure 7-13: Visualization of smoke spread (cropped at 10 m or less visibility), FFFS, reduced exhaust rate. Figure 7-14 and Figure 7-15 show temperature and carbon monoxide along the tunnel and there is a noticeable increase in both quantities in the active FFFS zone. This is attributable to the FFFS mixing products of combustion down from the ceiling. There is a gradual recovery once remote from the FFFS zone. Note that the peak temperature in Figure 7-14 is less than observed in Figure 7-7, and the same is noted for carbon monoxide in Figure 7-8 and Figure 7-15. The reason for the different results is not obvious since the larger fire case would have been expected to have the larger peaks. It may be due to the interaction between the volume heat source and turbulent flow. Inspection of the results does show, as expected, that the larger fire cases have a much longer domain affected by heat and carbon monoxide. ARCHIVED

Visualization of the temperature field is provided in Figure 7-16, Figure 7-17 and Figure 7-18 for the 20 MW scenarios with no FFFS, FFFS and FFFS with reduced exhaust rate. The results show that the FFFS results in a reduced extent of high temperatures. Thus, while the FFFS might mix some hot gas downward in the zone of operation, overall, there is cooling.

Figure 7-14: Temperature 2.4 m above the roadway for 20 MW fires (EVS-15-5 and EVS-15-8 and EVS-15-13).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-15: Carbon monoxide 2.4 m above the roadway for 20 MW fires (EVS-15-5 and EVS-15-8 and EVS-15-13).

<!-- image -->

Engineering drawing

Figure 7-16: Visualization of temperature (cropped below 60 ⁰ C), no FFFS.

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

The results presented to in this section confirm expected behavior, which is that the FFFS mixes products of combustion down toward roadway level in the region of the tunnel where the FFFS operates. Figure 7-19 and Figure 7-20 show some additional visualization where the temperature field shows values 28 ⁰C and higher. This clearly shows the additional heat being mixed down in the  region  of  the  FFFS  and  recovery  beyond  the  FFFS  zone  as  combustion  products  are exhausted and residual heat causes smoke to restratify, which has been observed in field tests [36].

Figure 7-17: Visualization of temperature (cropped below 60 ⁰ C), FFFS. Figure 7-18: Visualization of temperature (cropped below 60 ⁰ C), FFFS, reduced exhaust rate. ARCHIVED

More ventilation capacity is not suggested to try and recover tenability of conditions in the zone where the FFFS is active since the reduction in tenability is caused by the downward mixing induced by the water spray. The FFFS helps the EVS to operate more efficiently, as can be seen through the reduction in smoke spread extent and the small amount of additional smoke spread when the exhaust rate is reduced by 30 percent. Increasing the exhaust rate might render the FFFS less effective since it potentially could draw more water up into the exhaust duct and make it  harder to deliver water the fire site. It is also noted that the models herein do not model fire suppression and if that was considered, then it is likely that the smoke spread extent would reduce even more. Lastly, a typical FFFS zone length is 20 to 30 m in length (80 ft. to 100 ft.) and this is comparable to the  fire perimeter  length  (applies both  sides  of  the  fire)  noted  in  the  annex  of NFPA 502, where the text states that application of tenability criteria within the fire perimeter is impractical.

<!-- image -->

Engineering drawing

<!-- image -->

Engineering drawing

Figure 7-23 shows visibility along ceiling for the 100 MW cases. The base case model without FFFS (EVS-15-6) is compared to a model with FFFS (EVS-15-14, drop size 0.65 mm, water application  rate  5  mm/min) and  FFFS  in  conjunction  with  a  30 percent  reduced exhaust  rate (EVS-15-15). For this larger fire size, the impact of FFFS is greater. The FFFS reduces the smoke spread along the ceiling approximately 50 m both upstream and downstream of the fire location. However, like the 20 MW fires, the reduced smoke spread due to the FFFS does not cover the 30 percent reduction in exhaust rate since smoke spread along the tunnel ceiling is greater (model EVS-15-15 compared to EVS-15-6). Figure 7-24 shows results for the 100 MW fires at 2.4 m above the roadway and the trends are like the smoke spread at the tunnel ceiling.

Figure 7-19: Visualization of temperature (black is 28 ⁰ C and higher), no FFFS. Figure 7-20: Visualization of temperature (black is 28 ⁰ C and higher), FFFS. The  impact  of  varying  FHRR  and  FFFS  parameters  is  now  considered.  Figure 7-21  shows visibility for models with different FFFS input parameters. It is evident that decreasing the droplet size  or  increasing  the  water  application  rate  leads  to  less  smoke  spread  along  the  ceiling. Figure 7-22  provides  visibility  results  2.4 m  above  the  roadway,  with  less  pronounced  direct effects; likely a result of the complex interaction between the amount of smoke being exhausted and the down mixing of smoke by the FFFS. ARCHIVED

The FFFS mixing smoke downward for the 100 MW fire cases is not a factor because the volume of smoke is so large that the untenable zone extends well beyond the fire perimeter, typically 100 m to 200 m on both sides of the fire (see Figure 7-24). The FFFS improves conditions in this case because the cooling effect improves exhaust efficiency (with respect to distance the smoke spreads). Similar trends are seen for carbon monoxide, as shown in Figure 7-25.

Figure 7-21: Visibility along ceiling for 20 MW fires (EVS-15-9, EVS-15-10, EVS-15-11 and EVS-15-12). Droplet size and water application impact.

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-22: Visibility 2.4 m above the roadway for 20 MW fires (EVS-15-9, EVS-15-10, EVS-15-11 and EVS-15-12). Droplet size and water application impact.

Figure 7-23: Visibility along ceiling for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-24: Visibility 2.4 m above the roadway for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15).

<!-- image -->

Line chart

Figure 7-25: Carbon monoxide 2.4 m above the roadway for 100 MW fires (EVS-15-6, EVS-15-14 and EVS-15-15). 7.3 Transverse Ventilation - Point Exhaust The second ventilation configuration studied is a point exhaust system (cases EVS-16-XX). For this configuration, two larger exhaust points spanning the tunnel width are located at five different locations within the tunnel, as shown in Figure 7-26. Depending on the scenario, the exhaust points can be either on the ceiling (refer Figure 6-6) or sidewall (refer Figure 6-7). For most of the models, only four of the total ten exhaust points are operating (two pairs). Exhaust points are spaced 30 m apart with a dimension 2 m by 2 m for each point. The tunnel studied  with  this ventilation configuration is 200 m long with the fire located 70 m from portal (length units are expressed in plots relative to the fire set at 0 m). The upstream velocity was held constant in these models. Models with point exhaust are listed and described in Table 7-2 . The CFD methodology is the same as described in the previous section. ARCHIVED

Figure 7-26: Ventilation configuration for case EVS-16.

<!-- image -->

Engineering drawing

Table 7-2: Transverse ventilation - point exhaust.

| ID        | VENTILATION CONFIGURATION (SEE FIGURE 7-26 FOR LOCATION OF EXTRACT POINTS)                                    |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APPLICATION RATE (mm/min) |
|-----------|---------------------------------------------------------------------------------------------------------------|-------------|-----------------------|-----------------------------------|
| EVS-16-1  | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.          |          20 | N/A                   |                                 0 |
| EVS-16-2  | As per EVS-16-1                                                                                               |          20 | 0.65                  |                                 5 |
| EVS-16-19 | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.          |          20 | N/A                   |                                 0 |
| EVS-16-20 | As per EVS-16-19                                                                                              |          20 | 0.65                  |                                 5 |
| EVS-16-3  | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.            |          20 | N/A                   |                                 0 |
| EVS-16-4  | As per EVS-16-3                                                                                               |          20 | 0.65                  |                                 5 |
| EVS-16-21 | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.            |          20 | N/A                   |                                 0 |
| EVS-16-22 | As per EVS-16-21                                                                                              |          20 | 0.65                  |                                 5 |
| EVS-16-5  | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.          |         100 | N/A                   |                                 0 |
| EVS-16-6  | As per EVS-16-5                                                                                               |         100 | 0.65                  |                                 5 |
| EVS-16-7  | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s. ARCHIVED   |         100 | N/A                   |                                 0 |
| EVS-16-8  | As per EVS-16-7                                                                                               |         100 | 0.65                  |                                 5 |
| EVS-16-9  | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.          |         100 | 1.20                  |                                10 |
| EVS-16-10 | As per EVS-16-9                                                                                               |         100 | 0.155                 |                               2.5 |
| EVS-16-11 | Extract points each side of fire (A, C) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.   |          20 | N/A                   |                                 0 |
| EVS-16-12 | As per EVS-16-11                                                                                              |          20 | 0.65                  |                                 5 |
| EVS-16-13 | Extract points each side of fire (A, C) at sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.  |          20 | N/A                   |                                 0 |
| EVS-16-14 | As per EVS-16-13                                                                                              |          20 | 0.65                  |                                 5 |
| EVS-16-15 | Extract points each side of fire (A, C) at ceiling. Total exhaust rate 100 m 3 /s. Upstream velocity 1.3 m/s. |          20 | N/A                   |                                 0 |
| EVS-16-16 | As per EVS-16-15                                                                                              |          20 | 0.65                  |                                 5 |

| ID        | VENTILATION CONFIGURATION (SEE FIGURE 7-26 FOR LOCATION OF EXTRACT POINTS)                            |   FHRR (MW) | FFFS DROP SIZE (mm)   |   WATER APPLICATION RATE (mm/min) |
|-----------|-------------------------------------------------------------------------------------------------------|-------------|-----------------------|-----------------------------------|
| EVS-16-17 | All extract points operating (A, B, C, D, E). Total exhaust rate 100 m3/s. Upstream velocity 1.0 m/s. |          20 | N/A                   |                                 0 |
| EVS-16-18 | As per EVS-16-17                                                                                      |          20 | 0.65                  |                                 5 |

Key conclusions are as follows:

- FFFS and exhaust points downstream: The results are showing that the effect of FFFS is limited when only exhausting downstream of fire (models EVS-16-1 to EVS-16-8). For these cases, the FFFS is only able to clearly decrease smoke spread for 20 MW fires when exhaust is at ceiling level, refer to Figure 7-27. With the fire size of 100 MW or with exhaust along at wall  level,  the  smoke  spread  is  similar  and  independent  of  operation  of  FFFS  (compare Figure 7-33 with Figure 7-34). · FFFS and exhaust points downstream, tenability effects: The effects of FFFS on tenability (examined here with visibility only since this quantity tends to be the first tenability criterion not met and carbon monoxide and temperature behave similar) at roadway level are minor, as seen in Figure 7-28 and Figure 7-30. The single point exhaust models have a much larger exhaust rate and longitudinal velocity in the region of fire and FFFS zone, thus meaning that the mixing of combustion products is dominated by turbulent flow with the FFFS mixing having only a minor additional impact. · FFFS and exhaust points downstream, adjusted upstream velocity: A lower upstream velocity results in slight smoke spread upstream of the fire location when FFFS is not applied (EVS16-19 and EVS-16-21). When FFFS is applied (EVS-16-20 and EVS-16-22) the smoke spread upstream is limited, refer to Figure 7-29 and Figure 7-32. A lower upstream velocity also leads to  less  smoke  spread  downstream of the fire  (compare  Figure 7-27  with  Figure 7-29, and Figure 7-31 and Figure 7-32). ARCHIVED
- FFFS and exhaust points either side of the fire: For models with exhaust both upstream and downstream of the fire, smoke spread is clearly reduced when FFFS is operating. Dependent on ventilation configuration (exhaust at ceiling or wall level), the smoke spread is reduced either  upstream,  downstream  or  both  upstream  and  downstream  of  the  fire,  refer  to Figure 7-36 to Figure 7-41. When smoke spread is reduced, it is reduced to exhaust points closer  to  the  fire.  Figure 7-36  shows  that  smoke  spread  reduction  downstream  of  fire  of approximately 30 m since this is the distance between the exhaust locations (A and C in Figure 7-26).
- FFFS and exhaust points either side of the fire, tenability effects: For exhaust either side of the fire at ceiling level, the smoke management is more like the transverse system considered in  the  previous  section.  Figure 7-37  shows  visibility.  Velocity  local  to  the  fire  is  reduced somewhat and smoke stratification is observed. When the FFFS is operated in this case there is some mixing of the smoke downwards and a reduction in visibility as a result. When the

- exhaust is on the sidewall, see Figure 7-39, the velocity due to the sidewall exhaust tends to mix smoke down and the exhaust is not as effective. In this scenario the FFFS cooling helps to improve smoke capture slightly.
- Droplet  size  and  water  application:  Results  in  Figure 7-35  indicate  that  small  droplets  in conjunction with a lower water application rate (EVS-16-10) can be more effective in terms of smoke control compared to a model with large droplet size and a high water application rate (EVS-16-9).

<!-- image -->

Line chart

Figure 7-27: Visibility along ceiling EVS-16-1 and EVS-16-2 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s).

<!-- image -->

Logo

ARCHIVED

Figure 7-28: Visibility 2.4 m above roadway, EVS-16-1 and EVS-16-2 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-29: Visibility along ceiling EVS-16-19 and EVS-16-20 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s, decreased upstream velocity).

Figure 7-30: Visibility 2.4 m above roadway, EVS-16-19 and EVS-16-20 (20 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s, decreased upstream velocity).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-31: Visibility along ceiling EVS-16-3 and EVS-16-4 (20 MW, extract points C and E at sidewall, total exhaust rate 150 m 3 /s).

Figure 7-32: Visibility along ceiling EVS-16-21 and EVS-16-22 (20 MW, extract points C and E at sidewall, total exhaust rate 150 m 3 /s, decreased upstream velocity).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-33: Visibility along ceiling EVS-16-5 and EVS-16-6 (100 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s).

Figure 7-34: Visibility along ceiling EVS-16-7 and EVS-16-8 (100 MW, extract points C and E at sidewall, total exhaust rate 150 m 3 /s).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-35: Visibility along ceiling EVS-16-9 and EVS-16-10 (100 MW, extract points C and E at ceiling level, total exhaust rate 150 m 3 /s), FFFS parameters sensitivity.

Figure 7-36: Visibility along ceiling EVS-16-11 and EVS-16-12 (20 MW, extract points A and C at ceiling level, total exhaust rate 150 m 3 /s).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-37: Visibility 2.4 m above roadway, EVS-16-11 and EVS-16-12 (20 MW, extract points A and C at ceiling level, total exhaust rate 150 m 3 /s).

Figure 7-38: Visibility along ceiling EVS-16-13 and EVS-16-14 (20 MW, extract points A and C at sidewall, total exhaust rate 150 m 3 /s).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-39: Visibility 2.4 m above roadway EVS-16-13 and EVS-16-14 (20 MW, extract points A and C at sidewall, total exhaust rate 150 m 3 /s).

Figure 7-40: Visibility along ceiling EVS-16-15 and EVS-16-16 (20 MW, extract points A and C at ceiling level, total exhaust rate 100 m 3 /s).

<!-- image -->

Line chart

<!-- image -->

Line chart

ARCHIVED

Figure 7-41: Visibility along ceiling EVS-16-17 and EVS-16-18 (all extract points A, B, C, D, and E at ceiling level, total exhaust rate 100 m 3 /s).

## 7.4 Research Findings

The transverse ventilation results show that FFFSs can be effective for improving smoke control. The smoke spread along the tunnel ceiling was reduced for 20 MW and 100 MW fires when FFFS was modeled. It can therefore be argued that a FFFS can be used to decrease the ventilation capacity  needed  within  a  tunnel;  with  either  a  distributed  transverse  system  or  a  single  point transverse system.

The FFFS can cause combustion products to be mixed downward toward the roadway, possibly causing a reduction in tenability in the region local to the fire and active FFFS zone. The tenability tends to be regained once remote from the immediate fire perimeter. It is suggested that local loss of tenability needs to be balanced against the benefits, which can include improved smoke exhaust effectiveness (less smoke spread remote from the fire) and a possible reduction in FHRR. More exhaust is unlikely to improve conditions and may have a counter effect, since increased exhaust could potentially draw more water up into the exhaust duct, thereby decreasing FFFS effectiveness. Management in operation is suggested as the better way to handle any potential loss in visibility, with policy on when to operate the FFFS being informed by CFD models of the integrated FFFS and EVS operation. Some examples of FFFS operational practice suggest a preference to operate the FFFS early in an incident to reduce the chances that the fire grows to a large magnitude [37]. 7.5 Suggested Areas for Further Research Further parameter studies are one area for potential further research. The analysis did not aim to answer to what extent the ventilation rate can be decreased as that result would vary from project to project dependent on the different system parameters. The results also indicate that a small droplet size in conjunction with a low water application rate can be more effective in terms of smoke control compared to larger droplet sizes in conjunction with a greater water application rate. Future research could consider sensitivity of outcomes to grid resolution. ARCHIVED

## 8 CONCLUSION

## 8.1 Research Hypotheses and Discussion

The hypotheses for this work were looking at the integration of the FFFS and EVS, and modeling the systems using CFD. Principal hypotheses being investigated are described below.

The first hypothesis is that FFFS and EVS can be integrated and EVS capacity optimized as a result of the cooling effects of the FFFS water spray. The following points are made:

- This hypothesis can be verified via measurement of the critical (or confinement) velocity for smoke control, pressure loss due to the FFFS water spray and impact of the EVS on water delivery. If the hypothesis is true, then the critical (or confinement) velocity should decrease due to the cooling. Refer to Section 4.2 and Section 4.3 for an investigation of confinement velocity with no FFFS operating, and Section 4.5 for scenarios with the FFFS operating. The results  show  a  reduction  in  the  longitudinal  velocity  needed  to  control  the  smoke  spread upstream as a result of the cooling of combustion products. Similar trends are seen in the results from Section 5.
- Finally, the EVS should not cause excessive water droplet drift as to cause a negative effect on  water  droplet  delivery  to  the  fire  zone.  Refer  to  Chapter  6,  which  looks  at  interaction between the water spray and ventilation, Figure 6-4 and Figure 6-5. This result shows that droplet  drift  downstream  becomes  more  significant  for  smaller  water  drop  sizes.  Typical deluge system drop sizes are not affected too much. Operation of multiple FFFS zones might overcome issues with water droplet drift (activate a zone upstream of the fire for longitudinal ventilation), subject to CFD analysis to demonstrate the efficacy.
- For optimization of the EVS when FFFS is used, the additional airflow resistance introduced by the FFFS spray should be small with respect to other airflow resistance in the tunnel from items such as vehicles, wall friction, buoyancy, fire and external wind. Refer to Figure 4-13 in Section 4.5 for a result showing the pressure profile along the tunnel and the impact of the FFFS. The result shows slightly more additional pressure changes due to the FFFS. The magnitude of the difference suggests that the FFFS resistance should be considered in the EVS design but (for the parameters investigated herein) it is unlikely to be of a magnitude that dominates airflow resistance in the tunnel (this is subject to the FFFS parameters). Note that prediction of pressure profiles in a tunnel with FDS is an area of active research [29] [32] and caution is suggested when using FDS to predict pressure change due to the FFFS. Validated CFD modeling is noted to be a viable tool for predicting this airflow resistance. ARCHIVED

The second hypothesis is that CFD can be used to predict FFFS and EVS interaction for design integration. Integration combinations of FFFS and EVS include:

- Small and large water droplet systems.
- Varying water application rates and FFFS zone configurations.
- Longitudinal ventilation.

- Transverse ventilation.
- Single point exhaust.
- Varying tunnel geometry (area, perimeter, height, grade).

The following points are made about this hypothesis:

- This  hypothesis  has  been  verified  via  computer  modeling  herein.  The  modelling  shows validation results with correlation to test data for a range of scenarios; refer to Chapter 2 for validation of a tunnel fire scenario based on the Memorial Tunnel tests (longitudinal ventilation without FFFS), and Chapter 3 for validation of a full-scale test with FFFS.
- In  Chapters 4 and 5 it is shown via CFD that the FFFS can have an enhancing effect on ventilation performance under longitudinal ventilation. The confinement velocity needed for longitudinal smoke control can be reduced with the use of the FFFS.
- Chapter 7 shows a similar result with transverse ventilation with regard to the extent of smoke spread. When the FFFS is operated and exhaust rate held constant, the distance the smoke spreads along the tunnel is reduced. · In a transverse ventilation system where exhaust is used the smoke tends to rise to the tunnel ceiling and a tenable zone sometimes forms under the hot smoke layer (see Figure 7-11). Operation of the FFFS under this ventilation regime can cause the smoke to be mixed down, causing a reduction in tenability. Results in Section 7.2 confirmed this behavior. Increasing exhaust rate to counter this effect and improve tenability is not suggested since the FFFS helps  the  EVS  operate  more  effectively  (reduction  in  overall  smoke  spread  length),  and increasing the exhaust rate might render the FFFS less effective since it potentially could draw more water up into the exhaust duct and make it harder to deliver water the fire site. Lastly, a typical FFFS zone length is 20 m to 30 m in length (80 to 100 ft.) and this is comparable to the fire perimeter length (applies both sides of the fire) noted in the annex of NFPA 502, where the text states that application of tenability criteria within the fire perimeter is impractical. 8.2 Suggested Practices Based on Research Findings Suggested practices  are  discussed  in detail at  the  conclusion  of  each  chapter.  The  following points are noted: ARCHIVED
- Per Chapter 2 and Chapter 3, grid resolution in the range 0.2 m to 0.4 m gives reasonable results for predicting the tunnel environment under longitudinal ventilation; generally these models showed reasonable agreement between test data and CFD model results. A finer grid than 0.2 m is unlikely to be of much extra benefit to accuracy as results tended to be similar between 0.1 m and 0.2 m. Sensitivity analysis and caution with conclusions are suggested if seeking an accurate prediction of smoke backlayering length as this can be affected by the grid resolution.
- A volumetric heat source approach can be more stable with the version of the FDS software used, and it was shown to give reasonable results. Use of this method is suggested if stability

problems are encountered, however, it is also suggested to consider newer versions of FDS as the stability problems may have been addressed [34].

- A volumetric heat source scenario can be conducted without modeling radiation heat transfer, and the models tend to show reasonable results on a coarse grid. Thus, a volumetric heat source approach is a credible way to run initial models to capture the general performance and integrated behavior of an FFFS-EVS system. Sensitivity to the model set up parameters (grid, fire geometry, blockages), could be conducted and this analysis could also consider, where possible, sensitivity to using a mixing-controlled combustion model.
- The FFFS parameters are important; where possible, the droplet diameter, spray angles, and droplet speed, should be determined by matching a CFD model result to empirical data such as water spray distribution.

· For  longitudinal  ventilation,  equations  for  critical  and  confinement  velocity  as  provided  in NFPA 502 are suggested to give reasonable estimates for the velocity needed for smoke control. For impact of the FFFS, the equation by Ko and Hadjisophocleous [14] is suggested to give a reasonable estimate of the change in longitudinal velocity when operation of an FFFS is  introduced  (compared  to  the  same  scenario  with  no  FFFS).  It  is  noted  that  further investigation is needed before any specific equation can be suggested for use. · The approach  in  this  report  has  focused  on  the  region  near  to  the  fire.  For  purposes  of ventilation design, the regions of tunnel beyond the fire also need consideration factoring in how the FFFS affects critical velocity, temperatures downstream of the fire and pressure loss due to the fire and FFFS (see [1], Section 5.3). 8.3 Suggested Topics for Future Research The  suggested  next  steps  in  the  research  program  include  physical  testing  (task  4)  and development of the final research report (task 5). The testing could help to reconfirm the model validation  conducted  herein,  especially  with  the  FFFS  operational.  The  test  program  is  also suggesting to include detailed measurement of nozzle spray parameters, which is expected to be valuable information as these parameters are not usually published or detailed in test reports. CFD models of the tests would be conducted also, to reconfirm the validation performed herein. Finally, once the testing is complete and the CFD modeling method has been reconfirmed via models of the testing, a research report would be developed to summarize the results and provide suggested practices for the integration of the FFFS and EVS. ARCHIVED

Suggested further research included the following:

- Chapter 2 (CFD modeling): Sensitivity of CFD prediction of smoke backlayering to the grid resolution and treatment of near-wall turbulent flow.
- Chapter 3 (CFD modeling): Improvement of the prediction of the radiative heat flux with the CFD model versus measurements.
- Chapter 4 (CFD modeling for critical and  confinement  velocity): Improvement of  the  CFD method  to  better  understand  the  reasons  for  mixing-controlled  models  giving  numerically

unstable results. Investigation to understand the role of radiation heat transfer in FFFS-EVS interactions.

- Chapter 5 (longitudinal ventilation): Development of an equation for quantitative prediction of FFFS impact on the EVS. Further studies on refined grid resolution models. Experimental investigation of the ability of the FFFS to mitigate spalling in the event of a fire.
- Chapter 6 (transverse ventilation and water spray interaction): Further parameter studies on water drop size, longitudinal ventilation and extent of droplet drift to help develop an equation for the amount of water drift expected.
- Chapter 7 (transverse ventilation): Further parameter studies to understand more how the EVS and FFFS parameters impact the overall ventilation performance. Further studies  to check sensitivity to grid resolution.
- Other possible future investigations include: · Fire dynamics model of fire spread: The HRR for the primary fire would be based on a free burn tunnel test (such as in [38]). A target would be placed downstream of the primary fire and the target would represent a pile of wooden pallets. The primary fire would be unaffected by the FFFS, but fire spread to the target downstream would be impacted. These models would enable verification of the ability of a given FFFS to prevent fire spread, with the influence of ventilation rate included. Reduced water application rates could be modeled relative to the test, with no reduction in FHRR of the primary fire to identify the lowest water application rate needed to prevent fire spread. Previous studies have used a specified FHRR per unit area for the primary fire load [39] but not modeled a target downstream which can ignite if it reaches a given criterion, such as ignition temperature. · Liquid fuels: This is an area of interest for further investigation in the industry [1], especially as it relates to hazardous vehicle fires, and specific analyses are not considered in this current investigation. · Alternative energy vehicles: Impact of the FFFS on fires in these vehicles could be of interest. ARCHIVED

## REFERENCES

- [1] 'Fixed Firefighting and Emergency Ventilation Systems - Literature Survey and Synthesis.' Federal Highway Administration, FWHA-HIF-20-016, 2019. [Online]. Available: https://www.fhwa.dot.gov/bridge/tunnel/pubs/nhi09010/fixed\_firefighting.pdf
- [2] FHWA, 'Fixed Fire Fighting and Emergency Ventilation Systems for Highway Tunnels - Workshop Report.' Federal Highway Administration, FWHA-HIF-20-060, 2020.
- [3] PIARC, Fixed Fire Fighting Systems in Road Tunnels: Current Practices and Recommendations . Permanent International Association of Road Congresses, Technical Committee on Road Tunnel Operation, 3.3, 2016.
- [4] Y. Wu and M. Z. A. Bakar, 'Control of Smoke Flow in Tunnel Fires Using Longitudinal Ventilation Systems - A Study of the Critical Velocity,' Fire Safety Journal , pp. 363-390, 2000.
- [5] Y. Z. Li, B. Lei, and H. Ingason, 'Study of Critical Velocity and Backlayering Length in Longitudinally Ventilated Tunnel Fires,' Fire Safety Journal , vol. 45, pp. 361-370, 2010.
- [6] W. D. Kennedy, 'Critical Velocity Past, Present and Future,' in Independent Technical Conferences - Smoke and Critical Velocity in Tunnels , 1997, pp. 58-67.
- [7] 'NFPA 502 Standard for Road Tunnels, Bridges and Other Limited Access Highways 2017.' NFPA, 2017.
- [8] 'Fire Dynamics Simulator (Version 6) User's Guide.' National Institute of Standards and Technology, 2019. Accessed: Jan. 18, 2019. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1019.pdf
- [9] Bechtel - Parsons Brinckerhoff, 'Memorial Tunnel Fire Ventilation Comprehensive Test Report Volume 1.' Massachusetts Highway Department, 1995.
- [10] Bechtel - Parsons Brinckerhoff, 'Memorial Tunnel Fire Ventilation Test Program Phase IV Report.' Massachusetts Highway Department, 1999.
- [11] M. K. Cheong, W. O. Cheong, K. W. Leong, A. D. Lemaire, and L. M. Noordijk, 'Heat Release Rate of Heavy Goods Vehicle Fire in Tunnels with Fixed Water Based FireFighting System,' Fire Technology , vol. 50, no. 2, pp. 249-266, 2014.
- [12] 'NFPA 502 Standard for Road Tunnels, Bridges and Other Limited Access Highways 2014.' NFPA, 2014.
- [13] 'NFPA 502 Standard for Road Tunnels, Bridges and Other Limited Access Highways 2020 Edition.' NFPA, 2020.
- [14] Y. J. Ko and G. V. Hadjisophocleous, 'Study of Smoke Backlayering During Suppression in Tunnels,' Fire Safety Journal , vol. 58, pp. 240-247, 2013.

ARCHIVED

- [15] Bechtel - Parsons Brinckerhoff, 'Memorial Tunnel Fire Ventilation Comprehensive Test Report Volume 2 - Natural Ventilation and Longitudinal Ventilation with Jet Fans.' Massachusetts Highway Department, 1995.
- [16] S. Haaland, 'Simple and Explicit Formulas for the Friction Factor in Turbulent Flow,' Journal of Fluids Engineering , vol. 103, pp. 89-90, 1983.
- [17] H. Ingason, Y. Z. Li, and A. Lönnermark, 'Runehamar Tunnel Fire Tests,' SP Technical Research Institute of Sweden, SP Report 2011:55, 2011. Accessed: Apr. 03, 2019. [Online]. Available: https://linkinghub.elsevier.com/retrieve/pii/S0379711214001660
- [18] K. B. McGrattan, S. Hostikka, R. McDermott, M. Vanella, and J. Floyd, 'Fire Dynamics Simulator: Technical Reference Guide, Volume 1 - Mathematical Model,' National

- Institute of Standards and Technology, Gaithersburg, MD, NIST SP 1018-1, 2017. doi: 10.6028/NIST.SP.1018.
- [19] 'Fire Dynamics Simulator (Version 6) Technical Reference Guide Volume 3 Validation.' National Institute of Standards and Technology, 2019. Accessed: Jan. 18, 2019. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication1018.pdf
- [20] E. Kim, J. P. Woycheese, and N. A. Dembsey, 'Fire Dynamics Simulator (Version 4.0) Simulation for Tunnel Fire Scenarios with Forced, Transient, Longitudinal Ventilation Flows,' Fire Technology , vol. 44, no. 2, pp. 137-166, 2008, doi: 10.1007/s10694-0070028-2.
- [21] J. Holman, Heat Transfer , 7th ed. 1990.
- [22] K. McGrattan and R. McDermott, 'Response to 'Unexpected Oscillations in Fire Modelling Inside a Long Tunnel' by Ang et al.,' p. 5.
- [23] D. T. Sheppard, 'Spray Characteristics of Fire Sprinklers,' PhD Thesis, Northwestern University, 2002.
- [24] 'Sprinkler Spray Patterns.' Tyco, 2018.
- [25] E. Blanchard, P. Boulet, and P. Carlotti, 'Capability of a CFD Tool for Assessing a Water Mist System in a Tunnel,' in 15th International Symposium of Aerodynamics Ventilation and Fire in Tunnels , 2013, pp. 717-727.
- [26] 'NFPA 502 2020 Edition, Standard for Road Tunnels, Bridges and Other Limited Access Highways, Tentative Interim Amendment 1561.' Jun. 30, 2021.
- [27] Parsons Brinckerhoff Quade and Douglas, Subway Environmental Design Handbook , vol. 2. US Department of Transportation, Federal Transit Administration, Research and Special Programs Administration, 2002.
- [28] P. Carlotti and P. Salizzoni, 'Pressure Drop Caused by a Fire in a Tunnel,' in 17th International Symposium of Aerodynamics Ventilation and Fire in Tunnels , 2017, pp. 363-371.
- [29] I. Riess, D. Weber, M. Steck, and R. Ingenieur-GmbH, 'On the Air-Flow Resistance of Tunnel Fires in Longitudinal Ventilation - The Throttling Effect,' p. 10, 2020.
- [30] Y. Z. Li and H. Ingason, 'Model Scale Tunnel Fire Tests - Automatic Sprinkler,' SP Report 2011:31, 2011.
- [31] S. R. Lee and H. S. Ryou, 'An Experimental Study of the Effect of the Aspect Ratio on the Critical Velocity in Longitudinal Ventilation Tunnel Fires,' Journal of Fire Sciences , vol. 23, pp. 119-138, 2005.
- [32] I. Riess, 'Fixed Fire Fighting Systems and Tunnel Ventilation.'
- [33] C. Stacey and M. Beyer, 'Critical of Critical Velocity - An Industry Practitioner's Perspective,' Tunnel Safety and Ventilation Conference , p. 16, 2020.

ARCHIVED

- [34] C. D. Ang, G. Rein, and J. Peiro, 'Unexpected Oscillations in Fire Modelling Inside a Long Tunnel,' Fire Technol , vol. 56, no. 5, pp. 1937-1941, Sep. 2020, doi: 10.1007/s10694-020-01004-x.
- [35] R. Bellas, M. A. Gómez, A. González-Gil, J. Porteiro, and J. L. Míguez, 'Assessment of the Fire Dynamics Simulator for Modeling Fire Suppression in Engine Rooms of Ships with Low-Pressure Water Mist,' Fire Technol , vol. 56, no. 3, pp. 1315-1352, May 2020, doi: 10.1007/s10694-019-00931-8.
- [36] N. Agnew and B. Allen, 'Full Scale Car Burns in the Sydney Harbour Tunnel,' 2008.
- [37] FHWA, 'Tunnel Fire Protection Using Fixed Firefighting Systems - Advanced Practices in Australia and New Zealand,' Federal Highway Administration, 2018.

- [38] H. Ingason, 'Large Scale Fire Tests with Fixed Fire Fighting System in Runehamar Tunnel,' SP Technical Research Institute of Sweden, SP Report 2014:32, 2014.
- [39] J. Trelles and J. R. Mawhinney, 'CFD Investigation of Large Scale Pallet Stack Fires in Tunnels Protected by Water Mist Systems,' Journal of Fire Protection Engineering , vol. 20, no. 3, pp. 149-198, Aug. 2010, doi: 10.1177/1042391510367359.

<!-- image -->

Stamp

## APPENDIX A:    TABLE OF CFD RUNS REPORTED

|   CHAPTER | ID        | CASE                                                         | FHRR (MW)   |   VELOCITY (m/s) | DESCRIPTION                                                                         |
|-----------|-----------|--------------------------------------------------------------|-------------|------------------|-------------------------------------------------------------------------------------|
|         2 | EVS-02-37 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.10 m, no obstructions, 0.2 m grid                                |
|         2 | EVS-02-38 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.45 m, no obstructions, 0.2 m grid                                |
|         2 | EVS-02-39 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, no obstructions, 0.2 m grid                                |
|         2 | EVS-02-75 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, no obstructions, 0.4 m grid                                |
|         2 | EVS-02-74 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, no obstructions, 0.1 m grid                                |
|         2 | EVS-02-76 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.10 m, obstructions, 0.2 m grid                                   |
|         2 | EVS-02-77 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.45 m, obstructions, 0.2 m grid                                   |
|         2 | EVS-02-78 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, obstructions, 0.2 m grid                                   |
|         2 | EVS-02-79 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, obstructions, 0.4 m grid                                   |
|         2 | EVS-02-80 | Memorial Tunnel, cold flow model                             | N/A         |              2.5 | Roughness height 0.90 m, obstructions, 0.1 m grid                                   |
|         2 | EVS-02-27 | Memorial Tunnel, test 606A, longitudinal vent, 10 MW         | 9.9         |              1.8 | Base case model, 0.2 m grid, mixing-controlled fire model                           |
|         2 | EVS-02-43 | Memorial Tunnel, test 606A, longitudinal vent, 10 MW         | 9.9         |              1.8 | Roughness height 0.90 m, insulating material near fire                              |
|         2 | EVS-02-51 | Memorial Tunnel, test 612, longitudinal vent, 50 MW ARCHIVED | 47.2        |              2.5 | Base case model, roughness height 0.90 m, 0.2 m grid, mixing- controlled fire model |
|         2 | EVS-02-48 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        |              2.5 | Adiabatic boundary near fire zone                                                   |
|         2 | EVS-02-53 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        |              2.5 | Dynamic Smagorinsky model for turbulence                                            |
|         2 | EVS-02-54 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        |              2.5 | Changed turbulence closure coefficient from 0.1 to 0.2                              |
|         2 | EVS-02-47 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        |              2.5 | Compared with test 611 data                                                         |
|         2 | EVS-02-63 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 42.2        |              2.5 | Fire heat release rate reduction                                                    |

|   CHAPTER | ID        | CASE                                                         | FHRR (MW)   | VELOCITY (m/s)   | DESCRIPTION                                                                |
|-----------|-----------|--------------------------------------------------------------|-------------|------------------|----------------------------------------------------------------------------|
|           | EVS-02-50 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | Smooth wall model                                                          |
|           | EVS-02-62 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | No obstructions                                                            |
|           | EVS-02-64 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | As per EVS-02-51, coarse grid, 0.4 m instead of 0.2 m                      |
|           | EVS-02-71 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | As per EVS-02-51, grid refined to 0.1 m                                    |
|           | EVS-02-66 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | Volumetric heat source, no radiation, 0.4 m grid                           |
|           | EVS-02-67 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | Volumetric heat source, with radiation                                     |
|           | EVS-02-68 | Memorial Tunnel, test 612, longitudinal vent, 50 MW ARCHIVED | 47.2        | 2.5              | Volumetric heat source, no radiation, dynamic Smagorinsky turbulence model |
|           | EVS-02-69 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | Volumetric heat source, no radiation, 0.2 m grid                           |
|           | EVS-02-73 | Memorial Tunnel, test 612, longitudinal vent, 50 MW          | 47.2        | 2.5              | As per EVS-02-69, grid refined to 0.1 m                                    |
|         3 | EVS-10-16 | Calibration for nozzle at 40 LPM                             | N/A         | N/A              | N/A                                                                        |
|           | EVS-10-17 | Calibration for nozzle at 58 LPM                             | N/A         | N/A              | N/A                                                                        |
|           | EVS-10-18 | Calibration for nozzle at 82 LPM                             | N/A         | N/A              | N/A                                                                        |
|           | EVS-10-19 | Calibration for nozzle at 82 LPM based on trial A1           | N/A         | N/A              | N/A                                                                        |
|           | EVS-10-20 | Calibration for nozzle at 82 LPM, larger droplets (1 mm)     | N/A         | N/A              | N/A                                                                        |
|           | EVS-10-24 | Calibration for nozzle at 82 LPM, smaller droplets (0.55 mm) | N/A         | N/A              | N/A                                                                        |
|           | EVS-09-31 | LTA tests, base case, mixing-controlled model for fire       | Varies      | 3                | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-34 | LTA tests, shifted FHRR                                      | Varies      | 3                | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-35 | LTA tests, shifted FHRR, larger drops                        | Varies      | 3                | FHRR varies per Test 4 in reference                                        |

January 2022

|   CHAPTER | ID        | CASE                                                                                            | FHRR (MW)   |   VELOCITY (m/s) | DESCRIPTION                                                                |
|-----------|-----------|-------------------------------------------------------------------------------------------------|-------------|------------------|----------------------------------------------------------------------------|
|           | EVS-09-36 | LTA tests, shifted FHRR, smaller drops                                                          | Varies      |                3 | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-44 | LTA tests, 0.4 m grid                                                                           | Varies      |                3 | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-39 | LTA tests, shifted FHRR, volumetric heat source, volumetric heat source, 0.4 m grid             | Varies      |                3 | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-40 | LTA tests, shifted FHRR, volumetric heat source, finer grid 0.2 m                               | Varies      |                3 | FHRR varies per Test 4 in reference                                        |
|           | EVS-09-41 | LTA tests, shifted FHRR, volumetric heat source, radiation applied                              | Varies      |                3 | FHRR varies per Test 4 in reference                                        |
|         4 | EVS-19-1  | Small openings included, 0.4 m grid, mixing-controlled fire model                               | 46.7        |             2.73 | Ramp down velocity (based on ceiling temperature 25 deg C at 2 m upstream) |
|           | EVS-19-10 | Small openings included, 0.4 m grid, mixing-controlled fire model                               | 46.7        |              2.5 | Constant upstream velocity                                                 |
|           | EVS-19-24 | Close the small openings, 0.4 m grid, mixing-controlled fire model ARCHIVED                     | 46.7        |              2.5 | Constant upstream velocity                                                 |
|           | EVS-19-3  | Close the small openings, 0.2 m grid, mixing-controlled fire model                              | 46.7        |              2.5 | Constant upstream velocity                                                 |
|           | EVS-19-19 | WALE at walls, 0.4 m grid, mixing-controlled fire model                                         | 46.7        |              2.5 | Constant upstream velocity                                                 |
|           | EVS-19-20 | WALE at walls, refined grid at 0.2 m nominal and 0.1 m near walls, mixing-controlled fire model | 46.7        |              2.5 | Constant upstream velocity                                                 |
|           | EVS-19-11 | Small openings included, 0.4 m grid, mixing-controlled fire model                               | 46.7        |             2.25 | Constant upstream velocity                                                 |
|           | EVS-19-18 | Close the small openings, 0.2 m grid, mixing-controlled fire model                              | 46.7        |             2.25 | Constant upstream velocity                                                 |
|           | EVS-19-21 | Closed openings, 0.4 m grid, volumetric heat source fire                                        | 46.7        |              2.5 | Constant upstream velocity                                                 |

| CHAPTER   | ID        | CASE                                                                                                              |   FHRR (MW) |   VELOCITY (m/s) | DESCRIPTION                |
|-----------|-----------|-------------------------------------------------------------------------------------------------------------------|-------------|------------------|----------------------------|
|           | EVS-19-22 | Closed openings, 0.2 m grid, volumetric heat source fire                                                          |        46.7 |              2.5 | Constant upstream velocity |
|           | EVS-19-23 | Closed openings, 0.4 m grid, added a passive scalar (soot) via particles, volumetric heat source fire             |        46.7 |              2.5 | Constant upstream velocity |
|           | EVS-19-32 | closed openings + passive scalar (soot) + radiation, volumetric heat source fire                                  |        46.7 |              2.5 | Constant upstream velocity |
|           | EVS-19-13 | Grid 0.4 m, volumetric heat source fire                                                                           |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-15 | Change closure coefficient Cs=0.2, grid 0.4 m, volumetric heat source fire                                        |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-17 | Closed openings, 0.4 m grid, volumetric heat source fire                                                          |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-12 | Reynolds averaged Navier-Stokes turbulent model case (using ANSYS Fluent), nominal grid resolution 0.3 m ARCHIVED |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-9  | Similar to EVS-19-12 but with a reduced upstream velocity                                                         |        46.7 |             2.15 | Constant upstream velocity |
|           | EVS-19-16 | Closed openings, 0.2 m grid, volumetric heat source fire                                                          |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-36 | Closed openings, 0.2 m grid, adiabatic walls, volumetric heat source fire                                         |        46.7 |             2.25 | Constant upstream velocity |
|           | EVS-19-37 | Closed openings, 0.4 m grid, 2.0 m/s, volumetric heat source fire                                                 |        46.7 |                2 | Constant upstream velocity |
|           | EVS-19-33 | Scaled version of EVS- 19-32, by a factor of 4, volumetric heat source fire                                       |        1.46 |             1.25 | Constant upstream velocity |
|           | EVS-19-25 | No FFFS, 0.4 m grid, no openings, volumetric heat source fire                                                     |        18.7 |              2.3 | Constant upstream velocity |
|           | EVS-19-26 | FFFS starts part way through, 5 mm/min, volumetric heat source fire                                               |        18.7 |                1 | Constant upstream velocity |

|   CHAPTER | ID        | CASE                                                                                                                                                         |   FHRR (MW) |   VELOCITY (m/s) | DESCRIPTION                                                                                          |
|-----------|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|------------------|------------------------------------------------------------------------------------------------------|
|           | EVS-19-34 | FFFS starts part way through, 5 mm/min all cases), included radiation, volumetric heat source fire                                                           |        18.7 |                1 | Constant upstream velocity                                                                           |
|           | EVS-19-27 | FFFS starts part way through, 5 mm/min, volumetric heat source fire                                                                                          |        18.7 |             1.43 | Ramp down velocity to find confinement velocity, sensor at 12 m (T=25 C)                             |
|           | EVS-19-28 | No FFFS, sensor at 12 m, volumetric heat source fire                                                                                                         |        18.7 |              1.8 | Ramp down velocity to find confinement velocity, sensor at 12 m (T=25 C)                             |
|           | EVS-19-29 | No FFFS, sensor at 4 m, volumetric heat source fire                                                                                                          |        18.7 |             2.23 | Ramp down velocity to find confinement velocity, sensor at 4 m (T=25 C)                              |
|           | EVS-19-30 | FFFS starts part way through, 5 mm/min all cases), sensor at 4 m, volumetric heat source fire                                                                |        18.7 |             1.77 | Ramp down velocity to find confinement velocity, sensor at 4 m (T=25 C)                              |
|           | EVS-19-35 | FFFS starts part way through, 5 mm/min, sensor at 4 m, included radiation, volumetric heat source fire                                                       |        18.7 |             1.84 | Ramp down velocity to find confinement velocity, sensor at 4 m (T=25 C)                              |
|           | EVS-19-38 | FFFS starts part way through, 5 mm/min, 0.4 m grid, no openings, volumetric heat source fire                                                                 |        18.7 |              2.3 | Constant upstream velocity                                                                           |
|         5 | EVS-21-1  | No sprinklers, all Chapter 5 models used a volumetric heat source fire unless otherwise noted, cross section 7.4 m wide and 5.2 m high unless noted ARCHIVED |           5 |             1.29 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|         5 | EVS-21-2  | 0.65 mm, 2.5 mm/min (droplet size, water application rate)                                                                                                   |           5 |             1.03 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|         5 | EVS-21-3  | 0.65 mm, 5 mm/min                                                                                                                                            |           5 |             0.77 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|         5 | EVS-21-4  | 0.155 mm, 5 mm/min                                                                                                                                           |           5 |             0.72 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |

| CHAPTER   | ID        | CASE                   |   FHRR (MW) |   VELOCITY (m/s) | DESCRIPTION                                                                                          |
|-----------|-----------|------------------------|-------------|------------------|------------------------------------------------------------------------------------------------------|
|           | EVS-21-5  | 0.65 mm, 10 mm/min     |           5 |             0.60 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-19 | No sprinklers          |           5 |             1.39 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 1 H (T=25 C) |
|           | EVS-21-21 | 0.65 mm, 2.5 mm/min    |           5 |             1.29 | Constant upstream velocity                                                                           |
|           | EVS-21-30 | No sprinklers          |           5 |             1.60 | Constant upstream velocity                                                                           |
|           | EVS-21-6  | No sprinklers          |          20 |             1.72 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-7  | 0.65 mm, 2.5 mm/min    |          20 |             1.56 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-8  | 0.65 mm, 5 mm/min      |          20 |             1.42 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-9  | 0.155 mm, 10 mm/min    |          20 |             1.01 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-20 | No sprinklers ARCHIVED |          20 |             1.87 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 1 H (T=25 C) |
|           | EVS-21-22 | 0.65 mm, 2.5 mm/min    |          20 |             1.72 | Constant upstream velocity                                                                           |
|           | EVS-21-31 | No sprinklers          |          20 |                2 | Constant upstream velocity                                                                           |
|           | EVS-21-11 | No sprinklers          |         100 |             1.76 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-12 | 0.65 mm, 2.5 mm/min    |         100 |             1.57 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-13 | 0.155 mm, 2.5 mm/min   |         100 |             1.31 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |

| CHAPTER   | ID                             | CASE                                                                    |   FHRR (MW) |   VELOCITY (m/s) | DESCRIPTION                                                                                          |
|-----------|--------------------------------|-------------------------------------------------------------------------|-------------|------------------|------------------------------------------------------------------------------------------------------|
|           | EVS-21-14                      | 0.65 mm, 5 mm/min                                                       |         100 |             1.46 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-15                      | 0.155 mm, 5 mm/min                                                      |         100 |             1.17 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-16                      | 0.65 mm, 10 mm/min                                                      |         100 |              1.2 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-17                      | 0.155 mm, 10 mm/min                                                     |         100 |                1 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-18                      | 1.2 mm, 10 mm/min                                                       |         100 |              1.5 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 2 H (T=25 C) |
|           | EVS-21-23                      | 0.65 mm, 2.5 mm/min                                                     |         100 |             1.76 | Constant upstream velocity                                                                           |
|           | EVS-21-32                      | No FFFS                                                                 |         100 |             2.25 | Constant upstream velocity                                                                           |
|           | EVS-13-1                       | No FFFS, extra wide cross section (30 m) by 5.2 m high ARCHIVED         |          20 |             2.14 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 4 m (T=25 C) |
|           | EVS-13-2                       | FFFS (0.65 mm, 5 mm/min), extra wide cross section (30 m) by 5.2 m high |          20 |             1.84 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 4 m (T=25 C) |
|           | EVS-14-1 No FFFS, Tunnel cross | Memorial section                                                        |          20 |             2.65 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 4 m (T=25 C) |
|           | EVS-14-2                       | FFFS (0.65 mm, 5 mm/min), Memorial Tunnel cross section                 |          20 |             1.99 | Ramp down velocity to find confinement velocity, sensor upstream at ceiling at distance 4 m (T=25 C) |
|           | EVS-12-6                       | No FFFS, mixing- controlled fire model                                  |          20 |              2.5 | Constant upstream velocity                                                                           |
|           | EVS-12-7                       | FFFS, 0.65 mm, 2.5 mm/min, mixing- controlled fire model                |          20 |              2.5 | Constant upstream velocity                                                                           |
|           | EVS-12-8                       | FFFS, 0.65 mm, 5 mm/min, mixing- controlled fire model                  |          20 |              2.5 | Constant upstream velocity                                                                           |
|           | EVS-12-11                      | No FFFS, mixing- controlled fire model                                  |         100 |              2.9 | Constant upstream velocity                                                                           |

January 2022

|   CHAPTER | ID                                                                                                  | CASE                                                                                                | FHRR (MW)   |   VELOCITY (m/s) | DESCRIPTION                                                         |
|-----------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|-------------|------------------|---------------------------------------------------------------------|
|           | EVS-12-13                                                                                           | FFFS, 0.155 mm, 2.5 mm/min, mixing- controlled fire model                                           | 100         |              2.7 | Constant upstream velocity                                          |
|           | EVS-12-14                                                                                           | FFFS, 0.155 mm, 5 mm/min, mixing- controlled fire model                                             | 100         |              2.8 | Constant upstream velocity                                          |
|           | EVS-12-15                                                                                           | FFFS, 0.65 mm, 5 mm/min, mixing- controlled fire model                                              | 100         |              2.7 | Constant upstream velocity                                          |
|         6 | EVS-11-16                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | No duct, trial A, 82 L/min/noz, 5 mm/min (approximately)            |
|         6 | EVS-11-17                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | No duct, mist 1, 39.6 L/min/noz, 2.5 mm/min (approximately)         |
|         6 | EVS-11-22                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | No duct, trial B, 82 L/min/noz, 5 mm/min (approximately)            |
|         6 | EVS-11-40                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | Duct modeled above, trial B, 82 L/min/noz, 5 mm/min (approximately) |
|         6 | EVS-11-18                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | No duct, trial A, 41 L/min/noz, 2.5 mm/min (approximately)          |
|         6 | EVS-11-19                                                                                           | Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port.                    | -           |              2.5 | No duct, trial B, 164 L/min/noz, 10 mm/min (approximately)          |
|         6 | EVS-11-20 Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port. ARCHIVED | EVS-11-20 Exhaust openings 1.0 x 0.2 m (width x length). Exhaust rate 0.8 m 3 /s per port. ARCHIVED | -           |                0 | No duct, trial A, 82 L/min/noz, 5 mm/min (approximately)            |
|         6 | EVS-11-31                                                                                           | Exhaust openings 2.0 x 0.2 m (width x length). Exhaust rate 40 m 3 /s per port.                     | -           |                0 | No duct, trial A, 82 L/min/noz, 5 mm/min (approximately)            |
|         6 | EVS-11-35                                                                                           | Exhaust openings 2.0 x 0.2 m (width x length). Exhaust rate 40 m 3 /s per port.                     | -           |                0 | Duct modeled above, trial A, 82 L/min/noz, 5 mm/min (approximately) |
|         6 | EVS-11-23                                                                                           | Exhaust openings 2.0 x 0.2 m (width x length). Exhaust rate 40 m 3 /s per port.                     | -           |              2.5 | No duct, trial A, 82 L/min/noz, 5 mm/min (approximately)            |

January 2022

|   CHAPTER | ID        | CASE                                                                            | FHRR (MW)   | VELOCITY (m/s)   | DESCRIPTION                                                                                          |
|-----------|-----------|---------------------------------------------------------------------------------|-------------|------------------|------------------------------------------------------------------------------------------------------|
|           | EVS-11-21 | Exhaust openings 2.0 x 4.0 m (width x length). Exhaust rate 40 m 3 /s per port. | -           | 2.5              | No duct, trial A, 82 L/min/noz, 5 mm/min (approximately)                                             |
|         7 | EVS-15-4  | No FFFS                                                                         | 5           | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-5  | No FFFS                                                                         | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-6  | No FFFS                                                                         | 100         | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-7  | 0.65 mm, 5 mm/min (droplet size, water application rate)                        | 5           | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-8  | 0.65 mm, 5 mm/min                                                               | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-9  | 0.155 mm, 5 mm/min                                                              | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-10 | 0.65 mm, 2.5 mm/min                                                             | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-11 | 0.65 mm, 10 mm/min                                                              | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-12 | 0.155 mm, 2.5 mm/min                                                            | 20          | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-13 | 0.65 mm, 5 mm/min                                                               | 20          | N/A              | 70 cfm/lane foot exhaust rate, evenly distributed                                                    |
|         7 | EVS-15-14 | 0.65 mm, 5 mm/min                                                               | 100         | N/A              | 100 cfm/lane foot exhaust rate, evenly distributed                                                   |
|         7 | EVS-15-15 | No FFFS                                                                         | 100         | N/A              | 70 cfm/lane foot exhaust rate, evenly distributed                                                    |
|         7 | EVS-16-1  | No FFFS ARCHIVED                                                                | 20          | N/A              | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s. |
|         7 | EVS-16-2  | 0.65 mm, 5 mm/min (droplet size, water application rate)                        | 20          | N/A              | As per EVS-16-1                                                                                      |
|         7 | EVS-16-19 | No FFFS                                                                         | 20          | N/A              | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s. |
|         7 | EVS-16-20 | 0.65 mm, 5 mm/min                                                               | 20          | N/A              | As per EVS-16-19                                                                                     |
|         7 | EVS-16-3  | No FFFS                                                                         | 20          | N/A              | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.   |
|         7 | EVS-16-4  | 0.65 mm, 5 mm/min                                                               | 20          | N/A              | As per EVS-16-3                                                                                      |

January 2022

| CHAPTER   | ID        | CASE                 |   FHRR (MW) | VELOCITY (m/s)   | DESCRIPTION                                                                                                           |
|-----------|-----------|----------------------|-------------|------------------|-----------------------------------------------------------------------------------------------------------------------|
|           | EVS-16-21 | No FFFS              |          20 | N/A              | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.                    |
|           | EVS-16-22 | 0.65 mm, 5 mm/min    |          20 | N/A              | As per EVS-16-21                                                                                                      |
|           | EVS-16-5  | No FFFS              |         100 | N/A              | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.                  |
|           | EVS-16-6  | 0.65 mm, 5 mm/min    |         100 | N/A              | As per EVS-16-5                                                                                                       |
|           | EVS-16-7  | No FFFS              |         100 | N/A              | Extract points downstream (C, E) sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.                    |
|           | EVS-16-8  | 0.65 mm, 5 mm/min    |         100 | N/A              | As per EVS-16-7                                                                                                       |
|           | EVS-16-9  | 1.2 mm, 10 mm/min    |         100 | N/A              | Extract points downstream (C, E) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 3 m/s.                  |
|           | EVS-16-10 | 0.155 mm, 2.5 mm/min |         100 | N/A              | As per EVS-16-9                                                                                                       |
|           | EVS-16-11 | No FFFS              |          20 | N/A              | Extract points each side of fire (A, C) at ceiling. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s.           |
|           | EVS-16-12 | 0.65 mm, 5 mm/min    |          20 | N/A              | As per EVS-16-11                                                                                                      |
|           | EVS-16-13 | No FFFS              |          20 | N/A              | Extract points each side of fire (A, C) at sidewall. Total exhaust rate 150 m 3 /s. Upstream velocity 2 m/s. ARCHIVED |
|           | EVS-16-14 | 0.65 mm, 5 mm/min    |          20 | N/A              | As per EVS-16-13                                                                                                      |
|           | EVS-16-15 | No FFFS              |          20 | N/A              | Extract points each side of fire (A, C) at ceiling. Total exhaust rate 100 m 3 /s. Upstream velocity 1.3 m/s.         |
|           | EVS-16-16 | 0.65 mm, 5 mm/min    |          20 | N/A              | As per EVS-16-15                                                                                                      |
|           | EVS-16-17 | No FFFS              |          20 | N/A              | All extract points operating (A, B, C, D, E). Total exhaust rate 100 m 3 /s. Upstream velocity 1.0 m/s.               |
|           | EVS-16-18 | 0.65 mm, 5 mm/min    |          20 | N/A              | As per EVS-16-17                                                                                                      |