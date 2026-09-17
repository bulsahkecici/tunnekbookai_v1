## Active learning with physics-informed neural networks for optimal sensor placement in deep tunneling through transversely isotropic elastic rocks

Alec Tristani a , Chloé Arson a

a Cornell University, Department of Earth and Atmospheric Sciences, Ithaca, NY 14850, USA

## Abstract

This paper presents a deep learning strategy to simultaneously solve Partial Differential Equations (PDEs) and backcalculate their parameters in the context of deep tunnel excavation. A Physics-Informed Neural Network (PINN) model is trained with synthetic data that emulates in-situ displacement measurements in the host rock and at the cavity wall, obtained from extensometers and convergence monitoring. As acquiring field observations can be costly, a sequential training approach based on active learning is implemented to determine the most informative locations for new sensors. In particular, Monte Carlo dropout is used to quantify epistemic uncertainty and query measurements in regions where the model is least confident. This approach reduces the amount of required field data and optimizes sensor placement. The PINN is tested to reconstruct the displacement field around a deep tunnel of circular section excavated in transversely isotropic elastic rock and to determine the rock constitutive and stress-field parameters. Results demonstrate excellent performance on small, scattered, and noisy datasets, achieving high precision for the Young's moduli, shear modulus, horizontal-to-vertical far-field stress ratio, and the orientation of the bedding planes. The proposed framework is compatible with traditional observational methods and shall ultimately support decision-making for optimal subsurface monitoring and for near real-time adaptive tunnel design and control.

Keywords: Active Learning, Physics-informed Neural Networks, Inverse Analysis, Deep Tunnels, Transversely Isotropic Elastic Rocks, Optimal Sensor Placement

## 1. Introduction

The ground response to tunnelling is usually simulated using computational models. Accurate determination of the governing physical parameters is therefore crucial for the robust design and long-term performance of underground infrastructure. This often necessitates field observations acquired during tunnel excavation as they provide information about the behavior at tunnel scale [1, 2, 3]. As formalized by Peck in 1969 [4] in the context of observational methods, computational models and their parameters are then considered as working hypotheses, subject to confirmation or modification during excavation. In that approach, field measurements, such as displacements, are used to iteratively update model parameters, ensuring an accurate simulation of the observed ground behavior. Observational methods help reduce construction time and costs, while enhancing safety and long-term performance. Nevertheless, their successful application requires two conditions: (i) observations must be reliable and reveal significant physical phenomena; (ii) back-analyses performed to update model parameters from field measurements must be computationally efficient.

As each rock constitutive relationship yields a different model formulation, performing back-analyses requires specific computational implementations. For instance, Sakurai and Takeuchi [5] developed a finite element (FE) formulation in which the rock behavior was assumed linear elastic to estimate the Young's modulus of the ground, using displacement measurements obtained at the cavity wall (from convergence instruments) and within the rock mass (from extensometers). When closed-form solutions are available, least-squares optimization methods are suitable. For example, Lecampion et al. [6] used synthetic data that emulates extensometer measurements to obtain the constitutive parameters of a Perzyna elasto-visco-plastic model. Schoen et al. [7] developed a three dimensional FE numerical model to perform inverse analysis from settlement measurements applied to mechanized tunnelling. Tristani et al. [8] derived an analytical solution for tunnels excavated in fractional viscoelastic plastic rocks and implemented a least-squares optimization scheme to characterize the rock mass. However, when the model is computationally costly, performing back-analysis of field data may be time-consuming as numerous forward passes are necessary. Efficient computational methods are therefore required.

∗ Corresponding author

1 email: ayt34@cornell.edu

More specifically, by seamlessly integrating prior knowledge from observational data and from PDEs, PINNs can make accurate predictions with small datasets, while other traditional deep learning techniques require large amounts of data [17]. In the PINN framework, the inverse problem is solved by simultaneously optimizing the network and physical parameters within a single unified loss function that combines PDE residuals, boundary condition residuals, and data misfit terms. PINNs have already been successfully applied across a wide range of scientific domains [18] as an alternative to numerical methods based on discretization schemes. In fluid mechanics, they have shown particular effectiveness [19], for example for solving inverse problems of unsaturated groundwater flow [20]. In solid mechanics, PINNs have been employed to solve both forward and inverse problems in elastic and plastic materials [21], as well as to predict dynamic stress fields [22]. In tunneling, PINNs have been used to predict ground surface settlements and estimate geotechnical parameters from settlement displacement data [23, 24, 25] or to estimate tunnel lining loads [26, 27].

Recent advances in differential programming (DP) have opened new avenues for the simulation of physical models [9, 10, 11, 12], where several classes of methods have been developed for solving both forward and inverse problems. By leveraging automatic differentiation (AD) [13], DP allows efficient and exact gradient computation (at machine precision) with respect to model inputs and parameters in an end-to-end manner, avoiding the need for manually derived adjoint formulations. Within this framework, both discrete and continuous formulations have been developed. While discrete approaches, whether based on FE formulations [14] or material point methods [15] solve the Partial Differential Equations (PDE) of the problem over a discretized mesh, continuous approaches approximate the solution with parametric functions over the entire domain. This continuous representation facilitates the evaluation of the solution at arbitrary locations, which can be advantageous when observations are sparse and irregularly distributed, as often encountered in tunnelling. In the context of Physics-Informed Machine Learning (PIML), Physics-Informed Neural Networks (PINNs) [16] approximate the solution in a continuous manner using neural networks, without relying on an explicit mesh. The governing equations are then enforced by evaluating PDE residuals at collocation points using AD.

Despite such promising achievements, the performance of PINNs strongly depends on the amount and distribution of the training data, including both observational measurements and residual (collocation) points. When sufficient observations cannot be obtained, one remedy is to train Machine Learning (ML) models on smaller but more informative datasets that capture the essential complexities of the underlying mapping, which can be facilitated by data sampling strategies [28]. When the number of measurements is fixed, adaptive sampling of residual points has proven to improve PINN accuracy. For instance, Lu et al. [29] suggested adding collocation points in regions exhibiting high PDE residuals. Nabian et al. [30] introduced an importance sampling algorithm to select the residual training points that contribute the most to the loss function. Wu et al. [31] compared uniform and non-uniform sampling strategies and developed a refined selection technique to minimize residual errors. However, in all the aforementioned studies, the number of field measurements is assumed to be fixed, and only the distribution of collocation points is optimized. As the inverse problem is often ill-posed and sensitive to the location and quantity of observation data [32], one may therefore need to query the most informative field observations in order to reveal the significant phenomena and identify the governing physical parameters [7].

Thus, in this study, we leverage the computational paradigm of PINNs to both reconstruct the displacement field around a deep tunnel and determine the constitutive parameters of the rock mass from sparse and noisy measurements, while simultaneously optimizing the placement of convergence and extensometer sensors. To efficiently acquire new observations, an active learning strategy is implemented to sequentially query and label the measurements that are expected to most significantly improve model performance. To this end, the PINN is trained using dropout as a stochastic regularization technique [47] which enables epistemic uncertainty estimation at inference time through

This can be achieved through the computational framework provided by modern Optimal Experimental Design (OED) [33]. Particularly, in the context of PIML, Active Learning (AL) relates to a class of algorithms designed to optimally choose the data to label and focuses on learning supervised predictive models [34]. The main idea behind AL is that a machine learning algorithm can achieve greater accuracy with fewer labeled training instances if it is allowed to choose the training data from which it learns [35]. AL algorithms sequentially select one new data point to label at a time, within a data-pool. As a special case of OED, AL aims to improve downstream predictions by maximizing information gain rather than by calibrating model parameters [36]. An important point is to specify the criterion to select new data, for example, by labeling the data for which the uncertainties of the current model are the highest [37, 38, 39, 40], by using query-by-committee techniques [41, 42], or by minimizing the loss function residual [43, 44, 45]. In most cases, AL outperforms traditional random sampling [46].

Monte Carlo dropout [48] and allows the model to query sensors in regions where predictions are least confident. The proposed approach aims to align with traditional observational methods and to support decision-making during the excavation phase by providing near real-time model parameter updates.

The remainder of this manuscript is organized as follows. Section 2 presents some theoretical background on PINNs and introduces the excavation problem in transversely isotropic elastic grounds in the form of non-dimensional equations. Section 3 details the model and formulates the active learning strategy developed in this study to best acquire the training data. Section 4 discusses the results obtained from a case study with several querying strategies, and demonstrates the effectiveness of the proposed approach using small, scattered, and noisy data. Finally, in Section 5, conclusions are drawn, and perspectives for future research are presented.

To illustrate the approach, we focus on a host rock that exhibits an elastic transversely isotropic behavior. In the field of tunneling, this constitutive model has been successfully used for grounds exhibiting a strong anisotropic behavior and for characterizing the instantaneous response of the rock mass. A synthetic dataset is generated using the high-fidelity finite element code MOOSE [49]. For such behaviors, it is worth emphasizing that analytical solutions to the problem of a cavity subjected to a biaxial far field stress have been derived in the past from the complex variable theory [50]. For example, the displacement field was expressed in the form of integer series for unlined [51] and lined [52] circular tunnels, and for tunnels of any cross-sectional shape (using conformal mapping techniques) [53]. Those analytical solutions assume that the constitutive parameters are known. Back-analysis approaches have also been proposed. For the cavity expansion problem, Kolymbas et al. [54] suggested an approximate solution to estimate the material constants, while Vu et al. [55] developed a semi-analytical solution to model displacement and stress fields around a tunnel section and to calculate constitutive parameters of the rock from convergence data.

## 2. Theoretical background

## 2.1. Physics-informed neural networks (PINNs)

Let us consider the following generic PDE expressed as:

<!-- formula-not-decoded -->

Here, D [ · ] denotes a linear differential operator acting on u , the solution of the differential equation; B [ · ] are boundary operators, λ denotes the PDE parameters, x is a position input vector in the spatial domain Ω ⊆ R d having boundary ∂Ω , where d ∈ { 1 , 2 , 3 } .

The PINN aims to approximate the true solution u ( x ) with a deep feedforward neural network N ( x ; θ ) , where θ = { w , b } denotes the trainable weights and biases. The network N ( x ; θ ) maps the spatial coordinates x to an approximation of the solution via a sequence of nested layer-wise transformations:

<!-- formula-not-decoded -->

where z 0 = x and z L = N ( x ; θ ) ≈ u ( x ) and where f corresponds to the activation function which carries the non-linearity of the system. Usually, f = tanh for all layers except the last one, which is linear.

Neural networks are trained to minimize a loss function L . For PINNs, this loss function is composed of three terms, as follows:

with:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where L pde ( θ ) represents the residual of the PINN solution, i.e., the extent to which the predicted solution fails to satisfy the governing PDEs that encode the physical constraints; L bc ( θ ) represents the deviation from the boundary conditions (BCs); and L data ( θ ) represents the discrepancy between the PINN-predicted solution and the available data at observation points.

The network parameters θ are tuned by minimizing the total training loss L ( θ ) . This is done during backpropagation at machine precision, i.e., at the highest numerical precision allowed by the floating-point representation on the hardware (typically float32 or float64), by leveraging AD [13] and using the Leibniz chain rule. In this study, AD is implemented in PyTorch [56]. Different optimizers can be chosen: stochastic optimization schemes such as Adam [57] or Nadam [58], or deterministic optimizers such as L-BFGS [59], which have also been widely used to train PINNs. A hybrid approach combining both optimizers can be used effectively to improve convergence [31]. In this study, the stochastic Nadam optimizer is used for training, while dropout [48] is further leveraged to train the model (see Section 3.4). Note that the weights w data , w pde , w bc are usually set constant prior to minimizing the total loss, which is the case in this work. They can alternatively be adapted during training, as proposed in the Self-Adaptive PINN method [60] or based on learning rate annealing methods [61]. In this work, fixed weights are assigned to each loss term as detailed in Section 3.3.

In equation 4, { x i } N Ω i =1 are residual points (also called collocation points) located in the domain Ω ; { x i } N ∂ Ω i =1 are boundary points; and { x i , ˆ y i } N data i =1 are measurements. N Ω , N ∂ Ω , N data denote the total number of collocation points, boundary points, and data points, respectively. w pde , w bc and w data are the weights associated with the PDE loss, BC loss, and data loss, respectively.

PINNs can be used to solve both forward and inverse problems. In the forward problem, the governing PDEs, material parameters, and boundary conditions are known and fixed. The objective is to compute the solution field u . The PINN is trained to minimize the PDE residuals and to satisfy boundary conditions, and no observational data is required. Note that in the case of forward problems, energy-based formulations have also been proposed for elasticity and hyperelasticity problems [62, 63, 64] as well as for viscoelasticity [65]. These approaches present advantages such as requiring only first-order derivatives and naturally satisfying homogeneous Neumann boundary conditions but are less suited for solving the inverse problem [66].

In the inverse problem, some coefficients of the PDEs or related to the boundary/initial conditions are unknown. The objective is to identify those unknown parameters from scattered and noisy measurements. The PINN is therefore trained to satisfy both the PDE/BC constraints and to minimize the data loss simultaneously. In practice, the unknown parameters are treated as additional trainable variables within the parameter set θ . Inverse problems are often ill-posed in the sense of Hadamard: a solution may not exist, may not be unique, or may be highly sensitive to the observational data. In the following, we focus on solving the inverse problem.

## 2.2. Physical governing equations

Rocks naturally exhibit heterogeneities. When the scale of those heterogeneities is similar to that of the tunnel diameter, the host rock cannot be considered as a continuum, and field discontinuities must be embedded in the formulation of the problem. Here, we study instead anisotropic rock formations that present heterogeneities that are at least two orders of magnitude smaller than the dimensions of the tunnel cross-section. We focus on sedimentary or metamorphic rocks, which develop a layered structure (through deposition of grains and particles in successive layers in the case of sedimentary rocks, or foliation during metamorphism in metamorphic rocks). This anisotropy can be accounted for through a transverse isotropic elastic behavior model to describe the response of the tunnel [51, 67, 54, 53]. In this case, the elasticity tensor depends on 5 independent parameters [68].

<!-- formula-not-decoded -->

In the following, we consider a deep circular tunnel excavated in a transversely isotropic elastic ground. We define the x -axis and z -axis as the axes that define the plane of isotropy of the host rock, as shown in Figure 1a. In the (x,y) plane, the angle formed between the bedding direction (x-axis) and the horizontal is noted β . The tunnel under study is excavated along the z -axis, which corresponds to the most unfavorable case, since the maximum deformations are expected to occur in the y -direction, which is the direction normal to the bedding plane. Two-dimensional plane-strain conditions are assumed. The in-situ stress state in a plane orthogonal to the z -axis is assumed to be homogeneous and anisotropic. Taking the horizontal and vertical axes as first and second directions of space, respectively, the in-situ stress state is defined as:

where K is the ratio between the horizontal and vertical stress (lateral earth pressure coefficient) and σ 0 is the far field vertical stress. A rotation by 2 β in the stress space ( β in the geometric space) yields the in-situ stress state components in the (x,y) coordinate system (see Figure 1b), as follows:

<!-- formula-not-decoded -->

Figure 1: Tunnel with circular cross-section of radius R excavated in transversely isotropic elastic rocks.

<!-- image -->

Engineering drawing

The total deformation ε t is decomposed into two parts: the so-called eigenstrain ε i , which corresponds to the initial deformation of the ground due to the in-situ state of stress; and ε , the deformation of the ground due to the excavation of the tunnel, which redistributes stresses around the cavity. The excavation deformation ε is thus calculated as:

<!-- formula-not-decoded -->

Noting S the compliance tensor of the transverse anisotropic rock mass, the stress and strain fields satisfy:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

and

where σ is the Cauchy stress tensor which corresponds to the stress field around the cavity.

In plane-strain, using Voigt notation for equation 7 yields:

<!-- formula-not-decoded -->

where E h and E v denote the Young's moduli in the plane of isotropy and in the direction normal to that plane, respectively. ν h is the Poisson's ratio for deformation within the plane of isotropy. ν hv and ν vh represent, respectively, the Poisson's ratio for the effect of in-plane stress on the strain normal to the plane, and the Poisson's ratio for the effect of normal stress on the strain within the plane of isotropy. These parameters are related by the reciprocity condition:

<!-- formula-not-decoded -->

Lastly, G vh is the shear modulus in any plane containing the normal direction to the plane of isotropy.

For small strains, the strain tensor is given by:

<!-- formula-not-decoded -->

where u ( x ) = ( u x , u y ) is the displacement vector at position x . In the absence of body forces, the equilibrium equation is:

The boundary condition at the tunnel wall is:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where n is the vector normal to the cavity wall. Note that this condition corresponds to the case of a tunnel that is fully excavated. Far away from the cavity, the perturbation induced by the excavation vanishes. Thus, the displacement field satisfies the far-field boundary condition:

<!-- formula-not-decoded -->

## 2.3. Non-dimensionalization

To avoid vanishing or exploding gradients during back-propagation, it is good practice to scale input and output variables. In the following, the domain is bounded by the tunnel and the locations where measurements are collected. We note R the radius of the tunnel section, and L the length of any extensometer that could be placed around the cavity to collect measurements. As suggested in [26], we introduce the following dimensionless variables:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

where:

This normalization serves two purposes: it provides a dimensionless formulation of the governing equations and ensures that the input and output variables remain within numerically convenient ranges during training. Note that the scaling coefficient u a was set to 10 - 1 mbecause the maximum displacement expected from the numerical analysis does not exceed 10 - 1 m.

Inserting the dimensionless variables defined in equation 16 into the equilibrium equation 13 yields the following expanded relationships:

<!-- formula-not-decoded -->

and inserting the dimensionless variables into the boundary equation 14, one obtains:

<!-- formula-not-decoded -->

where:

with:

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

## 3. Proposed approach: active learning to optimally place new sensors

## 3.1. Problem setup

During tunneling, assessing the response of the rock mass to excavation is essential for ensuring safety. As pointed out by Guayacán-Carrillo et al. [69], close monitoring of ground deformation around the tunnel provides useful information on ground response during and after excavation, as it helps reveal the significant observed phenomena. The collected measurements can subsequently serve as training data for machine learning models, enabling fast computations [70, 71]. Monitoring the ground behavior can be carried out by installing extensometers and convergence instruments around the tunnel wall. However, this process may be both costly and time-consuming, and the placement of sensors is often guided by empirical approaches. Fundamental questions naturally arise: How many measurements are necessary? Where should the sensors be placed? And, given the available measurements, can we reconstruct the displacement field and identify the constitutive parameters of the rock mass? Addressing these questions would not only improve our understanding of in-situ phenomena, but also contribute to more efficient and reliable tunnel design [7]. To this end, we leverage PINNs to propose an automatic, data-efficient framework based on their predictive capabilities. Specifically, we aim to reconstruct the displacement field around the tunnel while simultaneously identifying the rock mass parameters, namely, the horizontal-to-vertical stress ratio and the orientation of the bedding planes, using the smallest possible amount of measurement data.

Convergence measurements correspond to the relative displacement between two opposite points of the tunnel wall at a given section. They can also be obtained as the three-dimensional displacements of individual wall points measured by all the convergence stations. Convergence data provide valuable information about tunnel closure, allowing for a rapid assessment of ground behavior and for design updates if needed [72]. Because convergence is the easiest measurement to obtain, it is commonly monitored during and after excavation. Convergence and extensometer measurements at the wall have been shown to display similar trends [73]. Therefore, in this work, it is assumed that both convergence and extensometer measurements are equivalent indicators of tunnel closure.

Extensometers consist of radial cables installed around the tunnel cavity. They measure displacements at anchored points that are typically located every 3 - 4 meters along a radial cable starting from the tunnel wall. Because the measurement reflects the relative displacement between the anchored points and the extensometer head, it may represent either a relative or absolute displacement depending on whether the head itself moves. In this study, we assume that the extensometer head remains fixed, so that the recorded displacements correspond to the true ground displacements. In addition to extensometer data, tunnel convergence is usually monitored.

## 3.2. Synthetic dataset

In the following, the measurements are assumed to be drawn from a pool of observations P = { ( x i , y i ) } N data i =1 . These observations correspond to displacement measurements collected using field sensors. Each sensor, either an extensometer or a convergence point, provides an observation subset S i ⊂ P . When referred to as an extensometer , a sensor is represented by seven measurement points aligned along a radial direction within the domain and starting at the tunnel wall, with anchors placed every 4 m. Consecutive extensometers are spaced by an angle of 10 ◦ . When referred to as a convergence point , a sensor is a single measurement point located at the boundary of the domain, i.e., at the tunnel wall. For each sensor in the pool, in addition to computing the data loss term, the PINN also evaluates the PDE and BC residuals.

The domain is scaled as described in Section 2, so that all input coordinates and output displacements lie within the range [ - 1 , 1] . Note that since we are solving an inverse problem, the displacement measurements collected near the cavity act as Dirichlet-type constraints on the solution. These local observations help constrain the model to identify the constitutive parameters within the region of interest. Points located far away from the cavity, which would correspond to prescribed Dirichlet conditions at the far-field, are not included in the dataset, so that the learning process focuses on the area where observations are available.

Additionally, a second grid G = { ( x i , y i ) } N Ω i =1 ∪ { ( x i , y i ) } N ∂ Ω i =1 of size N r × N θ = 10 × 36 is defined, consisting of uniformly distributed collocation and boundary points. G is independent of the pool of observations P and is used throughout the training to enforce the PDE and BC in the domain. This ensures training stability and helps the model to accurately map the true solution around the tunnel. Therefore, the training set T consists of: (i) the n sensors that the model has already queried {S i } n i =1 , and (ii) the grid G containing the collocation and boundary points such that T = {S i } n i =1 ∪ G . The dataset is illustrated in Figure 2.

Lastly, model performance is evaluated on the full domain and along the boundary using a polar grid with N r = 50 radial points and N θ = 200 angular points, both uniformly distributed, totaling 10 , 000 evaluation points.

The reference dataset is generated using the high-fidelity finite element solver MOOSE. The computational domain is discretized using a mesh of 10,274 triangular linear elements, with local grid refinement near the tunnel wall. Collocation points are extracted using the LineValueSampler utility in MOOSE, which samples field values along predefined lines and interpolates when the target points do not coincide exactly with mesh nodes.

Figure 2: Training set. Left: pool of measurements P from which the model can query data, including both extensometers and convergence points. Right: grid of collocation and boundary points G used to solve the PDE and BC in the domain.

<!-- image -->

Scatter plot

## 3.3. PINN Model

To improve training stability and accelerate convergence [21], independent neural networks are defined to predict each output variable, namely u x and u y . In all experiments, the hyperbolic tangent (tanh) is used as the activation function. Each neural network consists of 10 hidden layers, with 40 neurons per layer. The displacement field is therefore approximated as:

<!-- formula-not-decoded -->

During training, the parameters of the PINN are optimized by the stochastic Nadam optimizer [58], which has been widely employed in the machine learning community. At each new iteration step, the model parameters, i.e., weights, biases, and PDE parameters, are initialized as those obtained at the last previous step. However, the optimizer is reinitialized, which means that its internal states are not retained across each step. This process avoids suboptimal solutions that correspond to local minima of the loss functions.

where N u x ( x ; θ ) and N u y ( x ; θ ) correspond to neural networks. This architecture is illustrated in Figure 3.

Equal weights can be assigned to each term of the loss function [21]. However, we observed in this work that using different weights improved the performance of the PINN. In particular, attributing superior weights to the data and BCs losses compared to the PDE loss yielded better convergence as it helped physically constrain the model, an observation that has also been reported in previous studies [61, 74]. In the remainder of this work, the following weighting scheme is adopted:

<!-- formula-not-decoded -->

A sensitivity analysis of the weighting scheme is presented in Appendix A.

## 3.4. Sequential learning approach

In most machine learning approaches, the model passively relies on a fixed training dataset. In contrast, active learning enables the model to strategically select the most informative data points or measurements from which to learn. The fundamental objective is to achieve maximal predictive performance while minimizing the amount of data required, making active learning closely aligned with the principles of optimal experimental design in statistics [35].

Figure 3: PINN architecture used in this study. Independent neural networks, N u x ( x ; θ ) and N u y ( x ; θ ) , are defined to predict the displacement components u x and u y , respectively. Each network takes the spatial coordinates ( x, y ) as input features.

<!-- image -->

Flow chart

In this work, dropout is used to train the PINN. The advantages of using dropout are twofold: i) by randomly deactivating neurons during training, it enables the quantification of epistemic uncertainty through multiple inference passes, a process known as Monte Carlo (MC) dropout, which approximates Bayesian inference [48]; and ii) it reduces overfitting to the training data, thereby improving model reliability [47].

An Active Learning (AL) strategy is then designed to efficiently query the most informative data points within the domain and thereby improve the robustness and accuracy of the machine learning models, as described in Algorithm 2. Data points are queried sequentially, and the PINNs are trained iteratively in a stage-wise manner. New measurements are labeled from the pool of observations based on the epistemic uncertainties of the PINN, evaluated at the end of each training stage. Note that the approximate epistemic uncertainty estimated via MC Dropout serves here as a practical criterion for sensor selection, rather than as a comprehensive uncertainty quantification framework. The relevance of this criterion is then assessed through its effect on the accuracy of the reconstructed displacement fields, as presented in Section 4.

A fixed dropout ratio equal to 5% is used for the first two hidden layers. Monte Carlo dropout is then performed to assess epistemic uncertainties. The model then selects the sensors yielding the highest predictive uncertainty in a manner consistent with the active learning strategy proposed in [37, 40]. Algorithm 1 details how a new sensor is selected.

## Algorithm 1 Query Strategy using Monte Carlo Dropout

- 1: Input: trained model, candidate sensor set {S i } N i =1 , current training set T
- 3: Perform n MC stochastic forward passes with dropout enabled N ( k ) u x ( S i ) , N ( k ) u y ( S i ) , k = 1 , . . . , n MC
- 2: for each candidate sensor S i do
- 4: Compute:
- mean prediction ¯ u x , ¯ u y of u x , u y over the n MC passes
- variance σ 2 u x , σ 2 u y of u x , u y over the n MC passes
- 5: Aggregate uncertainty of the sensor: ¯ σ 2 ( S i ) = mean of ( σ 2 u x + σ 2 u y ) over all points in S i
- 6: end for
- 7: Select highest-uncertainty sensor: S ⋆ = arg max S i ¯ σ 2 ( S i )
- 9: return updated training set T
- 8: Update training set: T ← T ∪ S ⋆

In Algorithm 2, at each step after initialization, the model can query one extensometer or one convergence sensor. We study two possibilities: the model can query i) only extensometer measurements or ii) only convergence measurements. At each step, when new sensors are queried, the corresponding collocation, boundary, and data points

## Algorithm 2 Active Learning

- 1: Initialization:
- 2: Select two initial extensometers S 1 , S 2 from the pool of measurements P such that T = S 1 ∪ S 2 .
- 4: Train the PINN for N epochs by computing L pde , L bc , and L data .
- 3: Initialize optimizer
- 5: Add the grid G : T ← T ∪ G
- 7: Train the PINN for N epochs by computing L pde , L bc , and L data .
- 6: Initialize optimizer
- 8: repeat
- 9: Initialize optimizer
- 11: Train the PINN for N epochs by computing L pde , L bc , and L data .
- 10: Query next sensor as described in Algorithm 1
- 12: Update the training set: T ← T ∪ S .
- 13: until the maximum allowed number of sensors is reached.

are simultaneously added to the training set. This ensures that the data, PDE, and boundary condition loss terms are all evaluated for the newly included samples during subsequent training. The proposed algorithms are greedy in nature, meaning that they do not guarantee convergence toward a global optimum. Nevertheless, increasing the number of accurate observations generally provides more information to the model, which helps constrain the solution space and solve the inverse problem. Figure 4 illustrates the active learning procedure presented in Algorithm 2.

Figure 4: Sequential active learning process where sensors are actively selected by the model and added to the training set. The color scale represents the total epistemic uncertainty σ 2 = σ 2 u x + σ 2 u y . Current sensors are shown in white, and the next sensor to be queried is highlighted in black. (a)-(b) Active learning when only extensometer observation points are added sequentially. (c)-(d) Active learning when only convergence observation points are added sequentially.

<!-- image -->

Scatter plot

Note that in Algorithm 2, the model is first initialized using two extensometers before the full grid is added. This strategy ensured that the model converged towards the true solution. One extensometer is placed at the crown and another on the left side of the tunnel, providing the initial set of observational data. This choice is motivated by the fact that these locations typically exhibit the most significant deformations in tunneling, making them natural starting points for model calibration. Additional observational data are then progressively incorporated when the corresponding measurement points are selected by AL.

## 4. Results

To evaluate the accuracy of the predicted displacement field ˆ u in reference to the true displacement field u , we compute the relative L 2 error over the test set:

For the inverse problem, the accuracy of the estimated rock mass parameter ˆ λ is quantified using the relative parameter error:

where λ denotes a true parameter.

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

To account for randomness arising from sampling, network initialization, and the optimization process, each experiment is repeated 10 times using random seeds, and the mean and standard deviation of the errors are reported.

## 4.1. Case study

To illustrate the approach, we aim to simultaneously reconstruct the displacement field and back-calculate rock properties around the Saint-Martin-la-Porte access gallery, located in Savoie, France. For context, the Saint-Martinla-Porte access gallery was excavated between 2003 and 2010. During excavation, the rock mass displayed pronounced anisotropic behavior, primarily associated with the Carboniferous formation (also known as the Productive Houillier).

In the following, we generate the synthetic dataset using the parameters obtained by Vu et al. [55]: the elastic parameters are E h = 620 MPa, E v = 340 MPa, G vh = 200 MPa, ν h = 0 . 12 , and ν hv = 0 . 2 ; the vertical stress is assumed to be 5 MPa, with a lateral pressure coefficient K = 0 . 75 ; and a varying bedding plane angle β ∈ { 0 ◦ , 45 ◦ , 90 ◦ , 135 ◦ }. Here, we aim to infer E h , E v , G vh , β , and K while ν h , and ν hv remain fixed. It is assumed that the tunnel is fully excavated, such that the radial stress at the wall is zero.

## 4.2. Reconstruction of the displacement field

We first compare the active learning strategy based on uncertainty-driven sampling against a random selection method. The evolution of the relative error, evaluated on the test set, is shown in Figure 5. Two querying methods are compared: sampling from extensometer data only (Figure 5a) and sampling from convergence data only (Figure 5b).

<!-- image -->

Line chart

(a) Querying only extensometers.

(b) Querying only convergence measurements.

Figure 5: Comparison of relative test errors obtained using active learning versus random selection for different types of sensors. The solid lines correspond to the mean values of the errors, and the shaded regions represent the associated standard deviations. Obtained for ten different random seeds in the case of β = 45 ◦ .

As shown in Figure 5, selecting measurements based on the highest estimated uncertainty consistently improves model performance compared to random sampling for both querying strategies. The performance gain is most pronounced when only a few measurements are available, with an improvement of 6-7% using three extensometers and 2-3% using four extensometers (Figure 5a). This effect is more significant when only convergence measurements are queried, as illustrated in Figure 5b. For a given query strategy (extensometer only or convergence only), the difference between random and active learning selection decreases as more measurements are included, since additional data help the model reconstruct the displacement field in regions with the largest uncertainties. This confirms the usefulness of AL in cases where observation data are scarce.

Figure 6 compares the model performance on the test set, which is divided into four concentric zones around the tunnel wall. Zone 1 corresponds to points within the interval [ R, 2 R ] , Zone 2 to [2 R, 3 R ] , Zone 3 to [3 R, 4 R ] , and Zone 4 to [4 R, 5 R ] . Figures 6a and 6b show the model performance for the horizontal and vertical displacement components, u x and u y , respectively, when only extensometer data are queried. Similarly, Figures 6c and 6d present the results for the horizontal and vertical displacement components when only convergence data are queried. For both querying strategies, the active learning selection method enables the model to progressively improve its performance as more measurements are queried. Overall, querying extensometer data yields lower relative test errors compared to querying only convergence data.

Figure 6: Mean relative test error evaluated in distinct zones. Zone 1: [ R, 2 R ] , Zone 2: [2 R, 3 R ] , Zone 3: [3 R, 4 R ] , Zone 4: [4 R, 5 R ] . Obtained for ten different random seeds in the case of β = 45 ◦ .

<!-- image -->

Line chart

In Zone 1, both querying strategies achieve similar performance. This suggests that it is possible in practice to reconstruct the displacement field around the tunnel with high accuracy up to one tunnel radius, with only two extensometers, those used for initialization at the crown and at the waist, and convergence data. With three extensometers, the error is approximately 4-5% for u y , while with the two initial extensometer data and one queried convergence, the error on u y is 7-8%. These errors gradually decrease to 3% and 5%, respectively, when five sensors in total are used. In Zones 2, 3, and 4, querying extensometer data yields better accuracy than querying convergence data: errors generally remain below 10% when using three extensometers and below 6% with five extensometers. By contrast, querying only convergence data does not sufficiently reduce the prediction error in Zones 2, 3, and 4, which are located farther from the tunnel wall. This outcome was expected, as no additional measurements from these zones are included in the training set.

Figure 7 shows the true displacement field generated using the finite element software MOOSE . Figures 8 and 9 illustrate the model predictions when only extensometer data are queried and when only convergence data are queried, respectively. The PINNs are trained using the sequential active learning procedures described in Section 3. The corresponding displacement predictions along the tunnel wall are shown for several training steps, after which no further changes are observed. To remain consistent with the available data, the predictions are restricted to a maximum radial distance of d = R + L , beyond which no measurements are assumed to be available.

Figure 7: Computations made using the MOOSE framework.

<!-- image -->

Other

Figure 8: Sequential active training and progressive reconstruction of the displacement field when querying only extensometer data. Obtained in the case of β = 45 ◦ .

<!-- image -->

Line chart

Figure 9: Sequential active training and progressive reconstruction of the displacement field when querying only convergence data. Obtained in the case of β = 45 ◦ .

<!-- image -->

Line chart

In Figure 8, the displacement field is partially reconstructed by the model using only two extensometers. With three or more extensometers, the displacement field is fully reconstructed for both horizontal and vertical components. Overall, the accuracy of the predicted displacement fields, both near the cavity and farther away, improves as additional extensometers are included. Similarly, in Figure 9, a progressive reconstruction of the displacement field is observed when only convergence data are queried. Using two extensometers and one convergence sensor, the model already reconstructs both displacement components around the tunnel with good accuracy. When two or more convergence measurements are queried, the model accurately reconstructs the displacement field close to the tunnel wall, although the predictions are less accurate in Zones 2, 3, and 4, which are farther from the wall.

Table 1 reports the relative errors on u x and u y for β ∈ { 0 ◦ , 45 ◦ , 90 ◦ , 135 ◦ } and both querying strategies, using 5 sensors in total.

Table 1: Relative error (%) on the displacement components u x and u y around the tunnel for different bedding plane orientations β and radial zones. Extensometers: 3 queried (5 in total). Convergences: 3 queried (2 extensometers + 3 convergences in total). Zone 1: [ R, 2 R ] , Zone 2: [2 R, 3 R ] , Zone 3: [3 R, 4 R ] , Zone 4: [4 R, 5 R ] .

|       |      | β = 0          | β = 0          | β = 45        | β = 45         | β = 90        | β = 90         | β = 135       | β = 135         |
|-------|------|----------------|----------------|---------------|----------------|---------------|----------------|---------------|-----------------|
| Comp. | Zone | Extenso.       | Converg.       | Extenso.      | Converg.       | Extenso.      | Converg.       | Extenso.      | Converg.        |
| u x   | 1    | 6 . 2 ± 0 . 9  | 9 . 3 ± 1 . 4  | 5 . 7 ± 1 . 4 | 6 . 1 ± 1 . 1  | 2 . 1 ± 0 . 3 | 4 . 9 ± 0 . 8  | 4 . 7 ± 0 . 7 | 7 . 4 ± 1 . 4   |
| u x   | 2    | 10 . 6 ± 2 . 7 | 17 . 2 ± 1 . 9 | 4 . 6 ± 1 . 2 | 8 . 7 ± 2 . 2  | 3 . 1 ± 0 . 9 | 12 . 5 ± 2 . 4 | 3 . 8 ± 0 . 9 | 10 . 2 ± 2 . 6  |
| u x   | 3    | 13 . 6 ± 3 . 2 | 21 . 5 ± 3 . 4 | 4 . 2 ± 1 . 0 | 13 . 4 ± 4 . 4 | 4 . 4 ± 1 . 5 | 21 . 5 ± 4 . 9 | 4 . 6 ± 1 . 4 | 15 . 0 ± 6 . 1  |
| u x   | 4    | 16 . 8 ± 3 . 9 | 24 . 9 ± 5 . 9 | 4 . 8 ± 1 . 2 | 19 . 4 ± 6 . 7 | 6 . 2 ± 2 . 1 | 31 . 4 ± 7 . 8 | 6 . 7 ± 2 . 4 | 20 . 9 ± 9 . 5  |
| u y   | 1    | 2 . 2 ± 0 . 7  | 6 . 8 ± 1 . 7  | 2 . 7 ± 1 . 0 | 4 . 3 ± 1 . 2  | 3 . 4 ± 0 . 8 | 6 . 8 ± 1 . 9  | 3 . 1 ± 0 . 9 | 6 . 7 ± 2 . 5   |
| u y   | 2    | 3 . 0 ± 1 . 2  | 18 . 5 ± 3 . 3 | 3 . 4 ± 1 . 7 | 10 . 7 ± 2 . 8 | 5 . 5 ± 1 . 7 | 12 . 7 ± 3 . 8 | 3 . 4 ± 1 . 0 | 15 . 0 ± 5 . 2  |
| u y   | 3    | 4 . 1 ± 1 . 3  | 32 . 7 ± 5 . 1 | 4 . 5 ± 2 . 4 | 19 . 3 ± 5 . 4 | 7 . 0 ± 2 . 2 | 18 . 8 ± 6 . 7 | 4 . 5 ± 1 . 1 | 24 . 6 ± 7 . 8  |
| u y   | 4    | 5 . 0 ± 1 . 3  | 47 . 7 ± 6 . 8 | 5 . 8 ± 2 . 7 | 29 . 2 ± 8 . 1 | 8 . 4 ± 2 . 7 | 26 . 4 ± 9 . 8 | 6 . 0 ± 1 . 4 | 35 . 1 ± 10 . 2 |

From Table 1, it can be observed that, when only extensometer data are queried ('extensometer mode'), low relative errors are achieved across all zones for β ∈ { 45 ◦ , 90 ◦ , 135 ◦ } . In particular, errors remain below approximately 5-7% in Zone 1 for both u x and u y , and increase moderately with distance, staying below 10% overall. For β = 0 ◦ , the model exhibits larger errors in the prediction of u x . This can be explained by the fact that the horizontal displacement component has a low amplitude in this configuration, making its reconstruction more difficult. In contrast, u y , which dominates the displacement field in this case, is predicted with good accuracy. When only convergence data are queried after the two initial extensometer data are read ('convergence mode'), the relative errors are systematically higher than in extensometer mode for all zones and bedding plane orientations. Nevertheless, the displacement field remains reasonably well reconstructed in Zone 1, while the accuracy degrades more significantly when the distance from the tunnel increases.

A limitation of the proposed approach is that a minimum of two extensometers is required to initialize the active learning process. If fewer measurements are employed, the model fails to reconstruct the displacement field and to identify the physical parameters. Furthermore, the current algorithm is inherently greedy, as it selects only the next measurement point without considering the overall arrangement of sensors. As a result, it does not optimize a global sensing strategy and may miss combinations of points that could collectively provide more informative or efficient coverage of the domain.

Finally, these results indicate that the proposed active learning strategy effectively enables (i) the selection of the most informative measurements to enhance model performance, and (ii) the progressive reconstruction of the displacement field around a deep circular tunnel.

## 4.3. Inverse analysis

We now evaluate the results of the inverse analysis. The corresponding results, reported in Table 2, show the estimated parameters at step 5 of the active learning process for both extensometer and convergence modes obtained after conducting for each case ten simulations using different random seeds.

As shown in Table 2, the model accurately recovers the physical parameters in both extensometer and convergence modes, although the latter exhibits higher errors overall. A notable observation is that the relative errors on E h (respectively E v ) are larger for β = 0 ◦ (respectively β = 90 ◦ ). This behavior can be explained by the reduced sensitivity of the displacement field to these parameters in the corresponding configurations. When the bedding planes are horizontal (respectively vertical), the displacement field is dominated by vertical (respectively horizontal) displacements, primarily governed by E v (respectively E h ). As a result, E h (respectively E v ) has a weaker influence on the observable response, leading to reduced identifiability in the inverse problem.

Table 2: Relative error (%) on the optimized model parameters obtained at step 5 of the active learning process. Results obtained after conducting ten computations corresponding to ten different random seeds.

|           | β = 0          | β = 0          | β = 45        | β = 45        | β = 90         | β = 90         | β = 135       | β = 135       |
|-----------|----------------|----------------|---------------|---------------|----------------|----------------|---------------|---------------|
| Parameter | Extenso.       | Converg.       | Extenso.      | Converg.      | Extenso.       | Converg.       | Extenso.      | Converg.      |
| E h       | 19 . 4 ± 7 . 8 | 23 . 0 ± 7 . 1 | 2 . 7 ± 2 . 2 | 3 . 6 ± 2 . 7 | 5 . 7 ± 2 . 2  | 5 . 9 ± 4 . 5  | 4 . 5 ± 2 . 5 | 6 . 3 ± 3 . 8 |
| E v       | 4 . 0 ± 1 . 5  | 3 . 8 ± 2 . 5  | 5 . 0 ± 3 . 7 | 5 . 6 ± 2 . 9 | 16 . 5 ± 6 . 6 | 33 . 0 ± 8 . 5 | 1 . 4 ± 1 . 1 | 8 . 0 ± 5 . 6 |
| G vh      | 6 . 0 ± 2 . 0  | 6 . 7 ± 2 . 6  | 2 . 4 ± 1 . 3 | 4 . 3 ± 3 . 4 | 1 . 2 ± 1 . 0  | 4 . 4 ± 2 . 5  | 4 . 2 ± 2 . 1 | 7 . 4 ± 4 . 3 |
| K         | 8 . 6 ± 2 . 7  | 8 . 9 ± 2 . 8  | 1 . 2 ± 0 . 8 | 1 . 1 ± 0 . 9 | 8 . 3 ± 2 . 9  | 11 . 9 ± 3 . 9 | 1 . 0 ± 0 . 8 | 5 . 7 ± 3 . 1 |
| β         | 1 . 3 ± 1 . 0  | 4 . 8 ± 2 . 0  | 5 . 0 ± 4 . 6 | 9 . 5 ± 5 . 3 | 1 . 1 ± 0 . 8  | 6 . 1 ± 3 . 6  | 1 . 1 ± 0 . 9 | 7 . 4 ± 4 . 4 |

To illustrate the optimization process during training, Figure 10 shows the values of the parameters optimized by the PINN as a function of the number of training epochs when using the active learning strategy with extensometer data only. Step 1 and step 2 correspond to model initialization, as detailed in Algorithm 2. In step 1, the training set consists of the observations from the two initial extensometers and their associated collocation/boundary points. In Step 2, the grid G is added to the training set. At each step, optimization begins with a reinitialized optimizer having a learning rate of l r = 10 - 4 , and the full batch of training data, that is, all available training points in T , is provided to the model. Early stopping is applied, resulting in a different number of epochs at each stage.

Figure 10: Sequential optimization of parameters using active training. Vertical dashed lines denote the stages at which additional measurements are queried and incorporated into the training set. Obtained in the case of β = 45 ◦ .

<!-- image -->

Line chart

To illustrate the sequential approach, Figure 11 presents the mean relative errors obtained with Algorithm 2 when querying either extensometer data or convergence data exclusively in the case of β = 45 ◦ . It can be observed that the sought parameters, i.e., E h , E v , G vh , K , and β , are successfully determined under both querying strategies. When querying extensometer data, E h , G vh , and K are the most accurately estimated parameters, with errors below 8% using two extensometers and below 5% with three. In contrast, the errors for E v and β remain under 15% with two and three extensometers, and decrease to below 6% and 5%, respectively, once four or more extensometers are used.

A similar trend is observed when querying only convergence data. The errors for E h , G vh , and K fall below 5% after three convergence measurements are added to the data pool, and continue to decrease thereafter. The error for E v remains below 10% and gradually reduces to approximately 6% with five convergence measurements. The error associated with β remains between 10% and 15% across all steps. This result can be attributed to the fact that convergence data are concentrated along the tunnel wall, which limits the model's ability to accurately optimize β , a parameter primarily influencing the displacement orientation rather than local displacement magnitudes.

Figure 11: Constitutive parameters obtained by the model after optimization step by step. The curves correspond to mean results obtained over 10 different seeds in the case of β = 45 ◦ .

<!-- image -->

Line chart

## 4.4. Computational time

Table 3 reports the computational time per active learning step, averaged over 10 seeds on an Apple M4 silicon chip. For both extensometer and convergence modes, each step requires between 3 and 6 minutes, and the full active learning process, from initialization to 7 sensors, is completed in approximately 25 minutes. This demonstrates that the proposed framework is computationally efficient and compatible with real-time tunnel monitoring, where excavation steps typically last from several hours to several days, leaving sufficient time to query new sensors, retrain the model, and update the displacement field and constitutive parameter estimates before the next excavation round.

Table 3: Computational time per active learning step and cumulative on an Apple M4 silicon chip. Step 1 and step 2 correspond to the initialization with 2 extensometers, common to both querying strategies.

|      |         | Extensometers   | Extensometers   | Convergences   | Convergences   |
|------|---------|-----------------|-----------------|----------------|----------------|
| Step | Sensors | Time (s)        | Cumul. (s)      | Time (s)       | Cumul. (s)     |
| 1    | 2       | 185 ± 5         | 185 ± 5         | 189 ± 5        | 189 ± 5        |
| 2    | 2       | 305 ± 26        | 490 ± 27        | 286 ± 36       | 475 ± 37       |
| 3    | 3       | 246 ± 32        | 736 ± 47        | 246 ± 35       | 721 ± 58       |
| 4    | 4       | 224 ± 24        | 960 ± 49        | 195 ± 31       | 916 ± 77       |
| 5    | 5       | 209 ± 32        | 1169 ± 62       | 178 ± 34       | 1094 ± 80      |
| 6    | 6       | 190 ± 24        | 1359 ± 53       | 158 ± 34       | 1252 ± 103     |
| 7    | 7       | 191 ± 31        | 1550 ± 60       | 167 ± 26       | 1419 ± 110     |

## 4.5. Model behavior using noisy data

We now analyze the sensitivity of the model to noisy data as it is an important problem in tunnelling where in-situ measurements are often noisy [69]. To assess the robustness of the model, synthetic heteroscedastic Gaussian noise was added to the displacement data. The noisy data ˜ u were generated as:

<!-- formula-not-decoded -->

where u denotes the true displacement vector and α controls the noise amplitude. In this work, α was set to 0.05, 0.10, and 0.15 to simulate noise levels of 5%, 10%, and 15%, respectively.

Figure 12 shows the relative displacement errors evaluated on the test set for different noise magnitudes. For noise levels of 5% and 10%, the model still achieves a good accuracy for both querying strategies. Using three extensometers, the error is approximately equal to 10% (respectively, 20%) for a noise level of 5% (respectively, 10%). With five extensometers, this error drops to 7% (respectively, 10%) for a noise level of 5% (respectively, 10%). At 15% of noise, the performance decreases, with errors around 25% at five extensometers. Furthermore, the standard deviation of the predictions increases, indicating a reduced confidence. Using two extensometer data and one convergence measurement, the error in the whole domain is about 25 % for 5% and 10% of noise magnitudes. This error decreases to approximately 17-20% when three convergence measurements are queried. At 15% of noise, the error is around 30% when three convergences are queried. For both querying strategies, a noise level above 15% considerably decreases model performance, at which point, the model can no longer converge. Further investigations are needed to treat inverse problems with high levels of noise - for example, through a Bayesian perspective [75].

Figure 12: Comparison of relative error in the test set for different noise magnitudes. The solid lines correspond to the mean values of the errors obtained over 10 repeated runs with different seeds, and the shaded regions represent the associated standard deviations.

<!-- image -->

Line chart

Figure 13 presents the results of the inverse analysis for noisy measurements with amplitudes of 5%, 10%, and 15%. The model provides reasonable predictions with data that contains small to moderate levels of noise: the overall trends are consistent with those obtained from noise-free data, although the mean relative error increases with noise level. For 5% noise, the model achieves errors below 15% for E h , G vh , and K using three extensometers, which progressively improves to approximately 5% with five extensometers (Figure 13a). The parameters E v and β are also correctly estimated, with errors around 17% and 25% at three extensometers, and errors of 10% at five extensometers. At a noise level of 10%, a similar trend is observed. Errors for E h , G vh , and K range between 15% and 18% for three extensometers and decrease to 13%-15% with five extensometers (Figure 13c). For E v and β , the errors are approximately 30% at three extensometers and reduce to around 20% and 25%, respectively, at five extensometers. For 15% noise, optimization becomes more challenging. The relative errors for E h , E v , G vh , and K lie between 15% and 25% with five extensometers, while the error for β remains relatively high, close to 30% (Figure 13e). When querying only convergence data, similar observations can be made although the direction of the bedding planes β is more difficult to determine.

Figure 13: Results of the inverse analysis for multiple noise levels, comparing extensometer and convergence data querying strategies. Solid lines indicate the mean errors obtained over 10 repeated runs with different seeds. Standard deviations are not represented for clarity.

<!-- image -->

Line chart

## 5. Conclusion

In this study, we propose a methodology to reconstruct the displacement field and characterize the rock mass surrounding deep circular tunnels excavated in transversely isotropic elastic media. To this end, we leverage the mesh-free nature of PINNs to back-analyze extensometer and convergence measurements collected during tunneling.

More specifically, by incorporating equilibrium equations, anisotropic constitutive laws, and boundary conditions as soft constraints into the loss function, the model can reconstruct the displacement field and identify the elastic parameters of the rock mass, the horizontal in-situ stress state, and the orientation of the planes of isotropy, even when observations are limited, irregularly distributed, or affected by small to moderate noise levels.

The main contribution of this work lies in enabling the PINN to autonomously select informative displacement measurements through an active learning framework based on epistemic uncertainty, quantified through dropout regularization. This strategy allows the sequential selection of sensors among extensometers and convergence measurements, which reduces the number of required observations and optimizes sensor placement. The developed methodology ultimately improves the reliability of the inverse identification and accuracy of the reconstructed displacement field.

Lastly, the methodology enables back-analysis using data collected at the tunnel scale during the excavation phase. The proposed tool is compatible with traditional observational methods as it can support near real time decision-making for optimal monitoring of ground behavior. Future work will focus on improved sensor-deployment strategies based on active planning computational methods. Other research directions include time-dependent effects typical of squeezing conditions and non-circular sections.

## 6. Code and data availability

The code and data used in this manuscript are publicly available at the GitHub repository [76] (see also https: //github.com/Alec-YT/AL-Tunnel ).

## 7. Acknowledgments

The authors wish to thank Prof. Herbert Einstein from MIT for discussions on sensor positioning and Prof. Yunan Yang from Cornell for her advice on training optimization.

## Appendix A. Sensitivity analysis of loss weights

This section presents a sensitivity analysis of the loss weights w bc and w data with w pde = 1 fi xed, conducted over the full active learning process (up to step 5) in extensometer mode and convergence mode for β = 135 ◦ .

As reported in Table A.4, convergence is reached if a relative test error lower than 30% is achieved; otherwise, the model is declared non-convergent.

Following the observations of Wang et al. [61, 74], that imbalanced gradients across loss terms can lead to training instabilities, we explored different weights for the data and boundary loss terms. In particular, the weights were increased as powers of 10 and 9 configurations were tested in total. Each of the 9 configurations was repeated ten times using different random seeds, corresponding to different network parameter initializations, resulting in 90 training runs for each extensometer and convergence modes (180 computations in total).

Table A.4: Convergence of the active learning procedure for different loss weight configurations ( w pde = 1 fi xed, extensometer mode (Extenso.) and convergence mode (Converg.), β = 135 ). "y" indicates convergence over 10 seeds; "n" indicates no convergence.

|   w bc |   w data | Extenso.   | Converg.   |
|--------|----------|------------|------------|
|      1 |        1 | n          | n          |
|      1 |       10 | n          | n          |
|      1 |      100 | n          | n          |
|      1 |     1000 | n          | n          |
|     10 |       10 | y          | y          |
|     10 |      100 | y          | y          |
|     10 |     1000 | n          | n          |
|    100 |      100 | y          | y          |
|    100 |     1000 | y          | y          |

From table A.4, it appears that the model is able to converge toward the right solution when w data ≥ w bc &gt; w pde . When w bc = w pde = 1 , the model fails to reconstruct the displacement field as the boundary conditions, which explicitly contain the parameters K and β , are insufficiently enforced. Conversely, when w data is excessively large, the data gradient dominates, and the PDE residuals are neglected, leading to a physically inconsistent solution.

Figure A.14 shows the evolution of the relative test error as a function of the number of sensors queried during the active learning process for the four configurations that yield convergence.

Figure A.14: Sensitivity analysis of loss weights in extensometer mode ( β = 135 ◦ , w pde = 1 fi xed). Results are averaged over 10 seeds and shaded regions represent one standard deviation.

<!-- image -->

Line chart

## References

- [1] E. Boidy, A. Bouvard, and F. Pellet. Back analysis of time-dependent behaviour of a test gallery in claystone. Tunnelling and Underground Space Technology , 17(4):415-424, October 2002. ISSN 0886-7798. doi:10.1016/S0886-7798(02)00066-4.
- [2] D. Sterpi and G. Gioda. Visco-Plastic Behaviour around Advancing Tunnels in Squeezing Rock. Rock Mechanics and Rock Engineering , 42(2):319-339, April 2009. ISSN 1434-453X. doi:10.1007/s00603-007-0137-8.
- [3] Frederic L Pellet. Contact between a Tunnel Lining and a Damage-Susceptible Viscoplastic Medium. Computer Modeling in Engineering &amp; Sciences , 2009.
- [4] Ralph B Peck. Advantages and limitations of the observational method in applied soil mechanics. Geotechnique , 19(2):171-187, 1969. doi:10.1680/geot.1969.19.2.171.
- [5] S. Sakurai and K. Takeuchi. Back analysis of measured displacements of tunnels. Rock Mechanics and Rock Engineering , 16(3):173-180, August 1983. ISSN 1434-453X. doi:10.1007/BF01033278. Number: 3.
- [6] B. Lecampion, A. Constantinescu, and D. Nguyen Minh. Parameter identification for lined tunnels in a viscoplastic medium. International Journal for Numerical and Analytical Methods in Geomechanics , 26(12):1191-1211, 2002. ISSN 1096-9853. doi:10.1002/nag.241. Number: 12 \_eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1002/nag.241.
- [7] Maximilian Schoen, Raoul Hölter, Daniela Boldini, and Arash Alimardani Lavasan. Application of optimal experiment design method to detect the ideal sensor positions: A case study of milan metro line 5. Tunnelling and Underground Space Technology , 130:104723, 2022. doi:10.1016/j.tust.2022.104723.
- [8] Alec Tristani, Jean Sulem, and Lina-María Guayacán-Carrillo. Analytical solutions considering face advance and time-dependent behavior for back-analysis of convergence measurements in deep circular tunnels under isotropic initial stress state. International Journal of Rock Mechanics and Mining Sciences , 182:105866, October 2024. ISSN 13651609. doi:10.1016/j.ijrmms.2024.105866.
- [9] Mike Innes, Alan Edelman, Keno Fischer, Chris Rackauckas, Elliot Saba, Viral B Shah, and Will Tebbutt. A differentiable programming system to bridge machine learning and scientific computing, 2019.

- [10] Christopher Rackauckas, Yingbo Ma, Julius Martensen, Collin Warner, Kirill Zubov, Rohit Supekar, Dominic Skinner, Ali Ramadhan, and Alan Edelman. Universal differential equations for scientific machine learning, 2021.
- [11] Mathieu Blondel and Vincent Roulet. The elements of differentiable programming, 2025.
- [12] Bleyer Jérémy. Jax-mat: Automated material constitutive modeling in jax, 2026. URL https://github.com/ erc-automatix/jaxmat .
- [13] Atilim Gunes Baydin, Barak A Pearlmutter, Alexey Andreyevich Radul, and Jeffrey Mark Siskind. Automatic differentiation in machine learning: a survey. Journal of machine learning research , 18(153):1-43, 2018.
- [14] Tianju Xue, Shuheng Liao, Zhengtao Gan, Chanwook Park, Xiaoyu Xie, Wing Kam Liu, and Jian Cao. Jax-fem: A differentiable gpu-accelerated 3d finite element solver for automatic inverse design and mechanistic data science. Computer Physics Communications , 291:108802, October 2023. ISSN 0010-4655. doi:10.1016/j.cpc.2023.108802.
- [15] Honghui Du and QiZhi He. Jax-mpm: A learning-augmented differentiable meshfree framework for gpuaccelerated lagrangian simulation and geophysical inverse modeling, 2025. URL https://arxiv.org/abs/ 2507.04192 .
- [16] M. Raissi, P. Perdikaris, and G.E. Karniadakis. Physics-informed neural networks: A deep learning framework for solving forward and inverse problems involving nonlinear partial differential equations. Journal of Computational Physics , 378:686-707, February 2019. ISSN 00219991. doi:10.1016/j.jcp.2018.10.045.
- [17] George Em Karniadakis, Ioannis G. Kevrekidis, Lu Lu, Paris Perdikaris, Sifan Wang, and Liu Yang. Physics-informed machine learning. Nature Reviews Physics , 3(6):422-440, May 2021. ISSN 2522-5820. doi:10.1038/s42254-021-00314-5.
- [18] Salvatore Cuomo, Vincenzo Schiano Di Cola, Fabio Giampaolo, Gianluigi Rozza, Maziar Raissi, and Francesco Piccialli. Scientific Machine Learning Through Physics-Informed Neural Networks: Where we are and What's Next. Journal of Scientific Computing , 92(3):88, July 2022. ISSN 1573-7691. doi:10.1007/s10915-022-01939-z.
- [19] Shengze Cai, Zhiping Mao, Zhicheng Wang, Minglang Yin, and George Em Karniadakis. Physics-informed neural networks (PINNs) for fluid mechanics: a review. Acta Mechanica Sinica , 37(12):1727-1738, December 2021. ISSN 1614-3116. doi:10.1007/s10409-021-01148-1.
- [20] Ivan Depina, Saket Jain, Sigurdur Mar Valsson, and Hrvoje Gotovac. Application of physicsinformed neural networks to inverse problems in unsaturated groundwater flow. Georisk: Assessment and Management of Risk for Engineered Systems and Geohazards , 16(1):21-36, January 2022. ISSN 1749-9518. doi:10.1080/17499518.2021.1971251. Number: 1 Publisher: Taylor &amp; Francis \_eprint: https://doi.org/10.1080/17499518.2021.1971251.
- [21] Ehsan Haghighat, Maziar Raissi, Adrian Moure, Hector Gomez, and Ruben Juanes. A physics-informed deep learning framework for inversion and surrogate modeling in solid mechanics. Computer Methods in Applied Mechanics and Engineering , 379:113741, June 2021. ISSN 00457825. doi:10.1016/j.cma.2021.113741.
- [22] Hamed Bolandi, Gautam Sreekumar, Xuyang Li, Nizar Lajnef, and Vishnu Naresh Boddeti. Physics informed neural network for dynamic stress prediction. Applied Intelligence , 53(22):26313-26328, November 2023. ISSN 0924-669X, 1573-7497. doi:10.1007/s10489-023-04923-8.
- [23] Zilong Zhang, Qiujing Pan, Zihan Yang, and Xiaoli Yang. Physics-informed deep learning method for predicting tunnelling-induced ground deformations. Acta Geotechnica , 18(9):4957-4972, September 2023. ISSN 1861-1133. doi:10.1007/s11440-023-01874-9.
- [24] Qipeng Cai, Khalid Elbaz, Xiangyu Guo, and Xuanming Ding. Physics-informed deep learning and analytical patterns for predicting deformations of existing tunnels induced by new tunnelling. Computers and Geotechnics , 187:107451, November 2025. ISSN 0266-352X. doi:10.1016/j.compgeo.2025.107451.
- [25] You Wang, Qianjun Fan, Fang Dai, Rui Wang, and Bosong Ding. A physics-data-driven method for predicting surface and building settlement induced by tunnel construction. Computers and Geotechnics , 179:107020, March 2025. ISSN 0266352X. doi:10.1016/j.compgeo.2024.107020.
- [26] Chen Xu, Ba Trung Cao, Yong Yuan, and Günther Meschke. Transfer learning based physics-informed neural networks for solving inverse problems in engineering structures under different loading scenarios. Computer Methods in Applied Mechanics and Engineering , 405:115852, February 2023. ISSN 00457825. doi:10.1016/j.cma.2022.115852.
- [27] G. Wang, Q. Fang, J. Wang, Q. M. Li, J. Y. Chen, and Y. Liu. Estimation of load for tunnel lining in elastic soil using physics-informed neural network. Computer-Aided Civil and Infrastructure Engineering , 39(17):2701-2718, 2024. ISSN 1467-8667. doi:10.1111/mice.13208.

- [28] Jan N. Fuhg, Govinda Anantha Padmanabha, Nikolaos Bouklas, Bahador Bahmani, WaiChing Sun, Nikolaos N. Vlassis, Moritz Flaschel, Pietro Carrara, and Laura De Lorenzis. A Review on Data-Driven Constitutive Laws for Solids. Archives of Computational Methods in Engineering , 32(3):1841-1883, April 2025. ISSN 1886-1784. doi:10.1007/s11831-024-10196-2.
- [29] Lu Lu, Xuhui Meng, Zhiping Mao, and George Em Karniadakis. DeepXDE: A Deep Learning Library for Solving Differential Equations. SIAM Review , 63(1):208-228, 2021. ISSN 0036-1445, 1095-7200. doi:10.1137/19M1274067.
- [30] Mohammad Amin Nabian, Rini Jasmine Gladstone, and Hadi Meidani. Efficient training of physics-informed neural networks via importance sampling. Computer-Aided Civil and Infrastructure Engineering , 36(8):962-977, August 2021. ISSN 1093-9687, 1467-8667. doi:10.1111/mice.12685. arXiv:2104.12325 [cs].
- [31] Chenxi Wu, Min Zhu, Qinyang Tan, Yadhu Kartha, and Lu Lu. A comprehensive study of non-adaptive and residual-based adaptive sampling for physics-informed neural networks. Computer Methods in Applied Mechanics and Engineering , 403:115671, January 2023. ISSN 00457825. doi:10.1016/j.cma.2022.115671.
- [32] Albert Tarantola. Inverse problem theory and methods for model parameter estimation . SIAM, 2005. doi:10.1137/1.9780898717921.
- [33] Xun Huan, Jayanth Jagalur, and Youssef Marzouk. Optimal experimental design: Formulations and computations. Acta Numerica , 33:715-840, July 2024. ISSN 0962-4929, 1474-0508. doi:10.1017/S0962492924000023. arXiv:2407.16212 [stat].
- [34] Sanjoy Dasgupta. Two faces of active learning. Theoretical Computer Science , 412(19):1767-1781, April 2011. ISSN 0304-3975. doi:10.1016/j.tcs.2010.12.054.
- [35] Burr Settles. Active Learning Literature Survey. Technical Report, University of Wisconsin-Madison Department of Computer Sciences, 2009. Accepted: 2012-03-15T17:23:56Z.
- [36] Tom Rainforth, Adam Foster, Desi R. Ivanova, and Freddie Bickford Smith. Modern Bayesian Experimental Design. Statistical Science , 39(1):100-114, February 2024. ISSN 0883-4237, 2168-8745. doi:10.1214/23-STS915. Publisher: Institute of Mathematical Statistics.
- [37] Maziar Raissi, Paris Perdikaris, and George Em Karniadakis. Inferring solutions of differential equations using noisy multi-fidelity data. Journal of Computational Physics , 335:736-746, April 2017. ISSN 0021-9991. doi:10.1016/j.jcp.2017.01.060.
- [38] Francisco Sahli Costabal, Yibo Yang, Paris Perdikaris, Daniel E. Hurtado, and Ellen Kuhl. Physics-Informed Neural Networks for Cardiac Activation Mapping. Frontiers in Physics , 8, February 2020. ISSN 2296-424X. doi:10.3389/fphy.2020.00042. Publisher: Frontiers.
- [39] Dongkun Zhang, Lu Lu, Ling Guo, and George Em Karniadakis. Quantifying total uncertainty in physicsinformed neural networks for solving forward and inverse stochastic problems. Journal of Computational Physics , 397:108850, November 2019. ISSN 00219991. doi:10.1016/j.jcp.2019.07.048.
- [40] Liu Yang, Xuhui Meng, and George Em Karniadakis. B-PINNs: Bayesian physics-informed neural networks for forward and inverse PDE problems with noisy data. Journal of Computational Physics , 425:109913, January 2021. ISSN 00219991. doi:10.1016/j.jcp.2020.109913.
- [41] H. S. Seung, M. Opper, and H. Sompolinsky. Query by committee. In Proceedings of the fifth annual workshop on Computational learning theory , COLT '92, pages 287-294, New York, NY, USA, July 1992. Association for Computing Machinery. ISBN 978-0-89791-497-0. doi:10.1145/130385.130417.
- [42] Justin S. Smith, Ben Nebgen, Nicholas Lubbers, Olexandr Isayev, and Adrian E. Roitberg. Less is more: Sampling chemical space with active learning. The Journal of Chemical Physics , 148(24):241733, June 2018. ISSN 0021-9606, 1089-7690. doi:10.1063/1.5023802.
- [43] Christopher J. Arthurs and Andrew P. King. Active training of physics-informed neural networks to aggregate and interpolate parametric solutions to the Navier-Stokes equations. Journal of Computational Physics , 438: 110364, August 2021. ISSN 00219991. doi:10.1016/j.jcp.2021.110364.
- [44] Zhiping Mao and Xuhui Meng. Physics-informed neural networks with residual/gradient-based adaptive sampling methods for solving partial differential equations with sharp solutions. Applied Mathematics and Mechanics , 44 (7):1069-1084, July 2023. ISSN 1573-2754. doi:10.1007/s10483-023-2994-7.
- [45] Wenhan Gao and Chunmei Wang. Active learning based sampling for high-dimensional nonlinear partial differential equations. Journal of Computational Physics , 475:111848, February 2023. ISSN 0021-9991. doi:10.1016/j.jcp.2022.111848.
- [46] Daniel Musekamp, Marimuthu Kalimuthu, David Holzmüller, Makoto Takamoto, and Mathias Niepert. Active Learning for Neural PDE Solvers, March 2025. arXiv:2408.01536 [cs].

- [47] Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov. Dropout: a simple way to prevent neural networks from overfitting. The journal of machine learning research , 15(1):19291958, 2014.
- [48] Yarin Gal and Zoubin Ghahramani. Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. In Proceedings of The 33rd International Conference on Machine Learning , pages 1050-1059. PMLR, June 2016. ISSN: 1938-7228.
- [49] Cody J Permann, Derek R Gaston, David Andrš, Robert W Carlsen, Fande Kong, Alexander D Lindsay, Jason M Miller, John W Peterson, Andrew E Slaughter, Roy H Stogner, et al. Moose: Enabling massively parallel multiphysics simulation. SoftwareX , 11:100430, 2020.
- [50] S. G. Lekhnitskii, P. Fern, Julius J. Brandstatter, and E. H. Dill. Theory of Elasticity of an Anisotropic Elastic Body. Physics Today , 17(1):84, January 1964. ISSN 0031-9228. doi:10.1063/1.3051394.
- [51] A. M. Hefny and K. Y. Lo. Analytical solutions for stresses and displacements around tunnels driven in cross-anisotropic rocks. International Journal for Numerical and Analytical Methods in Geomechanics , 23(2):161-177, 1999. ISSN 1096-9853. doi:10.1002/(SICI)1096-9853(199902)23:2&lt;161::AIDNAG963&gt;3.0.CO;2-B. \_eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1002/%28SICI%2910969853%28199902%2923%3A2%3C161%3A%3AAID-NAG963%3E3.0.CO%3B2-B.
- [52] Antonio Bobet. Lined Circular Tunnels in Elastic Transversely Anisotropic Rock at Depth. Rock Mechanics and Rock Engineering , 44(2):149-167, March 2011. ISSN 1434-453X. doi:10.1007/s00603-010-0118-1.
- [53] Huy Tran Manh, Jean Sulem, and Didier Subrin. A Closed-Form Solution for Tunnels with Arbitrary Cross Section Excavated in Elastic Anisotropic Ground. Rock Mechanics and Rock Engineering , 48(1):277-288, January 2015. ISSN 1434-453X. doi:10.1007/s00603-013-0542-0.
- [54] Dimitrios Kolymbas, Peter Wagner, and Anastasia Blioumi. Cavity expansion in cross-anisotropic rock. International Journal for Numerical and Analytical Methods in Geomechanics , 36(2):128-139, 2012. ISSN 1096-9853. doi:10.1002/nag.998. \_eprint: https://onlinelibrary.wiley.com/doi/pdf/10.1002/nag.998.
- [55] The Manh Vu, Jean Sulem, Didier Subrin, and Nathalie Monin. Semi-Analytical Solution for Stresses and Displacements in a Tunnel Excavated in Transversely Isotropic Formation with Non-Linear Behavior. Rock Mechanics and Rock Engineering , 46(2):213-229, March 2013. ISSN 0723-2632, 1434-453X. doi:10.1007/s00603012-0296-0. Number: 2.
- [56] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Kopf, Edward Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. PyTorch: An Imperative Style, High-Performance Deep Learning Library. In Advances in Neural Information Processing Systems , volume 32. Curran Associates, Inc., 2019.
- [57] Diederik P. Kingma and Jimmy Ba. Adam: A Method for Stochastic Optimization. arXiv:1412.6980 [cs] , January 2014. arXiv: 1412.6980.
- [58] Timothy Dozat. Incorporating Nesterov Momentum into Adam. February 2016.
- [59] Dong C. Liu and Jorge Nocedal. On the limited memory BFGS method for large scale optimization. Mathematical Programming , 45(1):503-528, August 1989. ISSN 1436-4646. doi:10.1007/BF01589116.
- [60] Levi D. McClenny and Ulisses M. Braga-Neto. Self-adaptive physics-informed neural networks. Journal of Computational Physics , 474:111722, February 2023. ISSN 00219991. doi:10.1016/j.jcp.2022.111722.
- [61] Sifan Wang, Yujun Teng, and Paris Perdikaris. Understanding and mitigating gradient pathologies in physicsinformed neural networks, January 2020. arXiv:2001.04536 [cs].
- [62] Esteban Samaniego, Cosmin Anitescu, Somdatta Goswami, Vien Minh Nguyen-Thanh, Hongwei Guo, Khader Hamdia, Xiaoying Zhuang, and Timon Rabczuk. An energy approach to the solution of partial differential equations in computational mechanics via machine learning: Concepts, implementation and applications. Computer Methods in Applied Mechanics and Engineering , 362:112790, 2020. doi:10.1016/j.cma.2019.112790.
- [63] Vien Minh Nguyen-Thanh, Xiaoying Zhuang, and Timon Rabczuk. A deep energy method for finite deformation hyperelasticity. European Journal of Mechanics-A/Solids , 80:103874, 2020. doi:10.1016/j.euromechsol.2019.103874.
- [64] Jan N Fuhg and Nikolaos Bouklas. The mixed deep energy method for resolving concentration features in finite strain hyperelasticity. Journal of Computational Physics , 451:110839, 2022. doi:10.1016/j.jcp.2021.110839.
- [65] Diab W Abueidda, Seid Koric, Rashid Abu Al-Rub, Corey M Parrott, Kai A James, and Nahil A Sobh. A deep learning energy method for hyperelasticity and viscoelasticity. European Journal of Mechanics-A/Solids , 95:104639, 2022. doi:10.1016/j.euromechsol.2022.104639.

- [66] Manish Thombre, Cosmin Anitescu, BVSS Bharadwaja, Yizheng Wang, Timon Rabczuk, and Alankar Alankar. Energy-based methods for solving forward and inverse linear elasticity problems in 2d structures. Computers &amp; Structures , 316:107899, 2025. doi:10.1016/j.compstruc.2025.107899.
- [67] F. Tonon and B. Amadei. Effect of Elastic Anisotropy on Tunnel Wall Displacements Behind a Tunnel Face. Rock Mechanics and Rock Engineering , 35(3):141-160, August 2002. ISSN 1434-453X. doi:10.1007/s00603-001-0019-4.
- [68] Haojiang Ding, Weiqiu Chen, and L. Zhang. Elasticity of Transversely Isotropic Materials , volume 126 of Solid Mechanics and Its Applications . Springer-Verlag, Berlin/Heidelberg, 2006. ISBN 978-1-4020-4033-7. doi:10.1007/1-4020-4034-2.
- [69] Lina-María Guayacán-Carrillo, Jean-Michel Pereira, and Jean Sulem. Lessons learned from using simple supervised learning tools on small-ensemble data-applicability to tunnel design and monitoring. International Journal for Numerical and Analytical Methods in Geomechanics , 2026. doi:10.1002/nag.70287.
- [70] Alec Tristani, Lina-María Guayacán-Carrillo, and Jean Sulem. Data-driven tools to evaluate support pressure, radial displacements, and face extrusion for tunnels excavated in elastoplastic grounds. International Journal for Numerical and Analytical Methods in Geomechanics , 49(2):654-664, 2025. doi:10.1002/nag.3889.
- [71] A. Tristani, L.M. Guayacán-Carrillo, and J. Sulem. A physics-informed machine learning surrogate model to assess the long-term ground-lining interaction in viscoelastic plastic grounds. , volume 59th U.S. Rock Mechanics/Geomechanics Symposium of U.S. Rock Mechanics/Geomechanics Symposium . June 2025. doi:10.56952/ARMA-2025-0533.
- [72] J Sulem, M Panet, and A Guenot. Closure Analysis in Deep Tunnels. International Journal of Rock Mechanics and Mining Sciences &amp; Geomechanics Abstracts , 1987.
- [73] Frederico Lara, Lina-María Guayacán-Carrillo, Jean Sulem, Jana Jaber, and Gilles Armand. Timedependent modeling of supported drifts excavated in Callovo-Oxfordian claystone considering the excavationinduced fractured zone. Computers and Geotechnics , 179:107030, March 2025. ISSN 0266-352X. doi:10.1016/j.compgeo.2024.107030.
- [74] Sifan Wang, Xinling Yu, and Paris Perdikaris. When and why PINNs fail to train: A neural tangent kernel perspective. Journal of Computational Physics , 449:110768, January 2022. ISSN 00219991. doi:10.1016/j.jcp.2021.110768.
- [75] A. M. Stuart. Inverse problems: A Bayesian perspective. Acta Numerica , 19:451-559, May 2010. ISSN 1474-0508, 0962-4929. doi:10.1017/S0962492910000061.
- [76] Alec Tristani. Active learning tunnel source code. https://doi.org/10.5281/zenodo.17712809 , 2025. Zenodo.