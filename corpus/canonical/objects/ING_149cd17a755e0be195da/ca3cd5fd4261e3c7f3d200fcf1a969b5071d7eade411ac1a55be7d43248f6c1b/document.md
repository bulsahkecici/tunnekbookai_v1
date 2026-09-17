## ITERATED SPLITTING AND THE CLASSIFICATION OF KNOT TUNNELS

SANGBUM CHO AND DARRYL MCCULLOUGH

Abstract. For a genus-1 1-bridge knot in S 3 , that is, a (1 , 1)-knot, a middle tunnel is a tunnel that is not an upper or lower tunnel for some (1 , 1)-position. Most torus knots have a middle tunnel, and nontorus-knot examples were obtained by Goda, Hayashi, and Ishihara. In a previous paper, we generalized their construction and calculated the slope invariants for the resulting examples. We give an iterated version of the construction that produces many more examples, and calculate their slope invariants. If one starts with the trivial knot, the iterated constructions produce all the 2-bridge knots, giving a new calculation of the slope invariants of their tunnels. In the final section we compile a list of the known possibilities for the set of tunnels of a given tunnel number 1 knot.

## Introduction

Genus-2 Heegaard splittings of the exteriors of knots in S 3 have been a topic of considerable interest for several decades. They form a class large enough to exhibit rich and interesting geometric behavior, but restricted enough to be tractable. Traditionally such splittings are discussed with the language of knot tunnels, which we will use from now on.

The article [4] developed two sets of invariants that together give a complete classification of all tunnels of all tunnel number 1 knots. One is a finite sequence of rational 'slope' invariants, the other a finite sequence of 'binary' invariants. The latter is trivial exactly when the tunnel is a (1 , 1)-tunnel, that is, a tunnel that arises as the 'upper' or 'lower' tunnel of a genus-1 1-bridge position of the knot. In the language of [4], the (1 , 1)-tunnels are called semisimple, apart from those which occur as the well-known upper and lower tunnels of a 2-bridge knot, which are distinguished by the term 'simple'. The tunnels which are not (1 , 1)-tunnels are called regular.

For quite a long time, the only known examples of knots having both regular and (1 , 1)-tunnels were (most) torus knots, whose tunnels were classified by M. Boileau, M. Rost, and H. Zieschang [3] and independently by Y. Moriah [15]. Recently, another example was found by H. Goda and C. Hayashi [11]. The knot is the Morimoto-Sakuma-Yokota (5 , 7 , 2)-knot, and Goda and Hayashi credit H. Song with bringing it to their attention. Using his algorithm to compute tunnel invariants, K. Ishihara verified that the tunnel is regular, and in view of this, we refer to this example as the GodaHayashi-Ishihara tunnel. As noted in [11], a simple modification of their construction, varying a nonzero integer parameter n , produces an infinite collection of very similar examples.

Date : April 23, 2022.

1991 Mathematics Subject Classification. Primary 57M25.

Key words and phrases. knot, tunnel, (1,1), torus knot, regular, splitting, 2-bridge.

The second author was supported in part by NSF grant DMS-0802424.

In [9], we gave an extensive generalization of the Goda-Hayashi-Ishihara example, called the splitting construction, to produce all examples directly obtainable by the geometric phenomenon that underlies it. In addition, we gave an effective method to compute the full set of invariants of the examples. Our construction will be reviewed in Section 1.

In this paper, we develop an iterative method that begins with the result of a splitting construction. The steps are not exactly splittings in the sense of [9], but are similar enough that we may call this iterated splitting. The steps may be repeated an arbitrary number of times, giving an immense collection of new examples of regular tunnels of (1 , 1)-knots. At each step, a choice of nonzero integer parameter allows further variation. Starting from each of the four splitting constructions, we find two distinct ways to iterate, giving eight types of iteration. Section 2 describes the constructions in detail.

As with the splitting construction, the binary invariants of these new tunnels are easy to find, but the slope invariants require more effort. Fortunately, the general method given in [9] for tunnels obtained by splitting can be applied to obtain the slope invariants for the iterated construction, as we detail in Section 3. The method is effective and could easily be programmed to read off slope invariants at will.

The iterated splitting construction actually sits in plain view in a very familiar family of examples, the semisimple tunnels of 2-bridge knots. In Section 4, we present a special case of the iterated splitting method that, as one varies its parameters, produces all semisimple tunnels of all 2-bridge knots. No doubt there is a geometric way to verify this, but our proof is short and entirely algebraic: we simply calculate the slope sequences of the tunnels produced by the iterations and see that they are exactly the sequences that arise from this class of tunnels. The binary invariants are trivial in both cases, and since the invariants together form a complete invariant of a knot tunnel, the verification is complete.

The work in this paper greatly enlarges the list of known examples of tunnels having a pair of (1 , 1)-tunnels and an additional regular tunnel, motivating us to compile a list of known phenomena for the set of tunnels of a given tunnel number 1 knot. In the final section, we give the list of seven known cases, which includes three new cases apparent from examples recently found by John Berge using his software package Heegaard. The

Figure 1. ℓ , m , and T 3 , 5 .

<!-- image -->

Icon

authors are very grateful to John, not only for the new examples, but also for providing patient consultation to help us understand his methods.

Although we do provide a review of the splitting construction of [9], this paper presupposes a reasonable familiarity with that work. We have not included a review of the general theory of [4], as condensed reviews are already available in several of our articles. For the present paper, we surmise that Section 1 of [6] together with the review sections of [8] form the best option for most readers.

## 1. The splitting construction

In this section we will review the splitting construction from [9]. To set notation, Figure 1 shows a standard Heegaard torus T in S 3 , and an oriented longitude-meridian pair { ℓ, m } which will be our ordered basis for H 1 ( T ) and for the homology of a product neighborhood T × I . For a relatively prime pair of integers ( p, q ), we denote by T p,q a torus knot isotopic to a ( p, q )- curve in T . In particular, ℓ = T 1 , 0 and m = T 0 , 1 , also T p,q is isotopic in S 3 to T q,p in S 3 , T - p, - q = T p,q since our knots are unoriented.

Four kinds of disks, called dropλ , liftλ , dropρ , and liftρ disks, are used in the splitting construction. Figure 2(a) shows a torus knot T p + r,q + s , its middle tunnel τ , the principal pair { λ, ρ } of τ , the knots K ρ = T p,q , and K λ = T r,s , and a dropλ disk, called σ there. Figure 2(b) is an isotopic repositioning of the configuration of Figure 2(a): the vertical coordinate is the I -coordinate in a product neighborhood T × I , K τ and K λ lie on concentric tori in T × I , and the 1-handle with cocore σ is a vertical 1handle connecting tubular neighborhoods of these two knots. The term 'dropλ ' is short for 'dropK λ ', motivated by the fact that a copy of K λ can be dropped to a lower torus level, as in Figure 2(b).

A liftλ disk is similar, and is shown in Figure 3. Dropρ and liftρ disks are similar, except that they cut across the upper copy of λ , travel over the portion of the neighborhood of T p + r,q + s that does not contain the dropλ disks, and cut across the lower copy of λ , while staying disjoint from the copies of ρ .

ρ

Figure 2. The dropλ disk σ , first as seen in a neighborhood of K τ = T p + r,q + s and the tunnel τ , then after dropping K λ = T r,s and part of K ρ = T p,q .

<!-- image -->

Engineering drawing

ρ

Figure 3. The liftλ disk σ , first as seen in a neighborhood of K τ = T p + r,q + s and the tunnel τ , then after lifting K λ = T r,s and part of K ρ = T p,q .

<!-- image -->

Engineering drawing

The splitting constructions split off a copy of K ρ = T p,q or K λ = T r,s from K τ = T p + r,q + s , producing copies of these knots on two concentric torus levels, then sum the copies together by a pair of arcs with some number of twists. In the case of the the dropλ splitting, the first step was illustrated

<!-- image -->

Engineering drawing

τ

τ

Figure 4. The disk γ n is obtained from ρ by n right-handed half-twists along σ . The case n = 3 is shown here. For n &lt; 0, the half-twists are left-handed, while γ 0 = ρ .

<!-- image -->

Engineering drawing

Figure 5. The setup for the first general slope calculation.

in Figure 2. Next, consider the disk γ n shown in Figure 4. It is obtained from ρ by n right-handed half-twists along σ . When n &lt; 0, the twists are left-handed, while γ 0 = ρ . The γ n are nonseparating, since each meets K τ in a single point.

̸

Each γ n with n = 0 is a tunnel for the knot obtained by joining the copies of K τ and K λ in Figure 2 by a pair of vertical arcs that have n right-handed half-twists. That is, for n = 0 going from τ to γ n is a cabling construction replacing ρ , so that the principal pair of γ n is { λ, τ } . The case of n = 0 does not produce a cabling construction (that is, the resulting tunnel would be ρ so the principal path would have reversed direction).

̸

The liftλ , dropρ , and liftρ splittings are exactly analogous, using the liftλ , dropρ , and liftρ disks as σ in the respective cases.

The slope invariants of the resulting tunnels are the slopes of the disks γ n in certain coordinates. To calculate them, we need the slopes of the dropand lift-disks. We review the method used in [9], which will apply to the iterated construction that we will develop in this paper.

Figure 5 illustrates the setup for the slope calculation. The first drawing shows tubular neighborhoods of two (oriented) knots K U and K L , contained in a product neighborhood T × I of a Heegaard torus T of S 3 . The neighborhoods are connected by a vertical 1-handle to yield a genus-2 handlebody H . In our context, H will always be unknotted, although that is not needed for the calculations of this and the next section.

We interpret K U as the 'upper' knot, contained in T × [0 , 1 / 4) and K L as the 'lower' knot, contained in T × (3 / 4 , 1] (the I -coordinate of T × I increases as one moves downward in our figures). The vertical 1-handle with cocore σ is assumed to run between T ×{ 1 / 4 } and T ×{ 3 / 4 } , with σ as its intersection with T ×{ 1 / 2 } .

The disks D + U and D - U in Figure 5 are parallel in H , as are the disks D + L and D - L , and these four disks bound a ball B . Figure 5(a) shows a slope disk D . Associated to D is a slope-0 separating disk D 0 , defined by the requirement that it meets D in a single arc and the core circles of its complementary solid tori in H have linking number 0 in S 3 . For this setup, [9, Proposition 5.1] tells us the slope m σ of σ in ( D,D 0 )-coordinates.

The homology group H 1 ( T × I ) ∼ = H 1 ( T ) will have ordered basis the oriented longitude and meridian ℓ and m shown in Figure 1. Our linking convention is that Lk( m × { 1 } , ℓ × { 0 } ) = +1. Now, suppose that K U represents ( ℓ U , m U ) and K L represents ( ℓ L , m L ) in H 1 ( T × I ). Since Lk( m × { 0 } , ℓ ×{ 1 } ) = 0, we have Lk( K U , K L ) = m U ℓ L .

Proposition 1.1. In Figure 5, the slope m σ of σ in ( D,D 0 ) -coordinates is 2Lk( K U , K L ) . Consequently, if K U represents ( ℓ U , m U ) and K L represents ( ℓ L , m L ) in H 1 ( T × I ) , then m σ equals 2 m U ℓ L .

Proposition 6.1 of [9] then gives the slope of γ n .

Proposition 1.2. The slope of γ n in ( D,D 0 ) -coordinates is m σ +1 /n .

As detailed in [9, Proposition 7.1], applying Proposition 1.1 to splitting disks gives their slopes in terms of p , q , r , and s .

Corollary 1.3. The slopes of the splitting disks are as follows:

- (a) In ( ρ, ρ 0 ) -coordinates, the dropλ disk has slope 2 r ( q + s ) .
- (b) In ( ρ, ρ 0 ) -coordinates, the liftλ disk has slope 2 s ( p + r ) .
- (c) In ( λ, λ 0 ) -coordinates, the dropρ disk has slope 2 p ( q + s )
- (d) In ( λ, λ 0 ) -coordinates, the liftρ disk has slope 2 q ( p + r ) .

Proposition 1.2 then gives immediately the slopes of the tunnels obtained by splitting constructions using γ n .

## Proposition 1.4. For the torus knot T p + r,q + s :

- (a) A dropλ splitting has slope 2 r ( q + s ) + 1 /n .
- (b) A liftλ splitting has slope 2 s ( p + r ) + 1 /n .
- (c) A dropρ splitting has slope 2 p ( q + s ) + 1 /n .
- (d) A liftρ splitting has slope 2 q ( p + r ) + 1 /n .

## 2. The iterated splitting construction

We are now prepared to describe the iterated splitting construction. We begin with the dropρ case, as it is the case we will need in our later application to 2-bridge knots in Section 4. Figure 6(a) shows a knot resulting from

ρ

Figure 6. The first case of the dropρ iteration.

<!-- image -->

Engineering drawing

a dropρ splitting. Its tunnel will now be denoted by γ 0 n 0 , the superscript distinguishing it from later tunnels. Its principal pair { ρ, τ } is also shown.

In S 3 , γ 0 n 0 would appear with twists along the horizontal dropρ disk σ , so Figure 6(a) is only a picture up to abstract homeomorphism. Nonetheless, the vertical coordinate represents the levels of T × I , which will be true in the remaining drawings of Figure 6, so it will be seen that knots in 1-bridge position will always be obtained.

In Figure 6(b), γ 0 n 0 and a portion of the surrounding handlebody H have been shrunk vertically, keeping K γ 0 n 0 fixed. The horizontal line at the bottom is a copy of K ρ , as indicated. The picture of γ 0 n 0 without twisting is now accurate, but in the true picture in S 3 , the two vertical 1-handles would be intertwined by n 0 right-hand half-twists rather than being straight. The bottom part of the picture in S 3 , from the level K γ 0 n 0 and below, is as seen in Figure 6(b).

Figure 6(c) is obtained from Figure 6(b) by an isotopy of H , keeping K γ 0 n 0 and K ρ fixed. The effect is to create the setup picture of Figure 5(a) near τ , with K U = K γ 0 n 0 and K L = K ρ . Notice that in the orientations needed for the first general slope calculation, K ρ is oriented left-to-right, and K γ 0 n 0 must be oriented so that the portion that intersects τ and originally came from the copy of K ρ in the splitting construction used to create K γ 0 n 0 is also oriented from left-to-right. With this orientation on K γ 0 n 0 the top portion that originally came from K τ will be oriented from left-to-right or from right-to-left according as n 0 is odd or even. This will be a key observation when we compute the slope invariants of the iterated splitting constructions in Sections 3.

Figure 6(d) differs from Figure 6(c) only in that τ has been replaced by γ 1 n 1 , which in S 3 would be seen with n 1 right-hand half-twists. This is a cabling construction. The resulting knot K γ 1 n 1 is in 1-bridge position, and was obtained from K γ 0 n 0 and the copy of K ρ by connecting them with two vertical arcs with n 1 half-twists. The principal pair of γ 1 n 1 is { ρ, γ 0 n 0 } .

The stage is now set to repeat the construction using γ 0 n 0 and γ 1 n 1 in the role of τ and γ 0 n 0 in the previous step. Figure 6(e) is obtained from Figure 6(d) two steps, analogous to the steps from Figure 6(a) to Figure 6(b) and from Figure 6(b) to Figure 6(c). First, γ 1 n 1 is shrunk vertically, then H is moved as indicated, creating the setup picture of Figure 5(a) in the lower left-hand area of Figure 6(d). Again, in S 3 the two vertical 1-handles in the middle would be intertwined with n 1 half-twists. Another copy of K ρ appears at the bottom.

The next cabling construction replaces γ 0 n 0 by γ 2 n 2 , and K γ 2 n 2 is obtained by joining K γ 1 n 1 and the copy of K ρ with two vertical arcs with n 2 halftwists. The principal pair of γ 2 n 2 is { ρ, γ 1 n 1 } . The true picture in S 3 has n 0 half-twists in the two vertical 1-handles connecting the top and second levels of Figure 5(e), n 1 half-twists in the two vertical 1-handles connecting the second and third levels, and γ 2 n 2 appears with n 2 half-twists.

The iteration can be continued indefinitely, producing a sequence of tunnels γ m n m with principal pairs { ρ, γ m - 1 n m - 1 } , and the knots K γ m nm in (1 , 1)- position.

We indicate this sequence by τ ց ρ γ 0 n 0 ց ρ γ 2 n 1 ց ρ · · · . The cabling constructions in the iterations all retain ρ in their principal pairs so have binary invariant 0, although the original dropρ splitting that produces γ 0 n 0 may have nontrivial binary invariant.

From Figure 6(a) there is a second way to proceed. Figure 7 shows an alternative to the isotopy in Figure 6(b), that shrinks γ 0 n 0 upward. The next step replaces ρ by γ 1 n 1 , which has principal pair { τ, γ 0 n 0 } , and K γ 1 n 1 is obtained by joining copies of K γ 0 n 0 and K τ by vertical arcs. The successive iterations each add on another copy of K τ , moving upward, and retain τ in their principal pairs. We indicate this sequence by τ ց ρ γ 0 n 0 τ ր γ 1 n 1 τ ր γ 2 n 2 τ ր · · · . The up-or-down direction of the diagonal arrow indicates whether the knot that is joined to the previous one is a copy of the original K U (in this case, K τ ) or the original K L (in this case, K ρ ), and the letter above it indicates which of ρ , λ , or τ is retained in the principal pair.

Figure 7. The second case of the dropρ iteration.

<!-- image -->

Engineering drawing

Starting with the dropλ splitting instead of the dropρ splitting produces two more interations,

<!-- formula-not-decoded -->

Starting with the liftρ splitting instead of the dropρ splitting produces two more,

<!-- formula-not-decoded -->

and starting these with the liftλ splitting give the latter two but with λ replacing ρ . Provided that one started with a tunnel τ which was not trivial and not simple, the eight sequences are distinct, since they have distinct principal paths.

## 3. The iterated splitting slope invariants

We begin with the slope invariants. Consider the first iteration discussed in Section 2, whose initial steps were illustrated in Figure 6. The initial step is a regular dropρ splitting, and according to Proposition 1.4(c), the slope of the resulting tunnel disk γ 0 n 0 is 2 p ( q + s ) + 1 /n 0 .

The first iterate γ 1 n 1 is obtained using the setup of Figure 5(a) with K U = K γ 0 n 0 and K L = K ρ as in Figure 6(c). Now K γ 0 n 0 is obtained by connecting K τ = T p + r,q + s and K ρ = T p,q with two arcs intertwined with n 0 half-twists. The portion of K γ 0 n 0 seen in setup picture for calculating the slope of γ 1 n 1 must be oriented from left-to-right, so it is obtained by adding the left-toright orientation of K ρ to either the left-to-right or right-to-left orientation of K τ , according as n 0 is odd or even. In H 1 ( T × I ), K τ (with left-to-right orientation) represents ( p + r, q + s ) and K ρ represents ( p, q ), so K γ 0 n 0 with this orientation represents ( p, q ) + ( - 1) 1+ n 0 ( p + r, q + s ) = (1+( - 1) 1+ n 0 )( p, q ) + ( - 1) 1+ n 0 ( r, s ). Therefore Lk( K γ 0 n 0 , K ρ ) = p ((1 + ( - 1) 1+ n 0 q + ( - 1) 1+ n 0 s ), and by Proposition 1.1 the slope of γ 1 n 1 in ( τ, τ 0 )-coordinates is 2 pq (1 + ( - 1) 1+ n 0 ) + 2 ps ( - 1) 1+ n 0 +1 /n 1 .

To continue this process, let us put ǫ ( k ) = ( - 1) 1+ n k , t ( r, k ) = ǫ ( r ) ǫ ( r + 1) · · · ǫ ( k - 1) for r &lt; k , and t ( k, k ) = 0. Now, define

<!-- formula-not-decoded -->

In particular, a (0) = A (0) = 1, a (1) = ǫ (0), A (1) = 1 + ǫ (0), and since ǫ ( k ) t ( r, k ) = t ( r, k +1),

<!-- formula-not-decoded -->

We orient each K γ k n k so that the portion that came from K L = K ρ is left-to-right, as this is the orientation needed in order to compute the slope of γ k +1 n k +1 in the setup of Figure 5(a). In H 1 ( T × I ), K γ 0 n 0 represents ( p, q ) + ǫ (0)( p + r, q + s ) = A (1)( p, q ) + a (1)( r, s ). For k ≥ 1 assume inductively that K γ k - 1 n k - 1 represents A ( k ) ( p, q ) + a ( k ) ( r, s ). In the orientation on K γ k n k , the direction on the portion from K γ k - 1 n k - 1 must be reversed exactly when n k is even. Therefore in H 1 ( T × I ), K γ k n k represents

<!-- formula-not-decoded -->

completing the induction.

For all k ≥ 1, then, Lk( K γ k - 1 n k - 1 , K ρ ) = p ( A ( k ) q + a ( k ) s ), and Proposition 1.1 gives the slope of γ k n k to be 2 p ( A ( k ) q + a ( k ) s ) + 1 /n k .

We now consider the second case τ ց ρ γ 0 n 0 τ ր γ 1 n 1 τ ր γ 2 n 2 τ ր · · · of the dropρ iteration. For the iterative step, when computing the slope of γ n k +1 , the setup picture Figure 5(a) has K U = K τ and K L = K γ k n k , the latter oriented so that its top portion is K τ oriented left-to-right, and bottom portion, originally K γ k - 1 n k - 1 , has top portion (from K τ ) oriented left-to-right or right-to-left according as n k is odd or even. For k = 0, K γ n 0 with this orientation represents

<!-- formula-not-decoded -->

Inductively, assume that K γ k - 1 n k - 1 represents ( A ( k ) - a ( k ))( p + r, q + s ) + a ( k )( p, q ). Then, with the needed orientation for the setup picture, K γ k n k represents

<!-- formula-not-decoded -->

The slope calculation of γ k n k is then

<!-- formula-not-decoded -->

These calculations have established the first two cases of the following result. Each of the remaining six cases is very similar to one of the first two. Summarizing, we have

Theorem 3.1. The slopes of the tunnels in the iterated splitting sequences for the torus knot T p + r,q + s are as follows.

| sequence   | sequence    | sequence    | sequence   | slope of γ k n k                                        |
|------------|-------------|-------------|------------|---------------------------------------------------------|
| τ          | ց ρ γ 0 n 0 | ց ρ γ 1 n 1 | ց ρ · · ·  | 2 p ( A ( k ) q + a ( k ) s )+1 /n k                    |
| τ          | ց ρ γ 0 n 0 | τ ր γ 1 n 1 | τ ր · · ·  | 2( q + s ) ( A ( k ) p +( A ( k ) - a ( k )) r )+1 /n k |
| τ          | ց λ γ 0 n 0 | ց λ γ 1 n 1 | ց λ · · ·  | 2 r ( A ( k ) s + a ( k ) q )+1 /n k                    |
| τ          | ց λ γ 0 n 0 | τ ր γ 1 n 1 | τ ր · · ·  | 2( q + s ) ( A ( k ) r +( A ( k ) - a ( k )) p )+1 /n k |
| τ          | ρ ր γ 0 n 0 | ρ ր γ 1 n 1 | ρ ր · · ·  | 2 q ( A ( k ) p + a ( k ) r )+1 /n k                    |
| τ          | ρ ր γ 0 n 0 | ց τ γ 1 n 1 | ց τ · · ·  | 2( p + r ) ( A ( k ) q +( A ( k ) - a ( k )) s )+1 /n k |
| τ          | λ ր γ 0 n 0 | λ ր γ 1 n 1 | λ ր · · ·  | 2 s ( A ( k ) r + a ( k ) p )+1 /n k                    |
| τ          | λ ր γ 0 n 0 | ց τ γ 1 n 1 | ց τ · · ·  | 2( p + r ) ( A ( k ) s +( A ( k ) - a ( k )) q )+1 /n k |

The binary invariants produced by splitting and iterated splitting are easily determined. When ρ is one of the disks of the principal pair of a tunnel (that is, one of the two disks in the principal vertex other than the tunnel disk itself), a dropρ or liftρ splitting or iterative step retains ρ and replaces the other disk of the principal pair. Thus, for example, in the all dropρ iteration, every binary invariant is 0 except possible that of the splitting, which depends on the cabling construction that preceded it (that is, the invariant is 0 if ρ was in the principal pair of the tunnel for the cabling construction that preceded the splitting, and 1 if ρ was the previous tunnel). In a sequence such as τ ց ρ γ 0 n 0 τ ր γ 1 n 1 τ ր · · · , the second binary invariant, associated to the first liftτ step of the iteration, has binary invariant 1, and all others except possibly the initial splitting have binary invariant 0.

Since a splitting-and-iteration sequence can never have more than two binary invariants equal to 1, with the two 1's contiguous in that case, the sequence can never increase the depth by more than 1 from that of the starting torus tunnel (see for example the last paragraph of Section 3 of [7]).

## 4. Two-bridge knots

A good example of the iterated splitting construction is furnished by 2bridge knots. Indeed, in some sense the iterated splitting construction is a far-reaching generalization of 2-bridge knots. In this section, we will see that any dropρ iteration of the first kind examined in Sections 2 and 3 and starting with the trivial knot positioned as T 1 , 1 produces a 2-bridge knot in the (1 , 1)-position whose upper tunnel is the upper semisimple tunnel of the knot, and moreover that every semisimple tunnel of every 2-bridge knot can be obtained in this way.

We wil use the notation and the description of the classification of 2bridge knots presented in [8, Section 10]. We first recall the calculation of the slope invariants of the upper semisimple tunnel of a 2-bridge knot given in [8, Proposition 10.4]:

̸

Proposition 4.1. Let K be a 2 -bridge knot in the 2 -bridge position corresponding to the continued fraction [2 a d , 2 b d , . . . , 2 a 0 , 2 b 0 ] , with b 0 = 0 and each a i = ± 1 . Then the slope invariants of the upper semisimple tunnel of K are as follows:

<!-- formula-not-decoded -->

- (ii) For 1 ≤ i ≤ d , m i = - 2 a i - 1 +1 /k i , where
- (a) k i = 2 b i +1 if a i = a i - 1 = 1 ,
- (b) k i = 2 b i if a i and a i - 1 have opposite signs, and
- (c) k i = 2 b i - 1 if a i = a i - 1 = - 1 .

Fix K as in Proposition 4.1. Denote the slope invariants of its upper semisimple tunnel as given in Proposition 4.1 by m 0 , . . . , m d .

Starting with the trivial knot T 1 , 1 , we will carry out a dropρ splitting and iteration, that is, the first type detailed in each of Sections 2 and 3. We have

<!-- formula-not-decoded -->

thus ( p, q ) = (1 , 0), ( r, s ) = (0 , 1), and K ρ = T 1 , 0 .

Perform the initial dropρ splitting with n 0 equal to 2 b 0 if a 0 = 1 and to 2 b 0 - 1 if a 0 = - 1. Note that every nonzero choice of n 0 occurs for some m 0 . By Proposition 1.4(c) (or Theorem 3.1 with k = 0), the slope of γ 0 n 0 is 2 + 1 /n 0 , so its simple slope is [ n 0 / (2 n 0 +1)]. By Proposition 4.1(i), this is m 0 .

Now we carry out the first d steps of the iteration, using n r = k r at each step. Again, every possible nonzero value of n r occurs for some choice of K . We have m 1 = - 2 a 0 +1 /k 1 . If a 0 = 1, then n 0 was even and (using the notation of Section 3) a (1) = ( - 1) 1+ n 0 = - 1. If a 0 = - 1, then n 0 was odd and a (1) = 1. In either case, a (1) = - a 0 . Theorem 3.1 gives the slope of γ 1 n 1 to be 2 a (1) + 1 /n 1 = - 2 a 0 +1 /k 1 = m 1 .

For r ≥ 2, assume inductively that a ( r ) = - a r - 1 . If n r = k r is even, then we are in Case (ii)(b) of Proposition 4.1, and a r - 1 = - a r . We find that a ( r +1) = ( - 1) 1+ n r a ( r ) = - a ( r ) = a r - 1 = - a r . If n r is odd, then we are in Case (ii)(a) or (ii)(c) of Proposition 4.1, and a r - 1 = a r . We find that a ( r +1) = ( - 1) 1+ n r a ( r ) = a ( r ) = - a r - 1 = - a r , completing the induction.

Theorem 3.1 now gives the slope of γ r n r to be

<!-- formula-not-decoded -->

completing the induction.

## 5. Classification of tunnels

At this point in history one may begin to contemplate a classification of tunnels of tunnel number 1 knots based on the examples that have been found during the past several decades. In this section we will list the cases that occur or appear to occur. It is plausible that this list may be complete or nearly so, but we are unaware of any evidence supporting this other than the absence of other examples found and a sense that there ought to be a fairly strict limitation on the complexity of tunnel behavior for a given knot.

In our list it is to be understood that in some cases, tunnels are equivalent due to symmetries or degeneracies. For example, the upper and lower tunnels of a 2-bridge knot may be equivalent under an involution of S 3 preserving the knot, and the middle tunnel of a torus knot is known to be isotopic to the upper or lower tunnel for certain cases (and hence is a (1 , 1)-tunnel rather than a regular tunnel).

We list the cases, then comment on them below.

Known Tunnel Phenomena. These are the known possibilities for the set of tunnels of a tunnel number 1 knot K , allowing some of the tunnels to be equivalent due to symmetries or degeneracies:

- I. K has a unique regular tunnel.
- II. K has one (1 , 1) -position and two (1 , 1) -tunnels.
- III. K has two (1 , 1) -positions and four (1 , 1) -tunnels.
- IV. K has one (1 , 1) -position and two (1 , 1) -tunnels, plus one regular tunnel.
- V. K has two (1 , 1) -positions and four (1 , 1) -tunnels, plus one regular tunnel.
- VI. K has one (1 , 1) -position and two (1 , 1) -tunnels, plus two regular tunnels.
- VII. K has no (1 , 1) -position, but has two regular tunnels.

We now comment on the individual cases.

Case I

As explained in [7, Section 3], results of M. Scharlemann and M. Tomova [18] and J. Johnson [14] combine to show that whenever K has a tunnel of Hempel distance at least 6 (that is, the Hempel distance of the associated genus-2 Heegaard splitting of the exterior of K ), it is the unique tunnel of K . Thus Case I holds for all high-distance tunnels.

## Case II

This seems likely to be the generic case when K has a (1 , 1)-tunnel, although we are not aware of any examples for which it has been proven that a specific knot admits exactly two (1 , 1)-tunnels, other than symmetric or degenerate cases such as torus knots for which the middle tunnel is equivalent to the upper or lower (1 , 1)-tunnel.

## Case III

Tunnels of 2-bridge knots are fully classified due to work of several authors, and they satisfy Case III. D. Heath and H. Song [12] proved that the ( - 2 , 3 , 7)-pretzel knot satisfies Case III, and there are expected to be other examples.

## Case IV

Torus knots and their middle tunnels are the long-known examples of Case IV. Assuming that at least some of them have no other unknown tunnels, the examples generated in [9] and this paper provide more such knots. See also the comments on the remaining three cases.

## Cases V, VI, and VII

These remaining cases describe examples recently found and kindly provided to us by John Berge [1]. They were obtained using his software Heegaard, which works with two-generator one-relator presentations of π 1 ( S 3 - K ) whose generators are free generators of the fundamental group of the exterior handlebody H ′ = S 3 - H , and whose relator is represented by the boundary C of a tunnel disk D in H . The knot K is the usual knot associated to D , that is, a core circle of the solid torus H - N ( D ), where N ( D ) is a regular neighborhood of D in H . Heegaard is able to distinguish equivalence classes of such C under diffeomorphism of H ′ , showing that the tunnel disks they bound cannot be equivalent. Regularity of the tunnels can be tested by using a procedure (also used by K. Ishihara [13]) that finds the principal meridian pair for K associated to a tunnel, and then checking whether either of the disks is primitive; primitivity of a disk E ⊂ H in our sense (that is, ∂E crosses the boundary of some disk E ′ ⊂ H ′ exactly once) is equivalent to primitivity of ∂E as an element of π 1 ( H ′ ), and can be checked algebraically.

Once a tunnel has been found, the software searches for more tunnels for the knot by a method that generates a large number of additional such two-generator one-relator presentations for π 1 ( S 3 - K ) and tests them for isomorphism with those already found. Although there is no known means to ensure that this method finds all of the tunnels for these examples, it seems likely that it does. For example, for the ( - 2 , 3 , 7)-pretzel knot, all four tunnels are found among the first few of the large number of presentations that the software examines.

Berge examined the hyperbolic double-primitive knots K having Dehn surgeries that produce lens spaces L ( p, q ) with p &lt; 100, and the 'sporadic' double-primitive knots of Types 9, 10, 11, and 12 (detailed in J. Berge [2])

having Dehn surgeries that produce lens spaces L ( p, q ) with p &lt; 500, as well as some non-double-primitive knots. Assuming that the software did find all tunnels of those knots, the possibilities listed in Cases V, VI, VII were obtained, as well as quite a few instances of the other cases including Case IV. Some of the examples of Case VII occurred for knots that are not double-primitive. We do not know whether the regular tunnels in his examples of Cases IV, V, and VI arise from (1 , 1)-positions by the construction we have examined in this paper.

## References

1. J. Berge, personal communication. He may be contacted at jberge@charter.net for additional information about Heegaard.
2. J. Berge, Some knots with surgeries yielding lens spaces, preprint.
3. M. Boileau, M. Rost, and H. Zieschang, On Heegaard decompositions of torus knot exteriors and related Seifert fibre spaces, Math. Ann. 279 (1988), 553-581.
4. S. Cho and D. McCullough, The tree of knot tunnels, Geom. Topol. 13 (2009) 769-815.
5. S. Cho and D. McCullough, Cabling sequences of tunnels of torus knots, Algebr. Geom. Topol. 9 (2009) 1-20.
6. S. Cho and D. McCullough, Constructing knot tunnels using giant steps, Proc. Amer. Math. Soc. 138 (2010), 375-384.
7. S. Cho and D. McCullough, Tunnel leveling, depth, and bridge numbers, Trans. Amer. Math. Soc. 353 (2011), 259-280.
8. S. Cho and D. McCullough, Semisimple tunnels, arXiv:1006.5232.
9. S. Cho and D. McCullough, Middle tunnels by splitting, arXiv:1108.3425
10. S. Cho and D. McCullough, software available at math.ou.edu/ ˜ dmccullough .
11. H. Goda and C. Hayashi, Genus two Heegaard splittings of exteriors of 1-genus 1bridge knots, to appear in Kobe J. Math.
12. D. Heath and H.-J. Song, Unknotting tunnels for P ( - 2 , 3 , 7), J. Knot Theory Ramifications 14 (2005), 1077-1085.
13. K. Ishihara, An algorithm for finding parameters of tunnels, Alg. Geom. Topology. 11 (2011), 2167-2190.
14. J. Johnson, Bridge number and the curve complex, arXiv math.GT/0603102.
15. Y. Moriah, Heegaard splittings of Seifert fibered spaces, Invent. Math. 91 (1988), 465-481.
16. K. Morimoto and M. Sakuma, On unknotting tunnels for knots, Math. Ann. 289 (1991), 143-167.
17. K. Morimoto, M. Sakuma, and Y.Yokota, Examples of tunnel number 1 knots which have the '1 + 1 = 3' property, Math. Proc. Camb. Phil. Soc. 119 (1996), 113-118.
18. M. Scharlemann and M. Tomova, Alternate Heegaard genus bounds distance, Geom. Topol. 10 (2006), 593-617.

Department of Mathematics Education, Hanyang University, Seoul 133-791, Korea

E-mail address :

scho@hanyang.ac.kr

Department of Mathematics, University of Oklahoma, Norman, Oklahoma 73019, USA

E-mail address : dmccullough@math.ou.edu URL : www.math.ou.edu/ ˜ dmccullough/