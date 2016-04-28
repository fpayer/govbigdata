'use strict';

var request = require('request');
var cheerio = require('cheerio');
var async = require('async');
var unzip = require('unzip2');
var mkdirp = require('mkdirp');
var Decompress = require('decompress');
var fs = require('fs');
var del = require('delete');
var AdmZip = require('adm-zip');

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
    async.each(process, function(session, c) {
      async.eachSeries(dirs, function(dir, b) {
        var url = BASE + '/' + session + '/' + dir + '/BILLSTATUS-' + session + '-' + dir + '.zip';
        var tmp = '/tmp/' + session + '.zip';
        var out = OUTPUT + session + '/' + dir;

        async.waterfall([
          function(a) {
            mkdirp(out, function(err) {
              a(err);
            });
          },
          function(a) {
            request(url).pipe(fs.createWriteStream(tmp)).on('close', function(err) {
              a();
            });
          },
          function(a) {
            var zip = new AdmZip(tmp);
            zip.extractAllTo(out, true);
            console.log('Decompressed ' + url);
            a();
          },
          function(a) {
            del([tmp], {force:true}, function(err) {
              a(err);
            });
          }
        ], b);
      }, c);
    }, d);
  }
], function(err, data) {
  console.log(err);
  console.log(data);
});


