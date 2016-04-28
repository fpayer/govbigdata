'use strict';

var request = require('request');
var cheerio = require('cheerio');
var async = require('async');
var unzip = require('unzip2');
var mkdirp = require('mkdirp');

var BASE = 'https://www.gpo.gov/fdsys/bulkdata/BILLSTATUS';
var OUTPUT = './data/';

var dirs = [ 
  'sres',
  'sjres',
  'sconres',
  's',
  'hres',
  'hr',
  'hjres',
  'hconres'
];

async.waterfall([
  function(d) {
    request(BASE, function(err, response, html) {
      d(err, html);
    });
  },
  function(html, d) {
    var $ = cheerio.load(html);
    var toProcess = [ ];

    $('#bulkdata td a').each(function(i, item) {
      var href = $(item).attr('href');

      if (href) {
        var end = href.split('/').pop();
        if (parseInt(end)) {
          toProcess.push(end);
        }
      }
    });
    d(null, toProcess);
  },
  function(process, d) {
    async.eachSeries(process, function(session, c) {
      async.eachSeries(dirs, function(dir, b) {
        var url = BASE + '/' + session + '/' + dir + '/BILLSTATUS-' + session + '-' + dir + '.zip';
        var out = OUTPUT + session + '/' + dir;

        async.waterfall([
          function(a) {
            mkdirp(out, function(err) {
              a(err);
            });
          },
          function(a) {
            request(url).pipe(unzip.Extract({
              path : out 
            })).on('close', function(err) {
              console.log('Completed scrape of', url);
              a(err);
            }).on('error', function(err) {
              console.log('Error', err, url);
              a(null);
              //a(err);
            });
          }
        ], b);

        /*
        request(url).pipe(unzip.Parse()).on('entry', function(entry) {
          var fileName = entry.path;
          console.log(fileName);
        }).on('error', function(err) {
          console.log('Error', err);
          b(err);
        }).on('exit', function() {
          b(err);
        });
       */

        //b();

        /*
        request(url)
          .pipe(unzip.Parse())
          .on('entry', function(entry) {

          })
          .on('exit', 
        ;
       */
        //b(null, url);
      }, c);
    }, d);
  }
], function(err, data) {
  console.log(err);
  console.log(data);
});


