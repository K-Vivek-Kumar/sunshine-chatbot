import json
import pickle
import math
from collections import Counter


from Trie import Trie, TrieNode


def encode(sentence):
    s = sentence.split(" ")
    with open("trie.pkl", "rb") as trie_file:
        trie: Trie = pickle.load(trie_file)
    vector = []
    for word in s:
        position = trie.search(word)
        if position is not None:
            vector.append(position)
    return vector


def build_frequency_vector(vec1, vec2):
    all_unique_numbers = list(set(vec1 + vec2))

    count_vec1 = Counter(vec1)
    count_vec2 = Counter(vec2)

    frequency_vec1 = [count_vec1.get(num, 0) for num in all_unique_numbers]
    frequency_vec2 = [count_vec2.get(num, 0) for num in all_unique_numbers]

    return frequency_vec1, frequency_vec2


def cosine_similarity(vec1, vec2):
    frequency_vec1, frequency_vec2 = build_frequency_vector(vec1, vec2)

    dot_product = sum(x * y for x, y in zip(frequency_vec1, frequency_vec2))
    magnitude_vec1 = math.sqrt(sum(x**2 for x in frequency_vec1))
    magnitude_vec2 = math.sqrt(sum(x**2 for x in frequency_vec2))

    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0.0

    return dot_product / (magnitude_vec1 * magnitude_vec2)


def top_2_responses(similarity_values):
    if len(similarity_values) < 2:
        return 0, 0

    first_max = second_max = -1
    first_idx = second_idx = 0

    for i, sim in enumerate(similarity_values):
        if sim > first_max:
            second_max = first_max
            second_idx = first_idx
            first_max = sim
            first_idx = i
        elif sim > second_max:
            second_max = sim
            second_idx = i

    return first_idx, second_idx


def respond(query):
    encoded_query = encode(query)
    print(f"{encoded_query=}")
    with open("bot_responses.json", "r") as bot_file:
        bot_responses = json.load(bot_file)["responses"]

    similarity_values = []

    for response in bot_responses:
        relevant_words = " ".join(response["relevancy"])
        encoded_response = encode(relevant_words)
        print(f"{encoded_response=}")
        similarity = cosine_similarity(encoded_query, encoded_response)
        similarity_values.append(similarity)

    print(f"{similarity_values=}")

    idx1, idx2 = top_2_responses(similarity_values)

    return bot_responses[idx1]["response"], bot_responses[idx2]["response"]


if __name__ == "__main__":
    query = "Hello Sunshine"
    response, _ = respond(query)
    print(response)
