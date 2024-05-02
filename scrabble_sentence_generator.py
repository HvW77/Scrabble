import random
import re

class ScrabbleHelper:
    def __init__(self, word_file):
        # Initialize the ScrabbleHelper object by loading the word dictionary from the word file
        # This dictionary will be used to find replacements for words in input sentences
        self.word_map = self.load_words(word_file)

    def load_words(self, file_path):
        while True:
            try:
                with open(file_path, 'r') as file:
                    word_map = {}
                    for line in file:
                        word = line.strip()  # Remove whitespace around the word
                        key = (word[0], len(word))  # Form the key from the word's first letter and its length
                        if key not in word_map:
                            word_map[key] = []  # Initialize the list if the key does not exist
                        word_map[key].append(word)  # Add the word to the corresponding list
                    return word_map
            except FileNotFoundError:
                print(f"The file {file_path} was not found.")
                # Prompt for the word list file path when the file is not found
                file_path = input("Please enter the correct path to the word list file: ")
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Break from the loop if other types of exceptions occurs

    def transform_sentence(self, sentence):
        # Transforms the input sentence by replacing each word with a random word that starts with the same letter
        # and has the same length, using the word_map dictionary
        # It avoids returning the same word if possible
        words = re.findall(r'\b\w+\b', sentence)  # Extract words while ignoring punctuation
        transformed_words = []

        for word in words:
            key = (word[0].lower(), len(word))  # Create a key for searching in the dictionary

            if key in self.word_map:
                possible_words = self.word_map[key]  # Get possible replacement words
                if len(possible_words) > 1:
                    # Attempt to exclude the original word from the list of candidates if there are other options
                    filtered_words = [w for w in possible_words if w != word.lower()]
                    new_word = random.choice(filtered_words if filtered_words else possible_words)
                else:
                    new_word = random.choice(possible_words)  # Use the available word if it's the only option
            else:
                new_word = word  # If no replacement is found, use the original word
            transformed_words.append(new_word)

        # Replace each word in the original sentence with the transformed word, maintaining the original punctuation
        transformed_sentence = re.sub(r'\b\w+\b', lambda x: transformed_words.pop(0), sentence)

        return transformed_sentence

    def is_valid_input(self, sentence):
        # Validates the user's input to ensure it contains only alphabetic characters, spaces and punctuation
        # This prevents errors in word processing that might occur from unexpected characters
        return all(c.isalpha() or c.isspace() or c in '.,;:!?' for c in sentence)
    

def main():
    # Main function to run the ScrabbleHelper. It initializes the helper and continuously processes user input
    helper = ScrabbleHelper('words_alpha.txt')

    print('Please enter any sentence to receive a newly generated sentence where each word starts with the same letter and has the same length as the corresponding word in your original sentence.')
    print('E.g. "Lightly fried fish are delicious" becomes "likable frier frog arm delegated".')

    while True:
        sentence = input('\nEnter a sentence (or type "exit" to quit): ')
        
        if sentence.lower() == 'exit':
            break  # Exit the program if the user types 'exit'
        if not helper.is_valid_input(sentence):
            print('Invalid input. Please enter a sentence that contains only letters, spaces, and standard punctuation.')
            continue  # Request new input if the current one is invalid

        # Display the transformed sentence to the user
        print('Transformed sentence:', helper.transform_sentence(sentence))

if __name__ == '__main__':
    main()  # Execute the main function when the script is run