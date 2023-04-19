import sys
import linecache
import dis
from typing import List, TextIO, Any, Type, Optional, Tuple, Dict
from types import CodeType
from traceback import TracebackType


class LFTracer():
    def __init__(self, target_func: List[str] = [], list_func: bool = False, file: TextIO = sys.stdout) -> None:
        self.target_func = target_func
        self.list_func = list_func
        self.file = file
        self.statements_map = {}

    def trace_lines(self, frame: Any, event: str, arg: Any):
        if event == 'line':
            lineno = frame.f_lineno
            code = frame.f_code
            filename = code.co_filename
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                filename = filename[:-1]
            line = linecache.getline(filename, lineno)
            if line.strip() and code.co_name in self.target_func:
                if filename not in self.statements_map:
                    self.statements_map[filename] = {}
                instructions = dis.get_instructions(line)
                for instruction in instructions:
                    statement = (instruction.opcode, instruction.arg)
                    if statement not in self.statements_map[filename]:
                        self.statements_map[filename][statement] = 0
                    self.statements_map[filename][statement] += 1

    def trace_lines(self, frame: Any, event: str, arg: Any):
        if event == 'line':
            lineno = frame.f_lineno
            code = frame.f_code
            filename = code.co_filename
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                filename = filename[:-1]
            line = linecache.getline(filename, lineno)
            if line.strip() and code.co_name in self.target_func:
                if filename not in self.statements_map:
                    self.statements_map[filename] = {}
                # reset statements_map if the function is called again
                if code.co_name in self.statements_map[filename]:
                    self.statements_map[filename][code.co_name] = {}
                instructions = dis.get_instructions(line)
                for instruction in instructions:
                    statement = (instruction.opcode, instruction.arg)
                    if statement not in self.statements_map[filename][code.co_name]:
                        self.statements_map[filename][code.co_name][statement] = 0
                    self.statements_map[filename][code.co_name][statement] += 1

    def __enter__(self) -> Any:
        sys.settrace(self.trace_lines)
        return self

    def __exit__(self, exc_tp: Type, exc_value: BaseException, exc_traceback: TracebackType) -> Optional[bool]:
        sys.settrace(None)
        return None

    def getLFMap(self) -> Dict[str, Dict[str, Dict[Tuple[int, Any], int]]]:
        return self.statements_map

    def __enter__(self) -> Any:
        sys.settrace(self.trace_lines)
        return self

    def __exit__(self, exc_tp: Type, exc_value: BaseException, exc_traceback: TracebackType) -> Optional[bool]:
        sys.settrace(None)
        return None

    def getLFMap(self) -> Dict[str, Dict[Tuple[int, Any], int]]:
        return self.statements_map
