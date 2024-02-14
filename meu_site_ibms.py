from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Função para gerar os quadros do vídeo
def gen_frames():
    video_capture = cv2.VideoCapture(0)  # Inicializa a captura de vídeo

    while True:
        success, frame = video_capture.read()  # Lê um quadro do vídeo

        if not success:
            break
        else:
            # Codifica o frame como JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define a rota para o streaming de vídeo
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Define a rota para a página inicial
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/contatos")
def contatos():
    return render_template("contatos.html")

@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)

if __name__ == "__main__":
    app.run(debug=True)
