import textwrap
import pytest


ANDROID_24H_CHAT = textwrap.dedent("""\
    12/01/23, 09:00 - Alice: Hello there
    12/01/23, 09:01 - Bob: Hi! How are you?
    12/01/23, 09:02 - Alice: Good, thanks - what about you?
    12/01/23, 09:03 - Bob: Great!
""")

ANDROID_12H_CHAT = textwrap.dedent("""\
    12/01/23, 9:00 am - Alice: Hello there
    12/01/23, 9:01 am - Bob: Hi! How are you?
    12/01/23, 9:02 am - Alice: Good, thanks
    12/01/23, 9:03 am - Bob: Great!
""")

IOS_CHAT = textwrap.dedent("""\
    [12/01/2023, 09:00:00] Alice: Hello there
    [12/01/2023, 09:01:00] Bob: Hi! How are you?
    [12/01/2023, 09:02:00] Alice: Good, thanks
    [12/01/2023, 09:03:00] Bob: Great!
""")

MULTILINE_CHAT = textwrap.dedent("""\
    12/01/23, 09:00 - Alice: Hello there
    this is a continuation
    12/01/23, 09:01 - Bob: Got it
""")

GARBAGE_CHAT = textwrap.dedent("""\
    this is not a chat export
    no timestamps here
    just random text
""")
