# How to revise paper writing

> Why this document exists: iterative revision is the key to writing a good paper. <!-- zh: 为什么要写这篇文档：迭代改进论文是写好一篇论文的关键。 -->

### Improving the writing logic

For an abstract, an introduction, a method section, or any single paragraph, the steps for improving its writing logic are as follows:

1. **Encode:** convert the raw text into a high-level outline of the writing logic.
2. **Analyse the logic:** answer the following two questions to find weak spots in the logic:
    1. Does the outline express the content you actually want to convey?
    2. Does the logic flow smoothly from one point to the next?
3. **Improve the logic:** fix the weak spots in the outline.
4. **Decode:** turn the revised high-level outline back into raw text.

<details>
<summary>A concrete writing example (useful, recommended reading)</summary>

1. The paragraph to be revised
    ```plain text
    Raw text:
    Inspired by \tocite{Hier gs, LoG, OctreeGS}, we model scene representation as $\mathcal{G}(v,t,\mu,R,S,o,SH)$ based gaussians primitives. Our method organizes gaussian primitives into a tree-based hierarchy with $L$ levels, higher level leading to coarser visual quality but better efficiency, vice versa. Gaussian primitives in higher level nodes are merged from lower level nodes in a designed way. To be specific, we interpolate all the attributes of level $l$ gaussian primitives, i.e. mean $\mu^{(l)}$, rotation $R^{(l)}$, scale $S^{(l)}$, opacity $o^{(l)}$ and $SH$ coefficients, to get attributes of level $l+1$ gaussian primitives. We adaptively select nodes to render according to camera view and manually set nodes' velocity by tracking information.
    ```
2. Encode the raw text into a high-level outline
    ```plain text
    High-level writing outline:
    1. We use gaussian primitives as the scene representation.
    2. We organise the gaussian primitives into a tree-based hierarchy. Higher levels have coarser visual quality but better efficiency.
    3. Gaussian primitives at higher levels are merged from lower-level ones.
    4. Specifically, we interpolate the level-$l$ gaussian primitives to obtain the level-$(l+1)$ ones.
    5. We progressively select nodes based on the camera view.
    ```
3. Analyse the outline by answering the two questions:
    1. Does the outline express what you want to convey?
        > 
        What we want to convey: <!-- zh: 我们想表达哪些内容： -->
        - The concrete design of this hierarchy tree.
        - The motivation behind designing this hierarchy tree.
        
        > 
        Whether the current outline conveys these two points: <!-- zh: 现在的写作思路能否体现以上两点内容： -->
        - On the "concrete design of the hierarchy tree", the current outline is too coarse and does not explain how it is designed.
        - On the "motivation for the hierarchy tree", the current outline says nothing.
        
    2. Does the logic flow smoothly?
        You can use GPT to help with the judgment. GPT can spot places where the logic does not flow:
        ![](./assets/revising-paper-writing/001.png)
4. Improve the outline and produce a better high-level version.
5. Decode the improved outline back into English text.

</details>

### Improving sentence flow

Definition of sentence flow: the logic between two consecutive sentences is connected, with no abrupt jump.

How to improve sentence flow:

1. For each pair of adjacent sentences, answer the following questions to find places where the flow breaks down:
    1. Does the second sentence continue talking about something from the first sentence?
    2. If the second sentence does not continue from the first, is there a transition between them?
    3. Does the second sentence introduce a new term, and if so, does that term appear out of the blue?
2. Based on the issues you find, rewrite the two sentences so they fit the sentence-flow criteria. GPT can help.

<details>
<summary>A concrete writing example (useful, recommended reading)</summary>

1. Two sentences:
    ```plain text
    Raw text:
    To be specific, we interpolate all the attributes of level $l$ gaussian primitives, i.e. mean $\mu^{(l)}$, rotation $R^{(l)}$, scale $S^{(l)}$, opacity $o^{(l)}$ and $SH$ coefficients, to get attributes of level $l+1$ gaussian primitives. We adaptively select nodes to render according to camera view and manually set nodes' velocity by tracking information.
    ```
2. Check whether they meet the sentence-flow criteria. GPT can spot the breaks:
    ![](./assets/revising-paper-writing/002.png)
3. Based on the issues, rewrite the two sentences.

</details>
