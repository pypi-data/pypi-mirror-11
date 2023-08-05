(function(){

    sock = {};
    var slides = document.getElementById("display");

    // For old debug purposes
	function print(s) {
		// console.log(s);
	}

    // Give us a global debug print function for use in devtools
	if (typeof window.dbg_print !== "undefined") {
		print = window.dbg_print;
	}

    // Clear the display
	function clearText() {
		while (slides.firstChild) {
			slides.removeChild(slides.firstChild);
		}
	}

    // Set our error display
	function errorText() {
		clearText();
		slides.innerHTML = '<li class="slide active error">&times;</li>';
	}

    // Set the display text
	function setText(text) {
		clearText();
		slides.innerHTML = '<li class="basic slide active"><span class="content">' + text + '</span></li>';
	}

    // Connect to server 
    function connect(host, port) {
        if (typeof host == "undefined") {
            host = window.location.host.split(":")[0];
        } 
        if (typeof port == "undefined") { 
            port = 8417;
        }
        var connString = host + ":" + port + "/display";
        if (typeof sock == "WebSocket") {
            sock.dontReconnect = true;
            sock.close();
        }
        sock = new WebSocket("ws://" + connString);
        print("Display: Connecting to ws://" + connString + "...")

        sock.onopen = function(e) {
            print("Display: Connected.");
            print("Open", e);
            clearText();
        };

        sock.onmessage = function(e) {
            if (e.data.substring(0, 6) == "slide:") {
                setText(e.data.substring(6).trim());
            }

            if (e.data.substring(0, 16) == "display refresh ") {
                setText(e.data.substring(16).trim());
            }
        }

        sock.onerror = function(e) {
            errorText();
        };

        sock.onclose = function(e) {
            switch (e.code) {
                case 1006:
                    print("Display: Failed to connect.");
                    break;
                case 1000: 
                    print("Display: Connection closed.");
                    break;
            }
            errorText();
            if (sock.dontReconnect === true) { 
            } else {
                setTimeout(function() { connect(host, port); }, 5000);
            }
        };
    }

	window.onbeforeunload = function() {
		if (sock.readyState < 2) {
			sock.close();
		}
	};

    print("Display: Initializing...");
    connect();

}());
