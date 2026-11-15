# Week 11 answers

## Exercise 1
1. The message the customer never saw: The system message which holds the instructions
2. How many times the customer has spoken: Twice
3. Can the model tell that the last reply came from the order tool? Why does that matter? No. In the history every reply has the role assistant, whether a rule, a tool, or the model wrote it. The model reads the whole history, so it can copy the pattern of an earlier tool answer and state something the tool never said.
4. The customer now types "thanks". How many messages are sent on the next call? 6. 