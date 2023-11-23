import sys
import os
import json
import easyocr
import warnings


# Initialization
SCRIPT_DIR = os.path.dirname(__file__)
DEFAULT_ATTACHMENTS_DIR = "../discord_integration/attachments"
ATTACHMENTS_DIR = os.getenv('ATTACHMENTS_DIR') or os.path.join(SCRIPT_DIR, DEFAULT_ATTACHMENTS_DIR)
warnings.filterwarnings('ignore')


# Extract Text from Image
def extract_text(file_names):
    results = [];
    img_file_names = [];

    if isinstance(file_names, list):
        img_file_names = file_names
    else:
        img_file_names.append(file_names)
    
    for img_file_name in img_file_names:
        img_path = os.path.join(ATTACHMENTS_DIR, img_file_name)

        reader = easyocr.Reader(['en'], verbose=False)
        img_texts = reader.readtext(img_path, detail = 0)
        results.append({ img_file_name : img_texts })

    return results


# Via Console
console_out = []
args = len(sys.argv)
if args >= 2:
    images = [];
    for i in range(1, args):
        images.append(sys.argv[i])
    
    sys.stdout.write(json.dumps(extract_text(images), indent=2))
    sys.stdout.write('\n')
