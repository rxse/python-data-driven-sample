import unittest
import argparse
import sys
import os
import xmlrunner


def create_test_suite_from_specs(loader, specs):
    if "**" in specs:
        # folder execution
        testsuite = loader.discover(specs[:specs.find("**")], "*.py")
    else:
        # single file execution
        mod_name = os.path.relpath(specs).replace(os.path.sep,
                                                  ".").replace(".py", "")
        testsuite = loader.loadTestsFromNames([mod_name])

    return testsuite


def create_test_suite_from_grep(loader, grep):
    mod_name = os.path.relpath(grep).replace(os.path.sep,
                                             ".").replace(".py", "")
    testsuite = loader.loadTestsFromName(mod_name)

    return testsuite


def main():
    parser = argparse.ArgumentParser(
        description='Ranorex Webtestit Python scaffold')
    parser.add_argument("--specs", type=str)
    parser.add_argument("--grep", type=str)
    args = parser.parse_args()
    loader = unittest.TestLoader()

    if hasattr(args, "specs") and args.specs is not None:
        testsuite = create_test_suite_from_specs(loader, args.specs)
    elif hasattr(args, "grep") and args.grep is not None:
        testsuite = create_test_suite_from_grep(loader, args.grep)
    else:
        # discover looks by default for files named in the pattern test_*
        testsuite = loader.discover("./tests", "*.py")

    if not os.path.exists("temp-reports"):
        os.mkdir("temp-reports")

    # JUnit reports generated in test-reports folder
    with open(
            os.path.join("temp-reports/",
                         os.environ.get("TEST_REPORT_FILENAME")),
            "wb") as output:
        result = xmlrunner.XMLTestRunner(output=output).run(testsuite)
        result.shouldStop = False
        sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
