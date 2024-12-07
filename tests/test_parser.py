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

