import re

class Lexer():
    def __init__(self):
        self.keywords = set([
            "while", "do", "end", "if", "elseif", "else", "then", "function", "return",
            "for", "in"]
        )
        self.operators = set([
            "<=", ">=", "=", "==", "(", ")", "<", "+", "-", "*", "/", ">", "{", "}", ";", "<>"]
        )

        self.operators_add_like = set(
            ["+", "-"]
        )

        self.operators_mul_like = set(
            ["*", "/"]
        )

        self.operators_compare_like = set(
            ["<=", ">=", "==", ">", "<", "<>"]
        )

        self.open_brackets = set(
            ["("]
        )

        self.close_brackets = set(
            [")"]
        )

        self.block_open_brackets = set(
            ["{"]
        )

        self.block_close_brackets = set(
            ["}"]
        )

        self.operator_sep = set(
            [";"]
        )

        self.operator_assignment = set(
            ["="]
        )


        self.tokens = []
        self.num = 0

    def next(self):
        res = None
        if self.num < len(self.tokens):
            res = self.tokens[self.num]
        self.num += 1

        return res

    def prev(self):
        res = None
        if self.num < len(self.tokens) and self.num > 0:
            res = self.tokens[self.num]

        self.num -= 1
        return res

    def lex(self, source):
        self.num = 0
        chars = list(source)
        self.tokens = []

        while len(chars):
            char = chars[0]

            if char == "\n":
                char = chars.pop(0)
                # self.tokens.append({"type": "NL"})
                continue

            if self.is_operator(''.join(chars[0:2])) or self.is_operator(char):
                type_ = "OP"
                operator = self.extract_operator(chars)
                if operator in self.operators_add_like:
                    type_ += '_addlike'
                elif operator in self.operators_mul_like:
                    type_ += '_mullike'
                elif operator in self.operators_compare_like:
                    type_ += '_comparelike'
                elif operator in self.open_brackets:
                    type_ += '_openbrackets'
                elif operator in self.close_brackets:
                    type_ += '_closebrackets'
                elif operator in self.block_open_brackets:
                    type_ += '_blockopenbrackets'
                elif operator in self.block_close_brackets:
                    type_ += '_blockclosebrackets'
                elif operator in self.operator_assignment: 
                    type_ += '_assignment'
                elif operator in self.operator_sep: 
                    type_ += '_sep'
                
                self.tokens.append({"type": type_, "value": operator})
                continue

            if len(chars) >= 2 and char == "-" and self.is_num(chars[1]):
                del chars[0:1]
                num = "-" + self.extract_num(chars)
                self.tokens.append({"type": "NUMBER", "value": num})
                continue

            if self.is_num(char):
                num = self.extract_num(chars)
                self.tokens.append({"type": "NUMBER", "value": num})
                continue

            if char == "'" or char == '"':
                string = self.extract_str(char, chars)
                self.tokens.append({"type": "STRING", "value": string})
                continue

    
            if self.is_letter(char):
                word = self.extract_word(chars)

                if self.is_keyword(word):
                    self.tokens.append({"type": "KEYWORD", "value": word})
                    continue

                self.tokens.append({"type": "NAME", "value": word})
                continue

            chars.pop(0)
        return self.tokens


    def is_operator(self, char):
        return char in self.operators


    def is_keyword(self, word):
        return word in self.keywords


    def is_letter(self, char):
        return re.search(r'[a-zA-Z]|_', char)


    def is_num(self, char):
        return re.search(r'[0-9]', char)


    def extract_operator(self, chars):
        op = ""
        for letter in chars:
            if not self.is_operator(op+letter):
                break

            op = op+letter
        del chars[0:len(op)]
        return op


    def extract_num(self, chars):
        num = ""

        for letter in chars:
            if not self.is_num(letter) and letter != ".":
                break

            num = num+letter
        del chars[0:len(num)]
        return num


    def extract_str(self, indicator, chars):
        out = ""
        for letter in chars[1:]:
            if letter == indicator:
                break

            out = out+letter
        del chars[0:len(out)+2]
        return out


    def extract_word(self, chars):
        word = ""
        for letter in chars:
            if not self.is_letter(letter) and not re.search(r'([0-9]|_)', letter):
                break

            word = word+letter
        del chars[0:len(word)]
        return word


    def extract_multiline_comment(self, chars):
        string_chars = "".join(chars)
        end_index = string_chars.index("--]]")

        val = string_chars[0:end_index]
        del chars[0:end_index+4]
        return val


    def extract_comment(self, chars):
        string_chars = "".join(chars)
        end_index = string_chars.index("\n")

        val = string_chars[2:end_index]
        del chars[0:end_index]
        return val


    def extract_multiline_str(self, chars):
        string_chars = "".join(chars)
        end_index = string_chars.index("]]")

        val = string_chars[2:end_index]
        del chars[0:end_index+2]
        return val




def main():
    string = """
    { 
        a = 5;
        b = 6;
        a + b < a - b;
    """

    lexer = Lexer()
    self.tokens = lexer.lex(string)

    for t in self.tokens:
        print(t)


if __name__ == '__main__':
    main()