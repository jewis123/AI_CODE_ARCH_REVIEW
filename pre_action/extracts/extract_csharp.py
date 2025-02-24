from typing import List, Tuple

from tree_sitter import Node

# 暂时采用硬编码提取，后续看看有没有通用的提取方式
def extract_class_info(node:Node) ->dict:
    class_info = {
        'class_name': None,
        'class_methods': set(),
        'class_fields': [],  # (name, type)
        'class_properties': [],# (name, type)
        'class_parent': [],
        'class_method_calls': [],
        'class_dependencies': set()# depend types
    }
    
    
    for child in node.children:
        if child.type == 'identifier':
            class_info['class_name'] = child.text.decode('utf-8')
        elif child.type == 'base_list':
            for base_type in child.children:
                if base_type.type == 'identifier':
                    type_name = base_type.text.decode('utf-8')
                    class_info['class_parent'].append(type_name)
                    add_dependency(class_info, type_name)
        elif child.type == 'declaration_list':
            for subchild in child.children:
                if subchild.type == 'property_declaration':
                    type_name= ""
                    type_child = subchild.child_by_field_name('type')
                    if type_child.type == 'identifier':
                        type_name = type_child.text.decode('utf-8')
                        add_dependency(class_info, type_name)
                    elif type_child.type == 'predefined_type':
                        type_name = type_child.text.decode('utf-8')
                    elif type_child.type == 'generic_name':
                        type_name = type_child.text.decode('utf-8')
                        for type_argument in type_child.children:
                            if type_argument.type == 'identifier':
                                add_dependency(class_info, type_argument.text.decode("utf-8"))
                            elif type_argument.type == 'type_argument_list':
                                for type_argument_child in type_argument.children:
                                    if type_argument_child.type == 'identifier':
                                        add_dependency(class_info, type_argument_child.text.decode("utf-8"))
                    elif type_child.type == 'array_type':
                        type_name = type_child.child_by_field_name('type').text.decode('utf-8')
                    else:
                        continue
                    property_name = subchild.child_by_field_name('name').text.decode('utf-8')
                    tp = (property_name, type_name)
                    class_info['class_properties'].append(tp)
                if subchild.type == 'field_declaration':
                    for variable_declaration in subchild.children:
                        if variable_declaration.type == 'variable_declaration':
                            type_child = variable_declaration.child_by_field_name('type')
                            decolator = None
                            for cNode in  variable_declaration.children:
                                if cNode.type == 'variable_declarator':
                                    decolator = cNode
                                    break
                            if type_child.type == 'identifier':
                                type_name = type_child.text.decode('utf-8')
                                add_dependency(class_info, type_name)
                            elif type_child.type == 'predefined_type':
                                type_name = type_child.text.decode('utf-8')
                            elif type_child.type == 'generic_name':
                                type_name = type_child.text.decode('utf-8')
                                for type_argument in type_child.children:
                                    if type_argument.type == 'identifier':
                                        add_dependency(class_info, type_argument.text.decode("utf-8"))
                                    elif type_argument.type == 'type_argument_list':
                                        for type_argument_child in type_argument.children:
                                            if type_argument_child.type == 'identifier':
                                                add_dependency(class_info, type_argument_child.text.decode("utf-8"))
                            elif type_child.type == 'array_type':
                                type_name = type_child.child_by_field_name('type').text.decode('utf-8')
                            else:
                                continue
                            
                            field_name = decolator.child_by_field_name('name').text.decode('utf-8')
                            tp = (field_name, type_name)
                            class_info['class_fields'].append(tp)
                elif subchild.type == 'method_declaration':
                    is_public = False
                    for cchild in subchild.children:
                        if cchild.type == 'modifier':
                            if cchild.text.decode('utf-8') == 'public':
                                is_public = True
                                break
                    if is_public:
                        method_name = subchild.child_by_field_name('name').text.decode('utf-8')
                        return_type = subchild.child_by_field_name('returns')
                        if return_type.type != 'predefined_type':
                            if return_type.type == 'identifier':
                                return_type = return_type.text.decode('utf-8')
                                add_dependency(class_info, return_type)
                            else:
                                for cchild in return_type.children:
                                    if cchild.type == 'identifier':
                                        return_type = cchild.text.decode('utf-8')
                                        add_dependency(class_info, return_type)
                                        break
                        class_info['class_methods'].add(method_name)
                        extract_method_calls(subchild, class_info)
                            

    class_info['class_dependencies'] = list(class_info['class_dependencies'])
    class_info['class_methods'] = list(class_info['class_methods'])
    return class_info

def add_dependency(classInfo:dict, type_name:str):
    if len(type_name) <=1 or type_name.istitle():
        return
    
    classInfo['class_dependencies'].add(type_name)
    
    
def extract_method_calls(node:Node, classInfo:dict)->List[Tuple]:
    method_calls = []

    def traverse(node:Node):
        if node.type == 'invocation_expression':
            function_node = node.child_by_field_name('function')
            if function_node.type == 'identifier':
                return
            
            exp_node = function_node.child_by_field_name('expression')
            if exp_node is None:
                return
            type_name = exp_node.text.decode('utf-8')
            method_name = function_node.child_by_field_name('name').text.decode('utf-8')
            result = next((item[1] for item in classInfo['class_fields'] if method_name == item[0]), None)
            if result is None:
                result = next((item[1] for item in classInfo['class_properties'] if method_name == item[0]), None)
            if result is not None:
                type_name = result
                
            if not type_name.istitle():
                return
            
            add_dependency(classInfo, type_name)
            tp = (type_name, method_name)
            
            if not any(item[1] == method_name for item in classInfo['class_method_calls']):
                classInfo['class_method_calls'].append(tp)
                return
        
        for child in node.children:
            traverse(child)

    traverse(node)
    
     

def extract_classes(root_node):
    classes = []

    def traverse(node):
        if node.type == 'class_declaration':
            class_info = extract_class_info(node)
            if  class_info['class_name'] is not None:
                classes.append(class_info)
        for child in node.children:
            traverse(child)

    traverse(root_node)
    return classes

def extract_csharp(root_node):
    classes = extract_classes(root_node)

    return classes