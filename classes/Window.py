#!/usr/bin/env python3

import pytermgui as ptg
from abc import ABC, abstractmethod
import os
from typing import Dict


class Window(ABC):
    @abstractmethod
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        pass

    def loadNamespace(self, path: str) -> ptg.WidgetNamespace:
        loader = ptg.YamlLoader()
        namespace: ptg.WidgetNamespace = None
        with open(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "windows",
                    f"{path}.yaml",
                ), "r"
        ) as f:
            namespace = loader.load(f)
        return namespace

    @abstractmethod
    def getNamespace(self) -> ptg.WidgetNamespace:
        pass

    @property
    @abstractmethod
    def buttons(self) -> Dict[str, ptg.Widget]:
        pass
