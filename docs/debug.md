# How to debug an algorithm or code

> Document index (GitHub repo): [https://github.com/pengsida/learning_research](https://github.com/pengsida/learning_research)

> **Why this document exists:** I noticed that some students get stuck while running experiments because of code problems. Algorithm questions can be discussed and unblocked by other people, but code problems are very hard for an outsider to help with unless they actually sit down and read your code. This document is here to help students get better at debugging code.
>
> **From now on, when a student asks me a code-debugging question, I will give the debugging idea and also point out which rule from *Debugging: The 9 Indispensable Rules* I'm applying, and which rules they should be using more flexibly during their debugging.**
>
> **The contents of this document also apply to debugging algorithms.**

I strongly recommend reading *Debugging: The 9 Indispensable Rules* carefully. It is to research what the *Nine Swords of Dugu* are to martial arts. **Once you have internalised the ideas in *Debugging: The 9 Indispensable Rules*, your debugging ability and your ability to solve problems in research will both go up a long way.**

The book itself is available from the original Notion page (PDF and EPUB attachments).

<details>
<summary>What online readers say about <em>Debugging: The 9 Indispensable Rules</em></summary>

> If every CS and EE student read this book a bit earlier, far fewer of them would be driven to a breakdown by bugs and end up giving up.
> Saved me from a really tough spot.
> A very good book. Not just for software and hardware problems either, I felt it could help with solving any kind of problem.
> Concise and to the point. Excellent.
> An amazing book. Reading it felt like every joint in my body had been opened up.

</details>

**The Chinese translation of *Debugging: The 9 Indispensable Rules* is, in my view, a bit hard to read.** I've written my own summary of the book below, and you can read that directly. The nine principles in the book come up constantly in programming and in research.

The summary below is informed by this article: [https://brainku.github.io/2016/12/11/debugging-the-9-rules/](https://brainku.github.io/2016/12/11/debugging-the-9-rules/).

![Cover of Debugging: The 9 Indispensable Rules](./assets/debug/001.png)

### Introduction

- If you've spent a lot of time looking for a bug, it's quite possible you've overlooked one of the most basic and most important rules.
- The rules below are ones you need to remember and apply.
- The whole book stays focused on one thing: **finding the root cause of the bug and fixing it.**

### Rule 1: understand the algorithm and the code (the foundation of debugging)

**Rule 1, understand the algorithm and the code: "We need to understand how the algorithm and code work, and the principles behind them. If there's a part of the algorithm or code we don't understand, that's usually exactly where the problem is."**

Notes on Rule 1:

- We need to understand the algorithm and the code well. This is the foundation of debugging them.
- Before you understand the workflow of the algorithm and code (and what each line of the important modules is doing), it's hard to debug the code. Once you understand those details, finding the problem becomes much easier.
- When looking for a bug, we have to check whether each module of the algorithm or code is working. To do that, we need to know exactly what the correct inputs and outputs of those modules look like.

### Rule 2: reproduce the bug and observe the run in detail (common technique 1)

**Rule 2, reproduce the bug and observe the run in detail: "Reproducing the bug has three benefits: you can observe the pattern of the bug; you can know exactly the conditions under which the bug fires, so you can focus on finding the cause; and you can tell whether the bug has been fixed."**

Notes on Rule 2:

- "Reproducing the bug" means: with the same test data as input, you trigger the same bug.
- "Observing the run in detail" means: stepping through the code and watching how the low-level details lead to the bug.
- Make sure the environment, data, model, and so on are the same when you reproduce the bug.
- How to handle intermittent bugs:
  - Look carefully for the conditions that trigger the bug, so you can trigger it on demand.
  - Record and observe the experimental results and the error messages each time the bug occurs. Try to find the root cause from the few occurrences you do have.
- Polish your debugging tools so that, when a bug shows up, you can observe the algorithm or code's results more easily. Think about how to design tools that make it easy to observe how the algorithm or code is running, for example visualisation tools, print tools, and breakpoints. The goal is to check whether a particular module is behaving as expected.

### Rule 3: locate the root cause of the bug from facts

**Rule 3, locate the root cause of the bug from facts: "Seeing with your own eyes how the low-level details cause the bug is very important. If you only guess at how the failure happens, you often end up fixing things that aren't actually the bug. That kind of fix doesn't solve the problem, and may break something else."**

Notes on Rule 3:

- As far as possible, confirm the cause of the bug from experiments rather than just guessing.
- When debugging, you do need to guess at causes, but the point is to narrow the bug's range and decide where to focus the search. Use "guessing" and "experimenting" together flexibly.

### Rule 4: divide and conquer (common technique 2)

**Rule 4, divide and conquer: "Divide and conquer is the core technique of debugging, and it can save you huge amounts of time. The way it works is to repeatedly split the problem into a good half and a bad half so you narrow the search range, then dig further into the bad half."**

Notes on Rule 4:

- During debugging, keep narrowing the bug's range until you close in on it.
- When debugging, first set a range for the bug. Search the first half of that range and check for errors. If there are errors, the search range becomes the first half, and you try again. If there are no errors, the search range becomes the second half, and you try again. Each search halves the range. After a few rounds, you find the target.
- A lot of the time, the code may have several bugs at once, which interferes with divide and conquer. Whenever you uncover a bug, fix it straight away and restart divide and conquer.
- Eliminate bugs caused by other factors. When using divide and conquer to find a bug, think about how to use toy data and a toy setting, so the chance that the bug comes from the data or the setting is reduced, and the chance of several bugs appearing at once is reduced.

### Rule 5: control your variables when debugging (common technique 3)

**Rule 5, control your variables when debugging: "Control variables and only change one place at a time, so you can fully confirm the effect of that change."**

Notes on Rule 5:

- Controlling variables is a standard scientific method. To see the effect of one variable, scientists control all the other variables that could affect the outcome.
- Change one thing at a time in the test data or test parameters, and observe its effect on the algorithm or code.
- Compare a failing example with a working example, compare the debugging logs of the two, and look for differences in how the algorithm or code runs in each case. (**This technique works really well, but it does take a fair bit of observation and comparison skill.**)
- When you compare a failing example with a working example, try to make sure only one variable differs.
- Find the most recent version of the algorithm or code from before the problem appeared, and work out what was changed after that version.

### Rule 6: keep good experimental records (common technique 4)

**Rule 6, keep good experimental records: "When you're investigating a problem, write down what you did, the order in which you did it, and what happened. This helps you watch the debugging information and the run details of the algorithm or code, and helps you find where the bug is."**

Notes on Rule 6:

- Learn to record the important experimental details and phenomena.
- Learn to connect the pieces of information in your experimental records and find patterns.

### Rule 7: stay sceptical of your assumptions

**Rule 7, stay sceptical of your assumptions: "Stay sceptical of your own assumptions, especially when those assumptions are central to a problem you can't otherwise explain."**

Notes on Rule 7:

- Never fully trust your own assumptions. As Sherlock Holmes put it: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth."
- Sometimes you even need to check whether your test data and your debugging tools are correct.

### Rule 8: ask other people for their view (common technique 5)

**Rule 8, ask other people for their view: "Asking others for help has at least three benefits: you get a fresh perspective, expert knowledge, and other people's experience with algorithms, code, and debugging."**

Notes on Rule 8:

- "Other people" here can mean: open-source code, large language models like Kimi or GPT, search engines, online forums, online Q&A sites, senior advisors, lab mates, friends, and the researchers you've met at meetings.
- After you've been debugging and running experiments for a long time, you can get stuck in your own head and lose the bigger picture, building up your own bias about the algorithm or code. Other people, looking at the problem from a different angle, can help you escape a local minimum.
- Sometimes the act of explaining the algorithm or code problem to someone else gives you a fresh understanding of it. The act of organising the problem helps you step out of your usual thinking pattern.
- Asking experts who know the algorithm or code well can help you get up to speed quickly, and gives you good ideas and directions for finding bugs.
- Borrow from other people's debugging experience.
- You'll need to be a bit outgoing about it: actively ask senior advisors, lab mates, and the researchers you've met at meetings, and even send a polite email to experienced researchers.
- "Being afraid to ask for help" causes a lot of difficulty in your programming, debugging, and research.

### Rule 9: fix the bug at its source

**Rule 9, fix the bug at its source: "You need to fix the bug at its source, otherwise the bug will keep coming back. For example, if a piece of hardware fails, don't assume it just broke for no reason. If something else is causing the part to break, replacing the part will only buy you a short period of working time, then the new part will break too. You have to find the actual point of failure."**

Notes on Rule 9:

- If we don't find the root cause of the bug and design our fix around it, but instead just patch around it by changing the data or the setting, or by adding a few tricks to suppress the bug, the bug is still there.
- Carefully check whether your debugging plan actually fixed the bug.

Related: [Are the intermediate outputs of each module what you expect?](./checking-module-outputs.md), [Ten classic questions for analysing experimental results](./ten-classic-experiment-questions.md).
