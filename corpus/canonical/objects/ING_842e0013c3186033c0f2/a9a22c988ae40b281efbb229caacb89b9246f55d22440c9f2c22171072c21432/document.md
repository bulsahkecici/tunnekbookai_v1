<!-- image -->

Logo

Article

## AGeometric Model for a Shield TBM Steering Simulator

<!-- image -->

Icon

Byungkwan Park 1 , Soon-Wook Choi 2 , Chulho Lee 2 , Tae-Ho Kang 2 , Seungchul Do 3 , Woon-Yong Lee 3 and Soo-Ho Chang 2, *

<!-- image -->

Icon

<!-- image -->

Icon

- 1 R&amp;D Team, Kangnung Construction Co., Ltd., Seoul 05578, Republic of Korea; pbk4829@gyeongdo.co.kr
- 2 Department of Geotechnical Engineering Research, Korea Institute of Civil Engineering and Building Technology, Goyang 10223, Republic of Korea; soonugi@kict.re.kr (S.-W.C.); chlee@kict.re.kr (C.L.); thkang@kict.re.kr (T.-H.K.)
- 3 DOONAInformation &amp; Technology Co., Ltd., Incheon 22106, Republic of Korea; scdo@doonaint.com (S.D.); web@doonaint.com (W.-Y.L.)
* Correspondence: sooho@kict.re.kr; Tel.: +82-31-910-0661

Abstract: This study aimed to simulate curved excavation using a tunnel boring machine (TBM) steering system based on the proposed mathematical methodology applied in a TBM simulator. We introduce the concept and mechanism of the TBM steering system and describe the mathematical formulae used for simulating curved excavation. Curved excavation in the top- right direction was simulated using a Python program to verify the mathematical formulae. In addition, Python simulations were undertaken to determine the effects of horizontal and vertical articulation angles on pitching and yawing angles. Finally, the proposed mathematical formulae were applied in the TBM operation simulator, and tested based on the mechanism of the TBM steering system.

Keywords: curved excavation; articulation jack; TBM steering system; shield jack; TBM simulator

## 1. Introduction

There are two main types of tunnel excavation: conventional tunneling by drilling and tunnel boring machines (TBMs), which are widely used in urban tunnels where rapid excavation is required with high safety standards. As there are many underground structures within a city, such as utility tunnels and building foundations, new tunnels are often a combination of straight and curved alignments. Therefore, TBM steering systems are critical in successfully producing tunnel curves.

Sugimoto and Sramoon [1] presented a theoretical model for TBM excavation based on the dynamic loading concept with which they simulated TBM operation, evaluated shield behavior, and undertook sensitivity analysis of the model parameters used for shield behavior in both straight and curved line excavations. Based on the simulation, they confirmed that shield movement could be affected by ground properties, with the influence on shield behavior being more marked in curved excavation than in straight line excavation.

Shen et al. [2,3] introduced geometrical and mathematical models to determine the three-dimensional orientations of a TBM during its advance, and they derived a transformation matrix to calculate the attitude of TBM position in terms of yaw, pitch, and roll as the coordinates of one tracking point of TBM position during advance.

Chanchaya and Suwansawat [4] introduced three operational factors (articulation angle, shield jack length difference, and copy cutter stroke) that are necessary for curved excavation and derived calculation methods for those factors and methods for forming curved alignments, including circular and spiral curves in two-dimensional space. They also compared three operational factors obtained from theoretical calculations with those measured in a real guidance system.

Festa et al. [5] and Festa et al. [6] described the kinematic behavior of a TBM in soft ground, defining TBM shield position and orientation with two reference points

<!-- image -->

Icon

<!-- image -->

Logo

Citation: Park, B.; Choi, S.-W.; Lee, C.; Kang, T.-H.; Do, S.; Lee, W.-Y.; Chang, S.-H. A Geometric Model for a Shield TBM Steering Simulator. Appl. Sci. 2023 , 13 , 10087. https://doi.org/ 10.3390/app131810087

Academic Editor: Mark J. Jackson

Received: 29 June 2023 Revised: 4 September 2023 Accepted: 6 September 2023 Published: 7 September 2023

<!-- image -->

Icon

Copyright: © 2023 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https:// creativecommons.org/licenses/by/ 4.0/).

<!-- image -->

Logo

and introducing the horizontal and vertical tendencies of the TBM calculated from the deviations of two reference points caused by the yaw and pitch of the shield. Based on these tendencies, they compared the relative positioning of the TBM with its planned tunnel alignments.

Kang et al. [7] undertook a numerical simulation to evaluate the structural stability of the TBM shield during a tightly curved excavation, identifying the load transfer mechanism from articulation and shield jacks to the shield skin and the effect of load transfer on the structural stability of the shield skin.

Kang et al. [8] developed a 1:17.7 scale model experiment to describe the behavior of thrust pressure based on different shield jacking force systems and articulation angles for curved excavation. Considering the uneven pressure, they proposed a guideline for the distribution of thrust force depending on articulation angle.

Recently, Brundan and Danno [9] described the overall TBM steering system and the related procedure required for tightly curved excavation, and they presented field case histories of TBM design and operational technology recognized as being successful in extremely tight curved excavation.

These previous studies highlight limitations in designing the steering system for the TBM simulator. Sugimoto and Sramoon [1] presented various factors related to shield behavior; Chanchaya and Suwansawat [4] introduced operational factors for TBM curved excavation, and the TBM navigation system (the critical part of the steering system) was partially covered in both studies. Shen et al. [2,3] suggested determining the TBM position and its deviation caused by pitch, yaw, and roll, but considered only one reference point when calculating TBM position, whereas at least three reference points must be considered for a navigation system in three-dimensional space. Festa et al. [5,6] considered two reference points (front and rear) to calculate horizontal and vertical tendencies. However, the navigation system was considered in two-dimensional space. Further studies have also aided the understanding of the overall TBM steering system [7-9].

As the excavation performance of TBMs depends heavily on the competence of their operators, TBM operator training is an issue of growing importance. Therefore, a few global leading research institutions in the TBM industry have recently developed the TBM simulators for operator training [10]. As part of the research project for developing the TBM steering simulator, this study aimed to derive a geometrical model for TBM steering simulation in curved excavation. We first considered the concept and mechanism of the TBM steering system, before deriving mathematical formulae for simulation based on the steering mechanism, including articulation and shield jack operations. Curved excavations were simulated using a Python program to verify the mathematical formulae. Simulations of different cases were undertaken to identify the effects of two articulation angles and two rotation angles on horizontal and vertical tendency. The proposed formulae were applied to a real TBM simulation of articulation operations.

## 2. Overview of the TBM Steering System for Curved Excavation

Thrust and articulation jacks are used for TBM steering. For straight or almost straight excavation, only the thrust jack can be used, with the jacks being extended simultaneously at the same rate, allowing the TBM to move forward. However, if the tunnel alignment comprises a straight line with a tightly curved line, both thrust and articulation jacks are used together, depending on tunnel line conditions. In this case, the articulation jacks change according to a predetermined articulation angle before the thrust jacks are extended.

Curved excavation with a TBM steering system generally includes several operations, i.e., a copy cutter, an articulation jack, and shield jack operation. The first overcutting secures adequate room for curved excavation, then the articulation jacks are extended to steer the front shield with the cutterhead in the target direction. Finally, the extension of the shield jacks moves the TBM forward. Copy cutter operation was not considered in this study, and operations in curved excavation are repeatedly executed as follows:

1. Extension of articulation jacks to the target articulation angle;

3 of 27 of the shield jacks moves the TBM forward. Copy cu tt er operation was not considered in

## this study, and operations in curved excavation are repeatedly executed as follows:

1. Extension of articulation jacks to the target articulation angle;
2. Extension of shield jacks to the segment width; 2. Extension of shield jacks to the segment width;
4. Return of shield jacks to the original position; 4. Return of shield jacks to the original position;
3. Return of articulation jacks to the original position; 3. Return of articulation jacks to the original position;
5. Installation of segment ring; 5. Installation of segment ring;
6. Repetition of step 1. 6. Repetition of step 1.

Shield jack extension differences, by one-sided extension and the use of tapered segments, are required for successful curved excavation [4]. Here, we assumed that the shield jacks are extended equally, simultaneously, and at the same rate. Shield jack extension differences, by one-sided extension and the use of tapered segments, are required for successful curved excavation [4]. Here, we assumed that the shield jacks are extended equally, simultaneously, and at the same rate.

There are two types of articulation systems: the 'V' and 'X' types, with the main difference between them being the location of the articulation point. In the V-type system, articulation jacks are extended in the opposite direction to that of the curve, with the articulation point being located opposite the extended jack. The X-type system involves the extension and retraction of the articulation jack simultaneously during articulation, with the articulation point always being at the center of the shield (Figure 1a). There are two types of articulation systems: the 'V' and 'X' types, with the main difference between them being the location of the articulation point. In the V-type system, articulation jacks are extended in the opposite direction to that of the curve, with the articulation point being located opposite the extended jack. The X-type system involves the extension and retraction of the articulation jack simultaneously during articulation, with the articulation point always being at the center of the shield (Figure 1a).

<!-- image -->

Engineering drawing

Figure 1. Two types of steering system (modified from Kang et al. [7]): ( a ) articulation system; ( b ) thrust system. Figure 1. Two types of steering system (modified from Kang et al. [7]): ( a ) articulation system; ( b ) thrust system.

In the X-type, a rotation pin is located at the articulation point to connect the front and middle shields. Because the pin is on the articulation point, it is possible to maintain the gap between both shields during articulation, with this being suitable for articulation sealing and water-resistance during articulation, although fewer articulation angles can be controlled than with the V-type. In the V-type system, the articulation point is on the shield skin plate during articulation. As there are no connected pins in the system, it is easy to rotate through any articulation angle in any direction. However, as the articulation angle increases, the gaps between shields also increase and it is difficult to prevent the inflow of muck and water during articulation [7-9]. As shown in Figure 1b, there are two types of thrust system: reaction force at the front shield and reaction force at the middle and tail shields. The la tt er is generally more appropriate for curved excavation; it can supply a constant thrust force to the segment ring without eccentric force, regardless of the rotation of the front shield [7-9]. In the X-type, a rotation pin is located at the articulation point to connect the front and middle shields. Because the pin is on the articulation point, it is possible to maintain the gap between both shields during articulation, with this being suitable for articulation sealing and water-resistance during articulation, although fewer articulation angles can be controlled than with the V-type. In the V-type system, the articulation point is on the shield skin plate during articulation. As there are no connected pins in the system, it is easy to rotate through any articulation angle in any direction. However, as the articulation angle increases, the gaps between shields also increase and it is difficult to prevent the inflow of muck and water during articulation [7-9]. As shown in Figure 1b, there are two types of thrust system: reaction force at the front shield and reaction force at the middle and tail shields. The latter is generally more appropriate for curved excavation; it can supply a constant thrust force to the segment ring without eccentric force, regardless of the rotation of the front shield [7-9].

In three-dimensional space, at least three reference points should be used for TBM positioning systems to report TBM behavior during its advance. The front reference point In three-dimensional space, at least three reference points should be used for TBM positioning systems to report TBM behavior during its advance. The front reference point is located on the plane of the shield face, and the rear left and rear right points are on the rear of both sides, on the plane of the shield face (Figure 2).

TBM operators attempt to follow the planned alignment by monitoring reference points. Owing to ground properties and machine weight, pitch, yaw, and roll rotations are inevitably generated during TBM advance (Figure 3a). Pitching means that the direction of shield advance deviates up or down, causing vertical deviations (Figure 3b). Yawing means Appl. Sci. 2023 , 13 , x FOR PEER REVIEW

that the direction deviates right or left, leading to horizontal deviation (Figure 3c). Rolling means the tendency of the shield body to rotate in the reverse direction to the cutterhead rotation (Figure 3d). When pitch and yaw occur, tail clearance is not assured between the shield machine and the segments. This should be corrected by extending a group of shield jacks (depending on the rotation direction) before they exceed the maximum value. If rolling occurs, the discharged soil will not be well loaded onto the conveyor, causing muck discharge problems. This also causes excessive load to be applied to the screw conveyor or segment ring, leading to failure. Rolling should also be corrected by rotating the cutterhead in the rolling direction before it exceeds its maximum value. 4  of  29 is located on the plane of the shield face, and the rear left and rear right points are on the rear of both sides, on the plane of the shield face (Figure 2).

Appl. Sci. 2023 , 13 , x FOR PEER REVIEW

5  of  29

Figure 2. TBM steering system with TBM position. Figure 2. TBM steering system with TBM position.

<!-- image -->

Engineering drawing

Figure 3. Three rotation angles (modified from Shen et al. [2,3]): ( a ) three rotations; ( b ) yaw; ( c ) pitch; ( d ) roll. Figure 3. Three rotation angles (modified from Shen et al. [2,3]): ( a ) three rotations; ( b ) yaw; ( c ) pitch; ( d ) roll.

<!-- image -->

Engineering drawing

## 3. Geometrical Model for Curved Excavation

## 3.1. Creation of Planned Route

In an excavation simulation, the route is planned first, with the TBM tunnel alignment involving a straight line and a curved line, with parallel rings being used for the

## 3. Geometrical Model for Curved Excavation

## 3.1. Creation of Planned Route

In an excavation simulation, the route is planned first, with the TBM tunnel alignment involving a straight line and a curved line, with parallel rings being used for the straight line excavation and left or right tapered segments for the curved excavation [11]. It is assumed that each tracking point is located at the center of the cross section of each segment ring. Based on this concept (Figure 4), the mathematical model for the curved line is as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where i is ring number; T i x is the i th term of the tracking point (segment ring) on the x coordinate; T i y is the i th term of the tracking point on the y coordinate; T i z is i th term of the tracking point on the z coordinate; ai is the horizontal angle on the x-y plane at position i ; bi is the vertical angle on the y-z plane at position i ; and dr is the average width of tapered segment rings. Appl. Sci. 2023 , 13 , x FOR PEER REVIEW 6  of  29

Figure 4. Example of a planned route in the vertical direction. Figure 4. Example of a planned route in the vertical direction.

<!-- image -->

Geographical map

## 3.2. Calculation of TBM Position Change by Articulation Jack Operation 3.2. Calculation of TBM Position Change by Articulation Jack Operation

In a curved excavation, articulation jacks are extended first to steer the front shield. Once the direction is set, shield jacks are extended to move the TBM forward in the target alignment. Several assumptions are involved in the calculation of reference points: the four articulation jacks (upper, lower, left, and right) are arranged in a circular array; the distance between each jack position and the center equals the shield radius (Figure 5); the distance between both rear reference points equals the shield diameter; and the distance between the reference points at the rear and front equals the length of the front shield (Figure 2). In a curved excavation, articulation jacks are extended first to steer the front shield. Once the direction is set, shield jacks are extended to move the TBM forward in the target alignment. Several assumptions are involved in the calculation of reference points: the four articulation jacks (upper, lower, left, and right) are arranged in a circular array; the distance between each jack position and the center equals the shield radius (Figure 5); the distance between both rear reference points equals the shield diameter; and the distance between the reference points at the rear and front equals the length of the front shield (Figure 2).

## 3.2.1. Articulation Jack Operation in the X-Type System

The X-type articulation system is shown in Figure 6. The articulation jack in the target direction is retracted, while the others are extended simultaneously. If the intention is to

<!-- image -->

Line chart

## 3.2. Calculation of TBM Position Change by Articulation Jack Operation

In a curved excavation, articulation jacks are extended first to steer the front shield. Once the direction is set, shield jacks are extended to move the TBM forward in the target alignment. Several assumptions are involved in the calculation of reference points: the

four articulation jacks (upper, lower, left, and right) are arranged in a circular array; the distance between each jack position and the center equals the shield radius (Figure 5); the

steer the TBM forward in an upward direction, only the upper articulation jack is retracted while the other jacks are automatically extended. Based on this principle, the length of each articulation jack in the X-type system is determined by the following: distance between both rear reference points equals the shield diameter; and the distance between the reference points at the rear and front equals the length of the front shield (Figure 2).

<!-- image -->

Engineering drawing

Figure 5. Cross section of the arrangement of articulation jacks. Figure 5. Cross section of the arrangement of articulation jacks.

<!-- formula-not-decoded -->

where lu , l d , l l , and l r are the length variations of upper, lower, left, and right articulation jacks, respectively; tu , t d , t l , and tr are the operation times for the setting of articulation jacks in the upper, lower, left, and right directions, respectively; and vu , vd , vl , and vr are the extension speeds of upper, lower, left, and right articulation jacks, respectively.

As a result of the changing length of articulation jacks, the articulation angle is determined as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where a is the articulation angle in the horizontal direction on the x-y plane; b is the angle in the vertical direction on the y-z plane; l lr is the length difference between left and right articulation jacks; l du is the length difference between lower and upper articulation jacks; and D is the TBM shield diameter (Figure 6).

During articulation for horizontal steering, three reference points change together. As the articulation point is located at the center, both rear reference points change symmetrically relative to the origin, while the front point moves to a new coordinate (Figure 6a). However, to steer the TBM in the vertical direction, both rear reference points remain unchanged while the front point changes during the extension of the articulation jack (Figure 6b). The reference points are recalculated for the articulation angle and the angle of the planned route as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

Engineering drawing

Figure 6. X-type system: ( a ) horizontal steering; ( b ) vertical steering. Figure 6. X-type system: ( a ) horizontal steering; ( b ) vertical steering.

<!-- image -->

Engineering drawing

## 3.2.2. Articulation Jack Operation in the V-Type System

The V-type articulation system is depicted in Figure 7. Here, only the articulation jack in the target direction is unchanged, while the others are extended. To steer the TBM in an upward direction, only the upper articulation jack is unchanged, while the others are retracted. The length of each articulation jack is determined as follows:

<!-- formula-not-decoded -->

For horizontal steering, two reference points change together, with that at the front moving to new coordinates, regardless of the direction of horizontal steering. However, as the articulation point is located within the articulation jack, the reference points at rear right and left either change or are unchanged, depending on the target direction. To determine the new reference points in horizontal steering, auxiliary variables are calculated first (Equations (11) and (12); Figure 7a):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where dFR is the distance between Rr ( R 0 ) and Fr ( F 0 ), and dF a is the distance between F 0 and Fr , which depends on the articulation angle in the horizontal direction.

Based on these auxiliary variables, reference points are recalculated depending on the rotation direction of the articulation angle and the angle of the planned route. If the articulation angle in the horizontal direction ( α ) is negative, the reference points are determined as follows (Figure 7a):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where c is the base angle of an isosceles triangle comprising three reference points based on the reference line at the rear ( ∠ F 0 L 0 R 0 = ∠ Fr Rr Lr = ∠ F 0 R 0 L 0 = ∠ Fr Lr Rr ) (Figure 7a).

If a is positive, the reference points are determined as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

Engineering drawing

Figure 7. V-type system: ( a ) horizontal steering; ( b ) vertical steering. Figure 7. V-type system: ( a ) horizontal steering; ( b ) vertical steering.

<!-- image -->

Engineering drawing

For vertical steering, the three reference points change together, with those at the rear moving to new coordinates by the same distance and those at the front moving more than those at the rear (Figure 6b). To determine the new reference points in vertical steering, the auxiliary variable is first calculated as follows (Figure 7b and Equation (19)):

<!-- formula-not-decoded -->

where dF b is the distance between F 0 and Fr caused by the articulation angle in the vertical direction.

The reference points are then recalculated depending on the rotation direction of the articulation angle and the angle of the planned route. If the articulation angle in the vertical direction ( b ) is positive, the reference points are determined as follows (Figure 7b):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

If b is negative, only the reference point at the front is recalculated, as follows:

<!-- formula-not-decoded -->

## 3.3. Calculation of Reference Point Change Owing to Shield Jack Operation

After articulation, a group of shield jacks is extended. The mechanism of shield jack operation is similar to that of the V-type articulation system, with only selected jacks being extended while the other shield jacks remain unchanged. As explained in Section 3.2, shield jack differences caused by one-sided shield jack extension are required for successful curved excavation during articulation. However, as we assumed that the shield jacks are extended equally and simultaneously at the same jack speed, the length of shield jacks is calculated as follows:

<!-- formula-not-decoded -->

where tt is the operation time for extension of the shield jack, and V is the extension speed of the jack.

During TBM advance, three reference points are changed by the same distance during the extension of the shield jack. Therefore, the new reference points are calculated after articulation work as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where F is the front reference point shifted by the TBM advance ( Fx , Fy , Fz ); R is the rearright point shifted by the TBM advance ( Rx , Ry , Rz ); and L is the rear-left point shifted by TBM advance ( Lx , Ly , Lz ).

During TBM advance, deviations in its position caused by pitch, yaw, and roll may occur, so the reference points are recalculated depending on these rotations according to Shen et al. [2] and Shen et al. [3] as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where T is the transformation matrix of three rotation angles; q is the pitch angle; j is the yaw angle; ˘ is the roll angle; FF is the front reference point affected by the three rotation angles ( FFx , FFy , FFz ); RR is the rear-right reference point affected by the three rotation angles ( RRx , RRy , RRz ); and LL is the rear-left reference point affected by the three rotation angles ( LLx , LLy , LLz ). Appl. Sci. 2023 , 13 , x FOR PEER REVIEW 13  of  29 rotation angles (𝐹𝐹 ௫ , 𝐹𝐹 ௬ , 𝐹𝐹 ௭ ) ;  𝑅𝑅 is  the rear-right reference point affected by the three (𝑅𝑅 , 𝑅𝑅 , 𝑅𝑅

Based on the work of Festa et al. [6], horizontal and vertical deviations caused by pitch and yaw can be calculated as follows, assuming that the TBM moves along the planned route well (Figure 8): rotation angles ௫ ௬ ௭ ); and LL is the rear-left reference point affected by the three rotation angles (𝐿𝐿௫ , 𝐿𝐿 ௬ , 𝐿𝐿 ௭ ). Based on the work of Festa et al. [6], horizontal and vertical deviations caused by pitch  and  yaw  can  be  calculated  as  follows,  assuming  that  the  TBM  moves  along  the planned route well (Figure 8):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Figure 8. Deviation tendencies: ( a ) horizontal tendency; ( b ) vertical tendency. Figure 8. Deviation tendencies: ( a ) horizontal tendency; ( b ) vertical tendency.

<!-- image -->

Engineering drawing

## 4. Example of Curved Excavation Simulation

Based on the above mathematical models, curved excavations were simulated using Python programming. The curved simulation involves two processes. After articulation, shield jacks are extended until the length of the jack equals the segment length. When Appl. Sci. 2023 , 13 , x FOR PEER REVIEW

## 4. Example of Curved Excavation Simulation

Based on the above mathematical models, curved excavations were simulated using Python programming. The curved simulation involves two processes. After articulation, shield jacks are extended until the length of the jack equals the segment length. When TBM advance is complete, a segment ring is created, and both articulation jacks and shield jacks are returned to their initial positions. The one cycle operation comprises a series of these processes, and this cycle operation is repeated continuously until the total simulation is complete (Table 1).

Table 1. Example of simulation conditions for curved excavation.

| Parameters                                                                                                                                                                                                                                                                                                                                                                     | Value                                                                                                    |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| TBM shield diameter ( D ) Length of front shield and cutterhead ( l F ) Average thickness of segment ring ( d r ) Articulation jack speed (= v u = v d = v l = v r ) Shield jack speed ( vv ) Initial front reference point ( F 0 x , F 0 y , F 0 z ) Initial rear-right reference point ( R 0 x , R 0 y , R 0 z ) Initial rear-left reference point ( L 0 x , L 0 y , L 0 z ) | 8000mm 3000mm 1500mm 1 mm/s 10 mm/s (0 mm, 3000 mm, 0 mm) (4000 mm, 0 mm, 0 mm) ( - 4000 mm, 0 mm, 0 mm) |

TBM manuals confirm that the maximum value of articulation angle in the vertical direction is near 0.5 ◦ , while the horizontal angle varies from 0.5 ◦ to 5.4 ◦ depending on TBM size and manufacturer. Therefore, the horizontal and vertical angles in the route planned for the simulation were both set at 0.5 ◦ here. The horizontal and vertical deviations caused by two rotation angles are essential indicators to be monitored in real time by the TBM operator. Therefore, simulations with different rotation angles (0-2.5 ◦ ) and articulation angles in the horizontal (0-2.5 ◦ ) and vertical (0-0.5 ◦ ) directions were tested to determine 14  of  29

the effects on horizontal and vertical deviations in Section 4.3. articulation angles in the horizontal (0-2.5°) and vertical (0-0.5°) directions were tested to

determine the effects on horizontal and vertical deviations in Section 4.3.

<!-- formula-not-decoded -->

Acomparison of the reference points used in the X- and V-type systems is provided in Figure 9. The articulation angles in the horizontal and vertical directions were set at 0.5 ◦ , with only the initial and final reference points being marked in Figure 9. A comparison of the reference points used in the X- and V-type systems is provided in Figure 9. The articulation angles in the horizontal and vertical directions were set at 0.5°, with only the initial and final reference points being marked in Figure 9.

Figure 9. Comparison of reference points from a single cycle simulation with the X- and V-type systems. Figure 9. Comparison of reference points from a single cycle simulation with the X- and V-type systems.

<!-- image -->

Line chart

Deviations in reference points are described in Table 2. As the locations of articulation points in the two systems are different, deviations can arise during articulation. Errors in the y coordinate ( 𝐿 ೝ , 𝑅 ೝ , 𝐹 ೝ )  are generally the highest of the three reference points, Deviations in reference points are described in Table 2. As the locations of articulation points in the two systems are different, deviations can arise during articulation. Errors in the y coordinate ( Ly r , Ry r , Fy r ) are generally the highest of the three reference points, with Lr and Rr having almost identical error values. Such errors may be changed depending on the direction and angle of articulation.

Table 2. Differences in reference points between the X- and V-type systems.

| Location of Reference Point   | Coordinate        | Position (mm)        | Position (mm)        | Error (%)         |
|-------------------------------|-------------------|----------------------|----------------------|-------------------|
| Location of Reference Point   | Coordinate        | X-Type               | V-Type               | Error (%)         |
| L r                           | L x r L y r L z r | - 3986.7 1534.9 13.1 | - 3986.3 1604.9 13.3 | 0.0 - 4.6 - 1.2   |
| R r                           | R x r R y r R z r | 4013.0 1464.9 13.1   | 4013.4 1534.9 13.3   | 0.0 - 4.8 - 1.2   |
| F r                           | F x r F y r F z r | 39.4 4499.7 39.4     | 39.8 4569.7 39.5     | - 1.2 - 1.6 - 0.4 |

The X-type system is clearly more appropriate for use in curved excavation as it has the advantages of articulation sealing and water resistance during articulation. The mathematical model of the X-type system is also less complex than that of the V-type. Therefore, we mainly focused on simulations of curved excavations with the X-type articulation system under predetermined simulation conditions (Table 1), with the simulation involving 100 cycles (100 rings), and with pitch and yaw being considered.

## 4.2. Curved Excavation in the Top-Right Direction

The planned route in the top-right direction was created by horizontal ( ai ) and vertical ( bi ) angles of 0.5 ◦ . To travel along this route, α and β were set to be the same as ai and bi , respectively. The articulation jacks were then extended, as shown in Table 3 (Equations (5) and (6)). The flow chart of the curved excavation process is presented in Figure 10.

Table 3. Adjustment of articulation jacks for curved excavation in the top-right direction.

| Location of Jack       | Required Length of Articulation Jack for a = 0.5 ◦ and b = 0.5 ◦   |
|------------------------|--------------------------------------------------------------------|
| Upper Lower Left Right | 0mm 70mm 70mm 0mm                                                  |

The simulation progress in curved excavation in the top-right direction, without consideration of the two rotation angles (pitch and yaw), is depicted in Figure 11a,b, for 25 and 75 cycles. Blue lines (Figure 11) indicate the planned route, and red triangles indicate the three reference points. The red triangle travels along almost the entire route during the simulation. After 100 cycles, the TBM has travelled ~150 m, with the final reference points being recorded in Table 4.

The deviation between tracking points of the planned route ( Tx , Ty , Tz ) and the rear reference point ( Mx , My , Mz ) are shown in Figure 12, without consideration of rotation angles. The estimated rear reference points are almost the same as the tracking point, as the 15,000 calculated deviations overlap each other around zero (Table 5). If the articulation angles are adjusted to be almost identical to the direction angles of the planned route, the curved excavation can be successfully performed by the TBM without consideration of the rotation angles.

Appl. Sci. 2023 , 13 , 10087

𝐹௭ ೝ

## 4.2. Curved Excavation in the Top-Right Direction

14 of 27 The planned route in the top-right direction was created by horizontal ( 𝑎௜ ) and vertical ( 𝑏௜ ) angles of 0.5°. To travel along this route, α and β were set to be the same as 𝑎௜ and 𝑏௜ , respectively. The articulation jacks were then extended, as shown in Table 3 (Equations (5) and (6)). The flow chart of the curved excavation process is presented in Figure 10.

Appl. Sci. 2023 , 13 , x FOR PEER REVIEW

Figure 11. Simulated curved excavation in top-right direction without consideration of rotation angles: ( a ) simulation with 25 cycles; ( b ) simulation with 75 cycles. Figure 11. Simulated curved excavation in top-right direction without consideration of rotation angles: ( a ) simulation with 25 cycles; ( b ) simulation with 75 cycles.

<!-- image -->

Full page image

Table 4. Location of reference points after 100 cycles in the top-right direction.

Location of Reference Point Position (

𝐿

x

,

y

,

z

39.4

39.5

-0.4

)

Table 4.

Location of reference points after 100 cycles in the top-right direction. 17  of  29

## Location of Reference Point

## Position ( x , y , z )

L (48,299 mm, 119,800 mm, 62,117 mm) R (53,427 mm, 113,659 mm, 62,117 mm) F (52,339 mm, 117,962 mm, 64,420 mm) LL (50,383 mm, 120,004 mm, 60,032 mm) RR (55,403 mm, 113,776 mm, 60,141 mm) FF (54,390 mm, 118,137 mm, 62,368 mm) The deviation between tracking points of the planned route ( 𝑇௫ , 𝑇 ௬ , 𝑇 ௭ ) and the rear reference point ( 𝑀௫, 𝑀௬ , 𝑀 ௭ ) are shown in Figure 12, without consideration of rotation angles. The estimated rear reference points are almost the same as the tracking point, as the 15,000 calculated deviations overlap each other around zero (Table 5). If the articulation angles are adjusted to be almost identical to the direction angles of the planned route, the curved excavation can be successfully performed by the TBM without consideration of the rotation angles.

Figure 12. Simulated deviations between tracking points of the planned route and rear reference points, without consideration of the rotation angles. Figure 12. Simulated deviations between tracking points of the planned route and rear reference points, without consideration of the rotation angles.

<!-- image -->

Line chart

Table 5. Deviations between tracking points of the planned route in the top-right direction and rear Table 5. Deviations between tracking points of the planned route in the top-right direction and rear reference points with consideration of the rotation angles.

reference points with consideration of the rotation angles.

| Type of Deviation                                                                                                                                           | Coordinate     | Average Deviation (mm) Average Deviation (mm)   |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|-------------------------------------------------|
| Type of Deviation Tracking point-rear reference point with no pitch or yaw ( 𝑀-𝑇 ) Tracking point-rear reference point with no pitch or yaw ( M - T ) x y z | Coordinate x y | 0.0 0.0 0.0                                     |
| Tracking point-rear reference                                                                                                                               | z              | 0.0 0.0                                         |
| x                                                                                                                                                           |                | 0.0 1152.3                                      |
| Tracking point-rear reference points with pitch 𝑀-𝑇𝑇 points with pitch and yaw ( M - TT ) y z                                                               | x y            | 1152.3 20.9 20.9 - 1152.4                       |
| and yaw ( )                                                                                                                                                 |                |                                                 |
|                                                                                                                                                             | z              | -1152.4                                         |

The simulated progress of curved excavation in the top-right direction, with consideration of the rotation angles (pitch = yaw = 1.0°), is shown in Figure 13 for 25 and 75 cycles. Here, the red triangle does not fully follow the route during the simulation. Due to pitch and yaw, the TBM is inevitably liable to vibrate during the excavation, causing deviations. The total distance travelled by the TBM is again ~150 m, with the final reference points being recorded in Table 4. The simulated progress of curved excavation in the top-right direction, with consideration of the rotation angles (pitch = yaw = 1.0 ◦ ), is shown in Figure 13 for 25 and 75 cycles. Here, the red triangle does not fully follow the route during the simulation. Due to pitch and yaw, the TBM is inevitably liable to vibrate during the excavation, causing deviations. The total distance travelled by the TBM is again ~150 m, with the final reference points being recorded in Table 4. The deviation between tracking points of the planned route ( Tx , Ty , Tz ) and the rear

reference point ( Mxx , Myy , Mzz ), with consideration of the rotation angles, is shown in Figure 13. The estimated rear reference points differ from the tracking point, as the 15,000 calculated deviations plot as an almost straight line. Through consideration of the rotation angles, and although articulation angles are adjusted to be almost identical to the direction angles of the planned route, there are deviations during the curved excavation caused by pitch and yaw. Therefore, the TBM operator would attempt to control the shield or articulation jacks to reduce deviations after or during one cycle of curved excavation.

Appl. Sci.

2023

,

Figure 13. Simulation of deviations between tracking points of the planned route in the top-right

<!-- image -->

Line chart

Figure 13. Simulation of deviations between tracking points of the planned route in the top-right direction and rear reference points, with consideration of two rotation angles. direction and rear reference points, with consideration of two rotation angles.

13

, x FOR PEER REVIEW

The deviation between tracking points of the planned route ( 𝑇௫ , 𝑇 ௬ , 𝑇 ௭ ) and the rear reference point ( 𝑀௫௫, 𝑀 ௬௬ , 𝑀 ௭௭ ), with consideration of the rotation angles, is shown in Figure 13. The estimated rear reference points differ from the tracking point, as the 15,000 calculated deviations plot as an almost straight line. Through consideration of the rotation angles, and although articulation angles are adjusted to be almost identical to the direction angles of the planned route, there are deviations during the curved excavation caused by pitch and yaw. Therefore, the TBM operator would a tt empt to control the shield or articThe averages calculated for the two types of deviation are summarized in Table 5. It is clear that the two rotation angles can cause considerable deviations, particularly in the x and z coordinates. As pitch and yaw have positive values, the calculated average deviations in the x and z coordinates have positive and negative values, respectively. Estimated horizontal ( dh ) and vertical ( dy ) tendencies for the y coordinate (Equations (32) and (33)) are shown in Figure 14. When the pitch ( q ) and yaw ( j ) are zero, no deviations are evident, with tendencies being zero. 19  of  29

𝛽

Figure 14. Horizontal and vertical tendency estimated from the simulation of the curved excavation in the top-right direction. Figure 14. Horizontal and vertical tendency estimated from the simulation of the curved excavation in the top-right direction.

<!-- image -->

Line chart

## 4.3. Effect of Articulation Angles and Rotation Angles on Tendencies

To determine the effect of both factors on horizontal and vertical tendency, simulations were undertaken for only ten cycles (Table 6). The maximum pitch for the test condition was &lt;3.0°, based on the TBM data recorded in a specific TBM tunneling site. The As the cumulative angle of the planned route increases, the horizontal and vertical tendencies change from 1.75 and - 1.75 to 0.71 and - 0.71, respectively. As the TBM moves forward, its advance direction in the y coordinate changes, changing the direction of both tendencies, with the magnitude of both approaching zero. If the articulation angles a and b are zero, both tendencies are constant at - 1.75 and +1.75, respectively. As pitch and yaw are equal at 1.0 ◦ , a and b are both 0.5 ◦ , with both tendencies showing the same pattern as the y symmetry axis.

## 4.3. Effect of Articulation Angles and Rotation Angles on Tendencies

To determine the effect of both factors on horizontal and vertical tendency, simulations were undertaken for only ten cycles (Table 6). The maximum pitch for the test condition was &lt;3.0 ◦ , based on the TBM data recorded in a specific TBM tunneling site. The maximum yaw for the test was determined to be same as maximum pitch. The maximum articulation angles in the horizontal and vertical directions were determined to be 2.5 ◦ and 0.5 ◦ , respectively, as averages of specifications for different machine manuals produced by different TBM manufacturers.

Table 6. Test simulations with different rotation and articulation angles.

| Case Number   | Simulation Conditions   | Simulation Conditions   | Simulation Conditions      | Simulation Conditions      |
|---------------|-------------------------|-------------------------|----------------------------|----------------------------|
| Case Number   | Type of Rotation Angle  | Type of Rotation Angle  | Type of Articulation Angle | Type of Articulation Angle |
| Case Number   | Pitch ( q )             | Yaw ( j )               | Horizontal Direction ( a ) | Vertical Direction ( b )   |
| 0             |                         | 0                       |                            |                            |
| 1             |                         | 0.5                     |                            |                            |
| 2             |                         | 1.0                     |                            |                            |
| 3             | 0                       | 1.5                     | 0.5                        | 0.5                        |
| 4             |                         | 2.0                     |                            |                            |
| 5             |                         | 2.5                     |                            |                            |
| 6             | 0.5                     |                         |                            |                            |
| 7             | 1.0                     |                         |                            |                            |
| 8             | 1.5                     | 0                       | 0.5                        | 0.5                        |
| 9             | 2.0                     |                         |                            |                            |
| 10            | 2.5                     |                         |                            |                            |
| 11            |                         |                         | 0                          |                            |
| 12            |                         |                         | 0.5                        |                            |
| 13            |                         |                         | 1.0                        |                            |
| 14            | 1.0                     | 1.0                     | 1.5                        | 0                          |
| 15            |                         |                         | 2.0                        |                            |
| 16            |                         |                         | 2.5                        |                            |
| 17            |                         |                         |                            | 0.1                        |
| 18            |                         |                         |                            | 0.2                        |
| 19            | 1.0                     | 1.0                     | 0                          | 0.3                        |
| 20            |                         |                         |                            | 0.4                        |
| 21            |                         |                         |                            | 0.5                        |
| 22            |                         |                         | 0.5                        | 0.1                        |
| 23            |                         |                         | 1.0                        | 0.2                        |
| 24            | 1.0                     | 1.0                     | 1.5                        | 0.3                        |
| 25            |                         |                         | 2.0                        | 0.4                        |
| 26            |                         |                         | 2.5                        | 0.5                        |

The average horizontal and vertical tendencies for cases 0-5 (Table 6) depend on yaw angle (Figure 15). As yaw increases from 0.0 ◦ to 2.5 ◦ , the magnitude of average horizontal tendency also increases from 0.00% to 4.34%, while vertical tendency is constant at 0.00%.

The average horizontal and vertical tendencies for cases 6-10 (Table 6) are shown in Figure 16 depending on pitch angle, with Case 0. As pitch increases from 0.0° to 2.5°, the average vertical tendency increases from 0.00% to 4.35%, while horizontal tendency is constant at 0.00%.

18 of 27 Overall, yaw only affects the horizontal tendency, while pitch only affects the vertical

## tendency.

Figure 15. Variation in horizontal and vertical tendency with yaw angle. Figure 15. Variation in horizontal and vertical tendency with yaw angle.

<!-- image -->

Line chart

The average horizontal and vertical tendencies for cases 6-10 (Table 6) are shown in Figure 16 depending on pitch angle, with Case 0. As pitch increases from 0.0 ◦ to 2.5 ◦ , the average vertical tendency increases from 0.00% to 4.35%, while horizontal tendency is constant at 0.00%. Appl. Sci. 2023 , 13 , x FOR PEER REVIEW 21  of  29

<!-- image -->

Line chart

Figure 16. Variation of horizontal and vertical tendency with pitch angle. Figure 16. Variation of horizontal and vertical tendency with pitch angle.

The average horizontal and vertical tendencies for cases 11-16 (Table 6) vary with articulation angle in the horizontal direction (Figure 17). With an articulation of 0.00°, both tendencies are constant to -1.745. As the horizontal articulation angle increases, the average horizontal tendency decreases from 1.745 to 1.742, 1.734, 1.720, 1.701, to 1.678, as the vertical tendency decreases from 1.745 to 1.741, 1.732, 1.718, 1.698, to 1.674. Overall, yaw only affects the horizontal tendency, while pitch only affects the vertical tendency. The average horizontal and vertical tendencies for cases 11-16 (Table 6) vary with articulation angle in the horizontal direction (Figure 17). With an articulation of 0.00 ◦ , both tendencies are constant to -1.745. As the horizontal articulation angle increases, the average horizontal tendency decreases from 1.745 to 1.742, 1.734, 1.720, 1.701, to 1.678, as the vertical tendency decreases from 1.745 to 1.741, 1.732, 1.718, 1.698, to 1.674.

<!-- image -->

Line chart

19 of 27 The average horizontal and vertical tendencies for cases 11-16 (Table 6) vary with articulation angle in the horizontal direction (Figure 17). With an articulation of 0.00°, both tendencies are constant to -1.745. As the horizontal articulation angle increases, the average horizontal tendency decreases from 1.745 to 1.742, 1.734, 1.720, 1.701, to 1.678, as the

vertical tendency decreases from 1.745 to 1.741, 1.732, 1.718, 1.698, to 1.674.

Figure 17. Variation of horizontal and vertical tendency with horizontal articulation angle. Figure 17. Variation of horizontal and vertical tendency with horizontal articulation angle.

<!-- image -->

Line chart

The average horizontal and vertical tendencies obtained for cases 17-21 (Table 6) vary with articulation angle in the horizontal direction (Figure 18). The average horizontal tendency decreases from 1.745 to 1.743, while the average vertical tendency decreases from 1.745 to 1.743, depending on the vertical articulation angle. The average horizontal and vertical tendencies obtained for cases 17-21 (Table 6) vary with articulation angle in the horizontal direction (Figure 18). The average horizontal tendency decreases from 1.745 to 1.743, while the average vertical tendency decreases from 1.745 to 1.743, depending on the vertical articulation angle. Appl. Sci. 2023 , 13 , x FOR PEER REVIEW

Figure 18. Variation in horizontal and vertical tendency with vertical articulation angle. Figure 18. Variation in horizontal and vertical tendency with vertical articulation angle.

<!-- image -->

Line chart

The average horizontal and vertical tendencies for cases 22-26 (Table 6) vary articulation angle in the horizontal and vertical direction (Figure 19). The average zontal tendency decreases from 1.745 to 1.741, 1.732, 1.717, 1.697, to 1.673, while ve tendency decreases from 1.745 to 1.742, 1.733, 1.719, to 1.676 as the articulation ang both directions increase. The average horizontal and vertical tendencies for cases 22-26 (Table 6) vary with articulation angle in the horizontal and vertical direction (Figure 19). The average horizontal tendency decreases from 1.745 to 1.741, 1.732, 1.717, 1.697, to 1.673, while vertical tendency decreases from 1.745 to 1.742, 1.733, 1.719, to 1.676 as the articulation angles in both directions increase.

The articulation angles in both directions have a strong influence on the hori and vertical tendencies, with both decreasing with increasing articulation angle. If t ticulations in both directions change together, both tendencies decrease more (no difference between Figures 17 and 19). It seems that the articulation angles in either

20 of 27 The articulation angles in both directions have a strong influence on the hori and vertical tendencies, with both decreasing with increasing articulation angle. If t ticulations in both directions change together, both tendencies decrease more (no difference between Figures 17 and 19). It seems that the articulation angles in either

tion can impact both tendencies independently.

Figure 19. Variation of horizontal and vertical tendency with horizontal and vertical articulat angles. Figure 19. Variation of horizontal and vertical tendency with horizontal and vertical articulation angles.

<!-- image -->

Line chart

5. Application in TBM Simulator The aim of this study was the training of TBM operators in the use of the ste system in curved excavation, using the simulator. Therefore, the proposed mathem models were applied and tested in the TBM simulator as the final stage of the study The articulation angles in both directions have a strong influence on the horizontal and vertical tendencies, with both decreasing with increasing articulation angle. If the articulations in both directions change together, both tendencies decrease more (note the difference between Figures 17 and 19). It seems that the articulation angles in either direction can impact both tendencies independently. 5. Application in TBM Simulator

The aim of this study was the training of TBM operators in the use of the steering system in curved excavation, using the simulator. Therefore, the proposed mathematical models were applied and tested in the TBM simulator as the final stage of the study.

The TBM simulator was created using the Adobe Air platform, written in Adobe ActionScript 3.0. Version 32.0 of Adobe Air SDK (software development kit) was used, with the Intellij IDEA employed as the IDE (integrated development environment). Adobe Air uses vector graphics, which allows for the creation of applications with low capacity and high performance. As there is no pre-configuration work for the installation, it is easy to access the platform. To compare the simulation results with Python, the simulations involved the test conditions presented in Tables 1, 3 and 6.

The simulator touch panel control for the setting of the articulation jack is shown in Figure 20, where the setting of the jack for curved excavation in the top-right direction, with articulation angles of 0.5 ◦ in the horizontal and vertical directions, is illustrated in Figure 20a. Through the adjustment of the four directions in the center, the lower and left articulation jacks are extended to 70 mm, and the articulation angles in both directions changed to 0.5 ◦ , as shown in Table 3. When the articulation setting is complete, shield jacks are extended, with the TBM moving forward along the planned route.

Figure 20b presents the setting of the articulation jack for the curved excavation in the top-left direction with the articulation angle of - 1.0 ◦ in the horizontal direction and 0.5 ◦ in the vertical direction. Through the adjustment of four directions in the center, lower and right articulation jacks are extended to 105 mm, and upper articulation jacks are extended to 35 mm, while the right articulation jacks are retracted to - 35 mm. Once the articulation setting is complete, the shield jacks are extended, and the TBM moves forward along the planned route.

21 of 27 the Intellij IDEA employed as the IDE (integrated development environment). Adobe Air uses vector graphics, which allows for the creation of applications with low capacity and high performance. As there is no pre-configuration work for the installation, it is easy to access the platform. To compare the simulation results with Python, the simulations involved the test conditions presented in Tables 1, 3 and 6.

The progress in the curved excavation is shown in Figure 21, with the cycles (rings) involved without consideration of the rotation angles. Figure 21a presents the simulation in the top-right direction at 25 cycles. The longitudinal section in the y and z coordinates is shown to the left of the panel. The travel range is shown as a bold red line, and the rest of the planned route as a pale green line. It is possible to check the current position in the y and z coordinates. The simulator touch panel control for the se tt ing of the articulation jack is shown in Figure 20, where the se tt ing of the jack for curved excavation in the top-right direction, with articulation angles of 0.5° in the horizontal and vertical directions, is illustrated in Figure 20a. Through the adjustment of the four directions in the center, the lower and left articulation jacks are extended to 70 mm, and the articulation angles in both directions changed to 0.5°, as shown in Table 3. When the articulation se tt ing is complete, shield jacks are extended, with the TBM moving forward along the planned route.

Figure 20. Example of se tt ing of articulation jack for curved excavation: ( a ) in the top-right direction; ( b ) in the top-left direction. Figure 20. Example of setting of articulation jack for curved excavation: ( a ) in the top-right direction; ( b ) in the top-left direction.

<!-- image -->

Engineering drawing

22 of 27 The progress in the curved excavation is shown in Figure 21, with the cycles (rings) involved without consideration of the rotation angles. Figure 21a presents the simulation in the top-right direction at 25 cycles. The longitudinal section in the y and z coordinates is shown to the left of the panel. The travel range is shown as a bold red line, and the rest of the planned route as a pale green line. It is possible to check the current position in the y and z coordinates.

Figure 21. Simulation progress of the curved excavation at 25 rings without considering rotation angles: ( a ) in top-right direction; ( b ) in top-left direction. Figure 21. Simulation progress of the curved excavation at 25 rings without considering rotation angles: ( a ) in top-right direction; ( b ) in top-left direction.

<!-- image -->

Engineering drawing

Figure 21b presents the simulation in the top-left direction at 25 cycles. The cross section in the x and z coordinates is shown to the right of the panel. The pale green dot indicates that the planned route is always located at the center of both coordinates. Depending on the deviations caused by the rotation angles, the small circle with a white crossline can shake. As there are no rotation angles, the crossline is the same as the rearmiddle reference point and overlaps the pale green dot. The purple arrow indicates the advance direction viewed in the x - z plane. Depending on the length of articulation jacks, the direction angle in the x - z plane is calculated as follows (Table 7).

Referring to Table 7, it can be seen that the arrow points to Quadrant II, and the direction angle is about 297 ◦ in the curved excavation with the top-left direction. In comparison, the arrow points to Quadrant I, and the direction angle is about 45 ◦ in the curved excavation with the top-right direction.

Figure 22 presents the simulation in the top-right direction at five cycles without consideration of the rotation angles for explaining how to adjust the articulation jacks during the excavation. As shown in Figure 22a, deviations between the planned route and the rear-middle reference point are accumulated during the excavation because of the difference between articulation angles (0.2 ◦ ) and angles in the route (0.2 ◦ ). As both articulation angles are increased to 0.5 ◦ , the deviations are highly decreased, and TBM travels along almost the entire route again.

Table 7. Direction angle in the x - z plane calculated from articulation jack lengths.

̸

| Condition           | Direction Angle (Clockwise)             |
|---------------------|-----------------------------------------|
| l u ≤ l d l l = l r | 0 ◦ (=360 ◦ )                           |
| l u > l d l l = l r | 180 ◦                                   |
| l u = l d l l > l r | 90 ◦                                    |
| l u = l d l l < l r | 270 ◦                                   |
| l u < l d l l < l r | tan - 1 ( l l - l r l d - l u ) + 360 ◦ |
| l u < l d l l > l r | tan - 1 ( l l - l r l d - l u )         |
| l u > l d l l = l r | tan - 1 ( l l - l r l d - l u ) + 180 ◦ |

The simulation progress in the curved excavation, with consideration of rotation angles, is shown in Figure 23. Figure 23a presents the curved excavation in the top-right direction at 25 cycles and 75 cycles. Figure 23b presents the curved excavation in the top-left direction at 25 cycles and 75 cycles. Due to the rotation angles, deviations between the planned route and the rear-middle reference point are measured during the excavation. As the total excavation distance increases, the deviations increase, as shown by the distance between the pale green dot and the crossline. Because the induced deviation is gradually accumulating, the TBM operator should correct the pitch and yaw using the shield jacks and articulation jacks.

In practice, deviations are frequently bound to occur during soil ground excavation because of the heterogeneous characteristic of soil grounds. Therefore, the operator adjusts both the articulation and the shield jacks by monitoring the TBM position in real time through the navigation panel depending on the deviations. In contrast, the operator is less concerned with deviations during the rock excavation as most rocks show more homogenous characteristics than soil. Therefore, once the articulation jacks are set in advance, the operator only adjusts the shield jacks to be extended during the excavation. Depending on the rotation angles assigned for the excavation simulation in real time, curved excavation in both soil ground and rock can also be experienced indirectly through the TBM simulator.

Figure 22. Simulation progress of the curved excavation at 5 rings without considering rotation angles: ( a ) articulation angles with 0.2°; ( b ) articulation angles with 0.5°. Figure 22. Simulation progress of the curved excavation at 5 rings without considering rotation angles: ( a ) articulation angles with 0.2 ◦ ; ( b ) articulation angles with 0.5 ◦ .

<!-- image -->

Engineering drawing

Figure 23. Simulation progress of the curved excavation at 25 rings and 75 rings with considering rotation angles: ( a ) in top-right direction; ( b ) in top-left direction. Figure 23. Simulation progress of the curved excavation at 25 rings and 75 rings with considering rotation angles: ( a ) in top-right direction; ( b ) in top-left direction.

<!-- image -->

Line chart

## 6. Conclusions

This study aims to develop the mathematical models for the shield TBM steering and apply the models into the TBM simulator. The concept of curved excavation and the TBM steering model were overviewed first. Next, the mathematical formulae, including the articulation jack operations and shield jack operations, were created for the simulation based on the steering mechanism. Then, curved excavations were simulated using a Python program based on different articulation systems and different planned routes to reflect the mathematical formulae. Moreover, simulations with different cases were tested to identify the effect of two articulation angles and two rotation angles on the horizontal tendency and vertical tendency. Finally, the proposed mathematical formulae were applied in the TBM simulator to simulate the articulation operations.

Firstly, the reference points estimated from one cycle simulation used in the 'X-type' system and 'V-type' system were compared. Due to the difference in location of the articulation point, differences of reference point between both systems occur during the articulation work, and the final reference points obtained from 'X-type' and 'V-type' have some errors.

Secondly, two simulations with different planned routes were executed without considering pitch and yaw. The estimated rear-middle reference points are almost equal to the tracking point of the route, if the pitch and yaw are not considered. In contrast, the deviations between the tracking point of the route and the rear-middle reference points occur if the pitch and yaw are considered. Even though the articulation angles are adjusted to be nearly identical to the direction angles of the planned route, there will be deviations during the curved excavation caused by pitch and yaw. Therefore, it is expected that the TBM operator attempts to control the shield jacks or articulation jacks to reduce deviations after or during the one cycle of curved excavation. Also, these deviations caused by pitch and yaw could differ depending on the magnitude and the direction of the articulation angle.

Thirdly, simulations with different cases were tested to identify the impact of articulation angles in the horizontal direction and vertical direction and rotation angles (pitch and yaw) on the horizontal tendency and vertical tendency calculated from the deviations. It is confirmed that the yaw affects the horizontal tendency, while the pitch only affects the vertical tendency. As both rotation angles increase, higher tendencies are estimated as a result. Lastly, the articulation angles in both directions strongly influence the horizontal tendency and vertical tendency. As the articulation angles in the horizontal direction or vertical direction increase, the smaller the estimated magnitude of tendencies. Lastly, the proposed mathematical models were applied and tested in the TBM simulator as the final stage of the study.

Generally, there are four groups for selecting shield jacks. The speed of each shield jack group can control the length of each shield jack group. The segment plane is always perpendicular to the rear shield axis during the curved excavation. Therefore, each shield jack group should be extended with different jack speeds depending on the curved direction. However, this study assumed that a group of shield jacks have the same extension speed. Therefore, it is difficult to consider the one-sided extension of the shield jack in parallel with articulation jack operations during the excavation. Future studies should focus on considering the jack speed of each shield jack group independently.

In addition, this study only focused on a shield TBM steering simulator. Future research will be aimed at the development of a steering system for an open (gripper) TBM simulator.

Author Contributions: Conceptualization, B.P. and S.-H.C.; methodology, B.P.; software, B.P. and C.L.; validation, W.-Y.L., S.D. and T.-H.K.; formal analysis, C.L., W.-Y.L. and T.-H.K.; investigation, B.P., C.L. and S.-W.C.; resources, W.-Y.L. and S.D.; data curation, W.-Y.L. and T.-H.K.; writing-original draft preparation, B.P.; writing-review and editing, B.P. and S.-H.C.; visualization, W.-Y.L., S.D. and T.-H.K.; supervision, S.-W.C.; project administration, S.-W.C. and S.-H.C.; funding acquisition, S.-W.C. and S.-H.C. All authors have read and agreed to the published version of the manuscript.

## References

1. Sugimoto, M.; Sramoon, A. Theoretical model of shield behavior during excavation. I: Theory. J. Geotech. Geoenvironm. Eng. 2002 , 128 , 138-155. [CrossRef]
2. Shen, X.; Lu, M.; Chen, W. Computing three-axis orientations of a tunnel-boring machine through surveying observation points. J. Comput. Civ. Eng. 2011 , 25 , 232-241. [CrossRef]
3. Shen, X.; Lu, M.; Chen, W. Tunnel-boring machine positioning during microtunneling operations through integrating automated data collection with real-time computing. J. Constr. Eng. Manag. 2011 , 137 , 72-85. [CrossRef]
4. Chanchaya, C.; Suwansawat, S. Directional Control of EPB Shield in Spiral Curve. In Geotechnical Aspects of Underground Construction in Soft Ground ; CRC Press: Boca Raton, FL, USA, 2014; pp. 561-566.
5. Festa, D.; Broere, W.; Bosch, J.W. On the effects of the TBM-shield body articulation on tunnelling in soft soil. In Proceedings of the 3rd International Conference on Computational Methods in Tunnelling and Subsurface Engineering, EURO: TUN 2013, Bochum, Germany, 17-19 April 2013; Aedificatio Publishers: Freiburg, Germany, 2013.
6. Festa, D.; Broere, W.; Bosch, J.W. Kinematic behaviour of a Tunnel Boring Machine in soft soil: Theory and observations. Tunn. Undergr. Space Technol. 2015 , 49 , 208-217. [CrossRef]
7. Kang, S.O.; Kim, H.; Kim, Y.M.; Kim, S.H. Application technique on thrust jacking pressure of shield TBM in the sharp curved tunnel alignment by model tests. J. Korean Tunn. Undergr. Space Assoc. 2017 , 19 , 335-353. (In Korean) [CrossRef]
8. Kang, S.H.; Kim, D.H.; Kim, H.T.; Song, S.W. Study on the structure of the articulation jack and skin plate of the sharp curve section shield TBM in numerical analysis. J. Korean Tunn. Undergr. Space Assoc. 2017 , 19 , 421-435. (In Korean) [CrossRef]
9. Brundan, W.; Danno, H. Tunnel Boring Machines for Extremely Tight Radius Curves. In Geotechnics for Sustainable Infrastructure Development ; Springer: Singapore, 2020; pp. 241-248.
10. TBM Staff. Big Data, Writ Large: Technology to Advance Tunnel Boring. Tunnel Business Magazine (TBM) , 17 April 2020; 24-27.
11. ITA, Working Group 2. Mechanized Tunnelling: Guidelines for the Design of Segmental Tunnel Linings ; ITA-AITES: Paris, France, 2019.

Disclaimer/Publisher's Note: The statements, opinions and data contained in all publications are solely those of the individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or the editor(s) disclaim responsibility for any injury to people or property resulting from any ideas, methods, instructions or products referred to in the content.

Funding: This research was funded and performed as part of the construction technology projects, 'Development of the automated TBM cutterhead design technology and TBM control system' (Project number: 21SCIP-C129646-05), and 'National R&amp;D project for Smart Construction Technology' (Project number: 20SMIP-A158708-04) of the Korea Agency for Infrastructure Technology Advancement (KAIA).

Institutional Review Board Statement: Not applicable.

Informed Consent Statement: Informed consent was obtained from all subjects involved in the study.

Data Availability Statement: Not applicable.

Acknowledgments: The authors appreciate the support of the Korea Agency for Infrastructure Technology Advancement under the Ministry of Land, Infrastructure, and Transport.

Conflicts of Interest: The authors declare no conflict of interest.