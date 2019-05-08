# Temporal Relation Annotation

This is temporal annotation project, tailored to the annotation of economic news. The annotation guidelines are many ways are a streamlining of TimeML, from which they draw deep inspiration.


This repository includes three things: the set-up files for annotation, a set of data annotated by three annotators, and the code needed to run our baseline classifier which was trained on the preliminary annotations. 

The project set-up files for use with [MAE](https://keighrim.github.io/mae-annotation/), which includes: 
+ MAE Set-up File (temporal_annoation.dtd)
+ Batched data of 100 articles in the annotation_data folder. 
+ The full source data as Full-Economic-News_DFW-839861.csv, for reference. 

The set of data annotated by three annotators can be found in raw_annotation_data, in subdirectories organized by annotator. 

**Code**

The code for running our classifier should be run in the following order. 

Converts the source csv to batched xml files for use in MAE:

+ csv_xml.py

Extract tags and their position information from MAE-generated XML files:

+ process_tags.py

Add “unspecified” tags to untagged adjacent pairs:

+ unspecified_generator.py

Read from the processed tags to calculate IAA scores by tag type:

+ IAA.py

Select shared tags to create standard train/test datasets: 

+ build_gold.py

Obtain bag-of-words and tag features from standard datasets:

+ extract_features.py

Implement a logistic regression model for link classification, train, and evaluate:

build_model.py

**Datasets**

annotation_data: all data from the news corpus

annotated_data: 

+ Starting with “NEWS” and ending with annotator initials: annotated files from MAE
+ Starting with number and ending with annotator initials: cleaned tag sets

raw_annotated_data: original files from annotators

silver.txt: all unique TLINK tags

features_silver.txt: feature vectors made from the silver dataset 



