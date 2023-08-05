(function(){

	/* Utility Functions */

	// String startsWith stupidity until ECMAScript 6 saves us all
	var stringStartsWith = function(str, substr) {
		return str.substring(0, substr.length) == substr;
	};

	var keyCodeNames = ["[NUL]", "???", "???", "[Cancel]", "???", "???", "[Help]", "???",
		"Backspace", "Tab", "???", "???", "[CLR]", "Enter", "Return", "???",
		"Shift", "Control", "Alt", "Pause", "Caps Lock",
		"KANA", "EISU", "JUNJA", "FINAL", "HANJA", "???",
		"Escape", "[CNV]", "[NCNV]", "[ACPT]", "[MDCH]", "Space", "Page Up",
		"Page Down", "End", "Home", "Left", "Up", "Right", "Down", "Select",
		"Print", "Execute", "Print Screen", "Insert", "Delete", "???",
		"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
		":", ";", "<", "=", ">", "?", "@",
		"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
		"O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
		"Windows", "???", "Menu", "???", "Sleep",
		"Numpad 0", "Numpad 1", "Numpad 2", "Numpad 3", "Numpad 4",
		"Numpad 5", "Numpad 6", "Numpad 7", "Numpad 8", "Numpad 9",
		"Numpad *", "Numpad +", "???", "Numpad -", "Numpad .", "Numpad /",
		"F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
		"F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19",
		"F20", "F21", "F22", "F23", "F24",
		"???", "???", "???", "???", "???", "???", "???", "???",
		"Num Lock", "Scroll Lock",
		"WIN_OEM_FJ_JISHO", "WIN_OEM_FJ_MASSHOU", "WIN_OEM_FJ_TOUROKU",
		"WIN_OEM_FJ_LOYA", "WIN_OEM_FJ_ROYA",
		"???", "???", "???", "???", "???", "???", "???", "???", "???",
		"^", "!", "\"", "#", "$", "%", "&", "_", "(", ")", "*", "+", "|",
		"-", "{", "}", "~",
		"???", "???", "???", "???",
		"Volume Mute", "Volume Down", "Volume Up",
		"???", "???",
		";", "=", ",", "-", ".", "/", "\\",
		"???", "???", "???", "???", "???", "???", "???", "???", "???", "???",
		"???", "???", "???", "???", "???", "???", "???", "???", "???", "???",
		"???", "???", "???", "???", "???", "???",
		"[", "\\", "]", "'", "???", "Meta", "AltGrave", "???", "Windows Help",
		"WIN_ICO_00", "???", "WIN_ICO_CLEAR", "???", "???", "WIN_OEM_RESET",
		"WIN_OEM_JUMP", "WIN_OEM_PA1", "WIN_OEM_PA2", "WIN_OEM_PA3",
		"WIN_OEM_WSCTRL", "WIN_OEM_CUSEL", "WIN_OEM_ATTN", "WIN_OEM_FINISH",
		"WIN_OEM_COPY", "WIN_OEM_AUTO", "WIN_OEM_ENLW", "WIN_OEM_BACKTAB",
		"ATTN", "CRSEL", "EXSEL", "EREOF", "Play", "Zoom", "???", "PA1",
		"WIN_OEM_CLEAR", ""];

	/* Classes */

	/**
	 * Manages and manipulates the state as sent by the server.
	 */
	var AdminState = function() {
		this.data = false;
		this.stateJSON = JSON.stringify(this.state);
	}; // Prototype methods follow

	AdminState.prototype.fromJSON = function(json) {
		if (typeof json !== "string") return;
		this.setState(JSON.parse(json));
	};

	AdminState.prototype.setState = function(state) {
		this.data = state;
	};

	AdminState.prototype.getCurrentSong = function() {
		return this.data.songs[this.data.currentSong];
	};

	AdminState.prototype.getCurrentMap = function(song) {
		return song.maps[song.currentMap];
	};

	AdminState.prototype.getCurrentSongVerses = function() {
		var verses = [];
		var song = this.getCurrentSong();
		var map = this.getCurrentMap(song);
		for (var i = 0; i < map.verses.length; i++) {
			verses.push(this.getVerseByName(song, map.verses[i]));
		}
		return verses;
	};

	AdminState.prototype.getVerseByName = function(song, verseName) {
		for (var i = 0; i < song.verses.length; i++) {
			if (song.verses[i].name == verseName) {
				return song.verses[i];
			}
		}
	};

	/**
	 * The websocket client class for managing an administrator connection.
	 * @param [callback] A logging callback.
	 */
	var AdminWebSocketClient = function() {
		this.log = console.log.bind(console);
		this.defaultPort = 8417;
		this.expectedServerVersion = "0.6.9";
		this.socket = false;
		this.state = new AdminState();

		window.socketClient = this;

		if (arguments.length >= 1) {
			this.log = arguments[0];
		}

		/**
		 * Disconnect the current socket if connected.
		 * @return {void}
		 */
		this.disconnect = function() {
			if (this.socket != false) {
				if (this.socket.readyState < 2) {
					this.socket.close();
				}
			}
		}

		/**
		 * Initializes the websocket and attempts to connect to the server.
		 * @return {void}
		 */
		this.connect = function() {
			var host = window.location.host.split(":")[0];
			var port = this.defaultPort;
			if (arguments.length >= 1) {
				host = arguments[0];
			}
			if (arguments.length >= 2) {
				port = arguments[1];
			}
			var connString = host + ":" + port.toString() + "/console";
			this.log("Client: Connecting to ws://" + connString + "...");
			this.socket = new WebSocket("ws://" + connString);
			this.addSocketHandlers();
		};

		/**
		 * Add the event listeners for the socket events and our custom message events.
		 *
		 * Changes to this should/will break compatibility.
		 * Cross-reference with socketMessage().
		 */
		this.addSocketHandlers = function() {
			var that = this;

			// Default websocket event handlers
			this.socket.addEventListener('open', function(e) { that.socketOpen(e); });
			this.socket.addEventListener('error', function(e) { that.socketError(e); });
			this.socket.addEventListener('message', function(e) { that.socketMessage(e); });
			this.socket.addEventListener('close', function(e) { that.socketClose(e); });

			// Message-type handlers
			// See socketMessage() for notes on how these are mapped.
			this.socket.addEventListener('consoleMessage', function(e) { that.socketConsoleMessage(e); });
			this.socket.addEventListener('displayMessage', function(e) { that.socketDisplayMessage(e); });
			this.socket.addEventListener('stateMessage', function(e) { that.socketStateMessage(e); });
			this.socket.addEventListener('handshakeMessage', function(e) { that.socketHandshakeMessage(e); });
			this.socket.addEventListener('unknownMessage', function(e) { that.socketUnknownMessage(e); });
		};

		/**
		 * The event handler for socket message events.
		 *
		 * This also re-dispatches predefined events with custom handlers.
		 *
		 * Changes to this should/will break compatibility.
		 * Cross-reference with addSocketHandlers().
		 * @param  {WebSocket.MessageEvent} e The websocket message event object. `e.data` contains the message string.
		 * @return {void}
		 */
		this.socketMessage = function(e) {
			var msg = e.data;

			// See addSocketHandlers() for notes on how these are added as listeners.
			var messageBindMap = [
				["console:", "consoleMessage"],
				["slide:", "displayMessage"],
				["state:", "stateMessage"],
				["LyricScreen server", "handshakeMessage"],
			];

			// Iterate the map
			for (var i = 0; i < messageBindMap.length; i++) {
				var bmi = messageBindMap[i];
				// Matches map "key"
				if (stringStartsWith(msg, bmi[0])) {
					// Dispatch event as described in map
					var args = msg.substring(bmi[0].length).trim();
					var messageEvent = new MessageEvent(bmi[1], {'data': {'original_event': e, 'message': msg, 'args': args}});
					this.socket.dispatchEvent(messageEvent);
					return;
				}
			}

			// All else fails, we dispatch as an unknown message type
			var unknownMessageEvent = new MessageEvent('unknownMessage', {'data': {'original_event': e, 'message': msg}});
			this.socket.dispatchEvent(unknownMessageEvent);
		};

		this.socketConsoleMessage = function(e) {
			// Console messages just get logged
			this.log("Server: " + e.data.args);
		};

		this.socketDisplayMessage = function(e) {
			// TODO: Show the current text
			// setText(e.data.substring(6).trim());
			if (this.onDisplayMessage) {
				this.onDisplayMessage(e);
			}
		};

		this.socketStateMessage = function(e) {
			this.state.fromJSON(e.data.args);
			if (this.onStateChange) {
				this.onStateChange(this.state);
			}
		};

		this.socketHandshakeMessage = function(e) {
			if (e.data.args !== this.expectedServerVersion) {
				this.log("Invalid server version.");
				this.disconnect();
			} else {
				this.sendStateRequest();
			}
		};

		this.socketUnknownMessage = function(e) {
			this.log("Unknown message received: " + e.data.message);
		};

		this.socketOpen = function(e) {
			this.log("Client: Connected.");
		};

		this.sendStateRequest = function() {
			this.send("state");
		};

		this.socketError = function(e) {
			// TODO: Error handling for websocket connections
		};

		this.socketClose = function(e) {
			switch (e.code) {
				case 1006:
					this.log("Client: Failed to connect.");
					break;
				case 1000:
					this.log("Client: Connection closed.");
					break;
			}
		};

		this.send = function(message) {
			if (this.onBeforeSend) {
				this.onBeforeSend(message);
			}
			this.socket.send(message);
		};
	};

	/**
	 * Handles the front-end <-> state synchronization and management.
	 */
	var AdminInterface = function() {
		this.debugConsole = false;
		this.songVerses = false;
		this.freezeButton = false;
		this.blankButton = false;
		this.client = false;
		this.shortcutKeyClicks = false;

		/**
		 * Prepares the interface for use.
		 * @return {void}
		 */
		this.setup = function() {
			this.client = new AdminWebSocketClient();
			this.client.log = this.print.bind(this);
			this.client.onStateChange = this.onStateChange.bind(this);

			this.debugConsole = document.getElementById("debug-console");
			this.songVerses = document.getElementById("song-verses");
			this.freezeButton = document.getElementById("freeze-button");
			this.blankButton = document.getElementById("blank-button");
			this.debugModeToggle = document.getElementById("debug-mode-toggle");
			this.mainMenuButton = document.getElementById("main-menu-button");
			this.mainMenu = document.getElementById("main-menu");

			var that = this;
			window.onbeforeunload = function() {
				that.client.disconnect();
			};

			window.onkeydown = function(e) {
				return that.onKeyDown(e);
			};

			this.bindClickShortcutKeys();
			this.bindMenuItems();
			this.duplicateLabelTitles(); 
      this.bindMainMenuItems();

			this.client.connect();
		};

		this.bindClickShortcutKeys = function() {
			var clickShortcutElements = document.querySelectorAll('[data-click-shortcut-keys]');

			this.shortcutKeyClicks = {};
			for (var i = 0; i < clickShortcutElements.length; i++) {
				var e = clickShortcutElements[i];
				var shortcutData = e.dataset.clickShortcutKeys;
				var shortcuts = shortcutData.split(",");
				e.title += " [";
				for (var j = 0; j < shortcuts.length; j++) {
					var shortcut = shortcuts[j];
					this.shortcutKeyClicks[shortcut.trim()] = e;
					var keyNameCode = "";
					for (var h = shortcut.length; h >= 0; h--) {
						var c = shortcut.charAt(h);
						if (c >= '0' && c <= '9') {
							keyNameCode = c + keyNameCode;
						}
					}
					var shortcutString = shortcut
						.replace("c", "Ctrl+")
						.replace("a", "Alt+")
						.replace("s", "Shift+")
						.replace("m", "Meta+")
						.replace(keyNameCode, keyCodeNames[parseInt(keyNameCode)])
						;
					e.title += shortcutString;
					if (j >= shortcuts.length - 1) {
						break;
					} else {
						e.title += ", ";
					}
				}
				e.title += "]";
			}
		};

		this.bindMenuItems = function() {
			var menuItems = this.mainMenu.querySelectorAll("ul li");
			for (var i = 0; i < menuItems.length; i++) {
				var menuItem = menuItems[i];
				console.log(menuItem);
				menuItem.onClick = function() {
					console.log(this);
					var ele = this.childNodes[0];
					var me = new MouseEvent('click', {
						'view': window,
						'bubbles': true,
						'cancelable': true,
					});
					var result = ele.dispatchEvent(me);
					e.preventDefault();
					return false;
				}
			}
		};

		// NOTE: Run AFTER bindClickShortcutKeys for best UX
		this.duplicateLabelTitles = function() {
			var labels = document.querySelectorAll('label');
			for (var i = 0; i < labels.length; i++) {
				var label = labels[i];
				var target = label.getAttribute('for');
				var targetElement = document.getElementById(target);
				label.setAttribute('title', targetElement.getAttribute('title'));
			}
		};

    this.bindMainMenuItems = function() {
      var mainMenuListItems = this.mainMenu.children[0].children;
      for (var i = 0; i < mainMenuListItems.length; i++) {
        mainMenuListItems[i].addEventListener("click", function(e) {
          for (var j = 0; j < this.children.length; j++) {
            if (this.children[j].tagName == "A" || this.children[j].tagName == "INPUT") {
              if (this == e.target) {
                this.children[j].click();
                break;
              }
            }
          }
        });
      }
    };

		this.onKeyDown = function(e) {
			var key = "" + e.keyCode;
			if (e.metaKey) key = "m" + key;
			if (e.shiftKey) key = "s" + key;
			if (e.altKey) key = "a" + key;
			if (e.ctrlKey) key = "c" + key;
			if (key in this.shortcutKeyClicks) {
				var ele = this.shortcutKeyClicks[key];
				var me = new MouseEvent('click', {
					'view': window,
					'bubbles': true,
					'cancelable': true,
				});
				var result = ele.dispatchEvent(me);
				e.preventDefault();
				return false;
			}
			return true;
		};

		/**
		 * Prints the specified message to our debug console and the development
		 * console.
		 * @param  {string} message Our message string.
		 * @return {void}
		 */
		this.print = function(message) {
			console.log(message);

			var dt = new Date();
			var h = dt.getHours().toString(); if (h.length < 2) h = "0" + h;
			var m = dt.getMinutes().toString(); if (m.length < 2) m = "0" + m;
			var s = dt.getSeconds().toString(); if (s.length < 2) s = "0" + s;
			var timestamp = document.createTextNode(h+":"+m+":"+s+" ");

			var l = document.createElement("li");
				var span = document.createElement("span");
				span.className = "timestamp";
				span.appendChild(timestamp)
			l.appendChild(span)
				var messageNode = document.createTextNode(message.toString());
			l.appendChild(messageNode)

			this.debugConsole.insertBefore(l, this.debugConsole.firstChild);

			while (this.debugConsole.childNodes.length > 100) {
				this.debugConsole.removeChild(this.debugConsole.lastChild);
			}
		};

		this.onStateChange = function(state) {
			var song = state.getCurrentSong();
			for (var si = 0; si < state.data.songs.length; si++) {
				// TODO: Add song switcher
			}

			var scroll = this.songVerses.scrollTop;
			while (this.songVerses.firstChild) {
				this.songVerses.removeChild(this.songVerses.firstChild);
			}

			if (state.data.currentSong > 0) {
				var slide = document.createElement("li");
				slide.className = "basic message-button";
				slide.setAttribute('data-message', "goto song " + (state.data.currentSong - 1));
				var slideText = "Go to Previous Song";
				slide.innerHTML = slideText;
				this.songVerses.appendChild(slide);
			}

			var map = state.getCurrentMap(song);
			var verses = state.getCurrentSongVerses();
			var activeSlide = false;
			for (var vi = 0; vi < verses.length; vi++) {
				var slide = document.createElement("li");
				slide.className = "basic jump-to-verse";
				if (vi == map.currentVerse) {
					slide.className += " active";
					activeSlide = slide;
				}
				slide.setAttribute('data-verse', vi);
				var slideText = "";
				slideText += "<span class=\"verse-name\">" + verses[vi].name + "</span>";
				slideText += verses[vi].content.replace(/\n/g, "<br />")
				slide.innerHTML = slideText;
				this.songVerses.appendChild(slide);
			}
			this.songVerses.scrollTop = scroll;
			if (activeSlide != false) {
				var svr = this.songVerses.getBoundingClientRect();
				var vpmin = this.songVerses.scrollTop;
				var vpmax = vpmin + svr.height;
				var smin = activeSlide.offsetTop;
				var smax = smin + activeSlide.offsetHeight;
				if (smin < vpmin) {
					this.songVerses.scrollTop = smin - 1;
				} else if (smax > vpmax) {
					this.songVerses.scrollTop = (smax - svr.height) + 1;
				}
			}

			if (state.data.currentSong < state.data.songs.length - 1) {
				var slide = document.createElement("li");
				slide.className = "basic message-button";
				slide.setAttribute('data-message', "next song");
				var slideText = "Go to Next Song";
				slide.innerHTML = slideText;
				this.songVerses.appendChild(slide);
			}

			this.updateBlankButton(state);
			this.updateFreezeButton(state);

			this.rebindInterfaceEvents();
		};

		this.updateFreezeButton = function(state) {
			if (state.data.isFrozen) {
				this.freezeButton.innerHTML = "<i class=\"fa fa-play\"></i>";
			} else {
				this.freezeButton.innerHTML = "<i class=\"fa fa-pause\"></i>";
			}
		};

		this.updateBlankButton = function(state) {
			if (state.data.isBlank) {
				this.blankButton.innerHTML = "<i class=\"fa fa-toggle-off\"></i>";
			} else {
				this.blankButton.innerHTML = "<i class=\"fa fa-toggle-on\"></i>";
			}
		};

		this.rebindInterfaceEvents = function() {
			var that = this;
			var verseJumpers = document.getElementsByClassName('jump-to-verse');
			for (var i = 0; i < verseJumpers.length; i++) {
				verseJumpers[i].onclick = function(e) { that.jumpToVerseCallback(e, this); };
			}

			var messageButtons = document.getElementsByClassName('message-button');
			for (var i = 0; i < messageButtons.length; i++) {
				messageButtons[i].onclick = function(e) { that.messageButtonCallback(e, this); };
			}

			this.debugModeToggle.onclick = function(e) {
				that.toggleDebugMode(e, this);
			};

			this.mainMenuButton.onclick = function(e) {
				that.toggleMainMenu(e, this);
			};
		};

		/* Interface Element Callbacks */

		this.toggleDebugMode = function(e, that) {
			if (that.checked) {
				document.body.className = "";
			} else {
				document.body.className = "just-controls";
			}
		};

		this.jumpToVerseCallback = function(e, that) {
			this.client.send("goto verse " + that.dataset.verse);
			e.preventDefault();
			return false;
		};

		this.messageButtonCallback = function(e, that) {
			this.client.send(that.dataset.message);
			e.preventDefault();
			return false;
		};

		this.toggleMainMenu = function(e, that) {
			if (this.mainMenu.style.display == "block") {
				this.mainMenuButton.className = "";
				this.mainMenu.style.display = "none";
			} else {
				this.mainMenuButton.className = "active";
				this.mainMenu.style.display = "block";
			}
		};

		return this;

	};

	var a = new AdminInterface();
	a.setup();

}());
