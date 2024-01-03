import click
import string
import unicodedata
import nltk
from nltk.corpus import stopwords

# Download the stopword set from NLTK
nltk.download('stopwords')

def remove_headers(text):
    """
    Remove the header of a Project Gutenberg file.
    """
    start_delim = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_delim = "*** END OF THE PROJECT GUTENBERG EBOOK"
    start_idx = text.find(start_delim)
    end_idx = text.find(end_delim)

    if start_idx != -1 and end_idx != -1:
        return text[start_idx + len(start_delim):end_idx].strip()
    else:
        return text

def clean_text(text, language):
    """
    Remove stop words, punctuation, convert to uppercase, and remove accents.
    """
    stop_words = set(stopwords.words(language))
    
    # Normalize and remove accents
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    
    # Keep only letters and spaces
    text = ''.join([char for char in text if char in string.ascii_letters + ' '])
    
    # Split words, remove stop words, and convert to uppercase
    words = text.split()
    cleaned_text = ' '.join([word.upper() for word in words if word.lower() not in stop_words or word.lower().endswith(".jpg")])
    
    return cleaned_text


def process_file(input_filename, language):
    """
    Process the given file, removing headers, stop words, punctuation, and converting to uppercase,
    and then save the output to another file.
    """
    output_filename = input_filename.replace('.txt', '_clean.txt')

    try:
        with open(input_filename, 'r', encoding='utf-8') as file:
            content = file.read()

        cleaned_content = clean_text(remove_headers(content), language)

        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(cleaned_content)
        print(f"Processed content saved to {output_filename}")

    except FileNotFoundError:
        print(f"The file {input_filename} was not found.")

@click.command()
@click.argument('input_filename')
@click.option('--language', default='english', help='Language to use for stop words.')
def process_file_cli(input_filename, language):
    process_file(input_filename, language)

if __name__ == "__main__":
    process_file_cli()
