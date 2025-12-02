from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

# ============================================================================
# Create Order Fulfillment Process Model
# ============================================================================

def create_fulfillment_process():
    """
    Creates the order fulfillment process as a Petri net.
    Process: Receive -> Validate -> Pick -> Pack -> Ship
    """
    net = PetriNet("order_fulfillment")
    
    # Create places
    source = PetriNet.Place("source")
    p_received = PetriNet.Place("p_received")
    p_validated = PetriNet.Place("p_validated")
    p_picked = PetriNet.Place("p_picked")
    p_packed = PetriNet.Place("p_packed")
    sink = PetriNet.Place("sink")
    
    net.places.add(source)
    net.places.add(p_received)
    net.places.add(p_validated)
    net.places.add(p_picked)
    net.places.add(p_packed)
    net.places.add(sink)
    
    # Create transitions (activities)
    t_receive = PetriNet.Transition("Receive", "Receive")
    t_validate = PetriNet.Transition("Validate", "Validate")
    t_pick = PetriNet.Transition("Pick", "Pick")
    t_pack = PetriNet.Transition("Pack", "Pack")
    t_ship = PetriNet.Transition("Ship", "Ship")
    
    net.transitions.add(t_receive)
    net.transitions.add(t_validate)
    net.transitions.add(t_pick)
    net.transitions.add(t_pack)
    net.transitions.add(t_ship)
    
    # Create arcs
    petri_utils.add_arc_from_to(source, t_receive, net)
    petri_utils.add_arc_from_to(t_receive, p_received, net)
    petri_utils.add_arc_from_to(p_received, t_validate, net)
    petri_utils.add_arc_from_to(t_validate, p_validated, net)
    petri_utils.add_arc_from_to(p_validated, t_pick, net)
    petri_utils.add_arc_from_to(t_pick, p_picked, net)
    petri_utils.add_arc_from_to(p_picked, t_pack, net)
    petri_utils.add_arc_from_to(t_pack, p_packed, net)
    petri_utils.add_arc_from_to(p_packed, t_ship, net)
    petri_utils.add_arc_from_to(t_ship, sink, net)
    
    # Markings
    initial_marking = Marking()
    initial_marking[source] = 1
    final_marking = Marking()
    final_marking[sink] = 1
    
    return net, initial_marking, final_marking


# ============================================================================
# Configure Activity Durations and Resources
# ============================================================================
# Activity durations (in minutes) - using normal distribution
ACTIVITY_DURATIONS = {
    'Receive': {'mean': 2, 'std': 0.5},      # Automatic, fast
    'Validate': {'mean': 5, 'std': 1.0},     # Manual validation
    'Pick': {'mean': 8, 'std': 1.5},         # Walking + picking items
    'Pack': {'mean': 6, 'std': 1.0},         # Packing boxes
    'Ship': {'mean': 3, 'std': 0.5}          # Label + handoff
}

# Resource pools
RESOURCES = {
    'Validate': 3,  # 3 validators
    'Pick': 5,      # 5 pickers
    'Pack': 2,      # 2 packers (BOTTLENECK)
    'Ship': 2       # 2 shippers
}

# ============================================================================
# Todo
# ============================================================================
# -) Create a Bot-Storm simulation
# -) Bottleneck analysis
#   -) Visualize the bottleneck
# -) Change the Resources to decrease the severity of the bottleneck
