2023-02-27

TESTLINK at IberLEF2023 (https://e3c.fbk.eu/testlinkiberlef) is a relation extraction task based on clinical cases taken from the E3C corpus, i.e. on Spanish and Basque written documents 
reporting statements of a clinical practice (thus including, for example, the reasons for a clinical visit, the physical exams undertaken, the assessment of the patient’s diagnosis and subsequent treatments).
The task consists in identifying test results and measurements and linking them to the textual mentions of the laboratory tests and measurements from which they were obtained.


training.txt

The training.txt file contains the 81 documents from the training set for the TESTLINK task in IberLEF 2023. The documents are in Pubtator format:
-	Identifier (e.g. 100002)
-	Separator (|t|)
-	Document text
-	Clinkart relations (e.g. 100002	REL	988-997	979-987	145 mg/dl	Glucemia)


Data Licence

All the data in this folder is available under CC-BY-NC-4.0 licence.


References

Bernardo Magnini, Begoña Altuna, Alberto Lavelli, Manuela Speranza, Roberto Zanoli, 2020. 
The E3C Project: Collection and Annotation of a Multilingual Corpus of Clinical Cases. 
Proceedings of the Seventh Italian Conference on Computational Linguistics, CLiC-It 2020. Bologna, Italy, March 1-3, 2021. 
http://ceur-ws.org/Vol-2769/paper_55.pdf 
