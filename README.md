# SpaCy 知识图谱构建与 LLM 集成系统

## 项目简介

本项目是一个基于 SpaCy 自然语言处理库和 DeepSeek LLM API 的知识图谱构建与问答系统。系统能够从文本数据中自动提取实体和关系，构建知识图谱，并利用大语言模型生成问题的答案。

## 核心功能

1. **实体与关系提取**：使用 SpaCy 从数据文本和问题文本中自动提取命名实体和语义关系
2. **知识库构建**：分别生成数据知识库（dataKB.txt）和问题知识库（questionKB.txt）
3. **知识筛选**：根据问题知识库筛选出数据知识库中的相关知识
4. **知识图谱构建**：生成初步知识图谱（preKG.txt），包含结构化的实体和关系信息
5. **LLM 智能问答**：调用 DeepSeek API，基于知识图谱生成问题答案
6. **答案输出**：将生成的答案保存至 answer.txt 文件

## 系统架构

```
输入文件 → SpaCy 处理 → 实体/关系提取 → 知识库构建 → 知识筛选 
    ↓
知识图谱构建 → DeepSeek LLM → 答案生成 → 输出文件
```

## 文件说明

### 输入文件
- `data.txt`：待分析的原始文本数据（中文）
- `question.txt`：用户提出的问题文本

### 输出文件
- `dataKB.txt`：从 data.txt 提取的知识库（包含实体和关系）
- `questionKB.txt`：从 question.txt 提取的知识库
- `preKG.txt`：筛选后的初步知识图谱（JSON + 可读格式）
- `answer.txt`：LLM 生成的答案

### 配置文件
- `.env`：环境变量配置，用于存储 DeepSeek API Key
- `requirements.txt`：Python 依赖包列表

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 下载 SpaCy 中文模型

```bash
python -m spacy download zh_core_web_sm
```

### 3. 配置 DeepSeek API Key

在 `.env` 文件中填入您的 DeepSeek API Key：

```
DEEPSEEK_API_KEY=your_actual_api_key_here
```

**获取 API Key：**
1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册并登录账号
3. 在 API 管理页面创建 API Key
4. 将 API Key 复制到 `.env` 文件中

## 使用方法

### 1. 准备输入文件

确保 `data.txt` 和 `question.txt` 文件存在并包含相应内容。

### 2. 运行程序

```bash
python main.py
```

### 3. 查看结果

程序运行后会生成以下文件：
- `dataKB.txt` - 完整的数据知识库
- `questionKB.txt` - 问题知识库
- `preKG.txt` - 知识图谱
- `answer.txt` - LLM 生成的答案

## 工作流程详解

### 步骤 1: 文本预处理
- 加载 SpaCy 中文模型
- 读取 data.txt 和 question.txt

### 步骤 2: 语言分析
- 对两个文本进行分词、词性标注和依存句法分析
- 识别命名实体（人名、地名、组织名等）

### 步骤 3: 知识提取
- **实体提取**：识别命名实体及其类型
- **关系提取**：基于依存句法分析提取主谓宾三元组

### 步骤 4: 知识库构建
- 将提取的实体和关系结构化存储
- 生成可读性强的知识库文件

### 步骤 5: 知识筛选
- 提取问题中的关键词和实体
- 在数据知识库中匹配相关知识
- 过滤无关信息，保留核心知识

### 步骤 6: 知识图谱构建
- 为实体和关系分配唯一 ID
- 构建图结构数据
- 同时保存为人类可读格式和 JSON 格式

### 步骤 7: LLM 推理
- 将知识图谱转换为自然语言提示
- 调用 DeepSeek API
- 生成基于知识的答案

## 输出示例

### dataKB.txt 格式
```
=== Data Knowledge Base ===

Named Entities:
- 厦门 (LOC)
- 江南 (LOC)
- 杏花春雨江南 (WORK_OF_ART)

Total Entities: 45

==================================================

Relations (Subject-Verb-Object):
- 他 -> 希望 -> 巷子
- 雨 -> 下在 -> 城市

Total Relations: 23
```

### preKG.txt 格式
```
=== Preliminary Knowledge Graph ===

Total Entities: 15
Total Relations: 8
Entity Types: LOC, PERSON, WORK_OF_ART

==================================================

ENTITIES:
[E0] 厦门 (LOC)
[E1] 江南 (LOC)
[E2] 雨 (NATURAL_PHENOMENON)

RELATIONS:
[R0] 他 --[希望]--> 巷子
[R1] 雨 --[下在]--> 城市

==================================================

JSON FORMAT:
{
  "entities": [...],
  "relations": [...],
  "metadata": {...}
}
```

## 自定义配置

### 更换 SpaCy 模型

如需使用其他模型，修改 `main.py` 中的 `load_model()` 函数调用：

```python
# 英文模型
nlp = load_model("en_core_web_sm")

# 更大的中文模型
nlp = load_model("zh_core_web_md")
```

### 调整筛选策略

修改 `filter_relevant_knowledge()` 函数中的逻辑来改变知识筛选的严格程度。

### 修改 LLM 参数

在 `call_deepseek_api()` 函数中可以调整：
- `temperature`：控制生成答案的创造性（0.0-1.0）
- `max_tokens`：限制答案最大长度

## 故障排除

### 问题：SpaCy 模型未找到
**解决方案**：
```bash
python -m spacy download zh_core_web_sm
```

### 问题：DeepSeek API 调用失败
**检查项**：
1. 确认 `.env` 文件中已正确配置 API Key
2. 检查网络连接
3. 确认 API Key 有效且有足够额度

### 问题：提取效果不佳
**建议**：
1. 尝试使用更大的 SpaCy 模型（如 `zh_core_web_md`）
2. 优化输入文本质量
3. 调整关系提取规则

## 技术栈

- **Python 3.12+**
- **SpaCy 3.7+**：自然语言处理
- **requests**：HTTP 请求
- **python-dotenv**：环境变量管理
- **DeepSeek API**：大语言模型服务

## 项目结构

```
f:\1-Research\SpacyTest
├── main.py                 # 主程序：知识图谱构建与 LLM 问答系统核心代码
│
├── data&question/          # 输入数据目录
│   ├── data.txt           # 输入：待分析的文本数据
│   ├── question.txt       # 输入：用户提出的问题
│   ├── dataKB.txt         # 输出：数据知识库（包含所有提取的实体和关系）
│   ├── questionKB.txt     # 输出：问题知识库（问题中的实体和关系）
│   └── preKG.txt          # 输出：初步知识图谱（筛选后的相关知识，含上下文）
│
├── answer/                 # 答案输出目录
│   └── answer.txt         # 输出：LLM 生成的最终答案
│
├── docs/                   # 文档目录：存放项目相关文档资料
│   ├── CHANGELOG.md       # 更新日志：记录项目的版本变更和新功能
│   ├── EXAMPLES.md        # 使用示例：详细的使用案例和场景演示
│   └── notes.md           # 备注说明：开发笔记和技术要点
│
├── reference/              # 参考资料目录：存放参考文献和论文
│   └── *.pdf              # 学术论文：如知识图谱问答相关的研究论文
│
├── QUICKSTART.md           # 快速上手指南：5 分钟快速开始教程，包含完整示例和常见问题
├── README.md               # 项目说明：本项目的主文档，包含功能介绍、安装和使用方法
├── requirements.txt        # 依赖列表：Python 包依赖清单
├── .env                    # 环境变量配置：存储 API Key 等敏感信息（不被 Git 跟踪）
├── .env.example            # 环境变量模板：.env 文件的示例模板
├── .gitignore              # Git 忽略配置：指定不需要版本控制的文件
├── test.py                 # API 测试脚本：测试 DeepSeek API 连接和配置
└── test_installation.py    # 安装测试脚本：验证系统环境和依赖是否齐全
```

**目录说明：**
- **`data&question/`**: 存放输入数据和生成的知识库文件
- **`answer/`**: 存放 LLM 生成的答案
- **`docs/`**: 项目文档资料，包括更新日志、使用示例和开发笔记
- **`reference/`**: 学术参考资料，如相关研究论文
- **根目录**: 核心代码、主文档和配置文件

**最佳实践：**
- ✅ 将不同的数据集放在 `data&question/` 目录下管理
- ✅ 答案统一输出到 `answer/` 目录，便于查找
- ✅ 技术文档存放在 `docs/` 目录
- ✅ 参考文献放在 `reference/` 目录
- ✅ 保持根目录整洁，只保留核心文件

## 扩展应用

本系统可以应用于：
- 📚 文献知识抽取
- 📰 新闻事件分析
- 📖 文学作品人物关系分析
- 🔍 情报检索与问答
- 📊 领域知识图谱构建

## 注意事项

1. **隐私保护**：不要上传敏感或个人隐私数据
2. **API 费用**：DeepSeek API 按使用量计费，请注意控制成本
3. **版权合规**：确保输入文本的使用符合版权法规
4. **结果验证**：建议人工审核 LLM 生成的答案

## 未来改进方向

- [ ] 支持多轮对话
- [ ] 增加知识图谱可视化
- [ ] 支持更多语言模型（ChatGLM、通义千问等）
- [ ] 实现更复杂的关系抽取算法
- [ ] 添加知识融合与消歧功能
- [ ] 提供 Web 界面

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，欢迎通过 GitHub Issues 联系。

---

**最后更新**: 2026-03-18
