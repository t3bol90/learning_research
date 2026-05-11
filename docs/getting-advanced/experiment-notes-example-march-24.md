# Experiment Notes Example: 24 March

Goals for this week:

1. Replace the generalisable rendering head
   1. Pre-train a rendering head with the same structure on DTU
   2. Swap it in

   After swapping it in, it did not work well.
   1. Suspect the sample count is the cause
   2. Suspect a bug in the code
2. Try single point
   1. Investigate how many points K-Planes and K-Planes IBR each need before they work
      1. K-Planes:
         1. 4, 8, 48
      2. K-Planes IBR:
         1. 4, 8, 48
   2. Use depth + 1 point.
      Results were poor.

<!-- Table of contents -->

## 1. Edge flickering

1. Adding a mask resolves it, but the outcome also depends on training time.

<table>
<tr>
<td>

[6.3 hours, no mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/42f4fb4e-d13d-4c63-a8cc-0930f0a29a09/step00000000.mp4) (video, Notion)

</td>
<td>

[With mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/97f19d17-7881-44e8-8a0c-e93fbd2eaa89/step00000000.mp4) (video, Notion)

</td>
</tr>
<tr>
<td>

[4.2 hours, no mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/63b38420-3d24-42f2-83db-b8bd8bc3b3b8/step00030000.mp4) (video, Notion)

</td>
<td>

[With mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/6bc223f5-db39-48bd-84d8-7553eed6c2cb/step00030000.mp4) (video, Notion)

</td>
</tr>
<tr>
<td>

[2.1 hours, no mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/74e39da6-2e6c-40be-b21d-4eaa898c9f9c/step00060000.mp4) (video, Notion)

</td>
<td>

[With mask](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/84ab22d8-e6a8-4fcf-ade7-b82bb14fea5d/step00060000.mp4) (video, Notion)

</td>
</tr>
</table>

## 2. Replacing the generalisable rendering head

### 2.1 Pre-train the ENeRF rendering head

1. Modify the ENeRF rendering head so it does not depend on the voxel features.
2. Modify the ENeRF rendering pipeline accordingly.

### 2.2 After swapping the rendering head, quality drops noticeably

![Loss curves after swapping the rendering head](./assets/experiment-notes-example-march-24/001.png)

<table>
<tr>
<td>

![Joint training](./assets/experiment-notes-example-march-24/002.png)

</td>
<td>

![Joint training, view 2](./assets/experiment-notes-example-march-24/003.png)

</td>
<td>

![Joint training, view 3](./assets/experiment-notes-example-march-24/004.png)

</td>
</tr>
<tr>
<td>

![No pre-training](./assets/experiment-notes-example-march-24/005.png)

</td>
<td>

![No pre-training, view 2](./assets/experiment-notes-example-march-24/006.png)

</td>
<td>

![No pre-training, view 3](./assets/experiment-notes-example-march-24/007.png)

</td>
</tr>
<tr>
<td>

![With pre-training](./assets/experiment-notes-example-march-24/008.png)

</td>
<td>

![With pre-training, view 2](./assets/experiment-notes-example-march-24/009.png)

</td>
<td>

![With pre-training, view 3](./assets/experiment-notes-example-march-24/010.png)

</td>
</tr>
</table>

### 2.2 Possible causes

1. Generalisation is not strong enough.
   1. Check how well ENeRF generalises to this scene.
   2. Possible fixes:
      1. Quickly fine-tune one frame.
      2. Use a slightly more involved policy: fine-tune the first n frames, then fine-tune every 10 frames after that.

   ![Fine-tuning schedule comparison](./assets/experiment-notes-example-march-24/011.png)

![Result, view 1](./assets/experiment-notes-example-march-24/012.png)
![Result, view 2](./assets/experiment-notes-example-march-24/013.png)
![Result, view 3](./assets/experiment-notes-example-march-24/014.png)
![Result, view 4](./assets/experiment-notes-example-march-24/015.png)

<table>
<tr>
<td>

![Result, view 5](./assets/experiment-notes-example-march-24/016.png)

</td>
<td>

![Result, view 6](./assets/experiment-notes-example-march-24/017.png)

</td>
</tr>
</table>

### 2.3 After swapping in a one-frame fine-tuned rendering head, the result improves

Current issues:

1. Training time is still long.
   1. Many hyper-parameters left to explore:
      1. Sampling strategy: \[256, 128, 48\]
      2. Half precision
      3. Pixel sampling strategy: use the human mask
      4. Compress the geometry-representation parameters: drop the MLP, use a smaller feature grid
2. The path-rendered output has some ghosting.
   1. Cause analysis:
      1. ~~Rendering head~~
      2. Other directions to investigate:
         1. Why does CNN + IBR head not have this problem?
            1. The IBR training strategy
            2. (other)
         2. Whether fine-tuning specifically on the failing frames helps

![Path rendering ghosting](./assets/experiment-notes-example-march-24/018.png)

<table>
<tr>
<td>

[Depth, step 30000](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/f4d05853-754b-4c5c-af2c-7eb736c29de2/step00030000_depth.mp4) (video, Notion)

</td>
<td>

[1.5 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/b5261581-84a7-4605-92f2-6847e7497023/step00030000.mp4) (video, Notion)

</td>
</tr>
<tr>
<td>

[Depth, step 60000](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/6a7419f2-2cb1-4b16-9202-efaed2d01bd5/step00060000_depth.mp4) (video, Notion)

</td>
<td>

[3 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/f9794f2d-e92a-4fa6-83dd-a516a97cbbd5/step00060000.mp4) (video, Notion)

</td>
</tr>
<tr>
<td>

[Depth, step 90000](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/5008e418-b756-4b15-9d8c-40580b71180e/step00090000_depth.mp4) (video, Notion)

</td>
<td>

[4.5 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/093d2942-4de4-4d87-80d2-3156072e38d8/step00090000.mp4) (video, Notion)

</td>
</tr>
</table>

<table>
<tr>
<td>

[Depth, step 0](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/6d84f366-3616-4e54-b74e-9207044cb6a9/step00000000_depth.mp4) (video, Notion)

</td>
<td>

[RGB, step 0](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/0ea92d03-5eed-4825-8976-8d75501dde2d/step00000000.mp4) (video, Notion)

</td>
</tr>
</table>

**KPlanes**

<table>
<tr>
<td>

[1.35 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/52443ef6-7c29-4618-9389-7fdec2fa8ea8/step00030000.mp4) (video, Notion)

</td>
<td>

[2.7 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/b5e8eb9f-c0d3-4ea4-ac9c-34d14538a7b2/step00060000.mp4) (video, Notion)

</td>
<td>

[4 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/546be128-cb58-411c-9427-f70cecf5c191/step00090000.mp4) (video, Notion)

</td>
</tr>
</table>

KPlanes IBR joint training

<table>
<tr>
<td>

[2.1 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/0673c044-ced3-4d85-b90e-c2847163a1ba/step00030000.mp4) (video, Notion)

</td>
<td>

[4.2 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/664e5518-6ce3-44ba-9d0f-f34d3f94a7a2/step00060000.mp4) (video, Notion)

</td>
<td>

[6.3 hours](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/ca47d4c6-831b-42a9-93e0-62593e40d3aa/step00000000.mp4) (video, Notion)

</td>
</tr>
</table>

<table>
<tr>
<td>

[Run A, step 0](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/f0615c4b-0884-44d4-91d4-34fa098a773d/step00000000.mp4) (video, Notion)

</td>
<td>

[Run B, step 0](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/7e645fa0-8ece-4d73-a445-6f4e0931f6bd/step00000000.mp4) (video, Notion)

</td>
</tr>
</table>

## 3. Depth sampling

1. Did not work. The point count may be too low for the model to converge.

![Depth-sampling result, view 1](./assets/experiment-notes-example-march-24/019.png)

<table>
<tr>
<td>

![48 samples + depth](./assets/experiment-notes-example-march-24/020.png)

</td>
<td>

![48 samples + depth, view 2](./assets/experiment-notes-example-march-24/021.png)

</td>
</tr>
<tr>
<td>

![24 / 48 samples](./assets/experiment-notes-example-march-24/022.png)

</td>
<td>

![24 / 48 samples, view 2](./assets/experiment-notes-example-march-24/023.png)

</td>
</tr>
<tr>
<td>

![8 samples](./assets/experiment-notes-example-march-24/024.png)

</td>
<td>

![8 samples, view 2](./assets/experiment-notes-example-march-24/025.png)

</td>
</tr>
</table>

## 4. The current problem: joint training still has issues

### 4.1 Current observations

1. Joint training shows flickering.
2. Single-frame joint training also shows flickering.
3. The source input looks fine.
4. It is not caused by random source images.

<table>
<tr>
<td>

[Joint training](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/2ed4fcb6-140a-4d60-825d-020321954ba5/step00000000.mp4) (video, Notion)

</td>
<td>

[Single-frame joint training](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/1ee817f8-753c-45e8-a963-a83ed81c9550/step00000000.mp4) (video, Notion)

</td>
</tr>
</table>

[Random multi-image](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/9615ad33-b059-4b38-8922-bba6ef11ff64/step00000000.mp4) (video, Notion)

### 4.2 Experimental observations

### 4.3 Causes and analysis
