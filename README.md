
# 代码架构分析系统

基于LangChain和LangGraph构建的智能代码架构分析系统，用于自动化分析代码库结构并提供架构评审建议。

## 功能特性

- 代码结构分析：基于AST解析代码结构，提取类关系
- 向量化存储：使用ChromaDB存储代码片段向量
- UML图生成：自动生成Mermaid格式的UML类图
- 多维度分析：从模块化、可扩展性等多个维度分析架构
- 智能评审：基于LLM提供架构改进建议

## 技术栈

- LangChain: 构建LLM应用框架
- LangGraph: 工作流编排
- ChromaDB: 向量数据库
- OpenAI/Gemini: 大语言模型接口
- Tree-sitter: 代码解析

## 核心模块

### 代码分析器
<mcfile name="code_analyzer.py" path="h:\AI_WORK\ai_review33\agents\code_analyzer.py"></mcfile>
- 基于Tree-sitter解析代码AST
- 使用LangChain的文本分割器处理代码片段
- 通过LLM分析代码质量

### Mermaid生成器
<mcfile name="mermaid_generator.py" path="h:\AI_WORK\ai_review33\agents\mermaid_generator.py"></mcfile>
- 从代码结构生成UML类图
- 使用Mermaid语法描述类关系

### 架构分析器
<mcfile name="framework_analyzer.py" path="h:\AI_WORK\ai_review33\agents\framework_analyzer.py"></mcfile>
- 多维度分析架构设计
- 提供改进建议

### 向量存储
<mcfile name="vector_store.py" path="h:\AI_WORK\ai_review33\vector_store.py"></mcfile>
- 使用ChromaDB存储代码向量
- 支持相似代码检索

## 安装使用

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
- ARK_API_KEY: OpenAI API密钥
- ARK_API_URL: API基础URL
- GEMINI_API_KEY: Gemini API密钥

3. 运行分析
```bash
python main.py
```

## 输出示例

- UML类图：保存在 docs/uml_diagram.mmd
- 架构分析报告：保存在 docs/framework_analyze.md
- 代码异味分析：保存在 docs/smell_analyze.md

## 项目结构

```
.
├── agents/          # 分析代理模块
├── docs/           # 分析结果文档
├── extracts/       # 代码提取工具
├── test/          # 测试用例
├── main.py        # 主入口
└── requirements.txt
```

## 依赖版本

- langchain >= 0.3.18
- langgraph >= 0.2.72
- chromadb >= 0.6.3
- python-dotenv >= 1.0.0

## 注意事项

1. 需要配置正确的API密钥才能使用
2. 大型代码库分析可能需要较长时间
3. 代码分析Agent是逐代码文件分析，耗时与token消耗和代码量成正比
4. 实现方案经供参考，主要关键点已打通。


## 许可证

Apache License 2.0

Copyright (c) 2024 [奥格](https://github.com/jewis123)

根据 Apache License 2.0 许可证的要求，在使用本项目时需要：

1. 包含原始版权声明
2. 包含 Apache License 2.0 许可证的副本
3. 声明对原始代码的修改（如果有）
4. 在衍生作品中保留作者署名信息

完整许可证文本请参见：[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
