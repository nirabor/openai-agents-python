# Sample Tutor Coach Interaction

This document shows a sample interaction flow with the tutor coach system.

## Running the Example

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Run the tutor coach
python -m examples.tutor_coach.main
```

## Sample Conversation Flow

### Example 1: Getting Math Help

```
You: I need help with derivatives
Triage Agent: I'll connect you with our Math Tutor who specializes in mathematics.
[Transferring from Triage Agent to Math Tutor]

Math Tutor: I'd be happy to help you with derivatives! What specific aspect would you like to explore?

You: How do I find the derivative of x^3?
Math Tutor: [Uses math_explanation_tool]
Great question! The derivative of x^3 uses the power rule: d/dx(x^n) = n*x^(n-1)

So for x^3:
- n = 3
- d/dx(x^3) = 3*x^(3-1) = 3x^2

Would you like to try another example?

You: Yes, what about the derivative of sin(x)?
Math Tutor: The derivative of sin(x) is cos(x). This is one of the fundamental trigonometric derivatives. 
Would you like me to explain why, or try some practice problems?
```

### Example 2: Getting Writing Help

```
You: I need to write an essay for my English class
Triage Agent: I'll connect you with our Writing Tutor for help with your essay.
[Transferring from Triage Agent to Writing Tutor]

Writing Tutor: I can help you with your essay! What's the topic, and what stage are you at?

You: It's about climate change and I'm just starting
Writing Tutor: Great topic! Let's start by developing a strong thesis statement. [Uses writing_feedback_tool]

A strong thesis should be:
1. Specific and focused
2. Debatable (not just a fact)
3. Supported by evidence
4. Clear about your position

For climate change, you might consider: "Immediate government action on climate change is essential 
because current voluntary measures are insufficient to prevent catastrophic environmental damage."

What do you think? Would you like to refine this or discuss the essay structure?
```

### Example 3: Study Strategy Help

```
You: I have a big test next week and I don't know how to prepare
Triage Agent: I'll connect you with our Study Coach for test preparation strategies.
[Transferring from Triage Agent to Study Coach]

Study Coach: I can definitely help you prepare effectively! Tell me about the test - what subject 
and what type of material will be covered?

You: It's a history test covering 3 chapters, mostly facts and dates
Study Coach: [Uses study_strategy_tool]
Perfect! For memorizing facts and dates, here's an effective approach:

1. Spaced repetition - Review the material at increasing intervals (today, tomorrow, in 3 days, in 5 days)
2. Active recall - Test yourself instead of just re-reading
3. Mnemonics and acronyms - Create memory aids for dates and events
4. Chunking - Group related historical events together

Let's create a study schedule for the next week. When's your test?

You: It's on Friday
Study Coach: Great! Here's a plan:
- Monday: Read chapter 1, create flashcards
- Tuesday: Review chapter 1 flashcards, read chapter 2
- Wednesday: Review all flashcards, read chapter 3
- Thursday: Practice test, focus on weak areas
- Friday morning: Quick review of main concepts

Would you like tips on creating effective flashcards or note-taking?
```

### Exiting the Session

```
You: quit

Study session summary:
1. Discussed derivatives and power rule
2. Practiced derivative of x^3 = 3x^2
3. Learned that d/dx(sin(x)) = cos(x)

Good luck with your studies!
```

## Multi-Topic Sessions

The system can handle switching between topics:

```
You: Can you help with both math and writing?
Triage Agent: Of course! Let's start with one - which would you like to tackle first?

You: Math please
[Transfers to Math Tutor]
...
[After math discussion]
You: Now can you help with my essay?
Math Tutor: I'll transfer you to our Writing Tutor for that!
[Transfers to Writing Tutor]
...
```

## Features Demonstrated

1. **Smart Routing**: The triage agent understands context and routes to the right specialist
2. **Context Preservation**: The system remembers the conversation throughout the session
3. **Session Notes**: Important points are tracked and summarized at the end
4. **Bidirectional Handoffs**: Agents can transfer back to triage when needed
5. **Multiple Domains**: Math, writing, and study strategies all in one system
