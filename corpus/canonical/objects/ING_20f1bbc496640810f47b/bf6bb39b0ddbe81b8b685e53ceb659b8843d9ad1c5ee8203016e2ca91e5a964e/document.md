GOSPODARKA

SUROWCAMI

MINERALNYMI

Tom 27

2011

Zeszyt 4

FABRIZIO BARPI*, MONICA BARBERO*, DANIELE PEILA**

## Numerical modelling of ground-tunnel support interaction using bedded-beam-spring model with fuzzy parameters

## Introduction

In order to design a tunnel lining following the usually applied codes and methods, the use of a computational tool to evaluate the underground and surface displacements, the plasticized zones around the void and the forecasted stresses acting inside the lining is required. On the other hand, the construction procedure could produce tunnel shapes different from the designed ones. For this reason, designers must always carry out parametrical analyses to asses the feasibility of the design. The British Tunnelling Society (2004) clearly states that the most important goal of a tunnel design is to provide an understanding of the rock mass and lining behaviour during tunnelling, including the evaluation of risks. Risk analysis is the essential way for producing a robust and safe design. Finally the design process should provide the basis for interpreting the monitoring results during construction. Due to the uncertainties concerning the properties of the rock mass and the loads induced in the lining the precision of the available analytical and numerical methods is often greater than the reliability and the accuracy of the data obtained from site investigations. Furthermore, the imperfections that unavoidably affect the tunnel construction have a great influence on the answer of the support system. Therefore, in order to understand the influence of input parameters on the analysis results, sensitivity analyses with the ground support interaction model have to be carried out.

The widely used lining design methods in tunneling practice are (AFTES 1976; USACE 1997; BTS 2004):

- ** Assistant Professor, Dept. of Structural and Geotechnical Engineering
- ** Professor. Dept. of Land, Environment and Geo-engineering, Politecnico di Torino

<!-- image -->

Music

- empirical methods, usually based on rock mass classification;
- analytical solutions, which are usually developed using:
- continuum analytical models (Muir Wood 1975),
- convergence-confinement method (Hoek and Brown 1980; Brown et al. 1983; Panet 1995),
- limit equilibrium methods, to evaluate the stability of rock blocks around a tunnel and the stability of tunnel face (Hoek and Brown 1980; Goodman and Shi 1985),
- bedded-beam-spring models (USACE 1997; Oreste 2007; Barpi and Peila 2011) where the tunnel lining is modelled as a series of beams connected to each other and to the ground by radial and tangential springs that simulate the ground support interaction;
- two and three-dimensional numerical analyses, which can be carried out using the finite element, the finite difference methods or the distinct element method with the ability to model complex geometrical, geological and geotechnical structures (BTS 2004).

The bedded-beam-spring model (also known as the hyperstatic reaction method) presents some disadvantages, such as the difficult to correct evaluate the spring stiffness (that is the object of the present investigation) and the loads to be applied to the lining, which has to be evaluated independently from the deformation of the system using, e.g., dead load approaches or rock mass classifications. Despite these drawbacks, this approach is widely applied in design practice thanks to its ease of use, and the possibility of obtaining a quick and simple evaluation of the actions inside the structural elements by varying the acting loads, and thus carrying out sensitivity analyses, that is, as mentioned before, of primary importance.

Tunnel designers should always take into account that every model could be affected by many error sources that could lead to poor predictions (Kalamaras 1996; BTS 2004; Peila 2009; Borio and Peila 2011) such as the theoretical shape of the tunnel, which can be different from the reality due to the construction method. For this reason, the present research analyses the tunnel boundary conditions after excavation and its influence on a ground-support system and on the stresses inside the lining.

The study of the ground-tunnel interaction is performed by introducing a predetermined degree of variation (fuzziness) into the input ground parameters. Given a certain degree of uncertainty in the parameters, the fuzzy set theory makes it possible to evaluate the uncertainty in the results, thereby avoiding the difficulties associated with stochastic analysis, since this method does not require any knowledge of the probability distribution functions.

Here it is assumed that model parameters are affected by a certain degree of uncertainty (defined by the so-called membership functions) and the computational results are calculated by solving the fuzzy equations, thus quantitatively estimating the influence of a given change in the model parameters.

## 1. Fuzzy logic

Fuzzy logic was introduced by Zadeh in the 60's in an attempt to formalize approximate knowledge and approximate reasoning (Zadeh 1968; Zadeh 1988). It is a superset of conventional Boolean logic extended to handle the concept of partial truth (i.e., truth values between 'completely true' and 'completely false'). Fuzzy logic recognizes more than true and false values: propositions can be represented with degrees of truthfulness and falsehood. This logic can be employed to develop complex systems, systems that are controlled by human experts, systems that use human observations as input and systems that are naturally vague (behavioural or social sciences).

It must be noticed that there are many similarities between fuzzy theory and probability theory; for example, both of them express uncertainty and have their values in the [0, 1] range, A detailed description of this technique is beyond the scope of this paper: the reader is referred to Dubois and Prade (1980) for a general treatment of this approach and to Schulz and Huwe (1997) for an example of application.

## 2. A new computational model for tunnel lining design

A new computational model has been developed in order to couple the bedded-beam-spring model with a fuzzy set analysis tool to take into account the imprecision in the data as outlined below.

This model is able to take into account a generic number of imprecise parameters and to solve the correspondent fuzzy equations. It performs the proper calculations (solution of the fuzzy equations) and output the membership function of the chosen parameters.

## 3. The bedded-beam-spring model

The bedded-beam spring model describes the tunnel lining as a series of beams connected at their nodes to a series of radial and tangential springs that are designed to model the ground reactions (Fig. 1).

The code used for the numerical simulations is based on the finite element concepts. The tunnel lining is discretized by using beam elements (with three degree of freedom) connected each other with nodes that are respectively connected to fixed point by normal and tangential springs. This procedure allows to take into account the interaction between ground and arch when the arch is affected by deformations induced by the applied loads (the ground action). The calculation procedure is the displacement method (Bathe 1996; Zienkiewicz, Taylor 2000), usually used in FEM models. The loads acting on the lining are evaluated by using an empirical formulation taking into account the properties of the rock mass and the geometry of the tunnel.

Fig. 1. Layout of the model, horizontal ( q h ) and vertical loads ( q v ) and node numbers ( R = 5.75 m) Rys. 1. Szkic modelu - obci¹¿enie poziome ( q h ) i pionowe ( q v ), zaznaczono numery wêz³ów (promieñ R = 5,75 m)

<!-- image -->

Engineering drawing

The structural elements (i.e., beams) are usually modelled as linear elastic; their stiffness is a function of the thickness and the elastic modulus of the constituting materials. Since the tunnel first lining is made of shotcrete and steel ribs it is necessary to define the equivalent tunnel cross section and a modulus of deformability that should take into due account the different properties of shotcrete (continuous) and steel ribs (discontinuous). The procedure used in this study is the one proposed by Hoek et al. (2008).

The stiffnesses of the springs Kn and Kt (Fig. 2) are usually evaluated from the rock mass data (Table 1) using very simple relationships as those derived from Winkler theory (DAUB 2005; AFTES 1976; USACE 1997). For example, USACE (1997) suggests to use:

<!-- formula-not-decoded -->

while Oreste (1999) suggests:

<!-- formula-not-decoded -->

where Req is the equivalent radius of the tunnel, E and c110 the elastic modulus and the Poisson coefficient of the ground, respectively.

Fig. 2. Constitutive relationship of the springs representing the ground reaction in the bedded-spring model p n and p t represent the normal and tangential load, c100 n and c100 n the normal and tangential displacement and K n and K t the normal and tangential stiffness

<!-- image -->

Line chart

Rys. 2. Zale¿noœæ konstytutywna opisuj¹ca relacjê oœrodka w modelu pow³okowo-belkowo-spre¿ystym p n i p t stanowi¹ normalne i styczne obci¹¿enia, c100 n i c100 n normalne i styczne przemieszczenia oraz K n i K t normalna i styczna sztywnoœæ

TABLE 1

TABELA 1

## Sztywnoœæ K n dla ró¿nych klas

Trzy wartoœci wspó³czynnika stopnia zniszczenia D: 0 - prace strza³owe doskona³ej jakoœci, 0,3 - stosunkowo p³ytkie naruszenie masywu skalnego, 0,7 - kontrolowane prace strza³owe

|                 |             | E d        | R eq K n   | E d        | R eq K n   | E d        | R eq K n   |
|-----------------|-------------|------------|------------|------------|------------|------------|------------|
| Rock mass class | RMR (aver.) | ( D = 0.0) | ( D = 0.0) | ( D = 0.3) | ( D = 0.3) | ( D = 0.7) | ( D = 0.7) |
|                 |             | GPa        | GPa        | GPa        | GPa        | GPa        | GPa        |
| I               | 90          | 74.49      | 62.49      | 63.70      | 53.08      | 48.70      | 40.58      |
| II              | 70          | 23.70      | 19.75      | 20.16      | 16.80      | 15.40      | 12.83      |
| III             | 50          | 7.50       | 6.25       | 6.37       | 5.31       | 4.87       | 4.06       |
| IV              | 30          | 2.37       | 1.98       | 2.01       | 1.68       | 1.54       | 1.28       |

Using Eqs. 1 and 2, the values of Kn for rock mass can be obtained from the RMR rock mass classification of Bieniawski as reported as an example in Table 1. The rock mass modulus of deformation is calculated using the formula suggested by Hoek et al. (2002) and the average values of RMR for each class of rock mass quality are used.

## Stiffness K n for different RMR classes

Three values of damage D are assumed: 0 (excellent quality controlled blasting), 0.3 (relatively shallow disturbance of the rock mass) and 0.7 (controlled blasting)

<!-- formula-not-decoded -->

where D represents the degree of disturbance of the rock mass, s ci the intact rock uniaxial compressive strength and GSI the geological strength index (Hoek, Brown 1997).

Recently, Oreste (2007) proposed more refined formulations with an hyperbolic constitutive relationship but, for the present work, a simpler formulation has been used due to the difficulty of determining the parameters suggested by the author from the in-situ investigation and, therefore, affected by the related uncertainties.

This design approach even if very simple is still widely used in tunnelling design also because it permits an easy parametric calculation; it is suggested by DAUB (2005) for the design of the shield in a mechanized tunnel.

In rock tunnels the lining is usually made of steel ribs and shotcrete and in the design the steel ribs are usually considered in contact with the rock along its whole length. This hypothesis is often far from the reality due to the irregularity of the rock boundary induced by blasting and by the natural joints pattern distribution. Actually, the steel ribs are in contact with the rock mass only in a discrete number of points (Fig. 3) and the empty spaces between rock and ribs are filled with shotcrete that is more deformable than the rock mass.

Fig. 3. Lining made of shocrete and steel ribs; ideal (on the left), real (on the right)

<!-- image -->

Engineering drawing

Rys. 3. Obudowa wykonana z torkretu i ³uków stalowych; wyidealizowany (po lewej), realny (po prawej)

The bedded spring model has therefore to take into account the presence of this shotcrete bed that has a crucial importance in the Kn and Kt evaluation. These parameters are influenced by the stiffness and thickness of the shotcrete bed since the stiffer element of the lining (the steel rib) interacts with the ground through the shotcrete bed that is thicker with the tunnel shape is more irregular.

The model used in the paper takes into account this irregularity using a fuzzy logic (Barpi, Peila 2011): the more irregular is expected to be the tunnel boundary after drill and blast excavation the largest will be the membership functions of Kn and Kt , thus the imprecision of the used values is increased.

with:

## 4. Application of fuzzy set analysis to ground-tunnel interaction

The influence of the uncertainty or imprecision affecting three parameters of the presented numerical model is assessed through a fuzzy approach. The parameters Kn and Kt (spring stiffness) and Es (elastic modulus of the lining, due to the possible irregular installation of the shotcrete) are considered to be fuzzy, i.e., associated with a certain degree of uncertainty, as defined through the appropriate membership functions c109 (triangular in this study). Such functions represent the level of confidence (or imprecision) of a variable; a typical shape could be triangular, trapezoidal, Gaussian or bell-shaped. Compared to stochastic analysis, this approach is a simpler and more intuitive way to allow for the uncertainty in some parameters, since it does not call for the determination of probability distribution functions. Given a value of the membership function it is possible to obtain a closed interval within which lies the variable of interest. The projections of c97 -cut (cut at level c97 ) on the axis of the variable define the left and right boundaries of this interval.

For example, c97 -cut = 0.5, as in Figure 5, defines intervals from 6.4 · 10 5 kN/m 3 to 9.6 · 10 5 kN/m 3 for Kn ; from 2.08 · 10 5 kN/m 3 to 3.12 · 10 5 kN/m 3 for Kt and from 1.14 · 10 7 kN/m 2 to 1.71 · 10 7 kN/m 2 for Es .

As a result, the variables of interest (output of the model), for instance the internal forces (bending moment M ( c113 ), normal force N ( c113 ) and shear force T ( c113 )) are expressed by fuzzy numbers (q is represented in Fig. 1). The same applies to any other output of the model, i.e., stresses in the boundary elements or in the structural elements. It means that M ( c113 ), N ( c113 ) and T ( c113 ) are associated with a certain membership function to be determined by finding, for each level 0 c163 c97 c163 1:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where the underline indicates the left boundary of a variable and the over-line the right boundary of the same variable, corresponding to a certain (given) value of c97 level.

The solution is found by minimizing and maximizing the fuzzy variables (subjected to the constraints in Eqs. 5) and calculating displacements, stresses, internal forces (or any other parameters of interest) for each level of c97 . The range of variation of the fuzzy variables represents their level of imprecision due to the imprecision in the input data.

The determination of the membership functions of internal forces, i.e., their level of imprecision, is achieved by repeating the calculation for different values of c97 . This problem can be viewed as an optimization problem, as explained in Dubois and Prade (1980).

## 6. Numerical simulations

In order to explain the proposed methodology, a case of a road tunnel excavated by drill and blast in the North of Italy was analyzed. The rock mass is constituted of dolomitic limestone (Fig. 4) with a RMR varying between classes II and III of Bieniawski (1989). No water was observed in the tunnel. The rock mass modulus of deformation was calculated with the Hoek-Brown formula (Hoek et al. 2002), thus the average values of Kn and Kt , to be used for the calculations were obtained, considering a thickness of the shotcrete bed equal to zero.

The applied loads q v and q h were evaluated using the Terzaghi formulation with a drained cohesion of 0.13 MPa and a drained friction angle of 23° for the rock mass. The obtained loads are q v = 0.37 MPa and q h = 0.5 · q v = 0.185 MPa.

The thickness of the lining was determined by homogenising (Hoek et al. 2008) the tunnel lining made of shotcrete (0.22 m thick) and steel ribs (two IPN180 ribs - standard European I beams, DIN 1025 - are installed side by side with a distance of 1 m, see Table 2).

The bedded-spring elements stiffnesses Kn and Kt (Fig. 1) were chosen to be equal to Kn = 8 · 10 5 Pa/m and Kt = 2.6 · 10 5 Pa/m while the elastic modulus of the lining Es = 1.42 · 10 7 N/m 2 . To avoid introducing any further uncertainties, the springs were designed to remain in the elastic range by raising the plasticization level.

TABLE 2

Material properties for shotcrete (0.22 m thick) and steel (two IPN180 ribs placed side by side) used as a first phase lining for the studied tunnel

TABELA 2

W³aœciwoœci torkretu (gruboœæ 0,22 m) i stali (dwa dwuteowniki IPN180 umieszczone obok siebie), stosowanych jako pierwszy etap podparcia dla badanego tunelu As mentioned above, parameters Kn , K t and Es are considered to be fuzzy and, hence, associated with given membership functions.

| Material   | Elastic modulus   | Poisson ratio   | Tensile strength   | Compressive strength   |
|------------|-------------------|-----------------|--------------------|------------------------|
| Material   | GPa               | -               | MPa                | MPa                    |
| Shotcrete  | 10                | 0.15            | 0.5                | 10                     |
| Steel      | 210               | 0.25            | 355.0              | 355                    |

Fig. 4: Simplified geological longitudinal section of the studied tunnel

<!-- image -->

Engineering drawing

Rys. 4. Uproszczony geologiczny przekrój pod³u¿ny analizowanego tlenku

To assess the influence of their shape, two different cases are examined. Each of them is described by the membership functions with symmetrical triangular shape with respect to the reference values showed in Figs. 5 and 6.

Fig. 5. Membership functions for K n , K t and E s

<!-- image -->

Line chart

for case 1 (left) and case 2 (right)

Rys. 5. Funkcja przynale¿noœci dla K n , K t i E s dla przypadku 1 (po lewej) i przypadku 2 (po prawej)

Fig. 6. Membership functions for bending moment, normal force and shear force (element 48) for case 1 Rys. 6. Funkcja przynale¿noœci dla momentu zginaj¹cego, si³y normalnej i si³y œcinaj¹cej w elemencie 48 dla przypadku 1

<!-- image -->

Line chart

## 7. Discussion of the results

The results of the analyses in terms of M, N and T on element 48 (located at the base of the arch, i.e., for c113 = 0 in Fig. 1) are shown in Figs. 6, 8 and 9 (case 1) and Figs. 7, 10 and 11 (case 2). Each diagram shows the values obtained for different c97 -cuts and allows to investigate the effects of parameters imprecision on the computed values and to identify the parameters with the most adverse influence on the response. For instance, in the element 48, for c97 -cut = 0, the bending moment ranges between 4.732 Nm/m and 3.308 Nm/m. With respect to the value 4.078 Nm/m that refers to c97 -cut = 1, the values of the bending moment that can be present in the lining are 18.9% smaller and 16.0% larger. Therefore, this range of variation should be considered in the interaction diagram.

It should be noted that, despite a linear membership functions of the input data is adopted (Fig. 5) the membership functions of the results (internal forces in the lining) are not linear. Furthermore the imprecision in the data results in a much higher imprecision in the values of T than in N or M , as shown in Fig. 6 (case 1). Similar consideration can be drawn for results of case 2 (Fig. 7), where the membership functions are 'narrow' comparing with to those of case 1.

Compared to a sensitivity analysis, the presented method allows to take into account an entire set of imprecise parameters and to determine the level of imprecision in the results. A different level of imprecision in the data can be obtained by changing the membership functions.

The results presented here show the relevance of taking into account properly the imprecision in model parameters and to quantitatively evaluate its influences on the results.

The interaction diagrams for shotcrete and steel are shown in Figs. 9, 10 and 11 according to the procedure outlined in Hoek et al. (2008) and Carranza-Torres and Diederichs (2009) (the material properties are listed in Table 2).

The diagrams for steel present two limit domains for the material strength: the larger curve is obtained using the maximum strength criterion i.e. the maximum principal stresses acting in the considered cross section (Hoek et al. 2008) while the smaller one is based on the well known Tresca criterion, i.e the material is considered yielded when the acting tangential stress reaches a pre-defined limit value.

Fig. 7. Membership functions for bending moment, normal force and shear force (element 48) for case 2 Rys. 7. Funkcja przynale¿noœci dla momentu zginaj¹cego, si³y normalnej i si³y œcinaj¹cej w elemencie 48 dla przypadku 2

<!-- image -->

Line chart

By using a safety factor of 1.5, some points for shotcrete fall outside the diagrams, which means a bending failure (Fig. 8). Similar considerations apply to Figs. 9, 10 and 11 based on the membership functions represented in Fig. 5. It must be pointed out that the data represented in Fig. 8, 9, 10 and 11 are related to the values of c97 = 0 and 1 (the minimum and the maximum c97 in the triangular used membership function of input parameters). The computed results (bending moments, normal force and shear force) are therefore represented by two different values: the minimum and the maximum that correspond to the chosen c97 -cut. Since the chosen membership function of input parameters is of triangular shape, for c97 = 0

Fig. 8. Bending moment vs. normal force for shotcrete (left) and steel ribs (right) (case 1)

<!-- image -->

Line chart

Rys. 8. Zale¿noœæ miêdzy momentem zginaj¹cym a si³¹ œcinaj¹c¹ dla torkretu (z lewej) i ³uków stalowych (z prawej) dla przypadku 1

Fig. 9. Shear force vs. normal force for shotcrete (left) and steel ribs (right) (case 1). In the right figure the dotted ellipse represent the Tresca criterion while the solid curve represent the maximum strength criterion

<!-- image -->

Line chart

Rys. 9. Zale¿noœæ miedzy si³¹ œcinaj¹c¹ a si³¹ normaln¹ dla torkretu (z lewej) i stalowych ³uków (z prawej) w przypadku 1. Na rysunku z prawej strony lini¹ przerywan¹ zaznaczono kryterium Tresca, a lini¹ ci¹g³¹ kryterium maksymalnej wytrzyma³oœci

Fig. 10. Bending moment vs. normal force for shotcrete (left) and steel ribs (right) (case 2) Rys. 10. Zale¿noœæ miedzy momentem zginaj¹cym a si³¹ normaln¹ dla torkretu (z lewej) i stalowych ³uków (z prawej) w przypadku 2

<!-- image -->

Line chart

Fig. 11. Shear force vs. normal force for shotcrete (left) and steel ribs (right) (case 2). In the right figure the dotted ellipse represent the Tresca criterion while the solid curve represent the maximum strength criterion

<!-- image -->

Line chart

Rys. 11. Zale¿noœæ miêdzy si³¹ œcinaj¹c¹ a si³¹ normaln¹ dla torkretu (z lewej) i stalowych ³uków (z prawej) w przypadku 2. Na rysunku z prawej strony lini¹ przerywan¹ zaznaczono kryterium Tresca, a lini¹ ci¹g³¹ kryterium maksymalnej wytrzyma³oœci

there are the two values of the computed results while for c97 = 1 (the reference values) the two values are coincident.

The results clearly show that if the average thickness is not considered, a wrong design could be obtained since the designed lining could be not adequate to support the applied loads, and cracks and damages could occur.

Based on this example, it is clear the contribution of the proposed methodology that permits an easy calculation of the effects of the imprecision and to find the most adverse combination of parameter.

## Conclusions

A new method for tunnel lining design is presented in the paper. It is based on a fuzzy approach, and applied to a well-known tunnel lining design method to take easily into account a degree of imprecision in model parameters. Furthermore the larger is the imprecision of the geometrical data (due to excavation procedure that cannot be completely forecasted at the design stage) the larger is the effect on the computed forces acting in the lining. The influence of this imprecision can lead to an underestimation of the structure strength that leads to cracks and damages. The considered imprecise parameters are the stiffness of the bed spring due to the irregular shape of the tunnel boundary induced by blasting and the deformation module of the beam that discretize the lining ( Kn , Kt and Es ).

The presented example permits to clarify the influence of the imprecision of input parameters on the results. Given this set of imprecise parameters (different membership functions), the influence of the imprecision affecting model results ( M , N and T ) is quantitatively evaluated.

It was clearly demonstrated that if the imprecision vary from +20% to + 40% from the average chosen value (the one that should be used in a deterministic analysis) the obtained results in term of acting forces go outside the yield criterion (i.e. the lining is fractured). Since the membership functions can be determined by using an expert judgment, the contribution of an expert in the field is easily included in the model and a complex statistical analysis can be avoided. Furthermore the set of parameters with the greatest influence on the answer of the system can be identified and properly taken into account at the design stage.

## REFERENCES

- Association Française des Tunnels et de l'Espace Souterrain, 1976 - Consideration on the usual method of tunnel lining design, Tunnels &amp; Ouvrages Souterrains, vol. 14, mars/avril.
- Barpi F., Peila D., 2011 - Influence of the tunnel shape on shotcrete linings stresses after excavation. Computer-Aided Civil and Infrastructure Engineering, on line version, DOI: 10.1111/j.1467-8667.2011.00728.x.
- Bathe K.J., 1996 - Finite Element Procedures. Prentice Hall.
- Bieniawski Z., 1989 - Engineering rock mass classifications: a complete manual for engineers and geologists in mining, civil, and petroleum engineering. Wiley-interscience publication, Wiley.
- Borio L., P e i l a D., 2011 - Laboratory test for EPB tunnelling assessment: results of test campaign on two different granular soils. Gospodarka Surowcami Mineralnymi, Vol. 27, No. 1, pp. 85-99.
- Brown E., Bray J., Ladanyi B., Hoek E., 1983 - Ground response curve for rock tunnels. Journal of Geotechnical Engineering, ASCE, Vol. 109, pp. 15-39.
- British Tunnelling Society (BTS), 2004 - Tunnel Lining Design Guide. Thomas Telford (London).
- Carranza-Torres C., Diederichs M., 2009 - Mechanical analysis of circular liners with particular reference to composite supports. For example, liners consisting of shotcrete and steel sets. Tunnelling and Underground Space Technology, Vol. 24, Elsevier, London, pp. 506-532.

- DAUB (German Commitee for Underground Construction), 2005 - Recommendation for static analysis of shield tunnelling machines. Tunnel, vol. 7, pp. 44-58.
- Dubois D., Prade H., 1980 - Fuzzy Sets and Systems: Theory and Application. Academic Press, San Diego.
- Goodman R., Shi G., 1985 - Block Theory and its Application to Rock Engineering. Prentice-Hall, New York.
- Hoek E., B r o w n E., 1997 - Practical estimates of rock mass strength. International Journal of Rock Mechanics and Mining Science, vol. 34, No. 8, pp. 1165-1186.
- Hoek E., Brown E., 1980 - Underground Excavation in Rock. The Institution of Mining and Metallurgy, London.
- Hoek E., C a r r a n z a -T o r r e s C., C o r k u m B., 2002 - Hoek-Brown failure criterion-2002 edition. 5 th North American Rock Mechanics Symposium, Toronto (Canada), pp. 267-273.
- Hoek E., Carranza-Torres C., Diederichs M., Corkum B., 2008 - The 2008 Kersten Lecture. Integration of geotechnical and structural design in tunnelling. 56 th Annual Geotechnical Engineering Conference, Minneapolis (USA), pp. 1-53.
- Kalamaras G., 1996 - A probabilistic approach to rock engineering design: application to tunnelling. Milestones in Rock Engineering: Bieniawski Jubilee Collection, Balkema, Rotterdam, pp. 113-135.
- Muir Wood A., 1975 - The circular tunnel in elastic ground. Geotechnique, vol. 25, No. 1, Thomas Telford, London, pp. 115-127.
- Oreste P., 1999 - Aspetti notevoli dell'analisi e dimensionamento dei sostegni di gallerie attraverso i metodi di calcolo numerici. Geoingegneria Ambientale e Mineraria, Vol. 57, Patron Editore, Bologna, pp. 39-50.
- Oreste P., 2007 - A numerical approach to the hyperstatic reaction method for the dimensioning of tunnel supports. Tunnelling and Underground Space Technology Vol. 22, No. 2, Elsevier, London, pp. 185-205.
- Panet M., 1995 - Le Calcul des Tunnels par la Méthode Convergence-Confinement. Presses de l'École Nationale des Ponts et Chaussées, Paris (France).
- Peila D., 2009 - Indagini preliminari nella costruzione di gallerie: analisi della letteratura tecnica. Geoingegneria Ambientale e Mineraria, Vol. XLVI, No. 3, Patron Editore, Bologna, pp. 37-59.
- Schulz K., Huwe B., 1997 - Water flow modelling in the unsaturated zone with imprecise parameters using a fuzzy approach'. Journal of Hydrology, Vol. 201, pp. 211-229.
- US Army Corps of Engineering (USACE), 1997 - Tunnels and shafts in rock. Engineering Manual 1110-2-2901, Washington (USA).
- Zadeh L., 1968 - Fuzzy algorithms. Information and Control, Vol. 12, pp. 94-102.
- Zadeh L., 1988 - Fuzzy logic. Institute of Electrical and Electronic Engineers Computer, Vol. 1, No. 14, pp. 83-93.
- Zienkiewicz O.C., Taylor R.L., 2000 - Finite Element Method: Volume 1, 2, 3, Butterworth-Heinemann.

MODELOWANIE NUMERYCZNE WSPÓ£PRACY OBUDOWY TUNELU Z OŒRODKIEM Z WYKORZYSTANIEM MODELU POW£OKOWO-BELKOWO-SPRÊ¯YNOWEGO ORAZ METODY ZBIORÓW ROZMYTYCH

## S³owa kluczowe

Obudowa modelu, model numeryczny, zbiory rozmyte

## Streszczenie

Przedstawiono i przeprowadzono dyskusjê wyników badañ wspó³pracy obudowy tunelu z oœrodkiem z wykorzystaniem okreœlonego stopnia zmiennoœci niektórych parametrów wybranego modelu. Badania te zwi¹zane s¹ z rozwa¿aniami, ¿e parametry i geometria modelu tunelu s¹ obarczone pewnym stopniem niepewnoœci, wynikaj¹cym z niedok³adnoœci konstrukcji i du¿¹ zmiennoœci¹ parametrów masywu skalnego. Badania zosta³y przeprowadzone z u¿yciem teorii zbiorów rozmytych zak³adaj¹c, ¿e trzy parametry modelu s¹ obarczone pewn¹ niepewnoœci¹ (zdeterminowan¹ przez funkcjê przynale¿noœci). Obliczenia numeryczne wykonano rozwi¹zuj¹c równanie funkcji losowych dla zró¿nicowanych funkcji przynale¿noœci. W celu sprawdzenia wp³ywu modelu parametrów i opracowania uproszczonej procedury i narzêdzi dla projektantów, przeprowadzono badania oparte na zbiorach losowych z u¿yciem znacznej i szeroko stosowanej metody wykorzystuj¹cej model pow³okowo-belkowo-sprê¿ynowy.

## NUMERICAL MODELLING OF GROUND-TUNNEL INTERACTION USING BEDDED-BEAM-SPRING MODEL WITH FUZZY PARAMETERS

Key words

Tunnel lining, numerical model, fuzzy logic

## Abstract

The study of the ground-tunnel interaction by introducing a predetermined degree of variation (fuzziness) in some parameters of the chosen model is presented and discussed. This research comes from the consideration that tunnel model parameters and geometry are usually affected by a degree of uncertainty, mainly due to construction imprecision and the great variability of rock mass properties. The research has been developed by using the fuzzy set theory assuming that three model parameters are affected by a certain amount of uncertainty (defined by the so-called membership functions). The response of the numerical model is calculated by solving the fuzzy equations for different shapes of the membership functions. In order to investigate the effects of some model parameters, and to provide a simple procedure and tool for the designers, a study on the effect of tunnel boundary conditions, based on a fuzzy model, has been carried out using a simple but well known and widely used design method such as the bedded-beam-spring model.