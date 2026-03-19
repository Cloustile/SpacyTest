"""
DeepSeek API Test Script
测试 DeepSeek API 连接

使用方法:
    python test.py

前提条件:
    pip install openai python-dotenv
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Check if openai is installed
try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: 'openai' library not installed!")
    print("   Please install it first: pip install openai")
    exit(1)


def main():
    """Test DeepSeek API connection."""
    print("="*60)
    print("DeepSeek API Test")
    print("="*60)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    # Validate API key
    if not api_key:
        print("\n❌ ERROR: DEEPSEEK_API_KEY not found")
        print("-"*60)
        print("Please configure your API key:")
        print("  1. Open .env file")
        print("  2. Replace 'your_api_key_here' with your actual API key")
        print("  3. Get your API key from: https://platform.deepseek.com/")
        return
    
    if api_key == "your_api_key_here":
        print("\n❌ ERROR: API key not configured")
        print("-"*60)
        print("Please edit .env file and add your actual API key")
        print("Get your API key from: https://platform.deepseek.com/")
        return
    
    print(f"\n✓ API key loaded: {api_key[:20]}...")
    
    # Initialize client
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        print("✓ OpenAI client initialized")
        print("-"*60)
        print("Sending test request to DeepSeek API...")
        
        # Send test request
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "你好！请用中文回答：API 测试成功了吗？"},
            ],
            stream=False,
            timeout=30
        )
        
        answer = response.choices[0].message.content
        
        print("\n✅ SUCCESS!")
        print("-"*60)
        print(f"Response: {answer}")
        print("-"*60)
        print("\n✓ Your API key is valid and working!")
        print("✓ Account balance is sufficient")
        
    except Exception as e:
        error_msg = str(e)
        
        print("\n❌ ERROR")
        print("-"*60)
        
        # Parse error type
        if "402" in error_msg or "Payment Required" in error_msg:
            print("Error Code: 402 Payment Required")
            print("-"*60)
            print("原因：账户余额不足或免费额度已用完")
            print("\n解决方案:")
            print("  1. 访问：https://platform.deepseek.com/")
            print("  2. 登录你的账户")
            print("  3. 进入'账户管理'或'充值'页面")
            print("  4. 进行充值")
            
        elif "401" in error_msg or "Authentication" in error_msg:
            print("Error Code: 401 Authentication Failed")
            print("-"*60)
            print("原因：API Key 无效")
            print("\n解决方案:")
            print("  1. 检查 .env 文件中的 API Key 是否正确")
            print("  2. 访问 https://platform.deepseek.com/ 获取新的 API Key")
            
        elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            print("Error: Request Timeout")
            print("-"*60)
            print("原因：请求超时（30 秒）")
            print("\n解决方案:")
            print("  1. 检查网络连接")
            print("  2. 检查是否需要科学上网")
            print("  3. 稍后重试")
            
        else:
            print(f"Error: {error_msg}")
        
        print("\n⚠️  API test failed")
        print("  Please fix the issues above and try again")


if __name__ == "__main__":
    main()
