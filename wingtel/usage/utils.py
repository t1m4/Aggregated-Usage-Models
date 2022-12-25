import os

from django.conf import settings


def get_object_or_none(klass, *args, **kwargs):
    try:
        return klass.objects.get(*args, **kwargs)
    except klass.DoesNotExist:
        return None


def read_file_to_string(file_path_from_django_base_dir: str) -> str:
    with open(os.path.join(settings.BASE_DIR, file_path_from_django_base_dir), "r") as f:
        return f.read()
