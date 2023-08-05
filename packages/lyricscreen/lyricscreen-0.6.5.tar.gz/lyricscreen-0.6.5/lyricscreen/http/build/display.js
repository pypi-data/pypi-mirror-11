(function(){

	function print(s) {
		// console.log(s);
	}

	if (typeof window.dbg_print !== "undefined") {
		print = window.dbg_print;
	}

	function clearText() {
		var slides = document.getElementById("display");
		while (slides.firstChild) {
			slides.removeChild(slides.firstChild);
		}
	}

	function errorText() {
		clearText();
		var slides = document.getElementById("display");
		slides.innerHTML = '<li class="slide active error">&times;</li>';
	}

	function setText(text) {
		clearText();
		var slides = document.getElementById("display");
		slides.innerHTML = '<li class="basic slide active"><span class="content">' + text + '</span></li>';
	}

	print("Display: Initializing...")
	var connString = window.location.host.split(":")[0] + ":8417/display"
	var sock = new WebSocket("ws://" + connString);
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

		if (e.data.substring(0, 6) == "display refresh ") {
			setText(e.data.substring(6).trim());
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
		console.log("Close", e);
		errorText();
	};

	window.onbeforeunload = function() {
		if (sock.readyState < 2) {
			sock.close();
		}
	};

}());
