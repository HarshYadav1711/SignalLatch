from django.utils import timezone

from flags.models import Flag


def mark_flag_irrelevant(flag: Flag) -> Flag:
    flag.status = Flag.Status.IRRELEVANT
    flag.reviewed_at = timezone.now()
    flag.reviewed_content_last_updated = flag.content_item.last_updated
    flag.save(update_fields=["status", "reviewed_at", "reviewed_content_last_updated"])
    return flag
