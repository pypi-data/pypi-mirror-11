var host = top.location.host;
var msnry;
var socket = new WebSocket('ws://' + host + '/socket');
var checkers, categories = [];
var firstLoad = true;

/**
 * Check that the socket is still alive.
 * @constructor
 * @param timeout
 */
function SocketTimer(timeout) {
    this.timeout = timeout;
    this.divId = 'connection-lost-message';
    this.alive = true;
    this.timer = null;
    
    this.timedOut = function () {
        console.log('timed out');
        this.alive = false;
        var container = document.getElementById('status-container');
        if(document.getElementById(this.divId) == null) {
            console.log('div found');
            var div = document.createElement('div');
            div.className = 'alert alert-danger';
            div.role = 'alert';
            div.innerHTML = 'Websocket connection timed out. Try refreshing.';
            div.id = 'connection-lost-message';
            container.appendChild(div);
        }
    };

    this.start = function () {
        console.log('Starting socket timer...');
        this.timer = window.setTimeout(this.timedOut, this.timeout);
    };

    this.keepAlive = function () {
        console.log('Keep alive');
        this.alive = true;
        var div = document.getElementById(this.divId);
        if(div != null) {
            div.parentNode.removeChild(div);
        }
        if(this.timer) {
            window.clearTimeout(this.timer);
            delete this.timer;
        }
        this.start();
    };
}

var timer = new SocketTimer(10000.0);
timer.start();

// Icon drawing macros
// -----------------------------------------------------------------------------

var icon = {
    ok: '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>',
    error: '<span aria-hidden="true" class="glyphicon glyphicon-remove"></span>',
    question: '<span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span>'
};

// Startup
// -----------------------------------------------------------------------------

socket.onopen = function() {
    if(firstLoad) {
        socket.send('info?');
        firstLoad = false;
    }
};

socket.onclose = function() {
};

// Handle incoming messages
// -----------------------------------------------------------------------------

var test;
socket.onmessage = function(msg) {
    var data = JSON.parse(msg.data);
    test = data;

    // Start timing for next message
    timer.keepAlive();

    // First response
    if(data.hasOwnProperty('response') && data.hasOwnProperty('first')) {
        // Get the initial data on the checkers and extract categories.
        checkers = data.checkers;
        for(var prop in checkers) {
            var checker = checkers[prop];
            var category = checker.category;
            if(categories.indexOf(category) == -1) {
                categories.push(category);
            }
        }

        // Create empty divs for each category.
        var container = document.getElementById('status-container');

        var grid = document.createElement('div');
        grid.className = 'grid';
        container.appendChild(grid);
        
        var sizer = document.createElement('div');
        sizer.className = 'grid-sizer';
        grid.appendChild(sizer);
        
        for(prop in categories) {
            category = categories[prop];
            var panel = document.createElement('div');
            panel.id = 'category-' + category; // TODO: lower case and hyphenate category
            panel.className = 'panel panel-default grid-item';
            grid.appendChild(panel);
        }

        // Populate the empty divs.
        for(prop in checkers) {
            checker = checkers[prop];
            var parent = document.getElementById('category-' + checker.category);
            if(parent.innerHTML == '') {
                parent.innerHTML += '<a href="#" class="list-group-item active">' + checker.category + '</a>';
            }
            var item = document.createElement('a');
            item.id = 'status-' + checker.name;
            item.href = '#';
            item.className = 'list-group-item';
            item.innerHTML = icon.question + '&nbsp;' + checker.description;
            parent.appendChild(item);
        }

        // Setup fluid grid boxes
        msnry = new Masonry(document.querySelector('.grid'), {
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer',
            percentPosition: true
        });
    }

    // Status update
    else {
        for(prop in data) {
            var status = data[prop], text, color;
            var element = document.getElementById('status-' + prop);
            if(status) {
                text = icon.ok + '&nbsp;' + checkers[prop].description;
                color = 'list-group-item-success';
            }
            else {
                text = icon.error + '&nbsp;' + checkers[prop].description;
                color = 'list-group-item-danger';
            }
            element.className = 'list-group-item ' + color;
            element.innerHTML = text;
        }
    }
};
