from time import sleep
from ns import buildings, config_store, core, internet, lte, mobility, network

# Global variables
ctr_totRx = 0       # Counter for total received packets
ctr_totTx = 0       # Counter for total transmitted packets
baseline = 150.0    # Baseline distance in meter (150m for urban, 320m for freeway)

def ReceivePacket(socket):
    node = socket.GetNode()
    posMobility = node.GetObject(mobility.MobilityModel.GetTypeId())
    posRx = posMobility.GetPosition()
    packet = socket.Recv ()
    size = packet.GetSize()
    a = packet.CopyData(size)
    print("Paket ist", ''.join(map(chr, a)))

def SidelinkV2xAnnouncementMacTraceCbGenerator(socket):
    def camGenerator():
        node = socket.GetNode()
        id = node.GetId()
        simTime = core.Simulator.Now().GetMilliSeconds()
        posMobility = node.GetObject(mobility.MobilityModel.GetTypeId())
        posTx = posMobility.GetPosition()

        # check for each UE distance to transmitter
        # for i in range(ueVeh.GetN()):
            # mob = ueVeh.Get(i).GetObject(mobility.MobilityModel.GetTypeId())
            # posRx = mob.GetPosition()
            
            # distance = math.sqrt(pow((posTx.x - posRx.x), 2.0) + pow((posTx.y - posRx.y), 2.0))
            # if distance > 0 and distance <= baseline:
            #     ctr_totTx += 1

        # Generate CAM
        cam = f"{id-1};{simTime};{posTx.x};{posTx.y}"
        print(cam)
        # print(len(cam))
        # std::ostringstream msgCam;
        # msgCam << id-1 << ";" << simTime << ";" << (int) posTx.x << ";" << (int) posTx.y << '\0';

        # packet = Create<Packet>((uint8_t*)msgCam.str().c_str(),lenCam);
        packet = network.Packet(cam, len(cam))
        socket.Send(packet)
        # print("AFTER send")
        # core.LogComponentEnableAll(core.LOG_LEVEL_ALL)
        # sleep(3)
        # *log_tx_data->GetStream() << ctr_totTx << ";" << simTime << ";"  << id-1 << ";" << (int) posTx.x << ";" << (int) posTx.y << std::endl;
    
    return camGenerator

ueVeh = network.NodeContainer()

simTime = 100               # Simulation time in seconds
numVeh = 100                # Number of vehicles
lenCam = 190                # Length of CAM message in bytes [50-300 Bytes]
ueTxPower = 23.0            # Transmission power in dBm
probResourceKeep = 0.0      # Probability to select the previous resource again [0.0-0.8]
mcs = 20                    # Modulation and Coding Scheme
harqEnabled = False         # Retransmission enabled 
adjacencyPscchPssch = True  # Subchannelization scheme
partialSensing = False      # Partial sensing enabled (actual only partialSensing is false supported)
sizeSubchannel = 10         # Number of RBs per subchannel
numSubchannel = 3           # Number of subchannels per subframe
startRbSubchannel = 0       # Index of first RB corresponding to subchannelization
pRsvp = 100                 # Resource reservation interval 
t1 = 4                      # T1 value of selection window
t2 = 100                    # T2 value of selection window
slBandwidth = None          # Sidelink bandwidth

print("Starting network configuration...")

# Set the UEs power in dBm
core.Config.SetDefault ("ns3::LteUePhy::TxPower", core.DoubleValue (ueTxPower))
core.Config.SetDefault ("ns3::LteUePhy::RsrpUeMeasThreshold", core.DoubleValue (-10.0))
# Enable V2X communication on PHY layer
core.Config.SetDefault ("ns3::LteUePhy::EnableV2x", core.BooleanValue (True))

# Set power
core.Config.SetDefault ("ns3::LteUePowerControl::Pcmax", core.DoubleValue (ueTxPower))
core.Config.SetDefault ("ns3::LteUePowerControl::PsschTxPower", core.DoubleValue (ueTxPower))
core.Config.SetDefault ("ns3::LteUePowerControl::PscchTxPower", core.DoubleValue (ueTxPower))

if adjacencyPscchPssch:
    slBandwidth = sizeSubchannel * numSubchannel
else:
    slBandwidth = (sizeSubchannel+2) * numSubchannel

# Configure for UE selected
core.Config.SetDefault ("ns3::LteUeMac::UlBandwidth", core.UintegerValue(slBandwidth))
core.Config.SetDefault ("ns3::LteUeMac::EnableV2xHarq", core.BooleanValue(harqEnabled))
core.Config.SetDefault ("ns3::LteUeMac::EnableAdjacencyPscchPssch", core.BooleanValue(adjacencyPscchPssch))
core.Config.SetDefault ("ns3::LteUeMac::EnablePartialSensing", core.BooleanValue(partialSensing))
core.Config.SetDefault ("ns3::LteUeMac::SlGrantMcs", core.UintegerValue(mcs))
core.Config.SetDefault ("ns3::LteUeMac::SlSubchannelSize", core.UintegerValue (sizeSubchannel))
core.Config.SetDefault ("ns3::LteUeMac::SlSubchannelNum", core.UintegerValue (numSubchannel))
core.Config.SetDefault ("ns3::LteUeMac::SlStartRbSubchannel", core.UintegerValue (startRbSubchannel))
core.Config.SetDefault ("ns3::LteUeMac::SlPrsvp", core.UintegerValue(pRsvp))
core.Config.SetDefault ("ns3::LteUeMac::SlProbResourceKeep", core.DoubleValue(probResourceKeep))
core.Config.SetDefault ("ns3::LteUeMac::SelectionWindowT1", core.UintegerValue(t1))
core.Config.SetDefault ("ns3::LteUeMac::SelectionWindowT2", core.UintegerValue(t2))
# core.Config.SetDefault ("ns3::LteUeMac::EnableExcludeSubframe", core.BooleanValue(excludeSubframe)) 

inputConfig = config_store.ConfigStore()
inputConfig.ConfigureDefaults()

# Create node container to hold all UEs 
ueAllNodes = network.NodeContainer()

print("Installing Mobility Model...")

# Create nodes
ueVeh.Create (numVeh)
ueAllNodes.Add (ueVeh)

# Install constant random positions 
mobVeh = mobility.MobilityHelper()
mobVeh.SetMobilityModel("ns3::ConstantPositionMobilityModel")

staticVeh = [None] * ueVeh.GetN()

for i in range(ueVeh.GetN()):
    staticVeh[i] = mobility.ListPositionAllocator()
    rand = core.UniformRandomVariable ()
    x = rand.GetValue (0,100)
    y = rand.GetValue (0,100)
    z = 1.5
    staticVeh[i].Add(core.Vector(x,y,z))
    mobVeh.SetPositionAllocator(staticVeh[i])
    mobVeh.Install(ueVeh.Get(i))

print("Creating helpers...")

# EPC
epcHelper = lte.PointToPointEpcHelper()
pgw = epcHelper.GetPgwNode()

# LTE Helper
lteHelper = lte.LteHelper()
lteHelper.SetEpcHelper(epcHelper)
lteHelper.DisableNewEnbPhy()       # Disable eNBs for out-of-coverage modelling
    
# V2X 
lteV2xHelper = lte.LteV2xHelper ()
lteV2xHelper.SetLteHelper (lteHelper)

# Configure eNBs' antenna parameters before deploying them.
lteHelper.SetEnbAntennaModelType ("ns3::NistParabolic3dAntennaModel")

# Set pathloss model
# FIXME: InstallEnbDevice overrides PathlossModel Frequency with values from Earfcn
# 
lteHelper.SetAttribute ("UseSameUlDlPropagationCondition", core.BooleanValue(True))
core.Config.SetDefault ("ns3::LteEnbNetDevice::UlEarfcn", core.StringValue ("54990"))
# core.Config.SetDefault ("ns3::CniUrbanmicrocellPropagationLossModel::Frequency", core.DoubleValue(5800e6));
lteHelper.SetAttribute ("PathlossModel", core.StringValue ("ns3::CniUrbanmicrocellPropagationLossModel"))

# Create eNB Container
eNodeB = network.NodeContainer()
eNodeB.Create(1)

# Topology eNodeB
pos_eNB = mobility.ListPositionAllocator()
pos_eNB.Add(core.Vector(0, 0, 0))

# Install mobility eNodeB
mob_eNB = mobility.MobilityHelper()
mob_eNB.SetMobilityModel("ns3::ConstantPositionMobilityModel")
mob_eNB.SetPositionAllocator(pos_eNB)
mob_eNB.Install(eNodeB)

# Install Service
enbDevs = lteHelper.InstallEnbDevice(eNodeB)

# Required to use NIST 3GPP model
buildings.BuildingsHelper.Install (eNodeB)
buildings.BuildingsHelper.Install (ueAllNodes)
buildings.BuildingsHelper.MakeMobilityModelConsistent ()

# Install LTE devices to all UEs 
print ("Installing UE's network devices...")
lteHelper.SetAttribute("UseSidelink", core.BooleanValue (True))
ueRespondersDevs = lteHelper.InstallUeDevice (ueVeh)
ueDevs = network.NetDeviceContainer()
ueDevs.Add (ueRespondersDevs)

# Install the IP stack on the UEs
print ("Installing IP stack...")
internet_stack_helper = internet.InternetStackHelper()
internet_stack_helper.Install (ueAllNodes)

# Assign IP adress to UEs
print ("Allocating IP addresses and setting up network route...")
ueIpIface = epcHelper.AssignUeIpv4Address (ueDevs)
ipv4RoutingHelper = internet.Ipv4StaticRoutingHelper()

for u in range(ueAllNodes.GetN()):
    ueNode = ueAllNodes.Get(u)
    # Set the default gateway for the UE
    ueNode_ipv4 = ueNode.GetObject(internet.Ipv4.GetTypeId())
    ueStaticRouting = ipv4RoutingHelper.GetStaticRouting(ueNode_ipv4)
    ueStaticRouting.SetDefaultRoute (epcHelper.GetUeDefaultGatewayAddress(), 1)

print ("Attaching UE's to LTE network...")
# Attach each UE to the best available eNB
lteHelper.Attach(ueDevs)

print ("Creating sidelink groups...")
txGroups = lteV2xHelper.AssociateForV2xBroadcast(ueRespondersDevs, numVeh)

lteV2xHelper.PrintGroups(txGroups)
# compute average number of receivers associated per transmitter and vice versa
totalRxs = 0.0
txPerUeMap = {}
groupsPerUe = {}

for group in txGroups:
    numDevs = group.GetN()
    totalRxs += numDevs-1

    for i in range(1, numDevs):
        nId = group.Get(i).GetNode().GetId()
        if nId not in txPerUeMap:
            txPerUeMap[nId] = 0
        txPerUeMap[nId] += 1

totalTxPerUe = 0

for txKey, txValue in txPerUeMap.items():
    totalTxPerUe += txValue
    if txValue not in groupsPerUe:
        groupsPerUe [txValue] = 0
    groupsPerUe [txValue] += 1

print ("Installing applications...")

# Application Setup for Responders
groupL2Addresses = []
groupL2Address = 0x00
internet.Ipv4AddressGenerator.Init(network.Ipv4Address ("225.0.0.0"), network.Ipv4Mask("255.0.0.0"))
clientRespondersAddress = internet.Ipv4AddressGenerator.NextAddress (network.Ipv4Mask ("255.0.0.0"))

application_port = 8000 # Application port to TX/RX
activeTxUes = network.NetDeviceContainer()

for group in txGroups:
    # Create Sidelink bearers
    # Use Tx for the group transmitter and Rx for all the receivers
    # Split Tx/Rx
 
    txUe = network.NetDeviceContainer (group.Get(0))    # TODO GPA: wirklich neues Objekt?
    activeTxUes.Add(txUe)
    rxUes = lteV2xHelper.RemoveNetDevice (group, txUe.Get (0))
    tft = lte.LteSlTft (lte.LteSlTft.TRANSMIT, clientRespondersAddress, groupL2Address)
    lteV2xHelper.ActivateSidelinkBearer (core.Seconds(0.0), txUe, tft)
    tft = lte.LteSlTft (lte.LteSlTft.RECEIVE, clientRespondersAddress, groupL2Address)
    lteV2xHelper.ActivateSidelinkBearer (core.Seconds(0.0), rxUes, tft)

    # print("Created group L2Address=", groupL2Address, " IPAddress=")
    # clientRespondersAddress.Print(std::cout); # eventuell clientRespondersAddress.Print(sys.stdout)
    # print("")

    # Individual Socket Traffic Broadcast everyone
    host = network.Socket.CreateSocket(txUe.Get(0).GetNode(), core.TypeId.LookupByName ("ns3::UdpSocketFactory"))
    host.Bind()
    host.Connect(network.InetSocketAddress(clientRespondersAddress, application_port))
    host.SetAllowBroadcast(True)
    host.ShutdownRecv()

    # Ptr<LteUeRrc> ueRrc = DynamicCast<LteUeRrc>( txUe.Get (0)->GetObject<LteUeNetDevice> ()->GetRrc () );    
    # ueRrc->TraceConnectWithoutContext ("SidelinkV2xMonitoring", MakeBoundCallback (&SidelinkV2xMonitoringTrace, stream));
    # oss << txUe.Get(0) ->GetObject<LteUeNetDevice>()->GetImsi(); 
    # Ptr<LteUePhy> uePhy = DynamicCast<LteUePhy>( txUe.Get (0)->GetObject<LteUeNetDevice> ()->GetPhy () );
    # uePhy->TraceConnect ("SidelinkV2xAnnouncement", oss.str() ,MakeBoundCallback (&SidelinkV2xAnnouncementPhyTrace, stream1));
    # uePhy->TraceConnectWithoutContext ("SidelinkV2xAnnouncement", MakeBoundCallback (&SidelinkV2xAnnouncementPhyTrace, host));
    ueMac = txUe.Get (0).GetObject(lte.LteUeNetDevice.GetTypeId()).GetMac ()
    ueMac.TraceConnectWithoutContext ("SidelinkV2xAnnouncement", SidelinkV2xAnnouncementMacTraceCbGenerator(host))
    # ueMac.TraceConnectWithoutContext ("SidelinkV2xAnnouncement", MakeBoundCallback (&SidelinkV2xAnnouncementMacTrace, host))    # TODO GPA: Callback
    # ueMac->TraceConnect ("SidelinkV2xAnnouncement", oss.str() ,MakeBoundCallback (&SidelinkV2xAnnouncementMacTrace, stream2));

    sink = network.Socket.CreateSocket(txUe.Get(0).GetNode(), core.TypeId.LookupByName ("ns3::UdpSocketFactory"))
    sink.Bind(network.InetSocketAddress (network.Ipv4Address.GetAny (), application_port))
    sink.SetRecvCallback (ReceivePacket)        # TODO GPA: Callback

    # store and increment addresses
    groupL2Addresses.append (groupL2Address)
    groupL2Address += 1
    clientRespondersAddress = internet.Ipv4AddressGenerator.NextAddress (network.Ipv4Mask ("255.0.0.0"))

print ("Creating Sidelink Configuration...")
ueSidelinkConfiguration = lte.LteUeRrcSl ()
ueSidelinkConfiguration.SetSlEnabled(True)
ueSidelinkConfiguration.SetV2xEnabled(True)

preconfiguration = lte.LteRrcSap.SlV2xPreconfiguration()
preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommPreconfigGeneral.carrierFreq = 54890
preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommPreconfigGeneral.slBandwidth = slBandwidth

preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommTxPoolList.nbPools = 1
preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommRxPoolList.nbPools = 1

pFactory = lte.SlV2xPreconfigPoolFactory()
pFactory.SetHaveUeSelectedResourceConfig (True)
pFactory.SetSlSubframe (0xFFFFF)
pFactory.SetAdjacencyPscchPssch (adjacencyPscchPssch)
pFactory.SetSizeSubchannel (sizeSubchannel)
pFactory.SetNumSubchannel (numSubchannel)
pFactory.SetStartRbSubchannel (startRbSubchannel)
pFactory.SetStartRbPscchPool (0)
pFactory.SetDataTxP0 (-4)
pFactory.SetDataTxAlpha (0.9)

preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommTxPoolList.pools[0] = pFactory.CreatePool ()
preconfiguration.v2xPreconfigFreqList.freq[0].v2xCommRxPoolList.pools[0] = pFactory.CreatePool ()
ueSidelinkConfiguration.SetSlV2xPreconfiguration (preconfiguration) 

# // Print Configuration
# *log_rx_data->GetStream() << "RxPackets;RxTime;RxId;TxId;TxTime;xPos;yPos" << std::endl;
# *log_tx_data->GetStream() << "TxPackets;TxTime;TxId;xPos;yPos" << std::endl;

print ("Installing Sidelink Configuration...")
lteHelper.InstallSidelinkV2xConfiguration (ueRespondersDevs, ueSidelinkConfiguration)

print ("Enabling LTE traces...")
lteHelper.EnableTraces()

# *log_simtime->GetStream() << "Simtime;TotalRx;TotalTx;PRR" << std::endl; 
# core.Simulator.Schedule(core.Seconds(1), &PrintStatus, 1, log_simtime)

print ("Starting Simulation...")
core.Simulator.Stop(core.MilliSeconds(simTime*1000+40))
core.Simulator.Run()
core.Simulator.Destroy()

print ("Simulation done.")
