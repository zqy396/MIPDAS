# MIPDAS: Development and Validation Artificial Intelligence-based Model for Standardized Immunophenotype of Bladder Cancer Using Whole Slide Images
MIPDAS is an analysis framework based on deep learning and computational pathology. It consists of two steps: 1) Hover-Net: Nuclear segmentation and classification; 2) Graph Neural Network: Feature extraction; 3) XGBoost: Constructing immunophenotype.

# Pre-requisites:
* Python (3.8.13)
* h5py (3.6.0)
* openslide (version 3.4.1)
* opencv (version 4.5.5)
* pillow (version 6.2.1)
* Pytorch (version 1.12.1)
* scikit-learn (version 1.0.2)
* matplotlib (version 3.5.2)
* seaborn (version 0.11.2)

# Abstract
The classification of immunophenotypes in muscle-invasive bladder cancer (MIBC) is critical for predicting immunotherapy response and patient outcomes. We aimed to develop an artificial intelligence (AI)-based MIBC Immunophenotype Diagnostic System (MIPDAS) using computational pathology and evaluate its clinical utility.

This is the official pytorch implementation of MIPDAS. Note that only the Nuclear segmentation and classification step supports batch processing.

# Data prepare
1. '''F1_CellSegment.py''' for nuclear segmentation and classification:

This step employs HoVer-Net for simultaneous nuclear segmentation and classification. The model is pre-trained based on PanNuke dataset and can be downloaded from url.

Provide your WSI files as input. We use '''.svs''' WSI files in our work, and theoretically it supports all WSI file formats allowed by HoVer-Net. The step outputs a '''.json''' file including all information on nuclear segmentation and classification for each sample.






