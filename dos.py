from flask import Flask, render_template, send_file, request, redirect
import socket
import os


NAME = []
FILES = []
app = Flask(__name__)


class System():
    currentFolder = os.path.split(os.path.abspath(__file__))[0]
    html = """ <!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <title>Your space</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
      </head>
      <body>
        <p><h3>Now online (ip): {%for p in NAME%}{{p}}, {%endfor%}</h3></p>
        <div class="container-fluid shadow w-50">
          <form align='center' action="/files" method="post" enctype="multipart/form-data">
            <input type="file" class='m-5' name="file" value="">
            <input type="submit" class='ml-5' name="" value="Submit">
          </form>
        </div>
        <a href="/download" class='mt-5'>Download the server</a>
      </body>
    </html>
    """

    def create_folder(self, name='Multiverse folder'):
        if name not in os.listdir(self.currentFolder):
            os.mkdir(name)
        FOLDER = os.path.join(self.currentFolder, name)
        app.config['UPLOAD_FOLDER'] = FOLDER

    def site(self):
        if 'templates' not in os.listdir():
            os.mkdir('templates')
            os.chdir('templates')
            with open('main.html', 'w+') as file:
                file.write(self.html)
                file.close()

    def getip(self):
        import netifaces
        adr = netifaces.ifaddresses('en0')
        address = adr[netifaces.AF_INET][0]['addr']
        del netifaces
        return address

    def gmf(self):
        if 'Multiverse folder' in os.listdir():
            os.chdir('Multiverse folder')
            f = os.listdir()
            for file in f:
                if file not in FILES:
                    FILES.append(file)
            os.chdir('..')
            return FILES


@app.route('/')
def main():
    sys = System()
    sys.create_folder()
    if request.remote_addr not in NAME:
        NAME.append(request.remote_addr)
    files = sys.gmf()
    return render_template('main.html', NAME=NAME, filesfold=files)


@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect('http://{}:5000'.format(ip))


@app.route('/download')
def download():
    file =  os.path.join(System().currentFolder, __file__)
    return send_file(file, as_attachment=True)


@app.route('/<f>')
def filedownload(f):
    fd = os.path.join(System().currentFolder, app.config['UPLOAD_FOLDER'], f)
    return send_file(fd, as_attachment=True)


sys = System()
sys.site()
ip = sys.getip()


app.run(host=ip)
