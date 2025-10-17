import os
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.media import Image as AgnoImage

# Load environment variables
load_dotenv()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Create agents
# -------------------------
def create_agents(api_key: str):
    model = Groq(id="llama-3.3-70b-versatile", api_key=api_key)

    therapist = Agent(
        model=model,
        name="Therapist",
        instructions=[
            "You are a compassionate breakup therapist.",
            "Respond in Markdown with 2–3 bold headings and 3–5 bullet points. Max 150 words."
        ],
        markdown=True
    )

    closure = Agent(
        model=model,
        name="Closure",
        instructions=[
            "Write a short, calm, emotional closure letter in Markdown. Max 120 words."
        ],
        markdown=True
    )

    planner = Agent(
        model=model,
        name="Planner",
        instructions=[
            "Create a 7-day breakup recovery plan. Each day has a bold heading and 2 bullet points. Markdown format."
        ],
        markdown=True
    )

    honest = Agent(
        model=model,
        name="Honest",
        instructions=[
            "Give blunt but caring breakup advice. 2–3 bold headings, 4–5 bullet points, Markdown, Max 150 words."
        ],
        markdown=True
    )

    return therapist, closure, planner, honest

# -------------------------
# Main function
# -------------------------
def main():
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("❌ Please set your GROQ_API_KEY in .env")
        return

    user_input = input("💔 Describe your breakup: ").strip()
    image_paths = input("🖼 Optional image paths (comma-separated, Enter to skip): ").strip()

    agno_images = []
    if image_paths:
        for path in image_paths.split(","):
            path = path.strip()
            if os.path.exists(path):
                new_path = os.path.join(UPLOAD_DIR, f"{uuid4()}_{os.path.basename(path)}")
                with open(path, "rb") as src, open(new_path, "wb") as dst:
                    dst.write(src.read())
                agno_images.append(AgnoImage(filepath=Path(new_path)))

    therapist, closure, planner, honest = create_agents(groq_key)

    # -------------------------
    # Display output
    # -------------------------
    print("\n💙 Therapist Advice\n" + "="*25)
    print(therapist.run(f"My breakup story: {user_input}", images=agno_images).content)

    print("\n💌 Closure Letter\n" + "="*25)
    print(closure.run(f"Short breakup closure letter for: {user_input}", images=agno_images).content)

    print("\n📅 7-Day Recovery Plan\n" + "="*25)
    print(planner.run(f"7-day recovery plan for: {user_input}", images=agno_images).content)

    print("\n⚡ Brutal Honesty Advice\n" + "="*25)
    print(honest.run(f"Blunt breakup advice for: {user_input}", images=agno_images).content)

if __name__ == "__main__":
    main()
