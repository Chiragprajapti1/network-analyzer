
from flask import Flask, render_template, request, Response, redirect, url_for
import csv, io, os
from werkzeug.utils import secure_filename
from scanner.scanner import scan_network, last_results
from deduplicator import remove_duplicates

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    def get_local_ip():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    results = None
    if request.method == 'POST':
        ip_range = request.form['ip_range']
        if ip_range == "auto":
            ip = get_local_ip()
            ip_range = ".".join(ip.split('.')[:3]) + ".0/24"
        results = scan_network(ip_range)
    return render_template('scanner.html', results=results)

@app.route('/download_csv')
def download_csv():
    from scanner.scanner import last_results
    import io, csv
    if not last_results:
        return "No data available", 400

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['IP Address', 'Status', 'Port', 'Protocol'])

    for row in last_results:
        writer.writerow([row['ip'], row['state'], row['port'], row['protocol']])

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=scan_results.csv"}
    )



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    cleaned = False
    if request.method == 'POST':
        file = request.files['report']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "cleaned_" + filename)
            remove_duplicates(file_path, output_path)
            return redirect(url_for('download_cleaned', filename="cleaned_" + filename))
    return render_template('upload.html', cleaned=cleaned)

@app.route('/download_cleaned/<filename>')
def download_cleaned(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(path, 'r') as f:
        data = f.read()
    return Response(data, mimetype="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == '__main__':
    app.run(debug=True)
