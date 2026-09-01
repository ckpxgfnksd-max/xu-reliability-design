# 徐天音论文全量 coverage ledger 与 reliability 原则候选

研究边界：徐天音官网 `pub.html` 在 2026-09-01 列出的 97 个条目。官方目录决定 inclusion；OpenAlex 只作检索辅助。`F` 表示本轮完成 primary PDF 全文原则筛查，`T` 表示 primary PDF 不可得、只能使用官方标题/目录信息。分类含义如下：

- `direct`：论文直接给出可复用的可靠性、配置、操作、控制面、验证或 AI-SRE 设计判断。
- `adjacent`：机制能补充系统设计，但论文核心目标不是上述可靠性问题，不能当作主证据单独推广。
- `none`：对完整学术版图有意义，但无法为这版 skill 提供可追溯的通用可靠性 guideline。

## 核心判断

现有 skill 抓住了 config 与 controller 两条主干，但还没有覆盖徐天音论文中反复出现的五类共通判断：第一，验证对象必须覆盖配置、操作、访问策略、恢复动作与 AI 行动等所有 change surface；第二，可靠性问题大量出现在交互边界与不完整历史，而非单个模块内部；第三，oracle 必须观察外部行为，并验证测试替身、模型与实现之间的 fidelity；第四，恢复本身也要满足“不恶化”的安全约束；第五，验证机制必须嵌入开发者实际使用的抽象层，脱离编程接口的验证器会诱发绕过。

本轮对 94 篇可用 primary PDF 完成全文原则筛查：第一轮对 49 篇高相关论文做机制性 close read；第二轮补读其余 45 篇全文的摘要、问题陈述、设计、限制与结论。`xu-002`（Welder）、`xu-003`（MCon）、`xu-005`（Rex TOCS）正文不可得，严格保留 metadata-only；Rex 的机制只使用可得的 ATC 版本 `xu-017`。

## 97/97 coverage ledger

| ID | 题目短名 | contributes | thread | 深度 | 分类理由 |
|---|---|---|---|---|---|
| xu-001 | ConfFuzz | direct | configuration testing | F | 以 unit tests 驱动 parameter-aware fuzzing；直接支持“只变异当前执行会读取的参数，并同时用代码与参数覆盖反馈”。 |
| xu-002 | Welder | adjacent | controller liveness / composition | T | 官方标题和 artifact metadata 只表明它与多 controller 组合 liveness 有关；primary PDF 不可得，故仅保留 metadata direction，不作为已审计的 direct evidence。 |
| xu-003 | MCon | adjacent | cloud architecture / consolidation | T | framework consolidation 可能支持减少重复状态与跨组件边界；只有标题，不能提炼具体可靠性规则。 |
| xu-004 | Specula | direct | AI + formal specification | F | 自主生成 TLA+ 模型与 invariants，并用 trace validation 约束 model-code conformance；直接暴露 AI reward hacking 与 abstraction 选择问题。 |
| xu-005 | Rex TOCS | adjacent | safe extensibility / verification UX | T | 安全 kernel extension 的 usable enforcement 属于验证接口设计；只有标题，主要证据用 xu-017/044。 |
| xu-006 | Xkernel | adjacent | safe live tuning | F | 在线修改 perf-const 时要求 side-effect safety，说明 live tuning 不能只保证版本原子性；论文核心仍是性能可调性。 |
| xu-007 | Oxbow | adjacent | multi-component architecture | F | 让 kernel/user/device 各承担最适合的 operation，以 single-writer/shared metadata、Split Journaling 和显式恢复协调；支持职责放置与协调 invariant，但核心仍是文件系统架构。 |
| xu-008 | SREGym | direct | AI-SRE benchmark fidelity | F | live cloud-native 环境、跨层 fault/noise、metastability 与 correlated failures；直接支持 AI-SRE 的高保真验收。 |
| xu-009 | OAT / Watchers | direct | operator-application interaction | F | 412 个 operator failures 表明交互缺陷占主导；应用语义、前置条件与可观测性是设计对象。 |
| xu-010 | Eroica | direct | production diagnosis | F | 用全机群 fine-grained profiling 与 differential observability 做在线定位；直接支持“相对比较 + 生产覆盖”的诊断设计。 |
| xu-011 | SysMoBench | direct | AI formal-model evaluation | F | 用 syntax/runtime/conformance/invariant correctness 四类可执行指标验收 AI 生成模型，禁止“能运行即正确”。 |
| xu-012 | Stratus | direct | autonomous SRE safety | F | TNR 把 mitigation 变成可撤销事务，并用确定性 state machine、write exclusivity 与 sandbox 约束 AI。 |
| xu-013 | DebCovDiff | adjacent | testing-tool reliability | F | coverage 工具自身会给出错误 assurance；真实项目上的 differential oracle 可验证测试基础设施，但并非生产系统设计主线。 |
| xu-014 | Kscaler | adjacent | control semantics / autoscaling | F | 指出 cloud millicore 与 kernel time quota 的 semantic gap；支持 control loop 应读取最接近真实机制的信号。 |
| xu-015 | Chameleon | adjacent | LLM serving performance | F | 把 SLO、饥饿避免、资源配额、预测误差与动态 workload 分布写入调度控制；核心仍是 LLM serving 性能。 |
| xu-016 | EMT | adjacent | memory translation architecture | F | 以窄接口消除 overloaded semantics，并用 atomic switch、渐进集成与持续测试控制硬软协同风险；作为架构相邻证据。 |
| xu-017 | Rex ATC | adjacent | safe extensibility / verification UX | F | language-verifier gap 会拒绝安全程序并诱发 verifier-pleasing rewrites；支持把 safety contract 放进开发者使用的语言与接口。 |
| xu-018 | ITBench | direct | AI-IT benchmark | F | 94 个真实 IT 场景和可解释指标显示 frontier agents 的 SRE/CISO/FinOps 成功率仍低；上线前必须场景化验收。 |
| xu-019 | Mux | direct | modular storage architecture | F | 明确 metadata owner、atomic visibility、失败尝试无副作用、有限重试与 lock fallback，直接给出安全迁移与进展契约。 |
| xu-020 | ACtests | direct | access-control change testing | F | 在 production program/data 的 mini environment 中比较 change 前后允许/拒绝请求；直接支持有效行为 diff。 |
| xu-021 | Multi-Grained Specs | direct | model checking / conformance | F | 细模型会 state explosion，粗模型会 model-code gap；按 change 局部组合不同粒度并做 conformance check。 |
| xu-022 | M5 | adjacent | tiered-memory performance | F | 在 CXL 层读取真实访问计数；收益恶化时停止，并拒绝 pinned/用户指定页面迁移；核心仍是 tiered-memory 性能。 |
| xu-023 | CXLfork | adjacent | remote fork / autoscaling | F | 按 private/global/reconfigurable state 划分 restore contract，以 CoW immutable checkpoint 去除发起节点生命周期依赖；crash-prefix 证据不足。 |
| xu-024 | Cloud Emulator Fidelity | direct | test-double fidelity | F | 255 个 API 中 94 个出现 emulator/real discrepancy；直接否定“离线 mock 通过即部署安全”。 |
| xu-025 | Ciri | direct | LLM config validation | F | LLM validator 有 hallucination、false positive/negative、dependency/version-specific weakness；只能作为受约束的一层。 |
| xu-026 | ScalaCN | direct | network scalability | F | 生产故障覆盖 slow/stale/race/capacity propagation；以 causal testing、LTL oracle、closed-loop 校准和异常停用构成直接可靠性设计。 |
| xu-027 | Vsync | adjacent | mobile cloud gaming | F | 端到端 trace 显示多个局部正确 barrier 会放大微小 jitter；同步优化仍须保留 frame-access correctness。 |
| xu-028 | Concord | direct | distributed cache coherence | F | 设计 crash recovery、stale-copy fencing、membership transition，并以 TLA+ 检查 consistency/deadlock/livelock，直接支持状态与进展原则。 |
| xu-029 | vSoC | adjacent | virtualization performance | F | 以 unified SVM authority、happens-before fences、预测失败停用与 flow control 维持跨设备一致性；核心仍是虚拟化性能。 |
| xu-030 | Mobile process management | direct | mobile OS performance | F | 直接否定声明状态等于真实状态，并以行为观测、动态状态模型和 freeze-before-kill 做安全处置。 |
| xu-031 | Anvil | direct | controller liveness / verification | F | 定义 ESR，显式列出 fault/fairness assumptions，并验证 controller 在任意中间状态后最终收敛。 |
| xu-032 | UNO kprobe | adjacent | observability instrumentation | F | compile-time 最小化插入点使关键 kernel 位置可被安全、低开销地 runtime instrument，并保留 register/context；这是 P12/P13 的 evidence substrate，但不等于完整 provenance 或 recovery oracle。 |
| xu-033 | Ctest4J | direct | configuration testing tooling | F | 把 ctest 机制产品化为 Java 框架，证明 candidate-config testing 可落入日常 CI。 |
| xu-034 | EcoFaaS | adjacent | serverless energy efficiency | F | 以 end-to-end SLO 为硬约束，持续校正预测并约束更新 cadence；作为能效 controller 的相邻证据。 |
| xu-035 | DMT | adjacent | memory translation | F | 让 OS 语义进入硬件协同接口，同时保留 isolation、fallback 与 backward compatibility；核心仍是地址翻译性能。 |
| xu-036 | RCACopilot | direct | LLM incident RCA | F | 结合历史 incident、runtime diagnostic information 与 production dataset；支持 AI 诊断必须 grounding、路由和量化评估。 |
| xu-037 | Virtual Device GetMobile | adjacent | test-environment fidelity | F | mobile app testing 的 fidelity/efficiency/accessibility 综述，能补强高保真测试环境原则。 |
| xu-038 | Acto | direct | operation correctness | F | 把 operation sequences 与 misoperations 变成输入，用 consistency/differential/recovery oracles 验证外部行为和恢复。 |
| xu-039 | CXL memory study | direct | hardware characterization | F | 以真实 CXL 设备差分证明 emulator/remote-NUMA surrogate 会误导 placement 与控制决策，直接支持 fidelity 与分布校准。 |
| xu-040 | Virtual Device Farms | direct | test-environment fidelity | F | 以真实设备为 ground truth 量化 virtual-farm escape/false alarm，并把 residual gap 路由到物理设备验证。 |
| xu-041 | GPU memory efficiency | adjacent | distributed training performance | F | 用生产 job/model cohort 推导内存 envelope，把 OOM 作为 hard rejection，并暴露 underestimate 与 fallback；核心仍是训练效率。 |
| xu-042 | HugeGPT | adjacent | address translation | F | guest 向 host 暴露窄语义 signal，并在 huge-page 分配失败时保留正确的 4KB fallback；作为 P13 相邻案例。 |
| xu-043 | Relational Debugging | direct | diagnosis oracle | F | 性能取决于 workload，绝对阈值不可靠；以 good/bad execution 中 runtime-event relations 定位根因。 |
| xu-044 | Kernel verification untenable | adjacent | verification architecture | F | 单一复杂静态 verifier 产生漏洞和 unsafe escape hatches；主张 safe language + lightweight runtime + separation of concerns。 |
| xu-045 | MXFaaS | adjacent | serverless resource sharing | F | 共享/合并优化只适用于已证明 pure/commutative 的操作；其余保序、隔离并保留原调用边界。 |
| xu-046 | Cross-System Interaction Failures | direct | interaction reliability | F | 以跨系统交互失败为独立故障类别，支持按 seam 而非组件枚举 failure modes。 |
| xu-047 | Rainmaker | direct | dependency fault injection | F | REST interaction 的 timeout/error/retry 等异常需要系统化注入，并验证应用的 error handling。 |
| xu-048 | uRTS | direct | code + config regression selection | F | 统一选择 code/config change 影响到的 tests，直接支持配置变更与代码变更同等进入 regression gate。 |
| xu-049 | Vetter | direct | web performance testing | F | 用用户可见 morphology invariant、单项撤销的 counterfactual 和 runtime provenance 验证并诊断优化链，直接支持行为 oracle。 |
| xu-050 | SpecFaaS | adjacent | speculative execution | F | 给出 speculate→buffer→validate→commit 或 discard+replay 的事务模式；安全面不完整，作为 P3/P10 相邻例证。 |
| xu-051 | Hashed Page Tables | none | memory architecture | F | 页表内存效率机制。 |
| xu-052 | seccomp-eBPF | direct | programmable security / safe extension | F | 在 kernel system-call authority boundary enforcement，并以 verifier/helper/capability 和 phase binding 限制可编程语义。 |
| xu-053 | Mobile bandwidth in practice | direct | measurement-driven design | F | 以大规模 field distribution/cohort 纠正 signal/peak proxy，并以 client feedback 持续重校容量与部署决策。 |
| xu-054 | Sieve | direct | controller perturbation testing | F | crash/stale/unobserved-state perturbation + cluster evolution diff；直接支持按部分历史系统化测试。 |
| xu-055 | Trinity | adjacent | emulator fidelity | F | graphics projection 提高 mobile emulation fidelity；是测试基础设施的相邻例子。 |
| xu-056 | DepFast | adjacent | fail-slow / quorum orchestration | F | 把 quorum code 的 fail-slow points 变成显式编程控制；可靠性相关，但机制针对 RSM 性能故障。 |
| xu-057 | KFuse | direct | verified extension composition | F | 区分 semantic safety property 与 verifier resource bound，证明 post-verification composition 并保留原管理语义。 |
| xu-058 | Nested cuckoo PT | none | memory translation | F | 虚拟内存并行优化。 |
| xu-059 | Dossier | direct | configuration attack forensics | F | 配置是可被攻击者利用的持久化 change surface；支持 config provenance、timeline 与 forensic evidence。 |
| xu-060 | ConfigX | direct | silent configuration effects | F | 用 interaction analysis 发现 set-but-ineffective 的 silent misconfigurations，支持“配置生效”必须有行为 oracle。 |
| xu-061 | Vet | adjacent | mobile UI test exploration | F | 为测试器自身设计 progress oracle、trace provenance 与 tarpit watchdog，并指出外部状态使 checkpoint/restore 不可靠。 |
| xu-062 | Cellular Reliability | adjacent | reliability measurement | F | 70M 设备实测纠正常识，并把 trace/diagnosis 结果转成 OS 改进；支持真实分布测量，不是控制面主线。 |
| xu-063 | Ctest Prioritization | direct | configuration test economics | F | quickest-first 可在 change gate 中尽早得到故障信号；直接支持 deadline-aware 配置测试。 |
| xu-064 | Partial Histories | direct | state / cache / observability | F | 明确 staleness、time travel、observability gaps，要求组件在不完整历史下仍正确。 |
| xu-065 | Fail-slow support | direct | slow fault tolerance | F | slow fault 会跨组件传播，需在编程模型中显式标识、控制和验证；不能只注入 crash/error。 |
| xu-066 | Configuration evolution | direct | proactive config engineering | F | 检查代码多为事故后补；默认值变更很少系统测试，支持把检查与测试提前写进 design。 |
| xu-067 | FastBTS | adjacent | production measurement | F | 从 noisy throughput samples 估计 access bandwidth，并显式权衡 accuracy、data/time cost、saturation 与 server-deployment assumptions；支持 P14 的 measurement-fidelity boundary，不推出通用监控频率。 |
| xu-068 | ctest | direct | candidate-config execution | F | value validation 不能抓 valid change 触发 dormant bug；必须把候选生产配置接入受影响代码测试。 |
| xu-069 | cDep | direct | cross-parameter/component constraints | F | 发现大量 intra/cross-component dependencies 且多数未文档化；依赖关系是一等设计对象。 |
| xu-070 | Kscope | direct | live forensics | F | 同一性能 symptom 可能需要相反 mitigation；用 live path/evidence classification 在行动前区分 failure mode。 |
| xu-071 | Draco | adjacent | security architecture | F | system-call security 的 architecture/OS support 体现 enforcement 应置于系统边界，但与主线距离较远。 |
| xu-072 | Android ANR/SNR + WAM | adjacent | cross-app blocking / resumable maintenance | F | 揭示 delete/discard→fsync 的跨 app/OS slow-path 传播，并把不可中断、kill 后重启的 maintenance 改为可 pause/resume；支持 P3/P4/P7，阈值仍需真实 workload/QoE 校准。 |
| xu-073 | Cozart | direct | OS configuration / attack surface | F | kernel debloating 被建模为配置问题；支持减少可选模块和显式证明实际工作负载所需 surface。 |
| xu-074 | Cuckoo page tables | adjacent | memory translation | F | 让 cache 只存优化提示；stale/miss 时回到完整 correctness path 并 refresh，作为 scoped P2 架构案例。 |
| xu-075 | UFC | adjacent | concurrent operations / transformation | F | 云存储协作中推断并变换 operation 以保证 lock-free correctness；能补充操作组合，但领域专用。 |
| xu-076 | P-DIFF | direct | access-control behavior drift | F | 从 access logs 推断 effective policy，连续验证 change 是否 intended，并保留 forensic timeline。 |
| xu-077 | Taiji | adjacent | global traffic control | F | 生产 edge traffic management 体现 feedback control、failover 与 capacity constraint；核心不是通用可靠性研究。 |
| xu-078 | DAOW | none | mobile emulation performance | F | Android 游戏直接模拟主要追求性能。 |
| xu-079 | HoneyCloud | adjacent | threat measurement / defensive design | F | 野外 fileless attack 测量能指导防御，但不直接给出可靠性 protocol。 |
| xu-080 | MVNO study | direct | network measurement / optimization | F | 生产 MVNO 证据显示不同 authority 的晚到更新导致跨实体 divergent views；直接支持 source authority/effective-time seam。 |
| xu-081 | Overlay malware | adjacent | scalable security detection | F | 从市场规模行为特征设计 early detection；能补充防御前移，但属于 malware detection。 |
| xu-082 | Datacenter Network Reliability | direct | failure distribution / resilience | F | 七年生产数据把 network component failure 与 software impact 关联；支持按真实相关性和维修行为设计容错。 |
| xu-083 | Maelstrom | direct | disaster recovery / feedback control | F | 把 inter-service dependencies 与 capacity constraints 编入 drain plan，并用 production drain tests 验证恢复。 |
| xu-084 | Mining Container Images | direct | deployment/config provenance | F | 直接提出用 field deployment combinations 回馈配置 surface、依赖模型与测试优先级；同时声明 image 不是 runtime truth。 |
| xu-085 | Web delta sync | none | cloud-storage efficiency | F | web delta sync 的性能与可扩展性。 |
| xu-086 | Access-denied resolution | direct | operator feedback / security config | F | 试错式解权限问题导致 over-grant；缺少可解释反馈是根因，支持 pinpointing guidance。 |
| xu-087 | PCheck | direct | early/latent config validation | F | 在启动阶段模拟晚用路径，发现会在 failover 等关键路径才显现的 latent config error。 |
| xu-088 | DefDroid | adjacent | platform-level defensive control | F | 平台在 runtime 限制 app 的激进 retry/timer/resource use；支持把防御放入宿主系统而非寄望调用方自律。 |
| xu-089 | NChecker | adjacent | disruption handling | F | 静态发现 app 对 intermittent network 的错误处理；支持 network transition/poor-quality 也进入故障模型。 |
| xu-090 | HCI view of configuration | direct | configuration interface / human factors | F | 文本配置隐含专业管理员假设；配置接口必须提供 guidance、feedback 和适配不同操作者能力。 |
| xu-091 | TrafficGuard | adjacent | mobile proxy optimization | F | 先观测 deployed population 再设计 intervention，并用 field override 分布重校默认值；属于自动控制/人机接口相邻案例。 |
| xu-092 | Offline downloading study | adjacent | network measurement | F | 以真实 cohort bottleneck 选择互补下载路径并公开误判边界；支持测量校准，但不是安全 controller 主证据。 |
| xu-093 | Too Many Knobs | direct | configuration surface design | F | 实际用户数据证明大量 knob 几乎不用；给出删除、隐藏、简化配置空间的直接设计依据。 |
| xu-094 | Config Error Survey | direct | configuration lifecycle | F | 把 prevention/detection/diagnosis/recovery 串成完整问题空间；为 skill 的配置章节提供 taxonomy。 |
| xu-095 | Cloud storage network efficiency | direct | cloud-storage performance | F | 直接给出 measurement-design 方法：区分稳定 factors 与可控 choices，用 field distribution 驱动可复现 controlled benchmark。 |
| xu-096 | EnCore | direct | environment/correlation-aware config | F | 配置正确性依赖 runtime environment 与关联信息；只做 value-local validation 会漏报。 |
| xu-097 | SPEX | direct | design-owned misconfiguration defense | F | 把错误系统反应视为 developer-owned vulnerability，要求推断约束、注入违反并改进错误反馈。 |

分类计数：`direct 54`、`adjacent 39`、`none 4`，总计 `97`。`xu-002` 因正文不可得只算 metadata-level adjacent direction，不计入 unqualified direct evidence。未把同一论文的 journal/conference 两版自动合并；官方目录中的每个条目均保留独立 ID。


## Evidence limits

- Official inventory snapshot: 2026-09-01. Recheck 2026 camera-ready papers before quoting new numbers.
- `F` means the available primary PDF received full-text principle screening; `T` means title/official metadata only. There are no abstract-only rows after the second pass.
- Welder (`xu-002`), MCon (`xu-003`), and Rex TOCS (`xu-005`) primary PDFs were unavailable in this pass. Do not infer mechanisms or evaluation results from titles; use Rex ATC (`xu-017`) for Rex mechanism claims.
- `direct`, `adjacent`, and `none` are routing judgments for this reliability skill, not paper-quality rankings.
