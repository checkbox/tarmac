TESTFLAGS=
test:
	trial $(TESTFLAGS) tarmaclib

test-fail:
	trial this-will-fail

.PHONY: test test-fail
