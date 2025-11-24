"""
Example: Using Intelligent Browser Automation

This example shows how to use the intelligent browser automation system
"""

import asyncio
from intelligent_planner import IntelligentBrowserAutomation


async def example_repeatable_task():
    """Example of a repeatable task that will generate a script"""
    
    print("=" * 70)
    print("EXAMPLE 1: Repeatable Task (HackerNews Top Post)")
    print("=" * 70)
    
    automation = IntelligentBrowserAutomation()
    
    result = await automation.execute(
        url="https://news.ycombinator.com",
        task="Find the title of the top post on HackerNews"
    )
    
    print(f"\n✅ Success: {result.success}")
    print(f"📊 Method Used: {result.method}")
    print(f"📝 Result: {result.result}")
    
    if result.method == "SCRIPT":
        print(f"💾 Script saved to: {result.script_path}")
        print("\n💡 Next time you run this task, it will use the saved script!")


async def example_non_repeatable_task():
    """Example of a non-repeatable task that will use browser-use"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Non-Repeatable Task (Research)")
    print("=" * 70)
    
    automation = IntelligentBrowserAutomation()
    
    result = await automation.execute(
        url="https://news.ycombinator.com",
        task="Find and summarize the top 3 AI-related posts"
    )
    
    print(f"\n✅ Success: {result.success}")
    print(f"📊 Method Used: {result.method}")
    print(f"📝 Result: {result.result}")


async def example_rerun_task():
    """Example of re-running a task (should use saved script)"""
    
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Re-run Task (Should Use Saved Script)")
    print("=" * 70)
    
    automation = IntelligentBrowserAutomation()
    
    result = await automation.execute(
        url="https://news.ycombinator.com",
        task="Find the title of the top post on HackerNews"
    )
    
    print(f"\n✅ Success: {result.success}")
    print(f"📊 Method Used: {result.method}")
    
    if result.method == "SCRIPT":
        print("⚡ Used saved script - 10x faster!")
    
    print(f"📝 Result: {result.result}")


async def main():
    """Run all examples"""
    
    # Example 1: Repeatable task (will generate script)
    await example_repeatable_task()
    
    # Example 2: Non-repeatable task (will use browser-use)
    await example_non_repeatable_task()
    
    # Example 3: Re-run task (will use saved script)
    await example_rerun_task()
    
    print("\n" + "=" * 70)
    print("✨ All examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
