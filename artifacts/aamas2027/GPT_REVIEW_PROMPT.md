# GPT 审阅提示词

请作为严格的 AAMAS 研究审稿人和实验代码审计员，审阅 FlowFence-Lite / PAPC 的 AAMAS 2027 补实验。目标是判断证据是否足以支撑论文贡献，以及最小必要修改是什么。不要替作者美化结论。

仓库：https://github.com/BlockChainLover/flowfence

审阅分支：`codex/aamas2027-experiment-extension`。实验实现提交：`ab30af9257d233508f2312475554b482c2bbbf34`。本分支基于 `codex/wine2026-rebuttal-noapi`；请仅审阅 AAMAS 增量，历史 WINE 内容只用于核查来源。

先阅读 `artifacts/aamas2027/EXPERIMENT_SUMMARY.md`、`PAPER_INTEGRATION.md`、`MANIFEST.json`、`PRIOR_EVIDENCE_AUDIT.md`、`TEST_REPORT.md`，再交叉核对 `configs/experiment/aamas2027/`、`src/experiments/aamas_*.py`、`src/defenses/mas_flowfence.py`、`scripts/package_aamas2027.py`、测试和各 E0–E4 `formal/` 安全 JSONL。`pilot/` 必须与正式样本分开。MANIFEST 的 SHA 和 pushed=false 是实验打包时状态，后续结果发布不改变实验源码版本。

请重点检查：

1. PAPC 与 IFC-SafeView 是否共享同样的 detector、safe-view generator/validator、registry 和所有拦截位置；是否存在旁路、特权信息、评测答案进入 agent 输入或不公平执行差异。
2. E1 是否确有三个 LLM 角色生成并消费受控上游输出，动作是否改变实际状态；固定调度和确定性工具对“多智能体”主张有何限制。任务成功检查是否过弱，预算从未绑定是否使 private-budget reasoning 主张失效。
3. 从保存记录复算样本数、成功率、暴露、干预和配对比较。区分注入源暴露与模型生成暴露、执行失败与保密失败、未完成测量与真实零暴露；确认未删除失败或混入 dry-run。
4. E0 只有一个历史任务，E1 是同一场景的 12 个公开参数变体。检查伪重复、bootstrap 单位、全打平的 [0,0] 区间及跨领域推断是否越界。
5. E2 的计时边界、预热、单位、分位数和实际序列化字节是否可复算；区分 24-event 存储投影与 E1 实际审计存储，不能将 Python 局部开销当作端到端延迟。
6. E3 格式变换、同接收者跨消息拼接、阈值推导的攻击者知识和重建判据是否合理；它们是确定性注入探针，不能写成实测 LLM 自主攻击。
7. E4 全部 HTTP 403 是否明确标为无第二模型证据；E5 未触发是否与配对打平一致；是否仍有未经验证的 topology necessity、语义保密或跨模型泛化主张。

核查锚点（请独立验证，而非照抄）：E0 270 episodes / 90 PAPC–IFC 配对，隐私与任务成功打平；E1 144 attempts、141 completed、3 parser failures，PAPC/IFC 各 48/48 成功且全部 48 配对打平；No Defense 44/48 task success、24/48 privacy-safe success；E2 45 trials；E3 90 probes 全部可重建；E4 20 次 403；pilot 8 episodes；含 pilot 共 470 API 请求。针对性测试 64 通过；全库 132 通过、1 个已存在的缺文件失败。

输出要求：先给总体判断，再按严重程度列出问题，每项附文件路径/行号、对应记录或复算过程、对结论的影响和最小修复建议。分清已证实缺陷、证据缺口和可选改进。给出“当前支持 / 必须收窄 / 不支持”的论文主张清单，以及最多三个最值得做的后续实验。若无法访问文件或执行复算，明确列出未核验项，不要声称完成审计。不调用付费 API，不修改原始结果，不编造结果或人类评分。
