#!/usr/bin/env python
"""Django 관리 명령을 실행하는 진입 파일입니다."""
import os
import sys


def main():
    # 프로젝트 설정 파일의 위치를 Django에 알려줍니다.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 불러올 수 없습니다. 가상환경과 설치 상태를 확인하세요."
        ) from exc

    # check, makemigrations, migrate, runserver 등의 명령을 실행합니다.
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()