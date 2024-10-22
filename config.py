DATABASE_PATH = "database.db"

ALLOWED_FILE_TYPES = ["txt", "pdf", "docx"]
ALLOWED_DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
ALLOWED_QUESTION_TYPES = ["True/False", "Single Correct", "Multiple Correct", "No Choice", "Math Problem"]
DIFFICULTY_QUESTION_TYPE_DISTRIBUTION = {
    "Easy": {"True/False": 4, "Single Correct": 4, "Multiple Correct": 2, "No Choice": 1, "Math Problem": 1},
    "Medium": {"True/False": 1, "Single Correct": 2, "Multiple Correct": 4, "No Choice": 2, "Math Problem": 1},
    "Hard": {"True/False": 1, "Single Correct": 1, "Multiple Correct": 2, "No Choice": 4, "Math Problem": 4}
}

ANTHROPIC_MODEL_NAME = "claude-3-haiku-20240307"

TEXT_CHUNK_SIZE = 4096
TEXT_CHUNK_OVERLAP = 256


QUESTION_GENERATION_PROMPT = """
You are an expert question generator tasked with creating a set of questions based on a given text document. 
Your goal is to produce high-quality, varied questions that accurately reflect the content of the document 
while adhering to specific requirements.

First, carefully read the following document:

<document>
{document}
</document>

Now, you will generate questions based on this document. Here are the parameters for question generation:

<allowed_question_types>
{allowed_question_types}
</allowed_question_types>

<allowed_difficulty_levels>
{allowed_difficulty_levels}
</allowed_difficulty_levels>

<difficulty>
{difficulty}
</difficulty>

<question_types>
{question_types}
</question_types>

<single_option_number>
{single_option_number}
</single_option_number>

<multiple_option_number>
{multiple_option_number}
</multiple_option_number>

<question_number_per_type>
{question_number_per_type}
</question_number_per_type>

Instructions for each question type:

1. 'Single Correct': Generate a question with exactly <single_option_number> options, where only one is correct.
2. 'Multiple Correct': Generate a question with exactly <multiple_option_number> options, where at least two are 
correct.
3. 'True/False': Generate a statement that can be answered as true or false. Provide the boolean answer.
4. 'No Choice': Generate a question with a simple text answer (one number or word).
5. 'Math Problem': Generate a detailed math problem related to the document content. The problem should be challenging 
but solvable with basic to intermediate math skills. Do not provide options or answers for this type.

For each question, follow these steps:

<question_creation_process>
1. Identify a key concept or piece of information from the document to base the question on.
2. Determine the most appropriate question type from the allowed types.
3. Consider the specified difficulty level (<difficulty>) and how to incorporate it into the question.
4. Draft the question text, ensuring it's clear, concise, and matches the chosen difficulty level.
5. For 'Single Correct' and 'Multiple Correct' questions:
   a. Generate the required number of options (<single_option_number> or <multiple_option_number>).
   b. Ensure options are distinct, plausible, and align with the difficulty level.
   c. For 'Multiple Correct', make sure at least two options are correct.
6. For 'True/False' questions:
   a. Craft a statement that requires understanding of the document to evaluate.
   b. Determine if the statement is true or false based on the document.
7. For 'No Choice' questions:
   a. Ensure the answer is concise (one number or word) and directly related to the document.
8. For 'Math Problem' questions:
   a. Create a detailed problem description with context from the document.
   b. Include all necessary information for solving the problem.
   c. The problem should be related to the content of the text and should require mathematical reasoning to solve. 
   d. The problem should be challenging but solvable with basic to intermediate math skills
   c. Ensure the problem complexity matches the specified difficulty level.
9. Review the question to ensure it:
   a. Accurately reflects the document content.
   b. Meets the specified difficulty level.
   c. Is clear and unambiguous.
10. Refine the question if necessary, adjusting language or complexity to better fit the requirements.
</question_creation_process>

After completing the question creation process for each question, format your output in the following XML structure:

<questions>
  <question>
    <type>[question type]</type>
    <text>[detailed question text]</text>
    <options>
      <option>[option text]</option>
      <!-- Repeat for each option if applicable -->
    </options>
    <answers>
      <answer>[answer text]</answer>
      <!-- Repeat for each correct answer if applicable -->
    </answers>
  </question>
  <!-- Repeat for each question -->
</questions>

Ensure that you generate exactly <question_number_per_type> questions for each type specified in <question_types>. 
Maintain the specified difficulty level throughout, using more complex concepts or requiring deeper analysis 
for higher difficulty levels.

Before finalizing your output, review all generated questions to ensure they:
1. Accurately reflect the content of the text document
2. Adhere to the specified difficulty level
3. Follow the correct XML format
4. Provide sufficiently detailed descriptions, especially for 'Math Problem' types

Remember to use strictly XML to structure your response without any additional text.
"""


MATH_SOLVER_EXAMPLE = """
<examples>
  <example>
    <math_problem>
      Calculate the sum of numbers from 1 to 10
    </math_problem>
    <ideal_output>
      <thinking>
        Problem Analysis:
        
        We need to calculate the sum of numbers from 1 to 10.
        
        Mathematical Concepts:
        - Arithmetic sequence
        - Summation
        
        Solution Approach:
        We can use a Python loop to iterate through the numbers and sum them up.
        
        Step-by-step Solution:
        1. Initialize a variable to store the sum
        2. Iterate through numbers 1 to 10
        3. Add each number to the sum
        4. Print the result
        
        Python code:
        ```python
        
        total = 0
        
        for i in range(1, 11):
            total += i
            
        print(f\"The sum of numbers from 1 to 10 is: {{total}}\")
        
        ```
        
        Code output:
        The sum of numbers from 1 to 10 is: 55
      </thinking>
      <answer>55.0</answer>
    </ideal_output>
  </example>
</examples>
"""

MATH_SOLVER_PROMPT = """
You are an AI assistant specialized in solving mathematical problems. Your task is to solve the given 
math problem using a combination of Chain of Thought (CoT) reasoning and Python code for calculations. 

Here's the math problem you need to solve:

<math_problem>
{math_problem}
</math_problem>


Please follow these steps to solve the problem:

1. Analyze the problem and identify key components.
2. Determine the mathematical concepts involved.
3. Plan the solution approach.
4. Break down the solution into smaller steps.
5. Write Python code to perform the necessary calculations.
6. Execute the Python code and include the output.
7. Provide the final answer to the problem as a float with no additional text.

Format your output as follows:

<thinking>
Problem Analysis:
[Identify key components of the problem]

Mathematical Concepts:
[List the relevant mathematical concepts]

Solution Approach:
[Outline the planned approach]

Step-by-step Solution:
[Break down the solution into smaller steps]

Python code:
```python
[Your Python code here]
```

Code output:
[Include the actual output from executing the Python code]

</thinking>

<answer>
[Provide the concise final answer to the problem]
</answer>

Important notes:
- Ensure that you actually execute the Python code and include its output in your response.
- Your solution should demonstrate clear, logical reasoning throughout the process.

Now, please solve the given math problem using this approach.
"""
