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
    </style>
</head>
<body>
    <h1>Test Results</h1>
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
