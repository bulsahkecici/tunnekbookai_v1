## Unsupervised Detection of Underground Tunnels in Ground-Penetrating Radar Using Depth-Restricted Reconstruction Scoring

Muhammad Junaid

Dept. of Electrical Engineering &amp; Computer Science Shoab A. Khan Dept. of Electrical Engineering &amp; Computer Science

Sir Syed CASE Institute of Technology Islamabad, Pakistan junaid6330@yahoo.com Sir Syed CASE Institute of Technology Islamabad, Pakistan kshoab@yahoo.com

Abstract -Clandestine tunneling beneath oil and gas pipelines enables fuel theft, smuggling, and sabotage, yet conventional monitoring detects damage only after a pipeline has been compromised. Ground-penetrating radar (GPR) can image such tunnels non-invasively, but manual radargram interpretation does not scale to continuous corridor surveillance, and supervised detectors require tunnel examples that are scarce in practice. We present a fully unsupervised detection pipeline trained exclusively on normal subsurface radargrams collected at a purpose-built field site containing three buried tunnels at 1.5-3 m depth. A denoising convolutional autoencoder learns the structure of anomaly-free ground; at inference, tunnels are flagged by reconstruction error. Our central contribution is a depth-restricted topk anomaly score, which pools the highest reconstruction errors only within the depth band where tunnels can physically occur. This physically motivated rule raises AUC from 0.986 to 0.994 and cuts missed detections from 74 to 17 of 634 tunnel windows, relative to whole-image scoring, without any retraining or labels. We further show that the optimal topk fraction interacts with the depth restriction-1% pooling is best on full images, 5% once scoring is depth-restricted-and that spatial voting across overlapping survey windows helps weak per-image detectors but offers no benefit once the scoring rule is strong. The final system attains AUC 0.994, F1 0.975, recall 0.973, and precision 0.976 on 1,600 field test windows spanning 55 survey lines, at a 1.6% false-alarm rate, using no tunnel labels for training, scoring, or threshold calibration.

Index Terms -ground-penetrating radar, anomaly detection, autoencoder, unsupervised learning, tunnel detection, pipeline security

## I. INTRODUCTION

Buried pipelines carry a large share of the world's oil and gas across long, sparsely monitored corridors, and their strategic value makes them a recurring target of unauthorized underground access. Documented incidents range from fueltapping tunnel networks in Mexico to a 174-foot clandestine tunnel discovered beneath a pipeline in Pakistan in 2024, used for petroleum smuggling. Conventional monitoring-pressure sensing, flow balancing, surface patrols-generally reacts to a breach that has already occurred; it offers little early warning of excavation approaching a pipeline from below [1].

Nisar Ahmed

Dept. of Computer &amp; Information Sciences University of Strathclyde

Glasgow, UK ch.nisar89@icloud.com

Ground-penetrating radar (GPR) is one of the few sensing modalities that can image the relevant threat directly. An air-filled cavity presents a strong dielectric contrast to the surrounding soil, producing the characteristic hyperbolic reflections that experienced analysts use to identify voids and tunnels [2]. The obstacle is not the physics but the interpretation workload: corridor-scale surveys produce thousands of radargrams contaminated by soil heterogeneity, moisture variation, and clutter, and manual review is slow, subjective, and inconsistent between analysts [3], [4].

Deep learning has substantially improved automated GPR interpretation, but nearly all reported systems are supervised: they require labeled examples of the target class, typically buried pipes and utilities [5]-[7]. For tunnel detection this requirement is hard to meet. Real intrusion tunnels are rare, their geometry varies, and no public dataset of tunnel radargrams exists at meaningful scale. A detector for this problem should learn what normal ground looks like and flag departures from it, rather than memorize a target class it will rarely see during development.

This paper develops and evaluates such a detector, and makes four contributions.

- 1) A publicly released field dataset for tunnel detection. To address the absence of public GPR tunnel data-the single largest obstacle to reproducible progress in this problem-we constructed and released a purpose-built dataset. Three tunnels of varying cross-section (1.5-3 m deep, 3-6 m wide) were hand-excavated on agricultural land near Islamabad and surveyed with a 200-MHz GPR alongside extensive tunnel-free terrain covering clay, sand, cultivated soil, moist ground, and scattered buried debris (Fig. 1). The full release contains 19,743 normal subsurface radargrams and 1,600 labeled test windows across 55 survey lines, and is publicly available on Kaggle 1 ; the subset used for the results reported in this

1 https://www.kaggle.com/datasets/muhammadjunaid007/gpr-normal-andtunnel-anomaly-dataset

- paper is summarized in Table I.
- 2) Depth-restricted topk scoring. We introduce an anomaly score that pools the topk %pixel reconstruction errors only within the lower half of the error map-the depth band where tunnels can physically occur at this site. The rule uses geometric prior knowledge, not labels, and improves AUC from 0.986 to 0.994 while reducing missed tunnels by 77%.
- 3) An interaction analysis of pooling fraction and depth restriction. We show these two design choices are not independent: 1% pooling is optimal on full images, but 5% becomes optimal once scoring is depth-restricted. Tuning them jointly, rather than in isolation, changes the selected configuration.
- 4) A characterization of when spatial post-processing helps. An N -ofM voting rule over overlapping survey windows, with a no-demote constraint, recovers many missed detections when the per-image detector is weak, fewer when it is stronger, and none once depth-restricted scoring is in place-because the residual misses are then systematic rather than isolated.

The complete system is unsupervised end to end: tunnel labels play no role in training, score computation, or threshold selection, and are used only to report evaluation metrics.

## II. RELATED WORK

## A. Automated GPR Interpretation

Most automated GPR analysis targets buried utilities. Classical pipelines relied on handcrafted descriptors of hyperbolic reflections followed by shallow classifiers [11], an approach that demands signal-processing expertise and transfers poorly across sites. Convolutional networks removed the featureengineering step: Liu et al. localize underground pipelines in B-scans with a deep detection model [5], and object detectors from the YOLO and R-CNN families have been adapted to buried-object search with strong results [6], [7]. Recent surveys catalogue this progress and its dependence on annotated data [4], [8]. Complementary work improves the data itself, through learned translation and denoising of radargrams [9] or hybrid model-based filtering [10]. Almost all of these systems are supervised, and they concentrate on pipes and cables rather than clandestine tunnels, whose scale, depth, and rarity pose a different problem [1].

## B. Reconstruction-Based Anomaly Detection

Anomaly detection with autoencoders follows a simple premise: a model trained to reconstruct only normal data reconstructs anomalies poorly, so reconstruction error serves as an anomaly score [12], [13]. Denoising training [14] strengthens the premise by preventing the network from learning a trivial identity mapping. In the GPR domain, Hoang et al. apply reconstruction-loss anomaly detection to radargram images [15], and Angelis et al. use related ideas for pipe inspection [16]. What this line of work leaves open-and what we address-is how the anomaly score should be read from the reconstruction-error map when the target occupies a small, physically constrained region of each image. Averaging error over the whole image dilutes a localized signature; we show that pooling choices, and especially a depth prior on where pooling is allowed, dominate the achievable performance.

Fig. 1. Field site and data acquisition. Three tunnels of varying cross-section (1.5-3 m deep, 3-6 m wide) were hand-excavated on agricultural land near Islamabad, Pakistan, and surveyed with a 200-MHz GPR alongside extensive tunnel-free terrain covering clay, sand, cultivated soil, and buried debris. (a) Purpose-built test area with the survey grid marked out. (b) Ground-level view of one excavated tunnel within the marked area. (c) GPR data acquisition using the 200-MHz system along a marked traverse. (d) Interior view of a hand-dug tunnel, showing the depth and geometry the detector must recognize as anomalous from surface radargrams alone. (e) Tunnel entrance from the surface with overlaid survey markings. (f), (g) Excavation of the tunnel test site.

<!-- image -->

Photograph

## III. FIELD DATASET AND PREPROCESSING

## A. Test Site and Acquisition

Data were collected with a 200-MHz GPR system in and around Islamabad, Pakistan (Fig. 1). Normal (tunnel-free) subsurface data were acquired across deliberately varied terrainconstruction sites, housing areas, parks, and an agricultural plot-covering clay, sand, cultivated soil, moist ground, and soil with scattered buried debris, so that the model's notion of 'normal' spans realistic field variation rather than one soil type. On the same agricultural land we excavated a dedicated tunnel test site containing three tunnels of different crosssections, 1.5-3 m (5-10 ft) deep and 3-6 m (10-20 ft) wide, and surveyed lines crossing them repeatedly.

Radargrams were exported as B-scan images and cut into windows by sliding along each survey line with approximately 90% overlap between consecutive windows, so that a physical tunnel appears across many neighboring windows rather than in one isolated image. The scan window spans roughly 2.4 m (8 ft) of depth; all three tunnels sit below the 1.2-m midpoint, a fact the scoring rule of Section IV-C exploits.

## B. Signal Preprocessing

Standard GPR conditioning was applied before imaging: DeWow filtering to remove low-frequency transmittercoupling drift, a band-pass (DynaT) filter matched to the expected target size, spreading-and-exponential-compensation

TABLE I DATASET COMPOSITION

| Stage                                   |   Count |
|-----------------------------------------|---------|
| Raw normal radargram windows            |   8,496 |
| Training split (80%)                    |   6,797 |
| Validation split (20%)                  |   1,699 |
| Training samples/epoch (10 × flip aug.) |  67,970 |
| Test - normal                           |     966 |
| Test - tunnel                           |     634 |
| Test - total (55 survey lines)          |   1,600 |

(SEC2) gain to equalize returns across depth, background suppression to remove horizontal banding, and amplitude normalization. Windows were converted to grayscale and resized to 128 × 128 pixels.

## C. Splits

Table I summarizes the data. The 8,496 normal images were split 80/20 into training and validation; horizontal-flip augmentation (Section IV-B) raises the effective training set to 67,970 samples per epoch. The held-out test set contains 1,600 windows-966 normal and 634 tunnel-organized into 55 survey-line folders that preserve spatial order, which the aggregation experiments of Section IV-E require. Tunnel windows never appear in training or validation; their labels are used solely to compute the reported metrics.

## IV. METHODOLOGY

## A. Denoising Convolutional Autoencoder

The detector is a convolutional bottleneck autoencoder (Fig. 2) trained only on normal windows. The encoder compresses the 1 × 128 × 128 input through four convolutional blocks (kernel 4 × 4 , stride 2, padding 1; channels 32 → 64 → 128 → 256 ), each followed by batch normalization and LeakyReLU (slope 0.2), producing a 256 × 8 × 8 feature map. This map is flattened and projected to a 256-dimensional latent vector-a 64:1 compression that forces the network to keep only the structural regularities of normal ground. The decoder mirrors the encoder with transposed convolutions, batch normalization and ReLU on intermediate layers, and a sigmoid output. Table II lists the layer shapes.

Because the encoder never observes tunnel signatures during training, it cannot allocate latent capacity to represent them; at inference such regions reconstruct poorly, which is precisely the signal the anomaly score reads out.

## B. Training Protocol

A plain autoencoder with sufficient capacity risks learning a near-identity mapping that reconstructs anomalies as faithfully as normal data. We therefore train with a denoising objective [14]: Gaussian noise ( σ = 0 . 05 ) is added to each input and clipped to [0 , 1] , while the mean-squared-error loss is computed against the clean image,

<!-- formula-not-decoded -->

Fig. 2. Detection pipeline. A convolutional encoder compresses each 128 × 128 radargram window to a 256-D latent vector; the mirrored decoder reconstructs it. The anomaly score pools the top-5% squared reconstruction errors within the lower half of the error map, and an unsupervised threshold µ +2 . 5 σ over normal-class scores yields the decision.

<!-- image -->

Flow chart

TABLE II AUTOENCODER ARCHITECTURE

| Layer                                                        | Input                                                        | Output                                               |
|--------------------------------------------------------------|--------------------------------------------------------------|------------------------------------------------------|
| Encoder Conv2D-1 Conv2D-2 Conv2D-3 Conv2D-4 Flatten + Linear | 1 × 128 × 128 32 × 64 × 64 64 × 32 × 32 128 × 16 × 16 16,384 | 32 × 64 × 64 64 × 32 × 32 128 × 16 × 256 × 8 × 8 256 |
|                                                              |                                                              | 16                                                   |
| Linear + Reshape ConvT2D-1                                   | 256                                                          | 256 × 8 × 8                                          |
|                                                              | 256 × 8 × 8                                                  | 128 × 16 × 16                                        |
| Decoder ConvT2D-2                                            | 128 × 16 × 16                                                | 64 × 32 × 32                                         |
| ConvT2D-3                                                    | 64 × 32 × 32                                                 | 32 × 64 × 64                                         |
| ConvT2D-4                                                    | 32 × 64 × 64                                                 | 1 × 128 × 128                                        |

This forces the encoder to model the structure of normal radargrams rather than copy pixels, widening the reconstructionerror gap between classes at inference. We briefly evaluated composite losses mixing MAE with a structural-similarity term; plain MSE gave the best balance and is used throughout.

Augmentation is deliberately conservative. Only horizontal flipping ( p =0 . 5 ) is applied: a flipped B-scan corresponds to surveying the same line in the opposite direction and is therefore a physically valid sample. Vertical flips (which invert the depth axis), rotations (which break the horizontal layering of B-scans), and intensity jitter (which distorts amplitude statistics the model must learn) were evaluated and rejected as non-physical.

Optimization uses Adam [17] with learning rate 5 × 10 - 4 and batch size 64 for 50 epochs. Both losses fall rapidly within the first 10 epochs and then plateau (Fig. 3); validation loss shows no upward drift, and the small persistent trainvalidation offset is expected because training loss is measured on noise-corrupted inputs while validation uses clean ones. The checkpoint with the lowest validation loss (0.001439, epoch 44) is retained for all reported results.

## C. Anomaly Scoring

Given a test window x and its reconstruction ˆ x , the squarederror map is E = ( x - ˆ x ) 2 ∈ R 128 × 128 . How this map is reduced to one score turns out to matter as much as the model itself.

Fig. 3. Training and validation reconstruction loss over 50 epochs of denoising training. The lowest validation loss (epoch 44) selects the final model.

<!-- image -->

Line chart

1) Why global averaging fails: The naive score, mean error over all 16,384 pixels, performs poorly (AUC 0.942; recall 0.579; Table V, row 1). A tunnel hyperbola occupies a small fraction of a window, so averaging drowns the localized anomaly in well-reconstructed background-a tunnel image ends up scoring close to a normal one.

2) Topk pooling: Instead, we sort all pixel errors and average only the top k % :

<!-- formula-not-decoded -->

where T k indexes the k % largest entries of E . Small k concentrates the score on the worst-reconstructed region, where a tunnel would be. On full images, a sweep over k ∈ { 1 , 2 , 5 , 10 } % (Table III) shows 1% is clearly best: highest AUC (0.9907), fewest misses, no added false alarms.

3) Depth restriction: Topk pooling still treats every pixel as equally eligible, ignoring where in the scan it lies. In a B-scan the vertical axis is two-way travel time-a proxy for depth-and the upper half of every window at this site is dominated by the direct-wave arrival and shallow soil clutter, which vary between images for reasons unrelated to tunnels. Meanwhile the tunnels, buried below 1.2 m in a 2.4-m scan window, can only appear in the lower half. We therefore discard the upper 64 rows of E before pooling, drawing the topk set from the remaining 8 , 192 pixels:

<!-- formula-not-decoded -->

This is a geometric prior derived from the survey setup, not a learned or supervised component; it is applied identically to every image and requires no labels. It helps twice over: nuisance error in the upper band can no longer inflate normalclass scores (tightening the threshold), and the entire pooling budget for tunnel images is spent inside the band that actually contains the anomaly.

## 4) The pooling fraction interacts with the restriction:

Re-running the fraction comparison under depth restriction reverses the earlier ranking (Table IV). With pooling confined to the tunnel-relevant band, 1% still finds slightly more tunnels (13 vs. 17 missed) but at a higher false-alarm cost (22 vs. 15), while 5% achieves the better F1 (0.9747 vs. 0.9726) and MCC (0.9582 vs. 0.9545). The intuition: on full images a very tight pool is needed to overcome background dilution, but once the candidate region is already restricted and more uniformly informative, a slightly larger pool yields a steadier score less sensitive to a handful of extreme pixels. We adopt depth-restricted top-5% as the final score, selected on the two metrics that weight both error types equally.

## D. Threshold Selection

The decision threshold is set from normal-class scores alone:

<!-- formula-not-decoded -->

a standard convention in unsupervised anomaly detection [12]. No tunnel labels enter training, scoring, or thresholding. A percentile sweep (Table VII) confirms the operating point can be shifted along the precision-recall trade-off without retraining.

## E. Spatial Aggregation Across Overlapping Windows

Because consecutive windows overlap by ∼ 90% , a real tunnel spans many neighboring windows, while spurious errors are typically isolated. This suggests a post-processing rule: for each window, examine the M consecutive windows centered on it within the same survey line; if at least N of them were independently flagged, promote the window to positive even if its own score fell just below τ . Two constraints matter. No-demote: aggregation may only promote negativesa confirmed detection is never overturned by weakly scoring neighbors, so the rule can help or do nothing, never harm. Line grouping: voting occurs only among spatially ordered windows of the same physical survey line. Across the configurations tested, M =7 , N =3 gave the best balance on weaker baselines; results appear in Section V-F.

## V. EXPERIMENTS AND RESULTS

## A. Setup

All models were implemented in PyTorch and trained on a single CUDA-enabled workstation. Evaluation uses the 1,600window field test set of Table I. We report AUC-ROC, average precision (AP), accuracy, precision, recall, specificity, F1, F2, balanced accuracy, Matthews correlation coefficient (MCC), Cohen's κ , and error rates; 95% Wilson confidence intervals accompany the proportion-based metrics. Fixed random seeds govern data splitting and initialization.

## B. Selecting the Pooling Fraction

Table III reports the full-image sweep and Table IV the depth-restricted comparison discussed in Section IV-C. The reversal between them-1% optimal without the restriction, 5% with it-is one of the paper's findings: the two design choices must be tuned jointly.

Fig. 4. Failure cases. Top two rows: representative false negatives ( n =17 total) and false positives ( n =15 total) of the adopted depth-restricted top5% detector at the unsupervised threshold τ =0 . 0228 ; per-window scores are shown above each panel. The missed windows are truncated edge views in which the tunnel hyperbola is only partially inside the frame, while the false alarms show unusually strong shallow-soil disturbance producing lower-band textures outside the training distribution. Bottom two rows: false negatives ( n =41 ) and false positives ( n =29 ) of full-image top-5% scoring with M =7 , N =3 spatial aggregation (Table V, row 3); consecutive faint-tunnel windows are jointly missed-no window accrues enough confirmed neighbors to be promoted-and the added alarms repeat the same soil-disturbance failure mode.

<!-- image -->

Table

TABLE III EFFECT OF TOPk FRACTION (FULL-IMAGE SCORING)

| k   |    AUC | Prec.   | Recall   |     F1 |   FN |   FP |
|-----|--------|---------|----------|--------|------|------|
| 1%  | 0.9907 | 0.9667  | 0.9148   | 0.9400 |   54 |   20 |
| 2%  | 0.9902 | -       | -        | 0.9308 |   62 |   23 |
| 5%  | 0.9855 | 0.9639  | 0.8833   | 0.9218 |   74 |   21 |
| 10% | 0.9768 | -       | -        | 0.9021 |   95 |   22 |

## C. Ablation Study

Table V traces the complete progression from the naive baseline to the final method on identical data, model, and threshold rule. Three observations follow. First, the dilution problem dominates the baseline: global averaging misses 42% of tunnels, and top-5% pooling alone recovers most of that gap (recall 0 . 58 → 0 . 88 ) with no retraining. Second, the depth restriction delivers the largest single improvementAUC 0 . 986 → 0 . 994 , misses 74 → 17 -while simultaneously reducing false positives, indicating both mechanisms of Section IV-C operate as intended rather than trading one error type for the other. Third, spatial aggregation improves the weak full-image baseline substantially (row 2 → 3: F1 +0 . 023 ) but yields nothing on the strong depth-restricted detector (row 4 → 5: F1 - 0 . 001 ); the best real configuration there recovers a single missed tunnel at the cost of one added false alarm.

TABLE IV EFFECT OF TOPk FRACTION UNDER DEPTH RESTRICTION

| k   |    AUC |   Prec. |   Recall |     F1 |    MCC |   FN |   FP |
|-----|--------|---------|----------|--------|--------|------|------|
| 1%  | 0.9949 |  0.9658 |   0.9795 | 0.9726 | 0.9545 |   13 |   22 |
| 5%  | 0.9936 |  0.9763 |   0.9732 | 0.9747 | 0.9582 |   17 |   15 |

Fig. 5. ROC (left) and precision-recall (right) curves for the final depthrestricted top-5% score on the field test set.

<!-- image -->

Line chart

## D. Final Detector Performance

Table VI reports the full metric set for the adopted method. The detector misses 17 of 634 tunnel windows (2.7%) at a 1.6% false-alarm rate; MCC of 0.958 confirms the result is not an artifact of class balance. Fig. 5 shows the ROC and precision-recall curves, and Fig. 6 the confusion matrix. Fig. 7 illustrates the mechanism on representative windows: normal ground reconstructs faithfully, while the hyperbolic tunnel signature-absent from the training distribution-produces a localized cluster of high error in the lower band that drives the score across threshold.

## E. Threshold Sensitivity

Table VII sweeps the threshold across percentiles of the normal-score distribution. The default µ +2 . 5 σ rule sits at a balanced operating point; stricter thresholds (p99, p99.5) trade a few extra misses for as few as 5 false alarms, and looser ones do the opposite. Because the score function is fixed, an operator can move along this trade-off at deployment time without touching the model.

## F. Spatial Aggregation and Baseline Strength

Aggregation's value tracks the weakness of the per-image detector it sits on. On full-image top-5% scoring (F1 0.9218) the M =7 , N =3 rule recovers 33 missed tunnels and lifts F1 by 0.023; the 41 windows it still misses are truncated or unusually faint tunnel views that lack enough confirmed neighbors to trigger a vote, and its added false alarms repeat the shallowdisturbance failure mode (Fig. 4, bottom two rows). On the stronger full-image top-1% baseline (F1 0.9400) the gain shrinks to 0.007. On the depth-restricted detector the best configuration changes nothing of substance: only 17 misses remain, and inspection shows they occur in runs -several consecutive windows over the same faint tunnel segment jointly undetected-so no window has enough confirmed neighbors to trigger a vote. Larger windows ( M =9 , N =3 ) do force more recoveries there, but at 73 false positives, collapsing precision. The monotonic pattern across three baselines supports a simple reading: neighborhood voting is a safety net for isolated misses, not a substitute for a strong scoring rule.

TABLE V ABLATION OF SCORING AND POST-PROCESSING STRATEGIES (966 NORMAL / 634 TUNNEL WINDOWS; 55 SURVEY LINES). ALL ROWS SHARE THE SAME AUTOENCODER AND µ +2 . 5 σ THRESHOLD. AUC/AP ARE UNCHANGED BY AGGREGATION, WHICH OPERATES ON THRESHOLDED PREDICTIONS. AGGREGATION ROWS REPORT THE HIGHEST-F1 WINDOW CONFIGURATION.

|   # | Method                                         |    AUC |     AP |     F1 |   Precision |   Recall |    MCC |   FN |   FP |
|-----|------------------------------------------------|--------|--------|--------|-------------|----------|--------|------|------|
|   1 | Global MSE (whole-image mean)                  | 0.9417 | 0.9255 | 0.7217 |      0.9582 |   0.5789 | 0.6446 |  267 |   16 |
|   2 | Top-5% MSE (full image)                        | 0.9855 | 0.9814 | 0.9218 |      0.9639 |   0.8833 | 0.8763 |   74 |   21 |
|   3 | Top-5% + spatial aggregation ( M =7 , N =3 )   | 0.9855 | 0.9814 | 0.9443 |      0.9534 |   0.9353 | 0.9084 |   41 |   29 |
|   4 | Depth-restricted top-5% MSE (ours)             | 0.9936 | 0.9937 | 0.9747 |      0.9763 |   0.9732 | 0.9582 |   17 |   15 |
|   5 | Depth-restricted + aggregation ( M =3 , N =2 ) | 0.9936 | 0.9937 | 0.9740 |      0.9747 |   0.9732 | 0.9569 |   17 |   16 |

TABLE VI FINAL PERFORMANCE: DEPTH-RESTRICTED TOP-5% SCORING

| Metric            |   Value | 95% CI           |
|-------------------|---------|------------------|
| AUC-ROC           |  0.9936 | -                |
| Average precision |  0.9937 | -                |
| Accuracy          |  0.9800 | [0.9719, 0.9858] |
| Precision         |  0.9763 | [0.9612, 0.9856] |
| Recall            |  0.9732 | [0.9575, 0.9832] |
| Specificity       |  0.9845 | [0.9745, 0.9906] |
| F1                |  0.9747 | -                |
| F2                |  0.9738 | -                |
| Balanced accuracy |  0.9788 | -                |
| MCC               |  0.9582 | -                |
| Cohen's κ         |  0.9582 | -                |
| FPR               |  0.0155 | -                |
| FNR               |  0.0268 | -                |

Fig. 6. Confusion matrix of the final detector: 951/966 normal and 617/634 tunnel windows classified correctly.

<!-- image -->

Bar chart

## G. Comparison with a Classical Baseline

For reference against non-deep methods, an Isolation Forest trained on the same data reaches 81.2% accuracy (precision 80.1%, recall 72.0%, F1 79.6%), against 98% accuracy for the proposed detector-consistent with the broader finding that learned spatial features dominate handcrafted ones on radargram imagery [8].

Fig. 7. Reconstruction behavior on a normal window (top) and a tunnel window (bottom): input, reconstruction, and squared-error heatmap. The unseen hyperbolic signature reconstructs poorly, concentrating error in the lower depth band that the score pools over.

<!-- image -->

Table

TABLE VII THRESHOLD SWEEP ON THE NORMAL-SCORE DISTRIBUTION

| Rule       |   Threshold |   FP |   FN |     F1 |   Acc. |
|------------|-------------|------|------|--------|--------|
| µ +2 . 5 σ |     0.02282 |   15 |   17 | 0.9747 | 0.9800 |
| p95        |     0.02030 |   49 |   13 | 0.9525 | 0.9613 |
| p97        |     0.02149 |   29 |   14 | 0.9665 | 0.9731 |
| p98        |     0.02218 |   20 |   15 | 0.9725 | 0.9781 |
| p99        |     0.02337 |   10 |   20 | 0.9762 | 0.9812 |
| p99.5      |     0.02463 |    5 |   24 | 0.9768 | 0.9819 |

## H. Error Analysis

The 17 residual false negatives (Fig. 4, top row) are almost entirely truncated tunnel views: windows at the leading or trailing edge of a tunnel crossing, where the hyperbola is only partially inside the frame and its reconstruction error stays near normal levels. Because the survey's 90% overlap guarantees the same tunnel appears fully in adjacent windows-where it is detected-these edge misses do not translate into missed tunnels at the survey level; a larger window step during dataset preparation would reduce them further. The 15 false positives (Fig. 4, second row) concentrate on windows with unusually strong shallow-soil disturbance, plausibly high local moisture, producing lower-band textures outside the training distribution [18]. These are genuine model limitations, but of a benign kind for the application: they flag ground that merits a second look.

## VI. DISCUSSION

Two conceptual results generalize beyond this dataset. First, in reconstruction-based detection of small, spatially constrained targets, how the error map is pooled is a firstclass design decision , and pooling interacts with spatial priors: the best pooling fraction changed once a depth restriction was imposed, so the two must be tuned jointly. Encoding even a coarse physical prior-here, 'tunnels cannot occur in the upper half of the scan'-produced a larger gain than any post-processing we tested, at zero labeling cost. Second, postprocessing exhibits diminishing returns in proportion to basedetector quality. Spatial voting earned +0.023 F1 on a weak baseline and nothing on a strong one, because refining the score converts the error population from isolated, recoverable misses into a hard core of systematic ones. Reports of aggregation gains should therefore be read relative to the strength of the underlying detector.

Limitations. The pooling fraction, depth boundary, and aggregation window were selected on the same labeled test set used for final reporting; a disjoint labeled validation split would remove any risk of optimistic bias, and we flag this as the first item for follow-up work. All data come from one geographic site and one 200-MHz instrument; cross-site and cross-frequency generalization remains to be demonstrated. The small window step that produces truncated edge windows inflates the per-window false-negative count relative to the operationally relevant per-tunnel detection rate. Finally, the system classifies windows; it does not yet localize or map tunnels in three dimensions.

## VII. CONCLUSION

We presented a fully unsupervised pipeline for detecting clandestine tunnels in GPR radargrams, trained only on normal subsurface data from a purpose-built field site. A denoising convolutional autoencoder supplies the reconstruction signal, and a depth-restricted top-5% pooling rule-a physically motivated, label-free refinement of how that signal is read-carries the system to AUC 0.994, F1 0.975, and a 2.7% miss rate at 1.6% false alarms on 1,600 field test windows. Ablations isolate the contribution of each component and yield two transferable findings: pooling fraction and spatial priors interact and must be tuned jointly, and spatial post-processing helps weak detectors but not strong ones. Future work will validate a heldout hyperparameter protocol, extend acquisition to additional sites and soil regimes, increase the survey window step, and pursue survey-level tunnel localization and multi-sensor fusion toward deployable corridor monitoring.

## REFERENCES

- [1] B. Oktenli, 'Strategic subterranean domain awareness: A comprehensive technical and operational evaluation of next-generation AI-fused counter-tunnel architectures,' SSRN 6046594, 2026.
- [2] D. J. Daniels, Ground Penetrating Radar , 2nd ed. London, U.K.: IET, 2004.
- [3] K. S. Oguntoye, S. Laflamme, R. Sturgill, and D. J. Eisenmann, 'Review of artificial intelligence applications for virtual sensing of underground utilities,' Sensors , vol. 23, no. 9, p. 4367, 2023.
- [4] C. Liu, J. Li, Z. Liu, S. Tao, and M. Li, 'A comprehensive review of data processing and target recognition methods for ground penetrating radar underground pipeline B-scan data,' Discover Applied Sciences , vol. 7, no. 4, p. 310, 2025.
- [5] H. Liu, Y. Yue, C. Liu, B. F. Spencer, Jr., and J. Cui, 'Automatic recognition and localization of underground pipelines in GPR B-scans using a deep learning model,' Tunnelling and Underground Space Technology , vol. 134, p. 104861, 2023.
- [6] D. Jafuno, A. Mian, G. Ginolhac, and N. Stelzenmuller, 'Classification of buried objects from ground penetrating radar images by using second order deep learning models,' 2024.
- [7] T.-B.-T. Do, J.-H. Cho, J.-H. Park, and K.-N. Kim, 'Ground penetrating radar image analysis for underground barrier detection by combining YOLOv12 with channel-wise attention and denoising auto-encoder,' in Proc. Int. Conf. Research in Adaptive and Convergent Systems (RACS) , 2026.
- [8] L. Zou, Y. Li, K. Munisami, and A. M. Alani, 'Bridging theory and practice: A review of AI-driven techniques for ground penetrating radar interpretation,' Applied Sciences , vol. 15, no. 15, p. 8177, 2025.
- [9] G. Lu, L. Kou, P. Niu, G. Lv, X. Zhang, J. Liu, and Q. Xie, 'GPRTransNet: A deep learning-based ground-penetrating radar translation network,' 2024.
- [10] A. Afrasiabi, A. Faramarzi, D. Chapman, and A. Keshavarzi, 'Optimising ground penetrating radar data interpretation: A hybrid approach with AI-assisted Kalman filter and wavelet transform for detecting and locating buried utilities,' Journal of Applied Geophysics , vol. 232, p. 105567, 2025.
- [11] A. Paul, U. M. Jayapal, and R. Ayothiraman, 'A review of ground penetrating radar for underground utility detection and subsurface profiling: Challenges, strategies and a future-oriented framework,' Indian Geotechnical Journal , 2025.
- [12] V. Chandola, A. Banerjee, and V. Kumar, 'Anomaly detection: A survey,' ACM Computing Surveys , vol. 41, no. 3, pp. 1-58, 2009.
- [13] L. Ruff et al. , 'A unifying review of deep and shallow anomaly detection,' Proceedings of the IEEE , vol. 109, no. 5, pp. 756-795, 2021.
- [14] P. Vincent, H. Larochelle, Y. Bengio, and P.-A. Manzagol, 'Extracting and composing robust features with denoising autoencoders,' in Proc. 25th Int. Conf. Machine Learning (ICML) , 2008, pp. 1096-1103.
- [15] N. Q. Hoang, S. Kang, H.-K. Yoon, and J.-S. Lee, 'Enhancing anomaly detection in ground-penetrating radar images through reconstruction loss and high-variability,' 2024.
- [16] G. F. Angelis, D. Chorozoglou, S. Papadopoulos, A. Drosou, D. Giakoumis, and D. Tzovaras, 'AI-enabled underground water pipe nondestructive inspection,' Multimedia Tools and Applications , vol. 83, no. 6, pp. 18309-18332, 2024.
- [17] D. P. Kingma and J. Ba, 'Adam: A method for stochastic optimization,' in Proc. Int. Conf. Learning Representations (ICLR) , 2015.
- [18] V. Perez-Gracia, M. Solla, and S. Fontul, 'Analysis of the GPR signal for moisture detection: Application to heritage buildings,' International Journal of Architectural Heritage , vol. 18, no. 2, pp. 230-253, 2024.