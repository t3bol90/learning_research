# Problems in the exploratory-experiment phase and how to avoid them

<!-- zh: 可能遇到的问题： -->
Problems you may run into:

<!-- zh: 1. 实现某个idea的时候，没有蒸馏相关方向已有开源代码的知识，全靠自己从零实现踩坑。这样导致花费了很多时间踩坑，让人心累。而且需要尝试很多小tricks来让一个pipeline work，没有去复用已有工作代码里使用的小tricks。 -->
1. When you implement an idea, you don't pull in what existing open-source code in the same area already knows. You build everything from scratch and hit every pitfall yourself. That eats a lot of time and wears you out. You also end up trying lots of small tricks to get the pipeline working, instead of reusing the small tricks already baked into existing code.

	<!-- zh: 如何避免：在实现一个idea的时候，最好寻找相关论文的开源代码，先仔细学习一下代码里的tricks。可以直接在这个代码上实现自己的idea，或者把这个代码移植到自己熟悉的框架下，在移植的过程中顺便学习了代码里的tricks。 -->
	How to avoid this: when you implement an idea, look for the open-source code that goes with related papers and study the tricks in that code first. You can either build your idea on top of that code directly, or port the code to a framework you know well and pick up the tricks along the way during the port.
