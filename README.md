# Python Compiler For CutePy
This project is implemented by the undergraduate students: -Vasileios Ioannis Bouzampalidis, -Alexandros Agapitos Christodoulou
For the Compilers course MYY802 of the Undergraduate Program in Computer Science And Engineering course of the University of Ioannina.

## Main Objective:
This project is aimed at creating a custom compiler for the custom-made CutePy programming language with unique grammar rules and syntax. The main goal of this project is to translate CutePy code into an assembly executable file, enabling it to run on RISC-V architecture. Using the techniques shown below, it facilitates the execution and debugging of CutePy programs by providing a reliable and efficient compilation process.

## Key Features:
- **Lexical Analysis:** Tokenizes the CutePy source code to identify keywords, operators, delimiters, and other syntactic elements.
- **Syntax Analysis:** Parses the tokenized code to ensure it adheres to the CutePy grammar rules.
- **Intermediate Code Generation:** Translates the parsed code into intermediate representations.
- **Error Handling:** Provides detailed error messages for easier debugging.

## Technical Details:
**Programming Language:** The compiler is written in Python, leveraging its robust libraries and tools for string manipulation, parsing, and more.
**Integrated Development Environment (IDE):** Development and testing of the compiler were conducted using Visual Studio Code.

## To Run the Program:
python cutePy_4744_4839.py your_source_file.cpy. 
Or use an existing test provided in the folder src/tests.
