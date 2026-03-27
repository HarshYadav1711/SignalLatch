from django.utils import timezone

from flags.models import Flag


def mark_flag_irrelevant(flag: Flag) -> Flag:
    flag.status = Flag.Status.IRRELEVANT
    flag.reviewed_at = timezone.now()
    flag.reviewed_content_last_updated = flag.content_item.last_updated
    flag.save(update_fields=["status", "reviewed_at", "reviewed_content_last_updated"])
    return flag


def update_flag_status(flag: Flag, status: str) -> Flag:
    if status == Flag.Status.IRRELEVANT:
        return mark_flag_irrelevant(flag)

    flag.status = status
    flag.reviewed_at = None
    flag.reviewed_content_last_updated = None
    flag.save(update_fields=["status", "reviewed_at", "reviewed_content_last_updated"])
    return flag
