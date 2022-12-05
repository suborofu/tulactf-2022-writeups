import sha256
import base64


def convert_to_hs(h):
    return [int.from_bytes(h[i * 4:i * 4 + 4], 'big') for i in range(8)]


def le_attack_sha256(sign: bytes, key_len: int, m: bytes, a: bytes):
    message = bytearray(b'X' * key_len + m)
    length = len(message) * 8
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)
    message += length.to_bytes(8, 'big')

    m1 = message

    message = bytearray(a)
    length = len(message) * 8
    message += length.to_bytes(8, 'big')

    broken_length = len(m1) * 8 + length
    broken_h = convert_to_hs(sign)
    m2 = m1[key_len:] + a

    s = sha256.generate_hash(a, False, broken_h, broken_length)
    return m2, s


def main():
    sign = b'cHJpbnQoIkhFTExPIFdPUkxEISIsIDErMiszKzQrNSk=&5684f9a13cb97ffc48662cca6d669475a1b7ede3af6fb842387f6e3395320cbc'
    m, h = sign.split(b'&')[-2:]
    m = base64.b64decode(m)
    h = int(h.decode('ASCII'), 16).to_bytes(32, 'big')
    print(m, h)
    m1, h1 = le_attack_sha256(h, 32, m, b'print(flag)')
    sign1 = base64.b64encode(m1) + b'&' + hex(int.from_bytes(h1, 'big')).encode('ascii')[2:]
    print(sign1.decode('ascii'))
    # print(server.check_sigh(sign1))


if __name__ == '__main__':
    main()
