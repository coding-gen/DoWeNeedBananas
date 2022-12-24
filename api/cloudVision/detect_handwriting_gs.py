#! /usr/bin/python3

def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    verbose = False

    response = client.document_text_detection(image=image)
    print_statement = ''
    result = []
    result = response.text_annotations[0].description

    """
    print(response['text_annotations'])

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print_statement += '\nBlock confidence: {}\n'.format(block.confidence)
            #print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print_statement += 'Paragraph confidence: {}'.format(
                    paragraph.confidence)
                if paragraph.confidence > 0.5:
                    phrase = ''
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        if len(phrase) == 0:
                            phrase += word_text
                        else:
                            phrase += ' ' + word_text
                    result.append(phrase)
                else:
                    continue

                if verbose: 
                    for word in paragraph.words:
                        word_text = ''.join([
                            symbol.text for symbol in word.symbols
                        ])
                        print_statement += 'Word text: {} (confidence: {})'.format(
                            word_text, word.confidence)

                        for symbol in word.symbols:
                            print_statement +='\tSymbol: {} (confidence: {})'.format(
                                symbol.text, symbol.confidence)

    if verbose:
        print(print_statement)
    """
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return result


if __name__ == "__main__":
    bucket = 'gs://doweneedbananas/IMG-4807.jpg'
    detect_document_uri(bucket)