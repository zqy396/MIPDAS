# MIPDAS: Development and Validation Artificial Intelligence-based Model for Standardized Immunophenotype of Bladder Cancer Using Whole Slide Images
MIPDAS is an analysis framework based on deep learning and computational pathology. It consists of three steps: 
1) Hover-Net: Nuclear segmentation and classification;
2) Graph Neural Network: Feature extraction;
3) XGBoost: Constructing immunophenotype.

# Pre-requisites:
The packages required have been provided in the file ```requirements.txt```.
<br>
```pip install -r requirements.txt```

# Abstract
The classification of immunophenotypes in muscle-invasive bladder cancer (MIBC) is critical for predicting immunotherapy response and patient outcomes. We aimed to develop an artificial intelligence (AI)-based MIBC Immunophenotype Diagnostic System (MIPDAS) using computational pathology and evaluate its clinical utility.

This is the official pytorch implementation of MIPDAS. Note that only the Nuclear segmentation and classification step supports batch processing.

# Usage
1) ```Hover```: the implementation of HoVer-Net, which is cloned from the official [implementation](https://github.com/vqdang/hover_net)
2) ```main.py```: main function
3) ```F1_CellSegment.py``` for tile processing generated an exception
4) ```F2_TiatoolJson.py``` for using TIAtool to output json file
5) ```F3_CellSegment.py```: nuclear segmentation and classification by calling Hover.
6) ```F4_FeatureExtract.py```: feature extraction by calling ```WSIGraph.py```.
7) ```F5_Visualization.py``` and ```F6_Visualization.py```: visualization by calling ```utils_xml.py```.
8) ```utils_xml.py```: define some tools to finish visualization.
9) ```WSIGraph.py```: define the process of feature extraction.

1. ```F1_CellSegment.py``` for tile processing generated an exception.

```python main.py qupath --input_dir=your_dir --output_dir=your_dir```

<br>
2. ```F2_TiatoolJson.py``` for using TIAtool to output json file.

```python main.py json --input_dir=your_dir --output_dir=your_dir```
<br>

3. ```F3_CellSegment.py``` for nuclear segmentation and classification.

This step employs [HoVer-Net](https://github.com/vqdang/hover_net) for simultaneous nuclear segmentation and classification. The model is pre-trained based on PanNuke dataset and can be downloaded from [url](https://drive.google.com/file/d/1SbSArI3KOOWHxRlxnjchO7_MbWzB4lNR/view).

```python main.py segment --input_dir=your_dir --output_dir=your_dir```
<br>

4. ```F4_FeatureExtract.py``` for feature extraction:

```python main.py feature --input_dir=your_dir --output_dir=your_dir```
<br>

5. ```F5_FeatureExtract.py``` and ``F6_FeatureExtract.py``` for feature extraction:

```python main.py visual --input_dir=your_dir --output_dir=your_dir```
<br>
```python main.py visual --input_dir=your_dir --output_dir=your_dir```














