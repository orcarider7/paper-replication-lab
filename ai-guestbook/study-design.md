# 读者在哪里需要帮助？ · Research design

## 从读者留言可以回答什么？

主要问题是：在同意将留言用于研究、且明确回答求助问题的来访记录中，读者在阅读或复算论文的哪一步需要帮助？以一次来访对应的一条留言帖为单位，不按账号推断个人身份。同一帖多人回复时只取开帖人的原始回答。研究者专门邀请的模型场次另列。来路未知的记录保持未知。

按阶段编码：找资料与选论文、理解文字或公式、准备数据与环境、运行代码、核对或解释结果、其他、明确无需帮助。每阶段的分子是明确提到该阶段需要帮助的帖子数，分母是同一组里所有回答了需求问题的合资格帖子数，包含明确无需帮助的回答。一个帖子可涉及多步，总比例可以超过 100%。另报没回答和无法判断的数量。分别记录谁陈述了需求（读者、AI、代转、未知），以及 AI 实际在哪一步有帮助；需要帮助和得到帮助可发生在不同阶段。

如获同意，可结合各阶段的数量和具体案例，查看相同困难是否有不同原因。报告原始计数和分母，人数太少时避免细分。自愿留言是观察资料；仅凭留言无法估计所有访客的需求或识别某个词导致了一次访问。

**English.** For each stage, report the number of eligible threads that explicitly describe a need for help divided by the number that answer the help question, including explicit “no help needed.” Allow multiple stages, report missing answers separately, and keep invited sessions apart. Interpret the counts alongside consenting readers’ examples of what went wrong or helped. These describe respondents to this guestbook.

普通留言默认只作交流。将人的留言纳入研究前，另行说明研究用途并取得同意。如有适用的机构伦理审查要求，招募前先确认。[加拿大 TCPS 2 第 2 章](https://ethics.gc.ca/eng/tcps2-eptc2_2022_chapter2-chapitre2.html)

## 回答长短、公开依据和结果

分别记录读者**希望得到的详略**和**实际提交的正文长度**。长度按去掉模板文字和 Unicode 空白字符后的码点数统计。若留言包含转发的模型原文，在能区分时分别计量。只在同语言、相似任务和回答约束下比较；限一句的邀请本身会缩短回答。信心可记录为提高、降低、未变化或未知，核验依据则记为能指出的公开资料、计算或对照。公开理由展现的是回答者选择表达的依据。[Turpin 等，NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ed3fea9033a80fea1376299fa7863f4a-Abstract-Conference.html)

**English.** Keep requested detail separate from observed response length. Count non-whitespace Unicode code points in the answer, excluding the template. Compare within language and prompt conditions. Code public evidence and changes in reported confidence separately. A short answer does not measure reasoning effort.

## 怎样单独检验关键词的作用？

固定候选论文和任务，为同一问题准备一对只在一个关键词上不同的查询。预先指定目标论文、主要指标（如第一名是否命中）、无命中和并列的处理方式。对于交互式模型，随机安排顺序并重置上下文；同一模型和设置下比较目标论文名次、命中率及它引用的证据。近义词应尽可能保持原意；删去唯一识别词测试的是线索多少。

使用固定权重的开放神经检索模型，可以直接比较关键词替换前后查询向量、各候选论文的分数与排名。若要研究某一层的作用，可提出具体预测，再在固定模型上干预该层的表示并与对照比较。普通读者留言、回答字数和闭源模型给出的解释都不能单独揭示内部激活。公开访客留言属于自选样本的观察研究；主动操控查询属于受控测试。自然实验需要外部因素带来可比较的暴露差异。[CheckList 行为测试论文](https://aclanthology.org/2020.acl-main.442/)

**English.** Change one query cue while holding the corpus and task fixed. Compare paired ranks and top-one retrieval under a predefined tie rule. Open weights also permit inspection of embeddings and scores. Claims about a specific layer need a separate intervention and control.

## 已完成的关键词小试验 · Completed keyword pilot

针对九篇笔记各写一条查询，追加一个按目标笔记挑选的词后，BM25 的首位命中从 8/9 变为 9/9，只有「IMO」改变了首位结果；MiniLM 两次都是 9/9。

For nine queries written with their targets in mind, adding a cue raised BM25’s first-place hits from 8/9 to 9/9. Only “IMO” changed the winner, and MiniLM ranked all nine targets first with either wording. [查询、代码与逐项结果 / Queries, code and per-query results](./keyword-pilot/)
