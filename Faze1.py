import re

# تعریف توکن‌ها و الگوهای Regex
# ترتیب قرارگیری مهم است (مثلاً کلمات کلیدی قبل از ID باشند)
TOKEN_SPECIFICATION = [
    ('FUNK',       r'\bfunk\b'),
    ('INT',        r'\bint\b'),
    ('AS',         r'\bas\b'),
    ('VECTOR',     r'\bvector\b'),
    ('FOR',        r'\bfor\b'),
    ('TO',         r'\bto\b'),
    ('LEN',        r'\blength\b'),
    ('BEGIN',      r'\bbegin\b'),
    ('ENDFOR',     r'\bendfor\b'),
    ('RETURN',     r'\breturn\b'),
    ('NUMBER',     r'\d+'),
    ('ID',         r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('DBL_COLON',  r'::'),
    ('EQ',         r'='),
    ('PLUS',       r'\+'),
    ('LESS_THAN',  r'<'),
    ('GREATER_THAN', r'>'),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LCURLYEBR',  r'\{'),
    ('RCURLYEBR',  r'\}'),
    ('LSQUAREBR',  r'\['),
    ('RSQUAREBR',  r'\]'),
    ('SEMI_COLON', r';'),
    ('NEWLINE',    r'\n'),           # برای مدیریت شماره سطر
    ('SKIP',       r'[ \t]+'),       # نادیده گرفتن فضاهای خالی
    ('MISMATCH',   r'.'),            # کاراکترهای غیرمجاز
]

def tokenize(code):
    # ترکیب تمام Regexها در یک عبارت واحد
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    line_num = 1
    line_start = 0
    
    # برای مدیریت کامنت‌های تودرتو، بهتر است قبل از توکنایز کردن، 
    # یک پیش‌پردازش برای حذف کامنت‌ها انجام دهیم (در ادامه توضیح می‌دهم)
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1
        
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            print(f'خطا: کاراکتر غیرمجاز {value} در سطر {line_num}')
            continue
            
        yield {
            'line': line_num,
            'column': column,
            'token': kind,
            'value': value
        }

# تست برنامه با ورودی نمونه
sample_code = """funk <int> sum(numlist as vector) {
    result :: int = 0;
}"""

print(f"{'Line':<8} | {'Column':<8} | {'Token':<15} | {'Value'}")
print("-" * 50)
for token in tokenize(sample_code):
    print(f"{token['line']:<8} | {token['column']:<8} | {token['token']:<15} | {token['value']}")
