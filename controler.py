import requests, time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LCUcontroler:
    def __init__(self):

        
        
        self.HANDLERS = {
        "/lol-gameflow/v1/gameflow-phase": self.gameFlowPhase,
        "/lol-gameflow/v1/session": self.gameFlowSesion,
        "/lol-lobby/v2/lobby": self.loby,
        "/lol-matchmaking/v1/ready-check": self.matchmakingReady,
        "/lol-champ-select/v1/session": self.champSelect,
        }

    

    LOBYIDS = {
        "CASUAL":480,
        "NORMALS":400,
        "SOLOQ":420,
        "FLEX":440,
        "5v5":710,
        "ARAM":450,
        "ARAMCAOS":24000,
        "ARENA":1750        
    }

    def getCredentials(self, port, token):
        self.PORT = port
        self.TOKEN =  token
        self.URL = f"https://127.0.0.1:{self.PORT}"
        self.AUTH = ("riot", self.TOKEN)

        print(self.TOKEN, self.PORT)

    def clearCredentials(self):
        self.PORT, self.TOKEN, self.AUTH, self.URL = (None*4)

    def tester(self, payload):
        with open("info.txt", "a", encoding="utf-8") as f:
            f.writelines([str(payload), "\n"])

    def gameFlowPhase(self, payload):
        phase = payload["data"]
        if phase == "ReadyCheck":
            self.acceptMatch()
        
    def gameFlowSesion(self, payload):
        pass

    def champSelect(self, payload):
        localPlayerId = payload["data"].get("localPlayerCellId", None)
        if not localPlayerId:
            return
        acciones = payload["data"]["actions"]
        for l in acciones:
            for accion in l:
                if accion["actorCellId"] == localPlayerId and accion["isInProgress"] == True:
                    if accion["type"] == "pick":
                        self.hoverChamp(accion["id"], 53) #TODO: metodo para conseguir el hover
                    if accion["type"] == "ban":
                        self.hoverChamp(accion["id"], 22) #TODO: lo mismo

    def loby(self, payload):
        summoner_ids = [member["summonerId"] for member in payload["data"].get("members", [])]
        print(summoner_ids) # interfaz luego , revisar nombres, id de iconos

        l = payload["data"]["gameConfig"]["queueId"]
        if l not in self.LOBYIDS.values():
            print(f"id: {l} not in LOBYIDS, inform the developer :D") # interfaz luego

    def matchmakingReady(self, payload):
        totalPenalty = payload["data"]["lowPriorityData"]["penaltyTime"]
        if totalPenalty != 0:
            remainingPenalty = payload ["data"]["lowPriorityData"]["penaltyTimeRemaining"]
            print(f"penalizacion de {totalPenalty}s, tiempo restante:{remainingPenalty}s") # interfaz luego

    def acceptMatch(self):
        requests.post(f'{self.URL}/lol-matchmaking/v1/ready-check/accept', auth=self.AUTH, verify=False)

    def crearSala(self, tipo):
        requests.post(f"{self.URL}/lol-lobby/v2/lobby", json={"queueId":tipo}, auth=self.AUTH, verify=False)

    def startQ(self):
        requests.post(f'{self.URL}/lol-lobby/v2/lobby/matchmaking/search', auth=self.AUTH, verify=False)

    def cancelQ(self):
        requests.delete(f'{self.URL}/lol-lobby/v2/lobby/matchmaking/search', auth=self.AUTH, verify=False)

    def kick(self, summonerId):
        requests.post(f"{self.URL}/lol-lobby/v2/lobby/members/{summonerId}/kick", auth=self.AUTH, verify=False)

    def promote(self, summonerId):
        requests.post(f"{self.URL}/lol-lobby/v2/lobby/members/{summonerId}/promote", auth=self.AUTH, verify=False)
    
    def hoverChamp(self, actionId, champId):
        r = requests.patch(f"{self.URL}/lol-champ-select/v1/session/actions/{actionId}", json={"championId":champId}, auth=self.AUTH, verify=False)
    
    def lockChamp(self, actionId, champId):
        r = requests.post(f"{self.URL}/lol-champ-select/v1/session/actions/{actionId}", json={"championId":champId}, auth=self.AUTH, verify=False)


#testing
xd = LCUcontroler()

#xd.getCredentials("61277","vG7bCYf9XBUZ7TUrqvdFjg")

#xd.crearSala(xd.LOBYIDS["NORMALS"])
#n = input()
#xd.kick(n)
#m = input()
#xd.promote(m)
#print(input())
#xd.hoverChamp()
#xd.pickChamp()

