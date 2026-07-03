from services.retrieval import retrieve_context


def main():
    query = "What is this document about?"

    try:
        results = retrieve_context(query)
    except ValueError as e:
        print(f"Error: {e}")
        return

    print(f"Total retrieved chunks: {len(results)}")
    print("=" * 60)
    for i, chunk in enumerate(results, 1):
        print(f"Chunk {i}:")
        print(chunk)
        print("-" * 40)


if __name__ == "__main__":
    main()
