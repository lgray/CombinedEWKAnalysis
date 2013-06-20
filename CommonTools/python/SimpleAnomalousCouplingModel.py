from HiggsAnalysis.CombinedLimit.PhysicsModel import *

# mainly based off of FloatingXSHiggs
# basic piping for a charged aTGC model
class ATGCModel(PhysicsModel):
    """allow TGC to float and change in a correlated way the Higgs mass"""
    def __init__(self):
        PhysicsModel.__init__(self)        
        self.anomCoupSearchWindows = {}
        self.modes = ["WW","WZ","Wgamma"]
        self.pois = [] #aka anomalous couplings

    #things coming in from the command line (XS interpolation files, etc)
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
                    raise RuntimeError, "Anomalous coupling range: Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"
    def doParametersOfInterest(self):
        pass
                
        

    
