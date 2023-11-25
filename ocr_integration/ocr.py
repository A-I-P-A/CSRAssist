import sys
import os
import json
import easyocr
import warnings
import argparse

# Console Arguments
parser = argparse.ArgumentParser(description='Extract text from a given image')
parser.add_argument('-f', '--file', help='Image path', required=True)

# Configurations
SCRIPT_DIR = os.path.dirname(__file__)
warnings.filterwarnings('ignore')


def extract_text(img_paths):
    """
    Extract Texts from Images

    Args:
        image_path: list of image paths
    
    Returns:
        results: list of elements containing extracted text for each image
    
    """

    results = []
    reader = easyocr.Reader(['en'], verbose=False)

    for img_path in img_paths:
        img_texts = reader.readtext(img_path, detail = 0)
        results.append({ 'image' : img_path, 'texts' : img_texts })

    return results


# Console
def main():
    args = parser.parse_args()
    sys.stdout.write(json.dumps(extract_text([args.file]), indent=2))
    sys.stdout.write('\n')

if __name__ == '__main__':
    main()
