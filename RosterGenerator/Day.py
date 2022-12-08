from NSF import NSF



class days:
    def __init__(self, date: int, day: str):

        self.date = date
        self.day = day

        self.AMDC = []
        self.AMreserve = []

        self.PMDC = []
        self.PMreserve = []

        self.available = []
        self.PMavailable = []

        self.AMreserveList = []
        self.PMreserveList = []
        
        self.exclusion = []

