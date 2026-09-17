## ORIGINAL RESEARCH PAPERS

## A Model for Optimizing Railway Alignment Considering Bridge Costs, Tunnel Costs, and Transition Curves

<!-- image -->

Icon

Benyamin Ghoreishi 1 · Yousef Shafahi 1 · Seyed Elyas Hashemian 2

<!-- image -->

Icon

Received: 9 November 2018 / Revised: 27 August 2019 / Accepted: 9 September 2019 / Published online: 12 October 2019 Ó The Author(s) 2019

Abstract Owing to wide-ranging searches (there are various alignments between two points) as well as complex and nonlinear cost functions and a variety of geometric constraints, the problem of optimal railway alignment is classified as a complex problem. Thus, choosing an alignment between two points is usually done based on a limited number of alignments designed by experts. In recent years, the study of railway alignment optimization has shown the importance of optimization and the introduction of various algorithms and their usefulness in solving different problems. It is expected that applying meta-heuristic optimization algorithms such as methods based on swarm intelligence can lead to better alignments. In this study, we tried to modify models based on previous studies in order to design and develop a model based on a single framework to provide three-dimensional optimization of alignments applicable in the real world. To obtain this, the particle swarm algorithm is used and a geographic information system is incorporated as a means of search in three-dimensional space. In particular, the cost function used in previous studies considering the costs related to structures (bridges and tunnels) are improved regarding hydraulic structure alignments. Furthermore, the transition curve of horizontal alignment and slope restrictions of curves are considered in this project by using the penalty

&amp; Seyed Elyas Hashemian s.elyas.hashemian@gmail.com

1 Department of Civil Engineering, Sharif University of Technology, Tehran, Iran

2 Department of Civil Engineering, Amirkabir University of Technology (Tehran Polytechnic), Tehran, Iran

Communicated by Paul Schonfeld.

function in order to obtain the most practical results possible. Finally, this study examines three problems for which the results are acceptable in cases of railway alignment geometry and its application in the real world.

Keywords Optimization  Railway alignment  Particle swarm optimization (PSO) algorithm  Transition curves  Bridges and tunnels  Geographic information systems

## 1 Introduction

When solving problems in continuous search space, there are many alignment alternatives between two points, which are characterized by topography, land ownership, and environmental issues. The objective function of the problem depends on various cost factors, which include supplier costs, user costs and out-of-system costs [1].

There are a number of constraints in railway alignment design, which can be classified as Capacity and alignment traffic constraints, Horizontal alignment constraints and Vertical alignment constraints [2].

Given the existing complexities in railway alignment design, researchers have considered many simplifying assumptions for the model railway alignment problem to achieve the proper alignment. Generally, these simplifications have led to final model solutions that are not applicable or cannot approximate the optimal solution obtained from the actual models. This work aims to reduce the simplifying assumptions and to modify optimization methods for existing algorithms. Results show that the applicability of the solutions of the proposed model are improved.

The paper is organized as follows: After the introduction, a review of the literature on methods previously developed for optimizing railway and highway alignments is provided in Sect. 2. Major railway costs and constraints associated with railway construction are discussed in Sect. 3, and the methodology developed for the railway alignment optimization model is introduced. In Sect. 4, we describe how we represent the railway alignment optimization problem in particle swarm optimization algorithms (PSO), and we discuss our approach to modeling railway alignments and structures in Sect. 5. Section 6 describes a basic model formulation. In Sect. 7 we demonstrate the model's capability and feasibility by applying it to real-world problems. Sections 8 and 9 provide a discussion and conclusions drawn from this study.

<!-- image -->

Icon

<!-- image -->

Logo

## 2 Literature Review

Originally, railway alignment design was a 3D optimization model. This model has a multivariate objective function, and there are many nonlinear constraints in it. Because of the behavioral complexity of the three-dimensional profile of the track, it requires a multistep solution to the problem. The three-dimensional solution seems to be a problem owing to a variety of design options and multiplicity of parameters involved. For this reason, in many studies, railway alignment design has been performed in two steps. In the first step, the horizontal alignment is determined, and the vertical alignment is then adjusted correspondingly. Because the horizontal and vertical alignments are interdependent, various studies have explored ways to solve these two problems at the same time [3].

Shafahi and Bagherian [3] categorized highway and rail path optimization models into three broad categories:

- a. Vertical alignment optimization models
- b. Horizontal alignment optimization models
- c. 3D optimization models (simultaneous horizontal and vertical alignment optimization)

Horizontal alignment optimization models are more complex than vertical alignment models, primarily because of the various parameters that must be considered, such as socioeconomic and environmental issues. Shafahi and Shahbazi [1] studied the design of optimal railway alignment using a genetic algorithm. The Shahbazi optimization model is non-backtracking. The vertical alignment is formed within an allowed range along the horizontal alignment for the maximum allowable gradient of the railway track. Turner and Miles [4] reported on a cost/ benefit alignment optimization model using the shortest path in a raster grid. Other studies have used calculus of variations [5-8] and network optimization [9-12].

Many studies in the literature have examined the optimization of vertical alignment. The most important parameter in the vertical alignment cost function is the volume of earthwork. The design of the vertical alignment, the problem of generating backtracking alignment, and the possibility of disconnecting alignments has not been posed because the vertical alignment is designed along the horizontal alignment.

Fwa et al. [13] proposed a method for optimizing vertical alignment by assuming a given horizontal alignment. They considered various constraints on the design of the vertical alignment, such as longitudinal slope, vertical curve, fixed points, and limitations of vertical curve on horizontal curves in the proposed model. A genetic algorithm was used as an optimization method, and a penalty function with a finite fixed unit was used to avoid unacceptable solutions.

The study by Easa [14] was one of the first to focus on alignment optimization. In order to optimize the longitudinal profile of the route and reduce the cost of earthwork, he proposed a model that minimizes the cost of earthwork and also fulfills the necessary geometric characteristics. In his model, the project line creates the necessary balance between earthwork sections (cut and fill sections), and the longitudinal slope and vertical curvature are subject to a maximum limit, while the minimum distance between the successive vertical curves is taken into account.

The major cost associated with the design of the vertical profile of a route is the cost of earthwork, which was addressed in a study by Goktepe et al. [15] on optimizing project line points with regard to the cost of earthwork units (embankment and excavation). They used the concept of weighted ground equivalency (WGE), which was achieved by placing the total embankment and excavation (earthwork) vectors in each cross section.

Studies using dynamic programming algorithms [16-19] and linear programming algorithms [20, 21] have been reported in the field of vertical alignment optimization.

Chew et al. [22] were the first researchers to solve the problem of simultaneous optimization of 3D alignment for horizontal and vertical profiles. They used a numerical search method in their study.

The use of a meta-heuristic algorithm for routing began with Jong's [23] research. Jong and Schonfeld [24] then tried to ameliorate some of the defects using genetic algorithms. They provided a solving order with genetic algorithm changes which are used in routing problems.

Jha and Schonfeld [25] used a geographic information system (GIS) and genetic algorithms to solve the problem of optimal alignment. Assuming that the search area is a rectangular region, they divide this area into a grid with similar square cells. The cells are considered small enough that an assumption of similarity of properties within them

(e.g., land costs, height) is reasonable. Hasany and Shafahi [2] used an ant colony optimization (ACO) method for optimizing railroad alignment. The modeling study was done in continuous space and utilizing GIS. In 2006, De Smith [26] used a network optimization method with limitations on curve radii and alignment gradient for route, railway, and pipeline routing. In the same year, Cheng and Lee [27] provided a 3D route optimization model using the neighborhood search method to determine a horizontal path and mixed hybrid planning to optimize the vertical path. Shafahi and Bagherian [3] used a relatively new and effective method in 2013 to solve the path routing problem with a particle optimization algorithm (bird swarm algorithm). This model uses geospatial data as a search space and performs searches in a continuous environment. Considering the geometric constraints in the design of the route, this model features the ability to produce return routes and the possibility of constructing the bridge and tunnel along the path, aligning with the list table, improving the cost functions used in previous studies and global search capability, and thus finding a near-optimal real-world path. To determine an alignment, first, a number of intersection points are indicated that make a broken and rugged alignment. Then, with the help of other algorithms, the horizontal and vertical curves are matched to achieve a smooth alignment. The intersection points from the optimization problem are variables. The range of these point changes are on lines parallel to one another.

Similarly, Lai and Schonfeld [28] proposed a methodology for concurrent optimization of station locations and rail transit alignment connecting those stations, by accommodating multiple system objectives, satisfying various design constraints, and integrating the analysis models with a GIS database. Li et al. [29, 30] used a genetic algorithm and bidirectional distance transform to optimize railway alignments in mountainous terrain. Concurrent optimization of mountain railway alignment and station locations using a distance transform algorithm was recently reported by Pu et al. [31].

Many studies have been carried out for three-dimensional route optimization with genetic algorithms, including Kim [32], Jong and Schonfeld [24], Tat and Tao [33], Kim et al. [34-37], and Kang et al. [38-41].

## 3 Railway Costs and Constraints

Several parameters directly or indirectly affect the construction or design of a railway track. Initial construction costs have a direct effect on the design (earthwork costs, superstructure costs), but other costs, including user costs and out-of-system costs, have an indirect impact on the design of the alignment, and therefore should be considered in the design process. It is very important that all the critical costs of the project are taken into account when designing the alignment in order to obtain the optimal alignment. Various railway costs have been examined in a number of studies [1, 2]. The costs considered in these articles include the following:

- Right-of-way-dependent costs
- Length-dependent costs
- Traffic-dependent costs
- Volume-dependent costs
- Hydrology and hydrologic-dependent costs
- Bridge- and tunnel-dependent costs

## 3.1 Right-of-Way-Dependent Costs

The costs associated with a road or railway route, depending on the passageway, include land acquisition and other costs for crossing the track from one area. Because of this, the railway track passageway has a special significance. According to the accuracy requirements, the study area is divided into cells with specific dimensions. It is assumed that each cell in the study area represents an area with the same cost of production. Crossing the railways from different cells carries different costs, and the final costs for the location depend on the total costs of the path components in the cells. With this cost system, cells that are located in areas where the railroad does not have to cross them (such as historic sites, or marsh locations or other special locations) can be defined as cells with a very high unit cost. This routing process will cause the total cost of the transit route in this area to be increased, and the probability of choosing it will be reduced.

## 3.2 Length-Dependent Costs

The hypothesized superstructure in this paper is a ballasted one. This type of track includes ballast, tie, fastener, and rail. The use of ballast is very common, as ballasted tracks have very good performance. Although the maintenance cost for this type of track is high, its construction cost is lower than for ballastless tracks. There have been no major changes in the principles of ballasted superstructures since railway tracks first emerged, but certain developments have occurred within the railway transport industry in order to promote greater safety and speed, such as continuous welded rail (CWR), the use of concrete ties and heavier rail sections, elastic fastenings, machining repair operations, and the development of advanced equipment for measuring various parameters of track components, maintenance management, and so on.

<!-- image -->

Icon

## 3.3 Traffic-Dependent Costs

In road design, typically only the costs of route construction are reviewed, while the effect of alignment selection in railways involves other costs, including operating costs. In this paper, in addition to construction costs, operating costs are also considered, which include the following [2]:

- a. The cost of purchasing, maintaining, and replacing rolling stock
- Locomotive purchases
- Locomotive maintenance
- Wagon purchases
- Wagon maintenance
- b. Track maintenance and reconstruction cost
- c. Cost in terms of the value of cargo and passenger time

## 3.4 Volume-Dependent Costs

In this paper, the average end-area method is used to calculate the volume of earthwork [42]. To calculate the volume of earthwork (excavation and embankment operations) on horizontal alignment at specified intervals, the area of transverse sections (stations) is determined, and the volume of soil operations between the two stations is then calculated. Accuracy in estimating the volume of earthwork is dependent on the distance between stations. When the distance is smaller, a more accurate estimate of earthwork will be achieved [43]. Here, for calculating the volume of earthwork, the distance between stations is considered to be identical and equal to 50 m.

## 3.5 Hydrology and Hydrologic-Dependent Costs

Since moisture and pore water pressure play a decisive role in the durability of ballast aggregates, the strength of construction, and stability of slopes, surface and underground water control are considered as key factors in the design and maintenance of railways. Given the importance of this issue with regard to railways, in this paper we have tried to consider the costs of the alignment of hydrologic affairs as much as possible.

Here, for transverse drainage, an approximate objective function is used. This function was developed using studies to determine the hydraulic sections in the second phase of the Chabahar-Zahedan railway project in Iran. We have tried to consider the mountainous and plain areas separately. In this case study (the second phase of the Chabahar-Zahedan railway project), the alignment was in the plain area from 15 to 85 km, and so a culvert was used every 370 m on average. Alignment was also considered to be a mountainous area from 85 to 155 km, with an average of 290 m used for the distance between the culverts (in a type of cost depending on the alignment length and location). In addition, the dimensions of the technical hydraulic structures used vary depending on the project and existing ground line location, and the average cost of each project is considered. Therefore:

<!-- image -->

Icon

<!-- formula-not-decoded -->

C H1 is the cost of technical structures in the plain areas, L is alignment length (m), and C is the average cost of one technical structure.

<!-- formula-not-decoded -->

C H2 is the cost of technical structures in mountainous areas, L is alignment length (m), and C is the average cost of one technical structure.

## 3.6 Bridge- and Tunnel-Dependent Costs

Bridges and tunnels are used as a substitute for bulky embankments and excavations as well as a solution for crossing inaccessible areas such as rivers. Given the complexity of the cost function of the bridge and tunnel and its dependence on various parameters such as topography and land diversification, calculating the cost of construction and efficiency, and determining the optimal location of the bridge and tunnel becomes a complex problem. Because of the high cost of a bridge or tunnel, its proper alignment during the design stage can prevent substantial waste. In this section, the use of bridges and tunnels in alignment optimization is investigated. Here, only an approximate estimate of the cost of bridge construction is required, and thus some errors are neglected. To estimate the bridge construction cost, the linear cost function provided by O'Connor [44] is used. Given that bridge maintenance and repair is of great importance, a previously proposed method [39] was used to estimate the bridge maintenance. The cost for the tunnel is considered according to the formulas presented in [43]. In this paper, we have tried to take an additional step in order to complete the alignment of the railway tracks, taking into account the bridge and tunnel and adding it to the original model. In order to determine the position of the alignment required for the construction of a technical structure, the following are considered:

- If the excavation height exceeds the permissible level according to the material, then a tunnel needs to be constructed.
- If the height of the embankment exceeds the virtual limit, it is necessary to construct a bridge along the alignment.
- The bridge should be constructed if an alignment passes through an environmentally sensitive, marshy or riverbound area with operational problems on the embankment.

## 3.7 Constraints in Railway Track Alignment

Limitations on the design of railroad geometry are a major consideration. Several studies have investigated how to consider the constraints in evolutionary and ontological methods. Six general approaches were mentioned in [45] and their cases were explained in [3]. The alignment problem-solving method chosen in the present work is based on artificial intelligence. In the following, the proposed solving method for dealing with the constraints in this paper, which is based mainly on the definition of the appropriate penalty function for violating any of these constraints, is described. Considering that there are many constraints in the design of the railway alignment, in this paper, in order to achieve an alignment that is feasible to implement in the real world, the following three important constraints are considered in the model:

1. Minimum radius of horizontal curve
2. Minimum vertical curve length
3. Maximum longitudinal slope of the alignment

## 3.7.1 Penalty Function for Violating the Minimum Horizontal Curve Radius

As long as the minimum radius of the track can be met along the way, the curvature limits of the alignment have been fulfilled. However, due to the small distance between the two points of intersection, there may be a discontinuity in horizontal alignment which is solved this problem using the algorithm reported in [46]. If the radius of the existing alignment is less than the minimum allowed radius of the route ( R min) according to Formula (3) (288 code in Iran), for the penalty of the alignment, the method presented in [47] is used.

<!-- formula-not-decoded -->

V max and V min is the speed of passenger and freight trains, respectively (km = h), Rm ð i Þ is minimum circular curve radius (m).

## 3.7.2 Penalty Function for Violating the Minimum Vertical Curve Length

In order to observe the minimum vertical curve length, an approach similar to that of the horizontal curve radius is used. To correct the discontinuity of the vertical curves, the method presented in [43] is used. If the minimum length of the vertical curve is less than the minimum allowed length of the vertical curve ( L min) according to Formula (5) [48], the penalty of the alignment presented in [47] is used.

<!-- formula-not-decoded -->

Lmi : minimum vertical curve length (ft.), D : the absolute magnitude of the slope variation on both sides of the curve (decimal), V : design speed (mph), K : conversion ratio (2.15), and A : the vertical acceleration, equal to 0.6 for passenger trains and 0.1 for freight trains

The minimum length of the vertical curve relative to the speed of the freight and passenger trains is equal to the maximum of the following:





<!-- formula-not-decoded -->

## 3.7.3 Penalty Function for Violating the Maximum Gradient of the Alignment

For the penalty function in the case of nonobservance of the maximum gradient for successive intersections i and i ? 1, a similar approach was encountered with two previous modes. The maximum allowed gradient for this part is considered to be 1.25%.

## 4 Representation of Railway Alignment in PSO

In the proposed railway alignment optimization model, a horizontal alignment is defined by the tangents, circular curves, and the connecting transition curve sections. A vertical alignment is defined by the graded tangents connected with parabolic curves. This arrangement of elements depends on the points of intersection of the horizontal alignment (PIs), so the definition of generating alignments can be summarized in the choice of different points of intersection. In this paper, the PSO algorithm is used to find the optimal railway track alignment.

<!-- image -->

Icon

The particle swarm optimization (PSO) algorithm is a one of the wide category of swarm Intelligence methods for solving optimization problems. The basic PSO algorithm was developed by Kennedy and Eberhart [49] and Tu et al. [50]. Execution of the PSO algorithm to solve highway alignment optimization problems is convenient for two reasons. First, PSO is inherently designed to solve continuous problems, and its efficiency has been reported in previous studies. Second, unlike the other algorithms proposed for highway alignment optimization (e.g., genetic algorithms), the PSO implicitly considers the spatial relations during the search process. Therefore, this algorithm can be considered as a promising method for alignment optimization problems [3].

PSO can be easily implemented, and it is computationally inexpensive compared with genetic algorithms, since its memory and CPU speed requirements are lower [50].

In the basic PSO algorithm, the position ( x ) and velocity ( v ) of each particle in the swarm can be updated after each iteration, using the following equations:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where C 1 and C 2 are the accelerator constants, r 1 and r 2 are randomly generated numbers distributed uniformly in the [0, 1] interval, g is the best solution found by the population to that point, and p is the best solution found by each particle.

There are many extensions of the basic PSO designed to improve its convergence behavior. Shi and Eberhart [51] introduced the ''inertia weight model,'' in which the inertia of the particle [the v ( t ) term] is multiplied by a parameter w , known as inertia weight. Consequently, Eq. (7) can be rewritten as

<!-- formula-not-decoded -->

In this equation, the inertia weight can either stay constant or decrease during the execution of the algorithm. Another modification is velocity clamping [52]. In each iteration, if the calculated displacement of a particle exceeds the specified maximum velocity, it is set to the maximum value. Let V max, j denote the maximum velocity allowed in dimension j . The particle velocity is then adjusted before the position update using  

<!-- formula-not-decoded -->

<!-- image -->

Icon

where v 0 ij ð t þ 1 Þ is the speed of the particle, obtained from Eq. (8), and vij ð t þ 1 Þ equals the modified value which is considered to be the particle's speed at step t ? 1.

In this model, each alignment is represented by a particle. Each particle contains the coordinates of the point of intersection [ PIi ( xi , yi , zi )] which is shown as PI in the model. In the PSO algorithms used for the railway alignment optimization model, first, a number of initial alignments are generated (each of which represents a particle). The various methods for producing the initial alignments are fully described by Shafahi and Bagherian [3]. In this paper, to cover the entire zone, the alignments are generated randomly at the study area. According to the studies conducted in this field and solving various examples, 25 alignments (particles) were selected as the initial alignment and 100 repetitions were considered as the criterion for stopping the PSO algorithms. Figure 1 shows orthogonal cutting planes where the PIs of a railway alignment are generated. The total number of cutting planes indicates the number of points of intersection. Here, the distance between the cutting planes is chosen to be equal, and each PI on these cutting planes has its own coordinates x , y , z . These points are generated in each replication of the algorithm for optimal alignment.

The number of cutting planes that are used affects the shape and even the cost of the alignment generated. For urban areas or areas with more complex topography, increasing the number of cutting planes will increase the accuracy of the solution, and for areas with simple topography or that are outside the city, an optimal solution can be achieved with fewer cutting planes [46]. Therefore, in this paper, the number of cutting planes is selected depending on the studied region, which is investigated in the results section.

It is important to note that in this paper, the cutting plane method was used, and since the alignment is non-backtracking, this method is not suitable for mountainous regions, as they have a length limit and should be backtracked.

## 5 Modeling Railway Alignments

## 5.1 Horizontal Alignment Model

The railway horizontal alignment is composed of a series of tangent and horizontal curves. Horizontal curves include transition and circular curves. Transition curves are typically used between the straight alignment (tangent) and the circular curve. This prevents a sudden change in the curve radius, and when travel from the straight alignment to the circular curve occurs, transition curves prevent an increase in lateral acceleration. In railways, the implementation of transition curves has particular importance.

Fig. 1 A series of points of intersection generated on corresponding orthogonal cutting planes [46]

<!-- image -->

Engineering drawing

## 5.2 Horizontal Alignment Model Formulation

Figure 2 shows an example of a horizontal alignment with point of intersection ( PIi ), circular curves and transition curves. The start and end points of the alignment are shown respectively by S and E. The important points used in the curve are defined in Table 1. It is clear in Fig. 2 that the points STi and TSi þ 1 are connected to each other by the direct line between PIi and PIi þ 1, point TSi is connected to SCi and CSi to STi by a transition curve, and SCi to CSi by a circular curve ( 8 i ¼ 1 ; . . . ; n ).

If the deviation angle of a PI is zero, then that point contains all points TSi , SCi , CSi , STi , and PIi .

To formulate the alignment, first, the coordinates of the intersection points are determined on the cutting planes. Then the coordinate positions TSi , SCi , CSi , and STi are calculated for ( 8 i ¼ 1 ; . . . ; n ). Figure 3 shows the details of the transition and circular curves [46].

Fig. 2 Horizontal alignment plan [46]

In Fig. 3, AB and CD are connected by a transition curve (clothoid) and BC by a circular curve . The point A ( TSi ) is the start of the clothoid and has an infinite radius (mean Rsi ¼ 1 in TSi ) and a curve degree of zero. The radius of the transition curve along its length ( l si ) decreases slowly until it reaches the radius of the circular curve at point B, which is the end point of the clothoid and the beginning of the circular curve (mean Rsi ¼ Rci in SCi ). These rules are also applied on the other side of the curve. A complete calculation can be seen in [53].

The point TSi is the starting point for the clothoid on the line between PIi   1 and PIi , and the distance between PIi and TSi is displayed by LTSi . The point STi is the starting point of the tangent on the other side of the curve; it is between points PIi and PIi þ 1, and its distance from point PIi is equal to the length LTSi . The next point, which represents the end of the clothoid and the beginning of the circular curve, is represented by SCi . The point CSi also

<!-- image -->

Line chart

<!-- image -->

Logo

Table 1 Definition of the critical points used in the horizontal curve [46]

## Points Definition

- TSi The point where the tangent of the alignment connects to the transition curve (the beginning of the transition curve) 8 i ¼ 1 ; . . . ; n
- SCi The point where the transition curve connects to the circular curve (the end of the transition curve and the beginning of the circular curve) 8 i ¼ 1 ; . . . ; n
- CSi The point where the circular curve connects to the transition curve (the end of the circular curve and the beginning of the transition curve) 8 i ¼ 1 ; . . . ; n
- STi The point where the transition curve connects to the tangent of the alignment (the end of the transition curve and the beginning of the alignment tangent) 8 i ¼ 1 ; . . . ; n

Fig. 3 Geometric properties of a horizontal curve with two clothoid curves and a circular curve [46]

<!-- image -->

Engineering drawing

connects the circular curve to the transition curve (clothoid) in the other direction. In accordance with the equations in the Appendix, the coordinates of the points can be calculated [46].

## 5.2.1 Condition for Establishing a Transition Curve

As seen in Fig. 3, the conditions for establishing the connecting curve are as follows:

<!-- formula-not-decoded -->

h PIi : deviation angle of main tangents for each PIi , and h STi : deviation angle of clothoid h STi ¼ LTS i 2 RC i

If this condition is not met, the curve cannot be fitted with geometric specifications. In this paper, the algorithm for horizontal curves is implemented in such a way that a circular curve with a large radius is used instead of the curve with the clothoid-circle-clothoid properties. In such a situation where the alignment has a geometric problem, a circular curve with a radius greater than 3000 m is used, in which there is no need to apply the superelevation for the railway alignment. Because of the lack of cant, no further use of clothoid is required.

<!-- image -->

Icon

## 5.3 Determining the Vertical Cutting Plane

In order to achieve three-dimensional alignment, a vertical plane is assumed on a cutting plane which allows the generation of three-dimensional alignments. In this paper, these vertical planes are limited to the maximum and minimum possible height in its top and bottom and search is performed in this range. Figure 5 shows the HZ diagram of an alignment, whose horizontal axis represents the length of the alignment and vertical axis represents the alignment height. In this graph H is the length of the alignment and Z is the altitude (height) [43]. As shown in Fig. 4, in this paper, the vertical curve on the alignment is used from the circular curve midpoint. The algorithm checks that the vertical curves are not located on the horizontal transition curves, and if this happens, the model will reduce the vertical curve length to overlap only the vertical curve with the horizontal circular curves. The coordinates of this point are determined by the following equation on the horizontal alignment:    

Fig. 4 Geometric relationship of the reference points for designing the vertical curve on the alignment plan

<!-- image -->

Line chart

<!-- formula-not-decoded -->





where x d i y d i corresponds to the coordinates of the circular curve center.

At points VPIi ; . . . ; VPIn þ 1 the vertical curve is braced to makethe alignment smoother. The coordinates of points VPI 0 and VPIn þ 1 are the coordinates of the points at the beginning and the end of the alignment, respectively. Therefore, the length of the horizontal alignment to point VPIi must be calculated for each point to determine the horizontal axis VPIi in the longitudinal profile (vertical alignment).

## 6 Basic Model Formulation

The objective function of this problem is a total cost function ( CT ) comprising nine major components: environmental costs ( CN ), earthwork costs ( CE ), length-dependent costs ( CL ), track maintenance costs ( CM ), bridgeand tunnel-dependent costs ( CB ), hydrology and hydrologic-dependent costs ( CH ), penalty for violating the minimum horizontal curve radius ( CR ), penalty for violating the minimum vertical curve length ( CV ), penalty for violating the maximum gradient of the alignment ( CG ). Therefore, a basic formulation for minimizing the total cost of railway alignments can be expressed as follows:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Ri ; Li and gi : based on the corresponding calculations obtained in the model. R min ; L min and g min: the calculations are presented in the previous sections.

The functions are fully described in Sect. 3.

## 7 Case Studies

In this part of the paper, three examples are discussed. The first example is hypothesized to validate the model. In the second and third examples, real cases using topographic data obtained from maps of 1/25,000 of a region between the cities of Isfahan and Shahreza in Isfahan province are considered, with two different points at the beginning and the end.

## 7.1 Design Parameters and Constraints Considered to Solve Examples

In the proposed model, three main constraints regarding the geometric design of the railway alignment are considered and are described, and explanations are provided as to how to deal with these constraints. In each of the three examples, the proposed railway track has a design specification in accordance with Table 2.

The distance between the stations is considered 50 m to calculate the earthwork volume.

## 7.2 Parameters Considered for the Problem-Solving Algorithm

To use the problem-solving algorithm that is fully described in Chapter 5, the parameters in Table 3 are used. It should be noted that in this paper, each of the alignments is considered a particle, and the initial solutions were produced randomly. The program's stop requirement is set to be 100 repetitions.

Table 2 Railway design assumptions

| Characteristic                      | Value   |
|-------------------------------------|---------|
| Passenger train design speed (km/h) | 160     |
| Freight train design speed (km/h)   | 80      |
| Ballast (cm)                        | 45      |
| Tie type                            | B70     |
| Rail type                           | UIC 60  |
| Cut slope                           | 1:2     |
| Fill slope                          | 1:2     |

<!-- image -->

Logo

Table 3 The constant parameters of the PSO algorithms

| Characteristic                      | Value                          |
|-------------------------------------|--------------------------------|
| Accelerator coefficients            | c 1 ¼ c 2 ¼ 2                  |
| Inertial weight                     | x ¼ 0 : 1-0.6 (linear)         |
| Maximum speed in each dimension     | Equivalent to 10% of its range |
| Number of primary particles (paths) | 25 particles (path)            |
| Algorithm repetitions               | 100 repetitions                |

Fig. 5 Control points on HZ profile [43]

<!-- image -->

Line chart

## 7.3 Number of Cutting Planes

In the alignment optimization problem, the number of cutting planes [representing the number of points of intersection (PIs) pathway] can vary for different regions. For example, for urban areas that have many complexities (the urban train alignment optimization problem), an increased number of cutting planes should be considered in order to obtain better results, but for suburban regions, this number can be smaller given the lower complexity (for example, the problem of optimizing the alignment of suburban railways).

As the number of points of intersection (and hence the number of cutting planes) increases, the calculation time increases. In each of the three examples, the number of cutting planes was considered for several different conditions and the solutions were compared. In order to make the design more realistic, these unit costs are based on the price list for the technical structure of the road and railways in 2014. In the following sections, the results and outputs obtained from the hypothetical example are first examined, and then the results of the second and third examples are presented as case studies of the Isfahan-Shahreza area.

<!-- image -->

Icon

Fig. 6 Horizontal alignments with different numbers of cutting planes in Example 1

<!-- image -->

Geographical map

## 7.4 The First Example

The study area is assumed to be a hypothetical domain as shown in Fig. 5. To investigate the model performance, the area is designed with a variety of restrictions and has two hills and one lake. The map dimensions in the east-west (EW) and north-south (NS) directions are equal to 10,800 and 8700 m, respectively. The origin coordinates in the lower left-hand side of the map are assumed to be ( x = 0, y = 0).

In this case, the positions of the first station and the last station are shown in Fig. 6. Cell dimensions are considered for calculating the costs mentioned in Chapter 3. These dimensions are considered to be 5 m in the first example and 10 m in the second and third examples in the transverse and longitudinal directions.

Because of the importance of the number of cutting planes in solving the alignment optimization problem, we first attempted to evaluate the effect of the number of cutting planes. As previously mentioned, increasing the number of cutting planes increases the horizontal and vertical curves and increases the solving time. Here, four different numbers of cutting planes (2, 3, 4, and 5) are used. In Fig. 6, the plan with the considered alignments is displayed. Fig. 7 shows the vertical alignment. As expected, the alignments generated for different modes differ from one another due to the differences in the number of cutting planes (and thus the number of horizontal and vertical curves). The comparison of the alignments, as expected, shows that the alignment from the application of five cutting planes has a lower cost than the alignments produced

<!-- image -->

Line chart

- (a) Vertical alignment obtained from 2 cutting planes

with the lower cutting line. The profiles of the above alignments are presented in Table 4.

## 7.4.1 Sensitivity Analysis of Model Parameters

In this section, sensitivity analysis of the parameters used in the objective function is carried out. In all of these analyses, the alignments are constructed by assuming five cutting planes.

Two scenarios were designed to analyze the model performance. In the first scenario, all costs except the cost of earthwork, bridge, and tunnel are considered, and in the second scenario, the earthwork cost is added to the model to be evaluated.

7.4.1.1 Scenario 1: Solving the Model Taking into Account the Length-Dependent Costs (All Costs Except Costs Related to the Volume of Earthwork, Bridges, and Tunnels) In this case, the model provides an alignment

<!-- image -->

Line chart

- (b) Vertical alignment obtained from 3 cutting planes
- (c) Vertical alignment obtained from 4 cutting planes
- (d) Vertical alignment obtained from 5 cutting planes

<!-- image -->

Line chart

<!-- image -->

Line chart

Fig. 7 The vertical alignments with different numbers of cutting planes in Example 1

<!-- image -->

Logo

Table 4 Comparison of alignment cost in Example 1

|   Number of cutting planes |   Alignment cost during the project period (  10 6 |   $ ) Maximum longitudinal gradient (%) |   Alignment length (m) |
|----------------------------|-----------------------------------------------------|-----------------------------------------|------------------------|
|                          2 |                                              164.36 |                                    0.75 |               11,883.7 |
|                          3 |                                              162.05 |                                     0.6 |               11,991.2 |
|                          4 |                                              161.03 |                                     0.9 |               12,361.5 |
|                          5 |                                              160.51 |                                     0.5 |               12,346.2 |

Fig. 8 Horizontal alignment for Scenario 1, Example 1

<!-- image -->

Topographical map

regardless of the cost of the earthwork, bridges ,and tunnels. Specifically, the final solution is a straight line that connects the origin and destination, and of course, all of the alignment restrictions are followed, and that is what was expected. Figure 8 shows the horizontal alignment and Fig. 9 shows the vertical alignment.

7.4.1.2 Scenario 2: Solving the Model with All Costs Without the Possibility of Having a Bridge or Tunnel In this scenario, since the model lacks the exploration of the bridge and tunnel option, it is expected that the optimal alignment will make detours around hills and lakes to avoid a high volume of earthwork. It should be noted that in this model, due to the lack of technical structures of the bridge and tunnel, the maximum altitude for earthwork is not considered, and the model assumes that the alignment can pass through the river and the lake at the embankment. As expected, the alignment tries to cross an area that is smaller in width than the rest of the river, and it is assumed that the river connected to the lake can be filled with soil and at a single cost such as drought. This is just a matter of sensitivity analysis, and it is clear that the result will not be an acceptable alignment.

<!-- image -->

Logo

Fig. 9 Vertical alignment for Scenario 1, Example 1

<!-- image -->

Line chart

In this example, the maximum slope is 0.5%. Figure 10 shows the map of the resulting alignment from the implementation of the model, and Fig. 11 shows the vertical alignment. As expected, the proposed alignment also detours around the mountain and the lake to avoid earthwork costs.

## 7.5 The Second Example

The region selected as the study area in Example 2 is an area of almost all plain and hillside near the city of Isfahan, as shown in Fig. 12. The origin of the map is equal to ( x = 559,081.537, y = 3,540,762.092). The area in the EW and NS direction is 23,270 m and 27,595 m respectively. In this example, the positions of the beginning of the alignment (first station) and the end of the alignment (the last station) are shown in Fig. 13.

In this example, the model is executed for the four different modes, with 11, 13, 15, and 17 cutting planes. The plan for the resulting alignments is displayed in Fig. 13. As expected, the alignments generated for different modes vary slightly due to the differences in the number of cutting planes (and consequently the number of horizontal and vertical curves). Figure 13 shows the horizontal alignments, and the vertical alignments are given in Fig. 14. The cost of these alignments is presented in Table 5. As expected, the alignment generated for the largest number of cutting planes (17 cutting planes) has the lowest cost.

Fig. 10 Horizontal alignment for Scenario 2, Example 1

<!-- image -->

Topographical map

Fig. 11 Vertical alignment for Scenario 2, Example 1

<!-- image -->

Line chart

Fig. 12 The study area in Example 2

<!-- image -->

Geographical map

Fig. 13 Horizontal alignments for different numbers of cutting planes in Example 2

<!-- image -->

Geographical map

## 7.6 The Third Example

The study area for Example 3 includes the region in the second example and its surroundings south of Isfahan province and north of Shahreza. The area was selected to include the Isfahan and Shahreza railway stations, in order to compare the alignment produced by the model with the current alignment of the Isfahan-Shahreza railway. This region, as previously mentioned, is almost all plain and hill-like terrain, and is shown in Fig. 15. The origin of the map is equal to ( x = 589,081.537, y = 3,540,762.092). The length of the area in the EW and NS direction is 35,225 and 41,300 m, respectively. The coordinates of the first station are equal to ( x = 579,069.785, y = 550,198.34, z = 1845.5), and the last station coordinates are equal to ( x = 579,069.785, y = 3,581,720.48, z = 1680). The alignment production by the model with different numbers of cutting planes showed that the alignment obtained with the most cutting planes (17) is the best alignment, as was also the case in Example 2. Horizontal and vertical alignments are displayed in Figs. 16 and 17, respectively. The cost of these alignments is presented in Table 6.

The track between the two cities of Isfahan and Shahreza is also shown in yellow. As we can see, the alignment obtained according to the proposed model differs from the existing alignment. Due to the inaccessibility of the longitudinal profile of the existing alignment and the impossibility of calculating the volume of earthwork or the

<!-- image -->

Logo

<!-- image -->

Line chart

- (c) Vertical alignment obtained from 15 cutting planes
- (d) Vertical alignment obtained from 17 cutting planes

Fig. 14 The vertical alignments with the different numbers of cutting planes in Example 2

Table 5 Comparison of alignment costs in Example 2

|   Number of cutting planes |   Alignment cost during the project period (  10 6 |   $ ) Maximum longitudinal gradient (%) |   Alignment length (m) |
|----------------------------|-----------------------------------------------------|-----------------------------------------|------------------------|
|                         11 |                                              394.81 |                                     1.2 |              37,366.76 |
|                         13 |                                              371.78 |                                    1.15 |              39,532.12 |
|                         15 |                                              361.54 |                                    1.25 |              38,802.80 |
|                         17 |                                              353.83 |                                    1.22 |              38,993.15 |

number of bridges and tunnels along the alignment, a comparison of the alignment costs obtained in this paper with the existing alignment was limited to the length of the alignment and its corridor. According to Google Earth, the length of the existing alignment is approximately 50 km. Therefore, the present study is only able to compare the passing location and the alignment length with that discussed for this model. It should be noted that the final alignment in the model is shorter than the existing alignment.

<!-- image -->

Logo

## 8 Discussion

In this work, the first example was hypothetical and meant to validate the model. The second example was evaluated based on real topography, and finally, the third example was a case study of the region between Shahreza and Isfahan.

The computer system used to run the model has the following characteristics.

Fig. 15 The study area in Example 3

<!-- image -->

Photograph

Fig. 16 Horizontal alignments with different numbers of cutting planes in Example 3

- Processor: Intel Ò Core TM i7 CPU
- RAM: 8 GB
- System type: 64-bit operating system

A period of approximately 6 hours was needed to run the largest problems in this paper with the above-mentioned computer setup.

In each example, a different number of cutting planes (with different values) was used in this model. As expected, it was shown that the model provided different solutions by changing the number of orthogonal cutting planes. Due to the high geometrical constraints of railway alignments, it is important to include bridges and tunnels in the model. Using transition curves for the railway alignment plays a very important role in avoiding abrupt changes in radii of alignments and increased lateral acceleration when trains approach curves from a straight alignment.

<!-- image -->

Geographical map

<!-- image -->

Logo

<!-- image -->

Line chart

<!-- image -->

Line chart

- (a) Vertical alignment obtained from 11 cutting planes
- (b) Vertical alignment obtained from 13 cutting planes

2400

<!-- image -->

Line chart

- (c) Vertical alignment obtained from 15 cutting planes
- (d) Vertical alignment obtained from 17 cutting planes

<!-- image -->

Line chart

Fig. 17 Vertical alignments with different numbers of cutting planes in Example 2

Table 6 Comparison of alignment costs in Example 3

|   Number of cutting planes |   Alignment cost during the project period (  10 6 |   $ ) Maximum longitudinal gradient (%) |   Alignment length (m) |
|----------------------------|-----------------------------------------------------|-----------------------------------------|------------------------|
|                         11 |                                              492.34 |                                       1 |                 51,800 |
|                         13 |                                              497.42 |                                    1.15 |               52,685.2 |
|                         15 |                                              487.17 |                                    1.12 |                 48,949 |
|                         17 |                                              482.05 |                                    1.22 |               48,895.7 |

## 9 Conclusion

This paper presented a railway alignment optimization model in which the sensitivity costs of alignments considering their geometric characteristics were included. Also, the solutions obtained were applicable in real-world scenarios. In this model, particle swarm optimization was used. The highlights of this paper can be noted as follows:

<!-- image -->

Icon

1. Three-dimensional optimization considering the transition curve on the horizontal alignment
2. Considering the possibility of constructing bridges and tunnels on the railway alignment
3. Considering the different characteristics of the railway alignment design to find the alignment that is most applicable
4. Improving the cost function used in previous studies and modifying simplifications that reduced the accuracy of the calculations

5. Handling data in a geographic information system
6. Using particle swarm optimization in railway alignment optimization.

Open Access This article is distributed under the terms of the Creative Commons Attribution 4.0 International License (http://crea tivecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license, and indicate if changes were made.

## Appendix

Find deflection angle ( h PIi ) at each PIi 8 i ¼ 1 ; . . . ; n : :  

<!-- formula-not-decoded -->

k k : corresponding vector length,  : internal multiplication. Find TSi and STi ( 8 i ¼ 1 ; . . . ; n : ):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->





<!-- formula-not-decoded -->

Find d i and Mi ( 8 i ¼ 1 ; . . . ; n : ):

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Find SCi and CSi ( 8 i ¼ 1 ; . . . ; n : ): 



<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## References

1. Shafahi Y, Shahbazi MJ (2012) Optimum railway alignment. Int J Commun Netw Syst Sci 5(9A)
2. Hasany RM, Shafahi Y (2016) Ant colony optimisation for finding the optimal railroad path. Paper presented at the Proceedings of the institution of civil engineers-transport
3. Shafahi Y, Bagherian M (2013) A customized particle swarm method to solve highway alignment optimization problem. Comput Aided Civ Infrastruct Eng 28(1):52-67
4. Turner AK, Miles RD (1971) The GCARS system: a computerassisted method of regional route location (No. 348)
5. Howard BE, Bramnick Z, Shaw J (1969) Optimum curvature principle in highway routing. J Highw Div 94:61-82
6. Shaw JF, Howard BE (1982) Expressway route optimization by OCP. J Transp Eng 108(TE3):227-243
7. Thomson N, Sykes J (1988) Route selection through a dynamic ice field using the maximum principle. Transp Res Part B Methodol 22(5):339-356
8. Wan F (1995) Introduction to the calculus of variations and its applications. CRC Press, Boca Raton
9. OECD (1973) Optimization of road alignment by the use of computers. Organisation for Economic Co-operation and Development, Paris
10. Parker NA (1977) Rural highway route corridor selection. Transp Plan Technol 3(4):247-256
11. Trietsch D (1987) Comprehensive design of highway networks. Transp Sci 21(1):26-35
12. Trietsch D (1987) A family of methods for preliminary highway alignment. Transp Sci 21(1):17-25
13. Fwa T, Chan W, Sim Y (2002) Optimal vertical alignment analysis for highway design. J Transp Eng 128(5):395-402
14. Easa SM (1988) Selection of roadway grades that minimize earthwork cost using linear programming. Transp Res Part A Gen 22(2):121-136
15. Goktepe AB, Lav AH, Altun S (2005) Dynamic optimization algorithm for vertical alignment of highways. Math Comput Appl 10(3):341-350
16. Fwa T (1989) Highway vertical alignment analysis by dynamic programming. Transp Res Rec 1239:2-3
17. Goh C, Chew E, Fwa T (1988) Discrete and continuous models for computation of optimal vertical highway alignment. Transp Res Part B Methodol 22(6):399-409
18. Murchland J (1973) Methods of vertical profile optimisation for an improvement to an existing road. Paper presented at the PTRC seminar proceedings, cost models and optimization in highways
19. Puy Huarte J (1973) OPYGAR: optimisation and automatic design of highway profiles. Paper presented at the PTRC seminar proceedings on cost models and optimization in highways, session L
20. Chapra SC, Canale RP (1988) Numerical methods for engineers, vol 2. McGraw-Hill, New York
21. Revelle CS, Whitlatch E, Wright J (1997) Civil and environmental systems engineering. Prentice Hall, New Jersey
22. Chew E, Goh C, Fwa T (1989) Simultaneous optimization of horizontal and vertical alignments for highways. Transp Res Part B Methodol 23(5):315-329
23. Jong J (1998) Optimizing highway alignments with genetic algorithms. University of Maryland, College Park. Ph.D. dissertation
24. Jong J-C, Schonfeld P (2003) An evolutionary model for simultaneously optimizing three-dimensional highway alignments. Transp Res Part B Methodol 37(2):107-128
25. Jha M, Schonfeld P (2000) Geographic information system-based analysis of right-of-way cost for highway optimization. Transp Res Rec J Transp Res Board 1719:241-249
26. De Smith MJ (2006) Determination of gradient and curvature constrained optimal paths. Comput Aided Civ Infrastruct Eng 21(1):24-38

<!-- image -->

Logo

27. Cheng J-F, Lee Y (2006) Model for three-dimensional highway alignment. J Transp Eng 132(12):913-920
28. Lai X, Schonfeld P (2016) Concurrent optimization of rail transit alignments and station locations. Urban Rail Transit 2(1):1-15
29. Li W, Pu H, Schonfeld P, Zhang H, Zheng X (2016) Methodology for optimizing constrained 3-dimensional railway alignments in mountainous terrain. Transp Res Part C Emerg Technol 68:549-565
30. Li W, Pu H, Schonfeld P, Yang J, Zhang H, Wang L, Xiong J (2017) Mountain railway alignment optimization with bidirectional distance transform and genetic algorithm. Comput Aided Civ Infrastruct Eng 32(8):691-709
31. Pu H, Zhang H, Li W, Xiong J, Hu J, Wang J (2019) Concurrent optimization of mountain railway alignment and station locations using a distance transform algorithm. Comput Ind Eng 127:1297-1314
32. Kim E (2001) Modeling intersections and other structures in highway alignment optimization. University of Maryland, College Park
33. Tat CW, Tao F (2003) Using GIS and genetic algorithm in highway alignment optimization. Paper presented at the Intelligent transportation systems, 2003. proceedings. IEEE
34. Kim E, Jha MK, Lovell DJ, Schonfeld P (2004) Intersection modeling for highway alignment optimization. Comput Aided Civ Infrastruct Eng 19(2):119-129
35. Kim E, Jha MK, Schonfeld P (2004) Intersection construction cost functions for alignment optimization. J Transp Eng 130(2):194-203
36. Kim E, Jha MK, Schonfeld P, Kim HS (2007) Highway alignment optimization incorporating bridges and tunnels. J Transp Eng 133(2):71-81
37. Kim E, Jha MK, Son B (2005) Improving the computational efficiency of highway alignment optimization models through a stepwise genetic algorithms approach. Transp Res Part B Methodol 39(4):339-360
38. Kang M, Yang N, Schonfeld P, Jha M (2010) Bilevel highway route optimization. Transp Res Rec J Transp Res Board 2197:107-117
39. Kang MW (2008) An alignment optimization model for a simple highway network. University of Maryland, College Park
40. Kang MW, Schonfeld P, Jong JC (2007) Highway alignment optimization through feasible gates. J Adv Transp 41(2):115-144
41. Kang MW, Schonfeld P, Yang N (2009) Prescreening and repairing in a genetic algorithm for highway alignment optimization. Comput Aided Civ Infrastruct Eng 24(2):109-119
42. Wright P, Dixon K (2004) Highway engineeringm, 7th Edn. Wiley, Hoboken
43. Jha MK, Jha MK, Schonfeld P, Jong J-C (2006) Intelligent road design, vol 19. WIT Press, Ashurst Lodge
44. O'Connor C (1971) Design of bridge superstructures. Wiley, New York
45. Li X, Engelbrecht AP (2007) Particle swarm optimization: an introduction and its recent developments. Paper presented at the Proceedings of the 9th annual conference companion on genetic and evolutionary computation
46. Kang M-W, Jha MK, Schonfeld P (2012) Applicability of highway alignment optimization models. Transp Res Part C Emerg Technol 21(1):257-286
47. Kazemi SF, Shafahi Y (2013) An integrated model of parallel processing and PSO algorithm for solving optimum highway alignment problem. Paper presented at the ECMS
48. Lindamood, Strong, McLeod (2009) Railway track design: practical guide to railway engineering, chapter 6. American Railway Engineering and Maintenance of Way Association, Maryland
49. Kennedy J, Eberhart R (1995) Particle swarm optimization. Proc IEEE Int Conf Neural Netw 4:1942-1948
50. Tu S, Guo X, Tu S (2008) Optimizing highway alignments based on improved particle swarm optimization and ArcGIS. In: The first international symposium on transportation and developmentinnovative best practices (TDIBP 2008). American Society of Civil Engineers, China Academy of Transportation Sciences
51. Shi Y, Eberhart R (1998) A modified particle swarm optimizer. In: 1998 IEEE international conference on evolutionary computation proceedings. IEEE world congress on computational intelligence (Cat. No. 98TH8360). IEEE, pp 69-73
52. Eberhart R, Simpson P, Dobbins R (1996) Computational intelligence PC tools. Academic Press Professional, Inc
53. Hickerson T (1964) Route location and design, 5th edn. McGrawHill, New York

<!-- image -->

Logo