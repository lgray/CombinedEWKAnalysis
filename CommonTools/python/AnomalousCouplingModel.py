from HiggsAnalysis.CombinedLimit.PhysicsModel import *

# mainly based off of FloatingXSHiggs
# basic piping for a charged aTGC model
class AnomalousCouplingModel(PhysicsModel):
    """allow TGC to float and change in a correlated way the Higgs mass"""
    def __init__(self):
        PhysicsModel.__init__(self)        
        self.anomCoupSearchWindows = {}
        self.processes = []
        self.channels = []
        self.pois = [] #aka anomalous couplings

    #things coming in from the command line
    def setPhysicsOptions(self,physOptions):
        """make the POI (anomalous couplings!) for each included mode"""
        for po in physOptions:
            if po.startswith("modes="):
                self.modes = po.replace("modes=","").split(",")
            if po.startswith("poi="):
                self.pois = po.replace("poi=","").split(",")
            #process the relevant POIs
            for poi in self.pois:
                if po.startswith("range_%s"%poi):
                    self.anomCoupSearchWindows[poi] = po.replace\
                                                      ("range_%s"%poi,"").\
                                                      split(",")
                    if len(self.anomCoupSearchWindows[poi]) != 2:
                        raise RuntimeError, "Anomalous couplings range definition requires two extrema"
                elif float(self.anomCoupSearchWindows[poi][0]) >= float(self.anomCoupSearchWindows[poi][1]):
                    raise RuntimeError, "Anomalous coupling range: Extrema for anomalous coupling range defined with inverterd order. Second must be larger the first"

    def buildScaling(self,process,channel):
        raise RuntimeError('NotImplemented',
                           'buildScaling() not implemented')
    
    def doParametersOfInterest(self):
        for poi in self.pois:
            lower = self.anomCoupSearchWindows[poi][0]
            upper = self.anomCoupSearchWindows[poi][1]
            self.modelBuilder.doVar('%s[%s,%s]'%(poi,lower,upper))
        self.modelBuilder.doSet('POI',','.join(self.pois))

        # in the derived classes this takes care of loading the
        # correct cross section scalings for each contributing channel
        # this is a bit tricky, maybe, since different channels for the same
        # mode can have different scaling functions due to phase space
        self.processScaling = {}
        for process in self.processes:
            for channel in self.channels:
                idx = '%s_%s'%(process,channel)
                self.processScaling[idx] = self.buildScaling(process,channel)
        
        # display the glory of our work
        self.modelBuilder.out.Print()
        print self.processScaling

    def getYieldScale(self,bin,process):
        for prefix, model in self.processScaling.iteritems():
            print prefix, model
            if process.startswith(prefix):
                return 'Scaling_'+model
        return 1
        

    
