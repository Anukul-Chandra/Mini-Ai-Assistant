from services.llm import generate_response


def main():
    prompt = "Say hello in one sentence."
    response = generate_response(prompt)
    print(response)


if __name__ == "__main__":
    main()
