<pre>This script creates a web application based on Flask and Flask-SocketIO. Here's how it works using HTML:

1. The necessary modules are imported: Flask, SocketIO, requests, and os.
2. The Flask application is instantiated and SocketIO is initialized.
3. The list of platforms to search by nickname is defined.
   The / route handles both GET and POST requests:
       If it is a POST request, the nickname is extracted from the form.
      The nickname is checked on the specified platforms.
      The results are saved to a file.
4. The logs are sent to the client using SocketIO.

If it is a GET request, the nickname input form and the log block are displayed.</pre>
<pre>



Install:
1. <p>git clone https://github.com/BYxarek/Search-nicknames.git</p>
2. <p>cd Search-nicknames</p>
3. <p>pip install -r requirements.txt</p>
</pre>
