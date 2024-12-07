class XMLParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.errors = []
        self.fixes = []

    def extract_tag(self, line, start):
        # Extract tag from line
        tag = ""
        for char in line[start:]:
            if char == ' ' or char == '>':
                break
            elif char == '<':
                continue
            tag += char
        return tag
    
    def check_consistency(self):
        # Check XML for mismatched tags
        self.errors = []
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            stack = []
            for i, line in enumerate(lines):
                for j, char in enumerate(line):
                    if char == '<':
                        tag = self.extract_tag(line, j)
                        
                        if tag[0] != '/':
                            stack.append(tag)
                        else:
                            if not stack:
                                self.errors.append((i, j, "Missing opening tag for " + tag[1:]))
                                self.fixes.append((i, j - 1, "<" + tag[1:] + ">"))
                            else:
                                if stack[-1] == tag[1:]:
                                    stack.pop()
                                else:
                                    self.errors.append((i, j, "Missing closing tag for " + stack[-1]))
                                    self.errors.append((i, j, "Missing opening tag for " + tag[1:]))
                                    self.fixes.append((i, j - 1, "</" + stack[-1] + ">"))
                                    self.fixes.append((i, j - 1, "<" + tag[1:] + ">"))
        
        return len(self.errors)

    def fix_errors(self):
        #Fix XML errors
        if not self.errors:
            print("No errors to fix!")
        else:
            # iterate through fixes and errors backwards
            for i in range(len(self.errors) - 1, -1, -1):
                error = self.errors[i]
                fix = self.fixes[i]
                with open(self.file_path, 'r') as file:
                    lines = file.readlines()
                    lines[error[0]] = lines[error[0]][:error[1]] + '(' + error[2] + ')' + ' ' + fix[2] + lines[error[0]][error[1]:]
                # open new file with _fixed.xml and write lines
                with open(self.file_path[:-4] + "_fixed.xml", 'w') as file:
                    file.writelines(lines)
            print("Errors fixed!")

# Test the XMLParser class
def test_extract_tag():
    parser = XMLParser("../samples/commented_sample.xml")
    assert parser.extract_tag("<tag>", 0) == "tag"
    assert parser.extract_tag("<tag attribute='value'>", 0) == "tag"
    assert parser.extract_tag("<tag attribute='value'>", 5) == "attribute='value'"
    assert parser.extract_tag("<tag attribute='value'>", 16) == "value"
    assert parser.extract_tag("</tag attribute='value'>", 0) == "/tag"
    
def test_check_consistency():
    parser = XMLParser("../samples/sample.xml")
    assert parser.check_consistency() == 6
    parser = XMLParser("../samples/commented_sample.xml")
    assert parser.check_consistency() == 1

def test_fix_errors():
    parser = XMLParser("../samples/sample.xml")
    parser.check_consistency()
    parser.fix_errors()
    parser = XMLParser("../samples/sample_fixed.xml")
    assert parser.check_consistency() == 0
    
    parser = XMLParser("../samples/commented_sample.xml")
    parser.check_consistency()
    parser.fix_errors()
    parser = XMLParser("../samples/commented_sample_fixed.xml")
    assert parser.check_consistency() == 0
    
    parser = XMLParser("../samples/large_sample.xml")
    parser.check_consistency()
    parser.fix_errors()
    parser = XMLParser("../samples/large_sample_fixed.xml")
    assert parser.check_consistency() == 0

