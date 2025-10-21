实验1/2 练习题代码设计及编写
一、实验目的
1、熟悉面向对象口软件构造的技术。
2、掌握类的编写、基类与子类派生的方法。
3、熟练掌握UML类图设计工具
4、能够按照功能单一原则，里氏转换原则和依赖倒转原则处理本构造。
5、能够进行JUnit单元测试进行核心逻辑代码测试
6、熟悉git代码管理工具。
二、实验任务
1.加，减法根据需要生成，纯加法或纯减法，混合加减法
2.可选择进行2个数纯加、纯减、加减法混合或3个数混合加减
3.运算结果，及三个数的中间结果>0,<100，正整数；参与运算数据也需>0,<100，正整数
4.生成数量可控制，如50，80道。
5.在加减法的基础上添加乘除法运算，可选择进行纯加、纯减、纯乘法、纯除法、加减法混合运算，乘除法混合运算，三个数加减乘除混合运算。运算结果，及三个数的中间结果>0,<100，正整数；参与运算数据也需>0,<100，正整数
6.输出数量及格式可设定，如30道题，每行5列展示，保存至CSV（逗号分隔值文件格式）格式文件中。
7.编写Junit测试相关代码，测试自己的核心功能
8.将编写的代码上传到自己的远程代码库中（附加题，如完成有加分，需要注册远程仓库，并上传）
三、实验要求
1. 项目要添加适当的注释，项目代码的书写要采用缩进格式。
2. 项目要具备一定的健壮性，即当输入数据非法时，页面也能适当地做出反应。
3. 项目要做到界面友好，在项目运行时用户可以根据相应的提示信息进行操作。
四、实验设计（设计思路、核心代码）
1. 整体设计：以面向对象的方式拆分为 `operations.py`（定义四则运算枚举及统一求值接口）、`expression.py`（封装算式与逐步求值过程）、`generator.py`（根据配置随机生成合法算式）和 `cli.py`（负责命令行参数解析及CSV落盘）。配置通过 `GeneratorConfig` 统一约束运算符集合、操作数个数、数值范围等参数，并支持注入随机种子保证结果可复现。
2. 生成策略：生成算式时先随机确定首个操作数，再逐步为每一步选择运算符对应的合法操作数集合，只接受能保证中间值与最终结果均落在 (0,100) 的候选，从而满足题目约束。乘除法通过搜索因子/约数确保乘积与商均为整数且不越界。
3. 命令行与输出：`python -m arithmetic_generator.cli --count 30 --operations add,sub,mul,div --operands 2,3 --columns 5 --output output/practice.csv --seed 42` 可生成混合题目并导出CSV；支持 `--include-results` 控制是否在题目后附带答案。
4. 核心代码片段：
```python
    def _valid_operands(self, current: int, operation: Operation) -> Tuple[int, ...]:
        if operation is Operation.ADD:
            upper = self._config.max_value - current
            return tuple(range(self._config.min_value, upper + 1)) if upper >= self._config.min_value else tuple()
        if operation is Operation.SUB:
            upper = current - self._config.min_value
            return tuple(range(self._config.min_value, current)) if upper >= self._config.min_value else tuple()
        if operation is Operation.MUL:
            upper = self._config.max_value // current if current else 0
            return tuple(range(self._config.min_value, upper + 1)) if upper >= self._config.min_value else tuple()
        candidates = [d for d in range(self._config.min_value, self._config.max_value + 1)
                      if d and current % d == 0 and self._config.min_value <= current // d <= self._config.max_value]
        return tuple(candidates)
```
七、思考题
1. 单一职责原则体现在算式求值、合法性判定与CSV输出各占独立模块，互不耦合；里氏替换原则通过 `Operation` 枚举统一提供 `apply` 接口，新增运算时无需修改调用端即可替换；依赖倒转原则借由 `GeneratorConfig` 让高层逻辑依赖抽象配置而非具体实现，命令行层只感知配置和接口，不直接操作底层生成细节。
八、总结（经验教训，遇到的问题及解决方法，待解决的问题）
1、问题与原因：初始计划使用Java/JUnit，但实验环境缺少JDK，遂改用Python实现；单元测试首次运行出现“Start directory is not importable”错误，原因是 `tests` 目录未显式声明为包。
2、规避方法：在无法安装运行环境时提前确认依赖并调整实现语言；编写测试前创建 `tests/__init__.py` 或使用 `python -m unittest discover -s tests` 规范启动方式，避免因包结构导致的发现失败。后续可补充更多边界条件测试（如仅除法、极限数值）与UML图以完善文档。
