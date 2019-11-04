# ClinicalRegex

## Install dependencies

```
sudo easy_install pip
```
```
pip3 install -r requirements.txt
```

## Start Program
```
python3 src/main.py
```

## Annotation pipeline
![img](ClinicalRegex.png)

- Please hit 'select' file
- Please select a RPDR format or CSV format file to be searched by the program.
- Select the column names of patient id and report text for CSV format file
- Type in the label names and keywords/regex (separated by ',') and press the "Run Regex" button. If you only have one label, leave the Label_2, Label_3 unclick/blank
- To modify the highlighted text spans, please select the label radiobutton and select the note text, and then hit "Add" or "Delete"
- The program will then go through each note. Press "Save" or hit "Next" at the top of the screen 
- Repeat this through each note until the end of the file 

- You can also select an output CSV file to continue the annotation by pressing the "Load annotation" button

## Output format

| patient id  | report text | L1_spans     | L1_text         | L2_spans, if applicable | .... |
| ----------- | ----------- | ----------------- | -------------------- | ---------------------------- | ---- |
| 12345678    | sample text | 1,5\|15,20\|100,300 | cancer\|CANCER\|Carcinoma | 200,250                      | .... |
