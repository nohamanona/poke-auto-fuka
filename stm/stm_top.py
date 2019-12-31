from transitions import Machine
from transitions.extensions.states import add_state_features, Volatile
from stm.volatile_class_hatch import VolatileClassHatch
from stm.volatile_class_run import VolatileClassRun
from stm.volatile_class_prepare import VolatileClassPrepare
from stm.volatile_class_get import VolatileClassGet


@add_state_features(Volatile)
class CustomMachine(Machine):
    pass

#states = [{'name':'STANBY'},
#          {'name':'PREPARE', 'volatile':VolatileClassPrepare},
#          {'name':'RUN', 'volatile':VolatileClassRun},
#          {'name':'HATCH', 'volatile':VolatileClassHatch},
#          {'name':'GET', 'volatile':VolatileClassGet}]
#
#transitions = [
#    {'trigger':'fromSTANBYtoPREPARE', 'source':'STANBY', 'dest':'PREPARE', 'after':'action_after'},
#    {'trigger':'fromPREPAREtoRUN', 'source':'PREPARE', 'dest':'RUN', 'after':'action_after'},
#    {'trigger':'fromRUNtoHATCH', 'source':'RUN', 'dest':'HATCH', 'after':'action_after'}   
#]

class Model(object):

    def action_after(self):
        print('////////////////////////',self.state,'////////////////////////')
        #self.scope.state_action()

    def action_after_PtoR(self):
        print('////////////////////////',self.state,'////////////////////////')
        self.scope.run_control_state ='AP'
    
    def action_after_HtoR(self):
        print('////////////////////////',self.state,'////////////////////////')
        self.scope.run_control_state ='RUN L'

    def action_after_GtoR(self):
        print('////////////////////////',self.state,'////////////////////////')
        self.scope.run_control_state ='AG'

    def __init__(self):
        self.states = [{'name':'STANBY'},
              {'name':'PREPARE', 'volatile':VolatileClassPrepare},
              {'name':'RUN', 'volatile':VolatileClassRun},
              {'name':'HATCH', 'volatile':VolatileClassHatch},
              {'name':'GET', 'volatile':VolatileClassGet}]

        self.transitions = [
                  {'trigger':'fromSTANBYtoPREPARE', 'source':'STANBY', 'dest':'PREPARE', 'after':'action_after'},
                  {'trigger':'fromPREPAREtoRUN', 'source':'PREPARE', 'dest':'RUN', 'after':'action_after_PtoR'},
                  {'trigger':'fromRUNtoHATCH', 'source':'RUN', 'dest':'HATCH', 'after':'action_after'},
                  {'trigger':'fromHATCHtoRUN', 'source':'HATCH', 'dest':'RUN', 'after':'action_after_HtoR'},
                  {'trigger':'fromRUNtoGET', 'source':'RUN', 'dest':'GET', 'after':'action_after'},
                  {'trigger':'fromGETtoRUN', 'source':'GET', 'dest':'RUN', 'after':'action_after_GtoR'}]


if __name__ == '__main__':
    model = Model()
    #print(model.states)
    machine = CustomMachine(model=model, states=model.states, transitions=model.transitions, initial=model.states[0]["name"], 
                            auto_transitions=False, ordered_transitions=False) 

    print(model.state)
    model.fromSTANBYtoPREPARE()
    print(model.state)
    if model.scope.next_state == 'RUN':
        model.fromPREPAREtoRUN()
    elif model.scope.next_state == 'HATCH':
        model.fromRUNtoHATCH()
