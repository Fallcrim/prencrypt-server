class Message:
    OPCODES = {
        0x00: "UKN",  # docs: unknown
        0x11: "REG",  # docs: register
        0x12: "GET",  # docs: get
        0x13: "TRF",  # docs: transfer
        0xFF: "ERR",  # docs: error
    }

    OPCODE_OFFSET = 0
    USERID_OFFSET = 1
    SIGNATURE_OFFSET = 4
    DATA_OFFSET = 261

    def __init__(self, opcode: str, userid: int, signature: bytes, data: bytes) -> None:
        self.opcode = opcode
        self.userid = userid
        self.signature = signature
        self.data = data

    def to_bytes(self) -> bytes:
        """
        Returns a bytes representation of the message
        :return:
        """
        return f"{self.opcode}{self.userid}{self.signature}{self.data}".encode()

    @staticmethod
    def parse_message(message: bytes):
        """
        Parses a bytes representation of the message and returns a Message object.
        :param message:
        :return:
        """
        opcode_b = message[Message.OPCODE_OFFSET]
        userid_b = message[Message.USERID_OFFSET:Message.USERID_OFFSET + 4]  # userid length = 4
        signature_b = message[Message.SIGNATURE_OFFSET:Message.SIGNATURE_OFFSET + 256]  # signature length = 256
        data = message[Message.DATA_OFFSET:]
        return Message(hex(opcode_b), int(userid_b), signature_b, data)
