from ivy.ivy import IvyServer

class MyAgent(IvyServer):
    def __init__(self, agent_name):
        IvyServer.__init__(self,agent_name)
        self.start('127.255.255.255:2010')

    """def connection_msg(self, agent, event):
        if event == IvyApplicationDisconnected :
            print('Ivy application ', agent, ' has disconnected')
        else:
            print('Ivy application ', agent, ' has connected')
        print('Ivy applications currently on the bus : %s',
            ','.join(IvyGetApplicationList()))"""