from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa

def generate_busStops():
    busstops = [
    "   <busStop id=\"4083982305\" lane=\"360929409_0\" startPos=\"40.93\" endPos=\"55.93\" name friendlyPos=\"1\" lines=\"196E 196F 196D\"/>",
    "   <busStop id=\"5366197376\" lane=\"358981135_0\" startPos=\"28.90\" endPos=\"43.90\" name friendlyPos=\"1\" lines=\"196E 196F 196D 154A 236B\"/>",
    "   <busStop id=\"5361514763\" lane=\"358980528#0_0\" startPos=\"12.77\" endPos=\"27.77\" name friendlyPos=\"1\" lines=\"196E 196F 196D 154A 236B\"/>",
    "   <busStop id=\"4945877795\" lane=\"344153330#1_0\" startPos=\"2.60\" endPos=\"17.60\" name friendlyPos=\"1\" lines=\"155C 196E 196F 196D 160 156 168\"/>",
    "   <busStop id=\"4696675292\" lane=\"55354008_0\" startPos=\"31.54\" endPos=\"46.54\" name friendlyPos=\"1\" lines=\"155C 196E 196F 196D 591 222A 156 168\"/>",
    "   <busStop id=\"5286257146\" lane=\"499726265_0\" startPos=\"3.47\" endPos=\"18.47\" name friendlyPos=\"1\" lines=\"212J 541I 541M 541K 541R 541T 541Q 196E 212B 196F 196D 541S 212C 212X 212S 212Q 591 590 222 221 222D\"/>",
    "   <busStop id=\"3729684442\" lane=\"301521095#2_0\" startPos=\"38.69\" endPos=\"53.69\" name friendlyPos=\"1\" lines=\"212J 541I 541M 541K 541R 541T 541Q 355B 355C 196E 212B 196F 1965 541S 212C 212X 212S\"/>",
    "   <busStop id=\"2435446332\" lane=\"368494308#2_0\" startPos=\"58.68\" endPos=\"73.68\" name friendlyPos=\"1\" lines=\"212J 541I 541M 541K 541R 541T 541Q 355B 355C 196E 212B 196F 1965 541S 212C 212X 212S 212Q\"/>",
    "   <busStop id=\"2435446333\" lane=\"368486584#2_0\" startPos=\"22.68\" endPos=\"37.68\" name friendlyPos=\"1\" lines=\"196E 196F 1965\"/>",
    "   <busStop id=\"2435470839\" lane=\"224088356_0\" startPos=\"0.00\" endPos=\"13.66\" name friendlyPos=\"1\" lines=\"196E 196F 1965\"/>",
    "   <busStop id=\"2035590397\" lane=\"777361473#1_0\" startPos=\"23.37\" endPos=\"38.37\" name friendlyPos=\"1\" lines=\"196E 196F 1965\"/>",
    "   <busStop id=\"2449072192\" lane=\"371535957#0_0\" startPos=\"6.87\" endPos=\"21.87\" name friendlyPos=\"1\" lines=\"196E 196F 1965\"/>",
    "   <busStop id=\"2449072194\" lane=\"478958532#1_0\" startPos=\"53.42\" endPos=\"68.42\" name friendlyPos=\"1\" lines=\"196E 196F 1965\"/>",
    "   <busStop id=\"2449072196\" lane=\"372500759#0_0\" startPos=\"22.07\" endPos=\"37.07\" name friendlyPos=\"1\" lines=\"196F 1965\"/>",
    "   <busStop id=\"2647914597\" lane=\"199426663_0\" startPos=\"105.98\" endPos=\"120.98\" name friendlyPos=\"1\" lines=\"196F 1965 Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"5557991904\" lane=\"459839153#2_0\" startPos=\"32.38\" endPos=\"47.38\" name friendlyPos=\"1\" lines=\"196F 1965\"/>",
    "   <busStop id=\"4945812529\" lane=\"259733754#2_0\" startPos=\"6.72\" endPos=\"21.72\" name friendlyPos=\"1\" lines=\"196E 196F\"/>",
    "   <busStop id=\"4945812528\" lane=\"363481691#2_0\" startPos=\"0.00\" endPos=\"11.08\" name friendlyPos=\"1\" lines=\"196E 196F\"/>",
    "   <busStop id=\"2976399351\" lane=\"363481691#8_0\" startPos=\"11.27\" endPos=\"26.27\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2976399348\" lane=\"363481691#12_0\" startPos=\"45.64\" endPos=\"60.64\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2976418641\" lane=\"303099159#2_0\" startPos=\"0.06\" endPos=\"15.06\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"4181552955\" lane=\"569156536#0_0\" startPos=\"72.81\" endPos=\"87.81\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2071578441\" lane=\"363480437#2_0\" startPos=\"11.25\" endPos=\"26.25\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"3135882098\" lane=\"303082591#2_0\" startPos=\"20.04\" endPos=\"32.47\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"6512254738\" lane=\"259470103#5_0\" startPos=\"17.33\" endPos=\"25.95\" name friendlyPos=\"1\" lines=\"196E 196F\"/>",
    "   <busStop id=\"3393237218\" lane=\"258407149#2_0\" startPos=\"0.00\" endPos=\"14.23\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"4544750287\" lane=\"303082587#2_0\" startPos=\"7.59\" endPos=\"22.59\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"1917492638\" lane=\"303107781#0_0\" startPos=\"35.44\" endPos=\"50.44\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"3743485949\" lane=\"303082585#2_0\" startPos=\"12.00\" endPos=\"27.00\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"3135882108\" lane=\"303082585#6_0\" startPos=\"1.17\" endPos=\"15.98\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2976551190\" lane=\"303082593#0_0\" startPos=\"4.00\" endPos=\"19.00\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2452978092\" lane=\"258407154_0\" startPos=\"71.00\" endPos=\"86.74\" name friendlyPos=\"1\" lines=\"196E 196F Santa Maria Porto Alegre via Cachoeira do Sul\"/>",
    "   <busStop id=\"2452978323\" lane=\"368091908#1_0\" startPos=\"24.27\" endPos=\"39.27\" name friendlyPos=\"1\" lines=\"Circular UFSM 196E 196F 1965 196I 196D 197C\"/>",
    "   <busStop id=\"2452978396\" lane=\"368091908#2_0\" startPos=\"24.00\" endPos=\"39.00\" name friendlyPos=\"1\" lines=\"Circular UFSM 196E 196F 1965 196I 196D 197C\"/>",
    "   <busStop id=\"4210138292\" lane=\"410386372_0\" startPos=\"47.00\" endPos=\"62.00\" name friendlyPos=\"1\" lines=\"196E 196F 1965 196I 196D 197C\"/>",
    "   <busStop id=\"3061763319\" lane=\"301981257#1_0\" startPos=\"58.85\" endPos=\"73.85\" name friendlyPos=\"1\" lines=\"196E 196F 1965 196I 196D 197C\"/>",
    "   <busStop id=\"2400147129\" lane=\"167699930#3_0\" startPos=\"2.00\" endPos=\"17.00\" name friendlyPos=\"1\" lines=\"Circular UFSM 196E 196F 1965 196I 196D 197C\"/>",
    "   <busStop id=\"3061763287\" lane=\"301981265#3_0\" startPos=\"15.00\" endPos=\"30.00\" name friendlyPos=\"1\" lines=\"Circular UFSM 196E 196F 1965 196I 196D 197C\"/>"
     ]
 
 
    with open("osm.busstop.xml", "w") as routes:
        print("""<?xml version="1.0" encoding="UTF-8"?>
<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">""", file=routes)
        i = 1
        a = 6 # default value for busstop
        for busstop  in busstops:
                if (i < 10): # busstop antes do Icaro
                    a = random.randint(5, 20)
                if (i >= 10 and i < 36): # paradas na faixa
                    a = random.randint(0, 10)
                if (i >= 35): # paradas proximas a UFSM
                    a = random.randint(0, 2)
                print(busstop.replace("name", "name=\"p%i\" personCapacity=\"%a\" ") %(i, a) , file=routes)
                i+=1
        print("</additional>", file=routes)
       


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    generate_busStops()

    
     
