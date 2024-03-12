import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union

from .list import advance_split

_FORBIDDEN_CHARACTERS = [
    " ",
    "\t",
    "\n",
    "\r",
    "\v",
    "\f",
    "\0",
    "\\",
    '"',
    "'",
    "=",
    ":",
    "|",
    ">",
    "<",
    "&",
    ";",
    "!",
    "@",
    "#",
    "$",
    "%",
    "^",
    "*",
    "(",
    ")",
    "+",
    "[",
    "]",
    "{",
    "}",
    "?",
    "/",
    "`",
    "~",
    ",",
    ".",
]


class CmdOpt:
    def __init__(
        self,
        full_name: str,
        short_name: str,
        info: str,
        Type: Union[Type[bool], Type[str], Type[int], Type[float]],
        default: Any = None,
    ):
        # 检查参数类型是否正确
        if default is None:
            default = False if Type == bool else None

        # 特殊字符检查
        for char in _FORBIDDEN_CHARACTERS:
            if char in full_name:
                raise ValueError(
                    f"The full name of an option should not contain '{char}'.",
                )
            if char in short_name:
                raise ValueError(
                    f"The short name of an option should not contain '{char}'.",
                )

        self.full_name = full_name
        self.short_name = short_name
        self.info = info
        self.Type = Type
        self.default = default

    def match(self, s: str) -> bool:
        """判断字符串是否匹配选项

        Args:
            s (str): 字符串

        Returns:
            bool: 是否匹配
        """

        return s == f"--{self.full_name}" or s == f"-{self.short_name}"

    def has_value(self) -> bool:
        """判断选项是否需要值

        Returns:
            bool: 是否需要值
        """

        return self.Type != bool

    def gen_format(self, short: bool = False) -> str:
        """生成选项格式化字符串

        Returns:
            str: 选项格式化字符串
        """

        if short:
            return (
                f"[-{self.short_name}]"
                if self.Type == bool
                else f"[-{self.short_name} <{self.short_name}>]"
            )
        return (
            f"[--{self.full_name}]"
            if self.Type == bool
            else f"[--{self.full_name} <{self.full_name}>]"
        )


class _CommandParam:
    def __init__(
        self,
        name: str,
        Type: Union[Type[str], Type[int], Type[float]],
        default: Any,
    ):
        self.name = name
        self.Type = Type
        self.default = default

    def gen_format(self) -> str:
        """生成参数格式化字符串

        Returns:
            str: 参数格式化字符串
        """

        if self.Type == bool:
            return f"[{self.name}]"
        return f"<{self.name}>"


def _get_func_param_info(func) -> List[_CommandParam]:
    """获取函数的参数信息

    Args:
        func (Callable): 函数

    Returns:
        List[_CommandParam]: 函数的参数对象列表
    """

    sig = inspect.signature(func)
    params = sig.parameters

    param_info = []
    for param in params.values():
        if param.name == "self" or param.name == "cls" or param.name == "_options":
            continue

        param_info.append(
            _CommandParam(
                param.name,
                param.annotation,
                param.default,
            ),
        )

    return param_info


class _Command:
    def __init__(
        self,
        route: str,
        info: str,
        options: List[CmdOpt],
        callback: Callable,
        params: Optional[List[_CommandParam]] = None,
    ):
        self.route: str = route
        self.info: str = info
        self.options: List[CmdOpt] = options
        self._callback: Callable = callback
        self.params: List[_CommandParam] = params if params else []

    def format(self, short: bool = False) -> str:
        """获取命令的格式化字符串

        Returns:
            str: 命令的格式化字符串
        """

        res = f"{self.route.replace('/', ' ')} "
        res += " ".join([option.gen_format(short) for option in self.options]) + " "
        res += " ".join([param.gen_format() for param in self.params])
        return res

    def desc(self) -> str:
        """获取命令的描述信息

        Returns:
            str: 命令的描述信息
        """

        res = f"Command: {self.route}\n"
        res += f"  Format: {self.format()} \n"
        res += f"  Description: {self.info}\n"
        res += "  Options: \n"
        for option in self.options:
            res += f"    --{option.full_name} (-{option.short_name})\n"
            res += f"        {option.info}\n"
        return res

    def short_desc(self) -> str:
        """获取命令的简短描述信息

        Returns:
            str: 命令的简短描述信息
        """

        res = f"Command: {self.format(short=True)}\n"
        res += f"  Description: {self.info}\n"
        return res

    def run(self, *args, **kwargs) -> Any:
        return self._callback(*args, **kwargs)

    def __str__(self) -> str:
        return f"<Command {self.route}>"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, _Command):
            return False
        return self.route == o.route


class CommandMaster:
    """命令行解析器

    用于解析命令行参数并执行对应的命令

    Examples:
        >>> master = CommandMaster()
        >>> master.reg_option("page", "p", "Show page number.", int, 1)
        >>> @master.reg_command("help", "Show help info.")
        ... def help(_options, command_name: str = "help"):
        ...     print(_options) # {'page': 1}
        ...     print(f"Show help info of command '{command_name}'. (page: {_options['page']})")
        ...     return "Help Info"
        >>> res = master.exec("help test -p 1")   # Show help info of command 'test'. (page: 1)
        >>> print(res)    # Help Info
    """

    def __init__(self) -> None:
        self._options: Dict[str, CmdOpt] = {}
        self._options_short: Dict[str, CmdOpt] = {}

        self._commands: Dict[str, _Command] = {}

    def reg_option(
        self,
        full_name: str,
        short_name: str,
        info: str = "No help info.",
        Type: Union[Type[bool], Type[str], Type[int], Type[float]] = bool,
        default: Any = None,
    ):
        """注册一个命令行选项

        Args:
            full_name (str): 选项的全名 (e.g. help)
            short_name (str): 选项的简称 (e.g. h)
            info (str, optional): 选项的帮助信息. Defaults to "No help info.".
            Type (Union[Type[bool], Type[str], Type[int], Type[float]], optional): 选项的类型. Defaults to bool.
            default (Any, optional): 选项的默认值. Defaults to None.
        """

        option = CmdOpt(
            full_name,
            short_name,
            info,
            Type,
            default,
        )

        if option.full_name in self._options:
            raise ValueError(
                f"The full name of option '{option.full_name}' has been registered.",
            )
        if option.short_name in self._options_short:
            raise ValueError(
                f"The short name of option '{option.short_name}' has been registered.",
            )

        self._options[option.full_name] = option
        self._options_short[option.short_name] = option

        return option

    def reg_command(
        self,
        route: str,
        info: str = "No help info.",
        options: Optional[List[Union[CmdOpt, str]]] = None,
    ) -> Callable[[Callable], Callable]:
        """注册一个命令

        Args:
            route (str): 命令路由 以 / 分割 (e.g. help/test)
            info (str, optional): 命令的帮助信息. Defaults to "No help info.".
            options (Optional[List[Union[CmdOpt, str]]], optional): 命令的选项列表. Defaults to None.

        Returns:
            Callable[[Callable], Callable]: 命令装饰器
        """

        options = options if options else []
        for idx, option in enumerate(options):
            if isinstance(option, str):
                option_obj = self._options.get(f"{option}")
                if option_obj is None:
                    raise ValueError(
                        f"The option '{option}' has not been registered.",
                    )
                options[idx] = option_obj
            elif isinstance(option, CmdOpt) and option.full_name not in self._options:
                raise ValueError(
                    f"The option '{option.full_name}' has not been registered.",
                )

        def command_decorator(func) -> Callable:
            nonlocal options
            if route in self._commands:
                raise ValueError(
                    f"The route '{route}' has been registered.",
                )

            if options is None:
                options = []

            params = _get_func_param_info(func)

            self._commands[route] = _Command(
                route,
                info,
                options,  # type: ignore
                func,
                params,
            )

            # 根据路由段长度降序排序命令便于匹配
            self._commands = dict(
                sorted(
                    self._commands.items(),
                    key=lambda x: len(x[0].split("/")),
                    reverse=True,
                ),
            )

            return func

        return command_decorator

    def exec(self, command_text: str) -> Any:
        """命令解析器 从命令文本中解析出命令对象信息

        Args:
            command_text (str): 命令文本

        Returns:
            Any: 命令执行结果

        Raises:
            ValueError: 命令解析失败
        """

        # 解析命令
        command_split = advance_split(command_text, " ", True)

        for route, command in self._commands.items():
            route_split = advance_split(route, "/")

            # 匹配命令路由
            if len(route_split) > len(command_split) or route != "/".join(
                command_split[: len(route_split)],
            ):
                continue

            # 获取到命令对象后开始解析选项
            options: Dict[str, Any] = {}
            params: Dict[str, Any] = {}
            params_tmp_list: List[str] = []

            # 先填充默认值
            for option in command.options:
                options[option.full_name] = option.default

            command_split = command_split[len(route_split) :]

            # 解析选项
            i = 0
            while i < len(command_split):
                option: CmdOpt
                for opt in self._options.values():
                    if opt.match(command_split[i]):
                        option = opt
                        break
                else:
                    params_tmp_list.append(command_split[i])
                    i += 1
                    continue

                if option.has_value():
                    if i + 1 >= len(command_split):
                        raise ValueError(
                            f"Option '{option.full_name}' needs a value.",
                        )
                    options[option.full_name] = option.Type(
                        command_split[i + 1],
                    )
                    i += 1
                else:
                    options[option.full_name] = True
                i += 1

            # 解析参数
            for i in range(len(command.params)):
                if i >= len(params_tmp_list):
                    break
                params[command.params[i].name] = command.params[i].Type(
                    params_tmp_list[i],
                )

            # 检查是否有多余的参数
            if len(params_tmp_list) > len(command.params):
                raise ValueError(
                    f"Too many parameters for command '{command.route}'.",
                )

            return command.run(_options=options, **params)

        else:
            raise ValueError(f'Command "{command_text[0]}" Not Found.')

    def gen_short_desc(self) -> str:
        """生成所有命令的简短描述信息

        Returns:
            str: 所有命令的简短描述信息
        """

        res = ""
        for command in self._commands.values():
            res += command.short_desc()
        return res

    def gen_desc(self) -> str:
        """生成所有命令的描述信息

        Returns:
            str: 所有命令的描述信息
        """

        res = ""
        for command in self._commands.values():
            res += command.desc()
        return res
