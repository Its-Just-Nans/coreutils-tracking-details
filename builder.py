import json
from pathlib import Path


# Function to generate the HTML content
def generate_html(data):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid #ccc;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        .pass {
            background-color: #d4edda;
        }
        .fail {
            background-color: #f8d7da;
        }
        .skip {
            background-color: #fff3cd;
        }
        #all:checked ~ table tr {
            display: table-row;
        }
        #pass:checked ~ table tr.fail, #pass:checked ~ table tr.skip {
            display: none;
        }
        #fail:checked ~ table tr.pass, #fail:checked ~ table tr.skip {
            display: none;
        }
        #skip:checked ~ table tr.pass, #skip:checked ~ table tr.fail {
            display: none;
        }
    </style>
</head>
<body>
    <h1>Test Results</h1>
    <input type="radio" id="all" name="show" checked/>
    <label for="all">All</label>
    <input type="radio" id="pass" name="show" />
    <label for="pass">Pass</label>
    <input type="radio" id="fail" name="show" />
    <label for="fail">Fail</label>
    <input type="radio" id="skip" name="show" />
    <label for="skip">Skip</label>
    <table>
        <thead>
            <tr>
                <th>Category</th>
                <th>Log File</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
"""

    for category, logs in data.items():
        for log_file, status in logs.items():
            status_class = status.lower()  # use status as class for styling
            html_content += f"""
            <tr class="{status_class}">
                <td>{category}</td>
                <td>{log_file}</td>
                <td>{status}</td>
            </tr>
"""
    html_content += """
        </tbody>
    </table>
</body>
</html>
"""
    return html_content


if __name__ == "__main__":
    json_data = json.loads(Path("gnu-full-result.json").read_text())
    html_content = generate_html(json_data)

    # Write the HTML content to an index.html file
    output_path = Path("index.html")
    output_path.write_text(html_content)
