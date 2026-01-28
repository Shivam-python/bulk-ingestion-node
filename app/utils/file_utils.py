MAX_UPLOAD_SIZE = 1024 * 100  # 50 KB (more than enough for 20 rows)


class FileTooLargeError(Exception):
    pass


async def read_limited_file(upload_file, max_size: int = MAX_UPLOAD_SIZE) -> str:
    size = 0
    chunks = []

    while chunk := await upload_file.read(1024):  # read 1KB at a time
        size += len(chunk)
        if size > max_size:
            raise FileTooLargeError("Uploaded file exceeds allowed size limit")

        chunks.append(chunk)

    return b"".join(chunks).decode("utf-8")
