# Import necessary modules
from m5.objects import *

# Create the system
system = System()

# Set the clock frequency and memory mode
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create the CPU with a branch predictor
system.cpu = TimingSimpleCPU()
system.cpu.branchPred = BranchPredictor()

# Enable pipelined tracing for detailed visualization
system.cpu[0].enable_pipelined_tracing = True

# Create the memory bus
system.membus = SystemXBar()

# Connect the CPU ports
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

# Set up the interrupt controller for the CPU
system.cpu.createInterruptController()

# Create a system-wide memory controller
system.system_port = system.membus.master

# Create a memory controller and connect it to the memory bus
system.mem_ctrl = DDR3_1600_8x8()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Create a process for running the workload
process = LiveProcess()
process.cmd = ['/path/to/your/workload']
system.cpu.workload = process
system.cpu.createThreads()

# Instantiate the system and run the simulation
root = Root(full_system = False, system = system)
m5.instantiate()

print("Starting simulation")
exit_event = m5.simulate()
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
