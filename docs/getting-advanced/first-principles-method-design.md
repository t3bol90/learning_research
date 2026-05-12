# Designing methods from first principles

<!-- zh: 什么是第一性原理：一层层剥开事物的表象，看到里面的本质，解决核心的问题。 -->
What first-principles thinking means: peel back the surface of a thing layer by layer until you can see what it really is, then solve the core problem.

<!-- zh: 如何基于第一性原理设计方法： -->
How to design methods from first principles:

1. Take a SOTA method's failure cases apart piece by piece, and answer clearly what the most fundamental reason is that the method does not work.
2. Solve that fundamental reason with **a new technique**.

> Why use a new technique:<br>Because the older techniques in this research direction have already been well explored, and there is no more room to push them further.<br>**If the research direction still has an important technical problem left, the older techniques almost certainly cannot improve on it.**<br>**If an older technique could solve the fundamental problem you are running into, then the failure case does not need a research solution at all. It is an engineering problem.**

> An example of first-principles thinking:<br>
> Musk has used this story in interviews. While Tesla was developing electric cars, the team ran into a hard problem: battery costs stayed stubbornly high. At the time, the market price for energy-storage batteries was 600 USD per kilowatt-hour, and that price was stable. It was not going to move much in the short term.
> But Musk thought about it from a first-principles angle. What materials does a battery pack actually consist of? What is the market price of those raw materials? If we bought the raw materials and assembled them into a battery ourselves, how much would it cost? The answer was about 80 USD per kilowatt-hour.
> Starting from the most fundamental level, working out what a battery is made of, then adding up the prices of those raw materials, gave him the lowest possible price for a battery. That way of thinking is what made commercial electric cars possible. Most people start from the assumption that the current state of a thing is fixed and cannot be changed. Musk's instinct is to look at the underlying reason behind that current state and ask whether it can be changed.
