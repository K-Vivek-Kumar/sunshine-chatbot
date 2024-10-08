import json
import pickle


class TrieNode:
    def __init__(self):
        self.children = {}
        self.output_number = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, output_number):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if node.output_number is None:
            node.output_number = output_number

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node.output_number

    def display(self):
        self._display_helper(self.root, "")

    def _display_helper(self, node, word):
        if node.output_number is not None:
            print(f"Word: {word}, Output Number: {node.output_number}")
        for char, child in node.children.items():
            self._display_helper(child, word + char)


if __name__ == "__main__":
    with open("dictionary.json", "r") as f:
        dictionary = json.load(f)

    with open("bot_responses.json", "r") as f:
        bot_responses = json.load(f)

    trie = Trie()
    output_number = 1

    for base_word, equivalents in dictionary.items():
        trie.insert(base_word, output_number)
        for equivalent in equivalents:
            trie.insert(equivalent, output_number)
        output_number += 1

    for response in bot_responses.get("responses", []):
        relevancy = response.get("relevancy", [])
        for word in relevancy:
            trie.insert(word, output_number)
            output_number += 1

    trie.display()

    with open("trie.pkl", "wb") as f:
        pickle.dump(trie, f)

    print("Saved as 'trie.pkl'.")
