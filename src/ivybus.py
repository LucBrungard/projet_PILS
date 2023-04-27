from ivy.ivy import IvyServer

class MyAgent(IvyServer):
    def __init__(self, agent_name):
        IvyServer.__init__(self, agent_name)
        self.start("127.255.255.255:2010")
