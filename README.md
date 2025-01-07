# Project Overview and Usage Guide

This repository contains a set of scripts and tools for analyzing software vulnerabilities, particularly in the context of the DASP TOP 10 categories. Below is a detailed explanation of each script and its purpose, along with a guide to setting up the environment and using the tools.

------

## **Setup Guide**

### **1. Create a Virtual Environment**

To isolate dependencies and ensure compatibility:

```bash
python -m venv venv
```

### **2. Activate the Virtual Environment**

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

### **3. Install Requirements**

Install all necessary Python dependencies:

```bash
pip install -r requirements.txt
```

## **Scripts Overview**

### **1. Vulnerability Analysis and Classification**

- **`calculate_literature_adherence.py`**
  - Computes adherence to known literature fixing strategies.
- **`calculate_vulnerability_distribution.py`**
  - Analyzes and distributes the fixing commits across the DASP TOP 10 vulnerability categories.
- **`commit_relevance_tagger.py`**
  - Assigns relevance tags and DASP categories to each commit.
- **`discard_not_relevant.py`**
  - Filters out commits deemed irrelevant to the analysis.

------

### **2. Literature Comparison and Novel Fix Identification**

- **`get_literature_untracked_fixes.py`**
  - Identifies commits containing fixes that are not documented in prior literature.
- **`get_new_fixes.py`**
  - Highlights commits containing novel, employable fixes not tracked in prior literature.
- **`is_in_literature_guidelines.py`**
  - Verifies whether a fixing strategy is already documented in the literature.
- **`is_new_fix.py`**
  - Checks if a literature-untracked fixing strategy is employable.

------

### **3. Conflict Resolution Tools**

- **`resolve_conflicts_on_literature_adherence.py`**
  - Facilitates resolving discrepancies in the evaluation of literature adherence.
- **`resolve_conflicts_on_employable_fixes.py`**
  - Aids in resolving disagreements on the employability of literature-untracked fixes.
- **`resolve_conflicts_on_commit_relevance.py`**
  - Helps resolve conflicts regarding the relevance and vulnerability classification of commits.

------

### **4. Statistical and Manual Analysis**

- `kappa.py`
  - Calculates Cohen's Kappa to measure inter-rater agreement for manual analyses.

------
## **Mining**
- The mining folder contains scripts for mining.
## **Sample Dataset**

- `/sample_of_interest/relevant_commits.csv`
  - A dataset containing all evaluated relevant commits.
  - Columns:
    - `Tag`: The DASP category assigned to the commit.
    - `IsInLiteratureGuidelines`: Indicates if the fix was already documented in the literature.
    - `IsEmployableFixTag`: States if the fix was uncovered in the literature and employable.

## **Previous Literature Guidelines**
- `guidelines.md`

## New fixes

* `new_fixes.json`shows the different fixing approaches used by developers that was previously untracked in the academic literature.
