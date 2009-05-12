TESTFLAGS=
test:
	trial $(TESTFLAGS) tarmac

test-fail:
	trial this-will-fail

.PHONY: test test-fail
