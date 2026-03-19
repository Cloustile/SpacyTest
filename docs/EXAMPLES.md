# 使用示例

## 快速开始指南

### 第一步：环境准备

1. **安装依赖包**
```bash
pip install -r requirements.txt
```

2. **下载 SpaCy 中文模型**
```bash
python -m spacy download zh_core_web_sm
```

3. **配置 DeepSeek API Key**

编辑 `.env` 文件，填入您的 API Key：
```
DEEPSEEK_API_KEY=sk-your-actual-api-key
```

### 第二步：准备输入文件

#### data.txt 示例内容

您可以放入任何中文文本，例如：

```
李白是唐代著名诗人，出生于碎叶城。他的诗歌风格豪放奔放，代表作有《将进酒》、《静夜思》等。
杜甫也是唐代伟大的现实主义诗人，与李白并称"李杜"。杜甫的诗被称为"诗史"。
白居易是唐代另一位重要诗人，主张"文章合为时而著，歌诗合为事而作"。
长安是唐朝的都城，许多诗人都曾在此居住。
```

#### question.txt 示例问题

```
唐代有哪些著名诗人？他们之间有什么关系？
```

或者

```
李白和杜甫是什么关系？
```

### 第三步：运行程序

```bash
python main.py
```

### 第四步：查看结果

程序运行后会显示类似输出：

```
============================================================
SpaCy 知识图谱构建与 LLM 集成系统
============================================================

[步骤 1/7] 加载 SpaCy 模型...
✓ 模型加载成功

[步骤 2/7] 读取输入文件...
✓ 数据文件已读取 (12543 字符)
✓ 问题文件已读取 (25 字符)

[步骤 3/7] 使用 SpaCy 处理文本...
✓ 数据处理完成

[步骤 4/7] 提取实体和关系...
✓ 从数据中提取 45 个实体，23 个关系
✓ 从问题中提取 3 个实体，1 个关系

[步骤 5/7] 构建知识库文件...
✓ 数据知识库已保存至 dataKB.txt
✓ 问题知识库已保存至 questionKB.txt

[步骤 6/7] 筛选相关知识...
✓ 筛选出 15 个相关实体，8 个相关关系

[步骤 7/7] 构建初步知识图谱...
✓ 知识图谱已保存至 preKG.txt

[额外步骤] 调用 DeepSeek LLM API 生成答案...
✓ 答案已生成并保存至 answer.txt

============================================================
处理完成！
============================================================

生成的文件:
  - dataKB.txt (数据知识库)
  - questionKB.txt (问题知识库)
  - preKG.txt (知识图谱)
  - answer.txt (LLM 生成的答案)
```

## 输出文件详解

### 1. dataKB.txt - 数据知识库

包含从 data.txt 中提取的所有实体和关系：

```
=== Data Knowledge Base ===

Named Entities:
- 李白 (PERSON)
- 唐代 (DATE)
- 碎叶城 (LOC)
- 将进酒 (WORK_OF_ART)
- 静夜思 (WORK_OF_ART)
- 杜甫 (PERSON)
- 长安 (LOC)
- 白居易 (PERSON)

Total Entities: 8

==================================================

Relations (Subject-Verb-Object):
- 李白 -> 是 -> 诗人
- 杜甫 -> 是 -> 诗人
- 白居易 -> 是 -> 诗人

Total Relations: 3
```

### 2. questionKB.txt - 问题知识库

包含从 question.txt 中提取的实体和关系：

```
=== Question Knowledge Base ===

Named Entities:
- 唐代 (DATE)
- 诗人 (NORP)

Total Entities: 2

==================================================

Relations (Subject-Verb-Object):

Total Relations: 0
```

### 3. preKG.txt - 知识图谱

筛选后的相关知识，包含结构化信息：

```
=== Preliminary Knowledge Graph ===

Total Entities: 8
Total Relations: 3
Entity Types: PERSON, DATE, LOC, WORK_OF_ART

==================================================

ENTITIES:
[E0] 李白 (PERSON)
[E1] 唐代 (DATE)
[E2] 杜甫 (PERSON)
[E3] 白居易 (PERSON)
[E4] 长安 (LOC)

RELATIONS:
[R0] 李白 --[是]--> 诗人
[R1] 杜甫 --[是]--> 诗人
[R2] 白居易 --[是]--> 诗人

==================================================

JSON FORMAT:
{
  "entities": [
    {"text": "李白", "label": "PERSON", "id": "E0"},
    {"text": "唐代", "label": "DATE", "id": "E1"},
    ...
  ],
  "relations": [
    {"subject": "李白", "predicate": "是", "object": "诗人", "id": "R0"},
    ...
  ],
  "metadata": {
    "total_entities": 8,
    "total_relations": 3,
    "entity_types": ["PERSON", "DATE", "LOC", "WORK_OF_ART"]
  }
}
```

### 4. answer.txt - LLM 生成的答案

```
=== Generated Answer ===

根据知识图谱中的信息，唐代有以下著名诗人：

1. **李白**
   - 出生于碎叶城
   - 诗歌风格：豪放奔放
   - 代表作：《将进酒》、《静夜思》

2. **杜甫**
   - 唐代伟大的现实主义诗人
   - 与李白并称"李杜"
   - 诗被称为"诗史"

3. **白居易**
   - 唐代另一位重要诗人
   - 主张："文章合为时而著，歌诗合为事而作"

**他们之间的关系：**
- 李白和杜甫并称为"李杜"，代表了唐代诗歌的两座高峰
- 三人都是唐代诗歌的代表人物，但风格各异
- 他们都曾在长安（唐朝都城）活动过

==================================================
答案已生成完毕。
```

## 不同场景示例

### 场景 1：文学作品分析

**data.txt**: 《红楼梦》片段
**question.txt**: 贾宝玉和林黛玉是什么关系？

### 场景 2：新闻事件抽取

**data.txt**: 新闻报道文本
**question.txt**: 这次事件涉及哪些公司和人物？

### 场景 3：历史资料研究

**data.txt**: 历史文献
**question.txt**: 这个朝代发生了哪些重大事件？

### 场景 4：科技论文挖掘

**data.txt**: 学术论文
**question.txt**: 这篇论文研究了哪些核心概念？

## 常见问题解答

### Q1: 为什么提取的实体数量很少？

**A**: 可能的原因：
1. SpaCy 中文模型的识别能力有限
2. 文本中的命名实体本身较少
3. 可以尝试使用更大的模型：`zh_core_web_md`

### Q2: 关系抽取效果不好怎么办？

**A**: 当前实现基于简单的依存句法分析，可以：
1. 优化文本质量，使用规范的语法
2. 修改 `extract_relations()` 函数添加更多规则
3. 考虑使用更先进的关系抽取模型

### Q3: DeepSeek API 返回错误怎么办？

**A**: 检查以下几点：
1. API Key 是否正确
2. 网络连接是否正常
3. API 账户是否有足够余额
4. 请求格式是否符合规范

### Q4: 如何提高答案质量？

**A**: 建议：
1. 提供更清晰、具体的问题
2. 确保 data.txt 中包含充分的背景信息
3. 调整知识筛选策略
4. 在 prompt 中添加更多约束条件

## 性能优化建议

### 处理长文本

如果 data.txt 非常大（>1MB），建议：
1. 分批处理文本
2. 使用更大的批处理大小
3. 考虑使用 GPU 加速

### 提高准确率

1. **自定义实体类型**：扩展 SpaCy 的 NER 模型
2. **领域词典**：添加专业术语词典
3. **后处理规则**：添加领域特定的过滤规则

## 实验与调试

### 查看 SpaCy 解析结果

可以在代码中添加调试输出：

```python
doc = nlp(text)
for token in doc:
    print(f"{token.text}: pos={token.pos_}, dep={token.dep_}")
```

### 测试不同模型

```python
# 尝试不同的模型
models_to_try = ["zh_core_web_sm", "zh_core_web_md", "zh_core_web_trf"]

for model_name in models_to_try:
    try:
        nlp = spacy.load(model_name)
        # 测试效果
    except:
        print(f"Model {model_name} not available")
```

## 进阶使用

### 批量处理多个问题

修改 `main.py` 支持批量处理：

```python
questions = [
    "问题 1",
    "问题 2",
    "问题 3"
]

for i, q in enumerate(questions):
    # 处理每个问题
    with open(f"question_{i}.txt", "w") as f:
        f.write(q)
    # 调用处理流程
```

### 导出可视化图谱

可以将 preKG.txt 中的 JSON 数据导入图数据库或可视化工具：
- Neo4j
- Gephi
- Cytoscape.js
- D3.js

---

**提示**: 建议先用小样本测试整个流程，确认一切正常后再处理大规模数据。
