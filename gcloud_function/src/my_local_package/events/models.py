class EventAction:
    def __init__(self, uid, action, timestamp, timestampo=None):
        self.uid = uid
        self.action = action
        self.timestamp = timestamp
        self.timestampo = timestampo

    def to_dict(self):
        return {"uid": self.uid, "action": self.action, "timestamp": self.timestamp}

    def __str__(self):
        return "{} {} {} {}".format(
            self.uid, self.action, self.timestamp, self.timestampo
        )

    def __repr__(self):
        return self.__str__()
