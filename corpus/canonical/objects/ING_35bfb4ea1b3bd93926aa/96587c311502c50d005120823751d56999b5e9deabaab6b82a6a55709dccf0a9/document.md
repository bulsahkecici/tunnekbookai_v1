<!-- image -->

Logo

## Face stability analysis of circular tunnels driven by a pressurized shield

Guilhem Mollon, Daniel Dias, Abdul-Hamid Soubra

## To cite this version:

Guilhem Mollon, Daniel Dias, Abdul-Hamid Soubra. Face stability analysis of circular tunnels driven by a pressurized shield. Journal of Geotechnical and Geoenvironmental Engineering, 2010, 136 (1), pp.215-229. ⟨10.1061/(ASCE)GT.1943-5606.0000194⟩. ⟨hal-01006892⟩

## HAL Id: hal-01006892 https://hal.science/hal-01006892v1

Submitted on 3 May 2018

HAL is a multi-disciplinary open access archive for the deposit and dissemination of scientific research documents, whether they are published or not. The documents may come from teaching and research institutions in France or abroad, or from public or private research centers.

L'archive ouverte pluridisciplinaire HAL , est destinée au dépôt et à la diffusion de documents scientifiques de niveau recherche, publiés ou non, émanant des établissements d'enseignement et de recherche français ou étrangers, des laboratoires publics ou privés.

<!-- image -->

Logo

## Face Stability Analysis of Circular Tunnels Driven by a Pressurized Shield

Guilhem Mollon 1 ; Daniel Dias 2 ; and Abdul-Hamid Soubra 3

Abstract: The aim of this paper is to determine the face collapse pressure of a circular tunnel driven by a pressurized shield. The analysis is performed in the framework of the kinematical approach of limit analysis theory. It is based on a translational three-dimensional multiblock failure mechanism. The present failure mechanism has a significant advantage with respect to the existing limit analysis mechanisms developed in the case of a frictional soil: it takes into account the entire circular tunnel face and not only an inscribed ellipse to this circular area. This was made possible by the use of a spatial discretization technique. Hence, the three-dimensional failure surface was generated 'point by point' instead of simple use of existing standard geometric shapes such as cones or cylinders. The numerical results have shown that a multiblock mechanism composed of three blocks is a good compromise between computation time and results accuracy. The present method significantly improves the best available solutions of the collapse pressure given by other kinematical approaches. Design charts are given in the case of a frictional and cohesive soil for practical use in geotechnical engineering.

K eywords: Tunnel; Limit analysis; Tunnel face stability; Pressurized shield; Upper-bound method.

## Introduction

The stability analysis and the assessment of ground surface settlement of a pressurized shield tunneling are of major importance in real shield tunneling projects. The aim of the stability analysis is to ensure safety against soil collapse in front of the tunnel face. This requires the determination of the minimal pressure ( air, slurry, or earth ) required to prevent the collapse of the tunnel face. On the other hand, the deformation analysis deals with the determination of the pattern of ground deformation that will result from the construction works. These ground deformations should be within a tolerable threshold to prevent damage to surface or subsurface structures. This paper is limited to the first problem, i.e., the face stability analysis of a shallow circular tunnel driven by a pressurized shield. Tunneling under compressed air is considered in the analysis.

The study of the face stability of circular tunnels driven by pressurized shields has been investigated by several writers in literature. Some writers have considered a purely cohesive soil ( Broms and Bennermark 1967; Mair 1979; Davis et al. 1980;

1 Ph.D. Student, INSA Lyon, LGCIE Site Coulomb 3, Géotechnique, Bât. J.C.A. Coulomb, Domaine scientifique de la Doua, 69621 Villeurbanne cedex, France. E-mail: guilhem.mollon@insa-lyon.fr

2 Associate Professor, INSA Lyon, LGCIE Site Coulomb 3, Géotechnique, Bât. J.C.A. Coulomb, Domaine scientifique de la Doua, 69621 Villeurbanne cedex, France. E-mail: daniel.dias@insa-lyon.fr

3 Professor, Dept. of Civil Engineering, Univ. of Nantes, Bd. de l'université, BP 152, 44603 Saint-Nazaire cedex, France ( corresponding author ) . E-mail: abed.soubra@univ-nantes.fr

Kimura and Mair 1981; Ellstein 1986; Augarde et al. 2003; Klar et al. 2007; among others ) . In this case, the stability of a tunnel face is governed by the so-called load factor N defined as N = ( 𝛔 s + 𝛄 H - 𝛔 t ) / c u where 𝛔 s = surcharge loading on the ground surface; 𝛔 t = uniform pressure applied on the tunnel face; H = depth of the tunnel axis; and c u = soil undrained cohesion. Broms and Bennermark ( 1967 ) stated from an experimental approach that the stability is maintained as long as N &lt; 6-7. Kimura and Mair ( 1981 ) conducted centrifuge tests and proposed a limit value of N between 5 and 10 depending on the tunnel cover. Later on, Ellstein ( 1986 ) gave an analytical expression of N for homogeneous cohesive soils based on a limit equilibrium analytical approach. His results are in good agreement with those by Kimura and Mair ( 1981 ) . More recently, an interesting numerical approach was proposed by Augarde et al. ( 2003 ) using a finiteelement limit analysis method based on classical plasticity theory. This promising approach is currently limited to a two-dimensional analysis. Finally, Klar et al. ( 2007 ) have suggested a new kinematical approach in limit analysis theory for the 2D and 3D stability analysis of circular tunnels in a purely cohesive soil. Their method is based on an admissible continuous velocity field. A velocity field that is proportional to a displacement field based on elasticity theory ( e.g., Verruijt and Booker 1996; Sagaseta 1987 ) was suggested by these writers. For the 3D face stability analysis, their numerical results were better than the values published by Davis et al. ( 1980 ) for great values of C / D where C = tunnel cover and D = tunnel diameter. A somewhat similar approach has been undertaken previously by Osman et al. ( 2006 ) for the 2D stability analysis of circular tunnels in a cohesive soil. However, the velocity field was based on the empirical Gaussian settlement trough near the ground surface instead of the analytical elasticity equations. For the case of a frictional soil, some writers have performed experimental tests ( cf., Chambon and Corté 1994; Takano et al. 2006 ) . Others ( Horn 1961; Leca and Dormieux 1990; Eisenstein and Ezzeldine 1994; Anagnostou and Kovari

1996; Broere 1998; Mollon et al. 2009 ) have performed analytical or numerical approaches. The aim of the centrifuge tests by Chambon and Corté ( 1994 ) was to visualize the collapse pattern and to determine the value of the critical face pressure. Chambon and Corté ( 1994 ) showed that the failure soil mass resembles to a chimney that does not necessarily outcrop at the ground surface. An arch effect that takes place above the tunnel face was pointed out by these writers to explain this phenomenon. On the other hand, Takano et al. ( 2006 ) have performed 1 g experimental tests using X-ray computed tomography scanner in order to visualize the three-dimensional shape of the failure mechanism. As in Chambon and Corté ( 1994 ) , a soil failure in the form of a chimney that does not necessarily attain the ground surface was pointed out by these writers. Finally, it was suggested that the shape of the failure zone can be simulated with logarithmic spirals in the vertical cross sections and elliptical shapes in the horizontal cross sections. Concerning the analytical models of a frictional soil, Anagnostou and Kovari ( 1996 ) and Broere ( 1998 ) have used the failure pattern proposed by Horn ( 1961 ) to determine the expression of the critical face pressure using the limit equilibrium method. They concluded that this method is quite simple to use but it is based on a priori assumptions concerning the shape of the failure mechanism and the normal stress distribution applied to the faces of the moving blocks. A more rigorous model based on the kinematical method of limit analysis was proposed by Leca and Dormieux ( 1990 ) . This model was then improved by Mollon et al. ( 2009 ) . On the other hand, Eisenstein and Ezzeldine ( 1994 ) have performed a numerical study for the stability analysis of a tunnel face using two models ( axisymetric and three dimensional ) . They stated that an axisymetric model is not enough accurate and underestimates the value of the critical collapse pressure.

As a conclusion, the kinematical limit analysis models by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) are among the most recent and significant approaches. It should be mentioned here that the upper-bound theorem ( kinematical approach ) states that if a work calculation is performed for a kinematically admissible collapse mechanism, then the loads thus deduced will be higher than ( or equal to ) those for collapse. Since the tunnel collapse pressure resists the collapse of soil into the tunnel, it is a negative load in the sense discussed earlier. Thus, the kinematical approach will provide an unsafe estimate of the tunnel pressure required to maintain stability ( i.e., smaller or equal to that actually required ) . The aim of this paper is to improve the existing solutions given by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) in the framework of the kinematical approach. The soil considered in the analysis is assumed to be frictional and/or cohesive. The main originality of the present work is that the failure mechanism presented herein includes the whole circular tunnel face while the existing mechanisms [ except that developed by Klar et al. ( 2007 ) in the case of a purely cohesive soil ] only involve an elliptical area inscribed to the circular face. This improvement required numerical generation 'point by point' of complex shapes of failure surfaces instead of simple use of existing standard geometric shapes ( such as cones or cylinders ) as it was made in Davis et al. ( 1980 ) , Leca and Dormieux ( 1990 ) , and Mollon et al. ( 2009 ) . After a short overview of the existing limit analysis failure mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) , the proposed mechanism and the corresponding numerical results are presented and discussed.

Fig. 1. Two-block failure mechanism by Leca and Dormieux ( 1990 )

<!-- image -->

Engineering drawing

## Overview of Previous Kinematical Limit Analysis Approaches

The problem of computation of the tunnel face collapse pressure 𝛔 c can be idealized as shown in Fig. 1 by considering a circular rigid tunnel of diameter D driven under a depth of cover C . Active collapse of the tunnel is triggered by application of surcharge 𝛔 s and self-weight, with the tunnel face pressure 𝛔 c providing resistance against failure. Under passive conditions, these roles are reversed, and blow-out of the soil mass in front of the tunnel face is caused by the tunnel pressure with resistance being provided by the surcharge and self-weight. The assumption of a uniform pressure at the tunnel face may be justified in the present paper where shield tunneling under compressed air is considered in the analysis. In this paper, only the active collapse of the tunnel face is considered in the analysis; the blow-out of the soil in front of the tunnel face being likely of less practical interest. As mentioned before, several theoretical models have been presented in literature for the computation of the tunnel face collapse pressures. The most recent and significant approaches are the ones presented by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) who considered three-dimensional failure mechanisms in the framework of the kinematical method in limit analysis. The mechanism by Mollon et al. ( 2009 ) constitutes an improvement of the failure mechanism by Leca and Dormieux ( 1990 ) since it allows the three-dimensional slip surface to develop more freely in comparison with the available two-block mechanism given by Leca and Dormieux ( 1990 ) . Both failure mechanisms are briefly described in the following sections in order to facilitate the understanding of the new failure mechanisms developed in the present paper.

The collapse mechanism presented by Leca and Dormieux in 1990 ( cf., Fig. 1 ) is composed of two truncated conical blocks with circular cross sections and with opening angles equal to 2 𝛗 in order to respect the normality condition in limit analysis. The lower conical block has an axis inclined at an angle 𝛇 with respect to the horizontal, and it intersects the tunnel face with a vertical ellipse tangent to the invert and to the crown of the tunnel face. The upper conical block has a vertical axis and it intersects the lower conical block with an elliptical area. In order to ensure the same contact area between both blocks, the inclination of the contact plane between the two blocks is such that the upper block is the mirror image of the lower block with respect to the normal to the area between both blocks ( i.e., plane 𝛑 shown in Fig. 1 ) . This is the reason why this mechanism is entirely defined by only one angular parameter 𝛇 . Notice that the assumption of a vertical axis for the upper block is not adequate and leads to nonoptimal collapse pressures.

Fig. 2. Multiblock failure mechanism by Mollon et al. ( 2009 ) ( after Mollon et al. 2009 )

<!-- image -->

Engineering drawing

The failure mechanism presented by Mollon et al. ( 2009 ) and described in more detail in Oberlé ( 1996 ) is an improvement of the two-block collapse mechanism presented by Leca and Dormieux ( 1990 ) . This mechanism is a multiblock ( cf., Fig. 2 ) . It is composed of n truncated rigid cones with circular cross sections and with opening angles equal to 2 𝛗 . A mechanism with n =5 is presented in Fig. 2. The geometrical construction of this mechanism is similar to that of Leca and Dormieux ( 1990 ) , i.e., each cone is the mirror image of the adjacent cone with respect to the plane that is normal to the contact surface separating these cones. This is a necessary condition to ensure the same elliptical contact area between adjacent cones. In order to make clearer the geometrical construction of the 3D failure mechanism, Fig. 3 shows how the first two truncated conical blocks adjacent to the tunnel face are constructed. The geometrical construction of the remaining truncated conical blocks is straightforward. As for the mechanism by Leca and Dormieux ( 1990 ) , Block 1 is a truncated circular cone adjacent to the tunnel face. The intersection of this truncated cone with the tunnel face is an elliptical surface that does not cover the entire circular face of the tunnel. This is a shortcoming not only of the multiblock mechanism by Mollon et al. ( 2009 ) but also of the two-block mechanism by Leca and Dormieux ( 1990 ) . On the other hand, Block 1 is truncated with Plane 1 which is inclined at an angle 𝛈 1 with the vertical direction ( cf., Fig. 3 ) . In order to obtain the same contact area with the adjacent truncated conical block, Block 2 is constructed in such a manner to be the mirror image of Block 1 with respect to the plane that is normal to the surface separating the two blocks ( i.e., Plane 2 as shown in Fig. 3 ) . The mechanism by Mollon et al.

Fig. 3. Detail of the construction of the multiblock failure mechanism by Mollon et al. ( 2009 ) ( after Mollon et al. 2009 )

<!-- image -->

Engineering drawing

( 2009 ) is completely defined by n angular parameters 𝛇 and 𝛈 i ( i =1, ... , n -1 ) where n is the number of the truncated conical blocks ( cf., Fig. 2 ) .

Notice finally that the upper rigid cone in the mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) will or will not intersect the ground surface depending on the 𝛗 and C / D values. This phenomenon of no outcropping at the ground surface was also pointed out by Chambon and Corté ( 1994 ) and Takano et al. ( 2006 ) while they performed experimental tests: As mentioned before, a failure soil mass which has the shape of a chimney that does not necessarily outcrop at the ground surface was observed by these writers.

Both mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) are translational kinematically admissible failure mechanisms. The different truncated conical blocks of these mechanisms move as rigid bodies. These truncated rigid cones translate with velocities of different directions, which are collinear with the cones axes and make an angle 𝛗 with the conical discontinuity surfaces in order to respect the normality condition required by the limit analysis theory. The velocity of each cone is determined by the condition that the relative velocity between the cones in contact has the direction that makes an angle 𝛗 with the contact surface.

The numerical results obtained by Mollon et al. ( 2009 ) have shown that a five-block ( i.e., n =5 ) mechanism was found sufficient since the increase in the number of blocks above five blocks increases ( i.e., improves ) the solutions by less than 1%. The improvement of the solution by Mollon et al. ( 2009 ) with respect to the one by Leca and Dormieux ( 1990 ) is due to the increase in the degree of freedom of the failure mechanism by Mollon et al. ( 2009 ) . Notice however that the solutions by Mollon et al. ( 2009 ) and those by Leca and Dormieux ( 1990 ) suffer from the fact that only an inscribed elliptical area to the entire circular tunnel face is involved by failure due to the conical shape of the rigid blocks; the remaining area of the tunnel face being at rest. This is striking and is contrary to what was observed in numerical simulations. This shortcoming will be removed in the following failure mechanisms developed in this paper.

## Kinematical Approach for the Computation of the Tunnel Face Collapse Pressure

The aim of this paper is to compute the tunnel face collapse pressure of a shallow circular tunnel driven by a pressurized shield in a frictional and/or cohesive soil. The theoretical model is based on a three-dimensional multiblock failure mechanism in the framework of the kinematical approach of the limit analysis theory. In order to render clearer the theoretical formulation of the multiblock mechanism, the geometrical construction of a mechanism composed of a single rigid block is first presented. It is then followed by the presentation of the multiblock mechanism. The one- and multiblock mechanisms developed in this paper will be referred to as improved mechanisms since they allow ( 1 ) to consider the entire circular area of the tunnel face and not only an inscribed ellipse inside this area; ( 2 ) to improve the solutions presented by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) in the framework of the kinematical approach of limit analysis.

## Improved One-Block Mechanism M1

M1 is a rigid translational one-block mechanism. It is defined by a single angular parameter 𝛃 ( cf., Fig. 4 ) . This angle corresponds to the inclination of the velocity of this block with respect to the longitudinal axis of the tunnel. Since a failure mechanism involving the whole circular area of the tunnel face is explored here, no simple geometrical shape ( such as a cone ) can be considered. It is necessary to generate the three-dimensional failure surface point by point using a spatial discretization technique.

Fig. 4. Cross section of the improved one-block mechanism in the ( y , z ) plane in two cases: ( a ) no outcrop of the mechanism at the ground surface; ( b ) outcrop at the ground surface

<!-- image -->

Engineering drawing

## Method of Generation of the Improved One-Block Mechanism

It is assumed ( cf., Fig. 4 ) that the cross section of the improved one-block mechanism in the vertical plane ( y , z ) containing the longitudinal axis of the tunnel is the same as that of the one-block mechanism composed of a single conical block with an opening angle equal to 2 𝛗 . This is to be expected because the conical one-block mechanism involves the entire diameter of the tunnel face only along the vertical diameter of the tunnel face. Referring to the ( y , z ) coordinate system shown in Fig. 4, the z -coordinate of the apex of the mechanism ( i.e., Point A ) is denoted z max . In case of no outcrop of the failure mechanism at the ground surface [ cf., Fig. 4 ( a )] , z max is given by

<!-- formula-not-decoded -->

Otherwise, the failure mechanism outcrops at the ground surface [ cf., Fig. 4 ( b )] and z max becomes equal to

<!-- formula-not-decoded -->

The three-dimensional failure surface of the improved one-block mechanism is determined here by defining the contours of this surface at several vertical planes parallel to the tunnel face ( cf., Fig. 5 ) . Notice that the contour of a given plane is defined from that of the preceding plane. The first vertical plane to be considered is that of the tunnel face for which the contour of the failure surface is circular as required. The different vertical planes are equidistant; the horizontal distance separating two successive planes being 𝛅 z = z max / nz where nz = number of slices considered in the spatial discretization of the 3D failure surface along the z -axis ( cf., Fig. 4 ) . The vertical planes are denoted by index j where j =0, ... , nz ; j =0 being that of the tunnel face ( cf., Fig. 5 ) . In the following, the generation of only the first contour ( i.e., that corresponding to j =1 ) of the failure surface located at a distance 𝛅 z from the tunnel face and using the contour of the tunnel face ( which is circular of diameter D ) will be presented. The generation of the subsequent contours is straightforward.

The contour of the tunnel face is discretized by a number n 𝛉 of points Pi ,0 uniformly distributed along this contour. Point Pi ,0 is defined by the parameters ( R , 𝛉 i ) in the polar coordinate system and by the following coordinates in the ( x , y ) plane corresponding to the tunnel face ( cf., Fig. 5 ) :

Fig. 5. Principle of generation of the 3D failure surface by using several contours parallel to the tunnel face and several points on each contour

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

Thus, each point of the failure surface is defined by two indices i ( index indicating the position of the point in a given vertical plane ) and j ( index of the vertical plane ) . The generation of point Pi ,1 in the first contour makes use of three points Pi ,0 , Pi -1,0 , and Pi +1,0 belonging to the tunnel face ( cf., Fig. 5 ) . The position of point Pi ,1 must satisfy the three following conditions ( cf., Fig. 6 ) : · Pi ,1 belongs to plane j =1, i.e.

<!-- formula-not-decoded -->

- The triangular surface formed by points Pi ,0 , Pi -1,0 , and Pi ,1 should respect the normality condition in limit analysis, i.e., the normal to the plane of this triangle should make an angle 𝛑 / 2+ 𝛗 with the velocity vector V . This normality condition is necessary for the failure mechanism to be kinematically admissible and for the limit analysis theory to be applicable.
- The triangular surface formed by points Pi ,0 , Pi +1,0 , and Pi ,1 should also respect the normality condition.

Fig. 6. Principle of generation of point Pi ,1 from point Pi ,0 located on the contour of the tunnel face

<!-- image -->

Engineering drawing

The procedure described earlier allows one to create for each point Pi , j a corresponding point Pi , j +1 in the following plane by respecting the normality condition in the neighborhood of Pi , j . The mathematical formulation of this problem can thus be briefly described as follows.

The three points Pi ,1 , Pi ,0 , and Pi -1,0 define a plane named ( 𝚪 1 ) , with a normal vector N 1 ( which is as yet unspecified ) . Also, vector A 1 belonging to the plane j =0 is defined as: A 1

= P i -1,0 P i ,0 where the coordinates of points Pi ,0 , and Pi -1,0 are given, respectively, by ( x i ,0 , y i ,0 , z i ,0 ) and ( x i -1,0 , y i -1,0 , z i -1,0 ) . Vectors N 1 and A 1 are given as follows:

<!-- formula-not-decoded -->

The normal vector N 1 must satisfy the three following conditions:

<!-- formula-not-decoded -->

From the three conditions, one can deduce the following system of equations:

<!-- formula-not-decoded -->

The following intermediate variables are defined:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Then, the coordinates of N 1 can be expressed as follows:

<!-- formula-not-decoded -->

Thus, the normal to plane ( 𝚪 1 ) containing point Pi ,1 has been defined. By proceeding in the same manner, one can also define the coordinates ( x n 2 , y n 2 , z n 2 ) of vector N 2 normal to plane ( 𝚪 2 ) which contains the points Pi ,1 , Pi ,0 , and Pi +1,0 . Notice that point Pi ,1 is located at the intersection between the two planes ( 𝚪 1 ) and ( 𝚪 2 ) , and the vertical plane corresponding to j =1 ( cf., Fig. 6 ) . Thus, its coordinates should verify the following system:

<!-- formula-not-decoded -->

The following intermediate variables are defined:

<!-- formula-not-decoded -->

Finally, the coordinates of point Pi ,1 are given by

<!-- formula-not-decoded -->

The procedure described earlier should be repeated for all the n 𝛉 points of the tunnel face to generate the corresponding n 𝛉 points in the plane j =1 ( cf., Fig. 5 ) . Once the first contour is generated, the same procedure is again applied to generate the points of the plane j =2 from those of plane j =1, and so on up to the plane j = nz .

Since a collapse ( i.e., an active state of stress ) of the soil mass in front of the tunnel face is considered in this paper, the failure mechanism must 'close to itself' as is the case of the failure mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) . When this mechanism closes, some erroneous Pi , j points systematically appear out of the intuitive collapse mechanism in the case of nonoutcropping mechanisms. Those points, which were generated by the numerical algorithm, can not be avoided with the use of the method of generation proposed in this paper. They should be removed to conserve only the points corresponding to the failure surface.

Notice finally that similar to the mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) , the rigid block will or will not intersect the ground surface depending on the 𝛗 and C / D values. In case of outcrop of the failure mechanism at the ground surface, the points generated by the present algorithm and located above the ground surface have also to be removed. The exact intersection points between the failure mechanism and the ground surface are computed here by linear interpolation between the points located directly above and below the ground surface. Fig. 7 shows the layout of the 3D generated one-block mechanism when 𝛗 =15°, C / D =0.2, and 𝛃 =50°.

Fig. 7. Layout of the 3D generated one-block mechanism in case of outcrop at the ground surface: ( a ) view in the ( x , y , z ) space; ( b ) plan view

<!-- image -->

Engineering drawing

## Improved Multiblock Mechanism Mn

The improved one-block mechanism described before does not offer a great degree of freedom since it is characterized by only a single angular parameter. In order to get better solutions of the collapse pressure, efforts were concentrated in this section on the improvement of the preceding one-block mechanism M1 by increasing the number of blocks. Thus, a multiblock failure mechanism Mn is suggested hereafter. Notice that the idea of a multiblock failure mechanism was first introduced by Michalowski ( 1997 ) and Soubra ( 1999 ) when dealing with the two-dimensional analysis of the bearing capacity of strip foundations and then by Soubra and Regenass ( 2000 ) , Michalowski ( 2001 ) , and Mollon et al. ( 2009 ) for the analysis of some stability problems in three dimensions. It was shown by these writers that a multiblock mechanism significantly improves the solutions given by the traditional two-block and logsandwich mechanisms in the case of a ponderable soil. This is due to the great freedom offered by this mechanism to move more freely with respect to the traditional mechanisms. The three-dimensional multiblock failure mechanism presented in this paper makes use of the idea of a multiblock mechanism suggested by Mollon et al. ( 2009 ) in order to obtain greater ( i.e., better ) solutions. A detailed description of this mechanism is as follows.

As mentioned before, the failure surface of the improved oneblock mechanism was generated from the circular tunnel face, but it can also be generated from any arbitrarily section since the surface is generated from the discretized contour of the tunnel face and not from its analytical expression. Consequently, it is possible to add a second block above the first block ( cf., Fig. 8 ) . Thus, the first block called 'Block 1' adjacent to the tunnel face is truncated with a plane named 'Plane 1' inclined at an angle 𝛂 2

with the vertical direction. The area resulting from this intersection ( which has a nonstandard shape ) is used to generate the second block called 'Block 2' whose axis is inclined at 𝛃 2 with the horizontal direction. Thus, Block 2 is defined by two angular parameters 𝛂 2 and 𝛃 2 . Notice also that Block 1 is defined by only one angular parameter 𝛃 1 which is the inclination of the axis of Block 1. One can see from Fig. 8 that Block 2 moves as a rigid body with velocity V 2 inclined at 𝛃 2 with the horizontal. The velocity of the first block is now denoted V 1 and it is inclined at 𝛃 1 with the horizontal.

The numerical implementation of the geometrical construction of Block 2 consists in determining the intersection points of the lateral surface of the first block with Plane 1 defined by 𝛂 2 . The process is similar to that of the ground surface, i.e., the points located above Plane 1 are deleted, and the exact intersection points are calculated by linear interpolation. These intersection points ( cf., Fig. 9 ) located on the contact area between adjacent blocks are used for the generation of the second block, using exactly the same equations as those for the first block except the fact that these equations are now used in the local axes related to the contact plane separating both blocks. Notice that the tentative ( i.e., nonoptimal ) failure surface shown in Fig. 9 corresponds to the case where 𝛗 =17°, C / D &gt; 0.8, 𝛃 1 =40°, 𝛃 2 =75°, and 𝛂 2 =60°.

Notice finally that the geometrical procedure of construction of an additional block described earlier is successively applied to generate the multiblock mechanism. This mechanism is entirely defined by the 2 n -1 as yet unspecified angular parameters 𝛂 k ( k =2, ... , n ) and 𝛃 l ( l = 1 , . . . , n ) where n is the number of blocks of the failure mechanism.

Fig. 8. Cross section of a two-block mechanism in the ( y , z ) plane

<!-- image -->

Engineering drawing

Fig. 9. Principle of generation of the second upper block

<!-- image -->

Engineering drawing

## Work Equation

The work equation is written here for the general case of a multiblock failure mechanism and for a frictional and cohesive ( 𝛗 , c ) soil. This mechanism is a translational kinematically admissible failure mechanism. The different truncated rigid blocks involved in this mechanism move as rigid bodies. These blocks translate with velocities of different directions, which are collinear with the blocks axes and make an angle 𝛗 with the lateral discontinuity surfaces in order to respect the normality condition required by the limit analysis theory. The velocity of each block is determined by the condition that the relative velocity between the blocks in contact has the direction that makes an angle 𝛗 with the contact surface. The velocity hodograph is given in Fig. 10. The velocity v i +1 of block i +1 and the interblock velocity v i , i +1 between blocks i and i +1 are determined from the velocity hodograph as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

It can be easily shown that v i and v i , i +1 are given by

<!-- formula-not-decoded -->

Fig. 10. Velocity hodograph between two successive blocks

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

Notice that the external forces involved in the present mechanism are the weights of the different truncated rigid blocks, the surcharge loading acting on the ground surface, and the collapse pressure of the tunnel face. The rate of external work of the surcharge loading should be calculated only in case of outcrop of the mechanism at the ground surface. The computation of the rate of external work of the different external forces is straightforward as follows:

- Rate of work of the weight of the different truncated blocks

<!-- formula-not-decoded -->

- Rate of work of a possible uniform surcharge loading on the ground surface

<!-- formula-not-decoded -->

- Rate of work of the collapse pressure of the tunnel face

<!-- formula-not-decoded -->

where Vi =volume of block i ; A n ′ =possible area of intersection of the last upper block with the ground surface ( if the mechanism outcrops ) ; and A 0 =surface of the tunnel face.

Since no general plastic deformation of the truncated blocks is permitted to occur, the rate of internal energy dissipation takes place only along the different velocity discontinuity surfaces. These are ( 1 ) the radial surfaces which are the contact areas between adjacent truncated blocks; ( 2 ) the lateral surfaces of the different truncated blocks. Notice that the rate of internal energy dissipation along a unit velocity discontinuity surface is equal to c · 𝛅 u ( Chen 1975 ) where 𝛅 u is the tangential component of the velocity along the velocity discontinuity surface. Calculation of the rate of internal energy dissipation along the different velocity discontinuity surfaces is straightforward. It is given by

<!-- formula-not-decoded -->

where Si =lateral surface of block i and Ai , i +1 =contact area between blocks i and i +1. Details on the computation of the volumes and surfaces are given in Appendix. The work equation consists in equating the rate of work of external forces to the rate of internal energy dissipation. It is given as follows:

Table 1. Influence of the Number of Blocks on the Critical Collapse Pressure: ( a ) Purely Cohesive Soils; ( b ) Cohesionless soils; and ( c ) Frictional and Cohesive Soils

|                                     | ( a ) Purely cohesive soils         | ( a ) Purely cohesive soils         | ( a ) Purely cohesive soils         | ( a ) Purely cohesive soils         |
|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|
|                                     | c =20 kPa, 𝛗 =0°                    | c =20 kPa, 𝛗 =0°                    | c =30 kPa , 𝛗 =0°                   | c =30 kPa , 𝛗 =0°                   |
| Number of blocks                    | Collapse pressure ( kPa )           | Improvement ( % )                   | Collapse pressure ( kPa )           | Improvement ( % )                   |
| 1                                   | 67.35                               |                                     | stable                              |                                     |
| 2                                   | 105.84                              | 57.1                                | 23.92                               |                                     |
| 3                                   | 107.86                              | 1.9                                 | 26.93                               | 12.6                                |
| 4                                   | 108.32                              | 0.4                                 | 27.59                               | 2.5                                 |
| 5                                   | 108.43                              | 0.1                                 | 27.80                               | 0.8                                 |
| ( b ) Cohesionless soils            | ( b ) Cohesionless soils            | ( b ) Cohesionless soils            | ( b ) Cohesionless soils            | ( b ) Cohesionless soils            |
|                                     | c =0 kPa, 𝛗 =20°                    | c =0 kPa, 𝛗 =20°                    | c =0 kPa, 𝛗 =40°                    | c =0 kPa, 𝛗 =40°                    |
| Number of blocks                    | Collapse pressure ( kPa )           | Improvement ( % )                   | Collapse pressure ( kPa )           | Improvement ( % )                   |
| 1                                   | 41.39                               |                                     | 13.15                               |                                     |
| 2                                   | 44.64                               | 7.9                                 | 13.45                               | 2.3                                 |
| 3                                   | 45.27                               | 1.4                                 | 13.48                               | 0.2                                 |
| 4                                   | 45.31                               | 0.1                                 | 13.49                               | 0.0                                 |
| 5                                   | 45.34                               | 0.1                                 | 13.50                               | 0.1                                 |
| ( c ) Frictional and cohesive soils | ( c ) Frictional and cohesive soils | ( c ) Frictional and cohesive soils | ( c ) Frictional and cohesive soils | ( c ) Frictional and cohesive soils |
| c =7 kPa, 𝛗 =17°                    | c =7 kPa, 𝛗 =17°                    | c =7 kPa, 𝛗 =17°                    | c =10 kPa, 𝛗 =25°                   | c =10 kPa, 𝛗 =25°                   |
| Number of blocks                    | Collapse pressure ( kPa )           | Improvement ( % )                   | Collapse pressure ( kPa )           | Improvement ( % )                   |
| 1                                   | 28.01                               |                                     | 8.90                                |                                     |
| 2                                   | 33.38                               | 19.2                                | 10.51                               | 18.1                                |
| 3                                   | 34.26                               | 2.6                                 | 10.76                               | 2.4                                 |
| 4                                   | 34.42                               | 0.5                                 | 10.87                               | 1.0                                 |
| 5                                   | 34.48                               | 0.2                                 | 10.88                               | 0.1                                 |

<!-- formula-not-decoded -->

After some simplifications, it is found that the tunnel collapse pressure is given by

<!-- formula-not-decoded -->

where N 𝛄 , Nc , and Ns are nondimensional coefficients. They represent, respectively, the effect of soil weight, cohesion, and surcharge loading. The expressions of the different coefficients N 𝛄 , Nc , and Ns are given as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

In Eq. ( 20 ) , 𝛔 c depends not only on the physical, mechanical and geometrical characteristics 𝛄 , c , 𝛗 , and C / D , but also on the

2 n -1 angular parameters 𝛂 k ( k =2, ... , n ) and 𝛃 l ( l =1, ... , n ) . In the following sections, the critical tunnel collapse pressure is obtained by maximization of 𝛔 c given by Eq. ( 20 ) with respect to the 𝛂 k ( k =2, ... , n ) and 𝛃 l ( l =1, ... , n ) angles.

## Numerical Results

A computer program has been written in Matlab language to define the different coefficients N 𝛄 , Nc , and Ns and the tunnel face collapse pressure 𝛔 c using Eqs. ( 20 ) - ( 23 ) . The maximization of the collapse pressure 𝛔 c with respect to the angular parameters of the failure mechanism was performed using the optimization tool implemented in Matlab. The number of subdivisions used for the generation of the collapse mechanism were n 𝛉 =180 and nz =200. These values are optimal and represent a good compromise between results accuracy and computation time. The increase in the number of subdivisions with respect to the aforementioned values slightly improves the obtained results, the difference being smaller than 0.1%. The CPU time necessary for the computation of the critical collapse pressure was about 5-10 min on a 2.4 GHz quad-core CPU.

## Influence of the Number of Blocks

Table 1 gives the values of the critical collapse pressure 𝛔 c obtained from the maximization of the tunnel pressure with respect to the angular parameters of the failure mechanism for three different types of soil: ( 1 ) a purely cohesive soil with c u =20 and 30 kPa; ( 2 ) a cohesionless soil with 𝛗 =20° and 40° ( i.e., a loose and a dense sand, respectively ) ; and ( 3 ) a frictional and cohesive soil with c =7 kPa and 𝛗 =17° ( i.e., a soft clay ) and with c =10 kPa and 𝛗 =25° ( i.e., a stiff clay ) . The computation is made in the case where 𝛄 =18 kN / m 3 and C / D =1. The results are given for different numbers of the rigid blocks varying from one to five. This table also gives the percent increase ( i.e., improvement ) in the collapse pressure with the increase in the number of blocks. The percent improvement corresponding to a given number n of blocks is computed with reference to the mechanism with n -1 blocks. From Table 1, it can be seen that the increase ( i.e., improvement ) in the collapse pressure decreases with the number of blocks increase and is smaller than 2.5% for n =4. Therefore, in the following, the three-block mechanism will be used to obtain the collapse pressure for the different types of soil considered in the paper. This mechanism is defined by five angular parameters ( 𝛂 2 , 𝛂 3 , 𝛃 1 , 𝛃 2 , and 𝛃 3 ) . Finally, it should be noticed that the one-block mechanism would be adequate only in the case of a cohesionless soil and for great values of the friction angle ( for example 𝛗 =40° ) . This is because the increase in the number of blocks slightly improves the solution in that case. Notice however that the improvement obtained by the use of a multiblock mechanism is significant for all the other cases; it is maximal in the case of a purely cohesive soil. For instance, when using two rigid blocks instead of one, an improvement of 57% was obtained in the case of a purely cohesive soil when c u =20 kPa.

Table 2. Numerical Results for the Nondimensional Coefficients N 𝛄 , Nc , and Ns : ( a ) Values of N 𝛄 ; ( b ) Values of Nc ; and ( c ) Values of Ns

| 𝛗                   | C / D               | C / D               | C / D               | C / D               | C / D               | C / D               | C / D               |
|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|
| ( degrees )         | 0.4                 | 0.6                 | 0.8                 | 1                   | 1.3                 | 1.6                 | 2                   |
| ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 | ( a ) Values of N 𝛄 |
| 15                  | 0.346               | 0.365               | 0.374               | 0.378               | 0.378               | 0.378               | 0.378               |
| 20                  | 0.247               | 0.251               | 0.252               | 0.252               | 0.252               | 0.252               | 0.252               |
| 25                  | 0.179               | 0.179               | 0.179               | 0.179               | 0.179               | 0.179               | 0.179               |
| 30                  | 0.132               | 0.132               | 0.132               | 0.132               | 0.132               | 0.132               | 0.132               |
| 35                  | 0.099               | 0.099               | 0.099               | 0.099               | 0.099               | 0.099               | 0.099               |
| 40                  | 0.075               | 0.075               | 0.075               | 0.075               | 0.075               | 0.075               | 0.075               |
| ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c | ( b ) Values of N c |
| 15                  | 3.172               | 3.399               | 3.558               | 3.708               | 3.731               | 3.731               | 3.731               |
| 20                  | 2.601               | 2.704               | 2.744               | 2.744               | 2.744               | 2.744               | 2.744               |
| 25                  | 2.141               | 2.141               | 2.141               | 2.141               | 2.141               | 2.141               | 2.141               |
| 30                  | 1.732               | 1.732               | 1.732               | 1.732               | 1.732               | 1.732               | 1.732               |
| 35                  | 1.428               | 1.428               | 1.428               | 1.428               | 1.428               | 1.428               | 1.428               |
| 40                  | 1.191               | 1.191               | 1.191               | 1.191               | 1.191               | 1.191               | 1.191               |
| ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s | ( c ) Values of N s |
| 15                  | 0.150               | 0.089               | 0.047               | 0.006               | 0                   | 0                   | 0                   |
| 20                  | 0.053               | 0.016               | 0                   | 0                   | 0                   | 0                   | 0                   |
| 25                  | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   |
| 30                  | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   |
| 35                  | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   |
| 40                  | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   | 0                   |

## Analysis of the Face Stability by the Superposition Method

Table 2 provides the critical values of N 𝛄 , Nc , and Ns for different values of C / D and 𝛗 as given by individual maximization of each coefficient with respect to the five angular parameters of the failure mechanism. The critical values of N 𝛄 , Nc , and Ns allow a quick calculation of the critical collapse pressure for practical purposes. This can be performed by simple application of Eq. ( 20 ) using the superposition principle. Notice that while the values of the critical coefficients N 𝛄 , Nc , and Ns and the critical collapse pressure 𝛔 c obtained by maximization are rigorous solutions in limit analysis, the collapse pressure 𝛔 c computed using the superposition method is not a rigorous solution since it is approximately calculated and it includes an error due to the superposition effect. In order to evaluate this error, Table 3 gives the values of the collapse pressures as obtained ( 1 ) by direct maximization of this pressure; ( 2 ) by application of Eq. ( 20 ) using the critical N 𝛄 , Nc , and Ns coefficients presented in Table 2, for the two cases of soft and stiff clays given before when C / D =1, and 𝛄 =18 kN / m 3 . One can observe that the error is quite small ( smaller than 0.5% ) and is always conservative. From Table 2, one can observe that the values of Nc and Ns found by numerical optimization verify the following equation:

<!-- formula-not-decoded -->

Table 3. Comparison of the Collapse Pressures as Given by the Superposition Method and by Direct Optimization

| Collapse pressure             |   Soft clay ( c =7 kPa, 𝛗 =17° ) |   Stiff clay ( c =10 kPa, 𝛗 =25° ) |
|-------------------------------|----------------------------------|------------------------------------|
| 𝛔 c ( superposition ) ( kPa ) |                            34.38 |                              10.81 |
| 𝛔 c ( optimization ) ( kPa )  |                            34.26 |                              10.76 |

Fig. 11. Comparison of present load factor N of a purely cohesive soil with that of other writers

<!-- image -->

Line chart

This may be explained by the theorem of corresponding states ( Caquot 1934 ) . Notice that this theorem allows one to compute the coefficient Nc using the coefficient Ns as can be easily seen from Eq. ( 24 ) .

## Collapse Pressures of a Purely Cohesive Soil

As mentioned in the introduction of this paper, the stability analysis of a tunnel face in the case of a purely cohesive soil is governed by the load factor N . It should be remembered here that the load factor N at failure is N = ( 𝛔 s + 𝛄 H - 𝛔 t ) / c u where 𝛔 t = 𝛔 c . Therefore, unlike the collapse pressure parameter 𝛔 c for which a greater value is searched to improve the best existing solutions, one should obtain a smaller value of the parameter N to improve the best solutions of this parameter. From the computed values of the critical collapse pressures 𝛔 c , the present critical load factors corresponding to the failure state ( i.e., 𝛔 t = 𝛔 c ) were plotted versus C / D in Fig. 11. The N values may also be obtained by an alternative and equivalent method by minimizing the N parameter given earlier with respect to the angular parameters of the failure mechanism. The critical values of N calculated based on the model by Mollon et al. ( 2009 ) and those given by Broms and Bennermark ( 1967 ) , Davis et al. ( 1980 ) , Kimura and Mair ( 1981 ) , and Ellstein ( 1986 ) are also given in this figure. Notice that Fig. 11 may be used to check the stability of the tunnel face in a purely cohesive soil in two different ways. Stability is ensured as long as N computed using the applied tunnel pressure 𝛔 t is smaller than the critical value of N deduced from Fig. 11. This check may also be performed by computing the collapse pressure 𝛔 c from the critical N value of Fig. 11 and comparing this pressure to the applied one ( i.e., 𝛔 t ) .

From Fig. 11, it appears that the present critical values of N are smaller ( i.e., better ) than the available solutions by Mollon et al. ( 2009 ) and Davis et al. ( 1980 ) using a kinematical approach. The improvement is equal to 8% with respect to the results by Mollon et al. ( 2009 ) and to 3.5% with respect to the results by Davis et al.

Fig. 12. Comparison of present solutions of 𝛔 c with those of other kinematical approaches for two cases of a cohesionless soil

<!-- image -->

Line chart

( 1980 ) in the case where C / D =2.5. Finally, it appears that a significant scatter exists between the solutions given by the kinematic and static approaches by Davis et al. ( 1980 ) . This may be explained by the simplified stress field used in the static approach of limit analysis. The centrifuge results by Kimura and Mair ( 1981 ) and the results by Ellstein ( 1986 ) show significant differences with the present solutions. The scatter attains 40% when C / D =2. This means that the case of a purely cohesive soil requires further investigations.

## Collapse Pressures of a Cohesionless Soil

The solutions of the critical tunnel face pressure as determined by Leca and Dormieux ( 1990 ) , Mollon et al. ( 2009 ) , and by the present approach are given in Fig. 12 for two cases of a cohesionless soil: 𝛗 =20° and 40°. It should be remembered here that all these results are based on the kinematical approach of limit analysis. One can see that the improvement ( i.e., increase of the collapse pressure ) of the present solution attains 12% with respect to the one by Mollon et al. ( 2009 ) and 19% with respect to that by Leca and Dormieux ( 1990 ) when 𝛗 =20° and C / D &gt; 0.5. This figure also shows that in the common range of variation of 𝛗 ( 𝛗 =20-40° ) , the parameter C / D has no influence on the collapse pressures when C / D is higher than 0.5 ( this geometrical condition is always true in practice ) . This is because the critical failure mechanism obtained from the maximization process is a nonoutcropping mechanism for these cases and it does not change with the increase of C / D .

Fig. 13 presents a comparison between the collapse pressures given by the proposed mechanism and those given by Anagnostou and Kovari ( 1996 ) using a limit equilibrium method, Eisenstein and Ezzeldine ( 1994 ) using a numerical approach, and Leca and Dormieux ( 1990 ) using kinematic and static approaches in limit analysis. Again, one can observe that the solutions obtained by Leca and Dormieux ( 1990 ) using the static approach in limit analysis are quite far from the results given by the other methods. This is because of the simplified stress field used by Leca and Dormieux ( 1990 ) . The present results improve the solutions given by Leca and Dormieux ( 1990 ) using a kinematic approach and are between the results given by Eisenstein and Ezzeldine ( 1994 ) and Anagnostou and Kovari ( 1996 ) .

Fig. 13. Comparison of present solutions of 𝛔 c with those of other writers in the case of a cohesionless soil

<!-- image -->

Line chart

Table 4 presents the collapse pressures obtained by Chambon and Corté ( 1994 ) from centrifuge tests in Nantes LCPC using sand. The ranges of shear strength characteristics given by Chambon and Corté ( 1994 ) are as follows: 𝛗 =38-42°, and c =0-5 kPa. As can be seen, these values of the shear strength parameters show that the soil exhibits a small nonnull cohesion for the sand. Chambon and Corté ( 1994 ) explained this phenomenon by some uncertainty in the measurements of internal friction angle and cohesion obtained from the shear box. Notice that the centrifuge tests were realized for several values of D , C / D , and 𝛄 . Table 4 also presents the corresponding collapse pressures as given by the proposed three-block mechanism, for the four combinations of extreme values of c and 𝛗 suggested by Chambon and Corté ( 1994 ) . In this table, a unique value of the calculated pressure is given for several values of C / D because of the high values of 𝛗 proposed by Chambon and Corté ( the mechanism never outcrops in these cases ) . As one can see, the results obtained by centrifuge tests are within the large range of values of the tunnel pressures computed based on the three-block mechanism using the different values of the soil shear strength parameters. The wide range of values of the shear strength parameters given by Chambon and Corté ( 1989 ) does not allow a fair and accurate comparison with the experimental collapse pressures.

Fig. 14. Comparison of present solutions of 𝛔 c with those of other kinematical approaches for two cases of a frictional and cohesive soil

<!-- image -->

Line chart

## Collapse Pressures of a Frictional and Cohesive Soil

Fig. 14 presents the solutions of the collapse pressure as given by Leca and Dormieux ( 1990 ) , Mollon et al. ( 2009 ) , and by the present approach for two soil configurations: c =7 kPa and 𝛗 =17° ( soft clay ) , and c =10 kPa and 𝛗 =25° ( stiff clay ) . All these results are based on the kinematical approach of limit analysis. For C / D &gt; 0.8, the improvement of the present solution with respect to the one by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) is about 44% and 20%, respectively, for the soft clay, and attains 89% and 40%, respectively, for the stiff clay. For the C / D values higher than 0.8 ( which is almost always true in practice ) , the values of the collapse pressures remain constant. Again, this phenomenon may be explained by the fact that the critical failure mechanism obtained from optimization does not outcrop at the ground surface for these cases.

Table 4. Comparison between Experimental and Computed Collapse Pressures

|           |               |                |         |     | 𝛔 c as given by           | 𝛔 c as given by the proposed three-block mechanism [ kPa ]   | 𝛔 c as given by the proposed three-block mechanism [ kPa ]   | 𝛔 c as given by the proposed three-block mechanism [ kPa ]   | 𝛔 c as given by the proposed three-block mechanism [ kPa ]   |
|-----------|---------------|----------------|---------|-----|---------------------------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|--------------------------------------------------------------|
| c [ kPa ] | 𝛗 [ degrees ] | 𝛄 [ kN / m 3 ] | D [ m ] | C/D | Chambon and Corté [ kPa ] | c =0 kPa, 𝛗 =38°                                             | c =5 kPa, 𝛗 =38°                                             | c =0 kPa, 𝛗 =42°                                             | c =5 kPa, 𝛗 =42°                                             |
| 0-5       | 38-42         | 16.1           | 5       | 0.5 | 3.6                       | 6.8                                                          | 0.4                                                          | 5.3                                                          | Stable                                                       |
|           |               |                |         | 0.5 | 3.5                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 1   | 3.5                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 1   | 3.0                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 1   | 3.3                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 2   | 4.0                       |                                                              |                                                              |                                                              |                                                              |
| 0-5       | 38-42         | 15.3           | 5       | 0.5 | 4.2                       | 6.5                                                          | 0.1                                                          | 5.0                                                          | Stable                                                       |
|           |               |                |         | 1   | 5.5                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 2   | 4.2                       |                                                              |                                                              |                                                              |                                                              |
| 0-5       | 38-42         | 16.0           | 10      | 1   | 7.4                       | 13.6                                                         | 7.1                                                          | 10.5                                                         | 5.0                                                          |
|           |               |                |         | 2   | 8.0                       |                                                              |                                                              |                                                              |                                                              |
|           |               |                |         | 4   | 8.2                       |                                                              |                                                              |                                                              |                                                              |
| 0-5       | 38-42         | 16.2           | 13      | 4   | 13.0                      | 17.9                                                         | 11.4                                                         | 13.8                                                         | 8.3                                                          |

## Critical Collapse Mechanisms

Fig. 15 shows a comparison between the critical failure mechanisms given by Mollon et al. ( 2009 ) and by the present approach in three different cases: ( 1 ) a purely cohesive soil with c u =20 kPa and C / D =1; ( 2 ) a cohesionless soil with 𝛗 =30° and C / D &gt; 0.5 ( case of a nonoutcropping mechanism ) ; and ( 3 ) a soft clay with 𝛗 =17°, c =7 kPa, and C / D &gt; 1. For both approaches, the failure mechanism outcrops in the case of a purely cohesive soil as expected. It means that for this type of soil, the parameter C / D is of major importance. This is not true for a cohesionless or a frictional and cohesive soil with high to moderate friction angle ( 𝛗 =20-40° ) since the critical tunnel pressure is independent of the tunnel cover in these cases. From Fig. 15, one can also see that the critical failure mechanisms given by both approaches are quite similar. Notice however that the prior mechanism by Mollon et al. ( 2009 ) does not intersect the whole tunnel face; the grey part of the tunnel face being at rest in the mechanism by Mollon et al. ( 2009 ) ( cf., Fig. 15 ) . This incompatibility of the mechanism with the tunnel cross section was removed in the method proposed herein. Notice also that the upper block of the present mechanism does not exhibit a unique apex as would appear from Fig. 15. Instead, a curved line was obtained at the top of this block as may be easily seen from Fig. 16. It should be emphasized here that for a small value of the friction angle, the curved line developed at the top of the upper block has a very limited length ( not shown in this paper ) . Thus, the upper block approaches ( but is not ) a regular cone in this case; the lines developed along the j index ( for a given i ) are approximately close to ( but are not ) straight lines. In this case, the last upper block terminates with a somewhat unique apex. Notice however that for greater values of the friction angle, the upper block is far from a regular cone as was shown in Fig. 16 for 𝛗 =30°.

## Design Chart

Fig. 17 depicts a design chart that may be used in practice to determine the critical collapse pressure of a circular tunnel face in the case of a frictional and cohesive soil. This chart allows one to evaluate the nondimensional collapse pressure 𝛔 c / 𝛄 D for different values of c / 𝛄 D and for various values of 𝛗 ( running from 15° to 40° ) when C / D &gt; 0.8 ( the condition C / D &gt; 0.8 is almost always true in practice ) . Notice that the range C / D &gt; 0.8 was chosen because the critical failure mechanism would be a nonoutcropping mechanism in this case for all the range of values of the soil parameters considered in the paper and this renders the chart independent of C / D . Notice finally that this chart may also be used for the computation of the required tunnel face pressure for which a prescribed safety factor Fs defined with respect to the soil shear strength parameters c and tan 𝛗 is desired. This may be achieved if one uses the chart with 𝛗 d and c d in lieu of 𝛗 and c where 𝛗 d and c d are based on the following equations:

Fig. 15. Comparison of the failure mechanisms as given by the present approach ( left ) and by Mollon et al. ( 2009 ) ( after Mollon et al. 2009 ) ( right ) : ( a ) 𝛗 =0° and c u =20 kPa; ( b ) 𝛗 =30° and c =0 kPa; and ( c ) 𝛗 =17° and c =7 kPa

<!-- image -->

Engineering drawing

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## Conclusions

A new multiblock translational failure mechanism based on the kinematical approach of limit analysis theory was presented in this paper in the aim to improve the existing solutions of the critical collapse pressure of a shallow circular tunnel driven by a pressurized shield. The present failure mechanism has a significant advantage with respect to the existing limit analysis mechanisms by Leca and Dormieux ( 1990 ) and Mollon et al. ( 2009 ) since it takes into account the entire circular tunnel face and not only an inscribed ellipse to this circular area. This was made possible by the use of a spatial discretization technique allowing one to generate the three-dimensional failure surface point by point. The three-dimensional failure surface was determined by defining the contours of this surface at several vertical planes parallel to the tunnel face. This failure mechanism respects the normality condition required by limit analysis since the threedimensional failure surface so generated is constructed in such a manner that the velocity vector makes an angle 𝛗 with the velocity discontinuity surfaces anywhere along these surfaces. Although the three-dimensional geometrical construction presented in this paper is applied to a circular tunnel face, it may be easily applied to any form of the tunnel face for the stability analysis of a tunnel driven by the classical methods. The numerical results have shown that:

Fig. 17. Design chart of the critical collapse pressure for a frictional and cohesive soil

<!-- image -->

Line chart

Fig. 16. Shape of the curved line at the top of the upper block of the failure mechanism when 𝛗 =30°

<!-- image -->

Engineering drawing

- A one-block mechanism would be adequate only in the case of a cohesionless soil and for great values of the friction angle ( for example 𝛗 =40° ) . This is because the increase in the number of blocks slightly improves the solution in that case. Notice however that the improvement obtained by the use of a multiblock mechanism is significant for all the other cases; it is maximal in the case of a purely cohesive soil. Finally, it was found that the use of a three-block mechanism gives accurate results for all the types of soils studied in the paper ( frictional and/or cohesive ) with a reasonable computation time of about 5-10 min.
- The critical values of N 𝛄 , Nc , and Ns are given in the paper for the computation of the tunnel collapse pressure using the superposition method. It was shown that the error induced by the superposition principle is quite small ( smaller than 0.5% ) and is always conservative. Notice however that the collapse pressures computed based on the superposition principle can not be considered as rigorous solutions in the framework of limit analysis theory.
- The proposed failure mechanism improves the available solutions of the load factor N and the collapse pressure 𝛔 c . In the case of purely cohesive soils, the improvement ( i.e., decrease ) of the critical value of N with respect to the one by Mollon et al. ( 2009 ) is equal to 8% for C / D =2.5. For cohesionless soils, the improvement ( i.e., increase ) of the critical collapse pressure 𝛔 c with respect to the one given by Mollon et al. ( 2009 ) is equal to 12% when 𝛗 =20°. This improvement can attain more than 40% for stiff clays. The comparison with other theoretical and experimental approaches has shown that a good agreement with other writers' results was obtained in the case of a cohesionless soil. However, significant differences exist with centrifuge tests in the case of a purely cohesive soil. These differences require further investigation.
- The failure mechanism always outcrops in the case of a purely cohesive soil as expected. It means that in this case the parameter C / D is of major importance. This is not the case for a cohesionless or a frictional and cohesive soil with high to moderate friction angle 𝛗 =20-40° since the critical tunnel pressure is independent of the tunnel cover in these cases.
- A design chart was proposed, allowing one to evaluate the critical collapse pressure for a frictional and cohesive soil. This chart may also be used for the computation of the required tunnel face pressure for which a prescribed safety factor Fs defined with respect to the soil shear strength parameters c and tan 𝛗 is desired.

Finally, it should be mentioned that the failure mechanism presented in this paper may be extended to the blow-out case of failure corresponding to the passive state in the soil in front of the tunnel face. This mechanism permits to compute the blow-out face pressures. In this case, the velocities are acting upwards and the failure mechanism always outcrops on the ground surface. Although this state of failure is not realistic in the case of a frictional and cohesive soil, it would be of some interest in the case of a soft clay.

Fig. 18. Principle of the volume and surface computation method

<!-- image -->

Engineering drawing

## Appendix. Volumes and Surfaces Calculation

The calculation of the volume and lateral surface of a given block is performed by a simple summation of elementary volumes and lateral surfaces Vi , j and Si , j associated with the different element areas of the failure surface of this block. This may be explained as follows. For a given element area of the failure surface bounded by four points ( Pi , j , Pi +1, j , Pi , j +1 , and Pi +1, j +1 ) , let ( P i , j ′ , P i +1, j ′ , P i , j +1 ′ , and P i +1, j +1 ′ ) be the projections of these four points on the plane x =0 as shown in Fig. 18. This quadrilateral element area may be subdivided into two triangular facets by two different ways: [( Pi , j ; Pi +1, j ; Pi , j +1 ) and ( Pi +1, j ; Pi , j +1 ; Pi +1, j +1 )] or [( Pi , j ; Pi , j +1 ; Pi +1, j +1 ) and ( Pi , j ; Pi +1, j ; Pi +1, j +1 )] . Those four triangular facets are denoted a , b , c , and d as shown in Fig. 18. In the same manner, the volume bounded by the four points ( Pi , j , Pi +1, j , Pi , j +1 , Pi +1, j +1 ) and their projection on the plane x =0, may be computed by defining four volumes Va , Vb , Vc , and Vd , each one being bounded by the corresponding triangular facet ( a , b , c , or d ) and its projection on the plane x =0. For example, the volume Va is bounded by the six points ( Pi , j ; Pi +1, j ; Pi , j +1 ; P i , j ′ ; P i +1, j ′ ; P i , j +1 ′ ) as shown in Fig. 18. For each one of the triangular facets, it is very easy to determine the surface and the corresponding volume ( which is equal to the projected surface of this triangle on the plane x =0 multiplied by the distance from the barycenter of the triangular facet to the projection plane x =0 ) using the coordinates of the three points of the triangle. The surface ( respectively volume ) of the four-points element is approximated here as the mean value between the surfaces ( respectively, volumes ) obtained from the two ways of subdividing the quadrilateral surface into two triangles, i.e.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Concerning the calculation of the interblock surfaces and of the outcropping surface, this was performed using the classical trapezoidal method.

## References

- Anagnostou, G., and Kovari, K. ( 1996 ) . 'Face stability conditions with earth-pressure-balanced shields.' Tunn. Undergr. Space Technol. , 11 ( 2 ) , 165-173.
- Augarde, C. E., Lyamin, A. V., and Sloan, S. W. ( 2003 ) . 'Stability of an undrained plane strain heading revisited.' Comput. Geotech. , 30, 419-430.
- Broere, W. ( 1998 ) . 'Face stability calculation for a slurry shield in heterogeneous soft soils.' Proc., World Tunnel Congress 98 on Tunnels and Metropolises , Vol. 1, Balkema, Rotterdam, The Netherlands, 215218.
- Broms, B. B., and Bennermark, H. ( 1967 ) . 'Stability of clay at vertical openings.' Soil Mech. Found. Eng. (Engl. Transl.) , 193 ( SM1 ) , 71-94.
- Caquot, A. I. ( 1934 ) . Equilibre des massifs à frottement interne-Stabilité des terres pulvérulents et cohérents , Gauthier-Villars, Paris ( in French ) .
- Chambon, P., and Corté, J. F. ( 1994 ) . 'Shallow tunnels in cohesionless soil: Stability of tunnel face.' J. Geotech. Eng. , 120 ( 7 ) , 1148-1165.
- Chen, W. F. ( 1975 ) . Limit analysis and soil plasticity , Elsevier Science, Amsterdam, The Netherlands.
- Davis, E. H., Gunn, M. J., Mair, R. J., and Seneviratne, H. N. ( 1980 ) . 'The stability of shallow tunnels and underground openings in cohesive material.' Geotechnique , 30 ( 4 ) , 397-416.
- Eisenstein, A. R., and Ezzeldine, O. ( 1994 ) . 'The role of face pressure for shields with positive ground control.' Tunneling and ground conditions , Balkema, Rotterdam, The Netherlands, 557-571.
- Ellstein, A.R. ( 1986 ) . 'Heading failure of lined tunnels in soft soils.' Tunnels and tunnelling , 18, 51-54.
- Horn, N. ( 1961 ) . 'Horizontaler erddruck auf senkrechte abschlussflächen von tunnelröhren.' Landeskonferenz der ungarischen tiefbauindustrie , Landeskonferenz der Ungarischen Tiefbauindustrie, Budapest, Hungary, 7-16.
- Kimura, T., and Mair, R. J. ( 1981 ) . 'Centrifugal testing of model tunnels in clay.' Proc., 10th Int. Conf. of Soil Mechanics and Foundation Engineering , Vol. 1, Balkema, Rotterdam, The Netherlands, 319-322.
- Klar, A., Osman, A. S., and Bolton, M. ( 2007 ) . '2D and 3D upper bound solutions for tunnel excavation using 'elastic' flow fields.' Int. J. Numer. Analyt. Meth. Geomech. , 31 ( 12 ) , 1367-1374.
- Leca, E., and Dormieux, L. ( 1990 ) . 'Upper and lower bound solutions for the face stability of shallow circular tunnels in frictional material.' Geotechnique , 40 ( 4 ) , 581-606.
- Mair, R. J. ( 1979 ) . 'Centrifugal modelling of tunnel construction in soft clay.' Ph.D. thesis, Univ. of Cambridge, Cambridge, U.K.
- Michalowski, R. L. ( 1997 ) . 'An estimate of the influence of soil weight on bearing capacity using limit analysis.' Soils Found. , 37 ( 4 ) , 57-64.
- Michalowski, R. L. ( 2001 ) . 'Upper-bound load estimates on square and rectangular footings.' Geotechnique , 51 ( 9 ) , 787-798.
- Mollon, G., Dias, D., and Soubra, A.-H. ( 2009 ) . 'Probabilistic analysis and design of circular tunnels against face stability.' Int. J. Geomech. , 9 ( 6 ) , 237-249.
- Oberlé, S. ( 1996 ) . 'Application de la méthode cinématique à l'étude de la

stabilité d'un front de taille de tunnel.' Final project , ENSAIS, France ( in French ) .

- Osman, A. S., Mair, R. J., and Bolton, M. D. ( 2006 ) . 'On the kinematics of 2D tunnel collapse in undrained clay.' Geotechnique , 56 ( 9 ) , 585595.
- Sagaseta, C. ( 1987 ) . 'Analysis of undrained soil deformation due to ground loss.' Geotechnique , 37 ( 3 ) , 301-320.
- Soubra, A.-H. ( 1999 ) . 'Upper-bound solutions for bearing capacity of foundations.' J. Geotech. Geoenviron. Eng. , 125 ( 1 ) , 59-68.
- Soubra, A.-H., and Regenass, P. ( 2000 ) . 'Three-dimensional passive earth

pressures by kinematical approach.' J. Geotech. Geoenviron. Eng. , 126 ( 11 ) , 969-978.

- Takano, D., Otani, J., Nagatani, H., and Mukunoki, T. ( 2006 ) . 'Application of X-ray CT boundary value problems in geotechnical engineering-Research on tunnel face failure.' Proc., Geocongress 2006 , ASCE, Reston, Va.
- Verruijt, A., and Booker, J. R. ( 1996 ) . 'Surface settlements due to deformation of a tunnel in an elastic half plane.' Geotechnique , 46 ( 4 ) , 753-756.