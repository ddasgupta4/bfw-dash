# Creating a Fairness Tool for Bias in Facial Recognition
Alice Loukianova, Dylan Dasgupta, Joseph Robinson, Rohan Krishnamurthi, and William Cutler

Our bios can be found <a href="bio.md">here</a>.
# Overview

Facial recognition (FR) technology is an advanced form of biometric security that involves assessing one’s face and comparing it to a known database to form an identity. This software has become increasingly popular in recent years, as the need for more complex security measures has become essential. While this concept has been around since the mid-1900s, it has only become so popular in recent years. However, with this intricate technology comes complicated issues. A major issue that has remained prevalent in the technology is a bias towards certain users because of their demographic. We will demonstrate this bias, and look at ways to eliminate it to create a nondiscriminatory evaluation available for all FR users. It is unfair some users are subject to experience more errors than others, due to their diverse backgrounds.


[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger)      [![Gem Version](http://img.shields.io/gem/v/badgerbadgerbadger.svg?style=flat-square)](https://rubygems.org/gems/badgerbadgerbadger) 
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org) 


![Dashboard UI](assets/DashBoard.png)


---

## Table of Contents 

- [Installation](#installation)
- [Usage](#usage)
- [Abstract](#abstract)
- [Key Terms](#key terms)
- [Features](#features)
- [Documentation](#documentation)
- [License](#license)

---

## Installation
Clone this repository:
```bash
git clone https://github.com/ddasgupta4/bfw-dash.git
```

Download requirements:
```bash
pip install requirements.txt
```


## Usage
To run the dashboard navigate to the directory and execute the following command:

```bash
python app.py
```

---
# Abstract
We work to reveal the bias present in the current FR technology, and create a means of eliminating the bias in the form of a fairness tool, our dashboard. We have utilized a Balanced Faces in the Wild (BFW) database that equally represents each ethnicity and gender, so the faces being looked at for identification will have no bias in itself. This database is key to an equal background, to begin with, as we represent ethnicities through four subgroups, and genders through male and female. The four subgroups regarding ethnicity are: Asian, black, Indian, and white. These subgroups are used to display how the bias differs between each combination of black males, black females, Asian males, and so forth. 

Gender and Race Database Statistics: Statistics of the Balanced Faces in the Wild (BFW) [1] database, grouped here by subgroup and a specific value. There are a million pairs total under analysis, with a constant 30,000 positive pairs being assessed for each gender under said subgroup. Overall, F performs inferior to M for I and W, while M performs inferior to W for A and B.

# Key Terms
False positive: Occurs when two faces are incorrectly identified as an identical match, AKA type 1 error

False negative: Occurs when two faces of the same person are not identified as an identical match, AKA type 2 error

SDM Curve: Signal detection model curve plots a distribution of scores, using imposter and genuine scores against each other to highlight the differences between accurate and incorrect facial identifications.

DET Curve: Detection error trade off curve plots the false negative rate (FNR) as a function of the false positive rate (FPR), displaying the tradeoff between the sensitivity with FPR and specificity with FNR.

ROC Curve: Receiever operating characteristic curve plots the true positive rate (TPR) against the false positive rate (FPR). It is a probability curve yielding the most ideal values in the top left, where FPR = 0 and TPR = 1. 

# Features
Our dashboard tool is universal, meaning anyone can learn how to use it and anyone can import their own unique dataset. It will use the data given to create various plots that include SDM curves, DET curves, ROC curves, and violin plots. Not only will a user's data be cleanly displayed in different visuals, but it will be assessed for bias. Each user will mst likely have a different dataset, meaning the bias will vary from set to set. Rather than having to manually assess your own data for bias, the dashboard will algorithimically do it for you. Another great visualization tool is the confusion matrix, which will display the error rate between stated subgroups for the entire dataset. By breaking it down to the intra-subgroup level we can assess which subgroups are confused the most, and which subgroups are confused by each other most. That is to say: if white males are confused with white males or white females, or even other subgroups. This way, the bias can be truly understood and it becomes evident where the data is skewed. 

A closer look at the plots can be found <a href="plots.md" target="_blank">here</a>.

---


## Documentation
- The research paper supporting this dashboard can be found <a href="assets/A Fairness Tool for Bias in FR Updated.pdf"  target="_blank">here</a>.
- This dashboard was presented at Northeastern University's RISE 2020.
    - The poster presented can be found <a href="assets/RISE Poster.pdf"  target="_blank">here</a>.
    - A recording of our presentation can be found <a href="https://web.microsoftstream.com/video/849f7262-b45e-41d7-9dd4-91a02dfe18cd" target="_blank">here</a>. 
- Going into more detail on code and technologies used
- This dashboard was produced as an extension of the work shared at https://github.com/visionjo/facerec-bias-bfw

---

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
