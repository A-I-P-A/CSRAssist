import json
import easyocr
import argparse

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
    parser = argparse.ArgumentParser(description='Extract text from a given image')
    parser.add_argument('-f', '--file', help='Image path', required=True)
    args = parser.parse_args()
    print(json.dumps(extract_text([args.file]), indent=2))

if __name__ == '__main__':
    main()
