<!-- image -->

Logo

## Rotational failure mechanisms for the face stability analysis of tunnels driven by a pressurized shield

Guilhem Mollon, Daniel Dias, Abdul-Hamid Soubra

## To cite this version:

Guilhem Mollon, Daniel Dias, Abdul-Hamid Soubra. Rotational failure mechanisms for the face stability analysis of tunnels driven by a pressurized shield. International Journal for Numerical and Analytical Methods in Geomechanics, 2011, 35 (12), pp.1363-1388. ⟨10.1002/nag.962⟩. ⟨hal-01007269⟩

## HAL Id: hal-01007269 https://hal.science/hal-01007269v1

Submitted on 3 May 2018

HAL is a multi-disciplinary open access archive for the deposit and dissemination of scientific research documents, whether they are published or not. The documents may come from teaching and research institutions in France or abroad, or from public or private research centers.

L'archive ouverte pluridisciplinaire HAL , est destinée au dépôt et à la diffusion de documents scientifiques de niveau recherche, publiés ou non, émanant des établissements d'enseignement et de recherche français ou étrangers, des laboratoires publics ou privés.

<!-- image -->

Logo

## Rotational failure mechanisms for the face stability analysis of tunnels driven by a pressurized shield

Guilhem Mollon 1 , ∗ , † , Daniel Dias 1 , ‡ and Abdul-Hamid Soubra 2 , §

1 INSA Lyon, LGCIE Equipe Géotechnique, Bât. J.C.A. Coulomb, Domaine scientifique de la Doua, 69621, Villeurbanne cedex, France

2 Civil Engineering Department, University of Nantes, Bd. de l'université, BP 152, 44603 Saint-Nazaire, cedex, France

The aim of this paper is to determine the collapse and blow-out face pressures of a circular tunnel driven by a pressurized shield. The analysis is performed in the framework of the kinematical approach of the limit analysis theory. Two rotational failure mechanisms are proposed for the active and passive cases. These mechanisms have two significant advantages with respect to the available ones: (i) they take into account the entire circular tunnel face instead of an inscribed ellipse to this circular area, and (ii) they are more consistent with the rotational rigid-block movement observed in the experimental tests. For both the active and passive cases, the three-dimensional failure surface was generated 'point by point' instead of simple use of the existing standard geometric shapes such as cones or cylinders. This was achieved by employing a spatial discretization technique. The numerical results have shown that the present rotational mechanisms provide, in the case of frictional soils (with or without cohesion), a significant improvement with respect to the translational mechanisms. Finally, an extension of the proposed collapse mechanism to include a tension cut-off in the classical Mohr-Coulomb failure criterion is presented and discussed.

KEY WORDS: tunnel face stability; limit analysis; pressurized shield; upper-bound methods; collapse; blow-out

## 1. INTRODUCTION

The stability analysis of a tunnel driven by a pressurized shield is a key issue in real shield tunnelling projects. This paper focuses on tunnel face stability and considers a shield tunnelling under compressed air. In this case, the applied pressure is uniformly distributed on the tunnel face. The aim of the face stability analysis is to ensure safety against soil collapse and blow-out in front of the tunnel face. A soil collapse occurs if the applied face pressure is not sufficient to prevent the movement of the soil mass towards the tunnel. On the other hand, a blow-out appears when the applied face pressure is high enough to 'push' the soil towards the ground surface. It is desirable to assess both the collapse and the blow-out face pressure and thus determine the range of air pressure required to prevent both kinds of failure.

∗ Correspondence to: Guilhem Mollon, INSA Lyon , LGCIE Equipe Géotechnique , Bât. J.C.A. Coulomb, Domaine scientifique de la Doua, 69621 Villeurbanne cedex, France.

† E-mail: Guilhem.Mollon@insa-lyon.fr

‡ Associate Professor.

§ Professor.

The study of the face stability of circular tunnels driven by pressurized shields has been investigated by several authors in the literature. Some authors have considered a purely cohesive soil ([1-8] among others). In this case, the stability of the tunnel face is governed by the so-called load factor N defined as N = ( afii9846 s + afii9828 · H - afii9846 t ) / c u where afii9846 s is the surcharge loading on the ground surface, afii9846 t is the uniform pressure applied on the tunnel face, H is the depth of the tunnel axis, afii9828 is the soil unit weight and c u is the soil undrained cohesion. For the case of a frictional soil, some authors have performed experimental tests [9, 10]. Others [11-18] have performed analytical or numerical approaches.

This paper focuses on the face stability analysis in the general case of a frictional and / or cohesive soil. The most relevant approaches of a purely cohesive soil were proposed by Osman and coworkers [7, 8]. Their method is based on an admissible continuous velocity field. On the other hand, the most significant results in the case of a frictional soil (with or without cohesion) can be described as follows:

- Concerning the experimental investigations, the centrifuge tests by Chambon and Corté [9] have shown that the soil failure resembles to a chimney that does not necessarily outcrop at the ground surface. An arch effect that takes place above the tunnel face was pointed out by these authors to explain this phenomenon. On the other hand, the experimental tests performed by Takano et al. [10] have shown, by using X-ray computed tomography scanner, that the shape of the failure zone can be simulated with logarithmic spirals in the vertical cross-sections and elliptical shapes in the horizontal cross-sections. Their observations are of particular interest since they imply that a rotational mechanism bounded by log-spirals may adequately simulate the soil failure.
- Concerning the analytical models, the most significant approaches are based on the kinematical approach of limit analysis (e.g. Leca and Dormieux [12], and Mollon et al . [16, 18]). All these authors have suggested translational three-dimensional (3D) failure mechanisms. Leca and Dormieux [12] have proposed a mechanism composed of two conical blocks for the collapse case (Figure 1(a)) and a mechanism composed of a single conical block outcropping at the ground surface for the blow-out case (Figure 1(d)). The mechanisms by Mollon et al. [16] for collapse (Figure 1(b)) and blow-out (Figure 1(e)) constitute an improvement of the failure mechanisms by Leca and Dormieux [12] since they are composed of five conical blocks and thus allow the 3D slip surfaces to develop more freely. Notice however that the solutions by Mollon et al. [16] and those by Leca and Dormieux [12] suffer from the fact that only an elliptical area inscribed to the circular tunnel face is involved by failure due to the conical shape of the rigid blocks, the remaining area of the tunnel face being at rest. This is striking and is contrary to what was observed in the experimental tests [10] and numerical simulations [13]. This shortcoming was removed in [18] when dealing with the collapse mechanism (Figure 1(c)). This was made possible by using a spatial discretization technique for the generation of the 3D failure surface. Although this mechanism provided a significant improvement of the best existing solutions of the collapse pressure in the framework of the kinematical approach, it does not simulate the rotational movement observed in the experimental tests by Takano et al. [10]. The present study aims at developing two 3D rotational mechanisms for the active and passive cases. One should note that 3D rotational failure mechanisms in frictional and / or cohesive soils were already investigated in the literature when studying some stability problems in geotechnical engineering [19, 20]. These valuable approaches are based on circular cross-sections. At a first glance, a mechanism with a circular cross-section could appear convenient for the failure of a circular tunnel face. However, experimental and numerical models [9, 13] have shown that the velocity field of a soil failure is not normal to the tunnel face, both for collapse and blow-out. It means that the intersection of a failure mechanism with a circular cross-section would not be circular but elliptic (like in the existing mechanisms published in [12, 16]). As will be shown later, the approach developed in this paper is more general than that presented in [19, 20] because it allows to consider the entire tunnel face even for an 'inclined' velocity field. This is made possible by the use of a spatial

Figure 1. Some available mechanisms for collapse [(a) Leca and Dormieux [12]; (b) Mollon et al. [16]; (c) Mollon et al. [18]] and blow-out [(d) Leca &amp; Dormieux [12]; and (e) Mollon et al. [16]].

<!-- image -->

Engineering drawing

discretization for the construction of the velocity discontinuity surface. The generation of both the active and passive failure mechanisms is explained in the next section.

## 2. VELOCITY FIELD

This section is devoted to the presentation of (i) the velocity field, (ii) the geometrical construction of the 3D failure surface and finally (iii) the work equation.

The study considers a circular tunnel of diameter D driven by a pressurized shield in a c - afii9850 soil under a cover depth C . Two rotational rigid-block mechanisms are considered for the active and passive cases. Figure 2 shows the cross-sections of both mechanisms in the ( Y , Z ) vertical plane passing through the tunnel axis. It is assumed that in both cases, the cross-section is bounded by two log-spirals emerging from A and B (i.e. the crown and invert of the tunnel face) with a common centre O . Their respective equations in a polar ( r , afii9826 ) coordinate system centred at O are as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Figure 2. Cross-sections of the proposed failure mechanisms in the ( Y , Z ) plane: (a) collapse and (b) blow-out.

<!-- image -->

Engineering drawing

where

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Notice that, in Equations (1)-(2) and in all the following equations, when two signs are used together, the upper and lower signs refer to the collapse and blow-out mechanisms, respectively. Notice also that r A , r B , afii9826 A , afii9826 B , YO and ZO in Equations (3)-(6) can be easily identified from Figure 2. As shown in Figure 2, the two log-spirals meet at point F. This point represents the top of the failure mechanism in case of collapse (Figure 2(a)), and is located outside of the failure mechanism in case of blow-out (Figure 2(b)).

A cylindrical rotational velocity field is considered in this paper. This means that both mechanisms rotate with a uniform angular velocity afii9853 around a horizontal X -axis passing through point O (cf. Figure 2). Thus, the velocity vector is independent of the X coordinate. This property will be used at several places when writing the work equation. As shown in Figure 2, the velocity vector at a given point I with radius rI is equal to afii9853 · rI and it is inclined at an angle afii9826 I with the horizontal direction. This vector points to the tunnel face in case of collapse and to the ground surface in case of blow-out. The velocity field is entirely defined by point O in the ( Y , Z ) plane, (i.e. by the two parameters YO and ZO ). The same two parameters YO and ZO are also those that entirely define the failure mechanism. This is because the failure surface will be constructed in such a manner to respect the normality condition everywhere along the velocity discontinuity surface (i.e. the velocity should make an angle afii9850 with the failure surface). A quite practical method is to use rE / D and afii9826 E (instead of YO and ZO ) as the set of parameters necessary to entirely describe the failure mechanism. This is because these parameters are dimensionless and represent, respectively, the normalized radius and the inclination of the velocity at point E , which is the centre of the tunnel face. Thus, the position of point O can be expressed as a function of rE / D

and afii9826 E as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Since F is located on the two log-spirals emerging from A and B , one can easily show that:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

By using Equations (3)-(8), one may see that the polar coordinates of point F (i.e. Equations (9)-(10)) are also function of r E / D and afii9826 E which are the parameters that entirely describe the failure mechanism.

## 3. GEOMETRICAL CONSTRUCTION OF THE 3D FAILURE SURFACE

To take into account the entire circular tunnel face, one cannot use a simple geometrical shape to describe the 3D failure surface, and it is necessary to use a spatial discretization technique. Thus, the failure surface will be determined 'point-by-point'. The process of discretization aims at defining the coordinates ( X , Y , Z ) of a set of points located on the velocity discontinuity surface (i.e. the surface of the moving block). This process is described in more detail in the following sections.

## 3.1. Principle of the discretization

The circular contour of the tunnel face is discretized by several points, and the moving block is discretized by several radial planes that all meet at point O (i.e. all these planes are normal to the velocity field). As may be seen from Figure 3(c), for both the active and passive cases, Section 1 contains the radial planes that cut the tunnel face and Section 3 contains the radial planes that do not cut the tunnel face. The main idea for the generation of the 3D failure surface consists of generating a set of points that represent the contour of the mechanism in a given plane using another set of points representing the contour of the mechanism in a previous plane; the first plane being afii9811 1 (passing through points O , A 1 and A ′ 1 ). This quite complex discretization process may be described in more detail as follows:

The tunnel face is discretized by n afii9835 points called Aj and A ′ j where 1 ⩽ j ⩽ n afii9835 / 2 (Figure 3(b)). The discretization parameter n afii9835 has to be even, because two symmetric points Aj and A ′ j must be located on the same horizontal line. The coordinates of point Aj in the ( X , Y , Z ) coordinate system shown in Figure 3(a) are:

<!-- formula-not-decoded -->

where afii9835 j is the angle between segment EAj and the vertical direction. It has to be mentioned that the present discretization is used for a circular tunnel face. For the more general case of a non-circular tunnel face, it is only needed to choose the points of the tunnel contour that respect the same 'symmetry' condition cited above.

In Section 1 shown in Figure 3(c), a radial plane is denoted by afii9811 j where 1 ⩽ j ⩽ n afii9835 / 2. In Section 3, a radial plane is also denoted by afii9811 j , but here j is greater than n afii9835 / 2. The plane afii9811 j in Section 3 is defined by rotation of plane afii9811 j - 1 around the OX -axis by a constant angle afii9829 afii9826 . Thus, it makes an angle afii9826 j = afii9826 j - 1 + afii9829 afii9826 with the vertical direction (Figure 3(c)). The planes of Section 2 are generated until reaching the top of the mechanism (i.e. point F ) in case of non-outcropping mechanism or until the log-spirals that emerge from A and B have both attained the ground surface as shown in Figure 3(c). The last plane is called afii9811 j max. Concerning plane afii9811 j in Section 1, this plane contains the three points O , Aj and A ′ j , and it makes an angle afii9826 j with the vertical direction. Angle afii9826 j is one of the polar coordinates of points Aj and A ′ j with respect to O , and it is given by:

Figure 3. Discretization technique for the generation of the collapse and blow-out mechanisms, for a given set of the geometric parameters rE / D and afii9826 E .

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

For each one of the radial planes of both Sections 1 and 3, a local coordinate system ( Cj , x j , y j ) is adopted as shown in Figure 3(c) where Cj is defined as the intersection point between the plane afii9811 j and the circle of centre O and radius rF . Notice that y j points towards O and x j is in the same direction as the X -axis. The coordinates of C j in the ( X , Y , Z ) coordinate system are given by:

<!-- formula-not-decoded -->

For each plane afii9811 j of Section 1 (i.e. for 1 ⩽ j ⩽ n afii9835 / 2), the two points Aj and A ′ j of the tunnel face are assigned two angular parameters afii9835 ′ j and afii9835 ′′ j in the ( Cj , x j , y j ) local coordinate system of plane with afii9811 j . These parameters represent the angles between both vectors - - - → AjCj and - - - → A ′ j Cj and vector y j . For instance, angle afii9835 ′ j is given by

Figure 4. Details of generation of point Pi , j + 1 from points Pi , j and Pi + 1 , j : (a) perspective view and (b) plan views in planes afii9811 j and afii9811 j + 1.

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 3.2. Generation of the mechanism

As shown in Figure 4(a), each point Pi , j of the failure surface is defined by an index i that represents the position of this point in a given plane, and by an index j that corresponds to the plane where this point is located. The basic idea for the generation of the 3D surface consists of computing the coordinates of each new point Pi , j + 1 of plane ( afii9811 j + 1), using the coordinates of two points Pi , j and Pi + 1 , j in the previous plane afii9811 j . This computation is slightly different in the two Sections 1 and 3 of the mechanism as will be shown below.

3.2.1. Principle of generation of a new point in Section 1. The generation of new points in Section 1 begins with the use of points A 1 and A ′ 1 of the tunnel face (Figure 3). These two points belong also to plane afii9811 1 and can be renamed Pi , 1 and Pi + 1 , 1. The angular parameters afii9835 i , 1 and afii9835 i + 1 , 1 of these points in plane afii9811 1 can be obtained from Equation (14) as follows:

<!-- formula-not-decoded -->

From these two points, a new point Pi , 2 can be generated in plane afii9811 2. More generally, it is possible to generate point Pi , j + 1 in any plane afii9811 j + 1 from two points Pi , j and Pi + 1 , j of plane afii9811 j (cf. Figure 4(a)) using the three following conditions:

1. The plane of the triangular facet Fi , j that includes the three points Pi , j , Pi + 1 , j , and Pi , j + 1 should respect the normality condition, which means that the normal vector → Ni , j to this plane (pointing outside of the mechanism) should make an angle afii9843 / 2 + afii9850 with the velocity vector, for both the active and passive cases. The same value of afii9843 / 2 + afii9850 was adopted in both cases because the velocity vector is pointing downwards in case of collapse and upwards in case of blow-out (see Figure 2). Notice that the normality condition is necessary for the mechanism to be kinematically admissible and for the kinematic theorem of the limit analysis to be applicable.
2. Pi , j + 1 belongs to afii9811 j + 1.
3. The angular coordinate afii9835 i , j + 1 of point Pi , j + 1 in the local coordinate system ( Cj + 1 , x j + 1 , y j + 1) of plane afii9811 j + 1 is arbitrarily chosen as the average value of the angular coordinates afii9835 i , j (of Pi , j ) and afii9835 i + 1 , j (of Pi + 1 , j ) in the local coordinate system ( Cj , x j , y j ) of plane afii9811 j (Figure 4(b)). This means that afii9835 i , j + 1 = ( afii9835 i , j + afii9835 i + 1 , j ) / 2. This condition is not necessary for the mechanism to be kinematically admissible. It has simply the advantage to ensure that the generated points on the contour of the sliding surface in plane afii9811 j + 1 are quasi-uniformly distributed along this contour.

Once Pi , 2 has been generated in afii9811 2, one can consider the two points A 2 and A ′ 2 of the tunnel face (which belong to afii9811 2 as well) and rename them Pi - 1 , 2 and Pi + 1 , 2. One therefore can consider two segments in afii9811 2 ( Pi - 1 , 2 Pi , 2 and Pi , 2 Pi + 1 , 2, respectively) and create two new points in afii9811 3 ( Pi - 1 , 3 and Pi , 3, respectively), following the same method. This operation is repeated until the end of Section 1. In each plane afii9811 j + 1, n j - 1 points are generated ( n j being the number of points in plane afii9811 j ) and two other points located on the contour of the tunnel face already exist. Thus, the total number of points that can be used to form the contour of the failure surface in plane afii9811 j + 1 is equal to n j + 1.

As a conclusion, this method allows, for each segment Pi , j Pi + 1 , j in afii9811 j , to define a corresponding point Pi , j + 1 in plane afii9811 j + 1 such that (i) the normality condition is respected for the triangular facet Fi , j and (ii) the generated points in afii9811 j + 1 are quasi-uniformly distributed along this contour.

- 3.2.2. Principle of generation of a new point in Section 2. At the end of Section 1, plane afii9811 n afii9835 / 2 contains n afii9835 / 2 + 1 points. This number is equal to the number of segments since the contour of the discontinuity surface in plane afii9811 n afii9835 / 2 + 1 is closed. These n afii9835 / 2 + 1 segments allow one to generate n afii9835 / 2 + 1 new points in plane afii9811 n afii9835 / 2 + 1 . This generation is done following the three conditions mentioned in Section 1. The contours are then successively generated, until the end of Section 2 (Figure 3(c)). The mathematical formulation for the generation of point Pi , j + 1 from points Pi , j and Pi + 1 , j is detailed below.

3.2.3. Mathematical formulation for the generation of a new point from the two previous ones. As mentioned before, the normality condition states that the plane of each triangular facet Fi , j containing the three points Pi , j , Pi + 1 , j , and Pi , j + 1 should respect the normality condition. The ROTATIONAL FAILURE MECHANISMS

1371

ROTATIONAL FAILURE MECHANISMS

1371

coordinates of (i) vector - - - - - -→ Pi , j Pi + 1 , j that joins points Pi , j and Pi + 1 , j , and (ii) point P ′ i , j that is located at the centre of segment Pi , j Pi + 1 , j , in the ( X , Y , Z ) coordinate system are as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where the coordinates of points Pi , j , Pi + 1 , j , and Pi , j + 1 are as follows: Pi , j ( Xi , j , Yi , j , Zi , j ), Pi + 1 , j ( Xi + 1 , j , Yi + 1 , j , Zi + 1 , j ) , and Pi , j + 1 ( Xi , j + 1 , Yi , j + 1 , Zi , j + 1). On the other hand, the normal vector to facet Fi , j is given by ⃗ N ( Xn , Yn , Zn ). Notice that the velocity vector is considered to be applied at point P ′ i , j . Its norm depends on the position of this point. However, by the definition of the plane afii9811 j , the unit velocity vector → v j (i.e. the velocity vector divided by its norm) is constant in each plane afii9811 j , and its coordinates are given by:

<!-- formula-not-decoded -->

The coordinates of the normal vector → N should follow the three following conditions for both the collapse and blow-out cases:

- Fi , j should follow the normality condition and thus → N should make an angle afii9843 / 2 + afii9850 with → v j ;
- → N is a unit vector.
- → N is normal to Fi , j , and subsequently to the vector - - - - - -→ Pi , j Pi + 1 , j ;

These three conditions are expressed by the following system of equations:

<!-- formula-not-decoded -->

By substituting the expressions of vectors → v j , - → N , and - - - - - -→ Pi , j Pi + 1 , j into Equation (21), one obtains the following system of equations whose unknowns are Xn , Yn , and Zn :

<!-- formula-not-decoded -->

To solve this system, the following intermediate variables are introduced:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The coordinates of → N are finally given by:

<!-- formula-not-decoded -->

The negative or positive sign to be adopted for the computation of Zn in Equation (31) was chosen such that the normal vector → N points outside of the external surface of the failure mechanism. This condition was achieved by accepting the sign leading to - → N · ( - - - - - -→ Pi , j Pi + 1 , j × - → v j ) &gt; 0.

At this stage, it should be emphasized that Equation (31) gives the coordinates of the normal vector that respect the normality condition. In order to obtain the position of point Pi , j + 1 on plane afii9811 j + 1, one can write

<!-- formula-not-decoded -->

where ri , j + 1 is the distance between Cj + 1 and Pi , j + 1 (so far unspecified), and → afii9829 i , j + 1 is a unit vector with the following coordinates in the ( X , Y , Z ) global system of axis:

<!-- formula-not-decoded -->

To obtain the coordinates of point Pi , j + 1, the following normality condition is used:

The expressions of the coordinates of → afii9829 i , j + 1 are simply derived from the director cosines of this vector in the ( X , Y , Z ) axis system. It should be remembered here that → afii9829 i , j + 1 in Equation (33) imposes the value of the angle afii9835 i , j + 1 of point Pi , j + 1 as the average value of the angles afii9835 i , j and afii9835 i + 1 , j .

<!-- formula-not-decoded -->

In order to introduce Equation (32) into Equation (34) (i.e. in order to impose the angle afii9835 i , j + 1 for point Pi , j + 1), vector - - - - - - → P ′ i , j Pi , j + 1 may be written as follows:

<!-- formula-not-decoded -->

After some simplifications, Equation (34) leads to the following expression of ri , j + 1:

<!-- formula-not-decoded -->

Finally, the coordinates of Pi , j + 1 are given by:

<!-- formula-not-decoded -->

## 3.3. Closure of the mechanism

In the collapse case, the generation of the mechanism is stopped when one of the two conditions is reached: (i) the angle of the next plane afii9826 j + 1 is greater than afii9826 F , or (ii) all the points of the mechanism generated in plane afii9811 j + 1 are located above the ground surface (i.e. the mechanism has entirely outcropped, which is quite unlikely but can happen for very small values of afii9850 ). In the blow-out case, the second condition is the only one to consider, because the mechanism cannot close to itself and always outcrops. In the outcropping case (for both the collapse and blow-out mechanisms), the intersection between the moving block and the ground surface is defined as follows: Each triangular facet Fi , j is tested. If points P ′ i , j and Pi , j + 1 are both located above the ground surface, point Pi , j + 1 is deleted. If both points are below the ground surface, nothing is changed. However, if P ′ i , j is below the ground surface and Pi , j + 1 is above, point Pi , j + 1 is replaced by the intersection between the segment P ′ i , j Pi , j + 1 and the ground surface using a linear interpolation.

## 4. WORK EQUATION

At failure, the applied forces to the rotational rigid-block mechanism are: (i) the collapse or blowout face pressures (i.e. afii9846 c or afii9846 b), (ii) the possible surcharge loading afii9846 S acting on the ground surface (if the mechanism outcrops) and (iii) the weight of the soil composing the block. For the three calculations concerning the rate of work of these forces, one can use the fact that the velocity vector is independent of the X coordinate. For each external force, the computation of the rate of work is achieved by the summation of the elementary rates of work as follows (for details concerning the computation of the elementary volumes and surfaces, the reader may refer to the appendix given in [18]):

- Rate of work of the collapse and blow-out pressures are given, respectively, in Equations (38) and (39) as follows:

<!-- formula-not-decoded -->

- Rate of work of a possible uniform surcharge acting on the ground surface

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

- Rate of work of the soil weight

<!-- formula-not-decoded -->

where Ri , j and afii9826 i , j (respectively, R ′ i , j and afii9826 ′ i , j ) are the polar coordinates of the barycentre of the surface Si , j (respectively, S ′ i , j ) shown in Figure 5(c). Notice that all the other variables of Equations (38)-(41) may be easily identified from Figure 5(a)-(c), respectively.

- Rate of internal energy dissipation: Since a rigid block is considered, the only source of energy dissipation comes from the plastic soil deformation that occurs along the velocity discontinuity surface that separates the 3D failure surface and the soil at rest. Notice that the rate of internal energy dissipation along a unit velocity discontinuity surface is c · afii9829 u where afii9829 u is the tangential component of the velocity along the velocity discontinuity surface [21]. Calculations of the internal energy dissipation are made by the summation of the elementary energy dissipations along the different elementary surfaces as follows:

<!-- formula-not-decoded -->

It should be mentioned here that the computation of energy dissipation could also be made using an alternative convenient approach (for more details, see Michalowski and Drescher [20]). By equating the total rate of external force (i.e. Equations (38)-(41)) to the total rate of internal energy dissipation (i.e. Equation (42)), it is found after some simplifications that the face pressures for collapse and blow-out are given, respectively, by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where N afii9828 , N c , and N s are dimensionless coefficients given as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

These coefficients represent, respectively, the effect of soil weight, cohesion, and surcharge loading. To determine the value of the critical collapse and blow-out pressures, one has to maximize afii9846 c given by Equation (43) and minimize afii9846 b given by Equation (44) with respect to the two parameters of the mechanism ( rE / D and afii9826 E ). The maximization and minimization procedures were performed with the help of the optimization tool implemented in the commercial software Matlab. The discretization parameters used for the computation of the collapse and blow-out pressures are as follows: n afii9835 = 400 and afii9829 afii9825 = 0 . 5 ◦ . They were found to be the best compromises between accuracy and time-cost. The unconstrained optimization tool of Matlab uses an enhanced gradient optimization method. This process uses an arbitrary user-defined set of the parameters ( rE / D , afii9826 E ) as the starting point of the optimization, and converges to the unique optimum by a sequence of computations of the value of the pressure at several points of the space ( rE / D , afii9826 E ). The optimization automatically stops when a user-defined precision is obtained. With the discretization parameters mentioned above, one computation of the pressure takes about 2 s, using the four processors of a Core 2 Quad CPU 2.4 GHz Computer. The number of computations of the pressure is highly dependant on (i) the position of the starting point with respect to the optimal point and (ii) the user-defined final precision of the optimum. This number is generally smaller than 100 and leads to a computational time of nearly 3 min. Notice that this time could be reduced (i) by simplifying the computation of the dissipation term as proposed in [20], and (ii) by using a more efficient optimization tool.

Figure 5. Computation of the rates of work of: (a) the tunnel face pressure; (b) the surcharge at the possible outcropping surface; and (c) the soil weight of the moving block.

<!-- image -->

Engineering drawing

## 5. NUMERICAL RESULTS

The kinematic theorem of limit analysis is known as the 'upper-bound theorem' because it provides a rigorous upper bound of the ultimate load of a system. In the blow-out case, the applied pressure on the tunnel face is indeed a load, because it triggers the failure of the system. In the collapse case, however, the applied pressure is not a load, because it prevents the failure to appear. It may therefore be considered as a negative (or resisting) load. This is the reason why the kinematic theorem applied in the previous section will provide a rigorous upper bound of the ultimate blowout pressure, and a rigorous lower bound of the ultimate collapse pressure (despite the fact that the so-called 'upper-bound theorem' is applied).

## 5.1. Load factor of a purely cohesive soil

As mentioned in the introduction, the stability of a tunnel face in the case of a purely cohesive soil is entirely governed by the so-called load factor N . It should be emphasized here that the collapse and blow-out mechanisms lead to the same value of N . This is to be expected since the volume and surface involved by the failure mechanism in both cases are similar. The values of N provided by the proposed mechanism and by several authors are plotted as a function of the overburden ratio C / D (cf. Figure 6). It appears that the values provided by the present rotational mechanism are quite similar to the ones provided by the existing kinematic approaches using rigid-block mechanisms [3, 16, 18] for C / D &lt; 1 . 5, and less good (i.e. higher) for deeper tunnels ( C / D &gt; 1 . 8). On the other hand, Klar et al. [8] proposed a new kind of failure mechanism based on a continuous deformation of the soil mass, and obtained similar results to the existing rigid-block approaches. Nevertheless, it should be emphasized that the approach by Klar et al. [8] has a great potential, since the arbitrary velocity field chosen in this publication may be considerably improved. It should be mentioned that all these limit analysis approaches are quite far from the results obtained by the analytical methods [1], the numerical simulations [5], or the centrifuge tests [4]. It probably means that the present limit analysis approaches are not adequate to a purely cohesive soil. An extension of the approaches based on a continuous velocity field (developed by Osman et al. [7] in 2D and Klar et al. [8] in 2D and 3D) by choosing a more suitable velocity field appear much more promising. This will be the subject of future studies.

Figure 6. Load factor N versus C / D for a purely cohesive soil.

<!-- image -->

Line chart

Figure 7. Comparison of the collapse pressure with other authors' results.

<!-- image -->

Line chart

## 5.2. Limit pressures of a cohesionless soil

Figure 7 presents the values of the collapse pressure of a cohesionless soil as provided by the proposed mechanism and by several authors for the case D = 10m, afii9828 = 20kN / m 3 , and no outcrop of the moving block. The classical results by Leca and Dormieux [12] provide rigorous lower and upper bounds of the critical collapse pressure. The results obtained by Anagnostou and Kovari [14] (limit equilibrium) and by Eisenstein and Ezzeldine [13] (numerical model) are close to the lower bound provided by the kinematic approach by Leca and Dormieux [12]. From the figure, it can be seen that this rigorous bound was improved by the kinematic approach of Mollon et al. [18], and that the proposed mechanism improves again this last bound.

Figure 8(a) and (b) present a comparison between the collapse and blow-out pressures obtained by the present method and those of other kinematical approaches for two cohesionless soils ( afii9850 = 20 ◦ and afii9850 = 40 ◦ ). For the common values of C / D (i.e. C / D &gt; 1), the value of the collapse pressure afii9846 c remains constant (Figure 8(a)). This well-known phenomenon is due to the arch effect, which prevents the failure to reach the ground surface. The proposed results improve the best solutions of the collapse pressure provided by the multi-block translational mechanism by Mollon et al. [18]. The improvement is equal to 5.8 and 10.5% for afii9850 = 20 ◦ and afii9850 = 40 ◦ , respectively. The improvement with respect to the classical solutions by Leca and Dormieux [12] attains 26.1 and 25.7%, respectively.

On the other hand, the value of the blow-out pressure afii9846 b highly increases with the overburden ratio C / D (Figure 8(b)), since the blow-out always involves failure mechanisms reaching the ground surface. The improvement (i.e. reduction with respect to the best solutions of afii9846 b provided by Mollon et al. [16]) is significant, especially for large friction angles. Although the values of afii9846 b were significantly reduced with respect to the previous solutions, one should note that, in practical cases, the overburden ratio is hardly smaller that C / D = 1, and that the huge values of afii9846 b (larger than 1000 kPa) make the blow-out failure unrealistic even for small friction angles. The lack of numerical or experimental results prevents to determine if the proposed solutions of afii9846 b are close to the actual values. It is therefore difficult to know if this failure is actually unrealistic or if the proposed solution is still not good enough. For this reason, the blow-out failure phenomenon should be carefully investigated in future studies.

Figure 8. Critical pressure versus C / D for two sands ( D = 10m , afii9828 = 18kN / m 3 ): (a) collapse and (b) blow-out.

<!-- image -->

Line chart

## 5.3. Limit pressures of a frictional and cohesive soil

Figure 9(a) and (b) provides the collapse and blow-out pressures for two drained clays: (i) afii9850 = 17 ◦ and c = 7kPa (soft clay) and (ii) afii9850 = 25 ◦ and c = 10kPa (stiff clay), as given by the present method and by other kinematical approaches [12, 16, 18].

Concerning the collapse of the tunnel face (Figure 9(a)), the value of afii9846 c is improved by 12.4 and 34.9% (for the cases of soft and stiff clays, respectively) with respect to the best existing solution [18]. The improvement with respect to the classical solution by Leca and Dormieux [12]

Figure 9. Critical pressure versus C / D for two drained clays ( D = 10m , afii9828 = 18kN / m 3 ): (a) collapse and (b) blow-out.

<!-- image -->

Line chart

attains 62.3 and 154.8%, respectively. Concerning the failure by blow-out of the soil (Figure 9(b)), the observations are very similar to the case of a cohesionless soil: There is a strong improvement (i.e. reduction) in the values of afii9846 b, but these values remain very high, which makes such a failure quite unlikely. However, this could be because the proposed upper bounds of afii9846 b are still not good enough. Numerical and experimental studies should be carried out in the future to clarify this point.

## 5.4. Critical failure mechanisms

Two critical collapse mechanisms obtained from the maximization process are presented in Figure 10(a) and (b) for a sand ( afii9850 = 30 ◦ ) and for a drained clay ( afii9850 = 17 ◦ and c = 7kPa). Three views are provided for each mechanism. The diameter of the tunnel is equal to 10 m, and the overburden ratio is sufficiently high for the mechanisms not to outcrop (i.e. C / D &gt; 0 . 2 for the sand and C / D &gt; 0 . 6 for the clay). It was observed that the initial assumption concerning the shape of the failure surfaces (log-spirals) in the ( Y , Z ) plane is fully verified by the generated mechanism. One may observe that an important arch effect appears in the sand and leads to a less extended mechanism.

Figure 10. Views of the critical collapse mechanisms when D = 10m and afii9828 = 18kN / m 3 : (a) afii9850 = 30 ◦ and c = 0kPa and (b) afii9850 = 17 ◦ and c = 7kPa.

<!-- image -->

Line chart

The critical blow-out mechanisms are plotted for the same two cases in Figure 11(a) and (b). The geometrical data for the tunnel are D = 10m and C / D = 1. As expected, the size of the moving block is obviously much larger than in the collapse case and it increases with the increase of the value of afii9850 .

Finally, it should be noticed that the discretization chosen for plotting Figures 10 and 11 is quite coarse ( n afii9835 = 100 and afii9829 afii9825 = 2 ◦ ) in order to make visible the discretization of the 3D failure surface.

Figure 11. Views of the critical blow-out mechanisms when D = 10m and afii9828 = 18kN / m 3 : (a) afii9850 = 30 ◦ and c = 0kPa and (b) afii9850 = 17 ◦ and c = 7kPa.

<!-- image -->

Engineering drawing

It should be remembered here that the discretization parameters used for the computation of the collapse and blow-out pressures are as follows: n afii9835 = 400 and afii9829 afii9825 = 0 . 5 ◦ .

## 5.5. Design charts

Two design charts are provided in Figure 12(a) and (b) for the collapse and blow-out modes of failure in the case of a frictional soil (with or without cohesion). The results are provided in terms of the parameters afii9850 , c / afii9828 D , and afii9846 c / afii9828 D (or afii9846 b / afii9828 D ). For the collapse case (Figure 12(a)), the assumption of no-outcrop is made, which means that the overburden ratio C / D is larger than 0.8 (which is practically always true for the considered values of afii9850 ). For the blow-out case (Figure 12(b)), several charts should be plotted for various values of C / D , because this parameter has a significant impact on the blow-out pressures. Nevertheless, only one chart for C / D = 1 was provided here as an example, to limit the length of the manuscript. This overburden ratio was chosen because it is the smallest one that may occur in practice, and because higher values of this ratio make this kind of failure unlikely.

Figure 12. Design charts of the critical pressure for a frictional and cohesive soil: (a) collapse and (b) blow-out.

<!-- image -->

Line chart

Notice that the charts can be used to compute the collapse and blow-out pressures. They may also be used for the computation of the required tunnel face pressure for which a prescribed safety factor F s defined with respect to the soil shear strength parameters c and tan afii9850 is desired. This may be achieved if one uses the chart with cd and afii9850 d instead of c and afii9850 , where cd and afii9850 d are based on the following equations:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 6. IMPROVEMENT OF THE COLLAPSE MECHANISM

## 6.1. Principle of the improvement

This section focuses on a possible improvement of the collapse mechanism in the case of a frictional and cohesive soil. As shown in Figure 13 (case 1), the classical Mohr-Coulomb failure criterion leads to a tensile strength (chosen negative as a convention) equal to - c · cotan( afii9850 ). However, the usual behaviour of frictional and cohesive soils exhibits a smaller resistance to tension. The tensile strength (denoted by f t) should be considered as bounded by two limit values as follows:

<!-- formula-not-decoded -->

A reduction in the absolute value of the tensile resistance of the soil would logically lead to an improvement in the results of the collapse pressure provided by the classical Mohr-Coulomb criterion. The modified failure criterion proposed in this section is plotted in Figure 13. With respect to the classical Mohr-Coulomb criterion (case 1), the modified failure criterion is 'cut-off' by a circle tangent to the upper and lower linear envelopes, which meets the horizontal axis at a value f t of the axial stress. Figure 13 presents two cases (i) f t =- c (case 2) and (ii) f t = 0kPa (case 3). The rate of energy dissipation for an elementary discontinuity surface dS for which a normal velocity discontinuity v is considered, is given by Chen [21]:

<!-- formula-not-decoded -->

In order to take account of the tension cut-off in the computation of the collapse pressure, the failure mechanism described before is modified herein. It is truncated by a plane afii9811 j . This plane has to be normal to the discontinuity velocity v , for the failure to be purely tensile. The planes afii9811 j used for the discretization of the failure mechanism obviously fulfil this condition, because they meet at the centre of rotation O and are therefore normal to the velocity field (Figure 3). It means that a tensile failure may take place for any one of these planes, and that the choice of the critical tensile-failure plane brings a new degree of freedom in the optimization procedure. Thus, the present modified mechanism includes (i) failure by shear along the lateral surface and

Figure 13. Classical and modified (with tension cut-off) Mohr-Coulomb failure criterion.

<!-- image -->

Engineering drawing

(ii) failure by tension (tension cut-off) at the top of the mechanism. In this study, it was assumed that the plane afii9811 j cut along which tension failure occurs is located in Section 2, i.e. for j cut &gt; n afii9835 / 2. In that case, Equations (41) and (42) have to be replaced, respectively, by:

<!-- formula-not-decoded -->

The first term in Equation (53) corresponds to the rate of energy dissipation by shear failure along the external surface (up to plane afii9811 j cut) and the second term corresponds to the rate of energy dissipation due to tensile failure along plane afii9811 j cut. The total rate of energy dissipation is:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

In case where a tension failure takes place in a plane afii9811 j cut, the mechanism will not reach the ground surface. Thus, N s in Equation (43) vanishes, and the collapse pressure for a given set of parameters ( afii9826 E , rE / D ) and for a given value of j cut is given by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where

( N c ) j cut = cos afii9850 ∑ i , j ⩽ j cut ( Ri , j · Si , j + R ′ i , j · S ′ i , j ) + ∑ m ( f t c · afii9814 ′′ m · Rm ) ∑ k ( afii9814 k · Rk · cos afii9826 k ) (57) For the case where f t=0, Equation (57) may be rewritten in a simpler way as follows:

<!-- formula-not-decoded -->

where ( afii9846 c ) j cut - 1 is the collapse pressure for a mechanism composed of j cut - 1 slices and afii9829 afii9828 and afii9829 c (which are expressed in kPa) are the contributions of the slice numbered j cut to the critical collapse pressure (Figure 14). More precisely, afii9829 afii9828 is the contribution of the weight of the slice j cut , and afii9829 c is the contribution of the rate of energy dissipation due to shear failure of the same slice j cut. Their expressions are given as follows:

<!-- formula-not-decoded -->

∑ Figure 15 shows the variation of the collapse pressure ( afii9846 c ) j cut as a function of the index j cut (which represents a possible tension failure plane) for given values of the geometrical parameters ( afii9826 E , rE / D ) when f t = 0. For each slice of index j cut , afii9829 afii9828 and afii9829 c are also plotted on the same figure. One may see that for j cut &lt; j cut , max, the contribution of the soil weight of the slice j cut is greater than the contribution of its energy dissipation. The inverse is true when j cut &gt; j cut , max. Thus, the critical tensile plane j cut , max is the one for which a further slice reduces the ultimate pressure due to the fact that the contribution of soil weight of this slice is smaller than that of energy dissipation.

<!-- formula-not-decoded -->

Figure 14. Determination of the rate of energy dissipation on a tension failure plane.

<!-- image -->

Engineering drawing

Figure 15. Determination of the optimal plane for tension cut-off for a given set of the parameters afii9826 E and rE / D .

<!-- image -->

Line chart

As a conclusion, for the general case of a frictional and cohesive soil with tension cut-off, the critical collapse pressure is obtained by first searching the critical tensile plane for given values of ( afii9826 E , rE / D ) using a discrete maximization and then by searching the maximal collapse pressure among all possible values of ( afii9826 E , rE / D ).

## 6.2. Results with tension cut-off

Figure 16 presents some numerical results for the collapse mechanism with tension cut-off for several values of the tensile strength f t / c . This parameter varies from 0 to cotan( afii9850 ) for each considered soil. The most common case f t =- c is emphasized on the chart. Three drained clays are studied with various values of afii9850 and c . The improvement with respect to the classical MohrCoulomb criterion is presented in terms of per cent increase of the critical collapse pressure. One can observe that the improvement provided by the new criterion is much larger when the cohesion is high than when it is small. For example, the improvement provided by a zero tensile strength is only 1.0% for the case ( afii9850 = 17 ◦ , c = 7kPa), becomes equal to 3.8% for the case ( afii9850 = 25 ◦ , c = 10kPa), and reaches 19.9% for the case ( afii9850 = 15 ◦ , c = 15kPa). In this last case, the improvement is equal to 9% for the common value f t =- c , which proves that the phenomenon of tension failure is not to be neglected in frictional and cohesive soils.

Figure 16. Impact of the value of the tensile strength f t on the percent increase of the critical collapse pressure.

<!-- image -->

Line chart

Figure 17. Views of the critical collapse mechanism for a soil with a tension cut-off criterion with afii9850 = 15 ◦ , c = 15kPa, afii9828 = 18kN / m 3 , and f t = 0kPa.

<!-- image -->

Line chart

Three views of a critical collapse mechanism with tension cut-off are provided in Figure 17. The strength parameters are ( afii9850 = 15 ◦ , c = 15kPa , f t = 0kPa), and the critical collapse pressure is afii9846 c = 18 . 2kPa, whereas the same pressure for a classical Mohr-Coulomb criterion is afii9846 c = 15 . 2kPa.

## 7. CONCLUSION

Two new failure mechanisms based on the kinematical approach of limit analysis theory were presented in this paper in the aim to improve the existing solutions of the critical collapse and blow-out pressures of a shallow circular tunnel driven by a pressurized shield. The present failure mechanisms have a significant advantage with respect to the existing translational mechanisms by Leca and Dormieux [12] and Mollon et al. [16, 18] since (i) they take into account the entire circular tunnel face and not only an inscribed ellipse to this circular area, and (ii) they are closer to the observed rotational soil movement. This was made possible by the use of a spatial discretization technique allowing one to generate the 3D failure surface 'point-by-point'. The numerical results have shown that the proposed failure mechanisms decrease (i.e. improve) the existing solutions of the blow-out pressure and increase (i.e. improve) the existing solutions of the collapse pressure in the case of frictional soils (with or without cohesion). The improvement with respect to the classical collapse mechanism by Leca and Dormieux [12] attains 25% in the case of a cohesionless soil. In the case of purely cohesive soils, the improvement (i.e. decrease) of the critical value of N with respect to the one by Mollon et al. [16] is not significant. For this kind of soil, it is likely that a failure by movement of one or several rigid blocks is not adequate. Efforts should be done to extend the approaches by Osman et al. [7] and Klar et al. [8]. The chosen velocity fields in these publications are probably not optimal and may be improved. For frictional soils, two design charts were plotted for simple use in a practical context. In the last part, an improvement of the collapse mechanism in frictional and cohesive soils was proposed by taking into account a tension cut-off in the classical Mohr-Coulomb failure criterion. Such a modification induces a significant improvement when the cohesion of the soil is quite large, but this improvement is smaller when the cohesion is more reduced. However, the few cases studied here are not sufficient to draw a conclusion on this phenomenon, and this point probably requires further investigations.

Although the 3D geometrical construction presented in this paper is applied to a circular tunnel face, it may be easily extended to any form of the tunnel face for the stability analysis of a tunnel driven by the classical methods, since in the present work, the contour of the tunnel was not defined analytically but by discretization. More generally, this kind of technique could be quite easily applied to the failure of other geotechnical systems, such as slopes or foundations. Finally, notice that the use of a 'point-by-point' generation of the slip surface makes possible the application of the present method in spatially varying soils by considering the soil friction angle as a random field, which opens a wide range of applications.

## REFERENCES

1. Broms BB, Bennermark H. Stability of clay at vertical openings. Journal of the Soil Mechanics and Foundation Engineering 1967; 193 (SM1):71-94.
2. Mair RJ. Centrifugal modelling of tunnel construction in soft clay. Ph.D. Thesis , University of Cambridge, 1969.
3. Davis EH, Gunn MJ, Mair RJ, Seneviratne HN. The stability of shallow tunnels and underground openings in cohesive material. Géotechnique 1980; 30 (4):397-416.
4. Kimura T, Mair RJ. Centrifugal testing of model tunnels in clay. Proceedings of the 10th International Conference of Soil Mechanics and Foundation Engineering , vol. 1, Stockholm. Balkema: Rotterdam, 1981; 319-322.
5. Ellstein AR. Heading failure of lined tunnels in soft soils. Tunnels and Tunnelling 1986; 18 :51-54.
6. Augarde CE, Lyamin AV, Sloan SW. Stability of an undrained plane strain heading revisited. Computers and Geotechnics 2003; 30 :419-430.
7. Osman AS, Mair RJ, Bolton MD. On the kinematics of 2D tunnel collapse in undrained clay. Géotechnique 2006; 56 (9):585-595.
8. Klar A, Osman AS, Bolton M. 2D and 3D upper bound solutions for tunnel excavation using 'elastic' flow fields. International Journal for Numerical and Analytical Methods in Geomechanics 2007; 31 (12):1367-1374.
9. Chambon P, Corté JF. Shallow tunnels in cohesionless soil: stability of tunnel face. Journal of Geotechnical Engineering (ASCE) 1994; 120 (7):1148-1165.
10. Takano D, Otani J, Nagatani H, Mukunoki T. Application of X-ray CT on boundary value problems in geotechnical engineering-research on tunnel face failure. Proceedings of Geocongress , Proceedings of ASCE , Atlanta, 2006.
11. Horn N. Horizontaler erddruck auf senkrechte abschlussflächen von tunnelröhren. Landeskonferenz der Ungarischen Tiefbauindustrie 1961; 7-16.
12. Leca E, Dormieux L. Upper and lower bound solutions for the face stability of shallow circular tunnels in frictional material. Géotechnique 1990; 40 (4):581-606.
13. Eisenstein AR, Ezzeldine O. The role of face pressure for shieldswith positive ground control. Tunneling and Ground Conditions . Balkema: Rotterdam, 1994; 557-571.
14. Anagnostou G, Kovari K. Face stability conditions with earth-pressure-balanced shields. Tunnelling and Underground Space Technology 1996; 11 (2):165-173.

15. Broere W. Face stability calculation for a slurry shield in heterogeneous soft soils. Proceedings of the World Tunnel Congress 98 on Tunnels and Metropolises , vol. 1, Sao Paulo. Balkema: Rotterdam, 1998; 215-218.
16. Mollon G, Dias D, Soubra A-H. Probabilistic analysis and design of circular tunnels against face stability. International Journal of Geomechanics (ASCE) 2009; 9 (6):237-249.
17. Mollon G, Dias D, Soubra A-H. Probabilistic analysis of circular tunnels in homogeneous soils using response surface methodology. Journal of Geotechnical and Geoenvironmental Engineering (ASCE) 2009; 135 (9): 1314-1325.
18. Mollon G, Dias D, Soubra A-H. Face stability analysis of circular tunnels driven by a pressurized shield. Journal of Geotechnical and Geoenvironmental Engineering (ASCE) 2010; 136 (1):215-229.
19. De Buhan P, Garnier D. Three dimensional bearing capacity analysis of a foundation near a slope. Soils and Foundations 1998; 38 (3):153-163.
20. Michalowski RL, Drescher A. Three-dimensional stability of slopes and excavations. Geotechnique 2009; 59 (10):839-850.
21. Chen WF. Limit Analysis and Soil Plasticity . Elsevier: Amsterdam, 1975.