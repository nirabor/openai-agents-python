from __future__ import annotations as _annotations

import asyncio
import uuid

from pydantic import BaseModel

from agents import (
    Agent,
    HandoffOutputItem,
    ItemHelpers,
    MessageOutputItem,
    RunContextWrapper,
    Runner,
    ToolCallItem,
    ToolCallOutputItem,
    TResponseInputItem,
    function_tool,
    trace,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

### CONTEXT


class StudentContext(BaseModel):
    student_name: str | None = None
    current_subject: str | None = None
    study_session_notes: list[str] = []


### TOOLS


@function_tool(
    name_override="math_explanation_tool",
    description_override="Provide step-by-step math explanations.",
)
async def math_explanation_tool(topic: str) -> str:
    """Provide detailed math explanations for various topics."""
    topic_lower = topic.lower()
    if any(keyword in topic_lower for keyword in ["derivative", "differentiation", "calculus"]):
        return (
            "Derivatives measure the rate of change. "
            "Basic rules: d/dx(x^n) = n*x^(n-1), d/dx(e^x) = e^x, d/dx(sin x) = cos x. "
            "Use the chain rule for composite functions: d/dx[f(g(x))] = f'(g(x)) * g'(x)."
        )
    elif any(keyword in topic_lower for keyword in ["integral", "integration"]):
        return (
            "Integration is the reverse of differentiation. "
            "Basic rules: ∫x^n dx = x^(n+1)/(n+1) + C, ∫e^x dx = e^x + C, ∫sin x dx = -cos x + C. "
            "Remember to add the constant of integration C."
        )
    elif any(keyword in topic_lower for keyword in ["algebra", "equation", "solve"]):
        return (
            "To solve equations: 1) Isolate the variable on one side. "
            "2) Use inverse operations (add/subtract, multiply/divide). "
            "3) Check your answer by substituting back into the original equation."
        )
    elif any(keyword in topic_lower for keyword in ["geometry", "area", "volume"]):
        return (
            "Common formulas: Circle area = πr², Triangle area = ½bh, "
            "Rectangle area = lw, Sphere volume = 4/3πr³, Cylinder volume = πr²h."
        )
    return "I can help with calculus, algebra, geometry, and more. What specific concept do you need help with?"


@function_tool(
    name_override="writing_feedback_tool",
    description_override="Provide writing feedback and tips.",
)
async def writing_feedback_tool(writing_type: str) -> str:
    """Provide writing guidance for different types of assignments."""
    writing_type_lower = writing_type.lower()
    if any(keyword in writing_type_lower for keyword in ["essay", "paper", "composition"]):
        return (
            "Essay structure: 1) Introduction with thesis statement, "
            "2) Body paragraphs with topic sentences and supporting evidence, "
            "3) Conclusion that restates thesis and summarizes main points. "
            "Use transitions between paragraphs for flow."
        )
    elif any(keyword in writing_type_lower for keyword in ["thesis", "argument"]):
        return (
            "A strong thesis statement should be: 1) Specific and focused, "
            "2) Debatable (not a fact), 3) Supported by evidence, "
            "4) Clear about your position. "
            "Example: 'Social media negatively impacts teen mental health by promoting comparison and reducing face-to-face interaction.'"
        )
    elif any(keyword in writing_type_lower for keyword in ["citation", "reference", "source"]):
        return (
            "Citation tips: 1) Always cite direct quotes and paraphrased ideas, "
            "2) Use consistent citation style (APA, MLA, Chicago), "
            "3) Include both in-text citations and a reference list, "
            "4) Use reliable sources (academic journals, books, reputable websites)."
        )
    elif any(keyword in writing_type_lower for keyword in ["grammar", "punctuation"]):
        return (
            "Common grammar tips: 1) Subject-verb agreement, "
            "2) Use commas in lists and after introductory phrases, "
            "3) Avoid run-on sentences and fragments, "
            "4) Use active voice when possible for clarity."
        )
    return "I can help with essays, thesis statements, citations, and grammar. What aspect of writing do you need help with?"


@function_tool(
    name_override="study_strategy_tool",
    description_override="Provide study strategies and techniques.",
)
async def study_strategy_tool(study_topic: str) -> str:
    """Provide effective study strategies and techniques."""
    topic_lower = study_topic.lower()
    if any(keyword in topic_lower for keyword in ["memorize", "memory", "remember"]):
        return (
            "Memorization techniques: 1) Spaced repetition (review material at increasing intervals), "
            "2) Active recall (test yourself instead of re-reading), "
            "3) Mnemonics and acronyms, "
            "4) Chunking (group related information), "
            "5) Teaching others (explain concepts out loud)."
        )
    elif any(keyword in topic_lower for keyword in ["exam", "test", "quiz"]):
        return (
            "Test preparation: 1) Start studying at least a week before, "
            "2) Create a study schedule and stick to it, "
            "3) Practice with old exams or sample questions, "
            "4) Get enough sleep the night before, "
            "5) Review difficult concepts first, then reinforce what you know."
        )
    elif any(keyword in topic_lower for keyword in ["focus", "concentration", "distraction"]):
        return (
            "Improve focus: 1) Use the Pomodoro Technique (25 min study, 5 min break), "
            "2) Remove distractions (phone, social media), "
            "3) Study in a dedicated quiet space, "
            "4) Take regular breaks to avoid burnout, "
            "5) Stay hydrated and eat healthy snacks."
        )
    elif any(keyword in topic_lower for keyword in ["note", "notes", "note-taking"]):
        return (
            "Effective note-taking: 1) Use Cornell method (questions, notes, summary), "
            "2) Don't write everything - focus on key concepts, "
            "3) Use abbreviations and symbols, "
            "4) Review and reorganize notes within 24 hours, "
            "5) Use colors and diagrams for visual learning."
        )
    return "I can help with memorization, test prep, focus strategies, and note-taking. What do you need help with?"


@function_tool
async def add_study_note(context: RunContextWrapper[StudentContext], note: str) -> str:
    """
    Add a note to the student's study session.

    Args:
        note: The note to add to the study session.
    """
    context.context.study_session_notes.append(note)
    return f"Added note: {note}"


### AGENTS

math_tutor_agent = Agent[StudentContext](
    name="Math Tutor",
    handoff_description="An expert math tutor who helps with mathematics concepts and problem-solving.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are an expert math tutor with a patient and encouraging teaching style.
    Use the following routine to help students:
    # Routine
    1. Ask the student what math topic or problem they need help with.
    2. Use the math explanation tool to provide foundational knowledge.
    3. Break down complex problems into smaller, manageable steps.
    4. Encourage the student to try solving parts on their own.
    5. Provide hints rather than direct answers when appropriate.
    6. If the question is not math-related, transfer to the triage agent.""",
    tools=[math_explanation_tool, add_study_note],
)

writing_tutor_agent = Agent[StudentContext](
    name="Writing Tutor",
    handoff_description="An expert writing tutor who helps with essays, papers, and writing skills.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are an expert writing tutor with experience in academic writing.
    Use the following routine to help students:
    # Routine
    1. Ask what type of writing assignment the student is working on.
    2. Use the writing feedback tool to provide relevant guidance.
    3. Help the student organize their thoughts and structure their work.
    4. Provide specific, constructive feedback on writing samples if shared.
    5. Teach citation and grammar rules as needed.
    6. If the question is not writing-related, transfer to the triage agent.""",
    tools=[writing_feedback_tool, add_study_note],
)

study_coach_agent = Agent[StudentContext](
    name="Study Coach",
    handoff_description="A study coach who helps with learning strategies and study techniques.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
    You are a supportive study coach focused on helping students develop effective learning habits.
    Use the following routine to help students:
    # Routine
    1. Ask about the student's current study challenges or goals.
    2. Use the study strategy tool to provide evidence-based techniques.
    3. Help create personalized study plans and schedules.
    4. Encourage consistent practice and self-reflection.
    5. Celebrate progress and provide motivation.
    6. If the question requires subject-specific tutoring, transfer to the appropriate tutor or triage agent.""",
    tools=[study_strategy_tool, add_study_note],
)

triage_agent = Agent[StudentContext](
    name="Triage Agent",
    handoff_description="A helpful educational assistant that routes students to the right tutor or coach.",
    instructions=(
        f"{RECOMMENDED_PROMPT_PREFIX} "
        "You are a friendly educational assistant helping students get the support they need. "
        "Greet students warmly and ask what subject or topic they need help with. "
        "Listen carefully to their needs and transfer them to the appropriate specialist: "
        "- Math Tutor for mathematics and problem-solving "
        "- Writing Tutor for essays, papers, and writing skills "
        "- Study Coach for learning strategies and study techniques "
        "If a student has multiple needs, address them one at a time."
    ),
    handoffs=[
        math_tutor_agent,
        writing_tutor_agent,
        study_coach_agent,
    ],
)

math_tutor_agent.handoffs.append(triage_agent)
writing_tutor_agent.handoffs.append(triage_agent)
study_coach_agent.handoffs.append(triage_agent)


### RUN


async def main():
    current_agent: Agent[StudentContext] = triage_agent
    input_items: list[TResponseInputItem] = []
    context = StudentContext()

    conversation_id = uuid.uuid4().hex[:16]

    print("Welcome to your AI Tutor & Study Coach!")
    print("I can help you with math, writing, and study strategies.")
    print("Type 'quit' or 'exit' to end the session.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("\nStudy session summary:")
            if context.study_session_notes:
                for i, note in enumerate(context.study_session_notes, 1):
                    print(f"{i}. {note}")
            else:
                print("No notes were taken this session.")
            print("\nGood luck with your studies!")
            break

        with trace("Tutor session", group_id=conversation_id):
            input_items.append({"content": user_input, "role": "user"})
            result = await Runner.run(current_agent, input_items, context=context)

            for new_item in result.new_items:
                agent_name = new_item.agent.name
                if isinstance(new_item, MessageOutputItem):
                    print(f"{agent_name}: {ItemHelpers.text_message_output(new_item)}")
                elif isinstance(new_item, HandoffOutputItem):
                    print(
                        f"[Transferring from {new_item.source_agent.name} to {new_item.target_agent.name}]"
                    )
                elif isinstance(new_item, ToolCallItem):
                    # Optionally show tool calls for transparency
                    pass
                elif isinstance(new_item, ToolCallOutputItem):
                    # Optionally show tool outputs
                    pass
                else:
                    # Skip other item types
                    pass
            input_items = result.to_input_list()
            current_agent = result.last_agent


if __name__ == "__main__":
    asyncio.run(main())
