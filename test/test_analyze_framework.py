
import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)




from agents import framework_analyzer


with open("docs/uml_diagram.mmd", "r", encoding="utf-8") as f:
        mermaid_code = f.read()



print(framework_analyzer(mermaid_code))