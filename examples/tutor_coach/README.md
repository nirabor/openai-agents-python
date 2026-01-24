# Tutor Coach

An interactive AI-powered tutor and study coach system that provides personalized help across multiple academic subjects and study strategies.

## Overview

This example demonstrates a multi-agent educational assistant that can:

- Help with **mathematics** (calculus, algebra, geometry)
- Provide **writing assistance** (essays, citations, grammar)
- Offer **study strategies** (memorization, test prep, focus techniques)
- Maintain conversation context across topics
- Track study session notes

## Architecture

The system uses a **triage-based handoff pattern** with specialized tutor agents:

1. **Triage Agent**: Greets students and routes them to the appropriate specialist
2. **Math Tutor**: Provides step-by-step math explanations and problem-solving guidance
3. **Writing Tutor**: Helps with essays, papers, citations, and writing skills
4. **Study Coach**: Offers evidence-based study strategies and learning techniques

Each specialist agent can hand off back to the triage agent when questions fall outside their domain.

## Features

### Tools

- `math_explanation_tool`: Provides explanations for calculus, algebra, geometry, and more
- `writing_feedback_tool`: Offers guidance on essays, thesis statements, citations, and grammar
- `study_strategy_tool`: Shares effective study techniques for memorization, test prep, and focus
- `add_study_note`: Tracks important points during the study session

### Context Management

The system maintains a `StudentContext` that tracks:
- Student name
- Current subject being discussed
- Notes from the study session

## Running the Example

```bash
python -m examples.tutor_coach.main
```

Make sure you have set your `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Example Interactions

### Getting Math Help

```
You: I need help understanding derivatives
Triage Agent: I'll connect you with our Math Tutor for help with derivatives.
[Transferring from Triage Agent to Math Tutor]
Math Tutor: I'd be happy to help you with derivatives! What specific aspect of derivatives would you like to explore?
You: How do I find the derivative of x^3?
Math Tutor: [Uses math_explanation_tool to provide step-by-step guidance]
```

### Getting Writing Help

```
You: I need to write a thesis statement for my essay
Triage Agent: I'll connect you with our Writing Tutor for help with your thesis statement.
[Transferring from Triage Agent to Writing Tutor]
Writing Tutor: I can help you craft a strong thesis statement! What is your essay topic?
```

### Getting Study Tips

```
You: How can I study better for my exams?
Triage Agent: I'll connect you with our Study Coach for exam preparation strategies.
[Transferring from Triage Agent to Study Coach]
Study Coach: I can definitely help you improve your exam preparation! [Uses study_strategy_tool]
```

## Session Summary

When you exit (type 'quit' or 'exit'), the system displays all notes taken during the session, providing a helpful summary of key concepts discussed.

## Customization Ideas

Extend this example by:

1. **More subjects**: Add tutors for science, history, languages, etc.
2. **File upload**: Allow students to upload homework or essays for review
3. **Practice problems**: Generate and check practice problems
4. **Progress tracking**: Store student progress across multiple sessions
5. **Calendar integration**: Help students schedule study time
6. **Flashcard creation**: Auto-generate flashcards from study sessions
7. **Quiz generation**: Create custom quizzes based on topics covered

## Educational Approach

This tutor system follows evidence-based teaching practices:

- **Scaffolding**: Breaking complex topics into manageable steps
- **Active learning**: Encouraging students to try problems themselves
- **Spaced repetition**: Recommending review at intervals
- **Metacognition**: Teaching students how to learn effectively
- **Positive reinforcement**: Celebrating progress and providing encouragement
