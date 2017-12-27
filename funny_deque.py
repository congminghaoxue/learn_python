# -*- coding: utf-8 -*-
"""
implement a automation with deque and rotate
"""
import sys
import time
from collections import deque

fancy_loading = deque('>--------------------')
write, flush = sys.stdout.write, sys.stdout.flush
while True:
    write('\r%s' % ''.join(fancy_loading))
    fancy_loading.rotate(1)
    flush()
    write('\x08' * len(fancy_loading))
    time.sleep(0.08)
