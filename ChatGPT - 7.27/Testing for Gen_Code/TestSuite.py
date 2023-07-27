import unittest
from unittest import TestLoader
import TestCases
import time
from tracemalloc_utils import get_traced_memory
class TimedTestRunner:
    def run_tests(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCases.CombinedTests)
        times = []
        for test in suite:
            start = time.perf_counter()
            test.run()
            end = time.perf_counter()
            times.append({"name": test.id(), "time": end - start})
        return times


class TestRunner(object):

    def mem_run(self):
        # Load tests
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCases)
        unittest.TextTestRunner().run(suite)

        # Print memory for all tests
        print(f"Total memory used: {get_traced_memory() / 1024} KiB")


if __name__ == "__main__":
    runner = TimedTestRunner()
    times = runner.run_tests()
    tot_time = 0
    for result in times:
        print(f"{result['name']} took {result['time']:.4f} secs")
        tot_time += result["time"]
    print(tot_time)

    loader = TestLoader()
    suite = loader.loadTestsFromTestCase(TestCases.CombinedTests)
    runner = unittest.TextTestRunner()
    runner.run(suite)

    print(f"Total Memory Usage: {get_traced_memory()/1024} KiB")