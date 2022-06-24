from pyvesync import VeSync


class C300S:
    def __init__(self, id, password, timezone, index=0):
        self.index = index
        self.manager = VeSync(id, password, timezone, debug=False)

    def get_air_quality(self):
        self.manager.login()
        self.manager.update()
        return self.manager.fans[self.index].details['air_quality_value']


if __name__ == "__main__":
    import os

    id = os.environ['VESYNC_ID']
    password = os.environ['VESYNC_PASSWORD']
    timezone = os.environ['VESYNC_TIMEZONE']

    c300s = C300S(id, password, timezone)
    print(c300s.get_air_quality(), 'ug/㎥')
