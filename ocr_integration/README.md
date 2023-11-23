# OCR Integration
Extract text from image(s)

![Extract text from images](screenshot.png "Screenshot")

## Notes
EasyOCR does not support Python 3.12+ as of Nov 2023

## Quickstart
* Make sure to use Python ^3.10 up to 3.11.x
* Follow base README.md quickstart instructions, then proceed

## Usage
### Image Directory
* Default image directory is set to `../discord_integration/attachments`
* Image Directory can be set via env variable `ATTACHMENTS_DIR`

### Console
`python ocr.py {list of images}`

Ex: `python ocr.py image01.png image02.png`

### Script
```
  import ocr
  
  images = ["image01.png", "sample01.png"]
  result = ocr.extract_text(images)
  print(result)
```
  
