"""
Test script to verify the installation and basic functionality.
This script tests:
1. SpaCy model loading
2. Basic entity extraction
3. File I/O operations
"""

import spacy
from pathlib import Path


def test_spacy_model():
    """Test if SpaCy Chinese model is installed."""
    print("Testing SpaCy Chinese model...")
    try:
        nlp = spacy.load("zh_core_web_sm")
        doc = nlp("北京是中国的首都。")
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        print(f"✓ SpaCy model loaded successfully")
        print(f"  Test entities: {entities}")
        return True
    except OSError:
        print("✗ SpaCy model 'zh_core_web_sm' not found!")
        print("  Please run: python -m spacy download zh_core_web_sm")
        return False


def test_dependencies():
    """Test if all required Python packages are installed."""
    print("\nTesting Python dependencies...")
    missing = []
    
    try:
        import spacy
        print("✓ spacy")
    except ImportError:
        missing.append("spacy")
        print("✗ spacy")
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv")
    except ImportError:
        missing.append("python-dotenv")
        print("✗ python-dotenv")
    
    try:
        import requests
        print("✓ requests")
    except ImportError:
        missing.append("requests")
        print("✗ requests")
    
    if missing:
        print(f"\nMissing packages: {missing}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def test_files():
    """Test if required input files exist."""
    print("\nChecking input files...")
    required_files = ["data.txt", "question.txt"]
    missing = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} not found")
            missing.append(file)
    
    if missing:
        print(f"\nMissing files: {missing}")
        return False
    
    return True


def test_env_config():
    """Test if environment configuration exists."""
    print("\nChecking environment configuration...")
    env_file = Path(".env")
    
    if env_file.exists():
        content = env_file.read_text(encoding="utf-8")
        if "DEEPSEEK_API_KEY" in content:
            print("✓ .env file exists with DEEPSEEK_API_KEY")
            if "your_api_key_here" in content:
                print("⚠ Warning: API key not configured yet")
            return True
        else:
            print("✗ DEEPSEEK_API_KEY not found in .env")
            return False
    else:
        print("✗ .env file not found")
        print("  Creating from template...")
        example = Path(".env.example")
        if example.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✓ Created .env from .env.example")
            print("  Please edit .env and add your API key")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("SpaCy Knowledge Graph System - Installation Test")
    print("="*60)
    
    results = []
    
    # Test 1: Dependencies
    results.append(("Dependencies", test_dependencies()))
    
    # Test 2: SpaCy Model
    results.append(("SpaCy Model", test_spacy_model()))
    
    # Test 3: Files
    results.append(("Input Files", test_files()))
    
    # Test 4: Environment
    results.append(("Environment Config", test_env_config()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Configure your DEEPSEEK_API_KEY in .env")
        print("2. Prepare data.txt and question.txt")
        print("3. Run: python main.py")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
