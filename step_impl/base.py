from getgauge.python import step
from time import sleep

@step("wait for <15> seconds")
def wait_for_seconds(seconds):
    sleep(int(seconds))

@step("Reference <test_id>")
def reference(test_id):
    # This can be used to implement references to a test management DB
    pass