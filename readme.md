# Python YouTube Video Frame Capturer

## Descrição
Este script permite transformar os frames de um vídeo do Youtube em uma sequência de imagens.

## Instalação

É recomendada a criação de um ambiente virtual local com nome "env"

~~~
python -m venv env
~~~

e a instalação das bibliotecas necessárias (YT_DLP e Python-OpenCV)

~~~
pip install yt-dlp opencv-python
~~~

ou 
~~~
pip install -r requirements.txt
~~~

> É necessário ter instalado o FFmpeg no computador. Baixe-o pelo link <https://www.ffmpeg.org/download.html> e siga os passos para instalação.

## Configurações
Abra o arquivo `yt_capture.py` e modifique os valores
~~~python
video_url = "url de um vídeo do youtube"
interval = 5 # diferença de tempo (em segundos) entre as capturas
start_time = 20 # posição (em segundos) da primeira captura
end_time = 67 # limite de parada (em segundos). 0 ou valores negativos, limite passa a ser a duração do próprio vídeo
~~~

## Executar
para salvar as capturas, execute o comando abaixo:
~~~
python yt_capture.py
~~~

As imagens ficarão salvas na pasta `captures` numa subpasta com nome igual ao ID do vídeo do Youtube

## Notas Adicionais
As capturas geralmente são feitas seguindo os passos:
- `cap.set(cv.CAP_PROP_POS_FRAMES, frame)` para posicionar o cursor da captura no frame correto
- `ret, frame = cap.read()` para guardar os dados da imagem na variável `frame`
- `cv.imwrite(filename)` para salvar a imagem

Porém, o método `cap.set()` é bastante custoso e tende a deixar o processo lento.
Por isso, escolhi usar o método `cap.grab()` que simplesmenta avança o cursor da captura para o próximo frame várias vezes até que chegue ao frame correto.
Esse processo torna a execução muito mais rápida.