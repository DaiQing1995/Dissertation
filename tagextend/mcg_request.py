import requests
import json
import time

class MCGUtils:

    def getBLCScore(self, element, topK):
        for i in range(1000):
            request = "https://concept.research.microsoft.com/api/Concept/ScoreByCross?instance={instance}&topK={topK}"
            s = requests.session()
            s.keep_alive = False
            req = request.format(instance=element, topK=topK)
            response = requests.get(req)
            if response.status_code != 200:
                time.sleep(100 + i * 100)
                continue
            else:
                break
        return self.__parse2List(response)

    #Get Score by P(e|c)
    def getPCEScore(self, element, topK):
        for i in range(1000):
            request = "https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance={instance}&topK={topK}"
            s = requests.session()
            s.keep_alive = False
            req = request.format(instance=element, topK=topK)
            response = requests.get(req)
            if response.status_code != 200:
                time.sleep(100 + i * 100)
                continue
            else:
                break
        return self.__parse2List(response)

    #Get Score by P(c|e)
    def getPECScore(self, element, topK):
        for i in range(1000):
            request = "https://concept.research.microsoft.com/api/Concept/ScoreByProb?instance={instance}&topK={topK}"
            s = requests.session()
            s.keep_alive = False
            req = request.format(instance=element, topK=topK)
            response = requests.get(req)
            if response.status_code != 200:
                time.sleep(100 + i * 100)
                continue
            else:
                break
        return self.__parse2List(response)


    """
    return list of <concept, score> pair
    """
    def __parse2List(self, response):
        if (response.status_code != 200):
            return None
        jsonObj = json.loads(response.content)
        ret = {}
        for key in jsonObj:
            ret[key] = jsonObj[key]
        return ret

# kvs = MCGUtils().getBLCScore("docker",3)
# kvs = MCGUtils().getPCEScore("docker",3)
# kvs = MCGUtils().getPECScore("docker",3)
#print(kvs.items())