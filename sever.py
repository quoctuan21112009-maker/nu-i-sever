import requests
import time
import logging
from datetime import datetime
import os
from typing import Optional

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('keep_alive.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ServerKeeper:
    def __init__(self, url: str, interval: int = 25*60):  # 25 phút mặc định
        self.url = url
        self.interval = interval  # Giây
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def ping_server(self) -> bool:
        """Gửi request đến server và kiểm tra response"""
        try:
            logger.info(f"🔄 Đang ping server: {self.url}")
            response = self.session.get(self.url, timeout=30)
            
            if response.status_code == 200:
                logger.info(f"✅ Server OK! Status: {response.status_code}")
                logger.info(f"📊 Response: {len(response.content)} bytes")
                return True
            else:
                logger.warning(f"⚠️ Server response: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Lỗi kết nối: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Lỗi không xác định: {str(e)}")
            return False

    def run_forever(self):
        """Chạy vô hạn với interval"""
        logger.info("🚀 Bắt đầu Keep-Alive Server...")
        logger.info(f"⏱️  Interval: {self.interval//60} phút")
        
        success_count = 0
        fail_count = 0
        
        while True:
            try:
                if self.ping_server():
                    success_count += 1
                else:
                    fail_count += 1
                
                logger.info(f"📈 Stats - Success: {success_count}, Fail: {fail_count}")
                
                # Sleep trước khi ping lần tiếp theo
                logger.info(f"💤 Nghỉ {self.interval//60} phút...")
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                logger.info("🛑 Dừng bởi người dùng (Ctrl+C)")
                break
            except Exception as e:
                logger.error(f"❌ Lỗi trong main loop: {str(e)}")
                time.sleep(60)  # Nghỉ 1 phút nếu có lỗi

def main():
    # URL server cần nuôi
    SERVER_URL = "https://app-on-luyen-vn.onrender.com"
    
    # Tạo instance và chạy
    keeper = ServerKeeper(
        url=SERVER_URL,
        interval=25*60  # 25 phút (Render free tier sleep sau 15 phút)
    )
    
    keeper.run_forever()

if __name__ == "__main__":
    main()
