
# Discourse Marker Evaluation Workbench

The Discourse Marker Evaluation Workbench is a set of Python scripts designed to process annotated text files containing discourse markers in Hindi. It provides functionalities to extract specific information, convert Hindi words to English, and save the modified text to a new file. This README provides an overview of the project, installation instructions, usage guidelines, file structure, contribution guidelines, and licensing information.


## Features


- File Processing: Read and process text files containing annotated sentences.
- Annotation Conversion: Convert specific Hindi words to English annotations based on a predefined list.
- Text Extraction: Extract relevant information from sentences using regular expressions.
- Language Conversion: Utilize the WXC class from the wxconv library to convert Hindi text to English.

## Installation

Clone the repository:

```bash
  git clone https://github.com/your_username/your_repository.git

```
Install the required libraries:
```bash
  pip install wxconv
  pip install Flask

``` 


    
## Usage

1. Prepare Input Files: 
    Place the text file to be processed in the project directory with the name uploaded_file.
    
2. Ensure that the file format matches the expected format for processing.
3. Run the run.py script

```bash
    python run.py
```

4. Review Output:

    The script will process the input file and create a modified files named annotated_text, annotated_text_after_modification and duplicate_uploaded_file with the converted annotations.

## Example

Suppose you have a file named upload_file with the following content:

```bash
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078a>
#रासायनिक प्रक्रियाएँ सामान्यतः कणों के बीच के बंधन को ढीला {करते हैं}।
rAsAyanika_1,prakriyA_1,sAmAnyawaH_1,kaNa_1,bIca_1,baMXana_1,DIl+kara_1-wA_hE_1
1,2,3,4,5,6,7
,,,,,,
,,,,,,
2:mod,7:k1,7:krvn,6:r6,4:lwg__psp,7:k2,0:main
,,,,,,
,,,,,,
,,,,,,
affirmative
nil
</sent_id>

<sent_id=Geo_ncert_11stnd_6ch-bk1_0078b>
#तथा विलेय पदार्थों को घुला {देते हैं}।
vileya_1,paxArWa_1,Gula+xe_1-wA_hE_1
1,2,3
,,
,,
2:mod,3:k2,0:main
,,Geo_ncert_11stnd_6ch-bk1_0078a.7:samuccaya 
,,
,,
affirmative
nil
</sent_id>
```
Output: 

- Original Text Container:
    
```bash
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078a> रासायनिक प्रक्रियाएँ सामान्यतः कणों के बीच के बंधन को ढीला {करते हैं}। </sent_id>
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078b> तथा विलेय पदार्थों को घुला {देते हैं}। </sent_id>
```
- Annotated Discourse Container:
```bash
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078a> रासायनिक प्रक्रियाएँ सामान्यतः कणों के बीच के बंधन को ढीला {करते हैं}। </sent_id> समुच्चय <sent_id=Geo_ncert_11stnd_6ch-bk1_0078b> विलेय पदार्थों को घुला {देते हैं}। </sent_id> 
```

    1. Annotated Text will be stored in the `annotated_text` file.
    2. After authentication, you can modify the annotations.
    3. After modification, three new files will be created.



- Modifications in the uploaded file by making copy of it - duplicate_uploaded_file

```bash
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078a>
#रासायनिक प्रक्रियाएँ सामान्यतः कणों के बीच के बंधन को ढीला {करते हैं}।
rAsAyanika_1,prakriyA_1,sAmAnyawaH_1,kaNa_1,bIca_1,baMXana_1,DIl+kara_1-wA_hE_1
1,2,3,4,5,6,7
,,,,,,
,,,,,,
2:mod,7:k1,7:krvn,6:r6,4:lwg__psp,7:k2,0:main
,,,,,,
,,,,,,
,,,,,,
affirmative
nil
</sent_id>

<sent_id=Geo_ncert_11stnd_6ch-bk1_0078b>
#तथा विलेय पदार्थों को घुला {देते हैं}।
vileya_1,paxArWa_1,Gula+xe_1-wA_hE_1
1,2,3
,,
,,
2:mod,3:k2,0:main
,,Geo_ncert_11stnd_6ch-bk1_0078a.7:samAnakAla 
,,
,,
affirmative
nil
</sent_id>
```
- Annotated Discourse Container after modification - annotated_text_after_modification
```bash
<sent_id=Geo_ncert_11stnd_6ch-bk1_0078a> रासायनिक प्रक्रियाएँ सामान्यतः कणों के बीच के बंधन को ढीला {करते हैं}। </sent_id> समानकाल <sent_id=Geo_ncert_11stnd_6ch-bk1_0078b> विलेय पदार्थों को घुला {देते हैं}। </sent_id> 
```

    

