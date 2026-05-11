# Ten classic questions for analysing experimental results

> Document index (GitHub repo): [https://github.com/pengsida/learning_research](https://github.com/pengsida/learning_research)

Code debugging:

1. Are the intermediate outputs of each module what you expect?
   [How to debug an algorithm or code](./debug.md)
2. Reasons behind some classic code bugs (NaN, segmentation fault, and so on)
   [Reasons behind some classic code bugs (Notion)](https://www.notion.so/8beb455efdd54cf8bc6de579bca3c211) (Notion)

Failure cases:

1. Is there any pattern in the failure cases? Are there fixed patterns? These patterns can point to the technical cause behind them.
   <details>
   <summary>A short debugging story</summary>

   ![Debugging story, panel 1](./assets/ten-classic-experiment-questions/001.png)
   ![Debugging story, panel 2](./assets/ten-classic-experiment-questions/002.png)
   </details>

   Knowing how to visualise failure cases really matters.
   3D visualisation tools:
   1. [https://github.com/zju3dv/Wis3D](https://github.com/zju3dv/Wis3D)
   2. [https://github.com/koide3/iridescence](https://github.com/koide3/iridescence)
   3. [https://github.com/nerfstudio-project/viser](https://github.com/nerfstudio-project/viser)

Data:

1. The current method does not work well on the test set. How does it perform on the training set? Can it overfit?
2. How does it perform on simple data such as XX?
3. We remember it worked reasonably well on dataset XX. Why does it not work on this one? What are the differences between the two datasets?

Algorithm:

1. We remember algorithm XX did not perform this poorly on this dataset. Why is our method so much worse? Do we need an ablation to see which module is the problem? It might also be a coding bug.
2. If we run a simplified version of our algorithm, does it work? How does it perform?
3. Have you visualised the output of module XX? Check whether it matches expectations and whether anything looks odd.
