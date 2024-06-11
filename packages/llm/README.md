# Miose Toolkit 工具箱: LLM 子项目

## 介绍

LLM 子项目包含了一个对各种大语言模型进行了封装调用的方法，并提供一系列构造 LLM 项目的常用工具。

## 测试用例库 -> [用例库](./src/tests)

测试用例库中包含了所有模块的测试用例，可以参考其中的代码来使用模块。

## 功能列表

### 1. LLM 组件化框架 [测试用例](./src/tests/test_adapter.py)

LLM 组件化框架提供了一种基于组件的架构，可以方便地实现各种功能模块的组合，并提供统一的接口来调用。

```python
from miose_toolkit_llm import (
    BaseScene,
    BaseStore,
    Runner,
)
from miose_toolkit_llm.clients.openai import OpenAIChatClient
from miose_toolkit_llm.prompts.openai import OpenAIPromptCreator, SystemMessage, UserMessage, AiMessage
from miose_toolkit_llm.components import (
    BaseComponent,   # 基础组件
    VecHistoryComponent,  # 支持向量数据库检索的消息记录组件
    VecFunctionComponent, # 支持向量数据库检索的方法组件
    JsonResolveComponent,    # JSON 解析组件
    TextComponent,        # 文本提示词组件
)
from miose_toolkit_llm.tools.vector_db import ChomaVecDb
from miose_toolkit_llm.tools.tokenizers import TikTokenizer
from miose_toolkit_llm.exceptions import (
    ComponentExecutionError,
    ComponentError,
    ResolveError,
    TokenizationError,
    SceneRunningError,
)

# 1. 构造一个应用场景

class Scene(BaseScene):
    """场景类"""

    class Store(BaseStore):
        """场景数据源类"""
        history_key = "history"
        character = "艾丽娅"

scene = Scene()
store = scene.store # 可获取场景数据源

# 2. 准备场景组件
vec_histories = VecHistoryComponent(scene=scene).setup(use=ChomaVecDb)  # 使用向量数据库检索的消息记录组件
vec_functions = VecFunctionComponent(scene=scene).setup(use=ChomaVecDb) # 使用向量数据库检索的方法组件

@vec_functions.register(name="更新玩家属性")
def update_player_attribute(scene: "Scene", attr: str, value: str) -> str:
    """更新玩家属性

    Args:
        scene (Scene): 场景对象
        attr (str): 属性名称
        value (str): 属性值

    Returns:
        str: 响应消息
    """
    try:
        scene.store().set(attr, value)
    except Exception as e:
        raise ComponentExecutionError("更新玩家属性失败") from e
    return f"玩家属性 {attr} 已更新为 {value}"


class ActionResponse(JsonResolveComponent):
    """自定义动作响应器"""

    reaction: str = ""
    options: List[str] = []

    # 根据需要覆写 example 方法来生成解析结果示例，未覆写则直接使用默认值
    def example(self, random: bool = False) -> str:
        return '{"reaction": "你好，欢迎来到魔法世界！你的第一个动作是什么？", "options": ["打开魔法书", "查看地图", "查看物品"]}'


class CustomResponseResolver(JsonResolveComponent):
    """自定义结果解析器"""

    action: ActionResponse
    function: VecFunctionComponent   # 先定义基础组件，拿到响应后再用 vec_functions 来解析

resolver = CustomResponseResolver()

# custom_component = CustomComponent()  # 自定义组件 (需要继承 BaseComponent，实现 render_prompt 方法)

# 3. 构造 OpenAI 提示词
prompt_creator = OpenAIPromptCreator(
    SystemMessage(
        "你是一个文字冒险游戏的 GM，你会根据玩家的动作来编写合适的剧情发展，并且你的所有回复都必须满足 json 格式",
        "你可以使用以下方法来处理场景：",
        vec_functions.bind(store_key="game_functions", num=1),  # 可传递参数给组件，来指定渲染 prompt 逻辑
        "你的响应结果应该符合以下格式：",
        resolver.example(random=True),  # 随机生成一个解析结果示例
        sep="\n\n"  # 自定义构建 prompt 的分隔符 默认为 "\n"
    ),
    UserMessage(
        vec_histories.bind(store_key="history_key", num=1),    # 可传递参数给组件，来指定渲染 prompt 逻辑
        TextComponent("我想扮演一位 {character}，生活在一个魔法世界中，我的第一个行为是醒来，请开始游戏", src=store),   # 可手动指定渲染数据源，否则使用场景数据源
    ),
    # 生成使用的参数
    temperature=0.3,
    max_tokens=1000,
    presence_penalty=0.3,
    frequency_penalty=0.5,
)

scene.attach_runner(    # 为场景绑定 LLM 执行器
    Runner(
        client=OpenAIChatClient(model="gpt-3.5-turbo"), # 指定聊天客户端
        tokenizer=TikTokenizer(model="gpt-3.5-turbo"),  # 指定分词器
        prompt_creator=prompt_creator,
    ),
)


# 4. 获取结果与解析
try:
    result = scene.run()
    result.raw_text # 原始结果文本
except SceneRunningError as e:
    print(e)

try:
    resolved_result = result.resolve(resolver=resolver)  # 解析结果 (可指定解析器)
    function_result = resolved_result.function_result  # 解析结果中的方法调用结果
except ResolveError as e:
    print(e)

try:
    function_result.execute()  # 执行方法调用结果
except ComponentExecutionError as e:
    print(e)

resolved_result.action_result.reaction  # 结果: 你好，欢迎来到魔法世界！你的第一个动作是什么？

# 5. 反馈与保存数据 (可选)
result.save(prompt_file="prompt.txt", result_file="result.json") # 保存响应提示词和结果到文件 (可选)
result.feedback(rate=5) # 反馈生成质量到数据平台 (可选)
```
