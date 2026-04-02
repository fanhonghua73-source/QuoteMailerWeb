from wxauto4 import WeChat
import time

print('Testing wxauto4...')

try:
    wx = WeChat()
    print('✓ WeChat instance created')
    
    # Get chat info
    info = wx.ChatInfo()
    print(f'✓ ChatInfo: {info}')
    
    # Send a test message
    wx.SendMsg('@所有人 测试消息')
    print('✓ Message sent')
    
    print('All tests passed!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()