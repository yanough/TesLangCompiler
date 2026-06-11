import re

# لیست توکن‌ها (همان قبلی)
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
    ('NEWLINE',    r'\n'),
    ('SKIP',       r'[ \t]+'),
    ('MISMATCH',   r'.'),
]

def remove_comments(code):
    """
    این تابع کامنت‌های تودرتو را با فضای خالی جایگزین می‌کند 
    تا سطر و ستون توکن‌های واقعی تغییر نکند.
    """
    output = []
    i = 0
    depth = 0  # شمارنده برای مدیریت تودرتویی
    
    while i < len(code):
        # چک کردن شروع کامنت /*
        if i + 1 < len(code) and code[i:i+2] == '/*':
            depth += 1
            output.append('  ') # جایگزین کردن /* با دو فضا
            i += 2
        # چک کردن پایان کامنت */
        elif i + 1 < len(code) and code[i:i+2] == '*/':
            if depth > 0:
                depth -= 1
                output.append('  ') # جایگزین کردن */ با دو فضا
                i += 2
            else:
                # اگر */ بدون شروع بیاید، آن را کاراکتر عادی فرض می‌کنیم یا خطا می‌دهیم
                output.append(code[i])
                i += 1
        else:
            # اگر داخل کامنت هستیم، کاراکتر را با فضای خالی (یا اینتر) جایگزین می‌کنیم
            if depth > 0:
                if code[i] == '\n':
                    output.append('\n') # اینتر را نگه می‌داریم تا شماره سطر خراب نشود
                else:
                    output.append(' ')
            else:
                output.append(code[i])
            i += 1
            
    if depth > 0:
        print("هشدار: کامنت بسته نشده است!")
        
    return "".join(output)

def tokenize(code):
    # ابتدا کامنت‌ها را پاک می‌کنیم
    clean_code = remove_comments(code)
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
    line_num = 1
    line_start = 0
    
    for mo in re.finditer(tok_regex, clean_code):
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
            # نادیده گرفتن کاراکترهای خالی که جایگزین کامنت شده‌اند
            if value.strip() == '': continue 
            print(f'خطا: کاراکتر غیرمجاز {value} در سطر {line_num} ستون {column}')
            continue
            
        yield {
            'line': line_num,
            'column': column,
            'token': kind,
            'value': value
        }

# --- تست با کامنت تودرتو ---
sample_code = """funk <int> sum /* این یک کامنت /* تودرتو */ است */ (numlist as vector) {
    result :: int = 0; /* کامنت معمولی */
}"""

print(f"{'Line':<8} | {'Column':<8} | {'Token':<15} | {'Value'}")
print("-" * 55)
for token in tokenize(sample_code):
    print(f"{token['line']:<8} | {token['column']:<8} | {token['token']:<15} | {token['value']}")
