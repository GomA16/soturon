from typing import Self
class shareResource:
    def __init__(self):
        self.sharedPIN = []
        self.ballots = []
        self.revocationList = []

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
    
    def addBallot(self, ballot: list)->Self:
        self.ballots.append(ballot)
        return self

sharedResource = shareResource()