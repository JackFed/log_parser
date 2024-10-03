# Log Parser
This Python script is designed to parse AWS VPC Flow Logs version 2, extracting relevant fields, and generating an output summary.

## Project description
Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag. The dstport and protocol combination decide what tag can be applied.

## Usage Instructions

1. **Prepare the Input File:**
   - Ensure your input file is named `input.txt` and is formatted correctly. Each line should follow the structure:
   "&lt;version&gt; &lt;account-id&gt; &lt;interface-id&gt; &lt;srcaddr&gt; &lt;dstaddr&gt; &lt;srcport&gt; &lt;dstport&gt; &lt;protocol&gt; &lt;packets&gt; &lt;bytes&gt; &lt;start&gt; &lt;end&gt; &lt;action&gt; &lt;log-status&gt;"

2. **Run the Script:**
   - Execute the script in your terminal or command prompt. Use the following command:
     ```bash
     python log_parser.py <input-file.txt> <lookup-file.csv> <output-file.csv>
     ```

3. **Output:**
   - After the script runs successfully, check for a csv file with the specified name you gave in the same directory. This file will contain the parsed log data, organized by tags and counts, as well as the port and protocol combinations.

## Assumptions:
- The input logs are in AWS VPC Flow Logs version 2 format.
- Log inputs are provided in a `.txt` file.
- Each log record follows the format: "&lt;version&gt; &lt;account-id&gt; &lt;interface-id&gt; &lt;srcaddr&gt; &lt;dstaddr&gt; &lt;srcport&gt; &lt;dstport&gt; &lt;protocol&gt; &lt;packets&gt; &lt;bytes&gt; &lt;start&gt; &lt;end&gt; &lt;action&gt; &lt;log-status&gt;".
- output written to a `.csv` file.