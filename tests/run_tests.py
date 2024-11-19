import pytest
import sys

def main():
    """Run the test suite."""
    args = [
        "tests",
        "-v",
        "--asyncio-mode=auto",
        "--cov=app",
        "--cov-report=term-missing",
        "-s"
    ]
    
    result = pytest.main(args)
    
    if result == 0:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()