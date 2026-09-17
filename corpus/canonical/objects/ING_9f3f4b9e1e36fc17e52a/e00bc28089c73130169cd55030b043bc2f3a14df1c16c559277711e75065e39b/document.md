## Abstract

The magnetic perturbation due to the ferromagnetic test blanket modules (TBMs) may deteriorate fast ion confinement in ITER. This e ect must be quantified by numerical studies in 3D. We have implemented a combined finite element method (FEM) - Biot-Savart law integrator method (BSLIM) to calculate the ITER 3D magnetic field and vector potential in detail. Unavoidable geometry simplifications changed the mass of the TBMs and ferritic inserts (FIs) up to 26%. This has been compensated for by modifying the nonlinear ferromagnetic material properties accordingly. Despite the simplifications, the computation geometry and the calculated fields are highly detailed. The combination of careful FEM mesh design and using BSLIM enables the use of the fields unsmoothed for particle orbit-following simulations. The magnetic field was found to agree with earlier calculations and revealed finer details. The vector potential is intended to serve as input for plasma shielding calculations.

Keywords: ITER, Test Blanket Module, Magnetization, Ferritic Insert

## 1. Introduction

The goal of the fusion reactor ITER is to demonstrate the technological and scientific feasibility of fusion energy. The following reactor, DEMO, has a mission to demonstrate the largescale production of electrical power and tritium fuel self-sufficiency. One of the tasks of ITER is to be a testbed for DEMO components. ITER Test Blanket Modules (TBMs) will test the technology of tritium breeding modules for DEMO. Three of the eighteen ITER equatorial ports are reserved for these modules. The material chosen for DEMO is ferritic steel [1]. Therefore, the ITER TBMs will be made of ferromagnetic material that will get magnetized by the tokamak magnetic fields. The resulting local perturbation in the magnetic fields can deteriorate the confinement of the plasma. Especially, the weakly collisional fast ions may find a local 'hole' in the magnetic bottle and thus cause a hot spot on the first wall [2].

The TBM designs are checked for such threats by performing simulations of fast ions [3, 4]. The key ingredient for the simulations is a 3D magnetic field that includes the fields due to the magnetized components. This paper describes a method for calculating the field due to ferromagnetic ITER components. The used geometry describes the ferritic inserts and test blanket modules in detail. We also calculate another useful quantity: the magnetic vector potential - an important input for related plasma response calculations.

Input data. The key 'raw' data we use to calculate the 3D field consists of the geometry and electric current in toroidal field (TF) and poloidal field (PF) coils (including the central solenoid), the plasma equilibrium, and the geometry and material parameters of the ferromagnetic components. Two sets of components are considered: the TBMs and the ferritic inserts (FI) that are in place to reduce the variation of the toroidal field caused by having only 18 discrete TF coils.

Corresponding author

Email address: simppa.akaslompolo@alumni.aalto.fi (Simppa ¨ Ak¨ aslompolo)

Methods. Our main tool is the commercial COMSOL Multiphysics finite element method (FEM) platform (ver. 4.4.0.195) and its AC / DC Module. For geometry simplifications we also used the SpaceClaim Engineer 3D direct modeler. In addition, MATLAB routines were used to prepare and deliver information to COMSOL as well as to build the COMSOL model.

No FEM calculation can match the precision of a direct Biot-Savart law integration for magnetic fields from known coil geometry. To capitalise on this, we utilise a two-step COMSOL calculation: First we perform a magnetization calculation . Then a follow-up permanent magnet COMSOL calculation extracts the field due to the magnetization from the results of the magnetization calculation. The permanent magnet results from COMSOL are finally superimposed on the Biot-Savart law integrated fields. These fields are produced with the recently extended BioSaw code [5].

In the magnetization calculation, the magnetic fields (mf) interface of the AC / DC module in COMSOL solves the vector potential A and the divergence control variable from

<!-- formula-not-decoded -->

Symbol B denotes magnetic flux density and Je is the current density in coils or plasma. The nonlinear magnetic properties are described by the function H ( j B j ). At the boundaries

## Calculating the 3D magnetic field of ITER for European TBM studies

Simppa ¨ Ak¨ aslompolo a, , Otto Asunta a , Thijs Bergmans a , Mario Gagliardi b , Jose Galabert b , Eero Hirvijoki a , Taina Kurki-Suonio a , Seppo Sipil¨ a a , Antti Snicker a , Konsta S¨ arkim¨ aki a

a Department of Applied Physics, Aalto University, FI-00076 AALTO, FINLAND

b Fusion for Energy, Barcelona, Spain of the computational domain, the boundary condition is set to n A = 0 ; where n is the boundary's normal vector. However, the boundaries are e ectively several kilometres from the tokamak, as will be explained in the context of equation 2.

The permanent magnet model can be considered a reduced version of the above problem. We removed all coil and plasma currents and changed the constitutive relation inside the ferromagnetic components to B = 0 ( H + M ), where M is the magnetization vector. COMSOL extracts the magnetization from the solution of the first step and e ectively turns the ferromagnetic components into permanent magnets. The divergence condition variable is used for the permanent magnet model only when the vector potential needs to be evaluated.

## 2. Geometry

In this section we describe each major component present in the FEM model. The description justifies and explains all simplifications made to the geometry before importing it to COMSOL.

The 18 ITER toroidal field coils are D-shaped superconducting coils enclosing the plasma. We reconstructed the 3D geometry by sweeping the coil cross section [6] over the operating temperature spine curve [7]. However, the curve was not perfectly smooth and continuous after it was drawn according to the specifications. Therefore a 2 nd degree B´ ezier curve [8] was fitted to a dense sampling of the CAD curve. The numerically smooth final curve is in a format natively supported by COMSOL.

The poloidal field (PF) coils, the central solenoid (CS) and the plasma are assumed to be toroidally symmetric. We received the geometry information in EQDISK format, a quasistandard in fusion community. ITER has 6 CS coils and 6 PF coils. The only change to this input was the elimination of a 5 cm wide gap between the stacked CS coils by symmetrically stretching each coil vertically until they touched each other. Including this gap would have required small elements in the space between the coils without contributing significantly to the calculation. The current density was reduced to compensate for the increased cross-sectional area of the CS coils. The geometry is shown in Fig. 1.

The plasma cross-section was covered with a rectangular mesh (which was later swept toroidally) with the goal of extending the mesh up to the plasma-facing components (Fig. 1(b)). The mesh nodes were carefully fitted to coincide with the grid used in the EQDISK calculation, though the pitch was a multiple of the EQDISK grid pitch. This grid setting aligned the element edges to cylindrical coordinates. This was useful, as the current densities were now always parallel to an element. Furthermore, the calculated fields would later be exported in the same coordinate system.

The FI geometry we received represented the 'configuration model' of the components, including the special elements at the NBI ports. This is a simplified description primarily intended for checking that no two components in the vast ITER CAD model collide. Therefore small details such as bolt holes had already been removed. Nevertheless, the CAD data was still far too detailed for finite element analysis (FEA) as a part of a model encompassing the whole ITER torus.

Figure 1: (a) A single 20 degree sector including all the current-carrying domains. The calculation was performed in the complete 360 degree geometry. (b) The cross-sectional mesh of the toroidal current-carrying domains. The thick round curve is the plasma separatrix.

<!-- image -->

Engineering drawing

Figure 2: Various 3D models for the ferromagnetic components. (a) a simple FI geometry for fast testing. (b) and (c) are the FI models used for calculations (no di erence in results). (d) the original FI configuration model consisting of stacks of 40mm thick plates, which were merged in (c). The TBM geometry before (e) and after (f) simplification.

<!-- image -->

Engineering drawing

We made several simplified FI models starting from the configuration model, that are shown in Fig. 2(a-d). The first simplification was to remove radial gaps. The FIs are made of stacks of 40 mm thick steel plates with 4 mm gaps between the plates. To expedite the calculations, several toroidal gaps less than 10 mm wide were removed and a few somewhat wider gaps were extended by 10 mm. Modifying the gaps did not change the final results. Many small surface details, such as bevels, were also removed to simplify the final model.

Three equatorial ports of ITER are dedicated to TBMs, with room for two TBMs in each port. In our study, we placed a model of the European helium-cooled pebble bed (HCPB) TBM into all six TBM slots. In reality the di erent ITER partners will have their own test blanket module implementations in their slots.

The CAD model for the HCPB is very complex, but we received a model which had cooling ducts and many other smaller features already removed. We further simplified the model by, e.g., removing piping, merging thin plates together and removing air gaps. Figures 2(e-f) show the geometry before and after simplification.

The whole torus, including the coils, was enclosed inside a so called 'finite sphere' with a radius of 14 meters. This radius allowed us to fit the components inside the sphere with a margin of several meters in most cases, but only about one meter near a PF coil. The same structure was also implemented in the permanent magnet model albeit with all the coils absent. The finite sphere was enclosed inside a spherical shell, dubbed the 'infinite shell'. The name comes from the COMSOL feature we used to remap the radial coordinate % 2 = R 2 + z 2 inside the infinite shell in order to use boundary conditions at infinity:

<!-- formula-not-decoded -->

where % 0 is the inner radius of the infinite shell and % is the thickness of the shell. In our model the outer surface of the shell was mapped to a distance of several kilometers.

## 3. Current densities and material properties for the Finite Element Analysis

Weincluded the following free currents in our model: the toroidal and poloidal field coils (including the central solenoid) and the toroidal plasma current. The magnitude of the current density was assumed to be uniform in each coil. For the circular PF and CS coils, the current direction is trivial to calculate, but for the D-shaped TF coil we assumed the direction to be parallel to the spine curve described in section 2. COMSOL has the functionality to create a curvilinear coordinate system within the TF coil, but as this seemed to cause numerical problems in our geometry, we chose another route: a MATLAB routine returning a unit vector parallel to the spine curve of the TF coil was created. The magnitude of the toroidal plasma current density was calculated with a MATLAB routine from the current flux function f and the pressure flux function p read from the EQDISK file using equation 3.3.6 in [9]. (Note: there is a typo in that equation; 0 should be in the denominator.)

All domains were assumed to have the same electrical properties: relative permittivity " r = 1 and conductivity = 1 S / m. The current density was fixed in A / m 2 . Most domains had linear magnetic response with relative magnetic permeability r = 1, while for the ferromagnetic components we set the magnetization M as a function of magnetizing field H by defining the H - B curve, or H ( B ).

The FIs will be made of SS430 stainless steel, for which the B - H curve was the mean curve of the B - H curves in the table 4-1 of [10]. The magnetic properties data for the EUROFER steel [11] of the TBMs is temperature dependent, but we made a conservative assumption of uniform 350 C. A two-piece linear model for the H - B curve was constructed from the three available parameters. The first linear segment was assumed to pass through the origin, and the slope was calculated from the ratio of the coercive field Hc and the remanent magnetization Mr . The slope of the high field segment was vacuum permeability 0, and the knee point was calculated by solving the location where the first segment passes through saturation magnetization Ms .

Removing small details changed the metal volumes of the TBMs and FIs. To compensate for this, we modified the magnetic response of the materials, i.e., the H ( j B j ) function. We required that the simplifications would not change the magnetic moment M = R M d V of the objects at the uniform magnetic field limit. This resulted in the formula for a new H - B curve H ( B ), where the di erence in metal volume is accounted for:

<!-- formula-not-decoded -->

Here the volume ratio c is defined as c = V original = V simplified, and it varies between 0 : 7355 and 0 : 738 for the di erent kinds of FI sectors and is 1 : 001 for the TBMs.

## 4. Results

The COMSOL calculation produced 3D magnetic flux density B and vector potential A for various ITER scenarios. Figure 3 shows these fields for the 15 MA plasma current H-mode scenario during flat top phase. We then combined the COMSOL results with Biot-Savart law integrated background fields and analysed the field. Figure 4 shows a toroidal field ripple map (a measure of FI performance), the homoclinic tangle near the X-point, and Poincar´ e plots showing the structure inside the plasma separatrix. Finally, the field was decomposed into toroidal Fourier components, which are shown in Figure 5. These form the input for spectral plasma response codes. The magnetic fields were verified against earlier work [12] and were found to agree quantitatively. Please check the supplementary material (available electronically) for illustration.

## 5. Summary and Future work

We have devised a method for calculating the magnetization of ITER ferromagnetic components using the finite element method, and combined the resulting magnetic flux density B and magnetic vector potential A to Biot-Savart law integrated fields. The former can be used for studying, e.g., fast ion behaviour in the realistic ITER 3D field, while the latter provides the input for calculating the plasma response to the external perturbation.

Future work. Weare using the calculated fields in the ASCOT [13] suite of codes in order to simulate fast ion wall loads due to fusion alphas and heating neutral beams.

The simulations are in progress, and we already reported that the detail level at which the FIs are modeled in the field calculation does not appear to play a significant role for fusion alpha wall loads at least in the 15 MA H-mode case [14, 15]. The 3D fields will also be delivered to our collaborators so that the plasma response to the external perturbations can be included in future wall load simulations. At the time of writing this article, we have not discovered strong changes in the wall loads due the European TBMs. Only a couple of ITER scenarios have so far been addressed.

Figure 3: The magnetic flux density B (T) and the total magnetic vector potential A (T / m) as calculated by COMSOL. The total field is shown on the top row and the field due to the ferromagnetic components on the lower row. All images show three orthogonal cut planes displaying three orthogonal components of the field, as indicated in the figure. The thin black lines indicate component and domain boundaries in the model. There are harmless numerical artifacts visible in A in the 'infinite shell', caused by remapping of the spatial coordinates.

<!-- image -->

Geographical map

Figure 4: (a) Poloidal and (b) toroidal Poincar´ e plot showing the induced island structure within the plasma, (c) toroidal field ripple map, (d) the homoclinic tangle near X-point.

<!-- image -->

Line chart

10

Figure 5: Toroidal Fourier decomposition of the toroidal components of B and A fi elds. A single component on a poloidal plane is shown in figures (a), (b), (d) and (e). Figures (c) and (f) show the amplitude of the first 65 modes along the separatrix (black line).

<!-- image -->

Line chart

## Acknowledgements

The authors would like to thank Nicol` o Marconato and Pablo Vallejos for their help on using COMSOL.

This project has received funding from Fusion For Energy (grant F4E-GRT-379), the Academy of Finland (project No. 259675), Tekes - Finnish Funding Agency for Technology and Innovation. We acknowledge the computational resources from Aalto Science-IT project, CSC - IT center for science and the International Fusion Energy Research Centre.

## References

## References

- [1] L. Boccaccini, A. Aiello, O. Bede, F. Cismondi, L. Kosek, T. Ilkei, J.- F. Salavy, P. Sardain, L. Sedano, Present status of the conceptual design of the eu test blanket systems, Fusion Engineering and Design 86 (6-8) (2011) 478-483. doi:10.1016/j.fusengdes.2011.02.036 .
- [2] G. Kramer, B. Budny, R. Ellis, M. Gorelenkova, W. Heidbrink, T. KurkiSuonio, R. Nazikian, A. Salmi, M. Scha er, K. Shinohara, J. Snipes, D. Spong, T. Koskela, M. V. Zeeland, Fast-ion e ects during test blanket module simulation experiments in DIII-D, Nuclear Fusion 51 (10) (2011) 103029. doi:10.1088/0029-5515/51/10/103029 . URL http://stacks.iop.org/0029-5515/51/i=10/a=103029
- [3] T. Kurki-Suonio, O. Asunta, T. Hellsten, V. Hyn¨ onen, T. Johnson, T. Koskela, J. L¨ onnroth, V. Parail, M. Roccella, G. Saibene, A. Salmi, S. Sipil¨ a, ASCOT simulations of fast ion power loads to the plasmafacing components in ITER, Nuclear Fusion 49 (9) (2009) 095001. doi: 10.1088/0029-5515/49/9/095001 . URL http://stacks.iop.org/0029-5515/49/i=9/a=095001
- [4] K. Shinohara, T. Kurki-Suonio, D. Spong, O. Asunta, K. Tani, E. Strumberger, S. Briguglio, T. Koskela, G. Vlad, S. G¨ unter, G. Kramer, S. Putvinski, K. Hamamatsu, I. T. G. on Energetic Particles, E ects of complex symmetry-breakings on alpha particle power loads on first wall structures and equilibrium in ITER, Nuclear Fusion 51 (6) (2011) 063028. doi:10.1088/0029-5515/51/6/063028 .
5. [URL http://stacks.iop.org/0029-5515/51/i=6/a=063028](http://stacks.iop.org/0029-5515/51/i=6/a=063028)
- [5] T. Koskela, O. Asunta, E. Hirvijoki, T. Kurki-Suonio, S. ¨ Ak¨ aslompolo, ITER edge-localized modes control coils: the e ect on fast ion losses and edge confinement properties, Plasma Physics and Controlled Fusion 54 (10) (2012) 105008. doi:10.1088/0741-3335/54/10/105008 . URL http://stacks.iop.org/0741-3335/54/i=10/a=105008

- [6] ITER Organization, Desing Description Document 11-2: TF Coils and Structures, Tech. rep., ITER Organization, ITER D 2MVZNX v2.2 page 17, F4E D 25QXAR v1.0.

[URL https://user.iter.org/?uid=2MVZNX](https://user.iter.org/?uid=2MVZNX)

- [7] ITER Organization, TFW RADIAL PLATE, ITER D 28HP9H F, F4E D 25W2CJ v1.0 (2009).

[URL https://user.iter.org/?uid=28HP9H\_F](https://user.iter.org/?uid=28HP9H_F)

- [8] G. E. Farin (Ed.), Curves and surfaces for computer aided geometric design : a practical guide, 4th Edition, Academic Press Limited, 1997.
- [9] J. Wesson, Tokamaks, 2nd Edition, Vol. 48 of The Oxford Engineering Science Series, Clarendon Press, 1997.
- [10] C. Hamlyn-Harris, IWS Ferritic Material Magnetic Curves, Tech. rep., ITER Organization, F4E D 25NUFN v1.0, ITER D 3MBTJ7 v1.1 (2011).

[URL https://user.iter.org/?uid=3MBTJ7](https://user.iter.org/?uid=3MBTJ7)

- [11] F. Tavassoli, Fusion Demo Interim Structural Design Criteria (DISDC), Appendix A: Material Design Limit Data: A3.S18E Eurofer Steel, Tech. Rep. CEA / DMN / DIR / NT / 2005-01, Department of Materials for Nuclear, F4E D 22H6RK v1.0 (December 2005).

[URL https://idm.f4e.europa.eu/?uid=22H6RK](https://idm.f4e.europa.eu/?uid=22H6RK)

- [12] V. Amoskov, A. Belov, E. Gapionok, E. Lamzin, S. Sytchevsky, Database of magnetic field produced by tf coils, ferromagnetic inserts, and test blanket modules magnetized in toroidal and poloidal magnetic fields (15ma dt scenario at burn), Tech. Rep. ITER D 64D8GV v. 1.2, Saint Petersburg Company Energopul LTD (November 2011).

[URL https://user.iter.org/?uid=64D8GV](https://user.iter.org/?uid=64D8GV)

- [13] E. Hirvijoki, O. Asunta, T. Koskela, T. Kurki-Suonio, J. Miettunen, S. Sipil¨ a, A. Snicker, S. ¨ Ak¨ aslompolo, ASCOT: Solving the kinetic equation of minority particle species in tokamak plasmas, Computer Physics Communications 185 (4) (2014) 1310-1321. arXiv:1308.1904 , doi:10.1016/j.cpc.2014.01.014 . URL http://www.sciencedirect.com/science/article/pii/ S0010465514000277
- [14] T. Kurki-Suonio, S. ¨ Ak¨ aslompolo, K. S¨ arkim¨ aki, S. Sipil¨ a, A. Snicker, E. Hirvijoki, O. Asunta, T. Koskela, M. Gagliardi, Iter fusion alpha particle confinement in the presence of the european tbms and elm coils, in: 41st EPS Conference on Plasma Physics, Europhysics conference abstracts, European Physical Society, 2014, p. P5.017.

[URL http://ocs.ciemat.es/EPS2014PAP/pdf/P5.017.pdf](http://ocs.ciemat.es/EPS2014PAP/pdf/P5.017.pdf)

- [15] T. Kurki-Suonio, S. ¨ Ak¨ aslompolo, K. S¨ arkim¨ aki, S. Sipil¨ a, A. Snicker, E. Hirvijoki, O. Asunta, T. Koskela, M. Gagliardi, ITER energetic particle confinement in the presence of ELM control coils and european tbms, in: 25th Fusion Energy Conference (FEC 2014) Saint Petersburg, Russia 13 -18 October 2014, IAEA, 2014, pp. TH / P3-P30.