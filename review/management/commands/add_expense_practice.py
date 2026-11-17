from django.core.management.base import BaseCommand
from django.db import transaction

from review.models import Exercise


class Command(BaseCommand):
    help = "교통비 문제에 연결된 추가 연습 두 개를 등록합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        originals = Exercise.objects.select_for_update().filter(
            title="교통비만 골라 합계 내기", lesson__topic__code="1.3.2",
            lesson__topic__section="Python",
        ).order_by("pk")
        added = 0
        for original in originals:
            for count in (False, True):
                entries = [("교통", 1300), ("식비", 7400), ("간식", 2200), ("식비", 5900)]
                title = "식비를 쓴 횟수 세기" if count else "식비만 골라 합계 내기"
                value = "1" if count else "amount"
                expected = sum(1 if count else amount for category, amount in entries if category == "식비")
                _, created = Exercise.objects.get_or_create(
                    lesson=original.lesson,
                    title=title,
                    guidance__practice_for=original.pk,
                    defaults={
                        "description": "식비에 해당하는 건수를 세고 숫자만 출력하세요." if count else "식비에 해당하는 금액을 더하고 숫자만 출력하세요.",
                        "starter_code": f"expenses = {entries!r}\n",
                        "expected_output": str(expected),
                        "order": 5 if count else 4,
                        "guidance": {
                            "practice_for": original.pk,
                            "prompt": "조건에 맞을 때마다 건수는 1, 합계는 이번 금액을 더해요.",
                            "before": "total = total + ",
                            "after": "",
                            "answer": value,
                            "steps": [
                                ["total = 0", "합계 또는 건수를 0으로 시작해요."],
                                ["for category, amount in expenses:", "지출 분류와 금액을 하나씩 꺼내요."],
                                ['    if category == "식비":', "식비인 경우만 아래 줄을 실행해요."],
                                [f"        total = total + {value}", "한 건이므로 1을 더해요." if count else "이번 식비 금액을 더해요."],
                                ["print(total)", "반복이 끝난 뒤 결과를 한 번 출력해요."],
                            ],
                        },
                    },
                )
                added += created
        self.stdout.write(f"추가 연습 {added}개 등록")
