




from agents.framework_analyzer import framework_analyzer


with open("docs/uml_diagram.mmd", "r", encoding="utf-8") as f:
        mermaid_code = f.read()



print(framework_analyzer(mermaid_code))