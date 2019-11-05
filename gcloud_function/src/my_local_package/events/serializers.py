import datetime
import calendar

from marshmallow import Schema, fields, post_load

from my_local_package.events.models import EventAction


class EventActionSchema(Schema):
    uid = fields.Str(required=True)
    action = fields.Str(required=True)
    timestamp = fields.Int(required=True)
    timestampo = fields.Int(dump_only=True)

    class Meta:
        strict = True
        fields = (
            "uid",
            "action",
            "timestamp",
            "timestampo",
        )

    @post_load
    def make_event_action(self, data, **kwargs):
        utc_now = datetime.datetime.utcnow()
        timestampo = calendar.timegm(utc_now.utctimetuple())
        return EventAction(**data, timestampo=timestampo)
