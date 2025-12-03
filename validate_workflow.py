#!/usr/bin/env python3
"""Validate GitHub Actions workflow files."""

import yaml
import sys
from pathlib import Path

def validate_workflow(workflow_path):
    """Validate a GitHub Actions workflow file."""
    print(f"Validating {workflow_path}...")
    
    try:
        with open(workflow_path, 'r') as f:
            # Use FullLoader to handle 'on' keyword properly
            workflow = yaml.load(f, Loader=yaml.FullLoader)
        
        # Check required fields
        required_fields = ['name', 'jobs']
        for field in required_fields:
            if field not in workflow:
                print(f"  ❌ Missing required field: {field}")
                return False
        
        # Check 'on' field - PyYAML converts it to True (boolean)
        if True not in workflow and 'on' not in workflow:
            print(f"  ❌ Missing required field: on")
            return False
        
        print(f"  ✓ Has required fields: name, on, jobs")
        
        # Check jobs
        if not workflow['jobs']:
            print("  ❌ No jobs defined")
            return False
        
        print(f"  ✓ Found {len(workflow['jobs'])} job(s): {', '.join(workflow['jobs'].keys())}")
        
        # Check each job has steps
        for job_name, job_config in workflow['jobs'].items():
            if 'steps' not in job_config:
                print(f"  ❌ Job '{job_name}' has no steps")
                return False
            print(f"  ✓ Job '{job_name}' has {len(job_config['steps'])} steps")
            
            # Check for deprecated actions
            for i, step in enumerate(job_config['steps'], 1):
                if 'uses' in step:
                    action = step['uses']
                    if '@v3' in action and 'artifact' in action:
                        print(f"  ⚠️  Step {i} uses deprecated action: {action}")
                    elif '@v3' in action and 'cache' in action:
                        print(f"  ⚠️  Step {i} uses deprecated cache@v3: {action}")
        
        print(f"✅ {workflow_path} is valid!\n")
        return True
        
    except yaml.YAMLError as e:
        print(f"  ❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

if __name__ == '__main__':
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("❌ No .github/workflows directory found")
        sys.exit(1)
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("❌ No workflow files found")
        sys.exit(1)
    
    all_valid = True
    for workflow_file in workflow_files:
        if not validate_workflow(workflow_file):
            all_valid = False
    
    if all_valid:
        print("🎉 All workflows are valid!")
        sys.exit(0)
    else:
        print("❌ Some workflows have issues")
        sys.exit(1)
