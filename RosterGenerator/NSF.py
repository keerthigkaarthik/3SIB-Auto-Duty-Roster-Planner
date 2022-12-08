class NSF:
    
    all = []
    night = []
    morning = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        self.name = name
        self.exclusionDays = []
        self.NightDuty = NightDuty
        self.points = points
        self.NoOfWkeds = NoOfWkeds

        self.shifts_this_month = 0
        self.AMdates_served = []
        self.PMdates_served = []
        self.fulldates_served = []
        self.reservedates = []
        self.extras_served = []

        self.points_earned_this_month = 0
        self.NoOfWkeds_done_this_month = 0

        self.points_from_last_month = points
        self.NoOfWkeds_from_last_month = NoOfWkeds

        NSF.all.append(self)
        if NightDuty == True:
            NSF.night.append(self)
        elif NightDuty == False:
            NSF.morning.append(self)


class S1(NSF):
    all = []
    night = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        super().__init__(name, NightDuty, points=points, NoOfWkeds=NoOfWkeds)
        S1.all.append(self)
        if NightDuty == True:
            S1.night.append(self)


class S2(NSF):
    all = []
    night = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        super().__init__(name, NightDuty, points=points, NoOfWkeds=NoOfWkeds)
        S2.all.append(self)
        if NightDuty == True:
            S2.night.append(self)


class S3(NSF):
    all = []
    night = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        super().__init__(name, NightDuty, points=points, NoOfWkeds=NoOfWkeds)
        S3.all.append(self)
        if NightDuty == True:
            S3.night.append(self)


class S4(NSF):
    all = []
    night = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        super().__init__(name, NightDuty, points=points, NoOfWkeds=NoOfWkeds)
        S4.all.append(self)
        if NightDuty == True:
            S4.night.append(self)


class HQCOY(NSF):
    all = []
    night = []
    def __init__(self, name: str, NightDuty: bool, points: float, NoOfWkeds:float):
        super().__init__(name, NightDuty, points=points, NoOfWkeds=NoOfWkeds)
        HQCOY.all.append(self)
        if NightDuty == True:
            HQCOY.night.append(self)    