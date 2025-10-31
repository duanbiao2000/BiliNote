<!-- 9b080a5d-a4d2-4d9d-8c6b-d1e15e3d3004 89e20ad7-5946-4743-9bda-e5a99f510a98 -->
# 质量稳定与文档规范落地计划

## 目标

- 提升后端/前端的可测试性与稳定性（单元/集成测试、错误处理、可观测性）
- 建立团队统一的代码规范与贡献流程文档
- 不涉及上线与部署，更聚焦功能与质量

## 范围

- 后端（FastAPI）与前端（React/Vite）代码质量与开发者体验
- 文档与规范（贡献指南、代码风格、测试与运行指南）

## 实施内容

### 1) 测试体系搭建（优先）

- 后端
- 引入/完善 pytest 结构与样例：`backend/tests/`
- 单元测试：`app/services/note.py`（状态机/缓存/错误传播）、`app/routers/note.py`（参数校验与响应协议）
- 领域组件 mock：下载器/转写器/GPT 工厂（避免真实网络/大模型/ffmpeg）
- API 合同测试：用 `httpx.AsyncClient` 对 `/generate_note`、`/task_status/{id}` 做集成测试（使用临时目录与 SQLite 临时库）
- 前端
- 引入 Vitest + React Testing Library 基础：`BillNote_frontend/src/__tests__/`
- 测试 `hooks/useTaskPolling.ts`（状态变迁）、`services/note.ts`（错误分支与重试）、`NoteForm`（校验与 payload 组装）

### 2) 错误处理与重试/超时策略

- 后端
- 在 `NoteGenerator` 的三个阶段（下载/转写/GPT）加入幂等与指数退避重试（如 3 次），并设置阶段性超时
- 丰富 `TaskStatus` 的失败原因（错误码/简短消息），统一 `ResponseWrapper` 错误格式
- 将状态文件写入失败的回退路径统一封装（已有原子写，补充异常分支日志）
- 前端
- 在 `useTaskPolling` 遇到后端失败时的降级提示与“重试任务”入口优化
- `MarkdownViewer` 的失败态与半成功（状态缺失/结果缺失）兜底文案

### 3) 可观测性与日志

- 后端
- 结构化日志（JSON 可选）、在 `lifespan`/路由中注入 `X-Request-ID` 并贯穿日志
- 关键阶段打点与耗时：下载/转写/总结/保存，关联 `task_id`
- 错误分级：输入错误（4xx）/服务错误（5xx）/第三方错误（provider）
- 前端
- 将关键用户操作与接口失败在开发态打印并可切换静默模式

### 4) 文档与规范

- 在仓库根或相关目录新增：
- `CONTRIBUTING.md`：分支策略、提交流程、代码评审要点（含“教育性注释”范例）
- `CODE_STYLE.md`：Python/TS 命名与结构、日志与错误处理规范、注释规范
- `TESTING.md`：如何本地运行后端/前端测试、mock 策略、覆盖率目标
- 在 `doc/学习教程.md` 增补“如何运行测试/如何做 Code Review”章节链接

### 5) 代码质量工具（仅本地）

- 后端：Black + Ruff 基础规则；`pyproject.toml` 配置
- 前端：ESLint（已存在）+ Prettier 协同，统一 ignore 与格式化脚本
- EditorConfig：统一缩进与换行
- pre-commit 钩子：格式化与静态检查（不引入 CI，留本地使用）

## 关键文件（部分）

- 后端：`backend/app/services/note.py`、`backend/app/routers/note.py`、`backend/app/downloaders/*`、`backend/app/transcriber/*`、`backend/app/gpt/*`
- 前端：`BillNote_frontend/src/hooks/useTaskPolling.ts`、`BillNote_frontend/src/services/note.ts`、`BillNote_frontend/src/pages/HomePage/components/NoteForm.tsx`
- 文档：`CONTRIBUTING.md`、`CODE_STYLE.md`、`TESTING.md`、`doc/学习教程.md`

## 交付物

- 覆盖核心链路的后端/前端测试样例与可运行脚本
- 统一的错误返回规范与日志规范
- 团队贡献与风格指南文档

## 验收

- 本地一次命令完成后端/前端测试均通过
- 生成任务的失败路径可读可解释（错误码/消息/日志关联 task_id）
- PR 模板与评审要点生效，新增功能附带最小测试

### To-dos

- [ ] 搭建 pytest 并为 note 路由与服务编写测试
- [ ] 配置 Vitest 并为 hooks/services/components 编写测试
- [ ] 为下载/转写/GPT 增加重试与超时机制
- [ ] 引入请求ID与结构化日志，完善阶段打点
- [ ] 撰写 CONTRIBUTING.md 与 CODE_STYLE.md
- [ ] 撰写 TESTING.md 并在教程中添加链接
- [ ] 配置 Black/Ruff 与 Prettier/EditorConfig/pre-commit