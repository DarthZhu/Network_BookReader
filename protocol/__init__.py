import enum
from utils import get_config

config = get_config()

class MessageType(enum.IntEnum):
    """Link message type with integers
    """
    init = 0
    # Server Action
    login_success = 1
    send_list = 2
    send_page = 3
    send_chapter = 4
    send_book = 5
    send_book_done = 6
    page_num = 7
    total_page = 8
    chap_list = 9

    # Client Action
    login = 101
    download = 102
    read = 103
    require_page = 104
    require_list = 105
    update_bookmark = 106
    disconnect = 107

    # Failure
    login_fail = 201

class packet:
    def __init__(self, mt=MessageType.init, data=""):
        self.mt = mt
        self.data = data
        return
    
    def to_message(self):
        """Turn packet into a string
        """
        msg = str(self.mt.value)
        msg = '0' * (3 - len(msg)) + msg
        msg += str(self.data)
        return msg.encode(config["packet"]["format"])
    
    def to_packet(self, msg):
        """Turn message into packet
        """
        msg = msg.decode(config["packet"]["format"])
        self.mt = MessageType(int(msg[:3]))
        self.data = msg[3:]
        return self
    
    def to_message_no_encode(self):
        """Turn packet into a string without encode
        """
        msg = str(self.mt.value)
        msg = '0' * (3 - len(msg)) + msg
        msg = msg.encode(config["packet"]["format"])
        msg += self.data
        return msg

    def to_packet_no_decode(self, msg):
        """Turn message into packet
        """
        self.mt = MessageType(int(msg[:3].decode(config["packet"]["format"])))
        self.data = msg[3:]
        return self