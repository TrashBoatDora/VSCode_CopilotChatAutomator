# -*- coding: utf-8 -*-
"""
Hybrid UI Automation Script - 圖像辨識模組
處理截圖、圖像匹配、等待回應完成的視覺判斷
"""

import pyautogui
import cv2
import numpy as np
import time
from pathlib import Path
from typing import Optional, Tuple, List
import sys

# 導入配置和日誌
sys.path.append(str(Path(__file__).parent.parent))
from config.config import config
from src.logger import get_logger

class ImageRecognition:
    """圖像辨識處理器"""
    
    def __init__(self):
        """初始化圖像辨識器"""
        self.logger = get_logger("ImageRecognition")
        self.screenshot_count = 0
        self.logger.info("圖像辨識模組初始化完成")
    
    def take_screenshot(self, region: Tuple[int, int, int, int] = None, 
                       save_path: str = None) -> Optional[np.ndarray]:
        """
        截取螢幕畫面
        
        Args:
            region: 截圖區域 (left, top, width, height)，None 表示全螢幕
            save_path: 儲存截圖的路徑（可選）
            
        Returns:
            Optional[np.ndarray]: 截圖的 numpy 陣列，失敗則返回 None
        """
        try:
            self.screenshot_count += 1
            
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # 轉換為 OpenCV 格式
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # 如果指定了儲存路徑，儲存截圖
            if save_path:
                cv2.imwrite(save_path, screenshot_cv)
                self.logger.debug(f"截圖已儲存: {save_path}")
            
            self.logger.debug(f"截圖完成 #{self.screenshot_count}")
            return screenshot_cv
            
        except Exception as e:
            self.logger.error(f"截圖失敗: {str(e)}")
            return None
    
    def find_image_on_screen(self, template_path: str, confidence: float = None,
                           region: Tuple[int, int, int, int] = None) -> Optional[Tuple[int, int, int, int]]:
        """
        在螢幕上尋找指定圖像
        
        Args:
            template_path: 模板圖像路徑
            confidence: 匹配信心度閾值
            region: 搜尋區域
            
        Returns:
            Optional[Tuple[int, int, int, int]]: 找到的位置 (left, top, width, height)，失敗則返回 None
        """
        try:
            template_path = Path(template_path)
            if not template_path.exists():
                self.logger.error(f"模板圖像不存在: {template_path}")
                return None
            
            if confidence is None:
                confidence = config.IMAGE_CONFIDENCE
            
            # 使用 pyautogui 的圖像識別功能
            try:
                location = pyautogui.locateOnScreen(
                    str(template_path),
                    confidence=confidence,
                    region=region
                )
                
                if location:
                    self.logger.image_recognition(template_path.name, True, confidence)
                    return location
                else:
                    self.logger.image_recognition(template_path.name, False)
                    return None
                    
            except pyautogui.ImageNotFoundException:
                self.logger.image_recognition(template_path.name, False)
                return None
                
        except Exception as e:
            self.logger.error(f"圖像識別過程中發生錯誤: {str(e)}")
            return None
    
    def wait_for_image(self, template_path: str, timeout: int = 30,
                      check_interval: float = 1.0, confidence: float = None,
                      region: Tuple[int, int, int, int] = None) -> bool:
        """
        等待指定圖像出現
        
        Args:
            template_path: 模板圖像路徑
            timeout: 超時時間（秒）
            check_interval: 檢查間隔（秒）
            confidence: 匹配信心度
            region: 搜尋區域
            
        Returns:
            bool: 是否找到圖像
        """
        try:
            template_name = Path(template_path).name
            self.logger.info(f"等待圖像出現: {template_name} (超時: {timeout}秒)")
            
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                location = self.find_image_on_screen(template_path, confidence, region)
                
                if location:
                    elapsed = time.time() - start_time
                    self.logger.info(f"✅ 圖像 {template_name} 已出現 (耗時: {elapsed:.1f}秒)")
                    return True
                
                time.sleep(check_interval)
                
                # 每10秒記錄一次等待狀態
                elapsed = time.time() - start_time
                if int(elapsed) % 10 == 0 and int(elapsed) > 0:
                    self.logger.debug(f"等待圖像 {template_name}... ({elapsed:.0f}秒)")
            
            self.logger.warning(f"⏰ 等待圖像 {template_name} 超時")
            return False
            
        except Exception as e:
            self.logger.error(f"等待圖像時發生錯誤: {str(e)}")
            return False
    
    def click_on_image(self, template_path: str, confidence: float = None,
                      region: Tuple[int, int, int, int] = None, offset: Tuple[int, int] = None) -> bool:
        """
        在找到的圖像上點擊
        
        Args:
            template_path: 模板圖像路徑
            confidence: 匹配信心度
            region: 搜尋區域
            offset: 點擊位置偏移 (x, y)
            
        Returns:
            bool: 點擊是否成功
        """
        try:
            location = self.find_image_on_screen(template_path, confidence, region)
            
            if location:
                # 計算點擊位置（圖像中心）
                click_x = location.left + location.width // 2
                click_y = location.top + location.height // 2
                
                # 應用偏移
                if offset:
                    click_x += offset[0]
                    click_y += offset[1]
                
                # 執行點擊
                pyautogui.click(click_x, click_y)
                
                template_name = Path(template_path).name
                self.logger.info(f"✅ 點擊圖像 {template_name} 於位置 ({click_x}, {click_y})")
                return True
            else:
                template_name = Path(template_path).name
                self.logger.warning(f"⚠️ 無法找到圖像 {template_name}，點擊失敗")
                return False
                
        except Exception as e:
            self.logger.error(f"點擊圖像時發生錯誤: {str(e)}")
            return False
    
    def check_copilot_response_ready(self) -> bool:
        """
        檢查 Copilot 回應是否準備就緒
        
        Returns:
            bool: 回應是否準備就緒
        """
        try:
            # 檢查重新生成按鈕是否出現
            regenerate_button = self.find_image_on_screen(
                str(config.REGENERATE_BUTTON_IMAGE),
                confidence=config.IMAGE_CONFIDENCE
            )
            
            if regenerate_button:
                self.logger.debug("檢測到重新生成按鈕，回應可能已完成")
                return True
            
            # 可以添加其他檢查邏輯
            # 例如檢查是否有複製按鈕、輸入框狀態等
            
            return False
            
        except Exception as e:
            self.logger.debug(f"檢查 Copilot 回應狀態時發生錯誤: {str(e)}")
            return False
    
    def click_copilot_copy_button(self) -> bool:
        """
        點擊 Copilot 的複製按鈕
        
        Returns:
            bool: 點擊是否成功
        """
        try:
            return self.click_on_image(
                str(config.COPY_BUTTON_IMAGE),
                confidence=config.IMAGE_CONFIDENCE
            )
            
        except Exception as e:
            self.logger.error(f"點擊 Copilot 複製按鈕時發生錯誤: {str(e)}")
            return False
    
    def validate_required_images(self) -> bool:
        """
        驗證所需的圖像資源是否可用（現已變為可選）
        
        Returns:
            bool: 所有必需圖像是否都存在且可讀取
        """
        try:
            # 如果不要求圖像識別，直接通過
            if not config.IMAGE_RECOGNITION_REQUIRED:
                self.logger.info("圖像識別已設為可選，跳過圖像檔案檢查")
                return True
            
            required_images = [
                config.REGENERATE_BUTTON_IMAGE,
                config.COPY_BUTTON_IMAGE,
                config.COPILOT_INPUT_BOX_IMAGE
            ]
            
            missing_images = []
            invalid_images = []
            
            for image_path in required_images:
                if not image_path.exists():
                    missing_images.append(str(image_path))
                else:
                    # 嘗試讀取圖像驗證其有效性
                    try:
                        img = cv2.imread(str(image_path))
                        if img is None:
                            invalid_images.append(str(image_path))
                    except Exception:
                        invalid_images.append(str(image_path))
            
            if missing_images:
                self.logger.warning("缺少圖像資源（已設為可選）:")
                for img in missing_images:
                    self.logger.warning(f"  - {img}")
            
            if invalid_images:
                self.logger.warning("無效的圖像資源（已設為可選）:")
                for img in invalid_images:
                    self.logger.warning(f"  - {img}")
            
            # 即使有缺失圖像也不會失敗，因為現在是可選的
            if missing_images or invalid_images:
                self.logger.info("圖像識別功能不可用，將使用鍵盤操作替代方案")
                return True
            
            self.logger.info("✅ 所有必需的圖像資源驗證通過")
            return True
            
        except Exception as e:
            self.logger.error(f"驗證圖像資源時發生錯誤: {str(e)}")
            return False
    
    def create_template_screenshots(self) -> bool:
        """
        協助用戶創建模板截圖的指導函數
        
        Returns:
            bool: 是否成功提供指導
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("圖像模板創建指南")
            self.logger.info("=" * 60)
            
            templates_needed = [
                ("regenerate_button.png", "Copilot Chat 中的'重新生成'按鈕"),
                ("copy_button.png", "Copilot Chat 中的'複製'按鈕"),
                ("copilot_input.png", "Copilot Chat 的輸入框區域")
            ]
            
            self.logger.info("需要創建以下模板圖像:")
            for filename, description in templates_needed:
                self.logger.info(f"  - {filename}: {description}")
            
            self.logger.info("")
            self.logger.info("創建步驟:")
            self.logger.info("1. 打開 VS Code 並開啟 Copilot Chat")
            self.logger.info("2. 使用截圖工具（如 Snipping Tool）")
            self.logger.info("3. 精確截取上述 UI 元素的小範圍圖像")
            self.logger.info("4. 將圖像儲存到 assets/ 目錄下")
            self.logger.info("5. 確保圖像清晰且背景一致")
            
            self.logger.info("")
            self.logger.info(f"儲存路徑: {config.ASSETS_DIR}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"提供創建指南時發生錯誤: {str(e)}")
            return False

# 創建全域實例
image_recognition = ImageRecognition()

# 便捷函數
def find_image(template_path: str, confidence: float = None) -> Optional[Tuple[int, int, int, int]]:
    """尋找圖像的便捷函數"""
    return image_recognition.find_image_on_screen(template_path, confidence)

def wait_for_image(template_path: str, timeout: int = 30) -> bool:
    """等待圖像出現的便捷函數"""
    return image_recognition.wait_for_image(template_path, timeout)

def click_image(template_path: str, confidence: float = None) -> bool:
    """點擊圖像的便捷函數"""
    return image_recognition.click_on_image(template_path, confidence)

def check_copilot_ready() -> bool:
    """檢查 Copilot 準備狀態的便捷函數"""
    return image_recognition.check_copilot_response_ready()

def validate_image_assets() -> bool:
    """驗證圖像資源的便捷函數"""
    return image_recognition.validate_required_images()