# QTI Quiz Generator

## Overview
This repository contains a Python script for generating QTI v2.1-compliant quiz files from a CSV input. It creates individual XML files for each question, organizes them into a directory structure, and generates a corresponding `imsmanifest.xml` file to ensure compatibility with QTI-based systems.

## Features
- Converts quiz questions from a CSV file into QTI v2.1 XML format.
- Automatically generates directory structures for QTI items.
- Creates a valid `imsmanifest.xml` file to reference all quiz items.
- Flexible input structure to accommodate multiple-choice questions.

## Prerequisites
- Python 3.7 or higher

## Installation
Clone the repository:
   ```bash
   git clone https://github.com/your-username/qti-quiz-generator.git
   cd qti-quiz-generator
   ```

## Usage
1. Prepare a CSV file (`quiz_questions.csv`) with the following structure:

  | Item ID | Title | Question | ChoiceA | ChoiceB | ChoiceC | ChoiceD | Correct Choice |
|---------|-------|----------|---------|---------|---------|---------|----------------|
| Q1      | T1    | Q1_Text  | A1_Text | B1_Text | C1_Text | D1_Text | C              |
| Q2      | T2    | Q2_Text  | A2_Text | B2_Text | C2_Text | D2_Text | C              |

   **Note**: Columns `ChoiceA`, `ChoiceB`, etc., represent answer options. `Correct Choice` should contain the identifier of the correct answer (e.g., `A`, `B`, `C`, or `D`).

2. Run the script:
   ```bash
   python generate_qti_with_manifest.py
   ```

3. The script will generate:
   - A folder named `output_qti` containing:
     - Individual XML files for each question in subdirectories.
     - A `imsmanifest.xml` file referencing all generated items.

## Output Structure
The generated directory structure will look like this:
```
output_qti/
└── Items/
    ├── Item_Q1/
    │   └── Q1.xml
    ├── Item_Q2/
    │   └── Q2.xml
    ...
imsmanifest.xml
```

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author
[Probir Roy](https://github.com/proywm)
