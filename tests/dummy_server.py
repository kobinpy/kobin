import sys
import os
import socket

test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)

sys.path.append(os.path.dirname(test_root))
sys.path.append(test_root)

try:
    server = sys.argv[1]
    port = int(sys.argv[2])

    from kobin import Kobin
    app = Kobin()
    app.config.update({
        'PORT': port,
        'SERVER': server
    })

    @app.route('^/test$')
    def pong():
        return 'OK'

    app.run()

except socket.error:  # Port in use
    sys.exit(3)
except ImportError:
    sys.exit(128)
except KeyboardInterrupt:
    pass
