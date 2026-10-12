# Citation map

The manuscript uses `biblatex` with the `numeric` style. Printed numbers are generated from first citation order; the stable identifiers below are the keys in `paper/references.bib`. The source numbers in the thesis have no chapter or page suffixes.

This map records the passages used to check the background and the provenance of the displayed mathematics. It accompanies the sentence-level citations in the manuscript.

## German and Ukrainian background

Page numbers in this table refer to the page numbers printed in the source, rather than the PDF viewer's page index.

| Key | Source and language | Checked material |
| --- | --- | --- |
| `robotikde` | Christian Ott and Christian Hartl-Nesic, *Grundlagen der Robotik*, TU Wien, lecture manuscript 2025W; German | Chapter 3, pp. 45–69: coordinates, translation, rotation matrices, pose, homogeneous transformations, composition and inversion, skew matrices, axis–angle and exponential coordinates, Rodrigues' formula and scalar-first unit quaternions. [PDF](https://www.acin.tuwien.ac.at/file/teaching/master/Grundlagen_der_Robotik_VU/VU_Grundlagen_der_Robotik_2025W_Vorlesungsskript.pdf) |
| `wernerde` | Jochen Werner, *Numerische Lineare Algebra*, Göttingen, lecture manuscript, summer semesters 1998 and 2001; German | Section 1.3: notation and norms; Chapter 3, especially Sections 3.1, 3.3 and 3.5: least squares, SVD, pseudoinverse and sensitivity; Chapter 4: symmetric eigenproblems. [PDF](https://num.math.uni-goettingen.de/werner/numlin.pdf) |
| `buldyhinua` | В. В. Булдигін and co-authors, *Лінійна алгебра та аналітична геометрія*, ТВіМС, Kyiv, 2011; Ukrainian | Sections 1–4: matrices, transpose, multiplication, inverses, rank and linear systems; Sections 7–10: vectors, coordinates, scalar and vector products. Matrix arithmetic on pp. 9–17; scalar product on pp. 77–83; vector product beginning on p. 84. [KPI record](https://ela.kpi.ua/handle/123456789/16193) · [PDF](https://ela.kpi.ua/bitstreams/a3fd9323-b354-4e5d-88e2-6cc5ff8bdb29/download) |
| `bokhonovua` | Юрій Євгенович Бохонов, *Алгебра та геометрія: Лінійна алгебра*, КПІ ім. Ігоря Сікорського, Kyiv, 2021; Ukrainian | Section 2.4, pp. 85–87: spectral properties and extremal eigenvalue characterisation; Section 2.5, pp. 87–89: quaternion multiplication, conjugation and inverse; Chapter 5, especially Sections 5.2, 5.4 and 5.6: spectral decomposition, matrix functions and SVD. [KPI record](https://ela.kpi.ua/handle/123456789/42336) · [PDF](https://ela.kpi.ua/bitstreams/07ca0b1a-85f4-462d-b1e2-c1a0366ba75d/download) |
| `wenhardtde` | Stefan Wenhardt, *Ansichtenauswahl für die 3-D-Rekonstruktion statischer Szenen*, doctoral dissertation, Erlangen, 2013; German | Sections 2.1–2.2: projection and camera calibration; Section 2.3, pp. 27–31, especially Eqs. (2.31)–(2.44): rigid hand–eye relationship, relative-motion equation, rotation/translation split and nonparallel-axis observability. [PDF](https://www5.cs.fau.de/fileadmin/research/Publikationen/2013/Wenhardt13-AFD.pdf) |
| `halconde` | MVTec Software GmbH, HALCON 24.11 operator reference, *Hand-Auge-Kalibrierung*; German | “Bewegte Kamera”, “Stationäre Kamera” and acquisition guidance: fixed mounting relationships, robot and target poses, coordinate chains, intrinsic calibration and correspondence of image and robot observations. This source supports geometric and acquisition background; OpenCV behaviour is checked in OpenCV's own documentation and code. [Reference](https://www.mvtec.com/doc/halcon/2411/de/hand_eye_calibration.html) |
| `eauncertainty` | European co-operation for Accreditation, *Ermittlung der Messunsicherheit bei Kalibrierungen*, EA-4/02 M: 2022, DAkkS German translation dated 31 August 2022 | Sections 2–4: measurement model, input uncertainty, repeated observations, mean and propagation; Appendix D: correlated input quantities and shared uncertainty contributions. The thesis specifies its own accuracy, consistency and repeatability metrics using this measurement background. [PDF](https://www.dakks.de/files/Dokumentensuche/Dateien/EA-4-02%20M%202022_%C3%9Cbersetzung_Deutsche%20%C3%9Cbersetzung.pdf) |
| `dfgde` | Deutsche Forschungsgemeinschaft, *Leitlinien zur Sicherung guter wissenschaftlicher Praxis: Kodex*, corrected version 1.2, September 2024; German | Guidelines 11 and 12: documented methods, reproducibility and retention of results, including results that do not support a hypothesis. Used for the documentation and reporting rationale. [Publisher-linked record](https://zenodo.org/records/14281892) |

The entries are identified as textbooks, lecture manuscripts, a dissertation or technical guidance according to the source itself.

## Original method and software sources

The existing English original papers remain for the exact algorithms: `tsai`, `park`, `horaud`, `andreff` and `daniilidis`. The professor's recommended Corke book (`corke`), Tsai–Lenz paper and OpenCV documentation (`opencv`) remain in the bibliography. `marr2010` supports the attributed opening quotation. Wikipedia is not a reference.

Implementation claims use `opencvsource`, checked against Git blob `909bcedee6d34e5ebb6ada0fec19a6f4c6e9ed2c` in `modules/calib/src/calibration_handeye.cpp`. In particular:

| Routine | Checked behaviour |
| --- | --- |
| `calibrateHandEyeTsai` | Relative-motion construction, quaternion-vector thresholds 0.3 and 1.7, three-column rotation system, retained pairs in the translation fit |
| `calibrateHandEyePark` | Rotation-vector alignment, eigenvalue-based inverse square root, separate translation fit |
| `calibrateHandEyeHoraud` | Quaternion multiplication matrices, smallest eigenvector, separate translation fit |
| `normalizeRotation` / `calibrateHandEyeAndreff` | Row-wise reshaping, Kronecker blocks, joint linear system, determinant scaling and SVD projection, translation retained from the joint solve |
| `calibrateHandEyeDaniilidis` | Six-row dual-quaternion system, two smallest right singular vectors, quadratic roots and normalisation selection |

## Author calculations and choices

The numerical coordinate example, scalar least-squares example, diagonal eigenproblem, illustrative Tsai quaternion, constructed matrix check and translation example in Appendix B use values chosen in this thesis. Their citations identify the rules used in the calculation. They are not reported laboratory observations or reproductions of source-specific numerical examples.

Intermediate algebra is adapted to this thesis's notation and transformation directions. The eye-to-hand rearrangement is obtained from the fixed-pose coordinate chain. The determinant correction for a proper SVD rotation is derived in Section 4.3 from orthogonality and spectral properties, and the nearest-rotation interpretation is checked by expanding the Frobenius norm. Synthetic data and evaluation metrics are constructed from the cited geometric relations.

The proposed experimental choices, research question, document structure, personal acknowledgments and declaration are statements by the author. Sources cited alongside experimental choices support their mathematical or measurement rationale. Results and conclusions await the experiments.

## Displayed mathematics inventory

Every displayed equation block in the current manuscript has an adjacent `\mathsource{...}` citation. A block with multiple lines uses the listed sources for the complete derivation. Inline mathematical assertions are sourced in their surrounding sentences; technical table rows also carry citations.

| Block | Subsection | Equation label or first expression | Source keys | Provenance |
| --- | --- | --- | --- | --- |
| 1 | A Physical Point and Its Coordinates | `p=\begin{pmatrix}p_x\\p_y\\p_z\end{pmatrix}.` | `robotikde` | Relation or notation adapted from the cited background |
| 2 | Reading the Vector and Matrix Expressions | `(Rp)_i=R_{i1}p_x+R_{i2}p_y+R_{i3}p_z,\qquad i=1,2,3.` | `buldyhinua` | Relation or notation adapted from the cited background |
| 3 | Reading the Vector and Matrix Expressions | `u^\top v=u_xv_x+u_yv_y+u_zv_z.` | `buldyhinua` | Relation or notation adapted from the cited background |
| 4 | Reading the Vector and Matrix Expressions | `\\|u\\|=\sqrt{u^\top u}=\sqrt{u_x^2+u_y^2+u_z^2}.` | `buldyhinua` | Relation or notation adapted from the cited background |
| 5 | Direction of a Transformation | `eq:pointmap` | `robotikde` | Relation or notation adapted from the cited background |
| 6 | Rotation Matrices | `eq:so3` | `robotikde` | Relation or notation adapted from the cited background |
| 7 | Rotation Matrices | `\mathrm{SO}(3)=\{R\in\mathbb R^{3\times3}:R^\top R=I_3,\ \det R=1` | `robotikde` | Relation or notation adapted from the cited background |
| 8 | Rotation Matrices | `R_z(90^\circ)=` | `robotikde` | Relation or notation adapted from the cited background |
| 9 | A Numerical Coordinate Example | `t=\begin{pmatrix}100\\20\\0\end{pmatrix}\ \mathrm{mm}.` | `robotikde` | Author-chosen numerical example using cited premises |
| 10 | A Numerical Coordinate Example | `{}^{a}p=` | `robotikde` | Author-chosen numerical example using cited premises |
| 11 | Homogeneous Coordinates | `eq:homogeneous` | `robotikde` | Relation or notation adapted from the cited background |
| 12 | Homogeneous Coordinates | `\mathrm{SE}(3)=` | `robotikde` | Relation or notation adapted from the cited background |
| 13 | Composition and Inversion | `eq:composition` | `robotikde` | Relation or notation adapted from the cited background |
| 14 | Composition and Inversion | `eq:block-product` | `robotikde` | Relation or notation adapted from the cited background |
| 15 | Composition and Inversion | `eq:inverse` | `robotikde` | Relation or notation adapted from the cited background |
| 16 | Axis--Angle Representation | `r=\theta n,\qquad \\|n\\|=1.` | `robotikde` | Relation or notation adapted from the cited background |
| 17 | Axis--Angle Representation | `eq:skew` | `robotikde` | Relation or notation adapted from the cited background |
| 18 | Axis--Angle Representation | `eq:rodrigues` | `robotikde` | Relation or notation adapted from the cited background |
| 19 | Axis--Angle Representation | `p_\parallel=n(n^\top p),\qquad p_\perp=p-p_\parallel.` | `robotikde` | Relation or notation adapted from the cited background |
| 20 | Axis--Angle Representation | `Rp=p_\parallel+\cos\theta\,p_\perp+` | `robotikde` | Relation or notation adapted from the cited background |
| 21 | Axis--Angle Representation | `R=nn^\top+\cos\theta(I_3-nn^\top)+\sin\theta[n]_\times.` | `robotikde` | Relation or notation adapted from the cited background |
| 22 | Unit Quaternions | `q=\begin{pmatrix}q_0\\v\end{pmatrix}` | `robotikde` | Relation or notation adapted from the cited background |
| 23 | Unit Quaternions | `eq:quaternion-product` | `bokhonovua`, `robotikde` | Relation or notation adapted from the cited background |
| 24 | Unit Quaternions | `(0,Rp)=q\otimes(0,p)\otimes q^*.` | `bokhonovua`, `robotikde` | Relation or notation adapted from the cited background |
| 25 | Unit Quaternions | `eq:quaternion-rotation` | `robotikde` | Relation or notation adapted from the cited background |
| 26 | Least Squares: Fitting Imperfect Equations | `eq:least-squares` | `wernerde` | Relation or notation adapted from the cited background |
| 27 | Least Squares: Fitting Imperfect Equations | `D=U\Sigma V^\top.` | `wernerde` | Relation or notation adapted from the cited background |
| 28 | Homogeneous Systems and Physical Constraints | `\min_{\\|z\\|=1}\\|Dz\\|^2.` | `bokhonovua`, `wernerde` | Relation or notation adapted from the cited background |
| 29 | What the Camera Measures | `eq:pinhole` | `wenhardtde` | Relation or notation adapted from the cited background |
| 30 | What the Camera Measures | `K=\begin{pmatrix}f_x&0&c_x\\0&f_y&c_y\\0&0&1\end{pmatrix}.` | `wenhardtde` | Relation or notation adapted from the cited background |
| 31 | Frames and Available Poses | `G_k={}^{b}T_g^{(k)},` | `halconde` | Relation or notation adapted from the cited background |
| 32 | Frames and Available Poses | `C_k={}^{c}T_t^{(k)},` | `halconde` | Relation or notation adapted from the cited background |
| 33 | Eye-in-Hand: A Camera Attached to the Gripper | `X={}^{g}T_c,` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 34 | Eye-in-Hand: A Camera Attached to the Gripper | `\text{target}\ \longrightarrow\ \text{camera}\` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 35 | Eye-in-Hand: A Camera Attached to the Gripper | `eq:eye-in-hand-loop` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 36 | Eye-in-Hand: A Camera Attached to the Gripper | `G_iXC_i=G_jXC_j.` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 37 | Eye-in-Hand: A Camera Attached to the Gripper | `G_j^{-1}G_iXC_i=XC_j.` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 38 | Eye-in-Hand: A Camera Attached to the Gripper | `G_j^{-1}G_iX=XC_jC_i^{-1}.` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 39 | Eye-in-Hand: A Camera Attached to the Gripper | `eq:relative-motions` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 40 | Eye-in-Hand: A Camera Attached to the Gripper | `eq:axxb` | `halconde`, `wenhardtde` | Relation or notation adapted from the cited background |
| 41 | Eye-to-Hand: A Camera Fixed Relative to the Base | `X={}^{b}T_c,\qquad Z={}^{g}T_t.` | `halconde`, `robotikde` | Relation or notation adapted from the cited background |
| 42 | Eye-to-Hand: A Camera Fixed Relative to the Base | `eq:eye-to-hand` | `halconde`, `robotikde` | Relation or notation adapted from the cited background |
| 43 | Eye-to-Hand: A Camera Fixed Relative to the Base | `(H_j^{-1}H_i)X=X(C_jC_i^{-1}),` | `halconde`, `robotikde` | Relation or notation adapted from the cited background |
| 44 | Separating Rotation and Translation | `A=\begin{pmatrix}R_A&t_A\\0&1\end{pmatrix},\quad` | `wenhardtde` | Relation or notation adapted from the cited background |
| 45 | Separating Rotation and Translation | `AX=\begin{pmatrix}R_AR_X&R_At_X+t_A\\0&1\end{pmatrix},` | `wenhardtde` | Relation or notation adapted from the cited background |
| 46 | Separating Rotation and Translation | `eq:rotation-handeye` | `wenhardtde` | Relation or notation adapted from the cited background |
| 47 | Separating Rotation and Translation | `eq:translation-stack` | `wenhardtde`, `wernerde`, `opencvsource` | Relation or notation adapted from the cited background |
| 48 | What Makes a Dataset Informative? | `R_A=R_XR_BR_X^\top.` | `wenhardtde` | Relation or notation adapted from the cited background |
| 49 | A Constructed Check of the Matrix Equation | `B=\begin{pmatrix}` | `robotikde`, `wenhardtde` | Author-chosen numerical example using cited premises |
| 50 | A Constructed Check of the Matrix Equation | `A=\begin{pmatrix}` | `robotikde`, `wenhardtde` | Author-chosen numerical example using cited premises |
| 51 | A Constructed Check of the Matrix Equation | `AX=XB=` | `robotikde`, `wenhardtde` | Author-chosen numerical example using cited premises |
| 52 | A Common Problem, Different Representations | `A_\ell X\approx XB_\ell,\qquad \ell=1,\ldots,m.` | `wenhardtde`, `opencvsource` | Relation or notation adapted from the cited background |
| 53 | Tsai--Lenz: A Three-Parameter Rotation System | `q_A=(a_0,a),\qquad q_B=(b_0,b),\qquad q_X=(x_0,x),` | `tsai` | Method equation or algebra adapted to the stated convention |
| 54 | Tsai--Lenz: A Three-Parameter Rotation System | `q_A\otimes q_X=q_X\otimes q_B.` | `tsai` | Method equation or algebra adapted to the stated convention |
| 55 | Tsai--Lenz: A Three-Parameter Rotation System | `a_0x+x_0a+a\times x` | `tsai` | Method equation or algebra adapted to the stated convention |
| 56 | Tsai--Lenz: A Three-Parameter Rotation System | `(a+b)\times x=x_0(b-a).` | `tsai` | Method equation or algebra adapted to the stated convention |
| 57 | Tsai--Lenz: A Three-Parameter Rotation System | `eq:tsai-linear` | `tsai` | Method equation or algebra adapted to the stated convention |
| 58 | Tsai--Lenz: A Three-Parameter Rotation System | `[P_A+P_B]_\times u=P_B-P_A.` | `tsai` | Method equation or algebra adapted to the stated convention |
| 59 | Tsai--Lenz: A Three-Parameter Rotation System | `x_0^2+x^\top x=x_0^2(1+u^\top u)=1.` | `tsai` | Method equation or algebra adapted to the stated convention |
| 60 | Tsai--Lenz: A Three-Parameter Rotation System | `eq:tsai-recover` | `tsai` | Method equation or algebra adapted to the stated convention |
| 61 | Park--Martin: Aligning Rotation Vectors | `R=\exp([r]_\times)` | `robotikde`, `bokhonovua` | Method equation or algebra adapted to the stated convention |
| 62 | Park--Martin: Aligning Rotation Vectors | `r=\frac{\theta}{2\sin\theta}` | `robotikde`, `bokhonovua` | Method equation or algebra adapted to the stated convention |
| 63 | Park--Martin: Aligning Rotation Vectors | `\log R_A=R_X(\log R_B)R_X^\top.` | `park` | Method equation or algebra adapted to the stated convention |
| 64 | Park--Martin: Aligning Rotation Vectors | `eq:park-alignment` | `park` | Method equation or algebra adapted to the stated convention |
| 65 | Park--Martin: Aligning Rotation Vectors | `\sum_{\ell=1}^{m}\\|a_\ell-Rb_\ell\\|^2,` | `park` | Method equation or algebra adapted to the stated convention |
| 66 | Park--Martin: Aligning Rotation Vectors | `\sum_\ell\bigl(\\|a_\ell\\|^2+\\|b_\ell\\|^2\bigr)` | `park` | Method equation or algebra adapted to the stated convention |
| 67 | Park--Martin: Aligning Rotation Vectors | `eq:proper-rotation` | `wernerde`, `bokhonovua` | SVD projection derived in this thesis from cited properties |
| 68 | Park--Martin: Aligning Rotation Vectors | `\sum_i\sigma_iH_{ii}` | `wernerde`, `bokhonovua` | SVD projection derived in this thesis from cited properties |
| 69 | Park--Martin: Aligning Rotation Vectors | `R_X=(M^\top M)^{-1/2}M^\top` | `opencvsource` | Method equation or algebra adapted to the stated convention |
| 70 | Horaud--Dornaika: A Unit-Quaternion Eigenproblem | `eq:quaternion-matrices` | `bokhonovua`, `horaud` | Method equation or algebra adapted to the stated convention |
| 71 | Horaud--Dornaika: A Unit-Quaternion Eigenproblem | `\bigl(L(q_{A_\ell})-\mathcal R(q_{B_\ell})\bigr)q_X=0.` | `bokhonovua`, `horaud` | Method equation or algebra adapted to the stated convention |
| 72 | Horaud--Dornaika: A Unit-Quaternion Eigenproblem | `eq:horaud` | `horaud` | Method equation or algebra adapted to the stated convention |
| 73 | Horaud--Dornaika: A Unit-Quaternion Eigenproblem | `q^\top M_q q=\sum_j\lambda_jc_j^2.` | `bokhonovua`, `wernerde` | Method equation or algebra adapted to the stated convention |
| 74 | Andreff--Horaud--Espiau: A Joint Linear System | `r=\operatorname{rvec}(R_X)=` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 75 | Andreff--Horaud--Espiau: A Joint Linear System | `\begin{pmatrix}u_{11}&u_{12}\\u_{21}&u_{22}\end{pmatrix}` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 76 | Andreff--Horaud--Espiau: A Joint Linear System | `\operatorname{rvec}(URV^\top)` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 77 | Andreff--Horaud--Espiau: A Joint Linear System | `(I_9-R_A\otimes R_B)r=0.` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 78 | Andreff--Horaud--Espiau: A Joint Linear System | `R_Xt_B+(I_3-R_A)t_X=t_A.` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 79 | Andreff--Horaud--Espiau: A Joint Linear System | `eq:andreff` | `andreff`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 80 | Andreff--Horaud--Espiau: A Joint Linear System | `\widehat R_X=` | `wernerde`, `bokhonovua` | SVD projection derived in this thesis from cited properties |
| 81 | Daniilidis: A Dual Quaternion for the Full Pose | `(a+\varepsilon a')(b+\varepsilon b')` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 82 | Daniilidis: A Dual Quaternion for the Full Pose | `eq:dualquat` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 83 | Daniilidis: A Dual Quaternion for the Full Pose | `eq:dual-constraints` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 84 | Daniilidis: A Dual Quaternion for the Full Pose | `eq:dual-translation` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 85 | Daniilidis: A Dual Quaternion for the Full Pose | `Q_A\otimes Q_X=Q_X\otimes Q_B.` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 86 | Daniilidis: A Dual Quaternion for the Full Pose | `q_A\otimes q_X&=q_X\otimes q_B,\\` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 87 | Daniilidis: A Dual Quaternion for the Full Pose | `\begin{pmatrix}` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 88 | Daniilidis: A Dual Quaternion for the Full Pose | `eq:daniilidis-system` | `daniilidis`, `opencvsource` | Method equation or algebra adapted to the stated convention |
| 89 | Daniilidis: A Dual Quaternion for the Full Pose | `h_1=\begin{pmatrix}u_1\\v_1\end{pmatrix},` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 90 | Daniilidis: A Dual Quaternion for the Full Pose | `q_X=\lambda_1u_1+\lambda_2u_2,\qquad` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 91 | Daniilidis: A Dual Quaternion for the Full Pose | `\alpha\lambda_1^2+\beta\lambda_1\lambda_2` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 92 | Daniilidis: A Dual Quaternion for the Full Pose | `\alpha=u_1^\top v_1,\quad` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 93 | Daniilidis: A Dual Quaternion for the Full Pose | `eq:dual-quadratic` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 94 | Daniilidis: A Dual Quaternion for the Full Pose | `\lambda_2=\frac{1}{\\|su_1+u_2\\|},\qquad` | `daniilidis` | Method equation or algebra adapted to the stated convention |
| 95 | Synthetic Experiments with a Known Transformation | `C_k=X_\star^{-1}G_k^{-1}Y_\star.` | `robotikde`, `halconde` | Author construction using the cited geometric rules |
| 96 | Synthetic Experiments with a Known Transformation | `\widetilde R=\exp([\delta r]_\times)R.` | `robotikde` | Author construction using the cited geometric rules |
| 97 | Rotation and Translation Error Against a Reference | `eq:rotation-error` | `robotikde` | Evaluation relation defined or rearranged here from cited geometry |
| 98 | Rotation and Translation Error Against a Reference | `eq:translation-error` | `buldyhinua`, `robotikde` | Evaluation relation defined or rearranged here from cited geometry |
| 99 | Held-Out Pose Consistency | `\widehat Y_k=G_k\widehat X C_k.` | `halconde`, `robotikde` | Evaluation relation defined or rearranged here from cited geometry |
| 100 | Held-Out Pose Consistency | `\widehat Z_k=G_k^{-1}\widehat X C_k.` | `halconde`, `robotikde` | Evaluation relation defined or rearranged here from cited geometry |
| 101 | Relative-Motion Residuals and Image Validation | `r_{t,\ell}` | `wenhardtde` | Evaluation relation defined or rearranged here from cited geometry |
| 102 | Recovering Translation: A Small Linear Example | `R_z-I_3=` | `wenhardtde`, `wernerde` | Author-chosen numerical example using cited premises |
| 103 | Recovering Translation: A Small Linear Example | `(R_z-I_3)t_X=(-30,-10,0)^\top\ \mathrm{mm}.` | `wenhardtde`, `wernerde` | Author-chosen numerical example using cited premises |
| 104 | Recovering Translation: A Small Linear Example | `R_x-I_3=` | `wenhardtde`, `wernerde` | Author-chosen numerical example using cited premises |
