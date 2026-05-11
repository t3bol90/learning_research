# Improving your ability to design solutions

> Document index (GitHub repo): [https://github.com/pengsida/learning_research](https://github.com/pengsida/learning_research)

This document covers how to choose a topic: [How to build the ability to come up with ideas](./getting-advanced/coming-up-with-ideas.md).

This document covers how to analyse a problem: [Project core technical problem analysis template](./project-core-technical-problem-analysis.md) (Notion).

**Why I am writing this document:** because I have seen some students who do not have a clear playbook when they try to solve a problem. They do not know which angle to attack a failure case from, their thinking is not divergent enough, and the set of solutions they can come up with is small.

> How to fundamentally lift your ability to solve problems: read more papers; think more; run more experiments; talk to more people; build up your store of existing techniques, insights, and known problems.

> **Why solution-design ability matters from a PhD-training point of view:** a PhD student should work hard to become a very technical person, with **a strong ability to learn, think about, and pull apart existing and emerging techniques, so that they can deeply improve a technique on a given task and lift its performance on that task.** Simply using a technique on a task is something I believe most undergraduates can also do.
>
> I would guess that reviewers always want a paper to have technical contribution probably because they want to see more technical innovation and analysis in the paper, not just a new task, story, or applications. If a paper only tells a story without proposing a new technique, it actually does not help the development of techniques in the field.

> Even though most people in CV and CG are bringing in hammers from ML, "picking up a hammer and using it" and "actually getting the hammer to work" are very different.
>
> **The people who actually get the hammer to work are very strong. The people who just pick up a hammer and use it are mostly only doing brick-laying work.**

1. For the "problem" you have chosen, think about why this pipeline runs into this problem, and infer the many deeper technical reasons. How to infer technical reasons:

   1. First, distil knowledge from existing papers. Look for papers that solve a similar "problem" and check whether they analyse the technical reasons behind the "problem". (When looking for related papers, range widely, from papers in the same direction to papers in different directions. Mainly find papers yourself, and also ask your senior advisor and senior students whether they have seen related papers. **The first two or three paragraphs of a paper's Introduction usually discuss the problems of prior papers and their technical reasons.**)

      Related documents: [How to read papers effectively](./getting-advanced/reading-papers.md) (Notion), [How to find papers](./find-papers.md) (Notion).
   2. Then summarise the knowledge you got from the papers. Combine the analyses of those papers into your own line of thinking.

      Related document: [How to summarise papers](./literature-tree.md) (Notion).
   3. Then distil knowledge from experienced people. Find experienced people to discuss with, share your own thoughts on the problem, and use the act of sharing your view to deepen your own thinking and prompt yourself to think more. You also hope they have a different angle, so you can build up your understanding of the "problem" and accumulate possible technical reasons behind it. (**We should build the habit of finding people to discuss any paper that is inspiring. Just retelling the paper is fine, sharing your thoughts on it is fine.**)
   4. Then get knowledge from experiments. Run experiments to verify these technical reasons and gather more experimental observations.

2. From the many deeper technical reasons, propose a solution.

   > The next steps assume that the problem we are solving has no well-established solution in similar fields.
   >
   > We only solve failure cases in the following two situations:
   > 1. There is a task in a completely different data domain, but the technical core of the problem is the same, and a good solution exists.
   > 2. Across tasks in different fields, there is a similar technical problem, but no good solution exists in any of them.

   For the first situation, "there is a task in a completely different data domain, but the technical core of the problem is the same, and a good solution exists", here is how to propose a solution:

   1. Read the literature widely, looking for cases that match this situation: "there is a task in a completely different data domain, but the technical core of the problem is the same, and a good solution exists".
   2. Port the corresponding solution to your own task.

   For the second situation, "across tasks in different fields, there is a similar technical problem, but no good solution exists in any of them", here is how to propose a solution:

   1. Break down the technical problem into several sub-problems.
   2. For each sub-problem, look for cases that match this situation: "there is a task in a completely different data domain, but the technical core of the problem is the same, and a good solution exists". If there is no such case, keep breaking down the problem.
   3. Once you have a solution for each sub-problem, think about how to combine them into a complete solution.

   > What if the technical problem cannot be broken down and there is no solution to draw on? There are three possibilities:
   > 1. With your current ability, you do not know how to break down this problem.
   > 2. There is a solution you could draw on, but you have not found the related paper.
   > 3. The problem is very likely a world-class hard problem.
