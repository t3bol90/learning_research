# A specific process for coming up with ideas (goal-driven research)

1. Plan the general goal of your research direction, and lay out a roadmap to reach that general goal.

   <details>
   <summary>What this looks like in practice</summary>

   In general, the general goal is easy to define, but laying out the roadmap takes a deep understanding of the field.

   You can build that understanding by constructing a literature tree (doing a literature review and building a novelty tree and a challenge-insight tree).

   [How to build a literature tree](./literature-tree.md)

   </details>

2. **Picking the topic.** From the roadmap laid out by the novelty tree, pick a task that still has research room, and check whether the task has an important technical challenge. **Picking the topic is the single biggest decision in a research project, more so than the method that comes later.**

   > How to find an important research problem:
   >
   > Think about the long-term goal of the task: what does the final form look like?
   >
   > Ask why the current work only runs on these datasets and not on others. You should try data covering more general cases.
   >
   > **Aim to find new failure cases, and improve the existing technique by attacking those new failure cases.** (1) New task settings or new data make new failure cases easier to surface. (2) Trying methods on new data and showing the group new experimental conclusions is a big contribution.

   <details>
   <summary>How experienced researchers think about "finding important research problems"</summary>

   ![Researcher's notes on finding important research problems](./assets/idea-generation-process/001.png)

   </details>

3. **Picking the topic.** Think about whether the current failure case has a well-established solution. If it does, don't try to solve this failure case, switch to a different problem. If it doesn't, then the technical method that solves the failure case is bound to be novel.

   > How to judge whether the current failure case has a well-established solution:
   >
   > 1. Case one: a task with the same input and output already has a solid solution, and only some details aren't done well enough.
   > 2. Case two: a task whose input or output has changed already has a solid solution. Or several tasks across very different data domains, but with the same underlying technical problem, all have solid, similar solutions.
   > 3. Case three: only a small number (say, one or two) of completely different data domains with the same underlying technical problem have a decent solution.
   > 4. Case four: across various tasks in different fields, the technical problem is similar but none has a good solution.
   >
   > If you hit the first two cases, you must switch to a different failure case. Otherwise the project becomes boring and a struggle, wastes everyone's time, and burns out the team's research enthusiasm.
   >
   > Case three suits beginners. Case four suits more experienced researchers.

4. **Solving the problem.** How to build the ability to design solutions: [Improving your ability to design solutions](./designing-solutions.md)

   <details>
   <summary>How to build the ability to design solutions</summary>

   How to come up with novel and effective techniques: first, know what techniques exist and what problems they solve. Then combine some of them.

   My approach is: (1) build a challenge-insight tree. (2) Pick some of the techniques from the challenge-insight tree and combine them creatively to solve the technical challenge of the current task. (3) **List all the possible pipelines, then compare their pros and cons and pick one pipeline.**

   > One experienced researcher takes the view: **the essence of technique is combining methods. Combine small techniques into bigger ones, and combine old techniques into new ones.**
   >
   > Combining existing techniques and uncovering their properties on new tasks and new data is a substantial contribution.
   >
   > The combination cannot be the trivial input -> A -> intermediate output -> B -> output style of pure A + B (a stitched-together combination). **The combination needs to be a creative one.**
   >
   > **Normally, simply chaining two methods together also fails to solve the problem. Otherwise, the problem has no real technical challenge.**

   <details>
   <summary>Most new techniques follow this pattern (can you find a counter-example?)</summary>

   1. NeRF combined occupancy networks and differentiable rendering for the task of reconstruction from images.
   2. EG3D combined StyleGAN, GRAF, and convolutional occupancy networks for 3D GAN.
   3. DreamFusion combined SDS loss and NeRF for text-to-3D.
   4. MVP combined neural volumes and local radiance fields for image-based human reconstruction.

   </details>

   </details>

5. Validate the technical contribution on some data, and tune the results.

> You can't expect that, just because the paper's story sounds nice and the application is interesting, the reviewers will give your technical contribution a free pass.
>
> See this document for details: [https://www.notion.so/pengsida/434a6b3e34d0403ca178fb0db2338232 (Notion)](https://www.notion.so/pengsida/434a6b3e34d0403ca178fb0db2338232) (Notion)

<details>
<summary>An experienced researcher's discussion of goal-driven research (this person does not recommend idea-driven research)</summary>

See [Problem-driven research, Edinburgh PhD handbook](https://agents.inf.ed.ac.uk/phd-handbook/?show=problem-research).

<details>
<summary>My personal take on idea-driven research</summary>

Trying to propose a better technique on top of an existing one makes it hard to set a clear target (what counts as "better"?), and it's easy to get sucked into chasing numbers within the current task setting.

You should look at it from the angle of the general goal: which milestone tasks can the current technique still not solve? Don't get fixated on the technique's shortcomings on the current task setting. Once you're stuck chasing numbers, your view narrows.

**Don't improve a technique on its existing setting, data, or failure cases. The room for improvement there is usually small.** Find new failure cases and start from those.

</details>

</details>

[Idea-driven vs goal-driven research](./idea-vs-goal-driven-research.md)

<details>
<summary>How goal-driven research helps with research output</summary>

The style of goal-driven research is to chase important tasks and try every method to make the task work. By relaxing some conditions, you can almost always get an important task to produce some working result. This way the project is much more likely to have output.

Some people like chasing new techniques and pushing them to "work" no matter what. But our area is an experimental science, and you can't tell whether a technique really works without lots of experiments. That style of research is too risky.

</details>

<details>
<summary>A special case for coming up with ideas (**important!! this case often produces influential papers**)</summary>

When a new "hammer" appears, it's well worth picking up the new hammer to tackle one of the milestone tasks on your roadmap. This often produces influential work.

> Note, this is not about improving the new hammer on its own task setting (for example, tuning view-synthesis results on the dataset NeRF used). It's about using the new hammer to solve the milestone tasks you're working on (still goal-driven research).

<details>
<summary>There are many examples of this</summary>

1. When the Transformer came out, people used it for LoFTR.
2. When NeRF came out, people used it for Neural Body.
3. When Stable Diffusion came out, people used it for DreamFusion and DreamBooth.

What's the next new hammer? What's the next example?

</details>

</details>

<details>
<summary>Things to watch out for when coming up with ideas (what kinds of project are not worth doing)</summary>

> **You propose an idea and write a paper to make a real contribution to the field, not for the paper itself.**
>
> If a paper makes no contribution to the field, then doing the paper is wasting your own time, because the paper won't earn you the field's respect, and may even draw negative comments.
>
> Upsides of doing such a paper: (1) you get familiar with the submission process. (2) There is some chance of getting a paper out (but the probability is low).
>
> Downsides of doing such a paper: (1) you waste time. The time spent on this project could be used on something more meaningful. (2) You may be judged poorly.

</details>
