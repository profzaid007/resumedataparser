# Resume Data Parser

## Overview

This Python script is designed to parse resumes and extract relevant information, such as skills and education. The extracted data is then stored in a CSV file for further analysis. The skills dataset is sourced from Kaggle.

## Modules Used

- **pandas**: A powerful data manipulation library. It is used for handling and manipulating the CSV data.
- **nltk**: Natural Language Toolkit for natural language processing. Used for tokenization and text processing.
- **wordcloud**: A module for creating word clouds. Used to visualize unique skills and education.
- **streamlit**: A web application framework used for creating interactive data dashboards.

## How to Install Dependencies

You can install the required modules using the following commands:

```bash
pip install pandas nltk wordcloud docx2txt pdfminer streanlit matplotlib
```
```python
import os
import csv
import json
import re
import subprocess
import docx2txt
import nltk
import streamlit as st
import pandas as pd
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pdfminer.high_level import extract_text

```
## Input
Place resumes in the resumes directory for processing.

## Output
The processed data is stored in output_data.csv.

## Note
This script uses a Kaggle dataset for skills. The dataset (skills.csv) should be present in the project directory.
