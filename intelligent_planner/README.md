# Intelligent Browser Automation - Example Usage

This directory contains the intelligent browser automation system that uses LLM exploration to determine if tasks are repeatable and generates scripts accordingly.

## Quick Start

```python
import asyncio
from intelligent_planner import IntelligentBrowserAutomation

async def main():
    # Initialize
    automation = IntelligentBrowserAutomation()
    
    # Execute task
    result = await automation.execute(
        url="https://example.com",
        task="Your task description"
    )
    
    print(f"Success: {result.success}")
    print(f"Method: {result.method}")  # SCRIPT or BROWSER_USE
    print(f"Result: {result.result}")

asyncio.run(main())
```

## Components

- **llm_explorer.py** - Uses LLM to explore tasks
- **repeatability_analyzer.py** - Determines if task is repeatable
- **script_generator.py** - Generates Python scripts
- **browser_use_executor.py** - Executes with browser-use
- **orchestrator.py** - Main coordination logic
- **models.py** - Data models

## How It Works

1. **First Run**: LLM explores → analyzes → generates script (if repeatable)
2. **Subsequent Runs**: Uses saved script (10x faster, 90% cheaper)
3. **Fallback**: If script fails, automatically uses browser-use

## See Also

- `../examples/` - Example scripts
- `../README.md` - Full documentation
