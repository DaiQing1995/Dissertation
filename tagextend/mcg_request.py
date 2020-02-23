import requests
from requests.exceptions import ConnectionError
import json
import time

class MCGUtils:

    requests.adapters.DEFAULT_RETRIES = 8
    proxy = {"http": "112.84.52.181:9999"}

    # def getBLCScore(self, element, topK):
    #     for i in range(1000):
    #         request = "https://concept.research.microsoft.com/api/Concept/ScoreByCross?instance={instance}&topK={topK}"
    #         s = requests.session()
    #         s.proxies = self.proxy
    #         s.keep_alive = False
    #         req = request.format(instance=element, topK=topK)
    #         response = requests.get(req, timeout=50)
    #         if response.status_code != 200:
    #             time.sleep(100 + i * 100)
    #             continue
    #         else:
    #             break
    #     return self.__parse2List(response)

    pce_cache = {}
    #Get Score by P(e|c)
    def getPCEScore(self, element, topK):
        if element in self.pce_cache.keys():
            return self.pce_cache[element]
        for i in range(1000):
            request = "https://concept.research.microsoft.com/api/Concept/ScoreByTypi?instance={instance}&topK={topK}"
            s = requests.session()
            s.proxies = self.proxy
            s.keep_alive = False
            req = request.format(instance=element, topK=topK)
            try:
                response = requests.get(req, timeout=50)
                if response.status_code != 200:
                    time.sleep(10 + i * 5)
                    continue
                else:
                    break
            except ConnectionError:
                time.sleep(10 + i * 5)
                continue
        self.pce_cache[element] = self.__parse2List(response)
        return self.pce_cache[element]


    pec_cache = {}
    #Get Score by P(c|e)
    def getPECScore(self, element, topK):
        if element in self.pec_cache.keys():
            return self.pec_cache[element]
        for i in range(1000):
            request = "https://concept.research.microsoft.com/api/Concept/ScoreByProb?instance={instance}&topK={topK}"
            s = requests.session()
            s.proxies = self.proxy
            s.keep_alive = False
            req = request.format(instance=element, topK=topK)
            try:
                response = requests.get(req, timeout=50)
                if response.status_code != 200:
                    time.sleep(10 + i * 5)
                    continue
                else:
                    break
            except ConnectionError:
                time.sleep(10 + i * 5)
                continue
        self.pec_cache[element] = self.__parse2List(response)
        return self.pec_cache[element]


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