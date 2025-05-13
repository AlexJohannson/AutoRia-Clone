from uuid import uuid1


def upload_listing_photo(instance, filename: str) -> str:
    ext = filename.split('.')[-1]
    return f'listings/{instance.id or "temp"}/{uuid1()}.{ext}'

