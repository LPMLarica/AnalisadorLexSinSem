import re


token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),   
    ('ASSIGN',   r'='),             
    ('ID',       r'[A-Za-z_]\w*'),  
    ('OP',       r'[+\-*/]'),      
    ('SKIP',     r'[ \t]+'),       
    ('MISMATCH', r'.'),            
]

token_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)

def lexer(code):
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', value))
        elif kind == 'ID':
            tokens.append(('ID', value))
        elif kind == 'ASSIGN':
            tokens.append(('ASSIGN', value))
        elif kind == 'OP':
            tokens.append(('OP', value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Erro Léxico: caractere inválido '{value}'")
    return tokens


def parser(tokens):
    if len(tokens) < 3:
        raise SyntaxError("Erro Sintático: sentença incompleta")
    
    if tokens[0][0] != 'ID':
        raise SyntaxError("Erro Sintático: a sentença deve começar com um identificador")
    if tokens[1][0] != 'ASSIGN':
        raise SyntaxError("Erro Sintático: esperado '=' após o identificador")
    if tokens[2][0] not in ['ID', 'NUMBER']:
        raise SyntaxError("Erro Sintático: valor esperado após '='")


    for i in range(3, len(tokens), 2):
        if i >= len(tokens):
            break
        if tokens[i][0] != 'OP' or (i+1 >= len(tokens)) or tokens[i+1][0] not in ['ID', 'NUMBER']:
            raise SyntaxError("Erro Sintático: expressão aritmética mal formada")
    return True


def semantic_analyzer(tokens, symbol_table):
    lhs = tokens[0][1]
    rhs = tokens[2:]
    
    
    for i in range(0, len(rhs), 2):
        if rhs[i][0] == 'ID':
            if rhs[i][1] not in symbol_table:
                raise NameError(f"Erro Semântico: variável '{rhs[i][1]}' não declarada")
    
    
    symbol_table[lhs] = "number"

def main():
    symbol_table = {'y': 'number'} 

    # Entrada propositalmente com erros: 'x = y + $'
    code = "x = y + $"

    try:
        print("Analisando código:", code)
        tokens = lexer(code)
        print("Tokens:", tokens)
        parser(tokens)
        semantic_analyzer(tokens, symbol_table)
        print("Análise concluída com sucesso.")
    except Exception as e:
        print("Erro encontrado:", e)

if __name__ == "__main__":
    main()