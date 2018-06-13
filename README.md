# Etymo Workshop

You can download 243 papers from ArXiv converted
using pdfminer from 
[our S3 bucket](https://s3-eu-west-1.amazonaws.com/etymo-workshop/paper_texts.zip) (around 4MB)

If you want, you can also download the original PDFs too from 
[our S3 bucket](https://s3-eu-west-1.amazonaws.com/etymo-workshop/papers.zip) (around 400MB).

You can download the metadata and keywords of 10000 processed papers at
[this github repo](https://github.com/EtymoIO/OpenData) or by typing:
```sh
git clone git@github.com:EtymoIO/OpenData.git
```

## Etymo background

Description of who we are and what we do.

## Text extraction

Main methods of extraction, the main problems and which one looks the best.

Main problems:
- Whitespace
- Equation conversions
- Figures
- References

### pdf2txt

### pdfminer

### tesseract

### Pypdf2


How to download a bundle of text conversions.

## Keyword extraction

Overview of main methods

### RAKE

### TF-IDF

### Graph Theory approach



## Institution extraction

### University search (Heuristic 1 and 2)
TODO: make heuristic better

Briefly explain how it works in general terms, show examples

Build up method from very simple to more complicated.

Can we use the author's name?

### Deep learning

Deep learning? Object recognition

## The data

How to download a bundle of PDFs.
Brief look at some examples.
