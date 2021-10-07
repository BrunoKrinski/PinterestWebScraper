<h1>Pinterest Web Scraper</h1>

<h2>Installation:</h2>

<h3>Create the enviroment</h3>
conda create -n pws python=3.9

<h3>Install dependencies</h3>
pip install selenium
pip install chromedriver_autoinstaller
pip install wget
pip install opencv-python

or run:

pip install -r requeriments.txt

<h3>Execute:</h3>
python main.py --email "your email" --password "your password" --link "pinterest link"

or

python main.py --email "your email" --password "your password" --list "txt file with a list of pinterest links"