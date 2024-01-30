from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..miose_toolkit_common import CmdOpt, CommandMaster
else:
    from src.miose_toolkit_common import CmdOpt, CommandMaster


def test_command():
    cm = CommandMaster()

    opt_page: CmdOpt = cm.reg_option(
        full_name="page",
        short_name="p",
        info="Page number",
        Type=int,
        default=1,
    )

    @cm.reg_command(route="help", info="Show help info.", options=["page"])
    def _(_options, command_name: str = "help"):
        return f"Show help info of command '{command_name}'. (page: {_options['page']})"

    @cm.reg_command(route="test", info="Test command.", options=[opt_page])
    def _(_options, command_name: str = "test"):
        return f"Test command '{command_name}'. (page: {_options['page']})"

    assert (
        cm.exec(command_text="help test -p 1")
        == "Show help info of command 'test'. (page: 1)"
    )

    opt_test1: CmdOpt = cm.reg_option(
        full_name="test1",
        short_name="t1",
        info="Test option 1",
        Type=str,
        default="",
    )
    opt_test2: CmdOpt = cm.reg_option(
        full_name="test2",
        short_name="t2",
        info="Test option 2",
        Type=str,
        default="",
    )

    @cm.reg_command(
        route="test1",
        info="Test command 1.",
        options=[opt_page, opt_test1, opt_test2],
    )
    def _(_options, command_param1: str = "test1", command_param2: str = "test2"):
        return f"Test command '{command_param1} {command_param2}'. (page: {_options['page']}, test1: {_options['test1']}, test2: {_options['test2']})"

    assert (
        cm.exec(command_text="test1 --test2 test2 --test1 test1 -p 1 param1 param2")
        == cm.exec(command_text="test1 -t2 test2 -t1 test1 -p 1 param1 param2")
        == cm.exec(command_text="test1 -p 1 -t2 test2 -t1 test1 param1 param2")
        == cm.exec(command_text="test1 -p 1 -t1 test1 -t2 test2 param1 param2")
        == cm.exec(command_text="test1 -p 1 param1 param2 -t1 test1 -t2 test2")
        == cm.exec(command_text="test1 -p 1 param1 param2 -t2 test2 -t1 test1")
        == cm.exec(command_text="test1 param1 param2 -p 1 -t1 test1 -t2 test2")
        == "Test command 'param1 param2'. (page: 1, test1: test1, test2: test2)"
    )

    opt_bool: CmdOpt = cm.reg_option(
        full_name="bool",
        short_name="b",
        info="Test bool option",
        Type=bool,
        default=False,
    )

    @cm.reg_command(route="test2", info="Test command 2.", options=[opt_bool])
    def _(_options, command_name: str = "test2"):
        return f"Test command '{command_name}'. (bool: {_options['bool']})"

    assert (
        cm.exec(command_text="test2 name --bool")
        == cm.exec(command_text="test2 -b name")
        == "Test command 'name'. (bool: True)"
    )

    assert cm.exec(command_text="test2 name") == "Test command 'name'. (bool: False)"

    @cm.reg_command(route="parent/sub", info="Test command 3.", options=[opt_bool])
    def _(_options, command_name: str = "parent/sub"):
        return f"Test command '{command_name}'. (bool: {_options['bool']})"

    assert (
        cm.exec(command_text="parent sub name --bool")
        == cm.exec(command_text="parent sub -b name")
        == "Test command 'name'. (bool: True)"
    )

    assert cm.gen_desc()
    assert cm.gen_short_desc()

    # 显示指令帮助
    # print("commands:")
    # print(cm.gen_short_desc())
    # print()
    # print("commands full description:")
    # print(cm.gen_desc())
