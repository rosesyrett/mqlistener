import logging
import os
import time

import stomp

LOGGER = logging.getLogger("mqlistener")

class Listener(stomp.ConnectionListener):
    def on_error(self, frame):
        LOGGER.info(f'ERROR: {frame}')

    def on_message(self, frame):
        LOGGER.info(f'{frame.body}')

def run(host, port, topic, username, password):
    if (not username) or (not password) or (not topic):
        message = "USERNAME, PASSWORD or TOPIC environment variables must be set."
        LOGGER.error("LISTENER: ERROR: " + message)
        raise Exception(message)
    with stomp.Connection([(host, port)]) as conn:
        LOGGER.info(f"LISTENER: CONNECTING: host {host} port {port}")

        listen = Listener()
        conn.set_listener('printing', listen)
        conn.connect(username=username, passcode=password)
        conn.subscribe(destination=topic, id=1, ack='auto')

        LOGGER.info(f"LISTENER: DESTINATION: set to {topic}")

        try:
            while 1:
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopped with keyboard")

def main():
    host = os.getenv("HOST", "localhost")
    port = os.environ.get("PORT", "61613")
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    topic = os.environ.get("TOPIC")
    run(host, port, topic, username, password)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

