import json
import pickle
import math
import re

from Trie import Trie, TrieNode


def clean_sentence(sentence):
    return re.sub(r"[^a-zA-Z0-9 ]+", "", sentence)


def encode_weighted(sentence, decay_factor=0.9):
    s = sentence.split(" ")
    with open("trie.pkl", "rb") as trie_file:
        trie: Trie = pickle.load(trie_file)

    vector = []
    for index, word in enumerate(s):
        position = trie.search(word)
        if position is not None:
            weight = decay_factor**index
            vector.append((position, weight))

    return vector


def build_weighted_frequency_vector(vec1, vec2):
    all_unique_numbers = list(set(pos for pos, _ in vec1) | set(pos for pos, _ in vec2))

    count_vec1 = {pos: 0 for pos in all_unique_numbers}
    count_vec2 = {pos: 0 for pos in all_unique_numbers}

    for pos, weight in vec1:
        count_vec1[pos] += weight
    for pos, weight in vec2:
        count_vec2[pos] += weight

    frequency_vec1 = [count_vec1[pos] for pos in all_unique_numbers]
    frequency_vec2 = [count_vec2[pos] for pos in all_unique_numbers]

    return frequency_vec1, frequency_vec2


def cosine_similarity(vec1, vec2):
    frequency_vec1, frequency_vec2 = build_weighted_frequency_vector(vec1, vec2)

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


def respond(query, decay_factor=0.9):
    encoded_query = encode_weighted(query, decay_factor=1)
    print(f"{encoded_query=}")

    with open("bot_responses.json", "r") as bot_file:
        bot_responses = json.load(bot_file)["responses"]

    similarity_values = []

    for response in bot_responses:
        relevant_words = " ".join(response["relevancy"])
        encoded_response = encode_weighted(relevant_words, decay_factor)
        print(f"{encoded_response=}")
        similarity = cosine_similarity(encoded_query, encoded_response)
        similarity_values.append(similarity)

    print(f"{similarity_values=}")

    idx1, idx2 = top_2_responses(similarity_values)

    return bot_responses[idx1]["response"], bot_responses[idx2]["response"]


if __name__ == "__main__":
    query = "Hello!! This is Vivek Sunshine"
    response, _ = respond(clean_sentence(query))
    print(response)
