#!/usr/bin/env python3
"""
CareerViet Job Application Automation - Enhanced Version
Features:
- Task loaded from external file
- Multiple API keys with automatic retry
- Headless mode for GitHub Actions
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure we don't import the local browser_use folder
# Remove current directory from path to force using installed package
if '' in sys.path:
    sys.path.remove('')
if '.' in sys.path:
    sys.path.remove('.')

from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI
from pydantic import Field, ConfigDict, SecretStr

class GeminiOpenAI(ChatOpenAI):
    """Custom wrapper for Gemini via OpenAI compatibility layer"""
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    provider: str = Field(default="openai")

    def __init__(self, api_key: str):
        super().__init__(
            model="gemini-2.0-flash-exp",
            api_key=SecretStr(api_key),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            temperature=0.0,
        )

def get_gemini_llm(api_key: str):
    """Get Gemini Flash using OpenAI compatibility layer"""
    return GeminiOpenAI(api_key=api_key) 

def load_task_from_file(task_file: str = "tasks/careerviet_task.txt") -> str:
    """Load task from external file"""
    task_path = Path(__file__).parent / task_file
    
    if not task_path.exists():
        raise FileNotFoundError(f"Task file not found: {task_path}")
    
    with open(task_path, 'r', encoding='utf-8') as f:
        task = f.read().strip()
    
    print(f"✅ Task loaded from: {task_path}")
    return task


def load_api_keys(keys_file: str = "tasks/api_keys.txt") -> list[str]:
    """Load multiple Gemini API keys from file or environment"""
    keys_path = Path(__file__).parent / keys_file
    api_keys = []
    
    # First, check for API_KEYS environment variable (supports multiple keys)
    api_keys_env = os.getenv("API_KEYS")
    if api_keys_env:
        # Split by newline or comma
        for key in api_keys_env.replace(',', '\n').split('\n'):
            key = key.strip()
            if key and not key.startswith('#'):
                api_keys.append(key)
        print(f"✅ Loaded {len(api_keys)} key(s) from API_KEYS environment variable")
    
    # Try to load from file
    if keys_path.exists():
        with open(keys_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Extract key value
                    if '=' in line:
                        key = line.split('=', 1)[1].strip()
                        if key and key != 'your-primary-key-here' and key != 'your-backup-key-here' and key != 'your-third-key-here':
                            if key not in api_keys:
                                api_keys.append(key)
    
    # Also check individual environment variables
    for i in range(1, 10):  # Check up to 10 keys
        env_key = os.getenv(f"GOOGLE_API_KEY_{i}")
        if env_key and env_key not in api_keys:
            api_keys.append(env_key)
    
    # Fallback to single GOOGLE_API_KEY
    single_key = os.getenv("GOOGLE_API_KEY")
    if single_key and single_key not in api_keys:
        api_keys.insert(0, single_key)
    
    if not api_keys:
        raise ValueError(
            "No API keys found! Please either:\n"
            "1. Set GOOGLE_API_KEY environment variable, or\n"
            "2. Add keys to tasks/api_keys.txt, or\n"
            "3. Set GOOGLE_API_KEY_1, GOOGLE_API_KEY_2, etc."
        )
    
    print(f"✅ Loaded {len(api_keys)} API key(s)")
    return api_keys


async def run_with_retry(task: str, api_keys: list[str], headless: bool = True) -> tuple[bool, str]:
    """Run automation with API key retry logic"""
    
    for i, api_key in enumerate(api_keys, 1):
        try:
            print(f"\n{'=' * 70}")
            print(f"🔑 Attempting with API key #{i}/{len(api_keys)}")
            print(f"{'=' * 70}")
            
            # Initialize browser
            # Note: use_cloud=True requires BROWSER_USE_API_KEY
            # For now, using local browser (works best when run locally, not in GitHub Actions)
            browser = Browser(
                headless=headless,
                disable_security=False,
            )
            
            # Initialize Gemini Flash via OpenAI compatibility
            llm = get_gemini_llm(api_key=api_key)
            
            # Create agent
            agent = Agent(
                task=task,
                llm=llm,
                browser=browser,
                use_vision=True,
                max_actions_per_step=10
            )
            
            # Execute
            print("🚀 Starting automation...")
            history = await agent.run(max_steps=150)
            
            # Success!
            print(f"\n✅ Success with API key #{i}!")
            return True, str(history.final_result())
            
        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ API key #{i} failed: {error_msg}")
            
            # If this was the last key, raise the error
            if i == len(api_keys):
                print(f"\n⚠️  All {len(api_keys)} API keys failed!")
                raise
            
            # Otherwise, try next key
            print(f"🔄 Retrying with next API key...")
            await asyncio.sleep(2)  # Brief delay before retry
    
    return False, "All API keys failed"


async def main():
    print("=" * 70)
    print("🎯 CareerViet Auto Apply - Enhanced Version")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    try:
        # Load task from file
        task = load_task_from_file()
        
        # Load API keys
        api_keys = load_api_keys()
        
        # Determine if headless
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        if headless:
            print("🖥️  Mode: HEADLESS (GitHub Actions)")
        else:
            print("🖥️  Mode: VISIBLE (Local)")
        
        print()
        
        # Run with retry
        success, result = await run_with_retry(task, api_keys, headless)
        
        # Save results
        os.makedirs('results', exist_ok=True)
        result_file = f"results/careerviet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(f"CareerViet Auto Apply Results\n")
            f.write(f"{'=' * 70}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Success: {success}\n")
            f.write(f"\nResult:\n{result}\n")
        
        print(f"\n💾 Results saved to: {result_file}")
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error
        os.makedirs('results', exist_ok=True)
        error_file = f"results/error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f"Error: {str(e)}\n\n")
            f.write(traceback.format_exc())
        
        print(f"\n💾 Error saved to: {error_file}")
        sys.exit(1)
    
    finally:
        print("\n" + "=" * 70)
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
