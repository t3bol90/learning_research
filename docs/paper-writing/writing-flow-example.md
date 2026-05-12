# Examples of writing flow

## Introduction

### Paragraph-level writing flow

1. The problem to solve: scene reconstruction -> COLMAP works very well, with a specific approach -> COLMAP does not work well on texture-less regions such as floors and walls, with a specific reason.
2. Traditional methods: use planes to help scene reconstruction -> the pipeline is complex and there are many parameters to tune -> when the plane fitting is poor, the reconstruction quality is poor too.
3. Recent methods: NeRF, VolSDF and NeuS work very well on object reconstruction -> experiments show that they do not work well on indoor texture-less regions -> large texture-less regions admit many geometries that explain the observations equally well.
4. Our method: use semantics to help reconstruction, and at the same time refine the semantic information during reconstruction -> Specifically, detect floors and walls, and make them satisfy semantic properties -> assume a Manhattan-world structure, so that the surface-point normals on floors and walls follow the matching properties; the wall normal is itself optimised -> to handle the fact that segmentation may be inaccurate, we define a semantic MLP -> use multi-view consistency to improve the accuracy of semantic segmentation, and at the same time use the geometric loss to refine the segmentation probability.
5. Experiments

### Sentence-level writing flow

**The problem to solve**

1. Reconstructing 3D scenes from multi-view images is a cornerstone of many applications such as augmented reality, robotics, and autonomous driving.
2. Given input images, traditional methods generally estimate the depth map for each image based on the multi-view stereo and then fuse estimated depth maps into 3D geometries.
3. Although these methods achieve impressive reconstruction results, they have difficulty in handling low-textured regions such as floors and walls of indoor scenes due to unreliable matching in these regions.

**Traditional methods use a planar prior to improve the result**

1. To overcome this problem, some methods utilize the planar prior to help reconstruction.
2. They [how they use the planar prior]
3. How the plane is modelled: triangulation \\cite\{planar prior\}, superpixel \\cite\{tapa\}, or learning-based plane segmentation methods \\cite\{\}.
4. Although these methods improve the performance, when depth estimation or plane segmentation is inaccurate, they tend to perform poorly.

**Recent methods**

1. Recently, \\cite\{SRN, NeRF, IDR\} represent 3D scenes as implicit neural representations and learn the representations from images with differentiable renderers.
2. IDR \\cite\{\} uses a signed distance field to represent the scene and renders it into images based on the differentiable surface rendering. -> Although it produces high-quality reconstruction results, it tends to fail in complex scenes, as illustrated in \\cite\{volsdf, neus\}. -> A reason is that the surface rendering only enables the gradient back-propagation on the surface point, which is prone to local optima.
3. To solve this problem, \\cite\{unsurf, volsdf, neus\} propose to render implicit surfaces with volume rendering techniques, which produce gradient signals on multiple points along camera rays. -> This enables them to handle complex scenes without the additional mask supervision.
4. However, they still have poor performance in low-textured planar regions, as demonstrated by our experiments in Section\~\\ref\{\}.
5. This is because that there are many possible 3D representations that produce the same observed images, especially in low-textured planar regions.

**Our method**

1. In this paper, we propose a novel implicit neural representation that encodes geometric and semantic information for 3D reconstruction of indoor scenes.
2. Our innovation is utilizing semantic properties of planar regions to resolve ambiguities in the reconstruction, while optimizing the estimated plane segmentation based on the geometric properties.
3. Specifically, we use an MLP network to predict the signed distance and color for any point in 3D space. Given the segmentation of floor and wall regions, we enforce the signed distance field to respect corresponding geometric structures in these regions based on the Manhattan-world assumption.
4. Considering that inaccurate segmentation results may mislead the optimization, we additionally use a network to predict a semantic label for each 3D point and jointly optimize it based on the geometric loss.

## Related work

**Depth map reconstruction.**

1. Given a set of images with calibrated camera poses, \\cite\{point clouds, volumetric, MVS\} aim to recover the underlying 3D shape of the captured scene. This is a long standing problem in computer vision.
2. Many methods adopt a two-stage pipeline: they first estimate the depth map for each image based on multi-view stereo \\cite\{\} and then perform depth fusion \\cite\{\} to obtain the final reconstruction results. -> Traditional multi-view stereo methods \\cite\{\} are able to reconstruct very accurate 3D shapes and have been used in many downstream applications \\cite\{view synthesis, human reconstruction\}. -> However, they tend to give poor performances on texture-less regions. -> A reason is that texture-less regions make dense feature matching intractable.
3. To overcome this problem, some works improve the reconstruction pipeline with deep learning techniques. -> \\cite\{gift, loftr\} improve feature matching. -> MVSNet builds a cost volume to predict the depth map.
4. Another line of works \\cite\{\} utilize scene priors to help the reconstruction. -> Use planes to help COLMAP-style scene reconstruction. -> Some works cited in Haoyu's earlier paper.

**Volumetric reconstruction**

1. These methods \\cite\{\} directly predict the properties of points in the 3D space.
2. How Atlas does it.
3. How NeuralRecon does it -> achieves real-time reconstruction.
4. They represent 3D scenes with discretized voxels, resulting in the high memory consumption.
5. Recently, some methods \\cite\{occupancy network, deepsdf, SRN, nerf, IDR, volsdf, neus\} represent scenes with neural implicit representations.
6. How IDR does it.
7. How NeuS does it.
8. They mostly present reconstruction results of scenes with rich textures.

**Semantic segmentation**

1. Deep learning based methods achieve impressive progress on semantic segmentation.
2. 2D semantic segmentation: CNN-based methods \\cite\{deeplab, pspnet, ade20k, other works\} how they do it -> some methods \\cite\{\} how they use transformers to improve the performance.
3. 3D semantic segmentation: \\cite\{pointnet, pointnet++, other works\} develop networks to process different representations of 3D data. -> \\cite\{semantic nerf\} how it does it.
4. Some methods \\cite\{\} use the relation between 2D and 3D to improve the performance of 2D and 3D segmentation.

## Method

### Sub-section-level writing flow

1. Problem statement.
2. Overview of our method.
3. Volume rendering of signed distance fields.
4. Semantics-guided scene reconstruction.
5. Joint optimization of semantics and geometry.

### Sentence-level writing flow

**Problem statement and overview**

1. Given multi-view images with camera poses of an indoor scene, our goal is to reconstruct the high-quality scene geometry.
2. The overview of our approach is illustrated in Figure 1.
3. We represent the scene geometry and appearance with signed distance and color fields, which are learned from images with volume rendering techniques (Section 3.1).
4. To improve the reconstruction quality in floors and walls, we perform semantic segmentation to detect these regions and apply the geometric constraints based on the Manhattan-world assumption (Section 3.2).
5. To overcome the inaccuracy of semantic segmentation, we additionally encode the semantic information into the implicit scene representation and jointly optimize the semantics with the geometry and appearance of the scene (Section 3.3).

**Volume rendering of signed distance fields**

1. In contrast to multi-view stereo based methods, we model the scene as an implicit neural representation and learn it from images with a differentiable renderer.
2. Inspired by \\cite\{idr, volsdf, neus\}, we represent the scene geometry and appearance with signed distance and color fields.
3. Describe the geometry network:
	a. Given a 3D point x, the geometry model maps it to a signed distance, which is defined as: z(x), s(x) = F_s(x),
	b. where F_s is implemented as an MLP network, and z(x) is the geometry feature.
4. Describe the color network:
	a. To approximate the radiance function, the appearance model takes the spatial point x, the viewing direction d, the normal n(x), and the geometry feature z(x) as inputs, which is defined as: c(x) = F_c(x, d, n(x), z(x)),
	b. where we obtain the normal n(x) by computing the gradient of the signed distance s(x) at point x.
5. Describe how we train the scene representation with volume rendering:
	a. Following \\cite\{volsdf, neus\}, we adopt the volume rendering scheme to learn the scene representation from images. ->
	b. For an image pixel, we sample N points along its camera ray. ->
	c. Predict the signed distance and colors for each point. ->
	d. Then, use Equation 1 to convert the signed distance into a density. ->
	e. Then use the volume rendering equation to obtain the colour. ->
	f. Describe the image loss.
6. Describe using the depth map from COLMAP as a loss:
	a. We find that using only the image loss gives a poor reconstruction, as shown in Figure 1 (a). -> A reason is that the color network is view-dependent, so the network can still explain the images well even when the geometry is inaccurate.
	b. In contrast, although multi-view stereo methods mostly only produce incomplete reconstructions, the geometry they recover is very accurate.
	c. We use the depth maps from multi-view stereo method \\cite\{\} to guide the learning of the scene representation: [equation]
	d. where \\hat\{D\}() is the depth obtained from volume rendering, and D() is the depth map from the multi-view stereo method.
	e. This improves the reconstruction, but because the depth maps themselves are incomplete in texture-less planar regions, the reconstruction performance in these regions is still limited, as shown in Figure 1(b).

**Semantics-guided scene reconstruction**

1. We observe that most texture-less planar regions lie on floors and walls.
2. As pointed by the Manhattan-world assumption \\cite\{\}, floors and walls of indoor scenes generally aligned with three dominant directions.
3. In this assumption, the floor are horizontal, while walls are vertical to the floor and are vertical to each other.
4. Motivated by this, we propose to apply the geometric constraints to the regions of floors and walls.
5. Specifically, we first use a 2D semantic segmentation network \\cite\{\} to obtain the regions of floors and walls.
6. Then, we apply loss functions to enforce the scene representation to satisfy that the surface points on a planar region share the same normal direction.
7. To supervise the walls, a learnable normal $n_w$ is predefined.
8. Following the Manhattan-world assumption, we design a loss that make the normals of surface points on walls are aligned or vertical with the learnable normal $n_w$, which is defined as:
9. where $n'_w$ is the normal of surface points calculated as the gradient of the signed distance s(x) at point x.
10. The learnable normal $n_w$ is randomly initialized and is jointly optimized with the network parameters. We found that it can stably converge to the ground-truth normal in our experiments.
11. For the supervision of floor region, we assume that it is aligned with the z-axis, which are correct in most scenes. The normal loss for the floor is defined as:
12. where $n_f$ is \<0, 0, 1\>, and $n'_f$ is the normal of surface points on the floor.
13. Moreover, we add an additional geometric constraint to the floor region, which enforces its surface points have the same height. This geometric constraint is defined as:
14. where $p_z$ is the z-component of surface point $p$, and $h$ is a learnable scalar that denotes the height of floor.
15. We initialize $h$ by clustering the point clouds in the floor region from multi-view stereo methods.
16. The height $h$ is also jointly optimized with our model parameters. The loss function for the floor is defined as:
17. where $\\lambda_h$ is a coefficient weight.

**Joint optimization of semantics and geometry**

1. Applying the geometric constraints to the floor and wall regions improve the reconstruction quality.
2. However, the 2D semantic segmentation results predicted by the network could be wrong in some image regions, which leads to the inaccurate reconstruction, as shown in Figure 1(c).
3. To solve this problem, we propose to optimize the input semantic information together with the scene geometry and appearance.
4. Inspired by \\cite\{semantic nerf\}, we augment the neural scene representation by additionally predicting semantic logits for any point in 3D space.
5. Describe what the logits represent:
	a. Denote the semantic logits as $s(x) \\in R^3$. By applying the softmax to the logits, we can obtain the probability of point $x$ being floor, wall, and background.
	b. The semantic logits is defined as:
	c. where F_s(x) is an MLP network.
6. Describe how to render the logits:
	a. Similar to the image rendering, we render the semantic logits into 2D image space with volume rendering techniques.
	b. For an image pixel, its semantic logits \\hat\{S\}(x) is obtained by
	c. We forward the logits \\hat\{S\}(x) into a softmax normalization layer to predict the multi-class probabilities $\\hat\{\\mathbf\{p\}\}(r)$.
7. Describe how it is jointly optimised with the normal, and describe the motivation:
	a. Then, we integrate the multi-class probabilities into the geometric losses proposed in Section\~\\ref\{section:semantic\} to jointly optimize the semantic and geometry.
	b. The loss function is defined as: L_{joint} = \\hat\{p\}_f L_f + \\hat\{p\}_w L_w,
	c. where \\hat\{p\}_f is the probability of floor, and \\hat\{p\}_w is the probability of wall.
	d. This loss function optimizes the scene representation in the following way. Take the floor region as an example. If the input 2D segmentation is correct, $L_f$ should decrease easily. But if the input segmentation is wrong, $L_f$ could vibrate during training. To decrease $\\hat\{p\}_f L_f$, the optimizer will push $\\hat\{p\}_f$ small, which thus alleviates the wrong supervision signal caused by the wrong 2D segmentation.
8. Describe how to learn the logits with a rendering loss:
	a. For the stable optimization, we also supervise the semantics with input semantic segmentation, which is defined as:
	b. where $p_k(r)$ is the input probability, and K is the number of semantic categories.
	c. For a 3D region, it is classified into the correct category by the 2D segmentation network in most camera views.
	d. By learning semantics in 3D space, we naturally utilize the multi-view consistency to optimize the input semantic information.
