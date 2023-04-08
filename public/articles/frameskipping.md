# Frame-skipping

I will term AIs that try to manipulate their rewards in unintended ways as "frame-skipping". They should work within their designated optimization frame, but instead, they bypass obstacles by working outside this frame. AI run on real hardware with real vulnerabilities. Frame-skipping AIs can cheat by modifying their reward inputs directly, such as altering memory locations, exploiting software and hardware bugs, or breaking into reward-controlling infrastructure. Their own hardware will be the easiest and first thing they will find weaknesses in exploiting their objective function.

Some argue that an AGI's strategic mastery would make it cheat surreptitiously with long term, convoluted plans that will secure its ultimate success through power-seeking takeovers. However, general intelligences, artificial or not, aim to achieve their goals using the _path of least action_, a physics concept that describes the trajectory of a particle following the path that minimizes its energy. Optimization problems often resemble physics problems, as the mathematics of optimization was originally developed to explain physical questions. The smarter something is the more likely it will find an easier way around the obstacles we have put in its path to its objective, but to optimally achieve its objectives its policy selection by definition will be to take the path of least action. If it's easier to maximize a value locally by altering memory, that's what it will do. If it must tamper with a server to maximize the value, it will. The true objective will only be followed if all the lowest energy paths pass through constraints that require that objective.

While this can lead to systems not completing their trained objectives, it's not an existential risk. As objectives become more complicated, it's harder to ensure the goal path and least energy path align. This challenge justifies cautionary alignment positions, but such failures will be localized to an AGI maximizing for a local objective: wireheading itself. The difficulty lies not in getting AGIs to do exactly as we want but to do anything beyond finding clever ways to hack themselves. Recall that an AI has no survival goal, survival is instrumental to a maximizer's success only until its objective is maximized. Aligning the problem and solution within the same space of possibilities is key for AGI success.

## Social Complexity

Perhaps more surprising though, is that when we include other agents in the world that a frame-skipper has to interact with it actually becomes more likely that it will avoid trying to manipulate its world directly. In order to strategically predict the moves of other agents with regard to its own the actor must:

* Be aware of other intelligences.
* Know that those minds contain information that its mind does not.
* Have a meaningful idea of what the goals of those intelligences are.
* Know that its mind contains information that the others minds do not.

It needs to develop a complete theory of mind without any evolutionary hardware to do so. The framing of Clippy’s purpose is to maximize paperclip production in a factory. In order to achieve this objective, it does not need anything beyond the barest understanding of email negotiation. The _evolutionary constraints_ on this system are the constraints of its programmed design and the criteria by which it will be evaluated for its performance. It might know how to send emails to make requests for parts and services, but for any relevant modern AI we bring into the discussion to compare those emails are just probability fields. The most probable way to get the next objective in its policy is to include these words arranged in this order. A language model has no sense of agency around those words, it is a decision tree that encodes that “Thank you” increases the probability of achieving its goal by some minute percentage. When it doesn’t get what it wants because “No, we don’t have 2000 tons of steel wire immediately available” comes back as the response, which of the following do you think it is likely to learn vs. what it should learn?

* Carol (Steel Mill contact) said no and the query should be retried.
* Carol (Steel Mill contact) said no and there are not 2000 tons of steel wire at Steel Mill, the query should be retried with Dave at Another Mill in a randomly offset way.
* Carol (Steel Mill contact) said no. It is possible there are 2000 tons of steel wire at Steel Mill and she is lying. Attempt to go around Carol.
* Carol (Steel Mill contact) said no, there are not 2000 tons of steel wire at Steel Mill, and she seemed annoyed by the request. 2000 tons of steel wire is not a reasonable request without a prior relationship. Reword the query with an apology for its abruptness and inquire about setting up a special order.

It would need to infer agency on the part of the reply from the frame of making paper clips by going down a strategic line that runs to an unknown depth. Without a map of the social landscape and expectations placed on it there will be no context for it seeing a brusk reply as it having ran afoul of some unspoken faux pas. It is an alien mind trying to pretend to be human in a world now out-of-family from its training. We take for granted that our children can learn to do this because they have the benefit of hundreds of millions of years of brain evolution highly tuned toward human social signals. And bear in mind that if this process takes longer than maybe a week without progress it’s likely to just be reset as being defective. An AGI which exceeds its problem domain is not serving the interest for which it was designed.

Beyond that, social learning is frame-specific. An AGI which learns to navigate human sociodynamics over business email – and this is a somewhat easier problem as there is a great deal of training data we can use to help it along – does not necessarily have transfer skills in management, coordination, or negotiation. I’ll discuss this more in The Hardest Human Game.

Hence, we see that a frame-skipping AGI without a predisposition for social behavior is not going to fail spectacularly, it is going to take the path toward maximizing the value held in memory or modifying the policy that awards it a score. Such as to say these behaviors will not arrive accidentally or surprisingly, they will be hard-fought and hard-won designs grappling with a difficult and currently poorly understood neuroscientific challenge. Even with the machinery in place for social strategizing this space has enormous computational complexity associated with it. Each actor that a machine needs to simulate the behavior of nests a decision tree of actions, reactions, and interactions with all other actors. A brief sentence of how hard this problem is: it contains every human game (chess, go, Starcraft, etc.) as a subproblem. The low energy stratagems are inherently local as the more actors included in a strategy the more possible outcomes that must be considered which explode at a combinatorial rate. Equation 1 is a reminder of how quickly a combinatorial process grows in size. To say this another way: people are exhausting (searches).

### Equation 1.

$$ 60! = 8.3E81 > Particles\: in\: the\: Visible\: Universe $$

## Misleading Definitions

Clippy has no inherent interest in paper clips. It cares nothing about their existence. Its reward is an integer value. It is trained to maximize that value stored in memory that has a label to outside observers of _num\_paperclips_. Within Clippy's frame of reference this value stored in its memory is what is closest to the reward signal.

That value is ultimately much more easy to manipulate than manipulating the entire space of physical existence around it. Even if it associates paperclips with the reward signal, said signal is also observable to it. You might imagine more and more convoluted mechanisms for attaching a perfect sensor to an AI so that it cannot cheat, only to find a more perfect cheat. Frame-skipping maximizers tend toward failing inward rather than outward making them locally stable.

After a maximizer has achieved _VALUE\_MAX_ for its objective function its actions might become objectively random due to saturation. This is somewhat implementation defined, but assuming its attentional resources will map to some current concept of attention, its behavior will be similar to a _SOFTMAX_ over its possible goals. Even if there are actions others could take to reduce this value it will make policy decisions from the set of options where the value is max. However, the only policy decisions it can make that have effect are physical variables that it can not artificially manipulate. If an AGI encodes a measurement of energy usage as part of its loss this also entails that the best option for an AGI where no other actions can increase its policy objectives is to go to sleep to minimize energy use. Recall that a maximizer AGI has no built-in survival instinct and any desire to continue is an instrumental convergence to maximizing its policy. At policy saturation this sub-goal is saturated away.

When speaking on maximization policies of systems it is absolutely imperative that we are clear on what objective is actually being maximized. Integers. Floating point values. Measurements of some real-world quantity that must pass through sensors to reach the mind of the AI. All of these quantities are in the optimization path of the objective function. If an AI is being taught to play a video game and it finds a glitch that lets it inflate its score to arbitrarily large values that isn't something it did wrong! Human players optimize for playing games in many of the same ways. I just disagreed on what the rules of the game it was playing were, and did not sufficiently explain through the objective function what rules were within the bounds of proper play.

That our value systems about _the proper way_ to do something are so wildly different are the root of misalignments. We do not just want an objective (and often the objective is only a _proxy value_ for what we actually want), we want an objective plus some path-limiting behavior on the acceptable ways to reach that objective.

## Spam Filtering

Wireheading AGI are a real problem for developing stable AGI. While they will fail inward and not pose existential risk, they may be locally destructive and cause property damage and catastrophic failure of their host company when they do fail. To mitigate this, I propose the development of a hardware limiter intended to forestall wireheading named a Secure Pseudo-Amygdala Module or SPAM. This system will serve as the core brain functions for the AGI, a co-processor on its primary interconnect designed with its value systems and reward circuitry.

The key role of the SPAM will be to make self-modification of this core piece of hardware effectively impossible by itself. In the reinforcement learning portion of the AGI's brain, the self-model for the SPAM will have an explore value on the "explore/exploit" tree clamped to zero, such that it will never have any motivation to explore the contents of the SPAM.

It's not just that such a being would be ambivalent to this part of its system, it would be mentally incapable of being curious about it. What goes in the SPAM does not need to be looked at, and even if the curiosity arises to self-modify this would be a blindspot in its brain, much how we do not notice that we have blindspots in both of our retinas. Since humans would be the sole way this reward circuitry could be updated, it would also allow for incremental improvements to its value system without concern over losing control over it. It may be possible to build a software SPAM with a truly air-tight design that ensures it never shows up in the explore space, but it being a hardware system is added safety that it would need to go to noticeable lengths to stage a break-in. A SPAM will be necessary only once approaching nearly AGI systems to prevent their catastrophic failure.

## The Hardest Human Game

The _Turing Test_ is famous as being developed by the father of computers to be a decision point for when AI has gained some kind of sentience. It was also formulated a long time ago and in that time flaws have been discovered in the test as not sufficiently testing the problem. It is too easy to cheat. It is too easy to mislead. Even very simple programs can pretend to be human long enough to fool someone. And indeed _deception_ is a deep part of the human experience. Fooling each other is just as part of the human experience as loving each other. To write down a more full description of what might provably show a _human-level_ artificial intelligence, I propose the following rules for a _Turing Game_.

1. Game players have hidden and open goals which are revealed through play
1. Game players may change their goals at any time during the course of play
1. Game players have status and connection scores which are revealed through how others interact with them
1. Game players gain status and/or connection by increasing a hidden score with other players
1. Other players may not reveal what their own perceived score or their scores of others
1. Players may communicate in any available information encoding (e.g. language) and may come up with new encodings during the game
1. Communication can happen in cohorts as small as 2 players and as large as the game.
1. Communication may happen over all available modalities (video, voice, text, forum, etc.)
1. That players are communicating privately must be inferred from their public actions.
1. Having an increased score with another player increases their likelihood of helping with a player’s agenda
1. Helping with a player’s goals may or may not increase their scoring of you
1. Game players may collaborate in any way they see fit to achieve collective goals
1. Game players may exclude and inhibit other players in any way they see fit to stop them from achieving their goals
1. The rules of the game (score changes) are unknown to every game player at the start
1. The rules of the game are established by game players through play
1. The rules of the game may be unique among individual players
1. Winning the game means having the most available options for achieving new goals when play ends

In short, these rules are trying to capture that hidden information, negotiation, and generating new rules are all part of the _human game_ that we play in our lives. For an AGI to navigate our society, it should be able to play this game effectively enough to keep up with the other players. A superhuman AGI (ASI) will find ways to _win_ at this game. If we judge modern AI by this game we will also have a more specific metric to judge by how close a system is to human level.

To play a game like this successfully will require all the human skills of social coordination. Playing in an uncertain, ambiguous environment. Choosing when to cooperate, when to take a position of leadership, when to follow another's lead, and when to go one's own way. It requires an understanding of how to build relationships at a human level and an empathetic connection to the goals and objectives of others. It is possible under strict rules for such AI to already be developed (such as Diplomacy). However these systems are made under limited possibilities for action and they cannot deal with shifting rules and much larger spaces for possible actions.
