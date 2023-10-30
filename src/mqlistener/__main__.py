import stomp
import time
from collections import deque

class Listener(stomp.ConnectionListener):
    def on_error(self, frame):
        print(f'ERROR: {frame}')

    def on_message(self, frame):
        print(f'{frame.body}')

def run(host, port, topic):
    with stomp.Connection([(host, port)]) as conn:
        listen = Listener()
        conn.set_listener('printing', listen)
        conn.connect(username="username", passcode="passcode")
        conn.subscribe(destination=topic, id=1, ack='auto')
        print(f'Listening to messages on topic: {topic}')
        try:
            while 1:
                time.sleep(2)
        except KeyboardInterrupt:
            print("Stopped with keyboard")

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Listen to an activemq topic')
    parser.add_argument('-p', '--port', dest='port', type=int, default=61613, help="The port activeMQ is using")
    parser.add_argument('-H', '--host', dest='host', default='localhost', help="The hostname/address of the machine running activeMQ")
    parser.add_argument('topic', metavar='TOPIC')
    args = parser.parse_args()
    run(args.host, args.port, args.topic)

if __name__ == "__main__":
    main()

