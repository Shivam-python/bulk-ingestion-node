from app.core.custom_exceptions import FileTooLargeError

MAX_UPLOAD_SIZE = 1024 * 100  # 50 KB (more than enough for 20 rows)


async def read_limited_file(upload_file, max_size: int = MAX_UPLOAD_SIZE) -> str:
    size = 0
    chunks = []

    while chunk := await upload_file.read(1024):  # read 1KB at a time
        size += len(chunk)
        if size > max_size:
            raise FileTooLargeError()

        chunks.append(chunk)

    return b"".join(chunks).decode("utf-8")
