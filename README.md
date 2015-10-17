# What is this?
This is a ripper for http://csn.termi.lv/. It scrapes all of the questions from the pages and generates a PDF file with them and the correct answer marked in Bold. 


# Required stuff:
This requires Python 3.5.0 (although I would assume that this will work with any Python3 version), BeautifulSoup 4.4.0 and for PDF output you need Pdfkit 0.5.0 (which in turn requires wkhtmltopdf 0.12.2.1). If you don't want the PDF just comment it. Any other version of these libraries hasn't been tested.

# Note
After running the script it's recommended to use a service like http://smallpdf.com/compress-pdf to compress the file, otherwise you're end up with a really large PDF file.
