# Repository Guidelines

## Project Structure & Module Organization
- 保持实验简介 `wantto.md` 同步，将额外文档按需扩展到 `docs/`。
- 业务代码放在 `src/arithmetic_generator/`，按功能拆分模块（如 `generator.py`、`cli.py`、`expression.py`）。
- 测试代码放在 `tests/`，必要时在 `tests/resources/` 存放测试数据。
- UML 图与CSV示例放入 `assets/`，确保设计产出与程序结果可追踪。

## Build, Test, and Development Commands
- 创建虚拟环境后运行：`pip install -r requirements.txt`（若后续添加依赖）。
- 执行核心测试：`PYTHONPATH=src python3 -m unittest discover -s tests -t .`。
- 生成练习题CSV：`PYTHONPATH=src python3 -m arithmetic_generator.cli --count 30 --operations add,sub,mul,div --operands 2,3 --columns 5 --output output/practice.csv --seed 42`。
- 生成带答案文件追加 `--include-results` 选项。

## Coding Style & Naming Conventions
- 使用 Python 3.9+，保持 4 空格缩进，单行不超过 110 字符。
- 模块、包名使用下划线风格；类名 UpperCamelCase；函数/变量 lower_case_with_underscores。
- CSV 输出、随机生成逻辑放在专属函数中，避免 CLI 中混写业务逻辑。
- 提交前运行 `ruff` 或 `flake8`（待项目引入）保证风格一致。

## Testing Guidelines
- 使用 `unittest` 编写用例，命名格式 `test_*`，每个测试聚焦单一行为。
- 使用固定随机种子或控制输入数据，保证测试可复现。
- 覆盖生成逻辑（边界数值、纯除法）、CLI 参数解析与输出格式。
- 将未来的集成测试放入 `tests/integration/` 并标记运行耗时。

## Commit & Pull Request Guidelines
- 采用 Conventional Commits：`feat:`, `fix:`, `test:`, `docs:` 等。
- 提交信息包含修改范围与动机；PR 说明应补充测试记录和截图/CSV 样例。
- 新增功能需同步更新 `wantto.md` 的相关实验说明。
- CI 全绿后再请求合并，未完成事项用 TODO 并附追踪 Issue。

## Documentation & UML Expectations
- 类结构变化后更新 `assets/uml/` 下的 `.plantuml` 与导出图。
- 新增参数或命令时，在 `docs/configuration.md` 记录默认值与校验规则。
- 面向授课总结的经验、问题与改进建议统一沉淀到 `docs/roadmap.md`。
