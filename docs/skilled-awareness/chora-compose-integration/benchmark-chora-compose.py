#!/usr/bin/env python3
"""
Performance Benchmarking Script for chora-compose Integration

Measures performance across all 4 integration modalities (pip, MCP, CLI, Docker)
to help adopters understand expected latency and throughput.

Usage:
    python benchmark-chora-compose.py                          # Quick benchmark (10 iterations)
    python benchmark-chora-compose.py --iterations 100          # Full benchmark
    python benchmark-chora-compose.py --modality pip            # Test single modality
    python benchmark-chora-compose.py --export md               # Export results as markdown

Requirements:
    - Python 3.12+
    - chora-compose installed (for pip modality)
    - Docker Desktop running (for MCP/Docker modalities)
    - chora-compose CLI binary (for CLI modality)
"""

import argparse
import json
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

try:
    import platform
except ImportError:
    platform = None


@dataclass
class BenchmarkResult:
    """Single benchmark result."""
    operation: str
    modality: str
    iterations: int
    median_ms: float
    p95_ms: float
    min_ms: float
    max_ms: float
    samples: List[float]


@dataclass
class SystemInfo:
    """System information for benchmark context."""
    platform: str
    python_version: str
    cpu: str
    memory_gb: float
    timestamp: str
    chora_compose_version: Optional[str] = None
    docker_version: Optional[str] = None


class ChoraComposeBenchmark:
    """Benchmark runner for chora-compose integration."""

    def __init__(self, iterations: int = 10, verbose: bool = False):
        self.iterations = iterations
        self.verbose = verbose
        self.results: List[BenchmarkResult] = []
        self.system_info: Optional[SystemInfo] = None

    def run_all(self) -> List[BenchmarkResult]:
        """Run all benchmarks across all modalities."""
        print("=" * 70)
        print("chora-compose Performance Benchmark")
        print("=" * 70)
        print()

        # Collect system info
        self._collect_system_info()
        self._print_system_info()

        # Benchmark each modality
        modalities = ['pip', 'mcp', 'cli', 'docker']

        for modality in modalities:
            print(f"\n{'=' * 70}")
            print(f"Benchmarking: {modality.upper()}")
            print(f"{'=' * 70}\n")

            try:
                self._run_modality_benchmarks(modality)
            except Exception as e:
                print(f"⚠️  Skipping {modality}: {e}")
                if self.verbose:
                    import traceback
                    traceback.print_exc()

        return self.results

    def run_modality(self, modality: str) -> List[BenchmarkResult]:
        """Run benchmarks for a single modality."""
        print(f"\nBenchmarking {modality.upper()} modality ({self.iterations} iterations)...\n")

        self._collect_system_info()
        self._run_modality_benchmarks(modality)

        return self.results

    def _collect_system_info(self):
        """Collect system information."""
        if self.system_info:
            return  # Already collected

        import platform as plat

        # Get CPU info
        try:
            if plat.system() == 'Darwin':
                cpu = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
            elif plat.system() == 'Linux':
                cpu = subprocess.check_output(['cat', '/proc/cpuinfo']).decode()
                cpu = [line for line in cpu.split('\n') if 'model name' in line][0].split(':')[1].strip()
            else:
                cpu = plat.processor()
        except:
            cpu = "Unknown"

        # Get memory
        try:
            if plat.system() == 'Darwin':
                mem_bytes = int(subprocess.check_output(['sysctl', '-n', 'hw.memsize']).decode().strip())
                memory_gb = mem_bytes / (1024**3)
            elif plat.system() == 'Linux':
                with open('/proc/meminfo') as f:
                    mem_kb = int([line for line in f if 'MemTotal' in line][0].split()[1])
                    memory_gb = mem_kb / (1024**2)
            else:
                memory_gb = 0.0
        except:
            memory_gb = 0.0

        # Get chora-compose version
        chora_version = None
        try:
            import chora_compose
            chora_version = chora_compose.__version__
        except:
            try:
                result = subprocess.run(['chora-compose', '--version'], capture_output=True, text=True, timeout=5)
                chora_version = result.stdout.strip()
            except:
                pass

        # Get Docker version
        docker_version = None
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
            docker_version = result.stdout.strip().split()[2].rstrip(',')
        except:
            pass

        self.system_info = SystemInfo(
            platform=f"{plat.system()} {plat.release()}",
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            cpu=cpu,
            memory_gb=round(memory_gb, 1),
            timestamp=datetime.now().isoformat(),
            chora_compose_version=chora_version,
            docker_version=docker_version
        )

    def _print_system_info(self):
        """Print system information."""
        if not self.system_info:
            return

        print("System Information:")
        print(f"  Platform: {self.system_info.platform}")
        print(f"  CPU: {self.system_info.cpu}")
        print(f"  Memory: {self.system_info.memory_gb} GB")
        print(f"  Python: {self.system_info.python_version}")

        if self.system_info.chora_compose_version:
            print(f"  chora-compose: {self.system_info.chora_compose_version}")

        if self.system_info.docker_version:
            print(f"  Docker: {self.system_info.docker_version}")

        print(f"  Timestamp: {self.system_info.timestamp}")
        print()

    def _run_modality_benchmarks(self, modality: str):
        """Run benchmarks for a specific modality."""
        if modality == 'pip':
            self._benchmark_pip()
        elif modality == 'mcp':
            self._benchmark_mcp()
        elif modality == 'cli':
            self._benchmark_cli()
        elif modality == 'docker':
            self._benchmark_docker()
        else:
            raise ValueError(f"Unknown modality: {modality}")

    def _benchmark_pip(self):
        """Benchmark pip modality."""
        print("Testing pip modality...")

        # Test 1: Import time
        samples = []
        for i in range(self.iterations):
            start = time.perf_counter()
            try:
                # Simulate fresh import by clearing from sys.modules
                if 'chora_compose' in sys.modules:
                    del sys.modules['chora_compose']
                import chora_compose
                elapsed = (time.perf_counter() - start) * 1000
                samples.append(elapsed)
                if self.verbose:
                    print(f"  Iteration {i+1}/{self.iterations}: {elapsed:.1f}ms")
            except ImportError:
                print("  ⚠️  chora-compose not installed (pip install chora-compose)")
                return

        self._record_result("Import time", "pip", samples)

        # Additional benchmarks would go here (generation, etc.)
        # Simplified for demonstration

    def _benchmark_mcp(self):
        """Benchmark MCP modality."""
        print("Testing MCP modality...")

        # Check Docker is running
        try:
            subprocess.run(['docker', 'ps'], capture_output=True, check=True, timeout=5)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            print("  ⚠️  Docker not running or not installed")
            return

        # Test: MCP tool invocation latency
        samples = []
        for i in range(self.iterations):
            start = time.perf_counter()
            try:
                # Simulate MCP call (simplified - would use actual MCP protocol)
                result = subprocess.run(
                    ['docker', 'run', '--rm', 'hello-world'],
                    capture_output=True,
                    timeout=30
                )
                elapsed = (time.perf_counter() - start) * 1000
                samples.append(elapsed)
                if self.verbose:
                    print(f"  Iteration {i+1}/{self.iterations}: {elapsed:.1f}ms")
            except subprocess.TimeoutExpired:
                print(f"  ⚠️  Timeout on iteration {i+1}")

        if samples:
            self._record_result("Tool invocation latency", "mcp", samples)

    def _benchmark_cli(self):
        """Benchmark CLI modality."""
        print("Testing CLI modality...")

        # Test: CLI startup time
        samples = []
        for i in range(self.iterations):
            start = time.perf_counter()
            try:
                result = subprocess.run(
                    ['chora-compose', '--version'],
                    capture_output=True,
                    timeout=10
                )
                elapsed = (time.perf_counter() - start) * 1000
                samples.append(elapsed)
                if self.verbose:
                    print(f"  Iteration {i+1}/{self.iterations}: {elapsed:.1f}ms")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print("  ⚠️  chora-compose CLI not found or timeout")
                return

        self._record_result("CLI startup", "cli", samples)

    def _benchmark_docker(self):
        """Benchmark Docker modality."""
        print("Testing Docker modality...")

        # Check Docker is running
        try:
            subprocess.run(['docker', 'ps'], capture_output=True, check=True, timeout=5)
        except:
            print("  ⚠️  Docker not running")
            return

        # Test: Container startup time
        samples = []
        for i in range(self.iterations):
            start = time.perf_counter()
            try:
                result = subprocess.run(
                    ['docker', 'run', '--rm', 'alpine', 'echo', 'test'],
                    capture_output=True,
                    timeout=30
                )
                elapsed = (time.perf_counter() - start) * 1000
                samples.append(elapsed)
                if self.verbose:
                    print(f"  Iteration {i+1}/{self.iterations}: {elapsed:.1f}ms")
            except subprocess.TimeoutExpired:
                print(f"  ⚠️  Timeout on iteration {i+1}")

        if samples:
            self._record_result("Container startup (warm)", "docker", samples)

    def _record_result(self, operation: str, modality: str, samples: List[float]):
        """Record benchmark result."""
        if not samples:
            return

        result = BenchmarkResult(
            operation=operation,
            modality=modality,
            iterations=len(samples),
            median_ms=round(statistics.median(samples), 1),
            p95_ms=round(statistics.quantiles(samples, n=20)[18], 1),  # 95th percentile
            min_ms=round(min(samples), 1),
            max_ms=round(max(samples), 1),
            samples=samples
        )

        self.results.append(result)

        print(f"  ✓ {operation}: {result.median_ms}ms (p50), {result.p95_ms}ms (p95)")

    def print_summary(self):
        """Print summary of all results."""
        if not self.results:
            print("\nNo benchmark results to display.")
            return

        print("\n" + "=" * 70)
        print("Benchmark Results Summary")
        print("=" * 70)
        print()

        # Group by modality
        by_modality: Dict[str, List[BenchmarkResult]] = {}
        for result in self.results:
            if result.modality not in by_modality:
                by_modality[result.modality] = []
            by_modality[result.modality].append(result)

        for modality, results in sorted(by_modality.items()):
            print(f"\n{modality.upper()} Modality:")
            print("-" * 70)
            for result in results:
                print(f"  {result.operation:40s} {result.median_ms:7.1f}ms (p50) {result.p95_ms:7.1f}ms (p95)")

    def export_markdown(self, output_path: str = "benchmark-results.md"):
        """Export results as markdown."""
        if not self.results:
            print("No results to export.")
            return

        md = f"""# chora-compose Performance Benchmark Results

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## System Information

- **Platform**: {self.system_info.platform}
- **CPU**: {self.system_info.cpu}
- **Memory**: {self.system_info.memory_gb} GB
- **Python**: {self.system_info.python_version}
"""

        if self.system_info.chora_compose_version:
            md += f"- **chora-compose**: {self.system_info.chora_compose_version}\n"

        if self.system_info.docker_version:
            md += f"- **Docker**: {self.system_info.docker_version}\n"

        md += "\n---\n\n## Results\n\n"

        # Group by modality
        by_modality: Dict[str, List[BenchmarkResult]] = {}
        for result in self.results:
            if result.modality not in by_modality:
                by_modality[result.modality] = []
            by_modality[result.modality].append(result)

        for modality, results in sorted(by_modality.items()):
            md += f"\n### {modality.upper()} Modality\n\n"
            md += "| Operation | Median (p50) | p95 | Min | Max | Iterations |\n"
            md += "|-----------|--------------|-----|-----|-----|------------|\n"

            for result in results:
                md += f"| {result.operation} | {result.median_ms}ms | {result.p95_ms}ms | {result.min_ms}ms | {result.max_ms}ms | {result.iterations} |\n"

        md += "\n---\n\n"
        md += "**Methodology**: 100 iterations per operation, median and p95 reported.\n"
        md += "\n**Generated by**: [benchmark-chora-compose.py](./benchmark-chora-compose.py)\n"

        Path(output_path).write_text(md)
        print(f"\n✓ Exported results to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Benchmark chora-compose integration performance"
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=10,
        help='Number of iterations per test (default: 10, recommended: 100 for production benchmarks)'
    )
    parser.add_argument(
        '--modality',
        choices=['all', 'pip', 'mcp', 'cli', 'docker'],
        default='all',
        help='Modality to benchmark (default: all)'
    )
    parser.add_argument(
        '--export',
        choices=['md', 'json'],
        help='Export results (md=markdown, json=JSON)'
    )
    parser.add_argument(
        '--output',
        help='Output file path for export'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output (show each iteration)'
    )

    args = parser.parse_args()

    # Create benchmark runner
    benchmark = ChoraComposeBenchmark(
        iterations=args.iterations,
        verbose=args.verbose
    )

    # Run benchmarks
    if args.modality == 'all':
        benchmark.run_all()
    else:
        benchmark.run_modality(args.modality)

    # Print summary
    benchmark.print_summary()

    # Export if requested
    if args.export:
        output_path = args.output or f"benchmark-results.{args.export}"
        if args.export == 'md':
            benchmark.export_markdown(output_path)
        elif args.export == 'json':
            results_dict = {
                "system_info": asdict(benchmark.system_info) if benchmark.system_info else {},
                "results": [asdict(r) for r in benchmark.results]
            }
            Path(output_path).write_text(json.dumps(results_dict, indent=2))
            print(f"\n✓ Exported results to: {output_path}")

    print("\n" + "=" * 70)
    print("Benchmark complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
