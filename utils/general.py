def convert_userid(userid: bytes) -> int:
    return int.from_bytes(userid, byteorder='little', signed=False)