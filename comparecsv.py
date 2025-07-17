iimport csv

# Read the nonprod file and create a dictionary with the appname as key
def read_nonprod_file(file_path):
    nonprod_data = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Assuming the appname is in the second column (index 1)
            appname = row[1]
            nonprod_data[appname] = row
    return nonprod_data

# Compare prod and nonprod files, generate the output
def compare_and_generate_output(nonprod_file, prod_file):
    nonprod_data = read_nonprod_file(nonprod_file)
    output_rows = []

    with open(prod_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            appname = row[1]
            if appname in nonprod_data:
                nonprod_row = nonprod_data[appname]

                # Build the output format as described
                nonprod_appname = nonprod_row[1]
                nonprod_zip = nonprod_row[4]
                prod_appname = row[1]
                prod_zip = row[4]
                sit_blue = nonprod_row[2] + '-' + nonprod_row[3] + '-' + nonprod_zip
                prod_info = row[2] + '-' + row[3] + '-' + prod_zip

                output_rows.append([nonprod_appname, sit_blue, prod_info])

    return output_rows

# Function to write the output to a new CSV file
def write_output(output_rows, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(output_rows)

# Example usage
nonprod_file = 'nonprod.csv'
prod_file = 'prod.csv'
output_file = 'output.csv'

output_rows = compare_and_generate_output(nonprod_file, prod_file)
write_output(output_rows, output_file)

# Print the result for preview
for row in output_rows:
    print(row)


import csv

# Read the nonprod file and create a dictionary with the appname as key
def read_nonprod_file(file_path):
    nonprod_data = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            appname = row[1]
            nonprod_data[appname] = row
    return nonprod_data

# Compare prod and nonprod files, generate the output
def compare_and_generate_output(nonprod_file, prod_file):
    nonprod_data = read_nonprod_file(nonprod_file)
    output_rows = []

    with open(prod_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            appname = row[1]
            if appname in nonprod_data:
                nonprod_row = nonprod_data[appname]

                # Build the output format as described
                nonprod_appname = nonprod_row[1]
                nonprod_zip = nonprod_row[4]
                prod_appname = row[1]
                prod_zip = row[4]
                sit_blue = nonprod_row[2] + '-' + nonprod_row[3] + '-' + nonprod_zip
                prod_info = row[2] + '-' + row[3] + '-' + prod_zip

                output_rows.append([nonprod_appname, sit_blue, prod_info, nonprod_zip, prod_zip])

    return output_rows

# Function to write the output to an HTML file
def write_html_report(output_rows, output_file):
    html = """
    <html>
    <head>
        <style>
            table {width: 100%; border-collapse: collapse;}
            table, th, td {border: 1px solid black;}
            th, td {padding: 8px; text-align: left;}
            .same-zip {background-color: #ffcccb;}  /* Red background for same zip */
        </style>
    </head>
    <body>
        <h1>Comparison Report</h1>
        <table>
            <thead>
                <tr>
                    <th>App Name</th>
                    <th>SIT/BLUE</th>
                    <th>PROD</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for row in output_rows:
        nonprod_appname, sit_blue, prod_info, nonprod_zip, prod_zip = row
        
        # Apply color if the ZIP files are the same
        row_class = "same-zip" if nonprod_zip == prod_zip else ""
        
        html += f"""
        <tr class="{row_class}">
            <td>{nonprod_appname}</td>
            <td>{sit_blue}</td>
            <td>{prod_info}</td>
        </tr>
        """
    
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)

# Example usage
nonprod_file = 'nonprod.csv'
prod_file = 'prod.csv'
output_file = 'comparison_report.html'

output_rows = compare_and_generate_output(nonprod_file, prod_file)
write_html_report(output_rows, output_file)

print(f"HTML report generated: {output_file}")


#######################
import csv

def read_csv(file_path):
    """Reads the CSV file and returns a list of rows."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

def process_files(nonprod_file, prod_file):
    """Processes the nonprod and prod CSV files and generates the output."""
    nonprod_data = read_csv(nonprod_file)
    prod_data = read_csv(prod_file)
    
    result = []

    # Iterate through each row in prod.csv
    for prod_row in prod_data:
        prod_appname = prod_row[1]  # Extract APPNAME from prod file (second column)
        prod_filename = prod_row[4]  # Extract the filename from prod file (fifth column)
        prod_location = prod_row[3]  # Extract location from prod file (fourth column)
        
        # Find matching row in nonprod.csv
        for nonprod_row in nonprod_data:
            nonprod_appname = nonprod_row[1]  # Extract APPNAME from nonprod file (second column)
            nonprod_filename = nonprod_row[4]  # Extract the filename from nonprod file (fifth column)
            nonprod_location = nonprod_row[3]  # Extract location from nonprod file (fourth column)

            # If APPNAME matches between prod and nonprod, create the output row
            if prod_appname == nonprod_appname:
                # Format the combined output
                nonprod_combined = f"SIT-BLUE-{nonprod_filename}"
                prod_combined = f"PROD-{prod_location}-{prod_filename}"
                
                result.append([nonprod_row[0], nonprod_appname, nonprod_combined, prod_combined])

    return result

def write_output(output_file, data):
    """Writes the processed data to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Example usage
nonprod_file = 'nonprod.csv'
prod_file = 'prod.csv'
output_file = 'output.csv'

result = process_files(nonprod_file, prod_file)
write_output(output_file, result)

# Optionally, print the result to console
for row in result:
    print(row)





- name: Start async script
  shell: ./command.sh ALL
  args:
    chdir: /path/to/script
  async: 600
  poll: 0
  register: async_result

- name: Wait for script to finish and get output
  async_status:
    jid: "{{ async_result.ansible_job_id }}"
  register: job_status
  until: job_status.finished
  retries: 10
  delay: 5

- name: Print stdout lines
  debug:
    var: job_status.stdout_lines