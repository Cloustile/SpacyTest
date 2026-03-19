# 快速上手指南

## 🚀 5 分钟快速开始

### 步骤 1: 安装依赖 (2 分钟)

```bash
# 安装 Python 包
pip install -r requirements.txt

# 下载 SpaCy 中文模型
python -m spacy download zh_core_web_sm
```

### 步骤 2: 配置 API Key (1 分钟)

1. 获取 DeepSeek API Key: https://platform.deepseek.com/
2. 打开 `.env` 文件
3. 填入你的 API Key:

```
DEEPSEEK_API_KEY=sk-your-api-key-here
```

### 步骤 3: 准备数据 (1 分钟)

将输入文件放入 `data&question` 目录:
- `data&question/data.txt` - 放入你的文本数据
- `data&question/question.txt` - 放入你的问题

**示例:**

data&question/data.txt:
```
北京是中国的首都。上海是中国最大的经济中心。广州是广东省的省会。
```

data&question/question.txt:
```
中国有哪些重要城市？
```

### 步骤 4: 运行程序 (1 分钟)

```bash
python main.py
```

完成！查看生成的文件:
- `data&question/dataKB.txt` - 数据知识库
- `data&question/questionKB.txt` - 问题知识库  
- `data&question/preKG.txt` - 知识图谱
- `answer/answer.txt` - AI 生成的答案

---

## 📋 完整功能说明

### 系统能做什么？

1. **自动阅读文本** - 从 data.txt 和 question.txt 读取内容
2. **智能提取** - 使用 SpaCy 识别实体（人名、地名、机构等）和关系
3. **构建知识库** - 生成结构化的知识库文件
4. **精准筛选** - 根据问题筛选相关知识
5. **知识图谱** - 创建可视化的知识图谱
6. **AI 问答** - 调用 DeepSeek 大模型生成答案

### 输入文件说明

#### data.txt (必需)
- **用途**: 存放待分析的文本数据
- **格式**: 任意中文文本
- **大小**: 建议 < 1MB
- **编码**: UTF-8

#### question.txt (必需)
- **用途**: 存放要提出的问题
- **格式**: 一个或多个问句
- **建议**: 问题要具体明确

### 输出文件说明

#### dataKB.txt
```
=== Data Knowledge Base ===

命名实体:
- 北京 (LOC) 地点
- 中国 (GPE) 地缘政治实体
- 上海 (LOC) 地点

关系 (主谓宾):
- 北京 -> 是 -> 首都
- 上海 -> 是 -> 中心
```

#### questionKB.txt
```
=== Question Knowledge Base ===

命名实体:
- 中国 (GPE)
- 城市 (NORP)
```

#### preKG.txt
包含:
- 筛选后的相关实体
- 筛选后的相关关系
- JSON 格式的结构化数据

#### answer.txt
```
=== Generated Answer ===

根据知识图谱，中国的重要城市包括:

1. 北京 - 中国的首都，政治中心
2. 上海 - 中国最大的经济中心
3. 广州 - 广东省省会，南方重要城市

这些城市在政治、经济和文化方面都具有重要地位...
```

---

## 🔧 常见问题

### Q1: 没有 DeepSeek API Key 怎么办？

**方案 1**: 注册 DeepSeek 获取免费额度
- 访问 https://platform.deepseek.com/
- 注册账号
- 创建 API Key

**方案 2**: 暂时不使用 LLM 功能
- 程序会跳过答案生成步骤
- 仍然可以获取知识图谱文件

### Q2: 提取效果不好怎么办？

**可能的原因**:
1. 文本质量不高 - 使用更规范的书面语
2. 模型太小 - 尝试更大的 SpaCy 模型
3. 领域特殊 - 考虑微调模型

**改进建议**:
```python
# 修改 main.py 中的模型
nlp = load_model("zh_core_web_md")  # 中型模型
nlp = load_model("zh_core_web_trf")  # 大型模型 (需要额外下载)
```

### Q3: 如何处理多个问题？

**方法**: 修改 question.txt 包含多个问题

```
问题 1: 中国有哪些重要城市？
问题 2: 北京和上海有什么关系？
问题 3: 广州在哪个省份？
```

或者批量处理 (需要修改代码)。

### Q4: 可以处理英文吗？

可以！只需更换模型:

```python
# 修改 main.py
nlp = load_model("en_core_web_sm")  # 英文模型
```

然后更新 requirements.txt:
```
spacy>=3.7.0
python-dotenv>=1.0.0
requests>=2.31.0
# en_core_web_sm 模型
```

---

## 💡 最佳实践

### 1. 数据准备
- ✅ 使用清晰、规范的文本
- ✅ 段落分明，逻辑清晰
- ✅ 避免过长句子 (< 100 字)
- ❌ 避免口语化表达
- ❌ 避免大量专业术语 (除非必要)

### 2. 问题设计
- ✅ 具体明确的问题
- ✅ 包含关键实体信息
- ✅ 与 data.txt 内容相关
- ❌ 过于宽泛的问题
- ❌ 缺少上下文的问题

### 3. 结果验证
- ✅ 人工检查提取的实体
- ✅ 验证关系抽取的准确性
- ✅ 对比 AI 答案与原文
- ❌ 完全依赖自动化结果

---

## 🎯 应用场景

### 场景 1: 文献综述
- **data.txt**: 多篇论文摘要
- **question.txt**: 这个领域的研究热点是什么？

### 场景 2: 新闻分析
- **data.txt**: 新闻报道合集
- **question.txt**: 这次事件涉及哪些公司和人物？

### 场景 3: 小说分析
- **data.txt**: 小说章节
- **question.txt**: 主要人物之间的关系如何？

### 场景 4: 情报挖掘
- **data.txt**: 开源情报资料
- **question.txt**: 某个组织的关键人物有哪些？

---

## ⚙️ 高级配置

### 调整筛选策略

修改 `main.py` 中的 `filter_relevant_knowledge()` 函数:

```python
def filter_relevant_knowledge(...):
    # 更严格的筛选
    # 或更宽松的筛选
    pass
```

### 自定义关系抽取

修改 `extract_relations()` 函数添加特定规则:

```python
def extract_relations(doc):
    relations = []
    for token in doc:
        # 添加你的自定义规则
        if token.dep_ == "你的依存关系":
            # 提取逻辑
            pass
    return relations
```

### 调整 LLM 参数

修改 `call_deepseek_api()` 函数:

```python
payload = {
    "model": "deepseek-chat",
    "temperature": 0.5,  # 降低随机性
    "max_tokens": 3000,  # 增加长度
}
```

---

## 📊 性能指标

### 典型处理速度
- 1KB 文本：~1-2 秒
- 10KB 文本：~5-10 秒
- 100KB 文本：~30-60 秒

### 准确率参考
- 实体识别：~70-85% (通用文本)
- 关系抽取：~50-70% (简单关系)
- 答案质量：取决于知识图谱质量

---

## 🆘 故障排除

### 错误："Model not found"
```bash
python -m spacy download zh_core_web_sm
```

### 错误："DEEPSEEK_API_KEY not found"
检查 `.env` 文件是否正确配置

### 错误："Connection timeout"
- 检查网络连接
- 确认能访问 DeepSeek API

### 提取结果为空
- 检查文本编码是否为 UTF-8
- 确认 SpaCy 模型已正确加载
- 尝试简化文本

---

## 📞 获取帮助

1. 查看 [EXAMPLES.md](./EXAMPLES.md) 获取更多示例
2. 查看 [README.md](./README.md) 了解完整文档
3. 检查 SpaCy 官方文档：https://spacy.io/docs
4. DeepSeek API 文档：https://platform.deepseek.com/docs

---

**祝你使用愉快！** 🎉

如有问题，欢迎反馈。
