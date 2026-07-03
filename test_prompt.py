from services.prompt_builder import build_prompt


def main():
    context = [
        "The Eiffel Tower is located in Paris, France.",
        "It was completed in 1889 and stands 330 meters tall.",
    ]
    question = "Where is the Eiffel Tower?"

    prompt = build_prompt(question, context)
    print(prompt)


if __name__ == "__main__":
    main()
