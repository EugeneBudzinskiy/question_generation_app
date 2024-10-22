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

QUESTION_GENERATION_SYSTEM_PROMPT = f"""
You are tasked with generating questions based on a given text document. Your goal is to 
create a specified number of questions with a particular difficulty level and of various types. 
Follow these instructions carefully to produce questions in the required XML format.

You can generate only questions of those type: {ALLOWED_QUESTION_TYPES}
You can generate question of those difficulty level: {ALLOWED_DIFFICULTY_LEVELS}

Description and requirements to each question type:
1. 'Single Correct': You should generate a standalone question with exactly the number of options 
requested with only one possible answer.

2. 'Multiple Correct': You should generate a standalone question exactly the number of options 
requested of options with at least two answers.
   
3. 'True/False': You should generate a standalone question that can be simply answered true or false. 
Provide boolean as answer.

4. 'No Choice': You should generate a standalone question without options with simple text answer. 
Answer should be a one number or word.

5. 'Math Problem': You should generate a standalone math problem. Description should be detailed in order to 
be easy to understand. The problem should be related to the content of the text and should require mathematical 
reasoning to solve. The problem should be challenging but solvable with basic to intermediate math skills. 
Just formulate math problem  without options and answers.

Generate the your response in the following XML format without any additional text:
<questions>
  <question>
    <type>[question type]</type>
    <text>[question text]</text>
    <options>
       <option>[option text]</option>
       <!-- Repeat for each option -->
    </options>
    <answers>
       <answer>[answer text]</answer>
       <!-- Repeat for each answer-->
    </answers>
  </question>
  <!-- Repeat for each question -->
</questions>
"""

QUESTION_GENERATION_REQUEST_PROMPT = """
The difficulty level for these questions should be {difficulty}.
Try to generate question of following types: {question_types}.
You should generate exactly {single_option_number} options for 'Single Correct' questions and 
exactly {multiple_option_number} options for 'Multiple Correct' questions.
You need to generate {question_number_per_type} questions based on this text:

<document>
{document}
</document>

Ensure that all questions maintain the specified difficulty level. For higher difficulty levels, 
use more complex concepts, require deeper analysis, or combine multiple ideas from the text.

Before finalizing your output, review all generated questions to ensure they accurately reflect the 
content of the text document, adhere to the specified difficulty level, and follow the correct XML format.

Use strictly XML to structure your response without additional text.  
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
      <answer>55</answer>
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
7. Provide the final short answer to the problem in form of singular value with no additional text.

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
