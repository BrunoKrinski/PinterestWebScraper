<h1>Pinterest Web Scraper</h1>

<h2>Installation:</h2>

<h3>Create the enviroment:</h3>
conda create -n pws python=3.9

<h3>Install dependencies:</h3>
<p>pip install selenium<br>
pip install chromedriver_autoinstaller<br>
pip install wget<br>
pip install opencv-python</p>

<p>or run:</p>

<p>pip install -r requeriments.txt</p>

<h3>Execute:</h3>
<p>python main.py --email "your email" --password "your password" --link "pinterest link"</p>

<p>or</p>

<p>python main.py --email "your email" --password "your password" --list "txt file with a list of pinterest links"</p>