# Phase for Character Control

Reference articles:
1. [The path to intelligent motion generation (I): PFNN](https://zhuanlan.zhihu.com/p/485607474)
2. [The path to intelligent motion generation (II): Local Motion Phase](https://zhuanlan.zhihu.com/p/486996982)
3. [The path to intelligent motion generation (III): DeepPhase](https://zhuanlan.zhihu.com/p/562089658)

How this note is organised:
1. What Phase is.
2. How Phase is used for character control.
3. Why Phase was introduced.
4. The problems with Phase.
5. The fix for Phase: Local Motion Phase.
6. How Local Motion Phase is used for character control.
7. The problems with Local Phase.
8. The fix for Local Phase: DeepPhase.
9. How DeepPhase is used for character control.

**What Phase is: a person's movement is treated as a periodic function, and Phase represents a specific point in that cycle. Phase is a continuous value in [0, 2Pi].** For walking, the left foot touching the ground is 0 and the right foot touching the ground is Pi. For dribbling a ball, the ball in the hand is 0 and the ball on the ground is Pi.

> Note: Phase does not represent the frequency of the motion, only the state at a specific moment in time.

**How Phase is used for character control:**
1. Given some motion capture data, label the Phase at every frame.
2. Build a character control framework around Phase.
	1. Given a Phase, a hypernetwork predicts the weights of the character control network.
	2. The character control network takes (state at the previous frame, user input) as input, and produces (next-step movement, change in Phase) as output.
	3. Update Phase using the predicted change. Go back to step a.
3. Train the character control network from step 2 using the data extracted in step 1.

**Why Phase was introduced: to give the character control network more capacity.**
1. Without Phase, there is one global character control network that has to memorise the input-output mapping for every state.
2. With Phase, each Phase has its own character control network, and that network only has to memorise the input-output mapping for that one state.

**The problems with Phase: some motions are not periodic.**

> Periodic motions: walking; dribbling a ball on the spot.
> Non-periodic motions: walking while dribbling at the same time; the gait of a four-legged animal.

**The fix: Local Motion Phase.** Decompose a complex motion into a combination of several simple periodic motions.

> Example.
> A person playing basketball involves: each foot touching the ground, each hand cupping the ball, and the ball being dribbled.
> Local Motion Phase first breaks "playing basketball" into its core processes: left-foot motion, right-foot motion, left-hand-and-ball interaction, right-hand-and-ball interaction, and ball-ground contact. Combining these core processes reproduces the overall basketball motion.

**How Local Motion Phase is used for character control:**
1. Given some motion capture data, label the local phases at every frame.
2. Build a character control framework around the local phases.
	1. Given a set of local phases, a hypernetwork predicts the weights of the character control network.
	2. The character control network takes (state at the previous frame, user input) as input, and produces (next-step movement, change in local phases) as output.
	3. Update the local phases using the predicted change. Go back to step a.
3. Train the character control network from step 2 using the data extracted in step 1.

**The problems with Local Phase:**
1. **It is hard to decompose whole-body motion into individual periodic sub-motions.** For example, how do you decompose "kicking a football"?
2. **It cannot handle non-periodic motion.** For example, you cannot decompose "dancing".

**The fix: DeepPhase.** Train an autoencoder that extracts phase vectors directly from motion data.

**How DeepPhase is used for character control:**
1. Given some motion capture data, first use DeepPhase to extract a phase vector at every frame.
2. Build a character control framework around the phase vector.
	<details>
	<summary>The specific steps (the same shape as the Phase and Local Phase character control loop)</summary>

	1. Given a phase vector, a hypernetwork predicts the weights of the character control network.
	2. The character control network takes (state at the previous frame, user input) as input, and produces (next-step movement, change in the phase vector) as output.
	3. Update the phase vector using the predicted change. Go back to step a.
	</details>
3. Train the character control network from step 2 using the data extracted in step 1.
