#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Shift Manager - パッケージ実行エントリーポイント

このファイルは `python -m ai_shift_manager` で実行される際のエントリーポイントです。

使用方法:
    python -m ai_shift_manager
    
機能:
    - パッケージとしての実行を可能にする
    - main.py の main() 関数を呼び出す
    - エラーハンドリングとログ出力
    - 環境チェックと依存関係確認
"""

import sys
import os
import logging

def main():
    """パッケージ実行時のメインエントリーポイント"""
    try:
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # 起動メッセージ
        logger.info("AI Shift Manager package execution started")
        print("🤖 AI Shift Manager を起動中...")
        
        # 環境チェック
        if sys.version_info < (3, 8):
            error_msg = (
                f"Python 3.8以上が必要です。\n"
                f"現在のバージョン: {sys.version_info.major}.{sys.version_info.minor}\n"
                f"Python 3.8以上をインストールしてください。"
            )
            logger.error(error_msg)
            print(f"❌ エラー: {error_msg}")
            sys.exit(1)
        
        # パッケージのメイン関数をインポートして実行
        try:
            from .main import main as app_main
            logger.info("Main function imported successfully")
            
            # アプリケーションを起動
            app_main()
            
        except ImportError as e:
            logger.error(f"Main function import failed: {e}")
            
            # フォールバック: 直接インポートを試行
            try:
                import ai_shift_manager.main as main_module
                main_module.main()
                
            except ImportError as e2:
                logger.error(f"Fallback import failed: {e2}")
                
                # 最終フォールバック: 基本的なエラーメッセージ
                show_error_dialog(
                    "モジュールインポートエラー",
                    f"AI Shift Managerの起動に失敗しました。\n\n"
                    f"エラー詳細:\n{str(e)}\n\n"
                    f"解決方法:\n"
                    f"1. 依存関係を確認: pip install -r requirements.txt\n"
                    f"2. Pythonバージョン確認: Python 3.8以上\n"
                    f"3. パッケージの整合性確認"
                )
                sys.exit(1)
                
    except KeyboardInterrupt:
        # Ctrl+C による中断
        logger.info("Application interrupted by user")
        print("\n🛑 アプリケーションが中断されました")
        sys.exit(0)
        
    except Exception as e:
        # 予期しないエラー
        logger.error(f"Unexpected error: {e}")
        show_error_dialog(
            "予期しないエラー",
            f"予期しないエラーが発生しました。\n\n"
            f"エラー詳細:\n{str(e)}\n\n"
            f"この問題が継続する場合は、GitHub Issuesで報告してください。"
        )
        sys.exit(1)

def show_error_dialog(title, message):
    """エラーダイアログを表示"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # 隠しルートウィンドウを作成
        root = tk.Tk()
        root.withdraw()
        
        # エラーダイアログを表示
        messagebox.showerror(title, message)
        
        # ルートウィンドウを破棄
        root.destroy()
        
    except ImportError:
        # tkinterが利用できない場合はコンソールに出力
        print(f"\n❌ {title}")
        print(f"{message}")
        
    except Exception:
        # ダイアログ表示に失敗した場合もコンソールに出力
        print(f"\n❌ {title}")
        print(f"{message}")

def check_dependencies():
    """依存関係をチェック"""
    required_modules = [
        'tkinter',
        'pandas',
        'numpy',
        'matplotlib'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = (
            f"以下の必要なモジュールがインストールされていません:\n"
            f"{', '.join(missing_modules)}\n\n"
            f"インストール方法:\n"
            f"pip install -r requirements.txt"
        )
        show_error_dialog("依存関係エラー", error_msg)
        return False
    
    return True

def show_version_info():
    """バージョン情報を表示"""
    try:
        from . import __version__, __author__, __description__
        print(f"🤖 AI Shift Manager v{__version__}")
        print(f"📝 {__description__}")
        print(f"👨‍💻 {__author__}")
        print(f"🐍 Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"💻 Platform: {sys.platform}")
        
    except ImportError:
        print("🤖 AI Shift Manager")
        print("📝 中小企業向け完全オフラインシフト管理システム")

# コマンドライン引数の処理
if __name__ == "__main__":
    # 引数チェック
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--version', '-v']:
            show_version_info()
            sys.exit(0)
            
        elif arg in ['--help', '-h']:
            print("""
🤖 AI Shift Manager - 使用方法

基本的な使用方法:
    python -m ai_shift_manager          # アプリケーションを起動
    
オプション:
    --version, -v                       # バージョン情報を表示
    --help, -h                          # このヘルプを表示
    --check-deps                        # 依存関係をチェック
    
環境変数:
    AI_SHIFT_MANAGER_DEBUG=1           # デバッグモードで起動
    AI_SHIFT_MANAGER_QUIET=1           # 静寂モードで起動
    
詳細情報:
    README.md                           # 基本的な使用方法
    docs/                               # 詳細ドキュメント
    
サポート:
    GitHub: https://github.com/yourusername/ai-shift-manager
    Issues: https://github.com/yourusername/ai-shift-manager/issues
            """)
            sys.exit(0)
            
        elif arg == '--check-deps':
            print("🔍 依存関係をチェック中...")
            if check_dependencies():
                print("✅ すべての依存関係が満たされています")
            sys.exit(0)
            
        else:
            print(f"❌ 不明なオプション: {arg}")
            print("使用方法: python -m ai_shift_manager [--version|--help|--check-deps]")
            sys.exit(1)
    
    # メイン処理を実行
    main()