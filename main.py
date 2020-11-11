import random
import sys
import time
from Question import *

start = time.time()

# generate random ip address starting information
oct1 = random.randrange(1, 255)
oct2 = random.randrange(1, 255)
oct3 = random.randrange(1, 255)
oct4 = random.randrange(1, 255)
networkBits = random.randrange(16, 28)
hostBits = 32 - networkBits
ip = "{}.{}.{}.{}/{}".format(oct1, oct2, oct3, oct4, networkBits)

# determine octet number where separation takes place
if networkBits > 24:
    octNum = 4
    selectedOctet = oct4
    oct4 = 0
elif 24 >= networkBits > 16:
    octNum = 3
    selectedOctet = oct3
    # oct3 = 0
    oct4 = 0
elif 16 >= networkBits > 8:
    octNum = 2
    selectedOctet = 2
    oct3 = 0
    oct4 = 0
elif 8 >= networkBits:
    octNum = 1
    selectedOctet = oct1
    oct2 = 0
    oct3 = 0
    oct4 = 0
else:
    print("error determining octet number where separation takes place")


# Functions ##########
# track time to display at completion
def time_convert(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    print("You completed this quiz in "
          "{} Hours {} Minutes {} Seconds".format(int(hours), int(minutes), int(round(seconds, 2))))


# calculate binary representation
def to_binary():
    oct1binary = '{0:08b}'.format(oct1)
    oct2binary = '{0:08b}'.format(oct2)
    oct3binary = '{0:08b}'.format(oct3)
    oct4binary = '{0:08b}'.format(oct4)
    bin_rep = "{}.{}.{}.{}".format(oct1binary, oct2binary, oct3binary, oct4binary)

    return bin_rep


# determine subnet mask
subnet = [oct1, oct2, oct3, oct4]
ip = "{}.{}.{}.{}/{}".format(oct1, oct2, oct3, oct4, networkBits)


def calc_subnet_mask():
    oct_1_mask = 0
    oct_2_mask = 0
    oct_3_mask = 0
    oct_4_mask = 0

    if networkBits >= 24:
        diff = 32 - networkBits
        oct_1_mask = 255
        oct_2_mask = 255
        oct_3_mask = 255
        while diff < 8:
            oct_4_mask = oct_4_mask + (2**diff)
            diff = diff + 1
    elif 24 > networkBits >= 16:
        diff = 24 - networkBits
        oct_1_mask = 255
        oct_2_mask = 255
        while diff < 8:
            oct_3_mask = oct_3_mask + (2**diff)
            diff = diff + 1
    elif 16 > networkBits >= 8:
        diff = 16 - networkBits
        oct_1_mask = 255
        while diff < 8:
            oct_2_mask = oct_2_mask + (2**diff)
            diff = diff + 1
    elif 8 > networkBits:
        diff = 8 - networkBits
        while diff < 8:
            oct_1_mask = oct_1_mask + (2**diff)
            diff = diff + 1
    else:
        print("error determining subnet mask")
        
    subnet_mask = [oct_1_mask, oct_2_mask, oct_3_mask, oct_4_mask]
    return subnet_mask


# determine blockSize
def calc_block_size():
    if networkBits in (1, 9, 17, 25):
        block_size = 2**7
    elif networkBits in (2, 10, 18, 26):
        block_size = 2**6
    elif networkBits in (3, 11, 19, 27):
        block_size = 2**5
    elif networkBits in (4, 12, 20, 28):
        block_size = 2**4
    elif networkBits in (5, 13, 21, 29):
        block_size = 2**3
    elif networkBits in (6, 14, 22, 30):
        block_size = 2**2
    elif networkBits in (7, 15, 23, 31):
        block_size = 2**1
    else:
        block_size = 2 ** 8
    # print("error in determining block size")

    return block_size


# determine hosts per subnet
def calc_hosts_per_subnet():
    hosts_per_subnet = 2 ^ hostBits - 2

    return hosts_per_subnet


def calc_hosts_per_subnet_bb():
    hosts_per_subnet = 2 ** remainingHostBits - 2

    return hosts_per_subnet
# calculate Broadcast Address


def calc_broadcast_address():
    if (oct4 + hostsPerSubnet) <= 255:
        oct_4_bc = oct4 + hostsPerSubnet + 1
        oct_3_bc = oct3
        oct_2_bc = oct2
        oct_1_bc = oct1
    # if oct4 == 0:
    # oct_4_bc = oct_4_bc - 1
    else:
        oct_4_bc = 255
        oct_3_bc = oct3 + 1
        oct_2_bc = oct2
        oct_1_bc = oct1

    broadcast_address = [oct_1_bc, oct_2_bc, oct_3_bc, oct_4_bc]

    return broadcast_address


# calculate First Valid Host
def calc_first_valid_host():
    if oct4 < 255:
        oct_4_fvh = oct4 + 1
        oct_3_fvh = oct3
        oct_2_fvh = oct2
        oct_1_fvh = oct1
    elif oct4 == 255 and oct3 < 255:
        oct_4_fvh = 0
        oct_3_fvh = oct3 + 1
        oct_2_fvh = oct2
        oct_1_fvh = oct1
    elif oct3 == 255 and oct2 < 255:
        oct_4_fvh = 0
        oct_3_fvh = 0
        oct_2_fvh = oct2 + 1
        oct_1_fvh = oct1
    else:
        oct_4_fvh = 0
        oct_3_fvh = 0
        oct_2_fvh = 2
        oct_1_fvh = oct1 + 1
            
    first_valid_host = [oct_1_fvh, oct_2_fvh, oct_3_fvh, oct_4_fvh]
    return first_valid_host


# calculate Last Valid Host
def calc_last_valid_host():
    if oct4 < 255:
        oct_4_lvh = bCA[3] - 1
        oct_3_lvh = bCA[2]
        oct_2_lvh = oct2
        oct_1_lvh = oct1
    else:
        # elif oct4 == 255 and oct3 < 255:
        oct_4_lvh = bCA[3] - 1
        oct_3_lvh = oct3 + 1
        oct_2_lvh = oct2
        oct_1_lvh = oct1
        
    last_valid_host = [oct_1_lvh, oct_2_lvh, oct_3_lvh, oct_4_lvh]
    return last_valid_host


# determine random number of subnets (in range for ip) and # of bits to be borrowed to create them
# Num Sub Nets Borrowed Bits
def n_s_n_b_b():
    while True:
        num_subnets = random.randrange(3, 100)
        print("{}".format(num_subnets))
        if num_subnets <= 2:
            borrowed_bits = 1
        elif 2 < num_subnets <= 4:
            borrowed_bits = 2
        elif 4 < num_subnets <= 8:
            borrowed_bits = 3
        elif 8 < num_subnets <= 16:
            borrowed_bits = 4
        elif 16 < num_subnets <= 32:
            borrowed_bits = 5
        elif 32 < num_subnets <= 64:
            borrowed_bits = 6
        elif 64 < num_subnets <= 128:
            borrowed_bits = 7
        else:
            borrowed_bits = 8

            # make sure enough host bits are available to create n subnet masks so the
            # remainder of the questions can be answered
            # if not enough host bits are available start loop over to reset the number of subnet masks
            # this method works but can be very slow
            # this method makes me very sad
        
        if (hostBits - borrowed_bits) > 1:
            break

    return num_subnets, borrowed_bits


def calc_remaining_host_bits():
    remaining_host_bits = hostBits-borrowedBits

    return remaining_host_bits


# calc network address
def calc_network_address():
    network_address = subnet
    return network_address

# STARTING POINT FOR PROGRAM OUTPUT ##########


print("\nTo skip a question and reveal the solution type \"s\" \n\n")
print("**********************", ip, "**********************")

# Q1
binRep = to_binary()
q1 = Question(
    "What is the binary representation of the ip address above?",
    "{}".format(binRep),
    "refer to the division method OR subtraction method to convert each octet to binary\n\t{}".format(binRep))

# q1.present_question()

# Q2
subnetMask = calc_subnet_mask()
q2 = Question(
    "Write the subnet mask for this IP",
    "{}.{}.{}.{}".format(subnetMask[0], subnetMask[1], subnetMask[2], subnetMask[3]),
    "SNM = {}.{}.{}.{}".format(subnetMask[0], subnetMask[1], subnetMask[2], subnetMask[3])
    )

# q2.present_question()

# Q3
q3 = Question(
    "How many bits make up the network address?",
    networkBits,
    "{} network address bits. Indicated by the CIDR representation at the end of the ip".format(networkBits)
    )

# q3.present_question()

# Q4
q4 = Question(
    "How many bits make up the host address?",
    hostBits,
    "Host address bits = {}. 32 total bits in an ipv4 ip - the # of network bit = Host bits".format(hostBits)
    )

# q4.present_question()

# Q5
blockSize = calc_block_size()
q5 = Question(
    "What is the increment or block size of this subnet?",
    blockSize,
    "Block size = {}. Block size = value of the Least Significant Bit".format(blockSize)
    )

# q5.present_question()

# Q6
hostsPerSubnet = calc_hosts_per_subnet()
q6 = Question(
    "How many hosts can you have in this subnet?",
    hostsPerSubnet,
    "2^host bits - 1 network address - 1 broadcast address = {} possible hosts in this subnet.".format(hostsPerSubnet)
    )

# q6.present_question()

# Q7
q7 = Question(
    "What is the network address of this ip?",
    "{}.{}.{}.{}".format(oct1, oct2, oct3, oct4),
    "Network Address = {}.{}.{}.{}. the very first ip in the subnet block".format(oct1, oct2, oct3, oct4)
    )

# q7.present_question()

# Q8
bCA = calc_broadcast_address()
q8 = Question(
    "what is the broadcast address of the first subnet?",
    "{}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3]),
    "Broadcast address = {}.{}.{}.{}. the very last ip in the subnet block".format(bCA[0], bCA[1], bCA[2], bCA[3])
    )

# q8.present_question()

# Q9
fVH = calc_first_valid_host()
q9 = Question(
    "What is the first valid host address in this subnet?",
    "{}.{}.{}.{}".format(fVH[0], fVH[1], fVH[2], fVH[3]),
    "First valid host = {}.{}.{}.{}. the address following the network address".format(fVH[0], fVH[1], fVH[2], fVH[3])
    )

# q9.present_question()

# Q10
lVH = calc_last_valid_host()
q10 = Question(
    "What is the last valid host address in this subnet?",
    "{}.{}.{}.{}".format(lVH[0], lVH[1], lVH[2], lVH[3]),
    "Last valid host = {}.{}.{}.{}. the address preceding the broadcast address".format(lVH[0], lVH[1], lVH[2], lVH[3])
    )

# q10.present_question()

# randomize order of 1st 10 questions and remove questions post selection

prompts = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

random.shuffle(prompts)

for prompt in prompts:
    prompt.present_question()

# Questions past this point are presented in order
# Q11
numSubnets, borrowedBits = n_s_n_b_b()
q11 = Question(
    "You have been asked to create {} subnets. How many host bits do you need to borrow?".format(numSubnets),
    borrowedBits,
    "{} host bits need to be borrowed".format(borrowedBits).format(oct1, oct2, oct3, oct4)
    )

q11.present_question()

# Q12
remainingHostBits = calc_remaining_host_bits()
q12 = Question(
    "How many bits do you have left over for hosts?",
    remainingHostBits,
    "{} bits are left over for hosts".format(remainingHostBits)
    )

q12.present_question()

# Q13
# re-assign network bits and host bits
networkBits = networkBits + borrowedBits
# re-assign subnet mask
subnetMask = calc_subnet_mask()

q13 = Question(
    "What is the new subnet mask?",
    "{}.{}.{}.{}".format(subnetMask[0], subnetMask[1], subnetMask[2], subnetMask[3]),
    "New SNM = {}.{}.{}.{}".format(subnetMask[0], subnetMask[1], subnetMask[2], subnetMask[3])
    )

q13.present_question()

# Q14
q14 = Question(
    "What is the new CIDR notation (/XX)?",
    "/{}".format(networkBits),
    "CIDR address = /{}".format(networkBits)
    )

q14.present_question()

# Q15
maxSubnets = 2 ** borrowedBits

q15 = Question(
    "What is the max number of subnets supported by this mask?",
    maxSubnets,
    "{} max subnets could be supported".format(maxSubnets)
    )

q15.present_question()

# Q16
# re-assign block size
blockSize = calc_block_size()

q16 = Question(
    "What is the increment or block size of the new subnet?",
    blockSize,
    "Block size = {},".format(blockSize)
    )

q16.present_question()

# Q17
# re-assign possible hosts
hostsPerSubnet = calc_hosts_per_subnet_bb()
q17 = Question(
    "What is the max number of hosts per subnet?",
    hostsPerSubnet,
    "{} Hosts per subnet. 2 ^ host bits - 1 nw address - 1 bc address".format(hostsPerSubnet)
    )

q17.present_question()

print("*************** in the following questions write out information for the 1st 2 subnets ***************\n")

# Q18
q18 = Question(
    "What is the ID of the 1st subnet?",
    0,
    "1st ID = {}".format(0)
    )

q18.present_question()

# Q19
# calculate subnet # think something funny is going on here between subnet and network address
# subnet = [oct1, oct2, oct3, oct4]
# re-assign network address
networkAddress = calc_network_address()
# re-assign broadcast address
bCA = calc_broadcast_address()

q19 = Question(
    "What is the range of the 1st subnet mask??",
    "{}.{}.{}.{}-{}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3]),
    "Range = {}.{}.{}.{}-{}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3])
    )

q19.present_question()

# Q20
# call first valid host
firstValidHost = calc_first_valid_host()

q20 = Question(
    "What is the first valid host address in the 1st subnet?",
    "{}.{}.{}.{}".format(firstValidHost[0], firstValidHost[1], firstValidHost[2], firstValidHost[3]),
    "First valid host = {}.{}.{}.{}".format(firstValidHost[0], firstValidHost[1], firstValidHost[2], firstValidHost[3])
    )

q20.present_question()
# Q21
# call last valid host
lVH = calc_last_valid_host()
q21 = Question(
    "What is the last valid host address in the 1st subnet?",
    "{}.{}.{}.{}".format(lVH[0], lVH[1], lVH[2], lVH[3]),
    "Last valid host = {}.{}.{}.{}".format(lVH[0], lVH[1], lVH[2], lVH[3])
    )
q21.present_question()

# Q22
q22 = Question(
    "What is the broadcast address of the 1st subnet mask?",
    "{}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3]),
    "broadcast = {}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3])
    )

q22.present_question()

print("***************************************************")
print("\tRange = {}.{}.{}.{}-{}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3]))
print("\tFirst valid host = {}.{}.{}.{}".format(fVH[0], fVH[1], fVH[2], fVH[3]))
print("\tLast valid host = {}.{}.{}.{}".format(lVH[0], lVH[1], lVH[2], lVH[3]))
print("\tbroadcast = {}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3]))
print("***************************************************\n")

# round 2 of subnet masks #################################################

# Q23 2nd subnet range /////strip()?s
# have not figured out how to turn this in to function as it changes multiple variables
if bCA[3] == 255:
    oct1 = bCA[0]
    oct2 = bCA[1]
    oct3 = bCA[2] + 1
    oct4 = 0
elif bCA[3] < 255 and bCA[2] < 255:
    oct1 = bCA[0]
    oct2 = bCA[1]
    oct3 = bCA[2]
    oct4 = bCA[3] + 1
networkAddress = subnet

bCA = calc_broadcast_address()
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Q23
q23 = Question(
    "What is the range of the 2nd subnet mask?",
    "{}.{}.{}.{} - {}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3]),
    "Range = {}.{}.{}.{}-{}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3])
    )

q23.present_question()

# Q24
firstValidHost = calc_first_valid_host()

q24 = Question(
    "What is the first valid host address in the 2nd subnet?",
    "{}.{}.{}.{}".format(firstValidHost[0], firstValidHost[1], firstValidHost[2], firstValidHost[3]),
    "First valid host = {}.{}.{}.{}".format(firstValidHost[0], firstValidHost[1], firstValidHost[2], firstValidHost[3])
    )

q24.present_question()

# Q25
lastValidHost = calc_last_valid_host()

q25 = Question(
    "What is the last valid host address in the 2nd subnet??",
    "{}.{}.{}.{}".format(lastValidHost[0], lastValidHost[1], lastValidHost[2], lastValidHost[3]),
    "Last valid host = {}.{}.{}.{}".format(lastValidHost[0], lastValidHost[1], lastValidHost[2], lastValidHost[3])
    )

q25.present_question()

# Q26
q26 = Question(
    "What is the broadcast address of the 2nd subnet mask?",
    "{}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3]),
    "broadcast = {}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3])
    )

q26.present_question()

print("***************************************************")
print("\tRange = {}.{}.{}.{}-{}.{}.{}.{}".format(oct1, oct2, oct3, oct4, bCA[0], bCA[1], bCA[2], bCA[3]))
print("\tFirst valid host = {}.{}.{}.{}".format(fVH[0], fVH[1], fVH[2], fVH[3]))
print("\tLast valid host = {}.{}.{}.{}".format(lVH[0], lVH[1], lVH[2], lVH[3]))
print("\tbroadcast = {}.{}.{}.{}".format(bCA[0], bCA[1], bCA[2], bCA[3]))
print("***************************************************\n")


stop = time.time()
completion_time = stop - start
time_convert(completion_time)

sys.exit()
