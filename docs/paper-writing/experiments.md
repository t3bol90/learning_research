# Writing the Experiments section

> To write a good Experiments section, you need to answer three questions:
> 1. How do we show our method is stronger than existing methods? That is, which comparison experiments to run.
> 2. How do we show that the modules in our method are effective? That is, which ablation studies to run.
> 3. How do we fully show the upper bound of our method? That is, on which more challenging data to run a demo.

> For the text part of Experiments, the captions of figures and tables are the most important.
>
> Table captions and figure captions need to spell out the experimental setting and notation. If there is nothing else worth saying, you can describe the experimental result in a single sentence.
> Captions should not discuss experimental results at length, since that easily duplicates the body text.

> A layout tip for experimental figures and tables: a single-column figure or table looks better placed in the right column of the page, because readers' habit is to look for the first line of text in the top-left corner.

<details>
<summary>Which comparison experiments to run</summary>

<details>
<summary>Version 1: there are baseline methods</summary>

You need to compare against related and recent baseline methods.

</details>

<details>
<summary>Version 2: the task is very new and there are no directly related baseline methods</summary>

<details>
<summary>Some examples</summary>

1. Example 1: construct variants of the method.

   ![[https://arxiv.org/pdf/2008.02268.pdf](https://arxiv.org/pdf/2008.02268.pdf)](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/8b8babfb-70a5-4dd6-92e0-5ec85db4058d/Untitled.png)

</details>
</details>
</details>

<details>
<summary>Which ablation studies to run</summary>

A paper contains some core contributions and some design choices in each pipeline module. Readers usually **care a lot about how the core contributions affect performance**, and they are **curious about whether these design choices really help**.

So ablation studies usually need to include two parts:

1. A large table and a matching visual comparison figure, listing the paper's core contributions and some important components and their effect on the method's performance.

   <details>
   <summary>Some examples</summary>

   1. Example 1

      ![[https://arxiv.org/pdf/2003.08934.pdf](https://arxiv.org/pdf/2003.08934.pdf)](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/22237095-a0bf-4920-b9c0-7b48076370c8/Untitled.png)

   2. Example 2

      ![[https://arxiv.org/pdf/2304.06717.pdf](https://arxiv.org/pdf/2304.06717.pdf)](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/6736cb5f-0aff-4e83-bef8-c4d342f0d923/Untitled.png)

   3. Example 3

      ![[https://arxiv.org/pdf/2302.12237.pdf](https://arxiv.org/pdf/2302.12237.pdf)](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/25eb5132-931b-458e-8f9b-2c774f4b6f3d/Untitled.png)

   </details>

2. Some smaller tables and matching visual comparison figures. Each small table separately lists the effect on the method's performance of the design choices in one pipeline module (the method's sensitivity to hyperparameters, the method's sensitivity to input data quality, the effect on performance of dropping a particular design choice).

   <details>
   <summary>Some examples</summary>

   1. Example 1

      ![[https://arxiv.org/pdf/2302.12237.pdf](https://arxiv.org/pdf/2302.12237.pdf)](https://prod-files-secure.s3.us-west-2.amazonaws.com/952f5f87-b692-4249-a557-7f7ad0a77d56/60269689-8f65-4be5-b109-9bf20173e3be/Untitled.png)

   </details>

</details>

<details>
<summary>Which applications and demos to do (<strong>this has a very large effect on the impact of the paper</strong>)</summary>

[How to make appealing demos and applications](../demos-and-applications.md)

</details>
