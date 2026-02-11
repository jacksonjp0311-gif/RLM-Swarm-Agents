#!/usr/bin/env python3
"""
Multi-Repository Watch Mode for RLM-Swarm-Agents
Scans directory for repos and analyzes each

Usage:
  python watch_repos.py ~/code
  python watch_repos.py ~/code --apply --max-iter 20
  python watch_repos.py ~/code --output report.json
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def find_repos(root: Path) -> List[Path]:
    """Find all git repositories in directory"""
    repos = []
    
    for item in root.iterdir():
        if not item.is_dir():
            continue
        
        # Skip hidden, build, and cache directories
        if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', 'build']:
            continue
        
        # Check if it's a git repo
        if (item / '.git').exists():
            repos.append(item)
    
    return sorted(repos)


def analyze_repo(repo: Path, swarm_script: Path, apply: bool, max_iter: int) -> Dict:
    """Run analysis on single repo"""
    print(f"\n{'='*60}")
    print(f"Repository: {repo.name}")
    print(f"{'='*60}")
    
    cmd = [
        'python', str(swarm_script),
        str(repo),
        '--max-iter', str(max_iter)
    ]
    
    if apply:
        cmd.append('--apply')
    
    result = {
        'repo': str(repo),
        'name': repo.name,
        'timestamp': datetime.now().isoformat(),
        'success': False
    }
    
    try:
        # Run swarm analysis
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 min timeout
        )
        
        result['success'] = proc.returncode == 0
        result['output'] = proc.stdout
        result['error'] = proc.stderr if proc.stderr else None
        
        # Parse fixpoint_analysis.json if exists
        analysis_path = repo / 'runs'
        if analysis_path.exists():
            runs = sorted(analysis_path.glob('run_*'))
            if runs:
                latest = runs[-1] / 'fixpoint_analysis.json'
                if latest.exists():
                    result['analysis'] = json.loads(latest.read_text())
        
        print(f"✓ Complete: {repo.name}")
        
    except subprocess.TimeoutExpired:
        result['error'] = 'Timeout (5 min)'
        print(f"✗ Timeout: {repo.name}")
    except Exception as e:
        result['error'] = str(e)
        print(f"✗ Error: {repo.name} - {e}")
    
    return result


def generate_report(results: List[Dict]) -> Dict:
    """Generate consolidated report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_repos': len(results),
        'successful': sum(1 for r in results if r['success']),
        'failed': sum(1 for r in results if not r['success']),
        'repos': []
    }
    
    for r in results:
        repo_summary = {
            'name': r['name'],
            'path': r['repo'],
            'success': r['success']
        }
        
        if 'analysis' in r:
            repo_summary['iterations'] = r['analysis'].get('iterations', 0)
            repo_summary['converged'] = r['analysis'].get('iterations', 0) < 50
            repo_summary['final_state'] = r['analysis'].get('final_state', '')[:16]
        
        if r.get('error'):
            repo_summary['error'] = r['error']
        
        report['repos'].append(repo_summary)
    
    return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Multi-repository watch mode for RLM-Swarm-Agents'
    )
    parser.add_argument('directory', help='Directory containing repos')
    parser.add_argument('--apply', action='store_true', help='Apply transformations')
    parser.add_argument('--max-iter', type=int, default=20, help='Max iterations per repo')
    parser.add_argument('--output', help='Output report path (JSON)')
    parser.add_argument('--swarm', help='Path to run_swarm.py', 
                       default=Path(__file__).parent.parent / 'run_swarm.py')
    
    args = parser.parse_args()
    
    root = Path(args.directory).resolve()
    swarm_script = Path(args.swarm).resolve()
    
    if not root.exists():
        print(f"Error: Directory not found: {root}")
        return 1
    
    if not swarm_script.exists():
        print(f"Error: run_swarm.py not found: {swarm_script}")
        return 1
    
    # Find repositories
    repos = find_repos(root)
    
    if not repos:
        print(f"No repositories found in {root}")
        return 1
    
    print(f"Found {len(repos)} repositories")
    print(f"Mode: {'APPLY' if args.apply else 'ANALYZE'}")
    print(f"Max iterations: {args.max_iter}\n")
    
    # Analyze each repo
    results = []
    for repo in repos:
        result = analyze_repo(repo, swarm_script, args.apply, args.max_iter)
        results.append(result)
    
    # Generate report
    report = generate_report(results)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total repositories: {report['total_repos']}")
    print(f"Successful: {report['successful']}")
    print(f"Failed: {report['failed']}")
    
    # Show converged repos
    converged = [r for r in report['repos'] if r.get('converged')]
    if converged:
        print(f"\nConverged repos ({len(converged)}):")
        for r in converged:
            print(f"  ✓ {r['name']} ({r.get('iterations', 0)} iterations)")
    
    # Show failed repos
    failed = [r for r in report['repos'] if not r['success']]
    if failed:
        print(f"\nFailed repos ({len(failed)}):")
        for r in failed:
            error = r.get('error', 'Unknown')
            print(f"  ✗ {r['name']}: {error}")
    
    # Save report
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved: {output_path}")
    
    return 0 if report['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
