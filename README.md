# ngram_tools
Tools to process N-grams for language modeling

## Requirements
- Python 3.4

## File format
A line should have an N-gram and a frequency. Space characters should separate all words within N-gram and between N-gram and frequency. For example, an N-gram file might look like this.

    I am 10
    am Japanese 10
    I 100
    am 100
    Japanese 10


## Unit testing
Run the following command on the top of project directory.

    python -m unittest discover tests
