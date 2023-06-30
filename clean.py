def filter_words(input_file, output_file):
    # Read the input file.
    with open(input_file, 'r') as f:
        words = f.read().splitlines()

    # Initialize an empty set to hold the filtered words.
    filtered_words = set()

    # Iterate over the words.
    for word in words:
        # If the word is 7 characters or less, does not contain a hyphen, and 
        # it does not end with "'s" or if it ends with "'s" but the root word 
        # isn't in the filtered words, add it to the set.
        if len(word) <= 7 and '-' not in word and (not word.endswith("'s") or word[:-2] not in filtered_words):
            filtered_words.add(word)

    # Write the filtered words to the output file.
    with open(output_file, 'w') as f:
        for word in sorted(filtered_words):  # Sorting the words for better readability.
            f.write(word + '\n')


# Call the function.
filter_words('masterwords.txt', 'filtered_words.txt')
