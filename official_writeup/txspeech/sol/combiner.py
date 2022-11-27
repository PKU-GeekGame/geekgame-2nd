import io
import struct
from pathlib import Path

def crc32_forward(msg): # NOT the same as binascci.crc32
    crc = 0
    for b in msg:
        crc ^= b << 24
        for _ in range(8):
            crc = (crc << 1) ^ 0x04c11db7 if crc & 0x80000000 else crc << 1
    return crc & 0xffffffff

class OpusChunk:
    def __init__(self, chunk: bytes, last_position: int):
        chunk_io = io.BytesIO(chunk)
        assert chunk_io.read(4)==b'OggS'
        assert chunk_io.read(1)==b'\x00'
        self.header_type = struct.unpack('B', chunk_io.read(1))[0]
        self.position_delta = struct.unpack('<Q', chunk_io.read(8))[0] - last_position
        assert self.position_delta>=0
        self.stream = struct.unpack('<I', chunk_io.read(4))[0]
        self._seq = struct.unpack('<I', chunk_io.read(4))[0]
        self._checksum = struct.unpack('<I', chunk_io.read(4))[0]
        self.n_segs = struct.unpack('B', chunk_io.read(1))[0]
        self.segs_len = [
            struct.unpack('B', chunk_io.read(1))[0]
            for _ in range(self.n_segs)
        ]
        self.segs_data = [
            chunk_io.read(self.segs_len[i])
            for i in range(self.n_segs)
        ]
        self.remaining = chunk_io.read()

    def _save(self, last_position: int, seq: int, checksum: int) -> bytes:
        f = io.BytesIO()
        f.write(b'OggS\x00')
        f.write(struct.pack('<BQII', self.header_type, self.position_delta + last_position, self.stream, seq))
        f.write(struct.pack('<I', checksum)) # checksum
        f.write(struct.pack('B', self.n_segs))
        for seg_len in self.segs_len:
            f.write(struct.pack('B', seg_len))
        for seg_data in self.segs_data:
            f.write(seg_data)
        return f.getvalue()

    def save(self, last_position: int, seq: int) -> bytes:
        data = self._save(last_position, seq, 0)
        checksum = crc32_forward(data)
        return self._save(last_position, seq, checksum)

class OpusFile:
    def __init__(self, stream: int):
        self.chunks = []
        self.stream = stream

    @classmethod
    def load(cls, path: Path):
        with path.open('rb') as f:
            data = f.read()

        first_chunk = OpusChunk(data, 0)
        self = cls(first_chunk.stream)
        self.chunks = [first_chunk]
        cur_position = first_chunk.position_delta

        while self.chunks[-1].remaining:
            new_chunk = OpusChunk(self.chunks[-1].remaining, cur_position)
            cur_position += new_chunk.position_delta
            self.chunks[-1].remaining = b''
            self.chunks.append(new_chunk)

        return self

    def save(self) -> bytes:
        last_position = 0
        ret = b''
        for seq, chunk in enumerate(self.chunks):
            chunk.header_type = 2 if seq==0 else 4 if seq==len(self.chunks)-1 else 0
            chunk.stream = self.stream
            chk = chunk.save(last_position, seq)
            print('Chunk:', len(chk))
            ret += chk
            last_position += chunk.position_delta
        return ret

files = {p.name: OpusFile.load(p) for p in Path('.').glob('*.wav.ogg')}

header = files['part1.wav.ogg'].chunks[0]

tag_chunk: OpusChunk = files['part1.wav.ogg'].chunks[1]
tag_chunk.segs_data[0] = b'OpusTags\x00\x00\x00\x00\x00\x00\x00\x00'
tag_chunk.segs_len[0] = len(tag_chunk.segs_data[0])

combined_1 = OpusFile(114514)
combined_1.chunks = [
    header,
    tag_chunk,
    *files['part1.wav.ogg'].chunks[2:],
    *files['silence_9630.wav.ogg'].chunks[2:],
    *files['part2.wav.ogg'].chunks[2:],
    *files['silence_9630.wav.ogg'].chunks[2:],
    *files['part3.wav.ogg'].chunks[2:],
    *files['silence_9630.wav.ogg'].chunks[2:],
    *files['part4.wav.ogg'].chunks[2:],
    *files['silence_9630.wav.ogg'].chunks[2:],
    #*files['part5.wav.ogg'].chunks[2:],
]
combined_2 = OpusFile(1919810)
combined_2.chunks = [
    header,
    tag_chunk,
    *files['part5.wav.ogg'].chunks[2:],
]

tot_len = 0
with Path('combined.ogg_').open('wb') as f:
    tot_len += f.write(combined_1.save())
    tot_len += f.write(combined_2.save())
print(tot_len)