import json
from pprint import pprint
import requests
import time, random
import salt.client

resNodes = requests.get('URL')
reseng = requests.get('URL')
data = json.loads(resNodes.text)
dataeng = json.loads(reseng.text)

FUZZ = True

def fuzz():
    if FUZZ:
        time.sleep(random.random())

class processData(object):
    """docstring for processData, it will retrieve dict info
    """

    def __init__(self):
        self.nodeId = []
        for item in range(0, len(data['nodes']), 1):
            app = data['nodes'][item]['node-id']
            self.nodeId.append(app)

    def gen_node_type(self):
        self.typeDict = {}
        for item in range(0, len(data['nodes']), 1):
            self.type = data['nodes'][item]['type']
            self.typeDict[self.nodeId[item]] = self.type
        return self.typeDict

    def gen_node_req(self):
        self.reqDict = {}
        for item in range(0, len(data['nodes']), 1):
            if 'required-nodes' in data['nodes'][item]:
                self.req = data['nodes'][item]['required-nodes']
                self.reqDict[self.nodeId[item]] = self.req
        return self.reqDict

    def gen_node_status(self):
        self.statusDict = {}
        for item in range(0, len(data['nodes']), 1):
            self.status = data['nodes'][item]['status']
            self.statusDict[self.nodeId[item]] = self.status
        return self.statusDict

    def gen_node_name(self):
        self.nameDict = {}
        for item in range(0, len(data['nodes']), 1):
            if 'host-name' in data['nodes'][item]:
                self.name = data['nodes'][item]['host-name']
                self.nameDict[self.nodeId[item]] = self.name
        return self.nameDict

    def gen_node_primary(self):
        self.primaryDict = {}
        for item in range(0, len(data['nodes']), 1):
            if 'primary' in data['nodes'][item]:
                #self.primary = data['nodes'][item]['primary']
                self.type = data['nodes'][item]['type']
                self.primaryDict[self.nodeId[item]] = self.type
        return self.primaryDict

    def gen_node_internal(self):
        self.internalDict = {}
        for item in range(0, len(data['nodes']), 1):
            if 'internal' in data['nodes'][item]:
                #self.internal = data['nodes'][item]['internal']
                self.type = data['nodes'][item]['type']
                self.internalDict[self.nodeId[item]] = self.type
        return self.internalDict

    def gen_node_partitions(self):
        self.partitionDict = {}
        for item in range(0, len(dataeng['nodes']), 1):
            self.type = dataeng['nodes'][item]['type']
            self.partitionDict[self.nodeId[item]] = self.type
        return self.partitionDict

class deployNodes(processData):
    """deploy nodes"""
    def __init__(self, target):
        super(deployNodes,self).__init__()
        super(deployNodes,self).gen_node_req()
        super(deployNodes,self).gen_node_status()
        super(deployNodes,self).gen_node_name()
        super(deployNodes,self).gen_node_primary()
        super(deployNodes,self).gen_node_internal()
        self.target = target
        self.targetId = []
        self.check_name()
        self.check_req()

    @staticmethod
    def check_engPartitions():
        for key in dataeng['partitions'].keys():
            while dataeng['partitions'][key]['status'] != 'ALLOCATED':
                print 'Waititing partitions to allocate'
                print dataeng['partitions'][key]['status']


    def check_name(self):
        #check if node is found in the nameDict and return node ID
        for item in xrange(0, len(self.target), 1):
            for nameKey, nameValue in self.nameDict.iteritems():
                if self.target[item] in nameValue:
                    self.targetId.append(nameKey)

        return self.targetId

    def check_req(self):
        #check if node has a prior requirement and what are they
        for item in xrange(0, len(self.targetId), 1):
            try:
                self.check_reqNodeId(self, self.reqDict[self.targetId[item]], self.targetId[item])
            except:
                self.deploy_push(self, self.targetId[item])

    @staticmethod
    def check_reqNodeId(self, reqList, nodeId):
        typeListTemp = []
        #check required-nodes ids and call function to check status of each
        for item in xrange(0, len(reqList), 1):
            #check required-nodes ids are found on the primaryDict
            for priKey, priValue in self.primaryDict.iteritems():
                if reqList[item] == priValue:
                    typeListTemp.append(priKey)
            #check required-nodes ids are found on the internalDict
            for internalKey, internalValue in self.internalDict.iteritems():
                if reqList[item] == internalValue:
                    typeListTemp.append(internalKey)

        self.check_reqNodeStatus(self, typeListTemp, nodeId)

    @staticmethod
    def check_reqNodeStatus(self, nodeList, nodeId):
        #check required-nodes status
        self.countStatus = 0
        for item in xrange(0, len(nodeList), 1):
            if self.statusDict[nodeList[item]] == 'ACTIVE':
                self.countStatus += 1
        #Send the message to deploy if required-nodes are active
        if self.countStatus == len(nodeList):
            self.deploy_push(self, nodeId)


    @staticmethod
    def deploy_push(self, nodeId):
        if 'edge01' in self.nameDict[nodeId]:
            print ('Checking eng partitions!')
            self.check_engPartitions()

        message = EventPayload(self.nameDict[nodeId])
        message.firePayload()

class EventPayload(object):

    def __init__(self, minion):
        self.minion = minion

    caller = salt.client.Caller()

    def firePayload(self):
        print ('Deploy away with "%s"' % self.minion)
        fuzz()

        caller.sminion.functions['event.send'](
            'myco/myevent/success',
            {
                'success': True,
                'hostname': self.hostname,
                'message': self.payload,
            }
        )


if __name__ == '__main__':
    dpl = deployNodes(['node1', 'node2'])
