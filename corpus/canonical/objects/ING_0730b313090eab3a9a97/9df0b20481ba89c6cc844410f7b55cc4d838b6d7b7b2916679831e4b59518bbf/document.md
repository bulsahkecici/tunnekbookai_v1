## Abstract

The Clyde Tunnel in Glasgow, Scotland, is currently undergoing refurbishment. This refurbishment includes the installation of a new tunnel lining / fire protection system in both tunnel tubes. This lining system has already been shown to protect the tunnel structure from high temperatures However, there is a gap at the lower edge of the lining to allow any water accumulated behind the lining to run into a drainage channel within the main tunnel void. There were concerns that this small gap might lead to the exposure of the structural members to very high temperatures in the event of a fire in the tunnel.

A  heat  transfer  analysis  was  carried  out.  This  analysis  consisted  of  the  evaluation  of  the thermal  field  inside  the  tunnel  using  Computational  Fluid  Dynamics  (CFD)  computations.  This identified the locations in the tunnel which were most likely to be at risk, and predicted the conditions at  those  locations  in  the  event  of  a  'worst  case'  fire  scenario.  On  the  basis  of  this  information  a bounding  heat  transfer  analysis  was  carried  out  that  allowed  the  establishment  of  the  temperature evolution of the structural elements. CFD tools were not used for the heat transfer analysis because the complexity of the geometry made the uncertainty too large to justify a detailed CFD study. Instead, this  bounding  analysis  allowed  the  establishment  of  the  maximum  possible  temperatures  of  the structural elements.

It  was  found  that,  even  in  a  'worst  case'  scenario  fire,  the  temperature  of  the  structural elements would not exceed critical levels for several hours of maximum fire exposure. The design of the lining / channel is held to be more than satisfactory in this case.

## Introduction

(a) The Clyde Tunnel

<!-- image -->

Photograph

Figure 1 - Photographs of the tunnel during construction and the original tunnel lining.

<!-- image -->

Photograph

The  construction  of  the  second † road  tunnel  under  the  river  Clyde  was  started  in  1957  and  the northbound  tube  was  opened  by  Queen  Elizabeth  II  in  1963.  The  southbound  tube  opened  the following  year.  The  tunnels  are  762m  long,  are  constructed  out  of  iron  sections  and,  when  they

† The first tunnel under the Clyde, the 'Harbour Tunnel', was built in the 1890s. It was accessed by hydraulic lifts in the two 'rotundas' (which can still be seen on the banks of the Clyde). The tunnel was closed to vehicles in 1943 and the lifts were removed. It was closed to pedestrians in 1986 and filled-in in 1987.

<!-- image -->

Logo

Proc. Int. Conf. Risk and Fire Engineering for Tunnels, Stations and Linked Underground Spaces. 19-20 April 2006, Hong Kong. Organised by Tunnel Management International. pp. 31-39. ISBN: 1 901808 25 4

## CLYDE TUNNEL REFURBISHMENT: MODELLING THE PERFORMANCE OF THE NEW LINING SYSTEM AND DRAINAGE CHANNEL IN THE EVENT OF A FIRE.

R.O. Carvel &amp; J.L. Torero

BRE Centre for Fire Safety Engineering, University of Edinburgh, UK.

opened, were the steepest road tunnels in the world with a 6% slope (1:16). In 1957, the expected traffic density was 9,000 vehicles per day; in 1965 22,000 vehicles used the tunnel on a daily basis; today  the  daily  traffic  flow  is  over  65,000  vehicles.  The  original  ventilation  system  was  fully transverse, with air supplied through vents along the kerbside and periodic extraction vents along the ceiling, see Figure 1.

## (b) The refurbishment

Figure 2 - Photographs of the tunnel during refurbishment and the application of the fire protection.

<!-- image -->

Photograph

The £9M refurbishment  of  the  Clyde  Tunnel  includes  the  installation  of  a  new  tunnel  lining  /  fire protection system in both tunnel tubes, an overhaul of the ventilation system and the installation of a state of the art video monitoring system.

The primary requirement of the new lining system is that it should protect the iron sections of the tunnel structure in the event of a fire. The lining system consists of a steel framework attached to the iron sections, this is covered by steel sheeting and a wire mesh, to which a 40mm layer of cementitious fire protection is applied, by spraying in-situ, see Figure 2. This lining system has been furnace tested in the laboratory and has been shown to adequately protect the structural members from temperatures up  to  1350°C  for  over  two  hours,  according  to  the  standard  time-temperature  curve  proposed  by Rijkwaterstaat, the Netherlands (hereafter referred to as the RWS curve) [1].

## (c) The problem

Figure 3 - Simplified representation of the tunnel cross-section showing the lining system and the drainage channel.

<!-- image -->

Engineering drawing

One of the secondary functions of the lining system is to act as a drip shield, such that all leakage into the tunnel runs down the outer side of the lining system and drains into a channel in the main tunnel void ‡ .  In order to allow the water to pass from the cavity into the tunnel void, there has to be a gap between the lower edge of the lining system and the concrete which forms the drainage channel and protects the lower parts of the tunnel structure, see Figure 3. There was some concern that this gap might allow the structural members of the tunnel to be exposed to high temperatures in the event of a fire in the tunnel.

The University of Edinburgh were contracted to analyse the problem and report on the safety of this design. The analysis of the problem was carried out in two stages:

- Various scenarios involving a fire in the tunnel were simulated using a computer fire model, to determine the conditions in the vicinity of the gap in the event of a fire, and
- The  heat  transfer  to  the  tunnel  structure  was  calculated,  based  on  the  'worst  case'  values obtained from the computer simulations.

## Methodology

Due to the design of the gap and the drainage channel, there is no direct line-of-sight path for heat transfer from the void into the cavity by radiation, so it is assumed that any heat transfer into the cavity will be due to a pressure driven flow of hot gas. Thus the objective of the computer simulations was to identify those parts of the tunnel, near the gap, which exhibited the highest pressures. The rate of gas flow  into  the  cavity  could  then  be  estimated  if  the  pressure  in  the  cavity  is  assumed  to  remain  at ambient; this is deemed to be an extreme 'worst case' assumption as, in reality, the pressure would most  likely  be  above  ambient  initially  and  would  increase  to  be  equal  to  the  void  pressure  (thus eliminating the flow) within a matter of moments.

It was also assumed that the gas flow into the cavity would only transfer heat to the iron sections of the tunnel and not to the back of the lining material; this is another 'worst case' assumption. In reality there would be heat losses to the rear of the lining material and thus there would be less heat transfer to the structural elements.

## Computer simulations

The conditions in the tunnel in the event of a fire were modelled using the 'Fire Dynamics Simulator' (FDS)  model  (version  4).  FDS  is  a  computational  fluid  dynamics  (CFD)  model,  developed  by  the National Institute of Standards and Technology (NIST) in the USA [2]. This code is of generalized use in  the  Fire  safety  Engineering  community  and  relevant  validation  exercises  can  be  found  in  the literature supplied by the developers.

As the requirements of the lining system are those of the RWS fire, the aim of the modelling was to simulate fires in the tunnel which would generate peak gas temperatures of about 1350°C and then predict the peak temperatures and pressures in the vicinity of the gap. The growth and decay phases of the fires were not of direct relevance to the study, so the simulations carried out considered high heat release rate (HRR) fires with a constant output, so that the simulations would approximate to 'steadystate'  conditions. This scenario is actually  more severe than the RWS fire as the standard fire only remains at a peak temperature for a limited time.

All computer models have limitations and in the case of FDS they pertain mostly to the combustion model and radiation heat transfer associated to fire growth. As this study did not require the prediction of the fire burning behaviour (the fires were prescribed) or radiation, most of the limitations of FDS could be ignored.

‡ Throughout this paper the word 'cavity' will be used to describe the space between the lining system and the tunnel structure, whereas the word 'void' will be used to describe the main vehicle space in the tunnel.

However, the requirement that the simulated environment be constructed out of rectilinear cells cannot be overlooked. The upper parts of the Clyde Tunnel cross-section have a semi-circular aspect which must be represented by rectangular blocks in the simulated tunnel. This is not a particularly significant problem in this instance as the steps do not have a severe influence in the global nature of the flow. Temperatures, pressures and flow velocities depend mostly on the global behaviour of the flow, thus the 'step-like' geometry will provide very similar results to a smoothly curved wall. Also, the parts of the tunnel which are of interest are reasonably 'step-like' in themselves.

The cross-sectional profile of the simulated environment is shown in Figure 4. The geometry of the tunnel has been simplified to being constructed out of 1m 3 cubes, thus the kerb, elevated walkway and drainage channel have all been represented by a 1m high by 1m wide block at the side of the roadway. At eight locations through the tunnel, the fire safety installations have been included, modelled as a 1m high, 1m wide (as viewed in cross-section) and 2m deep box. The gas temperature and pressure have been recorded at various locations in the tunnel at the apex of the ceiling, beside the gap and just above each of the fire safety boxes.

Figure 4 - Typical cross-sectional profile of the simulated tunnel (with safety box)

<!-- image -->

Engineering drawing

The longitudinal profile of the simulated tunnel was based on the plans of the east tube, which has a slope of approximately 1:17 on the northern side and a slope of approximately 1:16 on the southern side. The simulated tunnel was therefore constructed out of long, 1m high steps, each 17m long on the north side and 16m long on the south side. The lowest section of the tunnel (between the first step on each side) was 33m long. There were twenty steps on each side. The longitudinal profile of the model tunnel is shown in Figure 5. The computational domain extended above and beyond the ends of the tunnel to allow modelling of the plume away from the portals.

Figure 5 - The longitudinal profile of the model tunnel (not to scale)

<!-- image -->

Engineering drawing

## Modelling results

If there was a large fuel spillage in the tunnel, for example a fuel tanker shed its load, the fuel would flow to the lowest point of the tunnel and form a pool. If this was to catch fire, a serious incident would develop. The first simulations carried out involved large fuel pools at the lowest point in the tunnel.  The  initial  run  was  carried  out  prescribing  a  fuel  vaporisation  rate  equivalent  to  a  HRR  of 220MW and assuming natural ventilation conditions. In this instance the HRR calculated by the model was substantially lower than the prescribed value as there was insufficient oxygen to allow burning at this  level.  As  a  consequence  of  this,  the  peak  temperatures  in  the  tunnel  were  only  of  the  order  of

600°C  and  nowhere  near  the  required  level.  Several  subsequent  runs  were  attempted,  varying  the prescribed  HRR  and  the  ventilation,  but  none  of  these  scenarios  attained  the  peak  temperatures required due to the (lack of) oxygen supply at the lowest point in the tunnel.

Further simulations were attempted using the scenario of a HGV fire about halfway up the slope on the  north  side  of  the  tunnel.  In  this  scenario,  it  was  expected  that  all  the  smoke,  hot  gases  and combustion products would flow up the tunnel to the north, due to buoyancy effects, while fresh air would  be  drawn  in  from  the  south  in  sufficient  quantities  to  elevate  the  HRR  of  the  fire  and  the temperatures in the tunnel to the values required by the RWS curve. The HGV was modelled as being on the 9th step up on the north side. Various HRR values were prescribed over the course of several simulations, and the predicted ceiling temperatures only satisfied the RWS curve requirements when the HRR was set at 500MW or higher.

It  should  be  noted  that  heat  release  rates  of  the  order  of  500MW  are  highly  unrealistic  for  fires  in tunnels. The highest measured HRR for an experimental fire in a tunnel was just over 200MW. This was for a mock up of a HGV trailer in a nearly horizontal tunnel, loaded with nearly 11 tonnes of wooden and plastic pallets, subject to a forced longitudinal airflow [3]. Even multiple vehicle fires in tunnels have not been estimated to have exhibited HRRs of this scale. In the Channel Tunnel fire of November 1996, the fire involved ten HGVs and their carrier wagons, and the peak HRR of that fire has been estimated to have been about 350MW [4]. Very high temperatures, as simulated by the RWS curve,  are  only  expected  to  be  produced  during  fires  in  tunnels  which  are  close  to  horizontal.  In tunnels with significant gradients, such as the Clyde Tunnel, the smoke and hot gases produced by a fire  will  be transported away much more rapidly, due to buoyancy effects. This will tend to lead to smaller temperatures in the tunnel. In the event of a fire in the Clyde Tunnel, it is highly unlikely that the temperatures in the tunnel would be as high as those simulated by the RWS curve. Thus is has been necessary to use an unrealistically high prescribed HRR to simulate the temperature conditions required by the RWS standard. Therefore, the modelled scenario has to be considered as an 'extreme worst case' condition.

The  results  of  the  500MW  HGV  fire  simulation  are  presented  in  the  figures  that  follow.  Figure  6 shows representations of the temperature, velocity and pressure profiles on the centreline of the tunnel at 'steady state' condition.

Figure 6 - 'Steady state' conditions for a 500MW HGV fire on the north slope of the Clyde Tunnel, eastern tube.

<!-- image -->

Line chart

The steady state temperature and pressure recorded at the virtual thermocouples at the ceiling and the gap are shown in Figures 7-10. In each graph, the data are presented versus distance along the tunnel; measured in 17m 'steps' from the HGV location (184-196m from the portal) towards the north portal.

<!-- image -->

Line chart

It  is  clear  from  Figure  10  that  the  pressure  conditions  near  the  gap  were  generally  found  to  be  at approximately ambient pressure, that is, at most gap locations there would be no pressure-driven flow of hot gas into the cavity in the event of a fire, as the pressure difference between the cavity and the void would be insignificant.

The  only  significant  variation  from  this  trend  is  above  the  safety  box  in  the  first  fire  point  recess (nearest the portal), where the pressure reached a value of about 50 Pa above ambient pressure, see Figure 11. Thus it is necessary to calculate what the effect of the flow of hot gas (at about 510°C, see Figure 12) into the cavity at this point would be.

Figure 11 - The pressure profile recorded above the first safety box.

<!-- image -->

Line chart

## Flow of hot gas into the cavity

Calculations have been made for the case of a flow of hot gas (assumed to be hot air) at 510°C into the cavity, which is assumed to remain at ambient pressure. In reality, the pressure in the cavity would most likely be much closer to the pressure in the tunnel void, so the flow would be expected to be smaller. Also, due to the volume and geometry of the cavity, it is likely that a pressure balance would be  reached  fairly  quickly  and  so  the  flow  would  cease  early  in  the  fire  development.  Thus,  these calculations are to be taken to represent a 'worst case' scenario; in reality the flow, and hence the heat transfer to the tunnel structure would be much less significant than calculated here.

Figure 12 - The temperature profile recorded above the first safety box.

<!-- image -->

Line chart

Based on the temperature and pressure calculated in the tunnel, the gas density is taken to be:

<!-- formula-not-decoded -->

where R is the universal gas constant, taken to be 287.05 Jkg -1 K -1 .

Thus, 0.445 783 287.05 100050 = × ρ = kgm -3 in the vicinity of the gap above the 1 st safety box.

From Bernoulli's theorem, the velocity of a fluid passing through an opening can be taken to be:

<!-- formula-not-decoded -->

where Cd is the 'coefficient of discharge' which generally has a value of about 0.6 for instances like this where there is a pressurised flow through an orifice [5], thus:

<!-- formula-not-decoded -->

In  the  scenario  considered,  the  gas  jet  passes  through  a  narrow  gap  into  the  void  behind  the  panel which is taken to be about 0.3m wide for the most part. Thus the velocity will be reduced according to the ratio of the width of the opening to the width of the gap behind the panel. Thus, if the gap is 50mm wide, the velocity will reduce by 50 / 300 in  the  void  to  give  1.5ms -1 ,  or  if  the  gap  is  30mm  wide, the velocity will reduce by 30 / 300 in the void to give 0.9ms -1 , and so on. Thus there is a flow of hot gas at about 510°C flowing over the iron segments of the tunnel with a velocity of up to 1.5ms -1 (depending on the geometry of the gap). In the analysis presented here we will assume the gap is 50mm wide, hence the velocity over the tunnel structure is taken to be 1.5ms -1 .

Convective  heat  transfer  rates  are  governed  by  a  number  of  non-dimensional  groups.  In  order  to calculate the heat transfer to the iron sections, it is necessary to calculate the Nusselt number of the flow. The Nusselt number (Nu) is a function of the Reynolds number (Re) and the Prandtl number (Pr) which define the relationship between the inertia and viscosity of a fluid and the relationship between the momentum diffusivity and thermal diffusivity of a fluid, respectively. These may be found using the following equations:

<!-- formula-not-decoded -->

where L is a characteristic length scale, µ is the dynamic viscosity, is the thermal diffusivity, υ is the kinematic viscosity, cp is the specific heat at constant pressure and k is the thermal conductivity.

Assuming  the  width  of  the  cavity  behind  the  lining  (i.e.  0.3m)  to  be  the  characteristic  length,  the Reynolds number (taking the viscosity of air at 500°C from [5]) is:

<!-- formula-not-decoded -->

and the Prandtl number may be found, directly from a table in a text book [5], to be Pr = 0.7 for air at approximately 500°C. If  the  flow  over  the  iron  panel  is  laminar,  the  local  Nusselt  number  may  be found using:

<!-- formula-not-decoded -->

Whereas if the flow is fully turbulent, the local Nusselt number may be found using:

<!-- formula-not-decoded -->

The convective heat transfer coefficient, h , can be calculated from the Nusselt number:

<!-- formula-not-decoded -->

taking the value of k for air at 500°C from [5] and assuming turbulent flow. Having established h as being about 4.7 Wm -2 K -1 , we need to calculate temperature rise in the iron. For a solid of unit surface area we have:

<!-- formula-not-decoded -->

where V is volume (= 1 × 1 × 0.03), not velocity. c p and values for iron can be found in a text book (= 447 and 7870, respectively, from [5]). If we define the temperature difference between the gas and the solid as:

<!-- formula-not-decoded -->

The problem resolves to:

<!-- formula-not-decoded -->

This has the solution:

<!-- formula-not-decoded -->

For example, after two hours of exposure to the heated flow, the temperature rise of the iron is:

<!-- formula-not-decoded -->

Thus, after two hours, the temperature of the iron is 363° below the hot gas temperature, i.e. 147°C.

The calculated temperature rise of the iron with time is shown in Figure 13.

Figure 13 - Calculated temperature rise of unit area of tunnel structural section with time.

<!-- image -->

Line chart

It should be noted that the results calculated here and displayed in Figure 13 take no account of heat losses from the structural members of the tunnel, either to the gas flow or to the surrounding ground. If these losses were taken into account, the rate of temperature rise would be slower.

## Conclusions

A numerical study of a fire within the Clyde Tunnel has been conducted. The heat release rate of the fire was defined so that the temperatures within the tunnel reached the values described by the RWS standard. This study was complemented by heat transfer calculations to establish the impact of a lower gap  on  the  temperatures  of  the  structural  members  behind  the  protective  lining.  The  following conclusions can be drawn:

- To  obtain  the  RWS  curve  the  HRR  used  has  to  be  established  at  values  which  are unrealistically high. Given the geometry of the tunnel, ventilation will limit the temperatures within the tunnel to values well below the RWS curve. This results in a conservative analysis.
- The pressure distributions within the tunnel show that pressures close to the gaps are generally at or below ambient, thus hot gases will generally not enter through the gap.
- Specific  regions  where  there  is  a  potential  for  above  ambient  pressure  near  the  gap  were identified.  Local  peak  pressures  and  temperatures  were  identified  and  used  to  calculate  the flow of hot gases through the gap. An idealized heat transfer analysis, that includes no losses, was conducted. The analysis showed that after 2 hours of fire exposure the temperature of the structural elements will reach only 147°C. This analysis can be deemed as very conservative.
- Given the nature of the imposed fire and the uncertainty of the conditions within the tunnel, a simple but very robust and conservative approach was preferred. A more detailed analysis of the  flow  and  heat  transfer  within  the  gap  could  not  be  justified  given  the  definition  of  this problem.

## Acknowledgements

The authors would like to thank Byzak Ltd. (Scotland office; www.byzak.co.uk) for their support and permission to publish this paper. Thanks also to Glasgow City Council and Jacobs Babtie for useful discussions during the consultancy.

## References

- 1 P.H.E. van de Leur 'Tunnel fire simulations for the Ministry of Public Works' TNO Report B 91-0043 (in Dutch), 1991
- 2 National Institute of Standards and Technology fire research web site: http://fire.nist.gov/
- 3 H.  Ingason  &amp;  A.  Lönnermark  'Large  scale  fire  tests  in  the  Runehamar  Tunnel:  Heat  Release Rate' Proc. Int. Conf. on Catastrophic Tunnel Fires, Borås, Sweden, 20-21 November 2003. SP Report 2004:05, pp. 81-92.
- 4 S.K. Liew, D.M. Deaves and A.G. Blyth 'Eurotunnel HGV fire on 18th November 1996: Fire development and effects'. Proc. 3 rd Int. Conf. on Safety in Road and Rail Tunnels, Nice, France, March 1998. pp. 29-40.
- 5 F.P. Incropera &amp; D.P. Dewitt 'Fundamentals of heat and mass transfer' (4 th Edition), John Wiley &amp; Sons, New York, 1996. ISBN 0-471-30460-3