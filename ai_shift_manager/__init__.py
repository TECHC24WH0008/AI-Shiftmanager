#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Shift Manager - 中小企業向け完全オフラインシフト管理システム

完全オフラインで動作する、中小企業向けの高機能シフト管理システム。
AI技術を活用した自動シフト生成、自然言語処理による直感的な操作、
業界別テンプレートによる即座の導入が可能。

主な機能:
- 完全オフライン動作
- AI自動シフト生成
- 自然言語処理エンジン
- 業界別テンプレート
- リアルタイム通知
- 緊急代替システム
- 分析・レポート機能

使用方法:
    # パッケージとして実行
    python -m ai_shift_manager
    
    # プログラムから使用
    from ai_shift_manager import main
    main()
    
    # 個別モジュールの使用
    from ai_shift_manager.core.config import AppConfig
    from ai_shift_manager.ai.nlg_engine import NLGEngine
"""

__version__ = "1.0.0"
__author__ = "AI Shift Manager Team"
__email__ = "contact@example.com"
__license__ = "MIT"
__description__ = "中小企業向け完全オフラインシフト管理システム"
__url__ = "https://github.com/yourusername/ai-shift-manager"

# パッケージレベルのインポート
try:
    from .core.config import AppConfig
    from .core.templates import IndustryTemplates
    from .ai.nlg_engine import NLGEngine
    from .data.data_manager import DataManager
    from .services.shift_service import ShiftService
    from .services.analytics_service import AnalyticsService
    from .main import main
except ImportError as e:
    # インポートエラーが発生した場合の処理
    import warnings
    warnings.warn(f"一部のモジュールのインポートに失敗しました: {e}", ImportWarning)
    
    # 最小限の機能を提供
    def main():
        """フォールバック用のメイン関数"""
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "AI Shift Manager",
            f"AI Shift Manager v{__version__}\n\n"
            "一部のモジュールが利用できません。\n"
            "依存関係を確認してください:\n\n"
            "pip install -r requirements.txt"
        )
        root.destroy()

# パブリックAPI
__all__ = [
    # メイン関数
    "main",
    
    # コアクラス
    "AppConfig",
    "IndustryTemplates", 
    "NLGEngine",
    "DataManager",
    "ShiftService",
    "AnalyticsService",
    
    # メタデータ
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    "__url__",
]

# パッケージ初期化時の設定
import sys
import os
import logging

# パッケージのルートディレクトリを取得
PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

# 最小Python要件チェック
if sys.version_info < (3, 8):
    raise RuntimeError(
        f"AI Shift Manager requires Python 3.8 or higher. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )

# 必要なディレクトリの作成
def ensure_directories():
    """必要なディレクトリが存在することを確認"""
    dirs = [
        os.path.join(PACKAGE_ROOT, "logs"),
        os.path.join(PACKAGE_ROOT, "exports"),
        os.path.join(PACKAGE_ROOT, "backups"),
    ]
    
    for dir_path in dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError:
            # ディレクトリ作成に失敗した場合は警告のみ
            pass

# パッケージ初期化
try:
    ensure_directories()
except Exception:
    # 初期化エラーは無視（権限不足等）
    pass

# ログ設定（オプション）
def setup_logging(level=logging.INFO):
    """ログ設定を行う"""
    try:
        log_file = os.path.join(PACKAGE_ROOT, "logs", "ai_shift_manager.log")
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger(__name__)
        logger.info(f"AI Shift Manager v{__version__} initialized")
        
    except Exception:
        # ログ設定に失敗した場合は基本設定のみ
        logging.basicConfig(level=level)

# 環境変数による設定
if os.getenv('AI_SHIFT_MANAGER_DEBUG'):
    setup_logging(logging.DEBUG)
elif os.getenv('AI_SHIFT_MANAGER_QUIET'):
    setup_logging(logging.WARNING)
else:
    setup_logging(logging.INFO)

# パッケージ情報の表示（デバッグモード時）
if os.getenv('AI_SHIFT_MANAGER_DEBUG'):
    print(f"🤖 AI Shift Manager v{__version__}")
    print(f"📁 Package root: {PACKAGE_ROOT}")
    print(f"🐍 Python version: {sys.version}")
    print(f"💻 Platform: {sys.platform}")