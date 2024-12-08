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
            elif char == '?' or char == '!':
                return -1
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
                        
                        if tag == -1:
                            continue
                        # Add opening tag to stack
                        if tag[0] != '/':
                            stack.append(tag)
                        else:
                            # If closing tag with no opening tag
                            if not stack:
                                self.errors.append((i, j, "Missing opening tag for " + tag[1:]))
                                self.fixes.append((i, j - 1, "<" + tag[1:] + ">"))
                            else:
                                # If closing tag matches opening tag
                                if stack[-1] == tag[1:]:
                                    stack.pop()
                                else:
                                    self.errors.append((i, j, "Missing closing tag for " + stack[-1]))
                                    self.errors.append((i, j, "Missing opening tag for " + tag[1:]))
                                    self.fixes.append((i, j - 1, "</" + stack[-1] + ">"))
                                    self.fixes.append((i, j - 1, "<" + tag[1:] + ">"))
                                    stack.pop()
        
        # Add errors for any remaining tags in stack
        for tag in stack:
            self.errors.append((-1, -1, "Missing closing tag for " + tag))
            self.fixes.append((-1, -1, "</" + tag + ">"))
        
        return len(self.errors)

    def fix_errors(self):
        #Fix XML errors
        if not self.errors:
            print("No errors to fix!")
        else:
            # iterate through fixes and errors backwards
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for i in range(len(self.errors) - 1, -1, -1):
                    error = self.errors[i]
                    fix = self.fixes[i]
                    if error[0] != -1:
                        lines[error[0]] = lines[error[0]][:error[1]] + '(' + error[2] + ')' + ' ' + fix[2] + lines[error[0]][error[1]:]
                    else:
                        lines.append('(' + error[2] + ')' + ' ' + fix[2] + '\n')    
                # open new file with _fixed.xml and write lines
                with open(self.file_path[:-4] + "_fixed.xml", 'w') as file:
                    file.writelines(lines)
            print("Errors fixed!")


# parser = XMLParser("Your file path here")
# parser.check_consistency()
# parser.fix_errors()
