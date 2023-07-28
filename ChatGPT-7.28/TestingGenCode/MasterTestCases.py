import unittest
from unittest import TestLoader
from TestingGenCode import TestCases
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

def get_total_time():
    runner = TimedTestRunner()
    times = runner.run_tests()
    total_time = 0
    for result in times:
        # print(f"{result['name']} took {result['time']:.4f} secs")
        total_time += result["time"]
    return total_time


def get_total_memory():
    loader = TestLoader()
    suite = loader.loadTestsFromTestCase(TestCases.CombinedTests)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    return get_traced_memory() / 1024

def tests_success():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases.CombinedTests)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    report = {'total': result.testsRun, 'passed': len(result.successes), 'failed': len(result.failures),
              'skipped': len(result.skipped), 'errors': len(result.errors), 'failure_details': []}
    for failure in result.failures:
        report['failure_details'].append({
            'test': failure[0],
            'exception': failure[1],
        })
    return report


#
# if __name__ == "__main__":
#     total_time = get_total_time()
#     print(total_time)
#
#     total_memory = get_total_memory()
#     print(f"Total Memory Usage: {total_memory} KiB")


# if __name__ == "__main__":
#     runner = TimedTestRunner()
#     times = runner.run_tests()
#     tot_time = 0
#     for result in times:
#         print(f"{result['name']} took {result['time']:.4f} secs")
#         tot_time += result["time"]
#     print(tot_time)
#
#     loader = TestLoader()
#     suite = loader.loadTestsFromTestCase(TestCases.CombinedTests)
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
#
#     print(f"Total Memory Usage: {get_traced_memory()/1024} KiB")