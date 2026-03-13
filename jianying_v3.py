# -*- coding: utf-8 -*-
"""
宇辰剪映小助手 优化版（无闪烁）
功能：从API获取草稿数据，下载素材并生成剪映可识别的草稿文件。
"""

import platform
import sys

# 优先在程序一开始就设置 Windows DPI 感知，避免窗口创建后再被系统重绘一次导致闪烁
if platform.system() == 'Windows':
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        # 忽略失败，不影响程序主体功能
        pass

import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import json
import time
import os
import uuid
import shutil
import traceback
import re
from urllib.parse import urlparse
import copy
import threading
import hashlib
import subprocess
import urllib.request
import base64
import tempfile
from PIL import Image, ImageTk
EMBEDDED_ICON_BASE64 = "AAABAAEAgIAAAAEAIAAoCAEAFgAAACgAAACAAAAAAAEAAAEAIAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMCgcA2bx8AMGobgfTt3kt2759ZOTFgpTpyoW06MmEwufJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExefJhMXoyYTC6cqFtOTFgpTbvn1k07d5LcGobgfZvHwADAoHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3sB/AMascQvavX1O58mEp+zNh+Puzoj68NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+7OiPrszYfj58mEp9q9fU7GrHEL3sB/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsJllAGRXOgHXuns258iEru7OiPXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7s6I9efIhK7Xuns2ZFc6AbCYZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMarcQCzm2YF3sF/Y+zMh+Pw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+zMh+PewX9js5tmBcarcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADFqnAAsJhkBuHDgHbuzojz8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+7OiPPhw4B2sJhkBsWqcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAs5tmACEcEgHfwX9q7s6I9PDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+7OiPTfwX9qIR0SAbObZgAAAAAAAAAAAAAAAAAAAAAAAAAAAGhbOwD11IwA2bx8Q+zNh+jw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+zNh+jZvXxD9dSMAGhaOwAAAAAAAAAAAAAAAAAAAAAA07d4AMyxdRPoyYW+8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGJ//DRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+jJhb7MsXUT07d4AAAAAAAAAAAAAAAAAI57UQD/6poA38F/Z+/PiPvw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0ov/8NCL/+zMhv/pyIL/6ciA/+rJgv/tzYf/8NGL//HSjP/x0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/78+I+9/Bf2f/6poAjntRAAAAAAAAAAAAz7N2AMuwdBHqy4XE8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yv/68uF/9OtZv+2ij//p3gn/6V0H/+mdB3/qHgg/66AKf+8kT7/0qxg/+bFff/w0Ir/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/6suFxMuwdBHPs3YAAAAAAAAAAADmx4MA2rx8Ru7OiPXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGK/9m1b/+rfDD/kFsI/4xWAP+OWAD/kFsA/5JdAP+UXwD/lmEA/5hjAP+caAT/qnkZ/8SZQ//gvXL/8NCK//HRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/uzoj12rx8RubHgwAAAAAAfW1IAP//rQDjxYKE8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/NpmD/lWEU/4hRAP+LVAH/jVcB/49ZAf+RWwH/k10B/5VgAf+XYgH/mWQB/5pmAf+cZwD/nmkA/6h2EP/Gm0L/5cJ4//HRi//w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/jxYKE//+tAH1tSADFq3EAwKZtB+rLhrbw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yr/zqdh/5BbEP+GTwD/iVIB/4pUAf+MVgH/jlgB/5BbAf+SXQH/lF8B/5ZhAf+YYwH/mmUB/5xoAf+eagH/oGsA/6JuAf+wfxj/0KhS/+vKgv/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+rLhrbApm0HxatxANG1dwDStngV7MyH1PDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8dGK/926dv+UYRn/g0sA/4ZPAf+IUQH/ilQB/4xWAf+OWAH/kFoB/5JcAf+UXgH/lmEB/5hjAf+aZQH/m2cB/55pAf+fawH/oW0B/6NvAP+mcwT/u4wo/9u2Zf/uzoj/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7MyH1NK2eBXRtXcA1Lh5ANS3eSDszIfh8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/uzoj/r4I+/4FJAP+DTAH/hU8B/4dRAf+JUwH/i1UB/41XAf+PWQH/kVwB/5NeAf+VYAH/l2IB/5lkAf+bZgH/nWgB/59rAf+hbQH/o28B/6VxAf+mcgD/rHoJ/8SYN//jwHP/8NGL//DRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/szYfh1Lh5INS4eQDQtHYAzrN2JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8dGK/9q2cv+LVhH/gEgA/4NMAf+FTgH/h1AB/4lSAf+KVAH/jFYB/45ZAf+QWwH/kl0B/5RfAf+WYQH/mGMB/5pmAf+caAH/nmoB/6BsAf+ibgH/pHAB/6ZyAf+odAH/qXYA/7SDE//Qp0v/6sh+//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yv/upBM/35HAf+ASQH/gksB/4RNAf+GTwH/iFEB/4pUAf+MVgH/jlgB/5BaAf+SXAH/lF4B/5ZhAf+YYwH/mmUB/5xnAf+daQH/n2sB/6FtAf+jcAH/pXIB/6d0Af+pdgH/q3gA/617Av++jyH/27Vf/+7Ohv/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+rKhf+baij/fEQA/39IAf+BSgH/g0wB/4VPAf+HUQH/iVMB/4tVAf+NVwH/j1kB/5FcAf+TXgH/lWAB/5diAf+ZZAH/m2YB/51pAf+fawH/oW0B/6NvAf+lcQH/p3MB/6l1Af+reAH/rHoB/657AP+zgQj/yJwy/+O/bv/w0Ir/8NGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yr/27l2/4dSEf98RAD/f0cB/4FKAf+DTAH/hU4B/4dQAf+JUgH/i1QB/41XAf+PWQH/kVsB/5NdAf+UXwH/lmEB/5hkAf+aZgH/nGgB/55qAf+gbAH/om4B/6RxAf+mcwH/qHUB/6p3Af+seQH/rnsB/7B9Af+xfwD/uokQ/9GoRP/px3v/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//LSi//Mp2X/fkcG/3xEAf9+RwH/gEkB/4JLAf+ETQH/hlAB/4hSAf+KVAH/jFYB/45YAf+QWgH/klwB/5RfAf+WYQH/mGMB/5plAf+cZwH/nmkB/6BsAf+ibgH/pHAB/6ZyAf+odAH/qXYB/6t5Af+tewH/r30B/7F/Af+zgQD/tYMB/8GSG//btFj/7c2E//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8tKL/76WVv96QgL/fEQB/35GAf+ASAH/gksB/4RNAf+GTwH/iFEB/4pTAf+LVQH/jlcB/49aAf+RXAH/k14B/5VgAf+XYgH/mWQB/5tnAf+daQH/n2sB/6FtAf+jbwH/pXEB/6d0Af+pdgH/q3gB/616Af+vfAH/sX4B/7OBAf+1gwH/toQA/7qJBf/Kniv/4r5o/+/PiP/w0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0ov/toxM/3hAAP97QwH/fUUB/39IAf+BSgH/g0wB/4VOAf+HUAH/iVIB/4tUAf+NVwH/j1kB/5FbAf+TXQH/lV8B/5dhAf+ZZAH/mmYB/5xoAf+eagH/oGwB/6JvAf+kcQH/pnMB/6h1Af+qdwH/rHkB/657Af+wfgH/soAB/7SCAf+2hAH/uIYB/7mHAP+/jwv/06k9/+jGdv/w0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HRi/+vhUX/dz8A/3pCAf98RQH/fkcB/4BJAf+CSwH/hE0B/4ZPAf+IUgH/ilQB/4xWAf+OWAH/kFoB/5JcAf+UXgH/lV8A/5ZhAP+YYwD/mmUA/51oAP+gawH/om4B/6RwAf+mcgH/qHQC/6l2Af+reQH/rXsB/699Af+xfwH/s4EB/7WDAf+3hQH/uYgB/7uKAP+9jAH/xpgX/9u0UP/sy4D/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6l+QP92PgD/ekIB/3xEAf9+RgH/gEgB/4JLAf+ETQH/hk8B/4hRAf+KUwH/jFUB/41XAf+PWQH/kFoA/5ZiCf+ldyj/sYpG/7eST/+yiT//qXsk/6FuCf+gawD/om4A/6VxAv+ncwL/qXUC/6t3Av+tegH/r3wB/7F+Af+zgQH/tYMB/7eFAf+5hwH/u4kB/7yLAf++jQD/wJAD/82gI//hvF//786G//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/qH0//3Y+AP95QQH/e0MB/31GAf9/SAH/gUoB/4NMAf+FTgH/h1AB/4lSAf+LVQH/jVYA/49ZBP+thUb/3Mqw//Tt5f/7+fb//fz6//r38//z7OD/4dCz/8anav+tfyH/pG8B/6ZyAf+odAL/qnYC/6x4Av+uewL/sH0C/7KAAf+0ggH/toQB/7iGAf+6iQH/vIsB/76NAf+/jwH/wJAA/8WVB//UqTL/6MVw//DQiv/w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ofT//dT0A/3lBAf97QwH/fUUB/39HAf+BSQH/g0sB/4VOAf+GUAH/iFIB/4pUAP+OWQf/vqBz//by7P/////////////+/v///v7///7//////////////v38//Dn1//MrnT/rX0Y/6dyAP+qdQH/rHgC/656Av+wfAL/sn8C/7SBAv+1gwH/t4YB/7mIAf+7igH/vYwB/76OAf/AkQH/wpMB/8SUAP/LnRH/3LRG/+zKe//w0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6d8P/90PQD/eEEB/3pCAf98RAH/fkYB/4BJAf+CSwH/hE0B/4ZPAf+IUQH/iVMB/7qbbf/6+PX////////+/v///v7///7+///+/v///v7///7+///+/v///v7///////79/P/r3sf/xJ9W/6x4C/+qdgD/rXkC/698Av+xfgL/s4AC/7WCAv+3hQL/uYcB/7uKAf+9jAH/vo4B/8CQAf/CkgH/xJQB/8WWAP/ImQL/0aUc/+O9WP/vzoT/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/p3w//3Q8AP93QAH/eUEB/3tDAf99RgH/f0gB/4FKAf+DTAH/hU4B/4ZPAP+dcTH/8Orh/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////7+PT/4c6o/7ySOP+seAP/rnoA/7B9Av+yfwL/tIEC/7aDAv+4hgL/uogC/7yLAf++jQH/v48B/8GRAf/DlAH/xZYB/8aXAf/DkwD/xJQF/9KlLP/mwGn/8NCJ//HRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+nfD//czsA/3c/Af95QQH/e0MB/31FAf9/RwH/gUkB/4NLAf+ETQH/hlAB/8mxj/////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v//////9/Hm/9e8hv+3iCD/r3oA/7F+Af+zgAL/tYMC/7eFAv+5hwL/u4kC/72MAv+/jgH/wJEB/8OTAf+5iAL/o28C/5lkAf+YYwH/m2YA/6dzDf/ClTz/48B2//HRi//w0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6Z7P/9yOgD/dj8B/3hBAf96QgH/fEQB/35GAf+ASQH/gksB/4NMAP+RXxr/6uHU/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v////////7+//Dl0f/NrGP/tYMQ/7J+AP+1ggL/t4QC/7mGAv+7iAL/vYsC/76NAv/AkQH/sYAC/5FcAv+MVQH/j1kB/5FcAf+UXgH/lmEA/5lkAP+odxf/zaVU/+rKg//x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/pns//3I6AP92PgH/eEAB/3pCAf98RAH/fkYB/39IAf+BSgH/gkoA/6J5Qf/59vP///7////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///////37+P/o17X/xp5D/7WCBv+2ggD/uIYC/7qIAv+8igL/vo0C/7iHAv+RXAL/iFIB/4xWAf+OWAH/kVsB/5NeAf+WYQH/mGMB/5plAP+eagT/tIYo/9q1Z//vz4j/8dGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+mej//cTkA/3U+Af93QAH/eUEB/3tDAf99RQH/f0cB/4FKAf+BSQD/tZRp/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///7+///////59ez/38eT/8GUKP+3hAH/uYcB/7yJAv++jAL/pHAD/4VPAv+IUgL/i1QC/41XAf+QWgH/kl0B/5VgAf+XYgH/mmUB/5xoAf+eagD/p3QL/8OYPP/jwHX/8NGL//DRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6V6P/9xOQD/dT0B/3Y/Af94QQH/ekIB/3xFAf9+RwH/gEkB/4FJAP/FrIv////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///79/////v////7/9OvZ/9W2bv+9jBL/uocA/7uJAv+TXQL/hE0C/4dRAv+KUwL/jFYC/49ZAv+RXAH/lF8B/5ZhAf+ZZAH/m2cB/55qAf+gbAD/o28B/69+FP/OpU3/6ciA//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/pXo//3A4AP90PAH/dj4B/3hAAf96QgH/fEQB/35GAf+ASAH/gUkA/8qzlf////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///79///+/f///v3///79///+/f///////fz5/+vbuP/Mpkf/t4QH/4lSAP+DTAL/hk8C/4lSAv+LVQL/jlgC/5BbAv+TXQH/lWAB/5hjAf+aZgH/nWkB/59rAf+ibgH/pHAA/6d0Av+5iiL/2bNg/+7Ohv/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+leT//bzcA/3M7Af91PgH/d0AB/3lBAf97QwH/fUUB/39HAf+ASQD/zLWY/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///79///+/f///v3///79///+/f///v3///////r27v/dxpj/mmwv/4JKAv+ETQH/iFEC/4pUAv+NVwL/j1oC/5JcAv+UXwL/l2IB/5llAf+cZwH/nmoB/6FtAf+jcAH/pnIB/6h0AP+ufAj/xZk0/+O/cP/w0Ir/8NGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6R5P/9vNgD/czsB/3Q9Af92PwH/eUEB/3pCAf98RQH/fkcB/4BIAP/MtZj////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///7+///////w6eD/vaB8/49eG/+FTgD/iVIB/4xWAv+OWAL/kVsC/5NeAv+WYQL/mGQC/5tmAf+eaQH/oGwB/6NvAf+lcQH/qHQB/6p3Af+seQD/toUR/9GnSP/qyHz/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/pHg//242AP9yOgH/dDwB/3Y+Af94QAH/ekIB/3xEAf9+RgH/f0cA/8y1mP////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////+/f3//Pr4//78+//////////////+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79/////v/+/fz/5dnK/6+MW/+MWA3/iVIA/41XAv+QWgL/kl0C/5VgAv+YYwL/mmUC/51oAv+fawH/om4B/6RwAf+ncwH/qXYB/6x5Af+uewD/sX8C/8CRH//atFr/7c2E//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+keD//bjUA/3E6Af9zPAH/dT4B/3dAAf95QQH/e0MB/31FAf9/RwD/y7WY/////////v7///7+///+/v///v7///7+///+/v///v7///7+///////59vP/18Sq/7iXY/+vikv/uZZY/8+1h//r4Mv//fz5/////////v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f//////+/j1/9jGrf+kej3/jVcE/45YAP+SXAL/lF8C/5diAv+ZZAL/nGcC/55qAv+hbQL/o28B/6ZyAf+odQH/q3gB/617Af+wfQH/sn8A/7aFBf/Imyz/4r5q/+/Qif/w0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6N4P/9tNAD/cTkB/3M7Af91PQH/dz8B/3lBAf97QwH/fUUB/35GAP/LtZj////////+/v///v7///7+///+/v///v7///7+///+/v//////9vHt/7ORY/+MVwj/jFUA/5FaAP+VXgD/mWQB/6Z1Fv/Hpmb/7+TQ///+/f////7///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v7///////Xw6f/Kso3/nW4k/49ZAf+TXQH/lmEC/5hjAv+bZgL/nWkC/6BsAv+ibwL/pXEC/6d0Af+qdwH/rHoB/698Af+xfwH/tIIB/7aEAP+9jAv/0qg+/+nGeP/w0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/o3c//2w0AP9wOAH/cjoB/3Q8Af92PwH/eEEB/3pCAf98RAH/fUUA/8u0mP////////7+///+/v///v7///7+///+/v///v7///7+//7+/f+9oX//hE0C/4lSAf+NVwL/kVsC/5VgAv+ZZAL/nWgB/6BrAP+vgR//1ruF//fx5f////////7+///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3////+///+/v/s49X/vJxq/5hmEv+TXQD/l2IC/5plAv+caAL/n2oC/6FtAv+kcAL/pnIC/6l1Af+reAH/rnsB/7B+Af+zgQH/tYMB/7iGAP+6iQH/xZYY/9y1U//tzIL/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+idz//bDMA/3A3Af9xOQH/czwB/3U+Af93QAH/eUEB/3tDAf99RQD/y7SY/////////v7///7+///+/v///v7///7+///+/v//////6eHX/4xbH/+CSwD/h1EB/4xVAv+QWgL/lF4C/5hjAv+cZwL/oGwC/6NvAP+odAP/vZM3/+TQp//8+fT////////+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///////9+/n/4dK5/7GKSf+XYwf/l2IA/5tnAv+eaQL/oGwC/6NvAv+lcQL/qHQC/6p3Av+tegH/r30B/7KAAf+0ggH/t4UB/7mIAf+7igD/v48E/82hKP/jv2X/78+I//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6J3P/9rMgD/bzcB/3E5Af9zOwH/dT0B/3c/Af95QQH/e0MB/3xEAP/KtJj////////+/v///v7///7+///+/v///v7///7+///////Is5v/fUYC/4JLAf+GTwL/ilQC/45YAv+SXQL/lmEC/5pmAv+fagL/o28C/6dzAv+qdgD/soAK/8ypVf/v4sb//v38/////////v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f//////+PTu/9S+mf+pey3/mWQC/5xnAf+fawL/om4C/6RxAv+ncwL/qXUC/6x4Av+ufAH/sX8B/7OBAf+2hAH/uIcB/7uKAf+9jAH/v44A/8WWCv/Vqzj/6cZz//DRiv/w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/onY//2oyAP9uNgH/cDgB/3I6Af90PQH/dj8B/3hBAf96QgH/e0MA/8qzmP////////7+///+/v///v7///7+///+/v///v7//////7GTcP96QgD/gUkB/4VOAv+JUgL/jVcC/5FbAv+VYAL/mWQC/51pAv+ibgL/pnIC/6p2Av+uegH/sX4A/7yNGP/avXf/9+/d/////////v7///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v7///////Hq3f/Hqnb/pHMX/51oAP+hbAH/o3AC/6ZyAv+odAL/q3cC/616Av+wfQL/soAB/7WDAf+4hgH/uokB/7yLAf++jgH/wJEA/8OTAP/LnRP/3bZL/+3Mfv/w0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+hdj//ajEA/241Af9wOAH/cjoB/3Q8Af92PgH/eEAB/3pCAf97QwD/yrOY/////////v7///7+///+/v///v7///7+///+/v/+/v3/p4Nc/3lAAP+ASAH/hE0C/4hRAv+MVgH/kFoB/5RfAf+YYwL/nGgC/6BsAv+kcQL/qHQC/615Av+xfQL/tIEB/7iGAf/InSz/59Kb//z47/////////79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///////79+//o28X/vJhU/6JvCv+hbQD/pXEC/6hzAv+qdgL/rHkC/698Av+xfwL/tIIB/7eFAf+5iAH/vIoB/76NAf/AkAH/wpMB/8SVAP/ImAL/06ch/+W/Xv/vz4b/8NGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6F1P/9pMAD/bTUB/283Af9xOQH/czsB/3U+Af93QAH/eUEB/3pCAP/Ks5j////////+/v///v7///7+///+/v///v7///7+//38+/+hfVX/eD8A/35HAf+CSwL/h1AC/4tUAf+PWQH/k10B/5diAf+bZgL/n2sC/6NvAv+ncwL/q3cC/698Av+zgAL/t4UC/7uJAP/AkAf/1LBJ//Dhuv/+/Pn////////+/f///v3///79///+/f///v7///7+///+/v///v3///79///+/f///v3///79///////6+PP/3cmm/7SKNv+kcAP/pnEB/6l1Av+seAL/rnoC/7F9Av+zgAL/toMC/7iHAf+7iQH/vYwB/7+PAf/BkgH/xJUB/8aXAf/ImQD/zZ8I/9qwMv/pxm7/8NCJ//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/oXU//2kvAP9tNAH/bzYB/3E4Af9yOwH/dD0B/3Y/Af94QQH/ekEA/8mzmP////////7+///+/v///v7///7+///+/v///v7//fz7/6B8VP93PgD/fUUC/4FKAv+FTgL/iVMB/41XAf+RXAH/lWAB/5plAv+eaQL/om4C/6ZyAv+qdgL/rnoC/7J/Av+2hAL/uogC/76NAf/BkAD/ypwR/+HCav/47tb////+/////v///v3///79///+/f///v7///7+///+/v///v7///79///+/f///v3///79///+/v//////9e/l/9K3g/+vgB7/p3IA/6p2Af+teQL/r3wC/7J/Av+1ggL/t4UB/7qIAf+8iwH/vo4B/8CRAf/DkwH/xZYB/8iZAf/KnAH/zJ4A/9OmEP/hukb/7ct7//DRi//w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+gdT//aC8A/2wzAf9uNQH/cDgB/3I6Af90PAH/dj4B/3hAAf95QQD/ybOY/////////v7///7+///+/v///v7///7+///+/v/9/Pv/n3tU/3U9AP98RAL/gEgC/4RNAv+IUQH/jFYB/5BaAf+UXwL/mGMC/5xoAf+gbAH/pHEB/6l1Af+tegH/sX4B/7WDAf+5hwH/vYwC/8CQAv+4hwH/qXUA/7SFJP/VvIz/9/Lp/////////v7///79///+/f///v7///7+///+/v///v7///7+///+/v///v3///79///+/f///////v79/+7iz//HpV//rXsO/6t2AP+uewL/sX4C/7OBAv+2gwL/uYYC/7uKAf+9jQH/v48B/8KSAf/ElQH/x5gB/8maAf/MnQH/zqAA/9GjAv/ZrRr/5sBW/+/Pg//w0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6B0P/9nLgD/azMB/201Af9vNwH/cTkB/3M7Af91PgH/d0AB/3hAAP/Jspj////////+/v///v7///7+///+/v///v7///7+//38+/+eelT/dDsA/3pDAv9/RwL/g0wC/4dQAv+LVAL/j1kC/5NdAv+XYgL/m2cB/59rAf+jcAH/p3QB/6t4Af+wfQH/tIIB/7iGAf+8iwH/tYQC/5JdAf+OWAH/k10A/5plBP+0iz3/4tCv//z69/////////79///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///////z69//k07H/v5ZA/656Bf+vfAD/s4AC/7WCAv+4hQL/uogC/72LAf++jgH/wZEB/8OUAf/GlwH/yJoB/8ucAf/NnwH/0KIB/9KkAP/WqAT/37Uq/+vHZ//w0Ij/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/oHQ//2cuAP9rMgH/bTQB/282Af9xOQH/czsB/3Q9Af92PwH/eEAA/8mymP/////////+///+/v///v7///7+///+/v///v7//fz7/515VP9zOgD/eUEC/31FAv+BSgL/hU8C/4pTAv+OWAL/klwC/5ZhAv+aZQH/nmoB/6JuAf+mcwH/qncB/658Af+ygAH/toUB/7uKAf+hbQH/h1AB/41XAf+SXQH/l2IB/5tmAP+mcw3/xqRe/+7jzf///v3////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////48+v/28KQ/7qMJv+xfQH/tIEB/7eEAv+5hwL/vIoC/76NAf/AkAH/wpMB/8WWAf/HmQH/ypsB/8yeAf/PoQH/0aQB/9SmAf/WqQD/264L/+W9Pf/uzHb/8NCL//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+fdD//Zi0A/2oxAf9sNAH/bjYB/3A4Af9yOgH/dDwB/3Y+Af93QAD/yLKY//////////7///7+///+/v///v7///7+///+/v/9/Pv/nHhU/3E5AP94QAL/fEQC/4BJAv+ETQL/iFIC/4xWAv+QWwL/lV8C/5lkAf+daAH/oW0B/6VxAf+pdgH/rXoB/7F/Af+1gwH/uYgB/5diAf+FTgH/i1UB/5BbAf+VYAH/m2YB/6BrAP+kcAD/s4Qc/9e8gf/38OT////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+/////////v7/8unX/9Gybf+4iBP/tYEA/7iGAf+7iQL/vYwC/7+PAv/BkgH/xJUB/8aXAf/JmgH/y50B/86gAf/RowH/06UB/9aoAf/YqwD/260B/+G1Fv/qw0//8M6A//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/59zP/9mLAD/ajEB/2szAf9tNQH/cDcB/3E5Af9zPAH/dT4B/3c/AP/Ispj//////////v///v7///7+///+/v///v7///7+//38+/+bd1T/cDcA/3c/Av97QwL/f0cC/4NMAv+HUAL/i1UC/49ZAv+TXgL/l2IB/5tnAf+gawH/pHAB/6h0Af+seQH/sH4B/7SCAf+4hwH/mWQC/4NLAf+JUgH/jlgB/5NeAf+ZZAH/nmoB/6NvAf+odAD/rXoC/8GXM//l0aP//Pnz/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///////vz6/+vcvf/KpEz/uYcH/7mHAP+8iwL/vo0C/8CQAv/DlAH/xZYB/8iZAf/KnAH/zZ8B/9CiAf/SpAH/1acB/9eqAf/arQH/3K8A/9+yA//muyT/7clh//DQhv/w0Iv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/n3M//2UsAP9pMAH/azIB/200Af9vNwH/cTkB/3M7Af91PQH/dj4A/8ixmP/////////+///+/v///v7///7+///+/v///v7//fz7/5p2VP9vNgD/dj4C/3lCAv9+RgL/gkoC/4ZPAv+KUwL/jlgC/5JcAv+WYQH/mmUB/55qAf+ibwH/pnMB/6p3Af+vfAH/s4EB/7iGAf+ibgL/gUoB/4dQAf+MVgH/kVwB/5diAf+cZwH/oW0B/6ZzAf+reQH/sH0A/7iHCf/QrVH/8OPD//79+/////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///////r38f/jzZ3/xZov/7uJAv+9jAH/v48C/8KSAf/ElQH/x5gB/8mbAf/MngH/z6AB/9GjAf/UpgH/1qkB/9msAf/brgH/3rEB/+CzAP/kuAj/6sE0//DNcf/w0Ir/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ecz//ZCsA/2gvAf9qMQH/bDQB/242Af9wOAH/cjoB/3Q8Af91PgD/yLGY//////////7///7+///+/v///v7///7+///+/v/9/Pv/mXVU/240AP90PAH/eEEC/3xEAf+ASQH/hE0B/4lSAf+NVgL/kVsB/5VgAf+ZZAH/nWkB/6FtAf+lcQH/qXYB/617Af+xfwH/toQB/7B9Av+GUAL/hE0B/4pUAf+PWgH/lV8B/5plAf+fawH/pHEB/6l2Af+vfAH/tIIB/7iGAP/DlRX/3cFz//fv3P////////7////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7////////27+D/2757/8OUGv++jQD/wZEB/8OUAf/GlwH/yJoB/8udAf/NnwH/0KIB/9KlAf/VpwH/2KoB/9qtAf/dsAH/37MB/+G1Af/kuAD/6b0S/+7ISv/w0IH/8NCL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/55yP/9kKgD/aC8B/2kxAf9sMwH/bjUB/283Af9xOQH/czwB/3U9AP/HsZj//////////v///v7///7+///+/v///v7///7+//38+/+ZdFT/bDMA/3M7Af93PwH/e0MB/39IAf+DTAH/h1EB/4tVAf+PWgH/lF4B/5diAf+cZwH/oGwB/6RwAf+odQH/rHkB/7B+Af+0ggH/uIYB/5plA/+CSwH/iFEB/41XAf+TXQH/mGMB/51pAf+ibgH/p3QB/616Af+ygAH/t4YB/7yLAP/AkAH/z6Yq/+rUl//8+O7////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////+/fz/8OTI/9SxWP/Ckwv/wpIA/8WWAf/HmQH/ypsB/82eAf/PoQH/0aQB/9SmAf/XqQH/2awB/9yvAf/esgH/4bQB/+O3Af/mugD/6b0C/+7EKf/xznD/8NCL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/n3NA/2MpAP9nLgH/aTAB/2syAf9tNQH/bzcB/3E5Af9zOwH/dDwA/8exmP/////////+/////v////7///7+///+/v///v7//fz7/5hzVP9rMgD/cToB/3Y+Af96QgH/fkYB/4JLAf+GTwH/ilQB/45YAf+SXQH/lmEB/5pmAf+eagH/om8B/6dzAf+reAH/r3wB/7OBAf+3hgH/soAD/4pUA/+FTgH/i1UB/5BbAf+WYQH/m2YB/6BsAf+lcgH/q3gB/7B+Af+1gwH/uokB/7+PAf/DkwD/ypsG/9y3Rf/z5Lf//vz5/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///////Pr1/+rXqv/Ppzr/xJQD/8aXAP/JmgH/zJ0B/86gAf/RowH/06UB/9aoAf/YqwH/264B/92xAf/gswH/4rYB/+W5Af/nvAH/6r4A/+7DF//xzF7/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HSi/+keEP/YykA/2YtAf9oMAH/ajIB/2w0Af9uNgH/cDgB/3I6Af90PAD/x7CY//////////7////+/////v///v7///7+///+/v/9/Pv/l3JU/2owAP9wOAH/dD0B/3lBAf99RQH/gUkB/4VOAf+JUgH/jVcB/5FbAf+VYAH/mWQB/51pAf+hbQH/pXIB/6p2Af+uewH/sn8B/7aEAf+6iQH/p3QD/4ZQAv+JUgH/jlkB/5ReAf+ZZAH/nmoB/6NwAf+pdQH/rnsB/7OBAf+4hwH/vY0B/8KSAf/HmAH/zJ0A/9WoEP/nyWb/+fDT///+/v///v////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///////nz5//hxn7/ypwU/8iYAP/LnAH/zZ8B/9CiAf/SpAH/1acB/9eqAf/arQH/3LAB/9+yAf/htQH/5LgB/+a7Af/pvQH/678A/+/DC//yzFP/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8dGL/6J2Qv9iKAD/Zi0B/2gvAf9qMQH/bDMB/241Af9wOAH/cjoB/3M7AP/GsJj//////////v////7////+///+/v///v7///7+//38+/+WcVT/aC8A/283Af9zOwH/d0AB/3tDAf9/SAH/g0wB/4hRAf+MVQH/kFoB/5RfAf+YYwH/nGcB/6BsAf+kcAH/qHUB/6x6Af+wfgH/tIIB/7mHAf+8iwH/oW0D/4hRAv+MVgH/klwB/5diAf+caAH/oW4B/6dzAf+seQH/sX8B/7aFAf+7igH/wJAB/8WWAf/KnAH/z6EA/9SmAP/ftiH/8dmJ//z36P////////7+///+/v///v7////+/////v///v7///7+///+/v///v7///7+///+/v///v7///////79/P/u3rT/0acq/8maAP/MngH/z6EB/9GjAf/UpgH/1qkB/9msAf/brwH/3rEB/+C0Af/jtwH/5boB/+i9Af/qvwH/7cEA//HECv/yzVz/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yv/onZA/2IoAP9lLAH/Zy4B/2kwAf9rMwH/bTUB/283Af9xOQH/cjoA/8awmP/////////+/////v////7////+///+/v////7//fz7/5VwVP9nLQD/bjUB/3I6Af92PwH/ekIB/35GAf+CSwH/hk8B/4pUAf+PWQH/k10B/5diAf+bZgH/n2sB/6NvAf+ndAH/q3gB/699Af+zgQH/t4UB/7yKAf+9jAL/oW0E/4tVAv+PWgH/lWAB/5plAf+fawH/pXEB/6p3Af+vfAH/tIIB/7qIAf++jgH/w5QB/8iZAf/NnwH/06UB/9iqAP/esAP/6cQ6//fnrP/+/Pb////////+/v///v7////+/////v////7///7+///+/v///v7///7+///+/v///v7///7+///////06Mr/06sx/8ucAP/OoAH/0KIB/9OlAf/VqAH/2KsB/9quAf/dsAH/37MB/+K2Af/kuQH/57sB/+m+Af/swAH/7sMA//LHFf/yz3H/8NCL//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HRi/+leUD/YigA/2QrAf9mLQH/aDAB/2syAf9sNAH/bjYB/3A4Af9yOgD/xrCZ//////////7////+/////v////7///7+/////v/9/fz/l3NY/2YsAP9sNAH/cTgB/3U9Af95QQH/fUUB/4FKAf+FTgH/iVIB/41XAf+RXAH/lWAB/5llAf+daQH/oW4B/6ZyAf+qdwH/rnsB/7KAAf+2hAH/uokB/76OAf+/jwL/pnMD/49ZAv+SXQH/mGMB/51pAf+jbwH/qHQB/616Af+ygAH/t4YB/7yMAf/BkQH/xpcB/8udAf/RowH/1qgB/9uuAf/gswD/57wM//PVYv/99t7////////+/v///v7////+/////v////7////+///+/v///v7///7+///+/v///v7///7+///////y5sP/0aYg/8yeAP/PoQH/0qQB/9SnAf/XqgH/2awB/9yvAf/esgH/4bUB/+O3Af/mugH/6L0B/+u/Af/twgH/8MQA//PKMf/x0IX/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6h9QP9kKgD/ZCoB/2YtAf9oLwH/ajEB/2wzAf9uNQH/cDcB/3E5AP/Gr5j//////////v////7////+/////v///v7////+//7+/P+ZdFr/ZCoA/2syAf9vNwH/czwB/3dAAf98RAH/gEgB/4RNAf+IUQH/jFYB/5BaAf+UXwH/mGMB/5xoAf+gbAH/pHEB/6h1Af+segH/sX4B/7WDAf+5hwH/vYwB/8CRAf/DkwH/sH4D/5ZhAv+VYAH/m2cB/6BtAf+mcgH/q3gB/7B+Af+1gwH/u4kB/7+PAf/ElQH/yZsB/8+gAf/UpgH/2awB/96yAf/jtwD/6bwA//PPPP/89NX////////+/v////7////+/////v////7////+///+/v///v7///7+///+/v///v7///7+///////o05P/zJ4F/86gAf/RowH/06YB/9aoAf/YqwH/264B/92xAf/gtAH/4rYB/+W5Af/nvAH/6r4B/+zAAf/vwwD/8sYJ//LOZf/w0Iv/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/qn9A/2gvAP9jKQH/ZSwB/2cuAf9pMAH/azMB/201Af9vNwH/cDgA/8WvmP/////////+/////v////7////+///+/v////7//v38/5hzWP9jKQD/ajEB/242Af9yOgH/dj8B/3pCAf9+RwH/gksB/4ZQAf+LVAH/j1kB/5NdAf+XYgH/m2YB/59rAf+jbwH/p3QB/6t4Af+vfQH/s4EB/7eGAf+8igH/v48B/8OUAf/HmAH/vIwD/6FtA/+ZZAH/nmoB/6RwAf+pdgH/rnwB/7OBAf+5hwH/vY0B/8KTAf/HmAH/zJ4B/9KkAf/XqgH/3LAB/+G1Af/nuwH/7L8A//bUSf/++uv///7//////v////7////+/////v////7////+///+/v///v7///7+///+/v///v7///////r26f/VsDf/zZ4A/9CiAf/SpQH/1acB/9eqAf/arQH/3LAB/9+yAf/htQH/5LgB/+a7Af/pvQH/7L8B/+7CAf/xxQD/88o3//DQiP/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+qf0D/bzYA/2MpAf9lKwH/Zy4B/2kwAf9rMgH/bTQB/282Af9wOAD/xa+Y//////////7////+/////v////7///7+/////v/+/fz/nHdY/2IoAP9pMAH/bTQB/3E5Af91PQH/eUEB/31FAf+BSgH/hU4B/4lTAf+NVwH/kVwB/5ZhAf+aZQH/nmkB/6JuAf+mcgH/qncB/657Af+ygAH/toQB/7qJAf++jgH/wZIB/8aXAf/KnAH/yJgC/7B+A/+eagL/oW0B/6d0Af+seQH/sX8B/7eFAf+8iwH/wJAB/8WWAf/KnAH/0KIB/9WnAf/arQH/37MB/+W5Af/qvgH/8MMD//rllv/////////+/////v////7////+/////v////7///7+///+/v///v7///7+///+/v///v7//////+PLf//MnQD/z6EB/9GkAf/UpgH/1qkB/9msAf/brwH/3rEB/+G0Af/jtwH/5roB/+i9Af/rvwH/7cEB//DEAP/yyBn/8c99//DQiv/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6p/QP91PAD/Zi0B/2QrAf9mLQH/aC8B/2oxAf9sNAH/bjYB/283AP/Frpj//////////v////7////+/////v////7////+//39+/+fe1b/ZCoA/2cuAf9sMwH/cDcB/3Q8Af94QAH/fEQB/4BIAf+ETQH/iFIB/4xWAf+QWwH/lF8B/5hjAf+daAH/oW0B/6VxAf+pdgH/rXoB/7F/Af+1gwH/uYgB/72MAf/AkQH/xJUB/8iaAf/NnwH/0KEB/7+OA/+mcwL/pHAB/6p3Af+vfQH/tYMB/7qIAf++jgH/w5QB/8iaAf/OnwH/06UB/9irAf/dsQH/47cB/+i8Af/twAD/9dRN//799/////7////+/////v////7////+/////v////7///7+///+/v///v7///7+///+/v//////7d6v/8yeBv/OoAH/0KMB/9OlAf/VqAH/2KsB/9uuAf/dsAH/4LMB/+K2Af/luQH/57wB/+q+Af/swAH/78MA//HGC//xzm//8NCL//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/qX5A/3c/AP9uNQH/YyoB/2UsAf9oLwH/aTEB/2szAf9tNQH/bzYA/8Wumf/////////+/////v////7////+/////v////7//f37/6F9Vf9rMQD/Zi0B/2oyAf9uNgH/cjsB/3Y/Af97QwH/f0cB/4NMAf+HUAH/i1UB/49ZAf+TXgH/l2IB/5tnAf+fawH/o3AB/6d0Af+seQH/sH0B/7SCAf+4hgH/vIsB/7+PAf/DlAH/x5gB/8udAf/PogH/1KYB/8udA/+xfwP/qHQB/617Af+zgAH/uIYB/72MAf/BkgH/xpcB/8ydAf/RowH/1qkB/9uvAf/htAH/5roB/+u/AP/zzzb//vvv//////////7////+/////v////7////+/////v////7////+///+/v///v7///7+///////v47z/y54K/82fAP/QogH/0qQB/9SnAf/XqgH/2q0B/9yvAf/fsgH/4bUB/+S4Af/muwH/6b0B/+u/Af/uwgH/8MUH//HOZv/w0Iv/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+pfkD/dj4A/3c/Af9nLgH/ZSsB/2cuAf9pMAH/azIB/200Af9uNQD/xa6Z//////////7////+/////v////7////+/////v/9/fv/oH1V/3U8AP9pMQH/aDAB/201Af9xOQH/dT4B/3lBAf99RQH/gUoB/4VPAf+KUwH/jlgB/5JcAf+WYQH/mmUB/55qAf+ibgH/pnMB/6p3Af+ufAH/soAB/7aFAf+7iQH/vo4B/8KSAf/GlwH/ypsB/86gAf/SpAH/16oB/9WnAv+8jAP/rHkC/7B+Af+2hAH/u4oB/7+PAf/ElQH/ypsB/8+hAf/UpwH/2awB/96yAf/kuAH/6bwA//LQR//+/Pb//////////v////7////+/////v////7////+/////v////7///7+///+/v///v7//////+3esv/KnAf/zJ4B/86gAf/RowH/06YB/9apAf/YqwH/264B/96xAf/gtAH/47cB/+W5Af/ovAH/6r4B/+3BAf/vxAf/8c5n//DQi//w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6h9QP91PQD/ekIB/3M7Af9lLAH/Zi0B/2gvAf9qMQH/bDMB/201AP/Erpn//////////v////7////+/////v////7////+//39+/+fe1T/dz4A/3hAAf9rMwH/azMB/3A4Af90PAH/eEAB/3xEAf+ASQH/hE0B/4hSAf+MVgH/kFsB/5RfAf+ZZAH/nWgB/6FtAf+lcQH/qXYB/616Af+xfwH/tYMB/7mIAf+9jAH/wJEB/8SVAf/JmgH/zZ4B/9GjAf/VpwH/2awB/9uuAv/GlwP/sX8C/7OBAf+5hwH/vo0B/8KTAf/ImQH/zZ8B/9KkAf/XqgH/3bAB/+K2Af/ouwH/9t+K//////////7////+/////v////7////+/////v////7////+/////v///v7///7+///+/v//////482K/8iYAP/LnQH/zp8B/9CiAf/SpQH/1agB/9eqAf/arQH/3bAB/9+zAf/itgH/5LgB/+e7Af/pvgH/7MAA/+/DDf/xznL/8NCK//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/qH1A/3Q9AP95QgH/fEQB/3A4Af9lLAH/Zy8B/2kxAf9rMwH/bTQA/8StmP/////////+/////v////7////+/////v////7//fz7/515VP91PAD/fkYB/3xFAf9wOAL/bjYB/3M7Af93PwH/e0MB/39HAf+DTAH/h1AB/4tVAf+PWQH/k14B/5diAf+cZwH/n2sB/6RwAf+odAH/rHkB/7B9Af+0ggH/uIYB/7yLAf+/jwH/w5QB/8eYAf/LnQH/z6IB/9SmAf/YqgH/3K8B/9+zAf/OnwP/tYQC/7aFAf+8iwH/wJEB/8aXAf/LnAH/0KIB/9WoAf/brgH/37IA/+rFN//89uH//////////v////7////+/////v////7////+/////v////7///7+///+/v///v7///////z48f/UsET/x5cA/8qbAf/NngH/z6EB/9GkAf/UpwH/16kB/9msAf/crwH/3rIB/+G0Af/jtwH/5roB/+i9Af/rvwD/78Qf//HPgf/w0Ir/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+nfED/dDwA/3lBAf98RAH/fUUB/283Av9nLgH/aTAB/2syAf9sNAD/xK2Y//////////7////+/////v////7////+/////v/9/Pv/nHhU/3M7AP98RAH/g0sB/4ROAv95QgL/cjsB/3U9Af95QgH/fkYB/4JLAf+GTwH/ilQB/45YAf+SXQH/lmEB/5pmAf+eagH/om4B/6ZzAf+reAH/r3wB/7OBAf+3hQH/u4oB/76OAf/CkwH/xpcB/8qcAf/OoAH/0qUB/9apAf/argH/37IB/+O3Af/RowP/t4YC/7qIAf+/jwH/xJQB/8maAf/OoAH/06YB/9iqAP/iuyn/+OzC//////////7////+/////v////7////+/////v////7////+/////v///v7///7+///+/v//////6dek/8aXCf/GlwD/yZoB/8ydAf/OoAH/0aMB/9OlAf/WqAH/2KsB/9uuAf/dsQH/4LMB/+K2Af/luQH/57wB/+q+AP/vx0T/8NCK//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6d8QP9zOwD/eEAB/3tDAf9+RgH/f0cB/3A5Av9oLwH/ajIB/2wzAP/DrZj//////////v////7////+/////v////7////+//38+/+bd1T/cTkA/3pDAf+ASQH/h1AB/4xWAf+IUgL/fkgC/3lCAf98RAH/gEkB/4VOAf+JUgH/jVcB/5FbAf+VYAH/mWQB/51pAf+hbQH/pXIB/6l2Af+tewH/sn8B/7aEAf+6iAH/vY0B/8GRAf/FlgH/yZoB/82fAf/RowH/1agB/9msAf/dsQH/4rYB/+W6Af/PoQP/uIcC/72MAf/CkgH/x5gB/8ydAP/RpAX/4r9J//ftzP/////////+/////v////7////+/////v////7////+/////v////7///7+///+/v///v7///////Ts1f/Moy7/wpMA/8aWAf/ImQH/y5wB/82fAf/QogH/0qQB/9WnAf/XqgH/2q0B/9ywAf/fsgH/4bUB/+S4Af/muwD/678R//DNcf/w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/pntA/3I6AP93PwH/ekIB/31FAf+ASQH/gUoB/3Q9Av9qMgH/azIA/8OsmP/////////+/////v////7////+/////v////7//fz7/5p1VP9wNwD/eEEB/39HAf+FTgH/i1UB/5JdAf+WYQH/kVwC/4hSAv+BSgL/g0wB/4dQAf+LVQH/j1oB/5ReAf+YYwH/nGcB/6BsAf+kcAH/qHUB/6x5Af+wfgH/tIIB/7iHAf+8iwH/wJAB/8OUAf/ImQH/zJ0B/9CiAf/UpgH/2KsB/9yvAf/gtAH/5bkB/+W5Av/DkwL/uokB/7+PAP/ElAH/0agm/+nTj//8+O3//////////v////7////+/////v////7////+/////v////7////+///+/v///v7///7+///////17tv/zqlE/7+PAP/CkwH/xZUB/8eYAf/KmwH/zJ4B/8+hAf/RowH/1KYB/9apAf/ZrAH/268B/96xAf/gtAH/47cB/+a6Af/txkb/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+me0D/cTkA/3Y+Af95QQH/fEQB/39IAf+CSwH/hE0B/3lCAv9sNAH/w6yZ//////////7////+/////v////7////+/////v/9/Pv/mHRU/241AP93PwH/fUUB/4NMAf+KUwH/kFoB/5ZhAf+daQH/om4B/55qAv+UXwL/i1UC/4pTAf+OWAH/kl0B/5ZhAf+aZgH/nmoB/6NvAf+ncwH/q3gB/698Af+zgQH/t4UB/7uKAf++jgH/wpMB/8aXAf/KnAH/zqAB/9KlAf/XqQH/264B/9+yAf/jtwH/6LwB/9GiAf+3hQD/wpQT/9u+bf/27tj////+//////////7////+/////v////7////+/////v////7////+/////v///v7///7+///+////////8OTJ/8qiPf+8iwD/v48B/8GRAf/DlAH/xpcB/8maAf/LnQH/zp8B/9CiAf/TpQH/1agB/9irAf/arQH/3bAB/9+zAf/itQD/6L8p//DOf//w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6V6QP9wOAD/dT4B/3hAAf97QwH/fkcB/4FKAf+ETQH/h1EB/4FKAf/HsZf//////////v////7////+/////v////7////+//38+/+Xc1T/bDMA/3U9Af97RAH/gkoB/4hRAf+OWAH/lF8B/5tmAf+hbQH/qHUB/657Af+tegL/om8C/5ZiAv+RXAH/lF8B/5lkAf+daQH/oW0B/6VyAf+pdgH/rnsB/7J/Af+2hAH/uogB/72NAf/BkQH/xZYB/8maAf/NnwH/0aMB/9WoAf/ZrQH/3rEB/+K1Af/mugD/z6AI/8qmS//t373//v36//////////7////+/////v////7////+/////v////7////+/////v////7///7+///+/v//////+/fy/+DLmf+/kyH/uYcA/7yLAf++jgH/wJAB/8KTAf/FlgH/yJkB/8qcAf/NngH/z6EB/9KkAf/UpwH/16oB/9msAf/crwH/3rEA/+S5Hf/uzHT/8NCL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/pXpA/283AP90PQH/d0AB/3pCAf99RgH/gEkB/4NMAf+GUAH/iVIA/8y0kv/////////+/////v////7////+/////v////7//fz7/5ZxVP9qMQD/czsB/3pCAf+ASAH/hk8B/4xWAf+TXQH/mWQB/59rAf+mcgH/rHkB/7OAAf+5iAH/uokC/7F/Av+ibgL/mmUC/5tnAf+gbAH/pHAB/6h1Af+seQH/sH4B/7SCAf+5hwH/vIsB/8CQAf/ElQH/yJkB/8yeAf/QogH/1KYB/9irAf/crwD/4LMB/+W+Lv/m053/+vfw//////////7////+/////v////7////+/////v////7////+///+/v///v7///7+///+/v///////v36//jruv/duUz/toQI/7WDAP+5hwH/u4oB/72NAf+/jwH/wZIB/8SVAf/HmAH/yZsB/8ydAf/OoAH/0aMB/9OmAf/WqAH/2KsB/9uuAP/itx7/7cpu//DQi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+keT//bzYA/3M8Af92PwH/ekIB/31FAf+ASAH/g0sB/4ZPAf+IUAD/zLSR//////////7////+/////v////7////+/////v/9/Pv/lXBU/2kvAP9xOgH/eEAB/35GAf+ETQH/i1QB/5FbAf+XYgH/nmkB/6RwAf+qdwH/sH4B/7eFAf+9jAH/w5QB/8aXAv++jQL/rHkC/6FtAv+ibgH/p3QB/6t4Af+vfQH/s4EB/7eGAf+7igH/v48B/8OTAf/HmAH/y5wB/8+hAf/TpQH/16kA/960Gf/t1Hj/+vPe///////////////+/////v////7////+/////v////7////+/////v///v7///7+///+/v////////////rz2v/u02z/570S/+W4AP/HmAL/tYMB/7iGAf+6iQH/vYwB/76OAf/BkQH/w5QB/8aXAf/ImgH/y5wB/82fAf/QogH/0qUB/9WnAP/YqwP/4bgw/+3Ld//w0Iv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6R4P/9uNQD/czsB/3Y+Af95QQH/fEQB/39HAf+CSwH/hU4B/4dPAP/Ls5H//////////v////7////+/////v////7////+//38+/+TblT/Zy0A/3A4Af92PgH/fEUB/4NMAf+JUgH/j1kB/5ZgAf+cZwH/om4B/6h1Af+vfAH/tYMB/7uKAf/BkQH/x5gB/86gAf/RowL/x5gD/7KAA/+mcwH/qXYB/657Af+ygAH/toQB/7qJAf++jQH/wZIB/8WWAf/JmwH/zZ4A/9OmCv/jw1f/9uzH///+/P////////7+///+/v///v7////+/////v////7////+/////v///v7///7+///+/v///v7///////z57f/x3ZX/5b8p/+O2Af/luQD/57wB/+O3Av/AkAP/toQB/7mIAf+8iwH/vo0B/8CQAf/CkwH/xZYB/8eZAf/KmwH/zJ4B/8+hAf/RowD/16oP/+S9S//vzoL/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/o3g//200AP9yOgH/dT0B/3hAAf97QwH/fkYB/4FKAf+ETQH/hk8A/822lf/////////+/////v////7////+/////v////7//Pz7/5JtVP9lKwD/bjYB/3Q9Af97QwH/gUoB/4dRAf+OWAH/lF4B/5plAf+gbAH/p3MB/616Af+zgQH/uogB/7+PAf/FlgH/y50B/9KkAf/ZrAH/260C/8maA/+wfgL/rHkB/7F+Af+1gwH/uYcB/72MAf/AkAH/xJQA/8iZA//WsTj/7t2p//379P////////7+///+/v///v7///7+///+/v///v7////+///+/v///v7///7+///+/v///v7///////79+f/05rf/5cJE/9+yBf/gtAD/4rYB/+S5Af/muwH/6b4B/9yvA/+5iAL/uIYB/7uJAf+9jAH/v48B/8GSAf/ElQH/xpcB/8maAf/LnAD/z6EF/9qwLP/pxmr/8NCJ//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+jdz//bDMA/3E5Af90PAH/d0AB/3pCAf99RQH/gEkB/4NMAf+GTgD/z7iY//////////7////+/////v////7////+/////v/8/Pv/kWxU/2MpAP9sNAH/cjsB/3lBAf9/SAH/hU8B/4xWAf+SXAH/mGMB/59qAf+lcQH/q3gB/7F/Af+4hgH/vo0B/8OUAf/KmwH/0KIB/9apAf/dsAH/5LgB/9utA/+5iAP/r3wB/7OBAf+3hgH/u4oA/76NAP/KnyD/48uG//n05v/////////+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7////////+/v/379P/5sll/9ywEP/brgD/3rEB/+CzAf/itgH/5LgB/+a6Af/nvAH/6b0B/8qbA/+2hQH/uogB/7yLAf++jgH/wJEB/8OTAf/FlgD/yJkB/9GlG//ivVf/7s6D//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6J3P/9rMgD/cDgB/3M7Af92PwH/eUEB/3xEAf9/SAH/gksB/4VOAP/OuJj////////+/v///v7////+/////v////7////+//z8+/+Qa1T/YScA/2syAf9xOQH/d0AB/31GAf+ETQH/ilQB/5BbAf+XYgH/nWgB/6NvAf+pdgH/sH0B/7aEAf+8iwH/wpIB/8iZAf/OoAH/1acB/9uuAf/htQH/6b0B/+GzA/+3hgL/sX8B/7WDAP+9jg//1bdj//Pq0v///v7////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////69ej/6tOI/9qxIf/XqQD/2awA/9uuAf/dsQH/37MB/+G1Af/jtwH/5bkB/+e7Af/qvgH/3K8C/7iHAf+5hwH/u4oB/72NAf+/jwH/wZIA/8mbEf/askX/68p7//DRi//w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/onY//2oxAP9vNwH/cjoB/3U+Af94QQH/e0MB/35HAf+BSgH/hE0A/863mP////////7+///+/v////7////+///+/v////7//Pz7/49qVP9gJQD/aTAB/283Af91PgH/fEQB/4JLAf+IUgH/j1kB/5VgAf+bZwH/oW4B/6h0Af+uewH/tIIB/7qJAf/AkAH/xpcB/8yeAf/TpQH/2awB/9+zAf/mugH/7cEB/8qZAf+wfgX/xqFD/+ratv/9+/j////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///////9+/b/79+u/9q1Ov/TpQP/1KcA/9epAf/ZrAH/2q4B/92wAf/esgH/4LQB/+K2Af/kuQH/5rsB/+m9Af/ktwH/vIsB/7eGAf+6iQH/vIsA/8GRCP/SpzT/58Nv//DQiv/w0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+hdT//aTAA/282Af9xOgH/dD0B/3hAAf97QwH/fkYB/4FJAf+DTAD/zreY/////////v7///7+///+/v////7///7+/////v/9/Pv/j2pU/14jAP9nLgH/bTUB/3Q8Af96QgH/gEkB/4dQAf+NVwH/k14B/5llAf+gbAH/pnMB/6x6Af+zgAH/uYcB/7+OAf/ElQH/y5wB/9GjAf/XqgH/3rEB/+S4AP/pvAH/0aYq/9vElP/59e3////////+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+/////////v3/9OnL/92+W//Qowz/0KEA/9KkAf/UpwH/1qkB/9irAf/arQH/3K8B/96xAf/gtAH/4rYB/+S4Af/mugH/6L0B/+S4Af+8iwH/toQA/7mIAv/HmiL/37pg/+7Ohv/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/6B1P/9pMAD/bjUB/3E5Af90PAH/dz8B/3pCAf99RQH/gEgB/4JLAP/Nt5j////////+/v///v7///7+///+/v///v7////+//38+/+PalT/XSIA/2UsAf9sMwH/cjoB/3hBAf9/RwH/hU4B/4tVAf+RXAH/mGMB/55qAf+kcQH/q3gB/7F/Af+3hQH/vY0B/8OTAf/JmgH/z6EB/9aoAf/brgD/5boU/+3ScP/17dv//////////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+////////+PLi/+LIfv/PpBv/y5wA/86fAP/QogH/0qQB/9SmAf/WqAH/16oB/9msAf/brwH/3bEB/9+zAf/htQH/47cB/+W5Af/ovQH/3K4B/7aEAf+9jRT/1K1M/+rJf//x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/oHQ//2gvAP9tNAH/cDgB/3M7Af92PwH/eUEB/3xEAf9/RwH/gUoA/822mP////////7+///+/v///v7///7+///+/v////7//fz7/49qVP9cIQD/YyoB/2oxAf9wOAH/dz8B/31FAf+DTAH/iVMB/5BaAf+WYQH/nGgB/6NvAf+pdgH/r30B/7WEAf+8iwH/wZEB/8eYAf/NngD/1acI/+XDTv/36sD//v36/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///////Pjx/+jUoP/PqDH/x5gC/8maAP/LnQH/zZ8B/8+hAf/RowH/06UB/9WoAf/XqgH/2awB/9uuAf/dsAH/37IB/+G0Af/jtwH/5bkB/+W5AP/Kmwz/yZ45/+XCdP/w0Iv/8NGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+fcz//Zy4A/2wzAf9vNwH/cjoB/3U+Af94QAH/e0MB/35GAf+ASQD/zLaY/////////v7///7+///+/v///v7///7+/////v/9/Pv/j2pU/1sgAP9iKAH/aC8B/282Af91PQH/e0MB/4FKAf+IUQH/jlgB/5RfAf+bZgH/oW0B/6d0Af+tewH/tIIB/7qJAf+/jwD/xZYC/9WtMf/t2p///fnx/////////v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///////vz6/+7hwP/Sr07/xJQI/8SUAP/GmAH/yJoB/8qcAf/MngH/zqAB/9CiAf/SpQH/1KcB/9apAf/YqwH/2q0B/9yvAf/esgH/4LQB/+K2AP/ktwT/4LQr/+C7Z//uzoj/8dGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/59zP/9mLQD/azIB/242Af9xOQH/dD0B/3dAAf96QgH/fUUB/4BIAP/Mtpj////////+/v///v7///7+///+/v///v7////+//7+/P+Tb1r/WyAA/2AnAf9mLQH/bTQB/3M7Af95QgH/gEgB/4ZPAf+MVgH/kl0B/5lkAf+fawH/pXIB/6x5Af+yfwD/t4UA/8SXG//fxX7/+PLi/////////v////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v/////////+//Ts2f/Yum//wpUU/7+PAP/CkgH/xJUB/8aXAf/ImQH/ypsB/8ydAf/OoAH/0KIB/9KkAf/TpgH/1agB/9eqAf/ZrQH/3K8B/92xAP/fswH/5LkY/+jDVP/tzIP/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/nnI//2UsAP9qMgH/bTUB/3A4Af9zPAH/dj8B/3lCAf98RQH/f0cA/8y1mP////////7+///+/v///v7///7+///+/v///v7//////519av9bIAD/XyUB/2UrAf9rMgH/cTkB/3hAAf9+RgH/hE0B/4pUAf+RWwH/l2IB/51pAf+kcAH/qXUA/7OBDP/OrFr/8OXL//7+/f////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///////n17P/fyJL/xJkn/7yKAf++jQD/v5AB/8GSAf/DlAH/xZYB/8eYAf/JmwH/y50B/82fAf/PoQH/0aMB/9OlAf/VpwH/16oB/9msAf/brgD/3rIM/+a/P//uzHj/8NCL//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+dcj//ZCsA/2kxAf9sNAH/cDcB/3M7Af92PgH/eUEB/3xEAf9+RgD/y7WY/////////v7///7+///+/v///v7///7+///+/v//////t6GT/1wiAP9eJAH/YykB/2kwAf9wNwH/dj4B/3xEAf+CSwH/iVIB/49ZAf+VYAH/m2YA/6JuBP+6kjz/49Gt//z59v////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///////369//o17P/x6BB/7iHBf+5iAD/vIsB/76NAf+/jwH/wZEB/8OTAf/FlgH/x5gB/8maAf/LnAH/zZ4B/8+gAf/QowH/0qUB/9SnAf/WqQD/2awF/+G4LP/ryGr/8NCJ//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/51xP/9jKgD/aTAB/2wzAf9vNgH/cjoB/3U9Af94QAH/e0MB/31FAP/LtJj////////+/v///v7///7+///+/v///v7///7+///////d083/aTQX/10jAP9hKAH/aC8B/241Af90PAH/ekMB/4FJAf+HUAH/jVcA/5JcAP+mdyP/0rmL//fx6f////////7+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///////7+/f/v5M//zaxg/7aGDv+0ggD/t4YB/7mIAf+7igH/vYwB/7+OAf/AkQH/wpMB/8SVAf/GlwH/yJkB/8qbAf/MngH/zqAB/9CiAf/SpAD/1KYC/9uwHf/nwlj/78+E//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/nHE//2MpAP9oLwH/azIB/242Af9xOQH/dDwB/3dAAf96QgH/fEQA/8u0mP////////7+///+/v///v7///7+///+/v///v7///7+//z7+v+dfGr/WyEA/2AmAf9mLQH/bDQB/3I6Af95QQH/f0cB/4RMAP+RXhD/u5pm/+3j1P///v7////+///+/v///v7///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///7+///////28OT/1buC/7eJHv+wfQD/s4AA/7WDAf+3hQH/uYcB/7uKAf+9jAH/vo4B/8CQAf/CkgH/xJQB/8WWAf/HmQH/yZsB/8udAf/NnwH/z6EA/9WoEf/hukf/7cx8//DRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ccD//YigA/2cuAf9qMQH/bTUB/3A4Af9zOwH/dj8B/3lBAf97QwD/yrOY/////////v3///7+///+/v///v7///7+///+/v///v7//////+rj3/+IYEj/XiQC/2InAP9pLwD/bzYA/3U8AP+BSwr/pHxJ/93Ouf/8+vn////////+/f///v3///79///+/v///v7///7+///+/v///v7///79///+/f///v3///79///////79/L/3sql/7qQNf+seQL/rnsA/7B+Af+ygAH/tIIB/7aEAf+4hwH/uokB/7yLAf++jQH/v48B/8GRAf/DlAH/xZYB/8eYAf/JmgH/ypwA/86gCP/asTT/6sdw//DQiv/w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5tvPv9hJwD/Zi0B/2kwAf9sNAH/bzcB/3I6Af91PgH/eEEB/3tCAP/Ks5j////////+/f///v7///7+///+/v///v7///7+///+/v///v7///////Dq5/+xl4n/h15C/4JUL/+NYjr/qoln/9bFs//39PD////////+/v///v3///79///+/f///v3///79///+/v///v7///79///+/f///v3///79///////+/fv/+OvA/+bET/+7igr/qHUA/6x5Af+uewH/sH0B/7F/Af+zggH/toQB/7eGAf+5iAH/u4oB/72MAf+/jwH/wJEB/8KTAf/ElQH/xpcA/8iZAv/SpyL/5MBg/+/Ph//w0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/m28+/2AmAP9lLAH/aC8B/2szAf9uNgH/cTkB/3Q9Af93QAH/ekIA/8qzmP////////79///+/v///v7///7+///+/v///v7///7+///+/v///v7////////+/v/49fT/8+7r//fz8f/+/f3////////+/v///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/v//////+vPf/+3SdP/luhX/5roA/+O2Af/DkgP/q3kC/616Af+vfQH/sX8B/7OBAf+1gwH/t4UB/7mHAf+7iQH/vYwB/76OAf/AkAH/wZIA/8OUAf/LnRT/3bZO/+zMgP/w0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+abj7/XyUA/2QrAf9nLgH/ajIB/241Af9xOQH/dDwB/3c/Af95QQD/ybKY/////////v3///7+///+/v///v7///7+///+/v///v7///7+///+/f///v3///7+///////////////+///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///////Pnv/+/bmv/iuy3/37IB/+K2AP/lugH/6b0B/+i8Av/ImQT/rXsC/658Af+wfgH/soAB/7SCAf+2hQH/uIcB/7qJAf+8iwH/vo0B/7+PAP/Elgz/1aw8/+nGdf/w0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5puPv9eJAD/ZCoB/2cuAf9qMQH/bTQB/3A4Af9zOwH/dj4B/3hAAP/Jspj////////+/f///v3///7+///+/f///v3///7+///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///////vz5//Lkuv/gvkn/2awH/9uuAP/esgH/4bUB/+S5Af/nvAH/678B/+y/Av/ImAT/rnsB/7B9Af+ygAH/tIIB/7aEAf+4hgH/uogB/7uKAP++jgX/zaEq/+O/aP/vz4j/8NGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/mm0+/14jAP9jKQH/Zi0B/2kwAf9sMwH/bzcB/3I6Af91PQH/dz8A/8evlv////////79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f////7///7+//bt1v/hxGr/1KgS/9SmAP/YqgH/264B/96wAv/htAH/5LgB/+e7Af/qvgH/7cIB/+i8Av+6iQP/r3wB/7F/Af+zgQH/tYMB/7eFAP+5hwH/xJYb/9u1V//tzIP/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ZbT7/XSMA/2IoAf9lLAH/aC8B/2syAf9uNgH/cTkB/3Q8Af92PgD/w6mN/////////v7///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v7///////r16f/lzo3/0ack/82eAP/QogD/1KYB/9epAv/arAL/3a8C/+CzAv/jtwH/5roB/+m9Af/swAH/8MQB/9KiAv+uewH/sH4B/7KAAf+0ggD/u4oO/9CnQv/ox3r/8NGL//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5ltPv9cIgD/YScB/2QrAf9nLgH/ajIB/201Af9wOAH/czsB/3Q8AP+xkW7////////+/v///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///////369v/r2q7/0as+/8eXBP/JmgD/zZ4B/9ChAv/TpAL/1qgC/9mrAv/crgL/37IB/+K2Af/luQH/6LwB/+u/Af/vxAH/2qwB/658Af+vfQD/tIIH/8aaMP/hvm3/79CK//HRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/mW0+/1wiAP9gJgH/YyoB/2YtAf9pMQH/bDQB/283Af9yOgH/czsA/5tzRv/69/X///7+///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3////+//7+/P/x5cv/1LNd/8KTDf/CkgD/xpYB/8mZAv/MnQL/z6AC/9KjAv/VpwL/2KsB/9uuAf/esgH/4bUB/+S4Af/nvAH/6r4B/+/DAf/UpAH/rXsD/76PIv/atF7/7c2F//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ZbT7/XCEA/2AmAf9iKQH/ZSwB/2kwAf9sMwH/bzYB/3I6Af90PAD/hlUe/+vj2v////////79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///79///+/f///v3///7+///////28OL/2b5+/8CTHP+8igD/v48B/8KSAv/FlQL/yJgC/8ucAv/OnwL/0aMB/9SnAf/XqgH/2q0B/92xAf/gtAH/47cB/+a7Af/qvgD/6LsB/8WWFf/OpUv/6ch+//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5ltPv9cIQD/XyUB/2IoAf9lKwH/aC8B/2syAf9uNQH/cTkB/3Q8Af93QAP/yLKa/////////v3///79///+/f///v7///7+///+/f///v3///79///+/f///v3///79///+/f///v3///79///////79/H/4cyg/8GXMv+2gwL/uYcA/7yLAf+/jgL/wZEC/8SUAv/HmAL/ypwB/82fAf/QogH/06YB/9apAf/arQH/3bAB/9+zAf/itgH/5roA/+m8Cf/gtjr/48B0//DQiv/w0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/mW0+/1whAP9eJAH/YScB/2QrAf9nLgH/ajEB/200Af9wOAH/czsB/3Q8AP+Wazz/8+7p/////////v3///79///+/v///v7///79///+/f///v3///79///+/f///v3///79///////9/Pr/6dvA/8WgT/+xfwj/sn8A/7WEAf+4hwH/u4oB/76NAv/AkAL/xJQC/8eXAf/KmwH/zZ4B/9CiAf/TpQH/1qgB/9msAf/crwH/37IA/+K2A//ovyX/7Mhj/+7OiP/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ZbT7/XCEA/14kAf9gJgH/YyoB/2YtAf9pMAH/bDQB/283Af9yOgH/dT0B/3hBA/+7nn///fz6/////v///v3///79///+/f///v3///79///+/f///v3///79/////v////7/8enZ/8utcP+ufRT/qncA/658Af+xfwH/tIMB/7eGAf+7iQH/vY0B/8CQAf/DkwH/xpcB/8maAf/MnQH/z6EB/9KkAf/VpwH/2KoA/9uuAf/hthj/6sVS/+/Pgv/w0Iv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5ltPv9cIQD/XiQB/18lAf9iKQH/ZSwB/2gvAf9rMwH/bjYB/3E5Af90PQH/dz8A/4BKDf/Cp4n/+vf1//////////7///79///+/f///v3////+////////////9vDn/9O7j/+vgij/pG8B/6d0AP+reAH/rnsB/7F+Af+0ggH/t4UB/7qIAf+9jAH/v48B/8KSAf/FlgH/yJkB/8ucAf/OoAH/0aMB/9SmAP/ZrA3/5LxA/+3MeP/w0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0Yv/mW0+/1whAP9eJAH/XyUB/2EoAf9kKwH/Zy4B/2oyAf9tNQH/cDgB/3M8Af92PwH/eUEA/39JCP+sh1v/4tXF//j18f/+/fz////+//78+//49O7/6N3L/8yyhv+tgjT/nmoE/6BrAP+kcAH/p3MB/6p3Af+tegH/sH0B/7OBAf+2hAH/uYcB/7yLAf++jgH/wZEB/8SVAf/HmAH/ypsB/82eAP/RowX/3LIu/+rHa//w0In/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DRi/+ZbT7/XCEA/14kAf9eJAH/YScB/2QqAf9nLQH/ajEB/200Af9wNwH/czsB/3Y+Af95QQH/e0MB/31FAP+JVhP/n3Q8/7KPX/+5mGj/s49Z/6d8N/+baRP/lmAB/5ljAP+daAH/oGwB/6NvAf+mcgH/qXYB/6x5Af+vfQH/soAB/7WDAf+4hgH/u4oB/76NAf/AkQH/w5QB/8aXAP/JmgH/06Yc/+O+Wf/uzoT/8NGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NGL/5tvQP9cIQD/XiQB/14kAf9gJgH/YykB/2YtAf9pMAH/bDMB/283Af9yOgH/dT0B/3hAAf97QwH/fkYB/4BJAP+CSwD/hU0A/4hRAP+LVAD/j1gA/5NdAP+WYQH/mWQB/5xoAf+fawH/om4B/6VyAf+odQH/q3gB/658Af+xfwH/tIIB/7eGAf+6iQH/vYwB/7+PAf/CkgD/ypwR/9uzRv/rynz/8NGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0ov/pHlH/1wiAP9eJAH/XiQB/18lAf9iKAH/ZSwB/2gvAf9rMgH/bjYB/3E5Af90PAH/d0AB/3pCAf99RQH/gEkB/4NMAf+GTwH/iVMB/4xWAf+PWQH/kl0B/5VgAf+YYwH/m2cB/55qAf+hbQH/pHEB/6d0Af+qdwH/rXsB/7B+Af+zgQH/toUB/7mIAf+8iwD/wZEI/9KoNf/nxHH/8NCK//DQiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//LSi/+rgEz/XSMA/14kAf9eJAH/XiUB/2EnAf9kKwH/Zy4B/2oxAf9tNQH/cDgB/3M7Af92PwH/eUEB/3xEAf9/SAH/gksB/4VOAf+IUgH/i1UB/45YAf+RXAH/lF8B/5diAf+aZgH/nWkB/6BsAf+jcAH/pnMB/6p2Af+tegH/sH0B/7OAAf+1gwD/uYcC/8eaI//fumH/7s6G//HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8tOL/7iQWf9fJgP/XiQB/14kAf9eJAH/YCYB/2MqAf9mLQH/aTAB/2w0Af9vNwH/cjoB/3U+Af94QQH/e0MB/35HAf+BSgH/hE0B/4dRAf+KVAH/jVcB/5BbAf+TXgH/l2EB/5llAf+daAH/oGsB/6JvAf+mcgH/qXUB/6x5Af+ufAD/sX8B/7yNFf/VrU7/68p///HRi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/y0ov/yaRo/2QsCP9eIwH/XiQB/14kAf9fJgH/YikB/2UsAf9oLwH/azMB/242Af9xOgH/dD0B/3dAAf96QwH/fUYB/4BJAf+ETQH/h1AB/4pTAf+NVgH/kFoB/5NdAf+WYQH/mWQB/5xnAf+fagH/om4B/6VxAf+odAH/qncA/7F/Cv/Jnjr/5cN1//DRi//w0Ir/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Ul68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HRiv/du3v/cz0W/10iAP9eJAH/XiQB/18lAf9hKAH/ZSsB/2gvAf9rMgH/bjUB/3E5Af90PAH/dz8B/3pCAf99RQH/gEgB/4NMAf+GTwH/iVIB/4xWAf+PWQH/klwB/5VgAf+YYwH/m2YB/55qAf+hbQH/o28A/6h1Bf+8jij/27dm/+7OiP/x0Yr/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA0LR2AM6zdSXrzIbl8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+3Nh/+RYjT/XCIA/14kAf9eJAH/XiQB/2EnAf9kKgH/Zy4B/2oxAf9tNAH/cDgB/3M7Af92PgH/eUEB/3xEAf9/RwH/gksB/4VOAf+IUQH/i1UB/45YAf+RWwH/lF8B/5diAf+aZQH/nWgA/6BsAf+wgBr/0apV/+vKgv/x0Yv/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/rzIblzrN2JdC0dwDQtHYAzrN1JevMhuXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8tKL/7qSWv9hJwT/XiQB/14kAf9eJAH/YCYB/2MpAf9mLQH/aTAB/2wzAf9vNwH/cjoB/3U+Af94QQH/e0MB/35GAf+BSgH/hE0B/4dRAf+KVAH/jVcB/5BbAf+TXgH/lmEB/5hjAP+ibw3/w5hC/+XDev/x0Yv/8NCK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+vMhuXOs3Yl0LR3ANC0dgDOs3Yl68yG5fDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yr/3718/3lEHP9dIgD/XiQB/14kAf9fJQH/YikB/2UsAf9oLwH/azIB/242Af9xOQH/dD0B/3dAAf96QgH/fUYB/4BJAf+DTAH/hlAB/4lTAf+MVgH/j1kB/5FcAP+YYwb/soQu/9m1a//vz4n/8dGK//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/68yG5c6zdiXQtHcA1Lh5ANS3eSDszIfh8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yr/sIZR/18mA/9eJAH/XiQB/18lAf9hJwH/ZCsB/2cuAf9qMgH/bTUB/3A4Af9zPAH/dj8B/3lBAf98RAH/f0gB/4JLAf+FTwH/iFIB/4tUAP+PWQL/onEd/8ylWv/ry4X/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/szYfh1Lh5INS4eQDRtXcA0rZ4FezMh9Tw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HRiv/kw4H/iVgt/10iAP9eJAH/XiQB/2AnAf9jKgH/Zi0B/2kxAf9tNAH/bzcB/3I7Af91PgH/eEEB/3xEAf9/RwH/gkoB/4RNAf+GUAD/lWER/76USf/kw33/8dGL//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+zMh9TTtngV0bV3AMWrcQDApm0H6suGtvDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HSiv/XtHX/fksi/10iAP9eJAH/YCYB/2MpAf9mLAH/aTAB/2wzAf9vNgH/cjoB/3U9Af94QAH/e0MB/31GAf9/SAD/iVMJ/6t+Nf/atnD/8NCK//HRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/6suGtsCmbQfFq3EAfW1HAP//rQDjxYKE8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HSi//YtXb/ilkt/2AmA/9eIwD/YigB/2UrAf9oLwH/azIB/242Af9xOQH/dDwB/3Y+AP94QAD/gksH/59vK//OqGT/7MyH//HSi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/jxYKE//+tAH1tSAAAAAAA5seDANq8fEbuzoj18NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HSiv/lxIH/roVR/3hFHf9kLAb/YikA/2UrAP9oLwD/azIA/283Af93QAf/iFUY/6Z4Ov/Np2b/6smE//HSi//w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7s6I9dq8fEbmx4MAAAAAAAAAAADPs3YAy7B0EerLhcTw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//HRiv/x0Yv/4L9+/8GbY/+nfEr/mm07/5psN/+idT//tIpQ/8ulZv/hwH3/7s+J//LSi//w0Yn/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/qy4XEy7B0Ec+zdgAAAAAAAAAAAI57UQD/6ZoA38F/Z+/PiPvw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/x0Yr/8tOL//HSjP/w0Iv/79CK//DRi//y0oz/8tKL//HRiv/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/78+I+9/Bf2f/6ZoAjntRAAAAAAAAAAAAAAAAANO3eADMsXUT6MmFvvDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/oyYW+zLF1E9O3eAAAAAAAAAAAAAAAAAAAAAAAaFs7APXUjADZvXxD7M2H6PDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7M2H6Nm8fEP11IwAaFo7AAAAAAAAAAAAAAAAAAAAAAAAAAAAs5tmACEdEgHfwX9q7s6I9PDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ/+7OiPTfwX9qIR0SAbObZgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxapwALCYZAbhw4B27s6I8/DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/uzojz4cOAdrCYZAbFqnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAxqtxALObZgXewX9j7MyH4/DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7MyH497Bf2Ozm2YFxqtxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsJllAGRXOgHXuns258iEru7OiPXw0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/7s6I9efIhK7Xuns2ZFc6AbCYZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN7AfwDGrHEL2r19TufJhKfszYfj7s6I+vDQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/w0In/8NCJ//DQif/uzoj67M2H4+fJhKfavX1OxqxxC97AfwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwKBwDZvHwAwahuB9O3eS3bvn1k5MWClOnKhbToyYTC58mExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF6MmExejJhMXoyYTF58mExejJhMLpyoW05MWClNu+fWTTt3ktwahuB9m8ewAMCgcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/+AAAAAAAAAAAAAAAAAH//+AAAAAAAAAAAAAAAAAAf/+AAAAAAAAAAAAAAAAAAB//AAAAAAAAAAAAAAAAAAAP/gAAAAAAAAAAAAAAAAAAB/wAAAAAAAAAAAAAAAAAAAP8AAAAAAAAAAAAAAAAAAAD+AAAAAAAAAAAAAAAAAAAAfgAAAAAAAAAAAAAAAAAAAHwAAAAAAAAAAAAAAAAAAAA8AAAAAAAAAAAAAAAAAAAAPAAAAAAAAAAAAAAAAAAAADgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAABgAAAAAAAAAAAAAAAAAAAAYAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAAAAAAAAAAADwAAAAAAAAAAAAAAAAAAAA8AAAAAAAAAAAAAAAAAAAAPgAAAAAAAAAAAAAAAAAAAH4AAAAAAAAAAAAAAAAAAAB/AAAAAAAAAAAAAAAAAAAA/wAAAAAAAAAAAAAAAAAAAP+AAAAAAAAAAAAAAAAAAAH/wAAAAAAAAAAAAAAAAAAD/+AAAAAAAAAAAAAAAAAAB//4AAAAAAAAAAAAAAAAAB///gAAAAAAAAAAAAAAAAB/8="

# ====================== 跨平台字体配置 ======================
def get_cross_platform_font():
    """获取跨平台通用字体"""
    system = platform.system()
    if system == 'Windows':
        return '微软雅黑'
    elif system == 'Darwin':  # macOS
        return 'PingFang SC'
    else:
        return 'Microsoft YaHei'

DEFAULT_FONT = get_cross_platform_font()

# ====================== 配置 ======================
API_URL = "https://www.yuchenagent.com/api/get_draft_data"
CONFIG_PATH = "config.ini"

EXAMPLE_DRAFT_ID = "fde55ea-0ba9-484d-8e6a-1acbbaad15b"
PLACEHOLDER_UUID = "0E685133-18CE-45ED-8CB8-2904A212EC80"

# 未来时间戳（微秒级，对应2055-01-01 00:00:00）
FUTURE_TIMESTAMP_MICRO = 2684352000000000

# ====================== 路径 ======================
# 本地缓存目录
appdata_dir = os.environ.get('APPDATA', '')
if not appdata_dir:
    appdata_dir = os.path.expanduser("~")
CACHE_DIR = os.path.join(appdata_dir, "剪映小助手", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 同时将二维码隐藏目录也放在 AppData 下
QR_HIDDEN_DIR = os.path.join(appdata_dir, "剪映小助手", ".qr_cache")
os.makedirs(QR_HIDDEN_DIR, exist_ok=True)
QR_CACHE_PATH = os.path.join(QR_HIDDEN_DIR, hashlib.md5(b"wechat_qr").hexdigest()[:16] + ".dat")
QR_INFO_PATH = os.path.join(QR_HIDDEN_DIR, "info.txt")

def set_hidden_windows(path):
    """在Windows上设置文件/文件夹隐藏属性"""
    if sys.platform == 'win32':
        try:
            # 使用 CREATE_NO_WINDOW 避免在设置隐藏属性时弹出黑色命令行窗口，减少启动闪烁
            creationflags = 0
            if hasattr(subprocess, "CREATE_NO_WINDOW"):
                creationflags = subprocess.CREATE_NO_WINDOW
            subprocess.run(
                ['attrib', '+h', path],
                check=False,
                capture_output=True,
                creationflags=creationflags
            )
        except Exception:
            pass  # 忽略错误，不影响功能

# 立即隐藏二维码目录
set_hidden_windows(QR_HIDDEN_DIR)

def get_draft_root():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def set_draft_root():
    path = filedialog.askdirectory(title="选择剪映 Drafts 目录")
    if path:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(path)
        messagebox.showinfo("成功", f"草稿目录：\n" + path)

def clear_cache():
    """清理缓存（在子线程中执行）"""
    def task():
        try:
            if os.path.exists(CACHE_DIR):
                total_size = 0
                for item in os.listdir(CACHE_DIR):
                    item_path = os.path.join(CACHE_DIR, item)
                    # 跳过隐蔽二维码目录
                    if os.path.basename(item_path) == os.path.basename(QR_HIDDEN_DIR):
                        continue
                    if os.path.isfile(item_path):
                        total_size += os.path.getsize(item_path)
                    else:
                        for dirpath, dirnames, filenames in os.walk(item_path):
                            for filename in filenames:
                                filepath = os.path.join(dirpath, filename)
                                total_size += os.path.getsize(filepath)
                # 询问确认（需在主线程）
                def ask():
                    if messagebox.askyesno("确认清理", f"缓存目录大小：{total_size / 1024 / 1024:.2f} MB\n确定要清理所有缓存文件吗？"):
                        for item in os.listdir(CACHE_DIR):
                            item_path = os.path.join(CACHE_DIR, item)
                            if os.path.basename(item_path) == os.path.basename(QR_HIDDEN_DIR):
                                continue
                            if os.path.isfile(item_path):
                                os.remove(item_path)
                            else:
                                shutil.rmtree(item_path, ignore_errors=True)
                        # 直接写入日志控件，避免使用未定义的 log_message
                        try:
                            log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}]缓存目录清理完成\n")
                            log.see(tk.END)
                        except Exception:
                            pass
                root.after(0, ask)
            else:
                root.after(0, lambda: messagebox.showinfo("提示", "缓存目录不存在"))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("错误", f"清理缓存目录失败：{str(e)}"))

    threading.Thread(target=task, daemon=True).start()

def update_qr_background():
    """后台线程：检查并更新微信群二维码到隐蔽位置"""
    try:
        qr_url = "https://ai.yuchenagent.com/yuchen_weixin_erweima/wechat_qr.png"

        # 确保隐蔽目录存在并保持隐藏
        os.makedirs(QR_HIDDEN_DIR, exist_ok=True)
        set_hidden_windows(QR_HIDDEN_DIR)

        # 获取远程文件信息（HEAD请求）
        req = urllib.request.Request(qr_url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as resp:
            remote_etag = resp.headers.get('ETag', '').strip('"')

        # 读取本地ETag
        local_etag = ""
        if os.path.exists(QR_INFO_PATH):
            with open(QR_INFO_PATH, 'r') as f:
                local_etag = f.read().strip()

        # 判断是否需要更新（ETag不同 或 缓存文件不存在）
        if remote_etag and (remote_etag != local_etag or not os.path.exists(QR_CACHE_PATH)):
            temp_path = QR_CACHE_PATH + ".tmp"
            urllib.request.urlretrieve(qr_url, temp_path)
            os.replace(temp_path, QR_CACHE_PATH)
            set_hidden_windows(QR_CACHE_PATH)      # 隐藏文件
            with open(QR_INFO_PATH, 'w') as f:
                f.write(remote_etag)
            set_hidden_windows(QR_INFO_PATH)       # 隐藏信息文件
    except Exception:
        # 静默失败，不影响主程序
        pass

def download_file(remote_url, log_func, save_path, media_type=None):
    """下载文件到指定位置并返回文件名。成功后通过log_func输出日志"""
    try:
        parsed_url = urlparse(remote_url)
        original_filename = parsed_url.path.split('/')[-1] or "media"
        ext = os.path.splitext(original_filename)[-1]
        if not ext:
            if media_type in ['image', 'photo']:
                ext = '.jpg'
            elif media_type == 'audio':
                ext = '.mp3'
            elif media_type == 'video':
                ext = '.mp4'
            else:
                ext = '.mp4'
        file_name = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(save_path, file_name)

        log_func(f"[{time.strftime('%H:%M:%S')}]开始下载：{remote_url}\n")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "identity"
        }

        resp = requests.get(remote_url, headers=headers, stream=True, timeout=120)
        resp.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        log_func(f"[{time.strftime('%H:%M:%S')}]下载完成：{remote_url}\n", "green")
        return file_name

    except Exception as e:
        raise Exception(f"下载失败：{str(e)}")

def save_cache(draft_id, data):
    """保存草稿数据到本地缓存"""
    try:
        cache_file = os.path.join(CACHE_DIR, f"{draft_id}.json")
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        return True
    except Exception as e:
        return False

def load_cache(draft_id):
    """从本地缓存加载草稿数据"""
    try:
        cache_file = os.path.join(CACHE_DIR, f"{draft_id}.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    except Exception as e:
        return None

def convert_to_jianying_pro(data, draft_id, log_func):
    """
    将API返回的原始数据转换为剪映可识别的格式，并替换所有时间戳为未来时间。
    """
    result = copy.deepcopy(data)

    # 递归替换所有时间戳为未来时间
    def replace_timestamps(obj):
        try:
            if isinstance(obj, dict):
                for key, value in list(obj.items()):
                    # 跳过关键帧中的 time_offset 字段
                    if key == 'time_offset':
                        continue
                    if isinstance(value, int) and ('time' in key.lower() or 'timestamp' in key.lower()):
                        obj[key] = FUTURE_TIMESTAMP_MICRO
                    else:
                        replace_timestamps(value)
            elif isinstance(obj, list):
                for item in obj:
                    replace_timestamps(item)
        except Exception as e:
            log_func(f"[{time.strftime('%H:%M:%S')}]时间戳替换出错: {e}\n")

    replace_timestamps(result)

    # 收集需要下载的素材
    download_list = []
    materials = result.get("materials", {})
    for mat_type, mat_list in materials.items():
        if mat_type in ["videos", "audios"]:
            for mat in mat_list:
                if 'path' in mat and mat['path'].startswith('http'):
                    download_list.append((mat, mat['path'], mat_type.rstrip('s')))
        elif mat_type == "images":
            for mat in mat_list:
                if 'path' in mat and mat['path'].startswith('http'):
                    download_list.append((mat, mat['path'], 'image'))

    return result, download_list

def generate():
    draft_id = entry_id.get("1.0", tk.END).strip()
    if not draft_id:
        messagebox.showwarning("提示", "请输入 draft_id")
        return
    root_path = get_draft_root()
    if not root_path:
        messagebox.showwarning("提示", "请先设置剪映目录")
        return

    # 禁用生成按钮
    def disable_btn():
        generate_btn.configure(text="生成中...", state=tk.DISABLED)
    root.after(0, disable_btn)

    # 启动子线程执行耗时任务
    def task():
        try:
            # 安全日志函数
            def log_msg(msg, tag=None):
                root.after(0, lambda: log_insert(msg, tag))

            def log_insert(msg, tag):
                log.insert(tk.END, msg, tag)
                log.see(tk.END)

            log_msg(f"[{time.strftime('%H:%M:%S')}]开始解析剪映草稿...\n\n")
            log_msg(f"[{time.strftime('%H:%M:%S')}]开始处理第1个草稿：{draft_id}\n")

            # 优先从本地缓存加载
            cached_data = load_cache(draft_id)
            if cached_data:
                log_msg(f"[{time.strftime('%H:%M:%S')}]从本地缓存加载草稿数据\n")
                original = cached_data
            else:
                log_msg(f"[{time.strftime('%H:%M:%S')}]获取草稿数据\n")
                resp = requests.post(API_URL, json={"draft_id": draft_id}, timeout=20)
                data = resp.json()
                if data.get("code") != 0:
                    log_msg(f"[{time.strftime('%H:%M:%S')}]接口错误：{data.get('msg')}\n")
                    root.after(0, lambda: messagebox.showerror("错误", f"接口返回错误：{data.get('msg')}"))
                    return
                original = data["data"]["draft_content"]
                save_cache(draft_id, original)
                log_msg(f"[{time.strftime('%H:%M:%S')}]草稿数据已保存到本地缓存\n")

            final_json, download_list = convert_to_jianying_pro(original, draft_id, log_msg)

            if not isinstance(final_json, dict):
                log_msg(f"[{time.strftime('%H:%M:%S')}]❌ 转换结果不是字典，无法写入\n")
                root.after(0, lambda: messagebox.showerror("错误", "转换结果不是字典"))
                return

            # 创建临时文件夹
            tmp_folder_name = f"tmp_{uuid.uuid4().hex}"
            tmp_folder = os.path.join(root_path, tmp_folder_name)
            os.makedirs(tmp_folder, exist_ok=True)
            log_msg(f"[{time.strftime('%H:%M:%S')}]创建草稿文件夹：{tmp_folder_name}\n")

            final_folder = os.path.join(root_path, draft_id)

            materials_folder_name = str(uuid.uuid4())
            materials_folder = os.path.join(tmp_folder, materials_folder_name)
            os.makedirs(materials_folder, exist_ok=True)

            for item, url, media_type in download_list:
                try:
                    file_name = download_file(url, log_msg, materials_folder, media_type=media_type)
                    item['path'] = f"##_draftpath_placeholder_{PLACEHOLDER_UUID}_##\\{materials_folder_name}\\{file_name}"
                    log_msg(f"[{time.strftime('%H:%M:%S')}]素材已下载：{file_name}\n")
                except Exception as e:
                    log_msg(f"[{time.strftime('%H:%M:%S')}]❌ 下载失败：{url} - {str(e)}\n")

            def write_json_safe(filepath, data):
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
                    f.flush()
                    os.fsync(f.fileno())

            write_json_safe(os.path.join(tmp_folder, f"{materials_folder_name}.json"), final_json)
            write_json_safe(os.path.join(tmp_folder, "draft_content.json"), final_json)
            write_json_safe(os.path.join(tmp_folder, "draft_info.json"), final_json)

            current_time_micro = int(time.time() * 1_000_000)
            meta = {
                "cloud_draft_cover": True,
                "cloud_draft_sync": True,
                "cloud_package_completed_time": "",
                "draft_cloud_capcut_purchase_info": "",
                "draft_cloud_last_action_download": False,
                "draft_cloud_package_type": "",
                "draft_cloud_purchase_info": "",
                "draft_cloud_template_id": "",
                "draft_cloud_tutorial_info": "",
                "draft_cloud_videocut_purchase_info": "",
                "draft_cover": "draft_cover.jpg",
                "draft_deeplink_url": "",
                "draft_enterprise_info": {
                    "draft_enterprise_extra": "",
                    "draft_enterprise_id": "",
                    "draft_enterprise_name": "",
                    "enterprise_material": []
                },
                "draft_fold_path": final_folder.replace('\\', '/'),
                "draft_id": str(uuid.uuid4()).upper(),
                "draft_is_ae_produce": False,
                "draft_is_ai_packaging_used": False,
                "draft_is_ai_shorts": False,
                "draft_is_ai_translate": False,
                "draft_is_article_video_draft": False,
                "draft_is_cloud_temp_draft": False,
                "draft_is_from_deeplink": "false",
                "draft_is_invisible": False,
                "draft_is_web_article_video": False,
                "draft_materials": [
                    {"type": 0, "value": []},
                    {"type": 1, "value": []},
                    {"type": 2, "value": []},
                    {"type": 3, "value": []},
                    {"type": 6, "value": []},
                    {"type": 7, "value": []},
                    {"type": 8, "value": []}
                ],
                "draft_materials_copied_info": [],
                "draft_name": draft_id,
                "draft_need_rename_folder": False,
                "draft_new_version": "",
                "draft_removable_storage_device": os.path.splitdrive(final_folder)[0],
                "draft_root_path": root_path.replace('\\', '\\\\'),
                "draft_segment_extra_info": [],
                "draft_timeline_materials_size_": len(download_list),
                "draft_type": "",
                "draft_web_article_video_enter_from": "",
                "tm_draft_cloud_completed": "",
                "tm_draft_cloud_entry_id": -1,
                "tm_draft_cloud_modified": 0,
                "tm_draft_cloud_parent_entry_id": -1,
                "tm_draft_cloud_space_id": -1,
                "tm_draft_cloud_user_id": -1,
                "tm_draft_create": current_time_micro,
                "tm_draft_modified": FUTURE_TIMESTAMP_MICRO,
                "tm_draft_removed": 0,
                "tm_duration": 0
            }
            write_json_safe(os.path.join(tmp_folder, "draft_meta_info.json"), meta)

            pc_common = {
                "pc_feature_flag": 0,
                "template_item_infos": [],
                "unlock_template_ids": []
            }
            write_json_safe(os.path.join(tmp_folder, "attachment_pc_common.json"), pc_common)

            agency_config = {
                "marterials": None,
                "use_converter": False,
                "video_resolution": 720
            }
            write_json_safe(os.path.join(tmp_folder, "draft_agency_config.json"), agency_config)

            with open(os.path.join(tmp_folder, "template.tmp"), "w") as f:
                f.write("")
                f.flush()
                os.fsync(f.fileno())

            time.sleep(0.5)

            if os.path.exists(final_folder):
                try:
                    shutil.rmtree(final_folder)
                    log_msg(f"[{time.strftime('%H:%M:%S')}]删除旧草稿文件夹\n")
                except:
                    backup_name = final_folder + "_backup_" + time.strftime("%Y%m%d%H%M%S")
                    os.rename(final_folder, backup_name)
                    log_msg(f"[{time.strftime('%H:%M:%S')}]旧草稿已备份为：{os.path.basename(backup_name)}\n")

            os.rename(tmp_folder, final_folder)
            log_msg(f"[{time.strftime('%H:%M:%S')}]重命名临时文件夹为最终草稿ID：{draft_id}\n")

            try:
                future_sec = FUTURE_TIMESTAMP_MICRO / 1_000_000
                os.utime(final_folder, (future_sec, future_sec))
                for fname in ["draft_meta_info.json", "draft_content.json", f"{materials_folder_name}.json"]:
                    fpath = os.path.join(final_folder, fname)
                    if os.path.exists(fpath):
                        os.utime(fpath, (future_sec, future_sec))
            except Exception as e:
                log_msg(f"[{time.strftime('%H:%M:%S')}]修改文件时间失败：{e}\n")

            log_msg(f"[{time.strftime('%H:%M:%S')}]剪映草稿处理完成，保存目录：{final_folder}\n")
            root.after(0, lambda: messagebox.showinfo("成功", "✅ 草稿生成成功！"))

        except Exception as e:
            log_msg(f"[{time.strftime('%H:%M:%S')}]❌ 处理失败：{str(e)}\n")
            log_msg(traceback.format_exc() + "\n")
            root.after(0, lambda: messagebox.showerror("失败", f"处理失败：{str(e)}"))
        finally:
            # 恢复生成按钮
            def enable_btn():
                generate_btn.configure(text="生成剪映草稿", state=tk.NORMAL)
            root.after(0, enable_btn)

    threading.Thread(target=task, daemon=True).start()

# ====================== 自定义圆角按钮类（轻微优化） ======================
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", command=None, width=100, height=40,
                 bg="#3498db", fg="white", font=(DEFAULT_FONT, 11, "bold"), radius=8, text_offset_x=0, text_offset_y=0):
        parent_bg = master.cget("bg") if master else "#ffffff"
        super().__init__(master, width=width, height=height,
                         highlightthickness=0, relief="flat", bd=0, bg=parent_bg)
        self.command = command
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.font = font
        self.text = text
        self.active_bg = "#2980b9"
        self.width = width
        self.height = height
        self.parent_bg = parent_bg
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Configure>", self.on_configure)

        self.config(width=width, height=height, bg=parent_bg)
        self.draw_button(self.bg)

    def draw_button(self, bg_color):
        self.delete("all")
        width = self.width
        height = self.height
        self.create_rounded_rectangle(0, 0, width, height,
                                     radius=self.radius, fill=bg_color)
        self.create_text(width/2 + self.text_offset_x, height/2 + self.text_offset_y,
                        text=self.text, fill=self.fg, font=self.font, anchor=tk.CENTER)

    def on_configure(self, event):
        self.width = event.width
        self.height = event.height
        self.draw_button(self.bg)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=8, **kwargs):
        points = [x1+radius, y1,
                 x2-radius, y1,
                 x2, y1, x2, y1+radius,
                 x2, y2-radius, x2, y2,
                 x2-radius, y2, x1+radius, y2,
                 x1, y2, x1, y2-radius,
                 x1, y1+radius, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.draw_button(self.active_bg)

    def on_leave(self, event):
        self.draw_button(self.bg)

    def configure(self, **kwargs):
        if "text" in kwargs:
            self.text = kwargs.pop("text")
        if "bg" in kwargs:
            self.bg = kwargs.pop("bg")
        if "command" in kwargs:
            self.command = kwargs.pop("command")
        if "state" in kwargs:
            state = kwargs.pop("state")
            # 简单处理：disabled时变灰，不响应点击
            if state == tk.DISABLED:
                self.bind("<Button-1>", lambda e: None)
                self.draw_button("#cccccc")
            else:
                self.bind("<Button-1>", self.on_click)
                self.draw_button(self.bg)
        super().configure(**kwargs)
        self.draw_button(self.bg)

    def lift(self, aboveThis=None):
        if aboveThis is None:
            self.tk.call('raise', self._w)
        else:
            super().lift(aboveThis)

# ====================== 界面 ======================
if __name__ == "__main__":
    # ----- 1. 创建根窗口并先隐藏，避免构建过程被用户看到 -----
    root = tk.Tk()
    root.withdraw()  # 先从屏幕和任务栏中隐藏窗口，后续界面构建完成后再展示
    root.title("剪映小助手")

    # 自定义关闭行为，确保进程彻底退出，不会出现关闭后又弹出一次窗口的情况
    def on_close():
        try:
            root.destroy()
        finally:
            # 双保险，彻底结束当前进程，防止 Tk 事件循环异常导致再次弹窗
            os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)

    # 设置窗口图标（保持不变）
    def set_window_icon(window=None):
        if window is None:
            window = root   # 如果没有指定窗口，就默认设置主窗口
        system = platform.system()

        # ---------- 1. 尝试从外部文件加载（优先） ----------
        possible_paths = [
            os.path.join(os.getcwd(), "app_icon.ico"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico"),
            os.path.join(os.path.expanduser("~"), "Desktop", "app_icon.ico")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    if system == 'Windows':
                        window.iconbitmap(path)
                    else:  # macOS 或其他
                        img = Image.open(path)
                        photo = ImageTk.PhotoImage(img)
                        window.iconphoto(True, photo)
                        window.icon_photo = photo  # 保持引用
                    return
                except:
                    pass

        # ---------- 2. 外部文件不存在或加载失败，从内嵌数据恢复 ----------
        try:
            fd, tmp_path = tempfile.mkstemp(suffix='.ico')
            with os.fdopen(fd, 'wb') as tmp:
                tmp.write(base64.b64decode(EMBEDDED_ICON_BASE64))

            if system == 'Windows':
                window.iconbitmap(tmp_path)
            else:
                img = Image.open(tmp_path)
                photo = ImageTk.PhotoImage(img)
                window.iconphoto(True, photo)
                window.icon_photo = photo

            os.unlink(tmp_path)
        except Exception as e:
            print(f"图标设置失败: {e}")
    set_window_icon()

    # ----- 2. 计算窗口位置和大小 -----
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = min(int(screen_width * 0.8), 1400)
    window_height = min(int(screen_height * 0.8), 800)
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#ffffff")
    root.minsize(800, 600)

    # ----- 4. 构建界面（全部控件在此添加，窗口仍透明）-----
    from tkinter import ttk

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Rounded.TEntry",
                   padding=10,
                   borderwidth=1,
                   relief="solid",
                   bordercolor="#e0e0e0")
    style.configure("Rounded.TFrame",
                   background="#ffffff",
                   relief="solid",
                   borderwidth=3,
                   bordercolor="#cccccc")

    header_frame = tk.Frame(root, bg="#2c3e50", height=60)
    header_frame.pack(fill=tk.X)

    logo_frame = tk.Frame(header_frame, bg="#2c3e50")
    logo_frame.pack(side=tk.LEFT, padx=20, pady=10)
    logo_label = tk.Label(logo_frame, text="宇辰AIGC", font=(DEFAULT_FONT, 16, 'bold'), fg="white", bg="#2c3e50")
    logo_label.pack()

    header_right = tk.Frame(header_frame, bg="#2c3e50")
    header_right.pack(side=tk.RIGHT, padx=20, pady=15)
    set_dir_btn = RoundedButton(header_right, text="设置剪映草稿目录", command=set_draft_root,
                               width=150, height=30, bg="#3498db")
    set_dir_btn.pack(side=tk.RIGHT)

    main_frame = tk.Frame(root, bg="#ffffff")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

    input_frame = tk.Frame(main_frame, bg="#ffffff")
    input_frame.pack(fill=tk.X, pady=(0, 20))
    input_label = tk.Label(input_frame, text="输入草稿ID，示例格式：", font=(DEFAULT_FONT, 12), bg="#ffffff", fg="#333333")
    input_label.pack(anchor=tk.W, pady=(0, 5))

    input_example_frame = tk.Frame(main_frame, bg="#ffffff")
    input_example_frame.pack(fill=tk.X, pady=(0, 10))
    input_example = tk.Label(input_example_frame, text="fde55ea-0ba9-484d-8e6a-1acbbaad15b", font=(DEFAULT_FONT, 11), bg="#ffffff", fg="#666666")
    input_example.pack(side=tk.LEFT, padx=(0, 10))

    input_container = ttk.Frame(main_frame, style="Rounded.TFrame")
    input_container.pack(fill=tk.X, pady=(0, 15))
    entry_id = tk.Text(input_container, height=4, font=(DEFAULT_FONT, 11), bd=0, bg="white", relief=tk.FLAT)
    entry_id.pack(fill=tk.X, padx=15, pady=15)

    def create_context_menu(event):
        context_menu = tk.Menu(entry_id, tearoff=0)
        context_menu.add_command(label="粘贴", command=lambda: entry_id.event_generate('<<Paste>>'))
        context_menu.add_separator()
        context_menu.add_command(label="全选", command=lambda: entry_id.tag_add(tk.SEL, "1.0", tk.END))
        context_menu.tk_popup(event.x_root, event.y_root)
    entry_id.bind("<Button-3>", create_context_menu)

    action_frame = tk.Frame(main_frame, bg="#ffffff")
    action_frame.pack(fill=tk.X, pady=(0, 25))
    generate_btn = RoundedButton(action_frame, text="生成剪映草稿", command=generate,
                                height=40, bg="#3498db")
    generate_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    clear_cache_btn = RoundedButton(action_frame, text="清理缓存", command=clear_cache,
                                   height=40, bg="#3498db")
    clear_cache_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    log_container = ttk.Frame(main_frame, style="Rounded.TFrame")
    log_container.pack(fill=tk.BOTH, expand=True)
    log_header = tk.Frame(log_container, bg="#e7e4f7", height=40)
    log_header.pack(fill=tk.X, padx=15, pady=(15, 0))
    log_title = tk.Label(log_header, text="下载日志记录", font=(DEFAULT_FONT, 11), bg="#f8f9fa", fg="#333333")
    log_title.pack(side=tk.LEFT, padx=10, pady=8)
    clear_log_btn = RoundedButton(log_header, text="清除日志",
                                 command=lambda: [log.delete(1.0, tk.END), log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}]日志已清除\n")],
                                 width=80, height=25, bg="#3498db")
    clear_log_btn.pack(side=tk.RIGHT, padx=10, pady=8)

    log = tk.Text(log_container, font=(DEFAULT_FONT, 11), bd=0, bg="white", relief=tk.FLAT)
    log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    log.tag_configure("blue", foreground="blue")
    log.tag_configure("green", foreground="#1ec64f")

    def download_log():
        try:
            log_content = log.get(1.0, tk.END)
            log_file_path = os.path.join(os.path.expanduser("~"), f"jianying_log_{time.strftime('%Y%m%d_%H%M%S')}.txt")
            with open(log_file_path, "w", encoding="utf-8") as f:
                f.write(log_content)
            messagebox.showinfo("成功", f"日志已下载到：\n{log_file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"下载日志失败：{str(e)}")

    def show_wechat_qr():
        try:
            from PIL import Image, ImageTk
            qr_window = tk.Toplevel(root)
            qr_window.withdraw()
            set_window_icon(qr_window)
            qr_window.title("宇辰AIGC")
            qr_window.resizable(False, False)
            qr_window.configure(bg="#abc8af")

            default_qr = os.path.join(os.getcwd(), "wechat_default.png")
            if os.path.exists(QR_CACHE_PATH):
                qr_path = QR_CACHE_PATH
            else:
                qr_path = default_qr

            if os.path.exists(qr_path):
                img = Image.open(qr_path).resize((250, 250), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                tk.Label(qr_window, image=photo, bg="#ffffff").pack(pady=(50, 30))
                qr_window.photo = photo
            else:
                tk.Label(qr_window,
                         text="请联系客服微信: lengge46",
                         font=(DEFAULT_FONT, 12), bg="#ffffff", fg="#666666").pack(pady=40)

            tk.Label(qr_window, text="扫描上方二维码加入微信交流群",
                     font=(DEFAULT_FONT, 12, "bold"),
                     bg="#ffffff", fg="#333333").pack(pady=(10, 20))

            qr_window.update_idletasks()
            x = root.winfo_x() + (root.winfo_width() // 2) - (350 // 2)
            y = root.winfo_y() + (root.winfo_height() // 2) - (350 // 2)
            qr_window.geometry(f"400x450+{x}+{y}")
            
            qr_window.deiconify()
        
        except ImportError:
            messagebox.showinfo("提示", "请先安装PIL库（pip install Pillow）以支持二维码显示功能")
        except Exception as e:
            messagebox.showerror("错误", f"显示二维码失败：{str(e)}")

    footer_frame = tk.Frame(root, bg="#ffffff", height=30)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    footer_version = tk.Label(footer_frame, text="版本号: 优化版", font=(DEFAULT_FONT, 10), bg="#ffffff", fg="#999999")
    footer_version.pack(anchor=tk.CENTER, pady=5)

    float_btn = RoundedButton(root, text="💬", command=show_wechat_qr,
                            width=50, height=45, bg="#c578db", font=(DEFAULT_FONT, 24, "bold"),
                            text_offset_x=0, text_offset_y=-3)
    float_btn.place(relx=0.96, rely=0.95, anchor=tk.SE)
    float_btn.lift()

    log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}]剪映小助手 已启动\n")

    # ----- 5. 强制完成所有布局和绘制（窗口仍处于隐藏状态）-----
    root.update_idletasks()

    # ----- 6. 现在显示窗口，用户直接看到最终布局状态 -----
    root.deiconify()

    # ----- 7. 启动后台线程（不影响界面）-----
    def start_background():
        threading.Thread(target=update_qr_background, daemon=True).start()
    root.after(100, start_background)

    root.mainloop()