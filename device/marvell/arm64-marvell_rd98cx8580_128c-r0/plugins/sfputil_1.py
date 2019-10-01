#!/usr/bin/env python

try:
    import os
    import time
    import re
    from sonic_sfp.sfputilbase import SfpUtilBase
except ImportError, e:
    raise ImportError (str(e) + "-required module not found")

smbus_present = 1
line_card_number = 0
per_line_card_port_number = 0

try:
    import smbus
except ImportError, e:
    smbus_present = 0

class SfpUtil(SfpUtilBase):
    """Platform specific sfputil class"""
    _port_start = 1
    _port_end = 128
    ports_in_block = 128

    _port_to_eeprom_mapping = {}
    port_to_i2c_mapping = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
        9 : 0,
        10 : 0,
        11 : 0,
        12 : 0,
        13 : 0,
        14 : 0,
        15 : 0,
        16 : 0,
        17 : 0,
        18 : 0,
        19 : 0,
        20 : 0,
        21 : 0,
        22 : 0,
        23 : 0,
        24 : 0,
        25 : 0,
        26 : 0,
        27 : 0,
        28 : 0,
        29 : 0,
        30 : 0,
        31 : 0,
        32 : 0,
        33 : 0,
        34 : 0,
        35 : 0,
        36 : 0,
        37 : 0,
        38 : 0,
        39 : 0,
        40 : 0,
        41 : 0,
        42 : 0,
        43 : 0,
        44 : 0,
        45 : 0,
        46 : 0,
        47 : 0,
        48 : 0,
        49 : 0,
        50 : 0,
        51 : 0,
        52 : 0,
        53 : 0,
        54 : 0,
        55 : 0,
        56 : 0,
        57 : 0,
        58 : 0,
        59 : 0,
        60 : 0,
        61 : 0,
        62 : 0,
        63 : 0,
        64 : 0,
        65 : 0,
        66 : 0,
        67 : 0,
        68 : 0,
        69 : 0,
        70 : 0,
        71 : 0,
        72 : 0,
        73 : 0,
        74 : 0,
        75 : 0,
        76 : 0,
        77 : 0,
        78 : 0,
        79 : 0,
        80 : 0,
        81 : 0,
        82 : 0,
        83 : 0,
        84 : 0,
        85 : 0,
        86 : 0,
        87 : 0,
        88 : 0,
        89 : 0,
        90 : 0,
        91 : 0,
        92 : 0,
        93 : 0,
        94 : 0,
        95 : 0,
        96 : 0,
        97 : 0,
        98 : 0,
        99 : 0,
        100 : 0,
        101 : 0,
        102 : 0,
        103 : 0,
        104 : 0,
        105 : 0,
        106 : 0,
        107 : 0,
        108 : 0,
        109 : 0,
        110 : 0,
        111 : 0,
        112 : 0,
        113 : 0,
        114 : 0,
        115 : 0,
        116 : 0,
        117 : 0,
        118 : 0,
        119 : 0,
        120 : 0,
        121 : 0,
        122 : 0,
        123 : 0,
        124 : 0,
        125 : 0,
        126 : 0,
        127 : 0,
        128 : 0
    }
    _qsfp_ports = range(_port_start, ports_in_block + 1)
  
    def __init__(self):
    # Should write

    def reset(self, port_num):
    # Should write

    def set_low_power_mode(self, port_nuM, lpmode):
        raise NotImplementedError

    def get_low_power_mode(self, port_num):
        raise NotImplementedError

    def i2c_get(self, device_addr, offset)
        if smbus_present == 0:
            cmdstatus, status = cmd.getstatusoutput('i2cget -y 0 device_addr offset')
            status = int(status, 16)
        else:
            bus = smbus.SMBus(0)
            status = bus.read_byte_data(device_addr, offset)
        return status

    def i2c_set(self, device_addr, offset, value)
        if smbus_present == 0:
            os.system(i2cset -y 0 device_addr offset value)
        else:
            bus = smbus.SMBus(0)
            bus.write_byte_data(device_addr, offset, value)

    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self._port_start or port_num > self._port_end:
            return False

        #Get the line card number and per_line_card port number
        per_line_card_port_number = portnum%16
        if per_line_card_port_number == 0:
            per_line_card_port_number = 16
        
        if per_line_card_port_number == 16:
            line_card_number = portnum/16 - 1
        else:
            line_card_number = portnum/16
   
        # Check for line_card status
        line_card_status = self.i2c_get( 0x76, 0x3)
          
        res = 1
        res = res << line_card_number
        if ((line_card_status & res) != res):
            return False
  
        else:
            self.i2c_set(0x76, 0x0d, 0x80)
            line_card_reg_addr_str = "0x" + str(line_card_number) + "0"
            line_card_reg_addr = int(line_card_reg_addr_str, 16)
            self.i2c_set(0x76, 0xe, hex(line_card_reg_addr))


            if per_line_card_port_number <= 8:
                portstatus = self.i2c_get(0x74, 0x4)
            else:
                portstatus = self.i2c_get(0x74, 0x5)
   
            bit_shift = (per_line_card_port_number-1)%8
            res = 1
            res = res << bit_shift
            if (portstatus & res == res):
                return True
            return False
 
    def read_porttab_mappings(self, porttabfile):
        logical = []
        logical_to_bcm = {}
        logical_to_physical = {}
        physical_to_logical = {}
        last_fp_port_index = 0
        last_portname = ""
        first = 1
        port_pos_in_file = 0
        parse_fmt_port_config_ini = False

        try:
            f = open(porttabfile)
        except:
            raise

        parse_fmt_port_config_ini = (os.path.basename(porttabfile) == "port_config.ini")

        # Read the porttab file and generate dicts
        # with mapping for future reference.
        #
        # TODO: Refactor this to use the portconfig.py module that now
        # exists as part of the sonic-config-engine package.
        title = []
        for line in f:
            line.strip()
            if re.search("^#", line) is not None:
                # The current format is: # name lanes alias index speed
                # Where the ordering of the columns can vary
                title = line.split()[1:]
                continue
            
            # Parsing logic for 'port_config.ini' file
            if (parse_fmt_port_config_ini):
                # bcm_port is not explicitly listed in port_config.ini format
                # Currently we assume ports are listed in numerical order according to bcm_port
                # so we use the port's position in the file (zero-based) as bcm_port
                portname = line.split()[0]

                bcm_port = str(port_pos_in_file)
                #print("portname " + portname)

                if "index" in title:
                    fp_port_index = int(line.split()[title.index("index")])
                # Leave the old code for backward compatibility
                elif len(line.split()) >= 4:
                    fp_port_index = int(line.split()[3])
                else:
                    fp_port_index = portname.split("Ethernet").pop()
                    fp_port_index = int(fp_port_index.split("s").pop(0))+1
                    #print(fp_port_index)
            else:  # Parsing logic for older 'portmap.ini' file
                (portname, bcm_port) = line.split("=")[1].split(",")[:2]

                fp_port_index = portname.split("Ethernet").pop()
                fp_port_index = int(fp_port_index.split("s").pop(0))+1

            if ((len(self.sfp_ports) > 0) and (fp_port_index not in self.sfp_ports)):
                continue
     
            if first == 1:
                # Initialize last_[physical|logical]_port
                # to the first valid port
                last_fp_port_index = fp_port_index
                last_portname = portname
                first = 0

            logical.append(portname)

            logical_to_bcm[portname] = "xe" + bcm_port
            logical_to_physical[portname] = [fp_port_index]
            if physical_to_logical.get(fp_port_index) is None:
                physical_to_logical[fp_port_index] = [portname]
            else:
                physical_to_logical[fp_port_index].append(
                    portname)

            if (fp_port_index - last_fp_port_index) > 1:
                # last port was a gang port
                for p in range(last_fp_port_index+1, fp_port_index):
                    logical_to_physical[last_portname].append(p)
                    if physical_to_logical.get(p) is None:
                        physical_to_logical[p] = [last_portname]
                    else:
                        physical_to_logical[p].append(last_portname)

            last_fp_port_index = fp_port_index
            last_portname = portname

            port_pos_in_file += 1

        self.logical = logical
        self.logical_to_bcm = logical_to_bcm
        self.logical_to_physical = logical_to_physical
        self.physical_to_logical = physical_to_logical

    @property
    def port_start(self):
        return self._port_start

    @property
    def port_end(self):
        return self._port_end

    @property
    def qsfp_ports(self):
        return self._qsfp_ports

    @property
    def port_to_eeprom_mapping(self):
         return self._port_to_eeprom_mapping

    @property
    def get_transceiver_change_event(self):
        raise NotImplementedError
                                           
