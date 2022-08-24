#!/usr/bin/env python3

import aws_cdk as cdk

from habi_backend_test.habi_backend_test_stack import HabiBackendTestStack


app = cdk.App()
local_stack = HabiBackendTestStack(app, "habi-backend-test")

cdk.Tags.of(local_stack).add('client', 'Habi')
cdk.Tags.of(local_stack).add('environment', 'Prod')
cdk.Tags.of(local_stack).add('version', '0.0.1')
cdk.Tags.of(local_stack).add('appName', 'HabiBackend')

app.synth()
