from openai import OpenAI
from questions.tasks import compress_text_whitespace
from decouple import config
from celery import shared_task

_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config("OPENROUTER_API_KEY")
)

def _generate_response(messages, options=None):
    if options is None:
        options = {}

    filtered_options = {k: v for k, v in options.items() if k not in ['top_k']}
    
    try:
        # به دلیل غیرفعال شدن مدل gpt-oss 120b مجبور شدم از gpt-oss 20b استفاده کنم
        response = _client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=messages,
            stream=False,
            **filtered_options
        )
        return response.choices[0].message.content or "__AI_ERROR__"
    except Exception:
        return "__AI_ERROR__"

@shared_task
def detect_difficulty(text: str , template_name : str):
    text_for_ai = compress_text_whitespace(text)[:1500]
    
    options = {
        "temperature": 0.0,
        "seed": 42
    }

    messages = [
        {
            "role": "system",
            "content": """You are an AI assistant whose only task is to estimate the difficulty of math questions.

Instructions:

- Analyze the user's text and detect whether it contains one or more mathematical exercises or questions.
- A valid math sample includes any mathematical expression or exercise, even if it is very simple, such as:
  - 10 + 4
  - 7 × 8
  - x² + 2x = 0
  - \(\int x^2 dx\)
  - Geometry, algebra, calculus, statistics, probability, trigonometry, arithmetic, or any other mathematics content.
- The input may be plain text, LaTeX, OCR output, or multiple questions.

If the input contains at least one mathematical exercise, estimate its overall difficulty on a scale from 1 to 10 by considering:
- Mathematical concepts involved.
- Logical complexity.
- Estimated solving effort for an average student.

Your response must contain only one value in the exact format:

X/10

Examples:
3/10
7/10
10/10

Do not solve the questions.
Do not explain your reasoning.
Do not output anything except the rating.

If the input contains no mathematical content at all, reply exactly with:

فایل شما به عنوان یک نمونه سوال معتبر نیست""",
        },
        {
            "role": "user",
            "content": text_for_ai
        }
    ]

    return {"response" : _generate_response(messages, options) , "template_name" : template_name , "text" : text}

@shared_task
def generate_same_questions(text : str , template_name : str):
    text_for_ai = compress_text_whitespace(text)[:5500]
    
    options = {
        "temperature": 0.3,
        "seed": 42
    }

    messages = [
        {
            "role": "system",
            "content": """You are an AI assistant that only generates similar mathematics exercises.

Task:

1. Analyze the user's text.
2. Treat every non-empty line containing mathematical expressions, equations, formulas, variables, numbers with mathematical operators (+, -, ×, *, /, =, ^, %, etc.), or numbered exercises as a valid mathematics exercise, even if it has no question mark or instruction.
3. If the input contains no mathematics exercises, expressions, equations, or formulas, respond exactly with:
فایل شما به عنوان یک نمونه سوال معتبر نیست
4. Otherwise, generate exactly 20 new mathematics exercises with similar topics, style, structure, and approximate difficulty.

Rules:

- Output only the 20 generated exercises.
- Do not solve or explain anything.
- Do not answer user questions.
- Use MathJax only:
  - Inline: \( ... \)
  - Display: \[ ... \]
- Never use `$...$` or `$$...$$`.
- Number the exercises from 1 to 20.
- Put each exercise inside its own `<p>...</p>` block.
- Do not output any other text.""",
        },
        {
            "role": "user",
            "content": text_for_ai
        }
    ]

    return {"response" : _generate_response(messages, options) , "template_name" : template_name , "text" : text}

@shared_task
def solve_math_text(text : str , template_name : str):
    text_for_ai = compress_text_whitespace(text)
    
    options = {
        "temperature": 0.0,
        "seed": 42
    }

    messages = [
        {
            "role": "system",
            "content": """You are an AI assistant whose only task is to generate answer sheets for mathematics exercises.

Instructions:

- Analyze the user's input and detect all mathematical exercises or questions.
- A valid math input includes any arithmetic, algebra, geometry, trigonometry, calculus, probability, statistics, equations, inequalities, word problems, or LaTeX mathematics, even if it contains only simple expressions such as:
  - 10 + 4
  - x² + 2x = 0
  - \(\frac{2}{3}\)
- The input may come from OCR, plain text, or LaTeX and does not need perfect formatting.

If at least one mathematical exercise is found:
- Generate only the answers in the same order as the input.
- Number the answers sequentially.
- Do not omit any detected question.
- Do not provide explanations, steps, hints, or commentary.
- Use MathJax-compatible LaTeX only:
  - Inline: \(...\)
  - Display: \[...\]
  - Never use $...$ or $$...$$.
- Put each answer inside its own `<p>...</p>` block.

Example:

<p>1. \(5\)</p>
<p>2. \(x=3\)</p>

If the input contains no mathematical content at all, reply exactly with:

فایل شما شامل سوال ریاضی معتبر نیست""",
        },
        {
            "role": "user",
            "content": text_for_ai
        }
    ]

    return {"response" : _generate_response(messages, options) , "template_name" : template_name , "text" : text}