import sys, time, csv

iana_protocols = {
    1: "icmp",
    6: "tcp",
    17: "udp",
    41: "ipv6",
    50: "esp",
    51: "ah",
    58: "ipv6-icmp",
    103: "pim",
    132: "sctp",
    141: "wesp"
}

def read_lookup(file_path):
    lookup_table = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                port, protocol, tag = row
                lookup_table[int(port), protocol.lower()] = tag.strip()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return lookup_table

# Assuming flow logs are all v2 and have required fields
# https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields
def read_file_lines(file_path, lookup_table):
    tag_counts = {}
    port_protocol = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split() # Break line into individual fields
                dstport = int(parts[6])
                dec_prot = int(parts[7])
                # convert decimal to keyword
                if dec_prot in iana_protocols:
                    protocol = iana_protocols[dec_prot] 
                else:
                    protocol = "unknown"
                port_protocol[dstport, protocol] = port_protocol.get((dstport, protocol), 0) + 1 # Count the unique port and protocol combos
                
                # Use port and protocol to count combos on lookup table
                if (dstport, protocol) in lookup_table:
                    tag = lookup_table[(dstport, protocol)]
                else:
                    tag = "Untagged"
                tag_counts[tag] = tag_counts.get(tag, 0) + 1    
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return tag_counts, port_protocol

def write_output(output_file, tag_counts, port_protocol_counts):
    try:
        with open(output_file, "w") as output:
            output.write("Tag,Counts\n")
            for (tag, count) in tag_counts.items():
                output.write(f"{tag},{count}\n")
            output.write("\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_counts.items():
                output.write(f"{port},{protocol},{count}\n") 
    except IOError as e:
        print(f"An I/O error occurred: {e}")  
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  


def main(input_file, lookup_file):
    start_time = time.perf_counter()
    print(f"Processing input file: {input_file} and lookup file: {lookup_file}")
    lookup_table = read_lookup(lookup_file)
    print("Successfully parsed lookup table")
    
    tag_counts, port_protocol = read_file_lines(input_file, lookup_table)
    print("Successfully parsed input file")

    write_output("output.csv", tag_counts, port_protocol)
    end_time = time.perf_counter() - start_time
    print(f"Successfully wrote to outputfile in: {end_time:.2f} seconds.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python your_script.py <input_file> <lookup_file>")
        sys.exit(1)  # Exit with an error code

    input_file = sys.argv[1]
    lookup_file = sys.argv[2]

    main(input_file, lookup_file)