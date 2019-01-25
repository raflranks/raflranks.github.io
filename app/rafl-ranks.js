/* Init minified.js */
var MINI = require('minified');
var _=MINI._, $=MINI.$, $$=MINI.$$, EE=MINI.EE, HTML=MINI.HTML;


window.onhashchange = function() {
    App.Route();
};


function loadData(uri, callback) {
    $.request('get', uri)
    .then(function(response) {
            console.log('Loaded (' + uri + ')');
            callback(response);
    })
    .error(function(status, statusText, responseText) {
            App.Error('Error[' + status +']: (' + uri + ')');
            callback(null);
    });
}


function getKeyOr(data, key, defaultValue) {
    return key in data ? data[key] : defaultValue;
}


function fixStr(str) {
    return decodeURIComponent(escape(unescape(str)));
}


function sumKeys(data) {
    var total = 0;
    Object.keys(data).forEach(function(key) {
        total += data[key];
    });
    return total;
}


String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}


function riderName(rider) {
    return rider.split('-').map(s => s.capitalize()).join(' ');
}


function auctionId(auction) {
    switch(auction) {
        case 'Red':
            return 'r';
        case 'Blue Tit':
            return 'b';
        case 'Shroom':
            return 'y';
        case 'Bert':
            return 'g';
        default:
            console.error('Unknown auction ' + auction);
            return 0;
    }
}


var App = {
    // scoreKeys: ['Stg', 'GC', 'PC', 'KOM', 'Spr', 'Sum', 'Bky', 'Ass'],
    // riders: null,
    scores: null,
    teams: null,
    riders: null,
    // league: null,
    home: null,

    auctionKeys: {
        'Red': 'r',
        'Blue Tit': 'b',
        'Shroom': 'y',
        'Bert': 'g',
    },
};


$(function() {
    App.Init();
});


(function(app) {
    'use strict';

    app.Init = function() {
        app.home = $('.intro');
        loadData('data/scores.json', function(response) {
            app.scores = $.parseJSON(response);
        });
        loadData('data/teams.json', function(response) {
            app.teams = $.parseJSON(response);
        });
        app.Route();
    };

    app.Route = function() {
        if (location.hash.length > 0) {
            var splitHash = location.hash.split(':');
            switch (splitHash[0]) {
                case '#league':
                    app.Loading();
                    app.League(splitHash[1], splitHash.length>2?splitHash[2]:'total');
                    break;
                case '#rider':
                    app.Loading();
                    app.Ready(function() {
                        app.DisplayRider(fixStr(splitHash[1]));
                    });
                    break;
                case '#riders':
                    app.Loading();
                    app.Ready(function() {
                        app.DisplayRiders(splitHash.length>1?splitHash[1]:'total');
                    });
                    break;
                case '#home':
                    app.Home();
                    break;
            }
        } else {
            location.hash = '#home';
        }
    };

    app.Loading = function() {
        $('#app').fill(EE('div', {$: 'sp-circle'}));
    };

    app.Ready = function(callback) {
        if (app.scores === null || app.teams === null) {
            setTimeout(function() { app.Ready(callback); }, 100);
            return;
        }

        if (app.riders === null) {
            app.prepareRiders();
        }

        callback();
    };

    app.Error = function(error) {
        console.error(error);
    };

    app.Home = function() {
        $('#app').fill(app.home);
    };

    app.prepareRiders = function() {
        console.log('Preparing team scores');

        var totals = app.scores['totals'];
        var riders = {};
        for(var auction in app.teams) {
            var auctionKey = app.auctionKeys[auction];
            for(var n = 0; n < app.teams[auction].length; n++) {
                var team = app.teams[auction][n];
                for(var rider in team['riders']) {
                    if (rider in riders) {
                        riders[rider]['ak'].push(auctionKey);
                    } else {
                        riders[rider] = {
                            'name': riderName(rider),
                            'score': (rider in totals) ? totals[rider] : 0,
                            'ak': [auctionKey],
                        };
                    }
                }
            }
        }

        console.log(riders);

    };

    app.DisplayRiders = function(rider) {

    };

})(App);
