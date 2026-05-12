# Given an idea, how to design exploratory experiments

<!-- zh: 拥有强大的实验设计能力的好处：<br>1. 降低实验成本。<br>2. 保持清楚的实验思路，提升改进Idea的效率。 -->
> Why strong experiment design matters:
> 1. It lowers the cost of running experiments.
> 2. It keeps your line of thinking clear, so you can iterate on the idea more efficiently.

<!-- zh: 实验设计的经典问题： -->
Classic questions to ask when designing an experiment:

<!-- zh: 1. 现在的实验是否同时包含了几个**exploration points**？怎么修改实验来减少要同时探索的点？ -->
1. Does the current experiment cover several exploration points at once? How can you change the setup to reduce the number of points being explored at the same time?
<!-- zh: 2. 现在的实验是否同时包含了几个**technical challenges**？怎么修改实验来减少其中的technical challenges？ -->
2. Does the current experiment combine several technical challenges at once? How can you change the setup to cut down on those technical challenges?
<!-- zh: 3. 我们目前重点想先搞清楚的exploration point是什么，最想解决的technical challenge是哪个？ -->
3. Which exploration point do you most want to figure out first, and which technical challenge do you most want to solve?

<!-- zh: 实验设计的基本准则：
1. 减少一个实验中包含的exploration points的数量
2. 减少一个实验中要解决的technical challenges的数量 -->
> The basic rules for experiment design:
> 1. Reduce the number of exploration points contained in a single experiment.
> 2. Reduce the number of technical challenges that a single experiment has to address.

<!-- zh: 为了满足实验的基本准则，有两个实际可行的操作： -->
There are two practical moves you can use to follow these rules:

<!-- zh: 1. Decomposition，把复杂的事情拆解成一组简单的事情，从简单到复杂 -->
1. Decomposition: break a complex thing into a set of simple things, then go from simple to complex.
<!-- zh: 1. 拆解复杂的实验：从简单的setting开始探索，慢慢加大难度，然后做实际的setting** → 可以降低exploration points和technical challenges** -->
   1. Break down a complex experiment: start exploring from a simple setting, slowly increase the difficulty, and then move to the actual setting. This cuts down both exploration points and technical challenges.
<!-- zh: 2. 拆解Idea：把Idea分解成各个部分，从可控的Idea开始做起，再加探索性、创新性的框架/模块** → 可以降低exploration points**（注意：可控的Idea是原先自己Idea的简化，而不是某某论文的pipeline） -->
   2. Break down the idea: split the idea into parts, start with the controllable version, then add the more exploratory or novel frameworks and modules. This cuts down exploration points. (Note: the controllable version should be a simplified form of your own idea, not the pipeline from some other paper.)
<!-- zh: 3. 考虑难度的同时，也要考虑exploration point和technical challenge的重要性。优先做更需要探索的exploration point和technical challenge。 -->
   3. Along with difficulty, also weigh how important each exploration point and technical challenge is. Do the ones that need exploration most first.
<!-- zh: 2. 在Toy experiment上探索Idea -->
2. Explore the idea on a toy experiment.
<!-- zh: 1. 简化实验setting，保留想解决的technical challenges** → 可以降低exploration points和technical challenges** -->
   1. Simplify the experiment setting while keeping the technical challenges you want to tackle. This cuts down both exploration points and technical challenges.
<!-- zh: 2. 简化数据，保留想解决的technical challenges** → 可以降低exploration points和technical challenges** -->
   2. Simplify the data while keeping the technical challenges you want to tackle. This cuts down both exploration points and technical challenges.

<!-- zh: 一些的实践例子： -->
A few real-world examples:
<!-- zh: 1. NeRF团队最开始是在2D Image上做的实验。 -->
1. The NeRF team started out running experiments on 2D images.
<!-- zh: 2. Train network先overfitting一个sample -->
2. Train the network to overfit a single sample first.
<!-- zh: 3. 小规模训练数据上训网络 -->
3. Train the network on a small-scale training set.
