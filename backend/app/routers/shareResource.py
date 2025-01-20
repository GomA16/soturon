from typing import Self

class Ballot:
    def __init__(self, candidate, pin, pk):
        self.candidate = candidate
        self.pk =pk
        self.pin = pin

    def __str__(self):
        return f"ballot: {self.candidate}, {self.pin}, {self.pk}"

class shareResource:
    def __init__(self):
        self.sharedPIN = []
        self.ballots:list[Ballot] = []
        self.revocationList:list[Ballot] = []
        self.mixedBallots:list[Ballot] = []

    def addPIN(self, pinDict: dict)-> Self:
        self.sharedPIN.append(pinDict)
        return self
    
    def updatePIN(self, pk: str, newPIN: str) -> Self:
        for i in range(len(self.sharedPIN)):
            if self.sharedPIN[i]["pk"] == pk :
                self.sharedPIN[i]["PIN"] = newPIN
        return self
    
    def updatePINList(self, pk:str, PIN:str) -> Self:
        for i in range(len(self.sharedPIN)):
            if self.sharedPIN[i]["pk"] == pk :
                self.sharedPIN[i]["PIN"] = PIN
                return self
        newElm = {"pk":pk, "PIN":PIN}
        self.addPIN(newElm)
        return self
    
    def getPINList(self) -> None:
        print(self.sharedPIN)
    
    def addRevocationList(self, element:list) -> Self:
        self.revocationList.append(element)
        return self
    
    def showRevocationList(self) -> None:
        for item in self.revocationList:
            print("revocated", item)
    
    def addBallot(self, ballot: list)->Self:
        self.ballots.append(Ballot(ballot[0], ballot[1], ballot[2]))
        return self
    
    def showBallots(self) -> None:
        for item in self.ballots:
            print(item)
        return None
    
    def setMixedBallots(self, mixedBallots:list[Ballot]) -> Self:
        self.mixedBallots = mixedBallots
        return self 

sharedResource = shareResource()