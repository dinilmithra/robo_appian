#!/usr/bin/env python3
"""Simple workflow validator."""

import yaml
from pathlib import Path

workflows_dir = Path('.github/workflows')
workflow_files = list(workflows_dir.glob('*.yml'))

print("Validating workflows...\n")

for wf in workflow_files:
    print(f"📄 {wf.name}")
    try:
        with open(wf) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        
        print(f"  ✓ Valid YAML")
        print(f"  ✓ Name: {data.get('name', 'N/A')}")
        
        # Check for 'on' trigger (PyYAML converts to True)
        has_trigger = True in data or 'on' in data
        print(f"  {'✓' if has_trigger else '❌'} Triggers defined: {has_trigger}")
        
        jobs = data.get('jobs', {})
        print(f"  ✓ Jobs: {len(jobs)} ({', '.join(jobs.keys())})")
        
        # Check for deprecated actions
        deprecated = []
        for job_name, job in jobs.items():
            for step in job.get('steps', []):
                if 'uses' in step:
                    action = step['uses']
                    if 'artifact@v3' in action or 'cache@v3' in action:
                        deprecated.append(action)
        
        if deprecated:
            print(f"  ⚠️  Deprecated actions: {', '.join(set(deprecated))}")
        else:
            print(f"  ✓ No deprecated actions")
        
        print()
        
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

print("✅ Validation complete!")
